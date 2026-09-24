#!/usr/bin/env python3
"""Show the example sentences the PDF would print for a range of characters.

For each character: its words, then every sentence in print order, numbered,
with * marking hand-written ones (CUSTOM_EXAMPLES). The header line lists
every character already known before the first one shown -- the vocabulary
available when writing new sentences for it.

Usage (from the project root):
    .venv/bin/python print/show_sentences.py 50 56
    .venv/bin/python print/show_sentences.py 57          # just #57
"""

import argparse
import xml.etree.ElementTree as ET

import build_print as b


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("first", type=int, help="first character number (1-based)")
    ap.add_argument("last", type=int, nargs="?", help="last character number (default: same as first)")
    ap.add_argument("--xml", default=b.ROOT / "outputs/regenerated.xml")
    args = ap.parse_args()
    last = args.last or args.first

    root = ET.parse(args.xml).getroot()
    lessons = root.findall("hanzi")
    free = {h.get("char") for h in root.findall("known/hanzi")}
    custom_path = b.ROOT / "data/examples/CUSTOM_EXAMPLES"
    custom = b.load_custom_sentences(custom_path, {h.get("char"): int(h.get("id")) for h in lessons}, free)
    chars = b.load_characters(root, custom_path, b.ROOT / "data/examples/HIDDEN_EXAMPLES",
                              args.first - 1, last - 1, b.load_glosses(b.ROOT / "data/glosses.tsv"),
                              10**6, 10**6, 30)

    print(f"free: {''.join(sorted(free))}   known before #{args.first}: "
          + "".join(h.get("char") for h in lessons[:args.first - 1]))
    for c in chars:
        mine = set(custom.get(c["id"], []))
        print(f"\n#{c['id'] + 1} {c['char']}  words: "
              + ", ".join(f"{w['hanzi']}={w['gloss'][:18]}" for w in c["heads"] + c["words"]))
        for i, s in enumerate(c["sentences"], 1):
            print(f"  {i:2} {'*' if s in mine else ' '} {s}")
        if not c["sentences"]:
            print("  (no sentences)")


if __name__ == "__main__":
    main()
