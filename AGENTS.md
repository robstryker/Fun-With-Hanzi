# Agent notes for Fun-With-Hanzi

A graded Chinese reader. Characters are taught one at a time; each one shows
the dictionary words and example sentences that become readable using only
characters taught so far. Rob reads the printed PDF with his daughter (in
China) over video chat, so the audience is a parent and child learning to
read together.

## Pipeline

```
data/commonchar  (teaching order, one char per line)
      │
      ▼  Java: dict.main.FullRunAllBooksWithFragments
outputs/regenerated.xml   (all ~2715 chars: words + corpus sentences, <known> tone words)
      │
      ▼  Python: print/build_print.py   (+ the hand-edited data files below)
outputs/sample.pdf  (quick review, first 60-125 chars, ~15-30 s)
outputs/print.pdf   (first 300 chars, ~3 min -- run in the background)
```

```
mvn -q compile                                                   # once, or after Java edits
java -cp target/classes dict.main.FullRunAllBooksWithFragments > outputs/regenerated.xml
.venv/bin/python print/build_print.py --to 125 --out outputs/sample.pdf
.venv/bin/python print/build_print.py --to 300 --out outputs/print.pdf
mvn test                                                         # 6 legacy JUnit tests
```

The Java run always covers the full order; limit the PDF instead. Run from the
project root (data paths are relative). `.venv` holds WeasyPrint.

## Files

| File | Role |
|---|---|
| `data/commonchar` | Teaching order. **Precious** -- edit only via `print/move_char.py`, only when Rob agrees. |
| `data/cedict_ts.u8` | CC-CEDICT dictionary (CRLF line endings -- keep byte-exact) |
| `data/examples/*` | Corpus sentences (Harry Potter `hpexamples.txt`, nciku `ALL_OUT_CN`, `storychina/`) |
| `data/examples/CUSTOM_EXAMPLES` | Hand-written sentences, one per line. Filed automatically under the character where they become readable; shown first; skip the automatic quality filters. |
| `data/examples/HIDDEN_EXAMPLES` | Sentences never shown. Matched on Chinese characters only (punctuation ignored); also hides custom lines. |
| `data/glosses.tsv` | `word<TAB>pinyin<TAB>meaning` overrides; meaning `-` hides that reading; blank pinyin = all readings |
| `data/hidden_words.txt` | Words never shown in any word list (places, dynasties, people, brands, long technical entries) |
| `data/known_chars.tsv` | Explanations for the free tone words (啊呀呢吧) on the intro page |
| `outputs/tmp.xml`, `tmp.xsl` | Historical 2012 output + browser stylesheet -- keep |

Free tone words come from `StringUtil.getDefaultZeroDifficultyChineseChars()`
and are written to the XML's `<known>` section.

## Tools (print/)

All run from the project root with `.venv/bin/python`, reuse `build_print.py`'s
functions, and follow exactly the same rules as the PDF build.

- **`show_sentences.py A [B]`** -- the sentences the PDF prints for characters
  A..B, numbered, `*` = hand-written, plus every character known before A.
  Read this before writing sentences for a character.
- **`add_sentences.py batch.tsv [--check]`** -- apply a batch of edits:
  `+N<TAB>sentence` adds under #N, `-<TAB>sentence` hides. Every add must land
  exactly at #N (its last-taught character is #N), use only characters in the
  order, and not be hidden; any problem -> nothing written. Always use this,
  never append to the data files by hand.
- **`char_report.py CHAR|N`** -- a character's most-used words (across the whole
  corpus), where each unlocks, and how its later sentences are spread. Use it
  to decide whether a character should move next to its partner. Peaks at
  哈 霍 妮 魔 杖 etc. are Harry Potter names, not real partner words.
- **`move_char.py X --before Y | --after Y | --to N [--regen] [--dry-run]`** --
  move a character in the order; `--regen` reruns Java afterwards. Custom and
  hidden sentences follow their characters automatically.
- **`build_print.py`** -- options `--from/--to`, `--max-words` (10),
  `--max-sentences` (100), `--paper A4|Letter`, `--html FILE`.

## How the PDF chooses what to show

- Words: those used in the shown sentences first (most used first), then the
  rest shortest-first; capped at 10. The character's own readings head the block.
- Sentences: hand-written first, then complete corpus sentences before
  fragments, then more distinct characters, then shorter; capped at 100;
  displayed sorted by length -- up to 8 characters three to a row, longer ones
  two to a row, numbered, filling down the columns.
- A character with no sentences gets a "needs a friend" note naming the next
  character.

## Editing rules Rob has set

- At least 4-5 sentences per character wherever possible; thin ones get 15-25+.
  Prefer complete, slightly longer sentences built on the compounds the
  character unlocks; only a few 3-4 character lines, and only when they clearly
  show a use. No chengyu, dialect, rude or esoteric lines.
- Hide fragments: dangling clauses (但是..., 如果..., 当...的时候), dialogue-tag
  leftovers, dash-broken lines, slash alternatives.
- A character whose main word needs a much later partner can move next to it
  (地→方, 以→可, 作→工, 自→己, 经→已, 无→论, 与→参, 公→平, 民→农). If pushing it down
  would dump 100+ sentences on one character, pull the partner **up** instead
  (果 moved up next to 如). Always ask before reordering.
- Build features literally as Rob describes; verify with the small sample, not
  the 3-minute full build.
- Ask before committing. Work is on branch `maven-layout` (not merged, not pushed).

## Gotchas

- Rob's global git config has `core.autocrlf=input`; CRLF data files
  (`cedict_ts.u8`, `GBK/3.txt`) must be staged byte-exact
  (`git hash-object -w --no-filters` + `git update-index --cacheinfo`) or git
  rewrites them.
- The Java side lowercases pinyin, so surname entries (Jia1) collide with real
  ones (jia1); the builder only lets a *shown* entry block duplicates.
- `IOUtil.readFile` ignores its encoding argument (Test6 reads GBK) -- known,
  unfixed.
