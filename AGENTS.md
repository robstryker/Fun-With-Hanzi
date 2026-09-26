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

The PDFs and `outputs/regenerated.xml` are generated and not committed (both
gitignored); regenerate the XML with the Java command after a fresh checkout.
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
  `+N<TAB>sentence` adds under #N, `-<TAB>sentence` hides. An add may land
  at #N or LATER (a good sentence using a later character is kept and filed
  there, with a "filed later" note); landing earlier than #N is an error. Adds
  must use only characters in the order and not be hidden; any problem -> nothing written. Always use this,
  never append to the data files by hand.
  `--check --range A B` also projects each character's resulting sentence count
  (before -> after, fragment rule included) without writing anything -- use it
  to confirm every character reaches 20 before applying.
- **`char_report.py CHAR|N`** -- a character's most-used words (across the whole
  corpus), where each unlocks, and how its later sentences are spread. Use it
  to decide whether a character should move next to its partner. Peaks at
  哈 霍 妮 魔 杖 etc. are Harry Potter names, not real partner words.
- **`move_char.py X --before Y | --after Y | --to N [--regen] [--dry-run]`** --
  move a character in the order; `--regen` reruns Java afterwards. Custom and
  hidden sentences follow their characters automatically.
- **`source_report.py [--from A] [--to B] [--source hp|nciku|custom|both] [--min-len N] [--list] [--tsv FILE]`**
  -- which corpus each sentence shown in the PDF comes from (hand-written,
  Harry Potter translation, nciku), by length and position. Local only. For
  public-release copyright review: long hp-only sentences are the risk.
  #1-1000 takes ~1.5 min.
- **`reuse_stats.py [A B] [--tsv FILE] [--batch FILE] [--short R50 R150 [--only CHARS]]`**
  -- per character: unlock (complete sentences landing on it), shown (printed),
  reuse50/reuse150 (sentences containing it that land on the next 50/150
  characters, i.e. does it keep coming back after being taught). Goal set
  2026-09-26: reuse50 >= 15 and reuse150 >= 40 for #51-340. `--batch` counts a
  batch's adds as applied; `--short` lists characters below target. Takes ~1 min.
- **`gloss_input.py A B [--slices N]`** / **`merge_glosses.py [--keep W P M] [--dry-run]`**
  -- build the input slices for a gloss pass, then validate and append the
  agents' output to data/glosses.tsv (see "Resuming at #251+").
- **`build_print.py`** -- options `--from/--to`, `--max-words` (10),
  `--max-sentences` (100), `--paper A4|Letter`, `--html FILE`.

## Parallel curation with subagents

For big ranges, one subagent per 10 characters writes a batch file to
`work/batches/A-B.tsv` (gitignored) and validates it with
`add_sentences.py work/batches/A-B.tsv --check --range A B` -- agents never
apply batches or edit data/. The main session then reviews each batch and
applies them one at a time, in order.

## Resuming at #251+ (status as of 2026-09-25)

**Done:** #1-250 curated (20+ sentences each, except #16 一 and #39 中) and
glossed (~1,300 hand-checked meanings in data/glosses.tsv). #251+ is raw corpus.

**Steps for the next range, in this order:**
1. `mvn -q compile` and regenerate `outputs/regenerated.xml` if it's missing
   (it's gitignored).
2. **Placement first.** Run `char_report.py` on thin characters in the range
   and decide moves with Rob *before* curating -- a move reshuffles every
   character after it, so curating first means redoing work (白 was pulled up to
   #131 for this reason). Use `move_char.py ... --regen`.
3. **Curate:** one subagent per 10 characters, prompt in
   `docs/agent_prompts/curate.md` (replace {A}/{B}). They write
   `work/batches/A-B.tsv`; they never apply.
4. **Review each batch before applying** (the main session reads every added
   sentence): cut awkward lines and ones the agent itself flags, add hides for
   odd corpus lines it kept. Then apply in order with `add_sentences.py`, and
   back up `CUSTOM_EXAMPLES`/`HIDDEN_EXAMPLES` first.
5. **Gloss:** `gloss_input.py A B --slices N`, one Sonnet agent per slice with
   `docs/agent_prompts/glosses.md` (replace {N}), then `merge_glosses.py
   --dry-run`, decide `--keep` for its "maybe used" list, and merge.
6. Count (every char >= 20), rebuild sample/print PDFs, let Rob check, commit
   (never the PDFs or regenerated.xml).

**Known issues / pitfalls:**
- **Proper-noun collisions (builder bug, unfixed):** the Java side lowercases
  pinyin, so CC-CEDICT proper-noun entries (现代 "Hyundai", 和平 "Heping
  district", 大学 "the Great Learning") collide with the ordinary word and can
  be printed instead. glosses.tsv fixes #1-250 only; the real fix is for the
  builder to prefer the non-proper-noun entry on a collision.
- **Automatic meanings can drop the main sense** (十分 showed "to divide into
  ten parts", 很 lost "very"): CC-CEDICT doesn't order senses by frequency.
  That's what the gloss pass is for -- don't skip it.
- **Heading clutter:** extra readings still print (大 dài "doctor", 着's four
  readings, 看 kān listed before kàn). Hide rare readings in glosses.tsv with "-".
- **Rob can't verify Chinese past ~#100.** Hand-written sentences are the risk;
  corpus grammar is native. Planned but not built: English translations
  (parent edition of the PDF) plus an AI "sounds unnatural?" flag pass, and
  native review by his family via sentence numbers.
- **Agents and usage limits:** a batch file written before a rate limit
  survives -- always re-run `--check --range` on every batch before trusting it.
  Agents' reports can arrive after the task shows "failed".
- **Harry Potter density rises past ~#800** (哈 Harry, 恩 Ron, 邓 Dumbledore hit
  the 100-sentence cap); `source_report.py` measures it.
- **Tokens:** subagents are cheaper than the main session (fresh context);
  use Sonnet for mechanical passes like glossing.
- Sentences are generic examples, not biography -- don't try to make "my
  daughter" lines agree with each other.

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

- **At least 20 sentences per character** except where genuinely not feasible
  (#16 一, #39 中 -- too few characters known; for #1-5 near-duplicates differing
  only in the tone word -- 不是我啊！/不是我吧！ -- are welcome). The builder
  drops corpus fragments once a character has 20+ complete sentences
  (`--min-complete`), so count after the change, not before.
  Prefer complete, slightly longer sentences built on the compounds the
  character unlocks; only a few 3-4 character lines, and only when they clearly
  show a use. No chengyu, dialect, esoteric lines, swearing or insults (去你的,
  下作小人). Everyday words for fighting (他打了我的头) and bodily functions
  (方便一下 = use the bathroom) are NOT to be hidden -- learners should know them.
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

## Reuse pass (2026-09-26)

Method: (1) `reuse_stats.py` flags characters below 15/40; (2) verdict agents
(`docs/agent_prompts/reuse_verdict.md`) judge each KEEP / DEMOTE / FINE on
linguistic grounds; (3) demotions are moved just before their partner with
`move_char.py --before`; (4) KEEP characters get reuse sentences from agents
(`docs/agent_prompts/reuse.md`, 15 chars each) that land inside each
character's window. `add_sentences.py` now accepts a sentence that lands LATER
than its +N (it files there); landing earlier is still an error. A sentence
filed on the character itself does not count toward that character's reuse.
30 characters demoted (政 毛 林 建 立 军 将 度 利 光 制 战 ...), 24 characters
pulled up to #304-340 (怎 孩 友 朋 找 谁 完 办 写 早 钱 校, family/food/colour words).
Remaining: #296-340 block needs curation, then its own reuse wave.
