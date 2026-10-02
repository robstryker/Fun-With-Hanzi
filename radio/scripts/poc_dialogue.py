"""Two-host proof of concept: "One 字 at a Time", episode intro chatter.

Rob = en-US-AndrewMultilingualNeural, Sunshine = zh-CN-XiaoxiaoMultilingualNeural.
One Azure request per line (150 ms gaps around Chinese), joined with ffmpeg.

Run from the project root:  PYTHONPATH=radio/scripts radio/.venv/bin/python radio/scripts/poc_dialogue.py
Writes radio/out/poc/poc_intro.mp3 (and the per-line clips beside it).
"""
import pathlib, subprocess
from azure_voices import creds
from azure_gaps import synth

VOICE = {"Rob": "en-US-AndrewMultilingualNeural",
         "Sunshine": "zh-CN-XiaoxiaoMultilingualNeural"}
TURN_GAP = 0.20  # seconds of silence between speakers

SCRIPT = [
    ("Sunshine", "Welcome back to One 字 at a Time. I'm Sunshine."),
    ("Rob", "And I'm Rob."),
    ("Sunshine", "Before we start on our second character, Rob, you were just telling me "
                 "about why you started this project. Can you go into that a bit for our audience?"),
    ("Rob", "Yeah, Sunshine, definitely. Well, my wife and kids are currently visiting "
            "grandparents in China, and my daughter seems really interested in learning the language."),
    ("Sunshine", "Oh yeah, I know that kind of kid. Just wants to soak it all up, right?"),
    ("Rob", "Yeah, definitely. That's exactly what she's like."),
]

if __name__ == "__main__":
    key, region = creds()
    out = pathlib.Path("radio/out/poc"); out.mkdir(parents=True, exist_ok=True)
    files = []
    for i, (who, text) in enumerate(SCRIPT, 1):
        f = out / f"line{i:02d}-{who}.mp3"
        f.write_bytes(synth(text, VOICE[who], key, region, 150))
        files.append(f)
    args = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in files: args += ["-i", str(f)]
    n = len(files)
    chain = "".join(f"[{i}:a]apad=pad_dur={TURN_GAP}[a{i}];" for i in range(n))
    chain += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]"
    args += ["-filter_complex", chain, "-map", "[o]", str(out / "poc_intro.mp3")]
    subprocess.run(args, check=True)
    print("wrote", out / "poc_intro.mp3", f"({n} lines)")
