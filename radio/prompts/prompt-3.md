# Prompt 3 — sentence dive

Part of the per-episode sequence of prompts (see `bible.md`'s Open TODOs,
"Per-episode generation pipeline"). This is the template for the segment that
works through a character's selected example sentences. No intro, no
character introduction or word unlock (prompts 1/2), and no conclusion
(a separate segment).

**Inputs:** the selected sentences, one per line, in
`copy/text/<episode>/zi-N-sentences.txt`, each paired with its PDF number
(`build_print.ordered_sentences` position -- see bible.md's sentence-dive
rules). The selection is made before this prompt runs; this prompt does not
choose sentences.

**Status:** first run 2026-10-02 against Opus 5.5 for s01e01 character #1
(是). Filled-in prompts are saved under `prompts/runs/`. Tags guidance matches
prompt-2's first run, so generated output stays comparable while the
`prompt-tuning-wip.md` patterns accumulate.

**Mechanical checks after a run** (done when converting the transcript to
`zi-N-sentences.yaml`): every pure-Chinese Sunshine turn must equal one of the
selected sentences verbatim, in order, with each selected sentence read
exactly once; each is preceded by an announcement turn naming its PDF number;
zero hanzi or pinyin in any Rob line.

---

```
You are writing one segment of a scripted two-host episode for "One 字
at a Time," a Chinese-learning radio show built from a graded reader.

HOSTS:
- Rob: fictionalized version of the creator, the show's host. He does NOT
  read, pronounce, or repeat any Chinese -- not hanzi, not pinyin/romanized
  syllables -- under any circumstance in this segment. HARD CONSTRAINT: no
  line spoken by Rob may contain a Chinese character or a romanized Chinese
  word. He reasons and translates in English only. He is the host, not a
  co-expert: Sunshine reads each sentence aloud first, and then Rob
  translates it, asks about it, or reacts. He has a prepared translation
  script, so he is not puzzling it out cold -- the comedy/pedagogy is in
  how he gets there, not in whether he's right.
- Sunshine: native Mandarin co-host, the guest expert. She reads every
  target sentence, confirms or corrects Rob's translations, and explains
  when he's puzzled. Early episode -- no hint yet that her realness is
  ambiguous; play her completely straight.

CONTENT RULES: everyday concrete language only; no chengyu, dialect,
swearing, or romance content.

THIS SEGMENT ONLY covers: working through the sentences listed in DATA, in
the order given. Do NOT include a cold open, recap, introduction of the
character or its words, or a closing/conclusion -- those are separate
segments. Start directly with Sunshine moving into the first sentence, and
end after the last sentence is discussed (no sign-off).

SENTENCE FORMAT RULES (hard rules):
- Before reading any sentence, Sunshine names its number as its own short
  turn, e.g. "Sentence 4." Never read a sentence without announcing its
  number first. Use the PDF number given in DATA, not a renumbering.
- The sentence itself is read on its own dedicated turn: Sunshine's turn
  contains ONLY the sentence, in hanzi, exactly as given in DATA, character
  for character with the same punctuation -- no tags, no paraphrase, no
  English, no extra words in that turn.
- Discussion and translation happen on the following turns, never in the
  sentence's own turn.
- Rob translates most sentences himself in English after Sunshine reads
  them; she confirms or adds nuance. Occasionally Sunshine reads a short run
  of sentences back-to-back (each still announced by number, each still on
  its own turn) and translates between them -- use this where stacking them
  makes a point (e.g. the same sentence with different punctuation, or a
  pattern shown across several in a row). Vary the rhythm; don't make every
  sentence the same shape.
- Keep it tight. Sentences that are trivially similar to the one before
  don't need a long discussion.

DATA:
<DATA>

Write the segment as a plain dialogue transcript, "Rob:" / "Sunshine:"
labels, one blank line between turns. Rob and Sunshine's voices are
expressive: put ElevenLabs-style bracket emotion tags inline within turns
where they help, e.g. [warmly] [laughs] [curious] [dryly] [excitedly]
[thoughtfully]. Rob is drier and more restrained, Sunshine more expressive.
Use them sparingly, not on every line. Never put a tag on its own line, and
never put a tag in a turn that is only a Chinese sentence.

Before finalizing, re-check: (1) every Rob line has zero Chinese characters
and zero romanized Chinese words; (2) every sentence turn is exactly one
sentence from DATA, verbatim; (3) every sentence is announced by its number
first, and every sentence from DATA is read exactly once, in order.
Output ONLY the transcript, nothing else.
```

---

## DATA block format

```
- Character #<N>: <char>, pinyin "<pinyin>", <tone>. Meaning: <meaning>.
- Already known: <characters taught before this one, plus the free tone words>.
- Sentences to work through, in this order (PDF number: sentence):
  <number>: <sentence>
  ...
- Notes on words in the sentences: <glosses for anything Rob might translate,
  e.g. the tone-word explanations>
```
