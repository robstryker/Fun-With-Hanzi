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
| `s01e01/zi-1-char` (是) | `runs/s01e01-zi-1-char.prompt.txt` (prompt-2 + adaptations) | 19 turns, 1,870 chars, 12 tags (Rob 6 / Sunshine 6), 2 hanzi | 15 turns, 1,527 chars, 7 tags (Rob 4 / Sunshine 2), 0 hanzi |

(Not yet reviewed: `s01e01/zi-0-char` and `intro` were hand-edited before
this tracking started, so there is no clean generated-vs-edited pair.)

## Candidate rules and evidence

"Evidence" lists the scripts where the pattern appeared. Confidence is my
read of how likely it is a real preference, not a decision.

| # | Candidate rule | Evidence | Confidence |
|---|---|---|---|
| 1 | Rob opens with plain host questions ("What's it mean?"); no meta-jokes or callbacks in the first two turns | zi-1-char | low-med (the one callback Rob kept was the closing "singular" one) |
| 2 | One thought per turn; don't split a point into set-up + echo ("merge ping-pong") | zi-1-char (19 -> 15 turns) | medium |
| 3 | Cut Sunshine's reactive praise/quips ("Good eye!", "Barely", "Enjoy it") and Rob's wry restatements ("so things exist. Fine.") | zi-1-char | medium |
| 4 | Describe character shapes in English only; no hanzi for components (日, 正) | zi-1-char | **low** -- contradicts the current prompt ("hanzi fine for parts"); could be TTS worry or taste, unknown which |
| 5 | When a shape is complicated, Rob jokes about the complexity instead of inventing a description ("...a lot to look at") | zi-1-char | low-med |
| 6 | Shorter disclaimers (e.g. "folk explanation, not real history, but it helps" -> "an old folk history trick") | zi-1-char | low |
| 7 | Fewer bracket tags; only for a real change in delivery. Rob cut Sunshine's from 6 to 2 and removed `[laughs]` / `[laughing]` / `[delighted]` / `[excitedly]` | zi-1-char | low -- cuts against the bible's "Sunshine more expressive"; unclear if tags were overused or if expressiveness should come from the writing |
| 8 | Capitalize a single word for emphasis (Rob used "WHEN") | zi-1-char | low (first use; ElevenLabs v4 docs say capitalization increases emphasis) |

## Notes / things to check when listening

- Typo to fix in zi-1-char line 9: "Wel,," (should be "Well,").
- zi-1-char lines 8-9: Rob's "...a lot to look at" followed by Sunshine's
  "Wel,, the box on top is the sun" may read as answering a different
  question. Check on playback.
