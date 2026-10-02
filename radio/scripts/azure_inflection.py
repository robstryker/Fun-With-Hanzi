"""Question-inflection variants for "Hear the difference?" (Xiaoxiao Multilingual).

Run from the project root:  radio/.venv/bin/python radio/scripts/azure_inflection.py
Writes radio/out/smoke/infl-<n>-<name>.mp3
"""
import pathlib, urllib.error, urllib.request
from azure_voices import creds

V = "zh-CN-XiaoxiaoMultilingualNeural"
LEAD = "不是我吧！ means 'It's not me, is it?' "
C = lambda txt, end: (f'<prosody contour="(0%,+0%) (55%,+0%) (100%,+{end}%)">{txt}</prosody>')

# name -> SSML body (inside <voice>)
VARIANTS = {
    "baseline-in-context":  f"{LEAD}Hear the difference? 你想吃什么？",
    "alone":                "Hear the difference?",
    "do-you-hear":          "Do you hear the difference?",
    "in-context-do-you":    f"{LEAD}Do you hear the difference? 你想吃什么？",
    "contour-45":           f"{LEAD}Hear the {C('difference?', 45)} 你想吃什么？",
    "contour-80":           f"{LEAD}Hear the {C('difference?', 80)} 你想吃什么？",
    "break-then-chinese":   f"{LEAD}Hear the difference?<break time='300ms'/> 你想吃什么？",
}

def synth(body, key, region):
    ssml = ("<speak version='1.0' xml:lang='en-US' "
            "xmlns:mstts='https://www.w3.org/2001/mstts'>"
            f"<voice name='{V}'>{body}</voice></speak>")
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
    for i, (name, body) in enumerate(VARIANTS.items(), 1):
        try:
            (out / f"infl-{i}-{name}.mp3").write_bytes(synth(body, key, region))
            print("wrote", i, name)
        except urllib.error.HTTPError as e:
            print("FAILED", i, name, e.code, e.read()[:200])
