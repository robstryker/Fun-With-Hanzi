You are giving a linguistic VERDICT on characters in a graded Chinese reader that fall short on "reuse". Work ONLY on the characters listed in /home/rob/rawbeast_bak/code/personal_projects/hanzi/Fun-With-Hanzi/work/reuse/targets_{K}.tsv . Write ONE output file: work/reuse/verdict_{K}.tsv . Do NOT write sentence batches, do NOT edit anything under data/, do NOT move characters, do NOT commit. Other agents handle other target files in parallel.

## Background
Project root: /home/rob/rawbeast_bak/code/personal_projects/hanzi/Fun-With-Hanzi . Read AGENTS.md first (skim; you need the pipeline idea only). Run tools from the root with `.venv/bin/python` (ignore warnings). The reader teaches characters one at a time in a fixed order (data/commonchar, ~2,700 characters ranked by corpus frequency -- a corpus of novels, Harry Potter and stories). Each sentence is filed under the highest-numbered character it contains and may use only characters taught up to there. A parent and his young daughter (she lives in China) read it together over video.

The owner wants every character to KEEP COMING BACK after it is taught. For a character X at position p, reuse50 / reuse150 = number of complete sentences containing X that are filed on characters #p+1..#p+50 / #p+1..#p+150. Target: reuse50 >= 15 and reuse150 >= 40. Each line of your targets file is a character below target, with its position, current counts and shortfall, its words available now, the words containing it that unlock inside its 150-place window (corpus use counts, and the character where each unlocks), and its biggest later words.

The stat is a blunt tool: the corpus is novels, so some good everyday characters look weak only because the corpus doesn't happen to reuse them, while others are genuinely literary or narrow. The owner wants each character judged on a LINGUISTIC level.

## Verdict for each character
- **KEEP**: a good, useful character with plenty of natural everyday uses in its window (compounds that unlock there, or natural grammar patterns using only characters known by then). Its shortfall is only the nature of the corpus, so new hand-written sentences can bring it to target without sounding forced. Say what the uses are.
- **DEMOTE**: it truly has little natural reuse at its position: its real uses are literary, technical, political or narrow, or its everyday compounds only unlock much later. Recommend a new position: usually "just before <partner char> (#N)" where its main partner unlocks, or a position number. Also demote when the character just isn't useful to a young learner this early even if a few sentences could be forced. Do not pick a position more than ~200 places from where it is now unless its partner is there.
- **FINE**: the stat undercounts it (e.g. it has strong compounds that will unlock steadily, or it is a core grammar word) and it needs nothing beyond what exists. Say why.

Be decisive and honest: a demotion recommendation is as valuable as a keep. If natural reuse would require awkward sentences, that is a DEMOTE, not a KEEP. Judge as a native speaker teaching a child, not by the numbers alone.

## Proof for KEEP
For every KEEP, write 3 example sentences that reuse X naturally and would land INSIDE its window, and check them: put them in a scratch file work/reuse/scratch_{K}.tsv (lines `+N<TAB>sentence`, N = the character you intend each to land on) and run `.venv/bin/python print/add_sentences.py work/reuse/scratch_{K}.tsv --check` -- it errors if a sentence lands EARLIER than N or uses a character not in the order, and prints a "filed later" note if it lands later than N (read these notes: the sentence must land within #p+1..#p+150 to count). Fix until 0 problems. Sentences: natural modern Mandarin, 6-15 characters, kid-friendly and everyday. These are samples only; they will not be applied.

Useful tools: `.venv/bin/python print/char_report.py <char>` (words and where they unlock); `.venv/bin/python print/show_sentences.py A B` (existing sentences and known characters for #A..#B).

## Output
work/reuse/verdict_{K}.tsv, one line per target character, tab-separated, in the same order, no header:
`#pos<TAB>char<TAB>KEEP|DEMOTE|FINE<TAB>where (for DEMOTE only: e.g. "before 治 #382"; else "-")<TAB>reason and main uses (one or two sentences)<TAB>sample sentences separated by " | " (KEEP only; else "-")`
Then reply with a short summary: counts of KEEP / DEMOTE / FINE, the list of DEMOTEs with destinations, and anything you are unsure about. Confirm the scratch check showed 0 problems.
