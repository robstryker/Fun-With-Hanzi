#!/usr/bin/env python3
"""Report where the sentences shown in the PDF come from.

For every sentence the PDF prints for characters A..B (same selection as
build_print.py), classify its source by searching the corpus files the Java
program reads -- punctuation ignored, since the builder trims it:

    custom      a line in data/examples/CUSTOM_EXAMPLES (hand-written)
    hp          only in data/examples/hpexamples.txt (Harry Potter translation)
    nciku       only in data/examples/ALL_OUT_CN (nciku dictionary examples)
    both        in both corpora
    not-found   in neither (shouldn't happen)

Purely local: reads files on disk, makes no network calls. Useful before any
public release, where long sentences from one copyrighted book are the risk.

Usage (from the project root):
    .venv/bin/python print/source_report.py --to 300
    .venv/bin/python print/source_report.py --from 101 --to 150 --source hp --min-len 13 --list
    .venv/bin/python print/source_report.py --to 1000 --tsv outputs/sources.tsv
"""

import argparse
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import build_print as b

SOURCES = ["custom", "nciku", "hp", "both", "not-found"]


def classify(chars):
    custom = {b.unquote(line)
              for line in (b.ROOT / "data/examples/CUSTOM_EXAMPLES").read_text(encoding="utf-8").splitlines()}
    hp = b.han_only((b.ROOT / "data/examples/hpexamples.txt").read_text(encoding="utf-8", errors="replace"))
    nciku = b.han_only((b.ROOT / "data/examples/ALL_OUT_CN").read_text(encoding="utf-8", errors="replace"))
    rows = []
    for c in chars:
        for s in c["sentences"]:
            bare = b.han_only(s)
            if s in custom:
                src = "custom"
            else:
                in_hp, in_nc = bare in hp, bare in nciku
                src = "both" if in_hp and in_nc else "hp" if in_hp else "nciku" if in_nc else "not-found"
            rows.append({"src": src, "len": len(bare), "num": c["id"] + 1, "char": c["char"], "text": s})
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="first", type=int, default=1, help="first character number (default 1)")
    ap.add_argument("--to", dest="last", type=int, default=300, help="last character number (default 300)")
    ap.add_argument("--source", choices=SOURCES, help="only report this source")
    ap.add_argument("--min-len", type=int, default=0, help="only sentences with at least this many Chinese characters")
    ap.add_argument("--list", action="store_true", help="print every matching sentence")
    ap.add_argument("--bucket", type=int, default=50, help="range size for the by-position table (default 50)")
    ap.add_argument("--tsv", type=Path, help="write all matching rows (source, length, #, char, sentence) here")
    ap.add_argument("--max-sentences", type=int, default=100, help="same cap as build_print.py (default 100)")
    args = ap.parse_args()

    root = ET.parse(b.ROOT / "outputs/regenerated.xml").getroot()
    chars = b.load_characters(root, b.ROOT / "data/examples/CUSTOM_EXAMPLES", b.ROOT / "data/examples/HIDDEN_EXAMPLES",
                              args.first - 1, args.last - 1, b.load_glosses(b.ROOT / "data/glosses.tsv"),
                              10, args.max_sentences, 30)
    rows = classify(chars)
    total = len(rows)
    print(f"sentences shown for #{args.first}-{args.last}: {total}")
    counts = Counter(r["src"] for r in rows)
    for s in SOURCES:
        print(f"  {s:<10} {counts[s]:6}  ({counts[s] / max(total, 1):.0%})")

    sel = [r for r in rows if (not args.source or r["src"] == args.source) and r["len"] >= args.min_len]
    label = f"{args.source or 'all sources'}, {args.min_len}+ characters" if args.min_len else (args.source or "all sources")
    print(f"\nselected ({label}): {len(sel)}")
    if sel:
        print("by length:", "  ".join(f"{lo}-{hi}: {sum(lo <= r['len'] <= hi for r in sel)}"
                                     for lo, hi in [(1, 5), (6, 8), (9, 12), (13, 16), (17, 999)]))
        print("by position:")
        for lo in range(args.first, args.last + 1, args.bucket):
            hi = min(lo + args.bucket - 1, args.last)
            print(f"  #{lo}-{hi}: {sum(lo <= r['num'] <= hi for r in sel)}")
        per = Counter((r["num"], r["char"]) for r in sel)
        print("most affected:", "   ".join(f"#{n} {c}: {k}" for (n, c), k in per.most_common(15)))
    if args.list:
        print()
        for r in sorted(sel, key=lambda r: (r["num"], r["len"])):
            print(f"#{r['num']} {r['char']}\t{r['src']}\t{r['len']}\t{r['text']}")
    if args.tsv:
        args.tsv.write_text("".join(f"{r['src']}\t{r['len']}\t#{r['num']}\t{r['char']}\t{r['text']}\n"
                                    for r in sorted(sel, key=lambda r: (r["num"], r["len"]))), encoding="utf-8")
        print(f"\nwrote {len(sel)} rows to {args.tsv}")


if __name__ == "__main__":
    main()
