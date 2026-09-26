You are improving the "reuse ramp" of characters in a graded Chinese reader. Work ONLY on the characters listed in /home/rob/rawbeast_bak/code/personal_projects/hanzi/Fun-With-Hanzi/work/reuse/targets_{K}.tsv . Write your output to two files (nothing else): work/batches/reuse_{K}.tsv (a batch) and work/reuse/report_{K}.md (your recommendations). Do NOT apply anything, do NOT edit data/, do NOT move characters, do NOT commit. Other agents work on other target files in parallel.

## Background
Project root: /home/rob/rawbeast_bak/code/personal_projects/hanzi/Fun-With-Hanzi . Read AGENTS.md first. Run everything from the root with `.venv/bin/python` (ignore warnings). The reader teaches characters one at a time in a fixed order; each sentence is filed under the highest-numbered character it contains, and may use only characters taught up to there. A parent and his young daughter (she lives in China) read it together.

The owner wants every character to KEEP COMING BACK after it is taught. For a character X at position p:
- reuse50  = number of complete sentences containing X that are filed on characters #p+1..#p+50
- reuse150 = same, for #p+1..#p+150
Goal: reuse50 >= 15 and reuse150 >= 40 for every character. Each line of your targets file is one character that currently falls short, with its position, current reuse counts and how many more it needs, its words available now, the words containing it that unlock inside the next 150 characters (with corpus use counts and the character where each unlocks), and its biggest later words.

## Your job, per character
Each character was already judged KEEP in an earlier pass (a good, natural character whose shortfall is due to the novel corpus; the verdict note at the end of its line says why). So your job is (A): write new natural sentences that reuse X inside its window. Only if you discover, while writing, that it truly can't be reused naturally, say so in the report (B) instead of forcing sentences.

(A) Write sentences filed on characters inside X's window (#p+1..#p+150) that naturally contain X -- best built on the compounds that unlock in the window (a compound unlocks at its later character, so a sentence with that compound is filed there or later). A sentence may reuse several needy characters at once; that is welcome and efficient. Use each tool below to place them so they really land inside the window (landing after #p+150 does not help X). Aim to close both gaps: reuse50 >= 15 and reuse150 >= 40. Sentences must be natural modern Mandarin a native speaker would say, roughly 6-15 characters, kid-friendly and everyday (family, daughter, school, food, weather, travel, China/America); varied subjects; no near-duplicates of each other or of existing ones (see `.venv/bin/python print/show_sentences.py A B` for what exists); no chengyu, dialect, swearing, romance/sex, Harry Potter content.

(B) If reaching the goal would need forced, awkward or unnatural sentences -- the character has no everyday compound inside its window, and its real uses are far later or literary/technical -- do NOT write bad sentences. Instead recommend demotion: say where it should move (just before its main partner character, or a specific position), why, and what its best compounds are. Also recommend demotion when the character is simply not useful for a young learner at its position. It is fine, and expected, for some characters to end up as (B) or as partly (A): write what is natural, and say honestly what remains short.

## Tools
- `.venv/bin/python print/show_sentences.py A B` -- current sentences and known characters for #A..#B.
- `.venv/bin/python print/add_sentences.py work/batches/reuse_{K}.tsv --check` -- validates a batch: lines `+N<TAB>sentence` add a sentence intended for #N. A sentence that lands LATER than N is accepted with a "filed later" note (check these notes -- they tell you where it really lands); landing EARLIER than N, or using a character outside the order, is an error. Iterate until 0 problems. Use N = the character you intend it to land on.
- `.venv/bin/python print/reuse_stats.py 51 400 --batch work/batches/reuse_{K}.tsv --short 15 40 --only "<your characters>"` -- shows which of YOUR characters still fall short if your batch were applied (blank output = all goals met). Iterate until as many as honestly possible are met.
- `.venv/bin/python print/char_report.py <char>` -- a character's words and where they unlock.
Batch format: one `+N<TAB>sentence` per line; no hides needed (you may include `-<TAB>sentence` lines only for junk you find).

## Final report (also write it to work/reuse/report_{K}.md, and reply with the same)
For each character: reuse50 / reuse150 before -> after (from the last reuse_stats run), number of sentences you added for it, and either "done" or "demote: <where and why>" or "partly: <what is left and why>". Keep it concise. Confirm the final add_sentences --check showed 0 problems.
