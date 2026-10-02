"""Real-production renderer for ONE SEGMENT of an episode (intro, zi-0000-char,
zi-0001-char, ...) -- text -> per-line audio -> timing manifest -> concatenated
segment mix. Not a whole-episode render: each segment YAML is rendered on its
own, so a segment can be drafted, listened to and re-taken independently.

Reads radio/copy/text/<episode>/<segment>.yaml:
    - speaker: Sunshine
      text: 'Welcome back to One "Zì" at a Time.'
    - speaker: Rob
      text: "And I'm Rob."
Bracket emotion tags (e.g. "[whispers] ...") go directly inline in `text` --
ElevenLabs v4 reads them as part of the string, no separate field needed.

Both hosts render on ElevenLabs v4, per-line (see eleven_creds.py for why:
one request per turn, not the multi-speaker Text-to-Dialogue endpoint --
bundling turns would force a full-scene re-bill on any single-line edit).

Content-addressed clips: a clip's name is derived ONLY from what determines
its sound -- speaker, voice id, model id and the stripped text:
    <Speaker>-<sha1("speaker|voice_id|model_id|text")[:16]>.mp3
There is no line number and no segment prefix in the name, so adding,
removing or reordering lines never renames or re-renders anything; only
lines whose content is new or changed cost credits. Order lives solely in
the manifest, rebuilt from the YAML on every run. Changing a voice or model
changes every hash, so a stale clip can never be served.

For each line, in order:
  1. clip already in audio/<episode>/  -> "cached"
  2. same-named clip anywhere else under radio/ (other episodes' audio
     folders, or anywhere under the radio root; .venv excluded) -> copied in, "reused from <path>" (never re-billed; check
     the notice -- an identical line replaying verbatim in another episode
     can be an unintended repeat)
  3. otherwise synthesized via the with-timestamps endpoint (same price as
     plain TTS) and saved with its alignment.
Each synthesized clip gets a sidecar <name>.json holding the per-character
alignment (character_start/end_times_seconds over the input characters,
bracket tags included at ~0 duration). Clips without a sidecar simply have
no alignment recorded -- the manifest shows `alignment: null` for them.

Edited lines leave their old clips behind in audio/<episode>/ -- harmless
orphans (their hash matches nothing in the current manifest).

Writes (paths are anchored to this script's location, so the cwd doesn't
matter and output never lands in a stray radio/ tree):
    radio/copy/audio/<episode>/<Speaker>-<hash>.mp3     (clips)
    radio/copy/audio/<episode>/<Speaker>-<hash>.json    (alignment sidecars)
    radio/copy/audio/<episode>/<segment>.manifest.json  (timing manifest,
        per bible.md's production note: segment_type, source_id, duration,
        running_start_time -- the single source of truth for later
        sentence-level highlighting, never recompute from the script)
    radio/copy/final/<episode>/<segment>-compiled.mp3   (this segment's mix)

Run:
    radio/.venv/bin/python radio/scripts/render_episode_segment.py s01e01 intro
"""
import base64, hashlib, json, os, pathlib, shutil, subprocess, sys, urllib.error, urllib.request
import yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eleven_creds import creds, MODEL_ID, VOICE

RADIO = pathlib.Path(__file__).resolve().parent.parent
TURN_GAP = 0.20  # seconds of silence between speaker turns

def clip_stem(speaker, text):
    key = f"{speaker}|{VOICE[speaker]}|{MODEL_ID}|{text}"
    return f"{speaker}-{hashlib.sha1(key.encode()).hexdigest()[:16]}"

def synth(text, voice_id, key):
    """One with-timestamps request -> (mp3 bytes, response dict minus audio)."""
    body = json.dumps({"text": text, "model_id": MODEL_ID}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps",
        data=body, method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        resp = json.loads(r.read())
    audio = base64.b64decode(resp.pop("audio_base64"))
    return audio, resp

def find_elsewhere(name, here):
    """First file called `name` anywhere under radio/ outside `here`."""
    for dirpath, dirnames, filenames in os.walk(RADIO):
        dirnames[:] = sorted(d for d in dirnames if d not in (".venv", "__pycache__"))
        if name in filenames and pathlib.Path(dirpath) != here:
            return pathlib.Path(dirpath) / name
    return None

def duration(path):
    """Length in seconds of the audio that actually DECODES from the clip.

    Not ffprobe's format.duration: for these mp3s that figure includes encoder
    padding and runs ~0.03-0.04s longer than the decoded audio, per clip. Summed
    into manifest running_start_time it drifted ~6s over a 170-line episode and
    would misalign any highlighting built on the manifest. So decode to raw
    samples and count them.
    """
    info = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "stream=sample_rate,channels", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip().split(",")
    rate, channels = int(info[0]), int(info[1])
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-"],
        capture_output=True, check=True).stdout
    return len(raw) / (2 * channels) / rate

def main(episode, segment):
    root = RADIO / "copy"
    script_path = root / "text" / episode / f"{segment}.yaml"
    audio_dir = root / "audio" / episode
    final_dir = root / "final" / episode
    audio_dir.mkdir(parents=True, exist_ok=True)
    final_dir.mkdir(parents=True, exist_ok=True)

    if not script_path.exists():
        sys.exit(f"no such segment script: {script_path}")
    turns = yaml.safe_load(script_path.read_text())
    key = creds()

    manifest = []
    t = 0.0
    files = []
    for turn in turns:
        speaker, text = turn["speaker"], turn["text"].strip()
        stem = clip_stem(speaker, text)
        f = audio_dir / f"{stem}.mp3"
        side = audio_dir / f"{stem}.json"
        if f.exists():
            print("cached", f.name)
        else:
            src = find_elsewhere(f.name, audio_dir)
            if src:
                shutil.copy2(src, f)
                if src.with_suffix(".json").exists():
                    shutil.copy2(src.with_suffix(".json"), side)
                print("reused", f.name, "from", src.parent.relative_to(RADIO))
            else:
                try:
                    audio, resp = synth(text, VOICE[speaker], key)
                except urllib.error.HTTPError as e:
                    print("FAILED", f.name, e.code, e.read()[:300])
                    raise
                f.write_bytes(audio)
                side.write_text(json.dumps(
                    {"speaker": speaker, "voice_id": VOICE[speaker],
                     "model_id": MODEL_ID, "text": text, **resp},
                    indent=2, ensure_ascii=False))
                print("wrote ", f.name)
        d = duration(f)
        manifest.append({
            "segment_type": "line", "source_id": f.name, "speaker": speaker,
            "text": text, "duration": d, "running_start_time": t,
            "alignment": side.name if side.exists() else None,
        })
        t += d
        manifest.append({
            "segment_type": "gap", "source_id": None, "duration": TURN_GAP,
            "running_start_time": t,
        })
        t += TURN_GAP
        files.append(f)

    manifest_path = audio_dir / f"{segment}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print("wrote", manifest_path)

    args = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in files: args += ["-i", str(f)]
    n = len(files)
    chain = "".join(f"[{i}:a]apad=pad_dur={TURN_GAP}[a{i}];" for i in range(n))
    chain += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]"
    compiled = final_dir / f"{segment}-compiled.mp3"
    args += ["-filter_complex", chain, "-map", "[o]", str(compiled)]
    subprocess.run(args, check=True)
    print("wrote", compiled, f"({n} lines, {t:.1f}s)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: render_episode_segment.py <episode, e.g. s01e01> "
                 "<segment, e.g. intro | zi-0000-char | zi-0001-char>")
    main(sys.argv[1], sys.argv[2])
