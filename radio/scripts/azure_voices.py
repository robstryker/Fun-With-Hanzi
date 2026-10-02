"""Azure Speech smoke test: mixed English/Mandarin in ONE request (no run-splitting).

Credentials: properties file (key1=..., region=...) at $AZURE_CREDS or
~/Documents/codes/azure.txt; AZURE_SPEECH_KEY / AZURE_SPEECH_REGION override.
The key is never printed or written into the repo.

Run from the project root:  radio/.venv/bin/python radio/scripts/azure_voices.py
Writes radio/out/smoke/azure-<voice>.mp3
"""
import os, pathlib, urllib.request, urllib.error
from xml.sax.saxutils import escape

def creds():
    key, region = os.environ.get("AZURE_SPEECH_KEY"), os.environ.get("AZURE_SPEECH_REGION")
    if not (key and region):
        path = pathlib.Path(os.environ.get("AZURE_CREDS", "~/Documents/codes/azure.txt")).expanduser()
        props = {}
        for line in path.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1); props[k.strip()] = v.strip()
        key, region = key or props["key1"], region or props["region"]
    return key, region

FEMALE = ("Now the character 不. It means 'not'. 我不是老师 -- I am not a teacher. "
          "不是我啊！ means 'It's not me!' and 不是我吧！ means 'It's not me, is it?' "
          "Hear the difference? 你想吃什么？ What do you want to eat?")
MALE = "Okay, so 不 means 'not', and that's our first negative. Let's try one together."

VOICES = {
    "zh-CN-XiaoxiaoMultilingualNeural": FEMALE,
    "zh-CN-XiaoyuMultilingualNeural": FEMALE,
    "en-US-AvaMultilingualNeural": FEMALE,
    "en-US-AndrewMultilingualNeural": MALE,
    "en-US-BrianMultilingualNeural": MALE,
}

def synth(text, voice, key, region):
    ssml = (f"<speak version='1.0' xml:lang='en-US'><voice name='{voice}'>"
            f"{escape(text)}</voice></speak>")
    req = urllib.request.Request(
        f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1",
        data=ssml.encode(), method="POST",
        headers={"Ocp-Apim-Subscription-Key": key,
                 "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3",
                 "User-Agent": "fun-with-hanzi-smoke"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

if __name__ == "__main__":
    key, region = creds()
    out = pathlib.Path("radio/out/smoke"); out.mkdir(parents=True, exist_ok=True)
    for voice, text in VOICES.items():
        try:
            (out / f"azure-{voice}.mp3").write_bytes(synth(text, voice, key, region))
            print("wrote", voice)
        except urllib.error.HTTPError as e:
            print("FAILED", voice, e.code, e.read()[:200])
