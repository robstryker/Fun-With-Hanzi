"""Shared ElevenLabs credential/voice constants for the real production pipeline.

Credentials: bare API key, one line, at $ELEVENLABS_CREDS or
~/Documents/codes/eleven.txt. The key is never printed or written into the repo.
"""
import os, pathlib

def creds():
    key = os.environ.get("ELEVENLABS_KEY")
    if not key:
        path = pathlib.Path(os.environ.get("ELEVENLABS_CREDS", "~/Documents/codes/eleven.txt")).expanduser()
        key = path.read_text().strip()
    return key

# Decided 2026-09-28: both hosts on ElevenLabs v4, per-line requests (not the
# multi-speaker Text-to-Dialogue endpoint -- bundling turns into one request
# would force a full-scene re-bill on any single-line edit/re-take).
MODEL_ID = "eleven_v4"
VOICE = {
    "Rob": "uh5qBlKfjqFl7XXhFnJi",       # James - Calm, Clear and Informative
    "Sunshine": "zmcVlqmyk3Jpn5AVYcAL",  # Sapphire - Sweet, Youthful, and Clear
}
