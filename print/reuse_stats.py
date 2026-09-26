#!/usr/bin/env python3
"""Per-character unlock and reuse stats, to find gaps in the order.

For each character #A..#B: how many complete sentences (corpus + hand-written,
minus hidden) land exactly on it ("unlock"), how many the PDF shows, and how many
sentences containing it land on the NEXT 50 / NEXT 150 characters ("reuse") --
i.e. whether the character keeps coming back after it is taught.

Usage: .venv/bin/python print/reuse_stats.py [A B] [--tsv FILE]
"""
import argparse, collections, sys
import xml.etree.ElementTree as ET
import build_print as b

ap = argparse.ArgumentParser()
ap.add_argument("a", type=int, nargs="?", default=1)
ap.add_argument("z", type=int, nargs="?", default=340)
ap.add_argument("--tsv")
ap.add_argument("--batch", action="append", default=[], help="add_sentences batch file(s) whose +N adds are counted as if applied")
ap.add_argument("--short", type=int, nargs=2, metavar=("R50", "R150"), help="list characters below these reuse targets")
ap.add_argument("--only", default="", help="restrict --short output to these characters")
args = ap.parse_args()

root = ET.parse(b.ROOT / "outputs/regenerated.xml").getroot()
lessons = root.findall("hanzi")
order = [h.get("char") for h in lessons]
pos = {c: i + 1 for i, c in enumerate(order)}
free = {h.get("char") for h in root.findall("known/hanzi")}
CUSTOM, HIDDEN = b.ROOT / "data/examples/CUSTOM_EXAMPLES", b.ROOT / "data/examples/HIDDEN_EXAMPLES"
hidden = b.load_hidden_sentences(HIDDEN)

sents = set()
for h in lessons:
    for s in h.iter("sent"):
        t = (s.text or "").strip()
        if t and t[-1] in "。？！?!”" and 6 <= len(b.han_only(t)) <= 25:
            sents.add(t)
sents |= {l.strip() for l in CUSTOM.read_text(encoding="utf-8").splitlines() if l.strip()}
for bf in args.batch:
    for l in open(bf, encoding="utf-8"):
        if l.startswith("+"):
            sents.add(l.split("\t", 1)[1].strip())
seen, land, contains = set(), collections.Counter(), collections.defaultdict(list)
for t in sents:
    key = b.han_only(t)
    if key in seen or key in hidden:
        continue
    seen.add(key)
    cs = {c for c in key if c not in free}
    if not cs or any(c not in pos for c in cs):
        continue
    top = max(pos[c] for c in cs)
    land[top] += 1
    for c in cs:
        contains[c].append(top)

gl = b.load_glosses(b.ROOT / "data/glosses.tsv")
shown = {c["id"] + 1: len(c["sentences"]) for c in
         b.load_characters(root, CUSTOM, HIDDEN, args.a - 1, args.z - 1, gl, 10, 100, 30)}
rows = []
for p in range(args.a, args.z + 1):
    ch = order[p - 1]
    tops = contains[ch]
    r50 = sum(1 for t in tops if p < t <= p + 50)
    r150 = sum(1 for t in tops if p < t <= p + 150)
    rows.append((p, ch, land[p], shown[p], r50, r150))
if args.short:
    t50, t150 = args.short
    for p, ch, u, sh, r50, r150 in rows:
        if (not args.only or ch in args.only) and (r50 < t50 or r150 < t150):
            print(f"#{p}{ch}: reuse50 {r50}/{t50} reuse150 {r150}/{t150}")
    sys.exit(0)
if args.tsv:
    with open(args.tsv, "w", encoding="utf-8") as f:
        f.write("pos\tchar\tunlock\tshown\treuse50\treuse150\n")
        for r in rows:
            f.write("\t".join(map(str, r)) + "\n")
print("complete sentences; unlock = land here, shown = printed in PDF, reuse = contain char, land in next 50/150")
for lo in range(args.a, args.z + 1, 50):
    chunk = [r for r in rows if lo <= r[0] < lo + 50]
    n = len(chunk)
    print(f"#{lo}-{lo+n-1}: avg unlock {sum(r[2] for r in chunk)/n:.0f}, shown {sum(r[3] for r in chunk)/n:.0f}, "
          f"reuse50 {sum(r[4] for r in chunk)/n:.0f}, reuse150 {sum(r[5] for r in chunk)/n:.0f}")
