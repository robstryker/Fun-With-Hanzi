#!/usr/bin/env python3
"""Report where a character earns its place in the order.

For one character: its position, how many sentences it shows now, which of its
words are actually common in the corpus (ranked by how many sentences use them)
and at which character each word becomes readable, plus the later characters
where sentences using it pile up. Use it to decide whether a character should
move next to its main partner.

Usage (from the project root):
    .venv/bin/python print/char_report.py 经
    .venv/bin/python print/char_report.py 97          # by position
    .venv/bin/python print/char_report.py 经 --words 20 --peaks 20
"""

import argparse
import xml.etree.ElementTree as ET

import build_print as b


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("char", help="a character, or its 1-based position")
    ap.add_argument("--words", type=int, default=15, help="how many words to list (default 15)")
    ap.add_argument("--peaks", type=int, default=10, help="how many of the biggest later peaks to list (default 10)")
    ap.add_argument("--xml", default=b.ROOT / "outputs/regenerated.xml")
    args = ap.parse_args()

    root = ET.parse(args.xml).getroot()
    lessons = root.findall("hanzi")
    order = [h.get("char") for h in lessons]
    ch = order[int(args.char) - 1] if args.char.isdigit() else args.char
    if ch not in order:
        raise SystemExit(f"{ch} is not in the order")
    at = order.index(ch)
    raw = [[s.text or "" for s in h.iter("sent")] for h in lessons]

    shown = b.load_characters(root, b.ROOT / "data/examples/CUSTOM_EXAMPLES",
                              b.ROOT / "data/examples/HIDDEN_EXAMPLES", at, at, {}, 10**6, 10**6, 30)[0]
    total = sum(ch in s for sents in raw for s in sents)
    print(f"{ch} is #{at + 1}; shows {len(shown['sentences'])} sentences now "
          f"(corpus sentences with {ch}: {total} across the whole book)")

    # Every dictionary word containing ch is listed under the character where it unlocks.
    words = {}
    for j, h in enumerate(lessons[at:], at):
        for w in h.iter("word"):
            m = w.findtext("m")
            if ch in m and len(m) > 1 and b.HAN.match(m) and m not in words:
                words[m] = j
    usage = {m: sum(m in s for sents in raw for s in sents) for m in words}
    ranked = sorted((m for m in words if usage[m]), key=lambda m: -usage[m])[:args.words]
    print(f"\nmost-used words with {ch} (sentences using it, whole book / unlocks at):")
    for m in ranked:
        j = words[m]
        here = sum(m in s for s in raw[j])
        print(f"  {m:<6} {usage[m]:>5} uses   unlocks at #{j + 1} {order[j]}"
              + ("   <- available now" if j == at else f"   (+{here} sentences there)"))

    later = [(j, sum(ch in s for s in raw[j])) for j in range(at + 1, len(lessons))]
    print(f"\nsentences with {ch} unlocking later, by distance:")
    for lo, hi in ((1, 10), (11, 50), (51, 150), (151, 500), (501, len(lessons))):
        n = sum(k for j, k in later if lo <= j - at <= hi)
        print(f"  next {lo}-{hi}: {n}")
    print(f"biggest later peaks:")
    for j, k in sorted(later, key=lambda t: -t[1])[:args.peaks]:
        print(f"  #{j + 1} {order[j]}: {k}")


if __name__ == "__main__":
    main()
