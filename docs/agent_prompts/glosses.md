Write short English meanings (glosses) for Chinese words in a children's graded reader. Use only the Read and Write tools; do not explore the project.

Input: /home/rob/rawbeast_bak/code/personal_projects/hanzi/Fun-With-Hanzi/work/glosses_in_{N}.tsv — one word per line, tab-separated: lesson number, word, numbered pinyin, the meaning currently printed, the full CC-CEDICT definition (senses separated by /).

Output: write /home/rob/rawbeast_bak/code/personal_projects/hanzi/Fun-With-Hanzi/work/glosses_out_{N}.tsv with exactly ONE line per input line, same order, three tab-separated fields: word<TAB>numbered pinyin (copied exactly from the input)<TAB>gloss. No header, no comments, nothing else.

Gloss rules:
- Put the meaning a learner most needs FIRST — the most common everyday sense in modern Mandarin, not necessarily the dictionary's first sense. Example: 十分 -> "very; fully" (not "to divide into ten parts"); 很 -> "very"; 看 kan4 -> "to see; to look at; to read".
- If the printed meaning is a company, place or person that happens to share the word (现代 "Hyundai", 和平 "Heping district"), replace it with the ordinary word's meaning ("modern", "peace").
- 1-3 short senses separated by "; ", about 30 characters total at most. Plain words, no dictionary jargon; avoid "sth"/"sb" (write "something"/"someone"). Parentheses only when truly needed (e.g. "(question particle)").
- For grammar words, say what they do briefly, e.g. 的 de5 -> "(shows possession: 's)"; 吗 ma5 -> "(makes a yes/no question)".
- If an entry is an obscure reading or sense a child will essentially never meet (archaic, surname-only, place name, rare technical), write "-" as the gloss to hide it.
- If the current printed meaning is already right and clear, you may keep it as is.
Read the whole input file first, then write the output file once. Finally reply with just the number of lines written and a few examples of glosses you changed most.
