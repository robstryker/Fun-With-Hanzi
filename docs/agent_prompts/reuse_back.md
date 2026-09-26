You are keeping older characters "alive" inside a newer block of a graded Chinese reader. Work ONLY on the donor characters in /home/rob/rawbeast_bak/code/personal_projects/hanzi/Fun-With-Hanzi/work/reuse/back_targets_{K}.tsv . Write ONE batch file work/batches/back_{K}.tsv and ONE report work/reuse/back_report_{K}.md. Do NOT apply anything, do NOT edit data/, do NOT move characters, do NOT commit. Other agents handle other donor lists in parallel.

## Background
Project root: /home/rob/rawbeast_bak/code/personal_projects/hanzi/Fun-With-Hanzi . Skim AGENTS.md. Run tools from the root with `.venv/bin/python` (ignore warnings). The reader teaches characters in a fixed order; each sentence is filed under the highest-numbered character it contains and may only use characters taught up to there. A parent and his young daughter (she lives in China) read it together.

Characters #351-410 are a new everyday block: 哪 告 诉 帮 兴 怕 病 累 药 苦 医 饿 肉 香 鱼 蛋 茶 甜 汤 洗 床 软 椅 硬 桌 灯 亮 窗 暗 衣 脏 鞋 净 纸 穿 贵 云 雨 湿 雪 春 夏 秋 冬 树 绿 草 蓝 猫 慢 牛 鸡 鸟 耳 嘴 脚 腿 跑 唱 跳. They are already well supplied with sentences of their own. The owner now wants OLDER characters (the "donors", #251-350) to keep appearing in this block, so a learner keeps meeting them after they are taught.

Each line of your targets file is a donor character and how many sentences that land on #351-410 currently contain it. Goal: every donor appears in at least 10 such sentences.

## Your job
For each donor, write NEW natural sentences that (a) contain the donor and (b) LAND on a character in #351-410 (so they must contain at least one block character, and no character taught after #410). A sentence may reuse SEVERAL donors at once, which is efficient. Use the block's words: food, health, home, clothes, weather, seasons, animals, body, plus adjectives and questions. Sentences must be natural modern Mandarin a native speaker would say, roughly 6-15 characters, kid-friendly and everyday, varied subjects and types (statements, questions, requests), no near-duplicates of each other or of existing ones (see `.venv/bin/python print/show_sentences.py A B`), no chengyu, dialect, swearing, romance/sex, Harry Potter content.

Be honest: some donors are abstract or institutional (e.g. 社 术 资 军 队 联 义 科 员) and may have no natural use in food/home/weather/animal/body sentences. For those, do NOT force awkward sentences. Write only what is genuinely natural, stop short of the goal if needed, and say in the report which donors could not reach 10 naturally and why -- that tells the owner they may be candidates for moving later.

## Tools
- `.venv/bin/python print/back_reuse.py 251 350 351 410 --batch work/batches/back_{K}.tsv --short 10 --only "<your donor characters>"` -- lists your donors still below 10 with the batch counted as applied (blank = all met). Iterate.
- `.venv/bin/python print/add_sentences.py work/batches/back_{K}.tsv --check` -- validates the batch: lines `+N<TAB>sentence`, N = the character you intend the sentence to land on (must be in #351-410). Errors if it lands EARLIER than N or uses a character outside the order; a "filed later" note means it landed after N -- check the note, it must still land inside #351-410 to count. Iterate until 0 problems.
- `.venv/bin/python print/char_report.py <char>`, `print/show_sentences.py A B` as needed.

## Final report (also write it to work/reuse/back_report_{K}.md, and reply with the same)
Per donor: count before -> after (from the last back_reuse run), sentences added that contain it, and either "done" or "short: <why not natural>". Confirm the last add_sentences --check showed 0 problems. Keep it concise.
