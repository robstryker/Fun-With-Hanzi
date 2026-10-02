# Prompt tuning -- work in progress

Rob edits each generated script after it's committed; the git diff against
the generated version shows his preferences. This file accumulates what those
edits show, **one script at a time**, so we can see which patterns repeat
before changing any prompt. Nothing here is applied to a prompt yet.

**Rule of thumb:** a pattern needs to show up in at least 2-3 different
scripts before it becomes a prompt change. One edit may just be that script.

## How to add a script

1. Generate, and commit the unedited output (prompt saved in `prompts/runs/`).
2. Rob edits; diff with `git diff -- radio/copy/text/<ep>/<segment>.yaml`
   (or `git show <generate commit>:<path>` vs. the working file).
3. Add a section below: what changed, plus a stats line. Then update the
   candidate-rules table (add the script to the evidence column, or add a row).

## Scripts reviewed

| Script | Prompt | Generated | Rob's version |
|---|---|---|---|
| `s01e01/zi-0001-char` (是) | `runs/s01e01-zi-0001-char.prompt.txt` (prompt-2 + adaptations) | 19 turns, 1,870 chars, 12 tags (Rob 6 / Sunshine 6), 2 hanzi | 15 turns, 1,527 chars, 7 tags (Rob 4 / Sunshine 2), 0 hanzi |
| `s01e01/zi-0001-sentences` (8 picks) | `runs/s01e01-zi-0001-sentences.prompt.txt` (first run of prompt-3) | 38 turns, 1,955 chars, 11 tags (Rob 4 / Sunshine 7) | 40 turns, 2,236 chars, 12 tags (Rob 4 / Sunshine 8). Additive only: a new opening exchange (one-off, see below), a few wording tweaks; nothing cut |
| `s01e01/zi-0002-char` (不, then split into `zi-0002-char` + `zi-0002-words`) | `runs/s01e01-zi-0002-char.prompt.txt` (prompt-2 adapted; filename mislabels it e02) | 25 turns, 2,869 chars, 14 tags (Rob 8 / Sunshine 6) | 27 turns, 2,773 chars, 15 tags (Rob 9 / Sunshine 6). Added family references, cut the model's jokes and the "not real history" disclaimer, swapped a rhetorical question for a practical one |

(Not yet reviewed: `s01e01/zi-0000-char` and `intro` were hand-edited before
this tracking started, so there is no clean generated-vs-edited pair.)

## Stated preferences (Rob's own explanation of his edits, 2026-10-02)

These come straight from Rob, not from my reading of his diffs, so they
outrank any inferred pattern below.

1. **Keep it from getting long-winded.** The show shouldn't be so long that
   people want to turn it off. This is a main driver of his cuts (shorter
   turns, trimmed disclaimers and asides, dropped riffs).
2. **Some jokes don't land -- that's fine.** Keep writing jokes; some do hit.
   He's happy to trim the ones that miss during review. So cuts of jokes
   (candidates #3, #7) are *not* a signal to stop writing jokes, only that
   the hit rate isn't perfect.

Implication for the candidate rules below: #2, #3 and #6 are mostly about
length and hit rate, not a rule against humor. If we change a prompt, aim at
"tighter and shorter", not "fewer jokes".

## Planned future prompt change (Rob, 2026-10-02)

Not from diffs -- stated in advance. Rob expects to **relax the ban on Rob
speaking hanzi** in later, longer sentences, since he can't break a long
sentence down and translate it without naming the pieces. Order of work:
tests first, then manual hanzi in Rob's lines when needed, and only *later*
expand the prompts (prompt-2/3 currently forbid any hanzi/pinyin in Rob's
lines, and the mechanical check enforces it). Don't change the prompts yet.
See bible.md Open TODOs for the side issues to check.

## Candidate rules and evidence

"Evidence" lists the scripts where the pattern appeared. Confidence is my
read of how likely it is a real preference, not a decision.

| # | Candidate rule | Evidence | Confidence |
|---|---|---|---|
| 1 | Rob opens with plain host questions ("What's it mean?"); no meta-jokes or callbacks in the first two turns | zi-0001-char; zi-0002-char ("How am I supposed to know which one it is?" -> "Is this a common use?") | medium (the one callback Rob kept in zi-0001-char was the closing "singular" one) |
| 2 | One thought per turn; don't split a point into set-up + echo ("merge ping-pong") | zi-0001-char (19 -> 15 turns). **Counter-evidence** in zi-0002-char: Rob split a long Sunshine turn at the topic transition and added short Rob reactions ("Nailed it."), 25 -> 27 turns | low (1 for, 1 against) |
| 3 | Cut Sunshine's reactive praise/quips ("Good eye!", "Barely", "Enjoy it") and Rob's wry restatements ("so things exist. Fine.") | zi-0001-char. **Not repeated** in zi-0001-sentences: Rob kept every quip ("I've noticed", "Sounds like me in a meeting"). **Repeated** in zi-0002-char: cut "caveman correcting you", "I've got nothing", the fence-sitting riff (-> "Nailed it."), "I'll leave the pronouncing to you" | medium (2 for, 1 against) |
| 4 | Describe character shapes in English only; no hanzi for components (日, 正) | zi-0001-char | **low** -- contradicts the current prompt ("hanzi fine for parts"); could be TTS worry or taste, unknown which |
| 5 | When a shape is complicated, Rob jokes about the complexity instead of inventing a description ("...a lot to look at") | zi-0001-char | low-med |
| 6 | Shorter disclaimers (e.g. "folk explanation, not real history, but it helps" -> "an old folk history trick") | zi-0001-char; zi-0002-char ("It's not real history, just a trick." cut entirely) | low-med |
| 7 | Fewer bracket tags; only for a real change in delivery. Rob cut Sunshine's from 6 to 2 and removed `[laughs]` / `[laughing]` / `[delighted]` / `[excitedly]` | zi-0001-char | low -- cuts against the bible's "Sunshine more expressive"; unclear if tags were overused or if expressiveness should come from the writing. **Not repeated** in zi-0001-sentences or zi-0002-char: no tags removed |
| 8 | Capitalize a single word for emphasis (Rob used "WHEN" in zi-0001-char; "LOTS" and "DO" in the lines he added to zi-0001-sentences) | zi-0001-char, zi-0001-sentences (3 uses, 2 scripts) | medium (ElevenLabs v4 docs say capitalization increases emphasis; note the zi-0001-sentences caps were in text Rob wrote himself, not edits of generated lines) |
| 9 | Use the show's own terms ("tone", "punctuation") instead of casual paraphrases ("the warm one" -> "the warm tone", "the dot at the end" -> "the punctuation") | zi-0001-sentences; zi-0002-char ("first word" -> "first compound word") | low-med |
| 10 | **Resolved (Rob, 2026-10-02):** Rob inserts throwaway daughter references ("my daughter's favorite word", "now my daughter will know how to reply..."), used like a pet or made-up person: no name, location or real behavior. Allowed for now; bible updated. I should still flag each mention in review. Not a prompt pattern (the model shouldn't write these; Rob adds them) | zi-0002-char | n/a |

## Not a prompt change (one-offs)

- zi-0001-sentences: Rob added a new opening exchange explaining where the
  example sentences come from (a document of his, which he hopes to make
  available). The generated segment started cold. This is s01e01-specific
  information the model couldn't have, so it's handled by hand, not by the
  prompt (Rob, 2026-10-02).

## Notes / things to check when listening

- Rob's zi-0001-char edits had a "Wel,," typo (line 9) that he fixed to "Well," before the audio was rendered.
- zi-0001-char lines 8-9: Rob's "...a lot to look at" followed by Sunshine's
  "Well, the box on top is the sun" may read as answering a different
  question. Check on playback.
