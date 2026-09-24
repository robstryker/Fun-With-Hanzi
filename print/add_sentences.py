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
    .venv/bin/python print/add_sentences.py batch.tsv           # validate, then apply
"""

import argparse
import sys
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch", type=Path)
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    ap.add_argument("--xml", default=b.ROOT / "outputs/regenerated.xml")
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
