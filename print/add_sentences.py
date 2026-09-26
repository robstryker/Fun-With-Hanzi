#!/usr/bin/env python3
"""Check and apply a batch of example-sentence edits.

A batch file has one edit per line, tab-separated:

    +57<TAB>下学以后，我就回家。     add under character #57
    -<TAB>之后呢?                    hide this sentence

Every added sentence is checked before anything is written:
  - it must land exactly at the given character: its last-taught character
    (ignoring the free tone words) must be that one, so it uses nothing
    that hasn't been taught yet
  - every character in it must be in the order at all
  - it must not be suppressed by HIDDEN_EXAMPLES or by a hide in the batch
Sentences already in CUSTOM_EXAMPLES are skipped. If any check fails,
nothing is written. Adds go to data/examples/CUSTOM_EXAMPLES, hides to
data/examples/HIDDEN_EXAMPLES.

Usage (from the project root):
    .venv/bin/python print/add_sentences.py batch.tsv --check   # validate only
    .venv/bin/python print/add_sentences.py batch.tsv --check --range 161 170
                                                  # ...and project counts for #161-170
    .venv/bin/python print/add_sentences.py batch.tsv           # validate, then apply
"""

import argparse
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import build_print as b

CUSTOM = b.ROOT / "data/examples/CUSTOM_EXAMPLES"
HIDDEN = b.ROOT / "data/examples/HIDDEN_EXAMPLES"


def landing(text, order, free):
    """1-based number of the character a sentence is filed under, or None
    with the characters that aren't in the order at all."""
    chars = [c for c in b.han_only(text) if c not in free]
    unknown = "".join(c for c in chars if c not in order)
    if unknown or not chars:
        return None, unknown
    return max(order[c] for c in chars) + 1, ""


def project(root, order, free, adds, hides, rng):
    """Print each affected character's sentence count before and after the batch,
    exactly as build_print.py would show it (fragment rule included), without
    touching the real data files."""
    nums = {n for n in (landing(t, order, free)[0] for t in adds + hides) if n}
    if rng:
        nums |= set(range(rng[0], rng[1] + 1))
    if not nums:
        return
    first, last = min(nums), max(nums)

    def counts(custom_path, hidden_path):
        chars = b.load_characters(root, custom_path, hidden_path, first - 1, last - 1, {}, 10, 100, 30)
        return {c["id"] + 1: (c["char"], len(c["sentences"])) for c in chars}

    before = counts(CUSTOM, HIDDEN)
    with tempfile.TemporaryDirectory() as tmp:
        tc, th = Path(tmp) / "custom", Path(tmp) / "hidden"
        tc.write_text(CUSTOM.read_text(encoding="utf-8") + "\n" + "\n".join(adds) + "\n", encoding="utf-8")
        th.write_text(HIDDEN.read_text(encoding="utf-8") + "\n" + "\n".join(hides) + "\n", encoding="utf-8")
        after = counts(tc, th)
    print("projected sentence counts (before -> after):")
    print("  " + "   ".join(f"#{n}{after[n][0]} {before[n][1]}->{after[n][1]}" + (" (<20)" if after[n][1] < 20 else "")
                           for n in sorted(nums) if n in after))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch", type=Path)
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    ap.add_argument("--xml", default=b.ROOT / "outputs/regenerated.xml")
    ap.add_argument("--range", type=int, nargs=2, metavar=("A", "B"),
                    help="also project sentence counts for every character #A..#B")
    args = ap.parse_args()

    root = ET.parse(args.xml).getroot()
    order = {h.get("char"): int(h.get("id")) for h in root.findall("hanzi")}
    free = {h.get("char") for h in root.findall("known/hanzi")}
    existing = {b.han_only(line) for line in CUSTOM.read_text(encoding="utf-8").splitlines()}

    adds, hides, problems = [], [], 0
    for n, line in enumerate(args.batch.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        tag, _, text = line.partition("\t")
        text = text.strip()
        if tag == "-":
            hides.append(text)
            continue
        if not tag.startswith("+") or not tag[1:].isdigit() or not text:
            problems += 1
            print(f"line {n}: expected '+N<TAB>sentence' or '-<TAB>sentence': {line}")
            continue
        target = int(tag[1:])
        lands, unknown = landing(text, order, free)
        if lands != target:
            problems += 1
            why = f"uses {unknown}, not in the order" if unknown else f"lands at #{lands}"
            print(f"line {n}: #{target} {why}: {text}")
        elif b.han_only(text) in existing:
            print(f"line {n}: already in CUSTOM_EXAMPLES, skipped: {text}")
        else:
            adds.append(text)

    hidden = b.load_hidden_sentences(HIDDEN) | {b.han_only(h) for h in hides}
    for text in adds:
        if b.han_only(text) in hidden:
            problems += 1
            print(f"would be hidden by HIDDEN_EXAMPLES: {text}")

    print(f"{len(adds)} adds, {len(hides)} hides, {problems} problems")
    project(root, order, free, adds, hides, args.range)
    if problems:
        print("nothing written")
        return 1
    if args.check:
        return 0
    with CUSTOM.open("a", encoding="utf-8") as f:
        f.write("".join(t + "\n" for t in adds))
    with HIDDEN.open("a", encoding="utf-8") as f:
        f.write("".join(t + "\n" for t in hides))
    print("applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
