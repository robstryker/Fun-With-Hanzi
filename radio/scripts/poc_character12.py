"""Two-host proof of concept: "One 字 at a Time", character #12 (们) segment.

Generated via radio/prompts/prompt-2.md against Opus 5.5 (2026-09-28,
post-shape-fix, verified run -- see that file for the prompt and the
zero-hanzi-in-Rob's-lines check). This is the baseline audio pass: same
fixed-gap mechanism as poc_dialogue.py, no filler bank / varied turn gaps
yet (see bible.md's "Naturalness research" -- that tooling isn't built).

Rob = en-US-AndrewMultilingualNeural, Sunshine = zh-CN-XiaoxiaoMultilingualNeural.
One Azure request per line (150 ms gaps around Chinese), joined with ffmpeg.

Run from the project root:  PYTHONPATH=radio/scripts radio/.venv/bin/python radio/scripts/poc_character12.py
Writes radio/out/poc/poc_character12.mp3 (and the per-line clips beside it).
"""
import pathlib, subprocess, time, urllib.error
from azure_voices import creds
from azure_gaps import synth


def synth_with_retry(text, voice, key, region, ms, max_attempts=6):
    """Azure's free/lower tier throttles rapid successive requests (HTTP 429).
    Retry with backoff, honoring Retry-After when the server sends one."""
    for attempt in range(max_attempts):
        try:
            return synth(text, voice, key, region, ms)
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == max_attempts - 1:
                raise
            wait = int(e.headers.get("Retry-After", 0)) or (2 ** attempt)
            print(f"  429, retrying in {wait}s (attempt {attempt + 1})")
            time.sleep(wait)

VOICE = {"Rob": "en-US-AndrewMultilingualNeural",
         "Sunshine": "zh-CN-XiaoxiaoMultilingualNeural"}
TURN_GAP = 0.20  # seconds of silence between speakers

SCRIPT = [
    ("Sunshine", "Character number twelve! This one is 们, \"men,\" and it's neutral "
                 "tone, so it's light and quick with no real pitch of its own. Say it "
                 "softly, almost like a little tail on the word before it."),
    ("Rob", "A tail. So it doesn't get to stand on its own?"),
    ("Sunshine", "Never. 们 isn't a word by itself. It attaches to pronouns and to "
                 "words for people, and it makes them plural. It turns one person "
                 "into a group."),
    ("Rob", "Okay, what does it look like?"),
    ("Sunshine", "On the left there's the person radical, the skinny standing figure "
                 "we've already seen a few times. On the right is 门, which means "
                 "door or gate. It's drawn like a two-leaf door, with a post on each "
                 "side and an opening in the middle. So picture a person standing "
                 "beside a gate."),
    ("Rob", "A person at the gate. And behind that gate are all their friends "
            "waiting to come in."),
    ("Sunshine", "I love that. It's a good way to remember it. One person at the "
                 "door, and 们 lets the whole crowd in."),
    ("Rob", "Great. So what does it unlock?"),
    ("Sunshine", "Six words today. First, 他们."),
    ("Rob", "Okay, the first part is the one you gave me for \"him.\" Add the crowd "
            "and it's a bunch of guys. The guys. The dudes?"),
    ("Sunshine", "Half right. 他们 means \"they\" or \"them.\" It does cover a group "
                 "of males, but it's also the default for any mixed group. Five "
                 "women and one man? Still 他们. And if you don't know who's in the "
                 "group, you use 他们 too."),
    ("Rob", "So it's the general-purpose \"they.\" Got it."),
    ("Sunshine", "Next is 他们的."),
    ("Rob", "That's the same thing plus the little possessive piece at the end. "
            "\"Their.\" Or \"theirs.\""),
    ("Sunshine", "Exactly right. 他们的 is \"their\" or \"theirs.\" Easy one."),
    ("Rob", "I'll take the easy ones. Keep them coming."),
    ("Sunshine", "你们."),
    ("Rob", "\"You,\" and then the gate opens and more of them walk in. So \"you "
            "all.\" Y'all. You guys."),
    ("Sunshine", "Perfect. 你们 is plural \"you.\" Use it when you're talking to "
                 "more than one person. English uses the same \"you\" for one "
                 "person or a whole room, but Chinese makes you choose."),
    ("Rob", "Honestly, English could use that."),
    ("Sunshine", "Now 她们."),
    ("Rob", "Okay, this one has the \"her\" piece in front, so it's a group of "
            "women. But wait, didn't the \"her\" character sound exactly like the "
            "\"him\" one? So how does anyone tell this apart from the first word "
            "when you say it out loud?"),
    ("Sunshine", "They can't! 她们 and 他们 sound exactly the same. The difference "
                 "only shows up in writing. 她们 means \"they\" or \"them\" when the "
                 "group is all female. Out loud, you figure it out from context."),
    ("Rob", "So it's a spelling thing, not a sound thing."),
    ("Sunshine", "Right. Next, 我们."),
    ("Rob", "\"Me,\" plus the crowd. So I'm the one at the gate, and everybody's "
            "with me. \"We.\" \"Us.\""),
    ("Sunshine", "Nailed it. 我们 is \"we\" or \"us.\""),
    ("Rob", "And I'm guessing the last one is that plus the possessive tail."),
    ("Sunshine", "It is. 我们的."),
    ("Rob", "\"Our.\" \"Ours.\""),
    ("Sunshine", "Exactly. 我们的 means \"our\" or \"ours.\" So with one little "
                 "character, we got \"they,\" \"their,\" plural \"you,\" the "
                 "all-female \"they,\" \"we,\" and \"our.\""),
    ("Rob", "Six words from one small tail. Not bad for something that can't stand "
            "on its own."),
]

if __name__ == "__main__":
    key, region = creds()
    out = pathlib.Path("radio/out/poc"); out.mkdir(parents=True, exist_ok=True)
    files = []
    for i, (who, text) in enumerate(SCRIPT, 1):
        f = out / f"char12-line{i:02d}-{who}.mp3"
        f.write_bytes(synth_with_retry(text, VOICE[who], key, region, 150))
        files.append(f)
        time.sleep(0.5)  # avoid tripping the rate limit again
    args = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in files: args += ["-i", str(f)]
    n = len(files)
    chain = "".join(f"[{i}:a]apad=pad_dur={TURN_GAP}[a{i}];" for i in range(n))
    chain += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]"
    args += ["-filter_complex", chain, "-map", "[o]", str(out / "poc_character12.mp3")]
    subprocess.run(args, check=True)
    print("wrote", out / "poc_character12.mp3", f"({n} lines)")
