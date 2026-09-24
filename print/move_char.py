#!/usr/bin/env python3
"""Move a character to a new place in the teaching order (data/commonchar).

Exactly one destination:
    --before X    directly before character X (e.g. 民 --before 农)
    --after X     directly after character X  (e.g. 果 --after 如)
    --to N        so that it ends up at position N (1-based)

The order file is rewritten byte-for-byte apart from the moved line. With
--regen the Java program is rerun afterwards so outputs/regenerated.xml
matches the new order (needs `mvn compile` to have been run once).
Hand-written and hidden sentences need no changes: they are filed by
content, so they follow their characters automatically.

Usage (from the project root):
    .venv/bin/python print/move_char.py 民 --before 农 --dry-run
    .venv/bin/python print/move_char.py 民 --before 农 --regen
    .venv/bin/python print/move_char.py 主 --to 94 --regen
"""

import argparse
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORDER = ROOT / "data/commonchar"
XML = ROOT / "outputs/regenerated.xml"


def show(lines, i, label):
    lo, hi = max(0, i - 2), min(len(lines), i + 3)
    print(f"{label}: " + "  ".join(f"#{j + 1}{lines[j]}" for j in range(lo, hi) if lines[j]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("char")
    dest = ap.add_mutually_exclusive_group(required=True)
    dest.add_argument("--before")
    dest.add_argument("--after")
    dest.add_argument("--to", type=int)
    ap.add_argument("--dry-run", action="store_true", help="show the result without writing")
    ap.add_argument("--regen", action="store_true", help="regenerate outputs/regenerated.xml afterwards")
    ap.add_argument("--order", type=Path, default=ORDER)
    args = ap.parse_args()

    # Keep line endings exactly as they are; only the moved line changes place.
    lines = args.order.read_bytes().decode("utf-8").split("\n")
    for c in [args.char, args.before, args.after]:
        if c is not None and c not in lines:
            sys.exit(f"{c} is not in {args.order}")
    if args.char in (args.before, args.after):
        sys.exit("a character can't move relative to itself")

    old = lines.index(args.char)
    show(lines, old, f"before: {args.char} at #{old + 1}")
    del lines[old]
    if args.before:
        new = lines.index(args.before)
    elif args.after:
        new = lines.index(args.after) + 1
    else:
        new = args.to - 1
        if not 0 <= new <= len([l for l in lines if l]):
            sys.exit(f"--to must be between 1 and {len([l for l in lines if l]) + 1}")
    lines.insert(new, args.char)
    show(lines, new, f"after:  {args.char} at #{new + 1}")
    if old == new:
        print("no change")
        return
    lo, hi, way = (old + 1, new, "up") if new > old else (new + 2, old + 1, "down")
    print(f"the characters now at #{lo}" + (f"-#{hi}" if hi > lo else "") + f" moved {way} one")

    if args.dry_run:
        print("dry run: nothing written")
        return
    args.order.write_bytes("\n".join(lines).encode("utf-8"))
    print(f"wrote {args.order}")

    if args.regen:
        with XML.open("wb") as out:
            r = subprocess.run(["java", "-cp", str(ROOT / "target/classes"),
                                "dict.main.FullRunAllBooksWithFragments", str(args.order)],
                               cwd=ROOT, stdout=out, stderr=subprocess.DEVNULL)
        if r.returncode:
            sys.exit(f"Java run failed (exit {r.returncode}); outputs/regenerated.xml may be incomplete")
        lessons = ET.parse(XML).getroot().findall("hanzi")
        at = [h.get("char") for h in lessons].index(args.char)
        print(f"regenerated {XML.relative_to(ROOT)}: {len(lessons)} characters, {args.char} at #{at + 1}")


if __name__ == "__main__":
    main()
