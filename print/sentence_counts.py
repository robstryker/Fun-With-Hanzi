#!/usr/bin/env python3
"""Raw sentence count per character over a range -- no analysis, just the numbers.

Same "shown" count show_sentences.py prints per character, one line each,
with no word lists or sentence text.

Usage (from the project root):
    .venv/bin/python print/sentence_counts.py 400 500
    .venv/bin/python print/sentence_counts.py 57          # just #57
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
    chars = b.load_characters(root, b.ROOT / "data/examples/CUSTOM_EXAMPLES", b.ROOT / "data/examples/HIDDEN_EXAMPLES",
                              args.first - 1, last - 1, b.load_glosses(b.ROOT / "data/glosses.tsv"),
                              10**6, 10**6, 30)
    for c in chars:
        print(f"#{c['id'] + 1} {c['char']}: {len(c['sentences'])}")


if __name__ == "__main__":
    main()
