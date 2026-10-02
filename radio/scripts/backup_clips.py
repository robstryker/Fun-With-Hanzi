"""Back up every rendered clip (and its alignment sidecar) to a flat folder.

Copies each content-addressed clip -- <Speaker>-<hash>.mp3 and its
<Speaker>-<hash>.json sidecar -- from radio/copy/audio/<episode>/ into one
flat backup directory, keeping the hash filename and NOT the episode folder
hierarchy. A clip's name is derived from its speaker/voice/model/text (see
render_episode_segment.py), so the same name means the same audio: the
flat layout can't mix up different clips, and it dedupes identical lines
across episodes for free.

Never overwrites or deletes. A file already in the backup is skipped (same
size) or reported as a CONFLICT (different size -- should never happen) and
left untouched. Segment manifests (<segment>.manifest.json) and anything not
matching the clip naming (e.g. old-scheme clips, orphans from before the
content-addressed rename) are not backed up; manifests live in git, and the
skipped count is printed so nothing is silently ignored.

Run:
    radio/.venv/bin/python radio/scripts/backup_clips.py
    radio/.venv/bin/python radio/scripts/backup_clips.py /some/other/dir
"""
import pathlib, re, shutil, sys

RADIO = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_DEST = pathlib.Path("/data/education/learnChinese/radio")
CLIP = re.compile(r"^(Rob|Sunshine)-[0-9a-f]{16}\.(mp3|json)$")

def main(dest):
    if not dest.is_dir():
        sys.exit(f"backup folder does not exist: {dest}")
    copied = present = skipped = conflicts = 0
    for src in sorted((RADIO / "copy" / "audio").glob("*/*")):
        if not src.is_file():
            continue
        if not CLIP.match(src.name):
            skipped += 1
            print("skipped (not a clip name):", src.relative_to(RADIO))
            continue
        out = dest / src.name
        if out.exists():
            if out.stat().st_size == src.stat().st_size:
                present += 1
            else:
                conflicts += 1
                print("CONFLICT (size differs, left untouched):", src.relative_to(RADIO))
            continue
        shutil.copy2(src, out)
        copied += 1
        print("copied", src.name)
    print(f"done: {copied} copied, {present} already present, "
          f"{skipped} skipped, {conflicts} conflicts -> {dest}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit("usage: backup_clips.py [backup dir]")
    main(pathlib.Path(sys.argv[1]) if len(sys.argv) == 2 else DEFAULT_DEST)
