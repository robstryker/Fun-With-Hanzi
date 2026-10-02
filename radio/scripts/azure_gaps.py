"""Language-switch gaps for Azure: a short <break> on each side of every CJK run.

add_gaps(text, ms) escapes the text and wraps each Chinese run in breaks, so
"Okay, so 不 means 'not'" no longer runs together as "sobu".

Run from the project root:  PYTHONPATH=radio/scripts radio/.venv/bin/python radio/scripts/azure_gaps.py
Writes radio/out/smoke/gap-<ms>-<voice>.mp3 for several gap sizes.
"""
import pathlib, re, urllib.error, urllib.request
from xml.sax.saxutils import escape
from azure_voices import creds, FEMALE, MALE

CJK = "一-鿿　-〿＀-￯"
DEFAULT_GAP_MS = 150  # chosen by ear 2026-09-25 (0/80 ran words together, 250 too long)

def add_gaps(text, ms=DEFAULT_GAP_MS):
    """Escape text, then put <break> before and after each Chinese run."""
    br = f'<break time="{ms}ms"/>'
    return "".join(br + escape(t) + br if i % 2 else escape(t)
                   for i, t in enumerate(RUN_SPLIT.split(text)))

RUN_SPLIT = re.compile(f"([{CJK}]+(?:\\s*[{CJK}]+)*)")

def synth(text, voice, key, region, ms):
    ssml = (f"<speak version='1.0' xml:lang='en-US'><voice name='{voice}'>"
            f"{add_gaps(text, ms)}</voice></speak>")
    req = urllib.request.Request(
        f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1",
        data=ssml.encode(), method="POST",
        headers={"Ocp-Apim-Subscription-Key": key,
                 "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3",
                 "User-Agent": "fun-with-hanzi-smoke"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

VOICES = {"en-US-AndrewMultilingualNeural": MALE,
          "en-US-BrianMultilingualNeural": MALE,
          "zh-CN-XiaoxiaoMultilingualNeural": FEMALE.replace(
              "Hear the difference?", "Do you hear the difference?")}
GAPS = [0, 80, 150, 250]

if __name__ == "__main__":
    key, region = creds()
    out = pathlib.Path("radio/out/smoke"); out.mkdir(parents=True, exist_ok=True)
    for ms in GAPS:
        for voice, text in VOICES.items():
            try:
                (out / f"gap-{ms:03d}-{voice}.mp3").write_bytes(synth(text, voice, key, region, ms))
                print("wrote", ms, voice)
            except urllib.error.HTTPError as e:
                print("FAILED", ms, voice, e.code, e.read()[:200])
