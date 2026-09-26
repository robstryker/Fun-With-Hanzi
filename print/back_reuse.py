#!/usr/bin/env python3
"""Backward reuse: how often do characters #A..#B appear in sentences that land on #LO..#HI?

Use it to keep older characters alive inside a newer block. Sentences = complete corpus
sentences + CUSTOM_EXAMPLES, minus hidden.

Usage: .venv/bin/python print/back_reuse.py A B LO HI [--batch FILE ...] [--short N [--only CHARS]]
  --batch  count a batch file's +N adds as if applied
  --short  list only characters with fewer than N such sentences (with their counts)
"""
import sys, collections, argparse
sys.path.insert(0,'print')
import xml.etree.ElementTree as ET
import build_print as b
root=ET.parse('outputs/regenerated.xml').getroot()
L=root.findall('hanzi'); order=[h.get('char') for h in L]
pos={c:i+1 for i,c in enumerate(order)}
free={h.get('char') for h in root.findall('known/hanzi')}
CUSTOM=b.ROOT/"data/examples/CUSTOM_EXAMPLES"; HIDDEN=b.ROOT/"data/examples/HIDDEN_EXAMPLES"
hidden=b.load_hidden_sentences(HIDDEN)
sents=set()
for h in L:
    for s in h.iter('sent'):
        t=(s.text or '').strip()
        if t and t[-1] in '。？！?!”' and 6<=len(b.han_only(t))<=25: sents.add(t)
sents|={l.strip() for l in CUSTOM.read_text(encoding='utf-8').splitlines() if l.strip()}
ap=argparse.ArgumentParser(); ap.add_argument('a',type=int); ap.add_argument('b',type=int); ap.add_argument('lo',type=int); ap.add_argument('hi',type=int)
ap.add_argument('--batch',action='append',default=[]); ap.add_argument('--short',type=int); ap.add_argument('--only',default='')
args=ap.parse_args(); A,B,Lo,Hi=args.a,args.b,args.lo,args.hi
for bf in args.batch:
    for l in open(bf,encoding='utf-8'):
        if l.startswith('+'): sents.add(l.split('\t',1)[1].strip())
cnt=collections.Counter(); seen=set()
for t in sents:
    k=b.han_only(t)
    if k in seen or k in hidden: continue
    seen.add(k)
    cs={c for c in k if c not in free}
    if not cs or any(c not in pos for c in cs): continue
    top=max(pos[c] for c in cs)
    if Lo<=top<=Hi:
        for c in cs:
            if A<=pos[c]<=B: cnt[c]+=1
rows=[(pos[c],c,cnt[c]) for c in order[A-1:B]]
if args.short:
    for p,c,n in rows:
        if n<args.short and (not args.only or c in args.only): print(f'#{p}{c}: {n}/{args.short}')
    sys.exit(0)
vals=sorted(r[2] for r in rows)
print(f'donor chars #{A}-{B}: sentences landing on #{Lo}-{Hi} that contain them')
print('min',vals[0],'p10',vals[len(vals)//10],'p25',vals[len(vals)//4],'median',vals[len(vals)//2],'p75',vals[3*len(vals)//4],'max',vals[-1])
for th in (3,5,8,10,15):
    print(f'  chars with < {th}: {sum(1 for r in rows if r[2]<th)} of {len(rows)}')
print(' '.join(f'#{p}{c}({n})' for p,c,n in rows if n<5))
