"""Join an episode's rendered segments into one episode mix + one manifest.

Segments are the YAML scripts in radio/copy/text/<episode>/, in this order:
    intro
    zi-NNNN-char, zi-NNNN-words, zi-NNNN-sentences, zi-NNNN-conclusion
        (NNNN ascending; any kind a character doesn't have is simply skipped)
    outro
The 4-digit NNNN is why the filenames sort in teaching order. Segments that
don't exist yet (no outro, no conclusion) are skipped, and the list used is
printed so a missing one is never silent. Files that are not segments
(zi-NNNN-sentences.txt selections, anything else) are ignored.

Reads each segment's timing manifest (audio/<episode>/<segment>.manifest.json,
written by render_episode_segment.py) and its clips -- it never calls the TTS
API and never re-synthesizes anything. Safety check: every segment's manifest
must match its YAML (same speakers/texts, same order); if a YAML was edited
after its last render, assembly stops and names the stale segment, since the
mix would otherwise contain old audio.

Writes (paths anchored to this script's location):
    radio/copy/audio/<episode>/<episode>.manifest.json  merged timing manifest
        (same fields as the segment manifests, plus `segment` on every entry
        and running_start_time offset across the whole episode; gaps carry
        gap_type "turn" or "segment")
    radio/copy/final/<episode>/<episode>-compiled.mp3   the whole-episode mix

Clips are joined directly (one encode, not a re-encode of each segment's
compiled mp3): TURN_GAP after every line (same as the segment renders), plus
SEGMENT_GAP of extra silence after the last line of each segment but the last.

Run:
    radio/.venv/bin/python radio/scripts/assemble_episode.py s01e01
    radio/.venv/bin/python radio/scripts/assemble_episode.py s01e01 --segment-gap 0.8
"""
import argparse, json, pathlib, re, subprocess, sys
import yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from render_episode_segment import TURN_GAP, duration

RADIO = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_SEGMENT_GAP = 0.6  # extra seconds of silence between segments
KIND_ORDER = {"char": 0, "words": 1, "sentences": 2, "conclusion": 3}
ZI = re.compile(r"^zi-(\d{4})-(char|words|sentences|conclusion)$")

def segment_order(name):
    if name == "intro":
        return (0, 0, 0)
    if name == "outro":
        return (2, 0, 0)
    m = ZI.match(name)
    if m:
        return (1, int(m.group(1)), KIND_ORDER[m.group(2)])
    return None

def find_segments(text_dir):
    segs = [p.stem for p in text_dir.glob("*.yaml") if segment_order(p.stem) is not None]
    return sorted(segs, key=segment_order)

def main(episode, segment_gap):
    text_dir = RADIO / "copy" / "text" / episode
    audio_dir = RADIO / "copy" / "audio" / episode
    final_dir = RADIO / "copy" / "final" / episode
    segs = find_segments(text_dir)
    if not segs:
        sys.exit(f"no segment YAMLs found in {text_dir}")
    print("segments:", " > ".join(segs))

    # load + verify every segment before building anything
    loaded = []
    for seg in segs:
        mpath = audio_dir / f"{seg}.manifest.json"
        if not mpath.exists():
            sys.exit(f"{seg}: not rendered yet (no {mpath.name}); run render_episode_segment.py {episode} {seg}")
        lines = [e for e in json.loads(mpath.read_text()) if e["segment_type"] == "line"]
        want = [(t["speaker"], t["text"].strip()) for t in yaml.safe_load((text_dir / f"{seg}.yaml").read_text())]
        have = [(e["speaker"], e["text"]) for e in lines]
        if want != have:
            sys.exit(f"{seg}: YAML differs from its last render (edited since?); re-render it: "
                     f"render_episode_segment.py {episode} {seg}")
        for e in lines:
            if not (audio_dir / e["source_id"]).exists():
                sys.exit(f"{seg}: missing clip {e['source_id']}")
        loaded.append((seg, lines))

    manifest, files, t = [], [], 0.0
    pads = []
    for si, (seg, lines) in enumerate(loaded):
        for li, e in enumerate(lines):
            f = audio_dir / e["source_id"]
            d = duration(f)
            manifest.append({**{k: e[k] for k in ("segment_type", "source_id", "speaker", "text")},
                             "segment": seg, "duration": d, "running_start_time": t,
                             "alignment": e.get("alignment")})
            t += d
            manifest.append({"segment_type": "gap", "gap_type": "turn", "segment": seg, "source_id": None,
                             "duration": TURN_GAP, "running_start_time": t})
            t += TURN_GAP
            pad = TURN_GAP
            if li == len(lines) - 1 and si < len(loaded) - 1:
                manifest.append({"segment_type": "gap", "gap_type": "segment", "segment": seg, "source_id": None,
                                 "duration": segment_gap, "running_start_time": t})
                t += segment_gap
                pad += segment_gap
            files.append(f)
            pads.append(pad)

    mpath = audio_dir / f"{episode}.manifest.json"
    mpath.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print("wrote", mpath)

    final_dir.mkdir(parents=True, exist_ok=True)
    out = final_dir / f"{episode}-compiled.mp3"
    n = len(files)
    args = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in files:
        args += ["-i", str(f)]
    chain = "".join(f"[{i}:a]apad=pad_dur={pads[i]}[a{i}];" for i in range(n))
    chain += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]"
    args += ["-filter_complex", chain, "-map", "[o]", str(out)]
    subprocess.run(args, check=True)
    actual = duration(out)
    print("wrote", out, f"({n} lines, {len(segs)} segments, manifest {t:.1f}s, file {actual:.1f}s)")
    if abs(actual - t) > 1.0:
        print(f"WARNING: file length differs from manifest by {abs(actual - t):.2f}s", file=sys.stderr)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Join an episode's rendered segments into one mix + manifest.")
    ap.add_argument("episode", help="e.g. s01e01")
    ap.add_argument("--segment-gap", type=float, default=DEFAULT_SEGMENT_GAP,
                    help=f"extra silence between segments in seconds (default {DEFAULT_SEGMENT_GAP})")
    a = ap.parse_args()
    main(a.episode, a.segment_gap)
