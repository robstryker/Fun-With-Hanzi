#!/usr/bin/env python3
"""Validate agent gloss output and append it to data/glosses.tsv.

Pairs work/glosses_in_NN.tsv with work/glosses_out_NN.tsv: every output line
must match its input line's word and pinyin, in order, with a non-empty gloss.
Anything wrong -> nothing written.

Before merging, review the "hidden but maybe used" list it prints: multi-character
words the agent hid ("-") that appear in their character's shown sentences.
Give those a short meaning with --keep WORD PINYIN MEANING (repeatable) instead
of hiding them. (Don't trust a plain text match for single characters -- a
character's rare reading always "appears" in its own sentences.)

Usage (from the project root):
    .venv/bin/python print/merge_glosses.py --dry-run
    .venv/bin/python print/merge_glosses.py --keep 北大 "bei3 da4" "Peking University" --label "#251-300"
"""

import argparse
import datetime
import xml.etree.ElementTree as ET

import build_print as b


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keep", nargs=3, action="append", default=[], metavar=("WORD", "PINYIN", "MEANING"))
    ap.add_argument("--label", default="", help="range label for the comment line, e.g. '#251-300'")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    work = b.ROOT / "work"
    ins, outs, problems = [], [], []
    for inp in sorted(work.glob("glosses_in_*.tsv")):
        outp = work / inp.name.replace("_in_", "_out_")
        i = [l.split("\t") for l in inp.read_text(encoding="utf-8").splitlines() if l.strip()]
        o = [l.split("\t") for l in outp.read_text(encoding="utf-8").splitlines() if l.strip()] if outp.exists() else []
        if len(i) != len(o):
            problems.append(f"{outp.name}: {len(i)} in, {len(o)} out")
        for a, z in zip(i, o):
            if len(z) != 3 or z[0] != a[1] or z[1] != a[2] or not z[2].strip():
                problems.append(f"{outp.name}: {a[1]} {a[2]} -> {z}")
        ins += i
        outs += o
    print(f"{len(ins)} in, {len(outs)} out, {len(problems)} problems")
    for p in problems[:20]:
        print("  ", p)
    if problems:
        return 1

    keep = {(w, p): m for w, p, m in args.keep}
    root = ET.parse(b.ROOT / "outputs/regenerated.xml").getroot()
    nums = sorted({int(a[0]) for a in ins})
    chars = {c["id"] + 1: c for c in b.load_characters(
        root, b.ROOT / "data/examples/CUSTOM_EXAMPLES", b.ROOT / "data/examples/HIDDEN_EXAMPLES",
        nums[0] - 1, nums[-1] - 1, {}, 10, 100, 30)}
    review = [(a[1], a[2]) for a, z in zip(ins, outs)
              if z[2].strip() == "-" and len(a[1]) > 1 and (a[1], a[2]) not in keep
              and any(a[1] in s for s in chars[int(a[0])]["sentences"])]
    print("hidden but maybe used in sentences (consider --keep):", review or "none")

    merged = [(a[1], a[2], keep.get((a[1], a[2]), z[2].strip())) for a, z in zip(ins, outs)]
    print(f"{len(merged)} entries, {sum(g == '-' for _, _, g in merged)} hidden")
    if args.dry_run:
        return 0
    path = b.ROOT / "data/glosses.tsv"
    header = f"\n# Drafted {datetime.date.today()} {args.label} by AI (most common meaning first; '-' hides).\n"
    path.write_text(path.read_text(encoding="utf-8").rstrip("\n") + "\n" + header
                    + "".join(f"{w}\t{p}\t{g}\n" for w, p, g in merged), encoding="utf-8")
    print(f"appended to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
