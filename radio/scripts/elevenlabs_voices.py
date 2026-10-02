"""ElevenLabs v4 smoke test: mixed English/Mandarin in ONE request, plain vs.
tagged (emotion/delivery bracket tags), for comparison against the existing
Azure clips (azure_voices.py).

Credentials: bare API key, one line, at $ELEVENLABS_CREDS or
~/Documents/codes/eleven.txt. The key is never printed or written into the
repo.

Run from the project root:  radio/.venv/bin/python radio/scripts/elevenlabs_voices.py
Writes radio/out/smoke/el-<voice>-<variant>.mp3
"""
import os, pathlib, urllib.request, urllib.error, json

def creds():
    key = os.environ.get("ELEVENLABS_KEY")
    if not key:
        path = pathlib.Path(os.environ.get("ELEVENLABS_CREDS", "~/Documents/codes/eleven.txt")).expanduser()
        key = path.read_text().strip()
    return key

# same base line as azure_voices.py's FEMALE, for direct comparison
PLAIN = ("Now the character 不. It means 'not'. 我不是老师 -- I am not a teacher. "
         "不是我啊！ means 'It's not me!' and 不是我吧！ means 'It's not me, is it?' "
         "Hear the difference? 你想吃什么？")

TAGGED = ("[curious] Now the character 不. It means 'not'. "
          "[whispers] 我不是老师 [normal] -- I am not a teacher. "
          "[laughs] 不是我啊！ means 'It's not me!' "
          "[hesitates] and 不是我吧！ means 'It's not me, is it?' "
          "[excited] Hear the difference? 你想吃什么？")

VOICES = {
    "Sarah": "EXAVITQu4vr4xnSDxMaL",
    "Alice": "Xb7hH8MSUJpSbSDYk0k2",
}

VARIANTS = {"plain": PLAIN, "tagged": TAGGED}

def synth(text, voice_id, key):
    body = json.dumps({
        "text": text,
        "model_id": "eleven_v4",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=body, method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

if __name__ == "__main__":
    key = creds()
    out = pathlib.Path("radio/out/smoke"); out.mkdir(parents=True, exist_ok=True)
    for vname, vid in VOICES.items():
        for variant, text in VARIANTS.items():
            try:
                audio = synth(text, vid, key)
                (out / f"el-{vname}-{variant}.mp3").write_bytes(audio)
                print("wrote", vname, variant, f"({len(audio)} bytes)")
            except urllib.error.HTTPError as e:
                print("FAILED", vname, variant, e.code, e.read()[:300])
