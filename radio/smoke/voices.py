"""Mixed English/Mandarin clip through candidate voices (edge-tts), v2.

Each line is split into runs by script (CJK vs. Latin); every run is
synthesized separately and the runs are joined with a short silence. This fixes
two v1 problems: English/Chinese words running together ("sobu means not") and
the service garbling long mixed strings (repeated phrases).

Run from the project root:  radio/.venv/bin/python radio/smoke/voices.py
Writes radio/out/smoke/<voice>.mp3 -- listen and compare.
"""
import asyncio, pathlib, re, subprocess, edge_tts

GAP = 0.12  # seconds of silence between runs

FEMALE = ("Now the character 不. It means 'not'. 我不是老师 -- I am not a teacher. "
          "不是我啊！ means 'It's not me!' and 不是我吧！ means 'It's not me, is it?' "
          "Hear the difference? 你想吃什么？ What do you want to eat?")
MALE = "Okay, so 不 means 'not', and that's our first negative. Let's try one together."

VOICES = {
    "zh-CN-XiaoxiaoNeural": FEMALE,
    "zh-CN-XiaoyiNeural": FEMALE,
    "en-US-AvaMultilingualNeural": FEMALE,
    "en-US-EmmaMultilingualNeural": FEMALE,
    "en-US-AndrewMultilingualNeural": MALE,
    "en-US-BrianMultilingualNeural": MALE,
}
out = pathlib.Path("radio/out/smoke"); out.mkdir(parents=True, exist_ok=True)

# a CJK run includes its own punctuation and any spaces inside it
CJK = r"[一-鿿　-〿＀-￯]"
RUN = re.compile(rf"{CJK}+(?:\s*{CJK}+)*|[^一-鿿　-〿＀-￯]+")

def runs(text):
    # drop leading punctuation/dashes (the service rejects some as "no audio")
    return [re.sub(r"^[\s.,;:\-\u2013\u2014]+", "", r) for r in RUN.findall(text)
            if re.search(r"\w", r)]

async def synth(text, voice, path):
    for attempt in range(3):
        try:
            return await edge_tts.Communicate(text, voice).save(str(path))
        except edge_tts.exceptions.NoAudioReceived:
            if attempt == 2:
                raise ValueError(f"{voice} produced no audio for {text!r}")

async def render(voice, text):
    tmp = out / f"_{voice}"; tmp.mkdir(exist_ok=True)
    parts = runs(text)
    files = []
    for i, p in enumerate(parts):
        f = tmp / f"{i:03d}.mp3"
        await synth(p, voice, f)
        files.append(f)
    # concat with silence between runs, via ffmpeg filter graph
    args = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in files: args += ["-i", str(f)]
    n = len(files)
    chain = "".join(f"[{i}:a]apad=pad_dur={GAP}[a{i}];" for i in range(n))
    chain += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]"
    args += ["-filter_complex", chain, "-map", "[o]", str(out / f"{voice}.mp3")]
    subprocess.run(args, check=True)
    for f in files: f.unlink()
    tmp.rmdir()
    print("wrote", voice, f"({n} runs)")

async def main():
    for v, text in VOICES.items():
        await render(v, text)
asyncio.run(main())
