#!/usr/bin/env python3
"""Write targets_K.tsv files for the reuse pass (see docs/agent_prompts/reuse_verdict.md).

One line per character in #A..#B that is below the reuse targets: position, char,
current reuse50/reuse150 with shortfall, words available now, words unlocking inside
the next 150 places (corpus uses, unlocking character), and the biggest later words.

Usage (project root): .venv/bin/python print/reuse_targets.py A B [--per N] [--out DIR]
Writes DIR/targets_1.tsv, targets_2.tsv ... (N characters each, default 12, DIR work/reuse).
"""
import argparse, collections
import xml.etree.ElementTree as ET
import build_print as b

ap = argparse.ArgumentParser()
ap.add_argument("a", type=int)
ap.add_argument("z", type=int)
ap.add_argument("--per", type=int, default=12)
ap.add_argument("--out", default=str(b.ROOT / "work/reuse"))
ap.add_argument("--r50", type=int, default=15)
ap.add_argument("--r150", type=int, default=40)
ap.add_argument("--forward", type=int, nargs=2, metavar=("LO", "HI"), help="only count sentences landing on #LO..#HI; list only chars that can still be helped from there, with the needed counts")
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
seen, contains = set(), collections.defaultdict(list)
for t in sents:
    key = b.han_only(t)
    if key in seen or key in hidden:
        continue
    seen.add(key)
    cs = {c for c in key if c not in free}
    if not cs or any(c not in pos for c in cs):
        continue
    top = max(pos[c] for c in cs)
    for c in cs:
        contains[c].append(top)

raw = [[s.text or "" for s in h.iter("sent")] for h in lessons]
# every dictionary word, under the character where it unlocks
word_at = {}
for j, h in enumerate(lessons):
    for w in h.iter("word"):
        m = w.findtext("m")
        if len(m) > 1 and b.HAN.match(m) and m not in word_at:
            word_at[m] = j

rows = []
for p in range(args.a, args.z + 1):
    ch = order[p - 1]
    tops = contains[ch]
    r50 = sum(1 for t in tops if p < t <= p + 50)
    r150 = sum(1 for t in tops if p < t <= p + 150)
    if args.forward:
        LO, HI = args.forward
        lo, hi = max(LO, p + 1), min(HI, p + 150)
        need150 = max(0, args.r150 - r150) if lo <= hi else 0
        need50 = max(0, args.r50 - r50) if p + 50 >= LO else 0
        if need150 == 0 and need50 == 0:
            continue
    elif r50 >= args.r50 and r150 >= args.r150:
        continue
    at = p - 1
    ws = {m: j for m, j in word_at.items() if ch in m}
    use = {m: sum(m in s for ss in raw for s in ss) for m in ws}
    now = [m for m, j in ws.items() if j <= at]
    win = sorted((m for m, j in ws.items() if at < j <= at + 150 and use[m]), key=lambda m: -use[m])[:12]
    late = sorted((m for m, j in ws.items() if j > at + 150 and use[m]), key=lambda m: -use[m])[:6]
    fmt = lambda m: f"{m}({use[m]} uses, unlocks #{ws[m] + 1}{order[ws[m]]})"
    rows.append("\t".join([
        f"#{p}", ch,
        (f"reuse50 {r50}/{args.r50} (need +{need50} landing on #{max(LO, p + 1)}-#{p + 50})" if args.forward else f"reuse50 {r50}/{args.r50} (short {max(0, args.r50 - r50)})"),
        (f"reuse150 {r150}/{args.r150} (need +{need150} landing on #{lo}-#{hi})" if args.forward else f"reuse150 {r150}/{args.r150} (short {max(0, args.r150 - r150)})"),
        "available now: " + (" ".join(now[:10]) or "-"),
        "unlock in window: " + (", ".join(fmt(m) for m in win) or "-"),
        "later: " + (", ".join(fmt(m) for m in late) or "-"),
    ]))

import pathlib
out = pathlib.Path(args.out)
out.mkdir(parents=True, exist_ok=True)
for k in range(0, len(rows), args.per):
    f = out / f"targets_{k // args.per + 1}.tsv"
    f.write_text("\n".join(rows[k:k + args.per]) + "\n", encoding="utf-8")
    print(f, len(rows[k:k + args.per]))
print(len(rows), "characters")
