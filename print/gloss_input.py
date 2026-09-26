#!/usr/bin/env python3
"""Build the input for a gloss (word-meaning) pass over characters A..B.

Lists every word the PDF prints for those characters whose automatic meaning
is doubtful -- a sense was trimmed away, or the first sense is a long or
parenthetical note -- and that has no entry in data/glosses.tsv yet. Writes
work/glosses_in_00.tsv, _01, ... (one slice per agent), each line:
lesson number, word, numbered pinyin, current meaning, full CC-CEDICT definition.
Local only, no AI. Feed each slice to an agent with docs/agent_prompts/glosses.md,
then merge with print/merge_glosses.py.

Usage (from the project root):
    .venv/bin/python print/gloss_input.py 251 300 --slices 2
"""

import argparse
import xml.etree.ElementTree as ET

import build_print as b


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("first", type=int)
    ap.add_argument("last", type=int)
    ap.add_argument("--slices", type=int, default=3, help="how many agent slices (default 3)")
    args = ap.parse_args()

    root = ET.parse(b.ROOT / "outputs/regenerated.xml").getroot()
    glosses = b.load_glosses(b.ROOT / "data/glosses.tsv")
    chars = b.load_characters(root, b.ROOT / "data/examples/CUSTOM_EXAMPLES", b.ROOT / "data/examples/HIDDEN_EXAMPLES",
                              args.first - 1, args.last - 1, glosses, 10, 100, 30)
    entries = {}
    for h in root.findall("hanzi"):
        for w in h.iter("word"):
            p = w.findtext("p")
            entries.setdefault((w.findtext("m"), b.pinyin_marks(p)), (p, w.findtext("d")))

    rows, seen, total = [], set(), 0
    for c in chars:
        for w in c["heads"] + c["words"]:
            total += 1
            num, d = entries[(w["hanzi"], w["pinyin"])]
            key = (w["hanzi"], num)
            if key in seen or key in glosses:
                continue
            seen.add(key)
            senses = [s.strip() for s in d.strip("/").split("/") if s.strip()]
            kept = w["gloss"].split("; ")
            dropped = [s for s in senses if s not in kept and not b.DROP_GLOSS.match(s)]
            if dropped or "(" in kept[0] or len(kept[0]) > 20:
                rows.append(f"{c['id'] + 1}\t{w['hanzi']}\t{num}\t{w['gloss']}\t{d}\n")

    out_dir = b.ROOT / "work"
    out_dir.mkdir(exist_ok=True)
    size = -(-len(rows) // args.slices)
    for i in range(args.slices):
        part = rows[i * size:(i + 1) * size]
        (out_dir / f"glosses_in_{i:02d}.tsv").write_text("".join(part), encoding="utf-8")
    print(f"#{args.first}-{args.last}: {total} printed words, {len(rows)} doubtful -> "
          f"work/glosses_in_00..{args.slices - 1:02d}.tsv (~{size} each)")


if __name__ == "__main__":
    main()
