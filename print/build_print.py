#!/usr/bin/env python3
"""Build a compact, printable PDF from the generated dictionary XML.

Reads the XML written by FullRunAllBooksWithFragments (one <hanzi> per
character, with its <word> entries and <sentences>), shortens definitions,
applies hand-written glosses from data/glosses.tsv, and lays several
characters out per page.

Usage (from the project root):
    .venv/bin/python print/build_print.py --to 20 --out outputs/sample.pdf
"""

import argparse
import html
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent

# Glosses that carry no meaning on their own, or only point elsewhere.
DROP_GLOSS = re.compile(
    r"^(CL:|see |see also|variant of|old variant|also written|surname|abbr\. for|"
    r"Japanese variant|used in |\(Tw\)|\(archaic\))", re.IGNORECASE)
# Parenthetical labels that are noise for a learner.
DROP_LABEL = re.compile(r"\s*\((idiom|coll\.|dialect|literary|formal|onom\.)\)")
HAN = re.compile(r"^[㐀-鿿豈-﫿]+$")


# ---------------------------------------------------------------- pinyin

TONE_MARKS = {
    "a": "āáǎà", "e": "ēéěè", "i": "īíǐì",
    "o": "ōóǒò", "u": "ūúǔù", "ü": "ǖǘǚǜ",
}


def syllable_to_marks(syl):
    """hao3 -> hǎo, lu:4 -> lǜ, de5 -> de."""
    m = re.match(r"^([a-zü:]+)([1-5])$", syl)
    if not m:
        return syl
    body, tone = m.group(1).replace("u:", "ü").replace("v", "ü"), int(m.group(2))
    if tone == 5:
        return body
    # Standard placement: a or e wins; "ou" marks the o; otherwise the last vowel.
    if "a" in body:
        i = body.index("a")
    elif "e" in body:
        i = body.index("e")
    elif "ou" in body:
        i = body.index("o")
    else:
        i = max(body.rfind(v) for v in "iouü")
        if i < 0:
            return body
    return body[:i] + TONE_MARKS[body[i]][tone - 1] + body[i + 1:]


def pinyin_marks(numbered):
    return " ".join(syllable_to_marks(s) for s in numbered.split())


# ---------------------------------------------------------------- glosses

def load_glosses(path):
    """word<TAB>pinyin<TAB>gloss. Blank pinyin matches every reading;
    a gloss of "-" hides that reading. Lines starting with # are comments."""
    glosses = {}
    if not path.exists():
        return glosses
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("\t")]
        if len(parts) < 3:
            continue
        word, pinyin, gloss = parts[0], parts[1].lower(), parts[2]
        glosses[(word, pinyin)] = gloss
    return glosses


def auto_gloss(desc, budget):
    """Keep the leading meanings of a CC-CEDICT definition, up to budget chars."""
    kept = []
    for g in desc.strip("/").split("/"):
        g = DROP_LABEL.sub("", g.strip())
        if not g or DROP_GLOSS.match(g):
            continue
        if kept and len("; ".join(kept + [g])) > budget:
            break
        kept.append(g)
    return "; ".join(kept)


def gloss_for(word, pinyin, desc, glosses, budget):
    """Returns the gloss to print, or None to hide the entry."""
    manual = glosses.get((word, pinyin), glosses.get((word, "")))
    if manual is not None:
        return None if manual == "-" else manual
    return auto_gloss(desc, budget) or None


# ---------------------------------------------------------------- sentences

EDGE_PUNCT = "\"'“”‘’「」『』《》()（）—–-…….,，、:：; ；"
LATIN = re.compile(r"[A-Za-zＡ-Ｚａ-ｚ]")
REPEAT = re.compile(r"([\u3400-\u9fff])\1\1")


def clean_sentence(text):
    """Trim stray quotes and dangling punctuation; None if not worth showing."""
    text = text.strip().strip(EDGE_PUNCT).strip()
    # "A/B" alternatives (是他们/她们的) are hard for a child to read.
    if not text or LATIN.search(text) or REPEAT.search(text) or "/" in text or "／" in text:
        return None
    if len(re.findall(r"[\u3400-\u9fff]", text)) < 3:
        return None
    return text


def han_only(text):
    return re.sub(r"[^㐀-鿿]", "", text)


def is_complete(text):
    return text[-1] in "。？！.?!"


def load_custom_sentences(path, order, free):
    """Hand-written sentences (data/examples/CUSTOM_EXAMPLES), one per line,
    keyed by the index of the character at which each becomes readable.
    These skip the automatic filters, so short ones like 是？ are allowed."""
    custom = {}
    if not path.exists():
        return custom
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip().strip("\"'“”").strip()
        chars = [c for c in han_only(text) if c not in free]
        if not chars:
            continue
        unknown = [c for c in chars if c not in order]
        if unknown:
            print(f"custom sentence skipped, {''.join(unknown)} not in the order: {text}", file=sys.stderr)
            continue
        custom.setdefault(max(order[c] for c in chars), []).append(text)
    return custom


def load_hidden_sentences(path):
    """Sentences never to show (data/examples/HIDDEN_EXAMPLES), one per line.
    Matched on their Chinese characters only, so punctuation differences don't
    matter. Applies to hand-written sentences too."""
    if not path.exists():
        return set()
    return {han_only(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#") and han_only(line)}


# ---------------------------------------------------------------- model

def load_known(root, known_path, budget):
    """The free mood particles from the XML's <known> section, with the
    hand-written explanations in data/known_chars.tsv (char, pinyin, explanation).
    Dictionary readings are shown only for the pinyin named in that file."""
    notes = {}
    if known_path.exists():
        for line in known_path.read_text(encoding="utf-8").splitlines():
            parts = [p.strip() for p in line.split("\t")]
            if line.strip() and not line.startswith("#") and len(parts) >= 3:
                notes[parts[0]] = (parts[1].lower(), parts[2])
    known = []
    for hanzi in root.findall("known/hanzi"):
        char = hanzi.get("char")
        pinyin, note = notes.get(char, ("", ""))
        readings = [auto_gloss(w.findtext("d"), budget) for w in hanzi.iter("word")
                    if not pinyin or w.findtext("p") == pinyin]
        known.append({"char": char, "pinyin": pinyin_marks(pinyin) if pinyin else "",
                      "note": note, "dictionary": "; ".join(r for r in readings if r)})
    return known


def load_characters(root, custom_path, hidden_path, first, last, glosses, max_words, max_sentences, budget):
    lessons = root.findall("hanzi")  # numbered characters only, not <known>
    order = {h.get("char"): int(h.get("id")) for h in lessons}
    free = {h.get("char") for h in root.findall("known/hanzi")}
    custom = load_custom_sentences(custom_path, order, free)
    hidden = load_hidden_sentences(hidden_path)
    chars = []
    for hanzi in lessons:
        idx = int(hanzi.get("id"))
        if idx < first:
            continue
        if idx > last:
            break
        char = hanzi.get("char")

        words, seen = [], set()
        for w in hanzi.iter("word"):
            modern, pinyin, desc = w.findtext("m"), w.findtext("p"), w.findtext("d")
            if char not in modern or not HAN.match(modern) or (modern, pinyin) in seen:
                continue  # zero-difficulty filler, letters/digits, or a traditional duplicate
            gloss = gloss_for(modern, pinyin, desc, glosses, budget)
            if gloss:
                # Only a shown entry blocks duplicates: "surname Jia" (Jia1, lowercased
                # to jia1 by the Java side) must not hide the real jia1 "home; family".
                seen.add((modern, pinyin))
                words.append({"hanzi": modern, "pinyin": pinyin_marks(pinyin), "gloss": gloss})

        # The character itself heads the block; the rest go shortest-first.
        heads = [w for w in words if w["hanzi"] == char]
        others = sorted((w for w in words if w["hanzi"] != char), key=lambda w: len(w["hanzi"]))

        sentences = sentences_for(hanzi, idx, custom, hidden)
        # With no sentences of its own, point at the next character.
        partner = None
        if not sentences and idx + 1 < len(lessons):
            partner = lessons[idx + 1].get("char"), idx + 2

        chars.append({
            "id": idx, "char": char, "heads": heads,
            "words": others[:max_words],
            "sentences": sentences[:max_sentences],
            "partner": partner,
        })
    return chars


def sentences_for(hanzi, idx, custom, hidden):
    """The sentences shown for one character: hand-written ones first, as written
    (是。 是？ 是！ are all kept), then cleaned-up sentences from the XML."""
    mine = [t for t in dict.fromkeys(custom.get(idx, [])) if han_only(t) not in hidden]
    found, seen_bare = [], {han_only(t) for t in mine}
    for s in hanzi.iter("sent"):
        text = clean_sentence(s.text or "")
        if not text:
            continue
        bare = han_only(text)
        if bare not in seen_bare and bare not in hidden:
            seen_bare.add(bare)
            found.append(text)
    # Whole sentences before fragments, then richer ones (more distinct characters), then shorter.
    found.sort(key=lambda t: (not is_complete(t), -len(set(han_only(t))), len(t)))
    return mine + found


# ---------------------------------------------------------------- render

CSS = """
@page { size: %(paper)s; margin: 12mm 12mm 14mm 12mm;
        @bottom-center { content: counter(page); font-family: "Noto Sans"; font-size: 8pt; color: #888; } }
body { font-family: "Noto Sans", "Droid Sans Fallback"; font-size: 9.5pt; color: #222; margin: 0; }
.char { break-inside: avoid; border-top: 1.2pt solid #333; padding: 2.5mm 0 3mm 0; }
.head { display: flex; align-items: flex-start; gap: 4mm; }
.big { font-size: 30pt; line-height: 1; }
.readings { flex: 1; padding-top: 4.2mm; }
.reading { margin-right: 9mm; }
.py { color: #a33; margin-right: 3mm; }
.num { font-size: 13pt; font-weight: bold; color: #444; padding-top: 3.2mm; }
.words { display: grid; grid-template-columns: 1fr 1fr; column-gap: 6mm; row-gap: 0.6mm; margin-top: 2mm; }
.word { padding-left: 1.2em; text-indent: -1.2em; }
.word .hz { font-size: 12pt; }
.sentences { display: grid; column-gap: 6mm; row-gap: 1.2mm;
             margin-top: 2.5mm; font-size: 12pt; line-height: 1.45; }
.sent { display: flex; gap: 1.5mm; }
.sent .n { color: #999; font-size: 8pt; min-width: 4mm; text-align: right; padding-top: 1.2mm; }
.nosent { margin-top: 2.5mm; font-size: 10pt; font-style: italic; color: #555; }
.intro { break-inside: avoid; border-top: 1.2pt solid #333; border-bottom: 1.2pt solid #333;
         padding: 3mm 0 4mm 0; margin-bottom: 4mm; }
.intro h1 { font-size: 14pt; margin: 0 0 1.5mm 0; }
.intro p { margin: 0 0 3mm 0; font-size: 10pt; }
.known { display: grid; grid-template-columns: 1fr 1fr; column-gap: 8mm; row-gap: 3mm; }
.known .kw { display: flex; gap: 4mm; align-items: flex-start; }
.known .note { font-size: 10pt; }
.known .dict { color: #777; font-size: 8.5pt; margin-top: 0.5mm; }
"""


def esc(s):
    return html.escape(s, quote=False)


def down_columns(n, cols=2):
    """Grid style that fills each column top to bottom before moving to the next."""
    return (f"grid-template-columns: repeat({cols}, 1fr); grid-auto-flow: column; "
            f"grid-template-rows: repeat({-(-n // cols)}, auto);")


SHORT_SENTENCE = 8  # sentences with at most this many Chinese characters go three to a row


def render_known(known):
    cells = []
    for k in known:
        py = f'<span class="py">{esc(k["pinyin"])}</span>' if k["pinyin"] else ""
        cells.append(f'<div class="kw"><span class="big">{esc(k["char"])}</span><div>'
                     f'<div class="note">{py}{esc(k["note"])}</div>'
                     f'<div class="dict">{esc(k["dictionary"])}</div></div></div>')
    return ('<div class="intro"><h1>Before we start: tone words</h1>'
            "<p>These little words don't carry a meaning of their own. They sit at the end of a "
            "sentence and change its tone, the way <i>OK.</i>, <i>OK?</i> and <i>OK!</i> sound "
            "different. They show up all through this book, so we count them as already known.</p>"
            f'<div class="known">{"".join(cells)}</div></div>')


def render_char(c):
    readings = "".join(
        f'<span class="reading"><span class="py">{esc(h["pinyin"])}</span> {esc(h["gloss"])}</span>'
        for h in c["heads"])
    out = [f'<div class="char"><div class="head"><span class="big">{esc(c["char"])}</span>'
           f'<span class="readings">{readings}</span><span class="num">#{c["id"] + 1}</span></div>']
    if c["words"]:
        out.append(f'<div class="words" style="{down_columns(len(c["words"]))}">')
        for w in c["words"]:
            out.append(f'<div class="word"><span class="hz">{esc(w["hanzi"])}</span> '
                       f'<span class="py">{esc(w["pinyin"])}</span> {esc(w["gloss"])}</div>')
        out.append("</div>")
    if c["sentences"]:
        # Shortest first: short ones in three columns, then longer ones in two, numbered straight through.
        ordered = sorted(c["sentences"], key=lambda t: len(han_only(t)))
        short = [t for t in ordered if len(han_only(t)) <= SHORT_SENTENCE]
        long_ = ordered[len(short):]
        n = 1
        for group, cols in ((short, 3), (long_, 2)):
            if not group:
                continue
            out.append(f'<div class="sentences" style="{down_columns(len(group), cols)}">')
            for t in group:
                out.append(f'<div class="sent"><span class="n">{n}</span><span>{esc(t)}</span></div>')
                n += 1
            out.append("</div>")
    else:
        out.append(f'<div class="nosent">{esc(no_sentences_note(c))}</div>')
    out.append("</div>")
    return "\n".join(out)


def no_sentences_note(c):
    """Kid-friendly note for a character that has no sentences yet."""
    if c["partner"]:
        partner, number = c["partner"]
        return (f"No sentences yet! {c['char']} needs a friend. "
                f"You will see it in sentences with {partner} (#{number}).")
    return f"No sentences yet! You will see {c['char']} in sentences soon."


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xml", default=ROOT / "outputs/regenerated.xml", type=Path)
    ap.add_argument("--glosses", default=ROOT / "data/glosses.tsv", type=Path)
    ap.add_argument("--custom", default=ROOT / "data/examples/CUSTOM_EXAMPLES", type=Path,
                    help="hand-written example sentences, one per line")
    ap.add_argument("--hidden", default=ROOT / "data/examples/HIDDEN_EXAMPLES", type=Path,
                    help="example sentences never to show, one per line")
    ap.add_argument("--known", default=ROOT / "data/known_chars.tsv", type=Path,
                    help="explanations for the free tone words shown before #1")
    ap.add_argument("--from", dest="first", type=int, default=1, help="first character number (1-based)")
    ap.add_argument("--to", dest="last", type=int, default=300, help="last character number (1-based)")
    ap.add_argument("--max-words", type=int, default=10)
    ap.add_argument("--max-sentences", type=int, default=100)
    ap.add_argument("--gloss-chars", type=int, default=30, help="length budget for automatic glosses")
    ap.add_argument("--paper", default="A4", help="A4 or Letter")
    ap.add_argument("--out", default=ROOT / "outputs/print.pdf", type=Path)
    ap.add_argument("--html", type=Path, help="also write the intermediate HTML here")
    args = ap.parse_args()

    glosses = load_glosses(args.glosses)
    root = ET.parse(args.xml).getroot()
    intro = render_known(load_known(root, args.known, args.gloss_chars)) if args.first == 1 else ""
    chars = load_characters(root, args.custom, args.hidden, args.first - 1, args.last - 1, glosses,
                            args.max_words, args.max_sentences, args.gloss_chars)
    doc = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><style>'
           + CSS % {"paper": args.paper} + "</style></head><body>"
           + intro + "\n".join(render_char(c) for c in chars) + "</body></html>")
    if args.html:
        args.html.write_text(doc, encoding="utf-8")
    HTML(string=doc).write_pdf(args.out)
    print(f"{len(chars)} characters, {len(glosses)} manual glosses -> {args.out}")


if __name__ == "__main__":
    main()
