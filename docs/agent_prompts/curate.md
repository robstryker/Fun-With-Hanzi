You are curating example sentences for a graded Chinese reader. Work ONLY on characters #{A} through #{B}. Write your proposed edits to ONE file: /home/rob/rawbeast_bak/code/personal_projects/hanzi/Fun-With-Hanzi/work/batches/{A}-{B}.tsv . Do NOT apply anything, do NOT edit any file under data/, do NOT run build_print.py, do NOT move characters, do NOT commit. Other agents are working on other ranges in parallel; your range is independent.

## Context
Project root: /home/rob/rawbeast_bak/code/personal_projects/hanzi/Fun-With-Hanzi . Read its AGENTS.md first. Run everything from the project root with `.venv/bin/python` (ignore WeasyPrint/VORG warnings). The reader teaches characters one at a time in a fixed order; each character shows sentences readable with only characters taught so far. A parent and his young daughter (she lives in China; he is American) read it together over video chat — sentences about family, a daughter, learning Chinese, school, America/China, everyday life fit well. Sentences are generic examples, not biography; they don't need to agree with each other.

Sentences are filed AUTOMATICALLY under the character where they become readable (the highest-numbered character they contain; the tone words 啊呀呢吧 are free). You don't place them; you only propose them.

## Tools
- `.venv/bin/python print/show_sentences.py {A} {B}` — current sentences per character (numbered, * = hand-written), each character's words, and the header lists every character known before #{A}. Chinese in your sentences may only use characters known up to the target character (plus 啊呀呢吧).
- `.venv/bin/python print/add_sentences.py work/batches/{A}-{B}.tsv --check --range {A} {B}` — validates your batch and PROJECTS the resulting sentence count per character (before -> after). It writes nothing. Iterate until it reports 0 problems.
- Optional: `.venv/bin/python print/char_report.py <char>` shows a character's most-used words and where they unlock.

## Batch file format (tab-separated, one edit per line)
`+N<TAB>sentence` = add a hand-written sentence intended for character #N (the checker verifies it really lands at #N, i.e. N is its highest-numbered character).
`-<TAB>sentence` = hide an existing corpus sentence (copy it exactly as shown by show_sentences; matching ignores punctuation).

## Goals and rules (from the project owner)
1. Every character #{A}-{B} must end up with AT LEAST 20 sentences per the projection. If one is genuinely impossible (almost no natural sentence can be formed with the known characters), get as close as honest Chinese allows and explain why in your final report.
2. Hide junk: fragments that trail off or don't demonstrate the character (dangling 但是…/如果…/当…的时候/…之前 clauses), dialogue-tag leftovers (…”他说。), dash-broken lines, slash alternatives, chengyu/idioms (four-character set phrases), dialect, archaic/literary phrasing, math/number junk, obvious Harry Potter content (names, "master" house-elf lines, Minister of Magic 部长 lines, Dobby 多比), swearing and insults (去你的, 下作小人), romance/sex/pregnancy lines. Once a character has 20+ complete sentences, the builder automatically stops showing corpus fragments, so you mainly need to hide junk among COMPLETE sentences (ending in 。？！ etc.).
3. DO NOT hide everyday words for fighting (他打了我的头) or bodily functions (方便一下 = use the bathroom) — the owner wants learners to know them.
4. New sentences: natural modern Mandarin a native speaker would say; mostly complete sentences of moderate length (roughly 6-15 characters) built on the compound words each character unlocks, with only a few 3-4 character lines and only when they clearly show a use. Prefer useful, concrete, kid-friendly content. Vary subjects (我/你/他/她/我们/他们/我的女儿/我的儿子/同学…). No near-duplicates of each other or of existing sentences.
5. Think about what each character is actually used for (its common compounds) and cover those uses.

## Final report (your final message)
For each character: its count before -> after (from the projection), what you hid and why (briefly), the main words/patterns your new sentences cover, and anything you could not do or are unsure about. Keep it concise. Confirm the final --check output showed 0 problems.
