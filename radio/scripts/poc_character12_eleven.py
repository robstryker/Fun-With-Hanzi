"""Character #12 (们) segment, Sunshine re-synthesized on ElevenLabs v4 (Sapphire),
Rob left untouched on Azure -- comparison test.

Reuses poc_character12.py's SCRIPT verbatim. Rob's lines are NOT re-synthesized;
this script reuses the existing char12-lineNN-Rob.mp3 files already sitting in
radio/out/poc/ (Azure Andrew). Only Sunshine's 16 lines are regenerated, on
ElevenLabs, and -- per the 2026-09-28 test showing Sapphire handles mixed
English/Mandarin much more dynamically unsplit -- sent as ONE plain-text
request per line, no CJK-run segmentation and no <break> insertion (that
splitting mechanism is Azure/SSML-specific; it doesn't apply here at all).

Requires: radio/out/poc/char12-lineNN-Rob.mp3 already exist (from
poc_character12.py). If any are missing, this script fails loudly rather
than silently re-billing Azure for them.

Run from the project root:  PYTHONPATH=radio/scripts radio/.venv/bin/python radio/scripts/poc_character12_eleven.py
Writes radio/out/poc/char12-lineNN-Sunshine-eleven.mp3 (new, old Sunshine
Azure clips untouched) and radio/out/poc/poc_character12_eleven.mp3 (full mix).
"""
import pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from elevenlabs_voices import creds
from poc_character12 import SCRIPT
import urllib.request

SAPPHIRE = "zmcVlqmyk3Jpn5AVYcAL"
TURN_GAP = 0.20  # seconds, matches poc_character12.py

def synth(text, key):
    import json
    body = json.dumps({"text": text, "model_id": "eleven_v4"}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{SAPPHIRE}",
        data=body, method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

if __name__ == "__main__":
    key = creds()
    out = pathlib.Path("radio/out/poc")
    files = []
    for i, (who, text) in enumerate(SCRIPT, 1):
        if who == "Rob":
            f = out / f"char12-line{i:02d}-Rob.mp3"
            if not f.exists():
                raise FileNotFoundError(f"{f} missing -- run poc_character12.py first")
        else:
            f = out / f"char12-line{i:02d}-Sunshine-eleven.mp3"
            f.write_bytes(synth(text, key))
            print("wrote", f)
        files.append(f)
    args = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in files: args += ["-i", str(f)]
    n = len(files)
    chain = "".join(f"[{i}:a]apad=pad_dur={TURN_GAP}[a{i}];" for i in range(n))
    chain += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]"
    args += ["-filter_complex", chain, "-map", "[o]", str(out / "poc_character12_eleven.mp3")]
    subprocess.run(args, check=True)
    print("wrote", out / "poc_character12_eleven.mp3", f"({n} lines, 16 re-synthesized)")
