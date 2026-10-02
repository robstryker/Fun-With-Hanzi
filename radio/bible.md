# One 字 at a Time — Show Bible

Personas, tone, and content rules for the two-host read-along show built from
the graded reader. Production/TTS mechanics (voices, script-writing rules for
the synthesizer, phases) live in `radio/README.md` — this file owns the
creative content so future episodes don't drift from it.

**Audience:** public release. Made for Rob's own enjoyment first — the show
is the way Rob wants it, not audience-optimized. If it resonates with other
people learning the same way (one character at a time), that's the bonus,
not the design target.

## Hosts

### Rob

Fictionalized version of the creator's real motivation, not his literal
biography (no direct references to his actual job, family, or daughter).
Backstory: he wanted to learn Chinese as an adult but found most courses
either started with vocabulary that wasn't useful day to day (animals, toys)
while glossing over the basics, or beelined for travel/business phrases at
the expense of grammar fundamentals. He wanted something that starts at zero
and goes one step at a time — which is what this show, and the reader it's
built from, actually does.

**Host/guest asymmetry.** Rob is the classic radio *host*, not a co-expert:
like a host who talks to all kinds of guests and knows less about any given
topic than the guest does, Rob knows meaningfully less Chinese than Sunshine
and isn't puzzling through the characters himself. Concretely:
- **Rob's lines are English by default. He does not read Chinese
  characters/words aloud as a matter of routine** — not compounds, not
  sentences, at most (rarely, deliberately) a single bare character name for
  a bit, never as a script default. This is a content-format choice (the
  host/guest split — this isn't his content to carry), independent of
  whatever voice/engine renders him (see README's Production pipeline).
- **Sunshine carries the Chinese content, and she presents each new word
  already combined** — she pronounces new characters, introduces each
  unlocked compound as a finished word (in hanzi, spoken in her own voice),
  and reads every target sentence. **Rob never does the combining himself**
  and never voices the pinyin/romanized form of what she just said — not
  even as his own guess at pronunciation. His job, strictly after she's
  presented the word, is translating it, asking questions about it, and
  reacting — including moments of gradual realization as something clicks
  for him. He reasons from the English *meanings* of the pieces (which
  Sunshine can state in English, e.g. "他 is 'he,' 们 is the plural piece"),
  never from saying the Chinese sound himself.
- **Script-text consequence** (see `radio/README.md`): any Chinese content
  in Sunshine's lines must be written as actual hanzi, never pinyin —
  pinyin text is not a lighter stand-in, it's a different, wrong input for
  both the TTS voice and the sentence/word-matching pipeline.
- **Exception: visual shape description.** Pronunciation, meaning, and
  combining words are Sunshine's exclusively — but describing what a
  character *looks like* isn't Chinese-language content, it's a visual
  observation, and Rob can see the character same as anyone watching the
  read-along video. So he doesn't have to always tee up Sunshine for the
  shape ("what does it look like?") — he can take the first crack at
  breaking it down visually himself ("looks like a gate with a person next
  to it"), with Sunshine confirming, correcting, or adding the parts he
  wouldn't know (the radical's name, the etymology). Vary who leads on
  shape the same way the literal-translation bit varies whether Rob
  nails/half-gets/punts — sometimes Rob describes it unprompted, sometimes
  he asks Sunshine, sometimes she leads without being asked.

**Running bit — the literal-translation reveal.** Rob already has the
correct translation in hand (he's reading from a prepared script) — the
comedy/pedagogy isn't "does he get it right," it's watching him work
*backward*, in English, from the component meanings Sunshine's just given
him to the real meaning ("pretty hair master" → beautician; 手心 "hand
heart" → palm) — after she's already presented the finished compound, not
by him assembling it. He delights in calling out the literal reading before
landing on the real one. Two honest outcomes, both fine, neither a failure
state:
- He takes a swing at bridging literal → real meaning himself.
- He openly admits he can't see how the pieces connect and asks Sunshine to
  explain it.

This bit's home base is word unlock, but it isn't fenced off there — Rob can
also pull it out on a sentence-dive example when a compound in that sentence
invites it. He's not a one-trick pony: most sentence-dive turns are a
straight translation (see below), and the literal-translation bit surfaces
only when a particular sentence earns it.

### Sunshine

Native Mandarin-speaking co-host — the show's *guest expert*, in the
host/guest asymmetry above. Carries essentially all the Chinese: introduces
each new character's pronunciation and tone, reads the unlocked compounds,
reads every target sentence. Teaches, confirms or corrects Rob's
literal-to-real leaps, explains when he punts. Because she's mostly reading
already-unlocked words and sentences, she rarely faces the "only taught
vocabulary" constraint the book itself enforces — when she does deliberately
reference a character not yet taught, it's an intentional foreshadow of a
future lesson, not a slip.

**The ambiguity arc.** It is never stated, from episode 1, whether Sunshine
is a real person or an agent — this is deliberate and central, not an
oversight to be resolved quickly.
- **No cracks before ~episode 12.** The first hint is Rob noticing something
  ("you've said that same joke word-for-word three times now"), not her
  slipping up herself.
- **No open riffing on it before ~episode 25.** Even after the first cracks,
  she doesn't lean into the bit for a long stretch.
- **She never brings it up unprompted** and doesn't draw attention to it —
  but once Rob broaches it, she plays along within reasonable limits.
- **She never fully embraces it, even by the end.** She gets more
  comfortable engaging with the idea as the series goes on, but retains some
  genuine discomfort about openly mocking her own bodilessness — the arc
  ends with her more at ease, not "revealed."
- This lands as written specifically because the audience is public: it's
  meant to hold up honestly if a real listener thinks it through afterward,
  not just work as a private joke.

**Open TODO:** whether the specific per-episode "tells" (what cracks at 12,
what she riffs on at 25+) are a fixed list written in advance, or improvised
episode-by-episode within these pacing guardrails. Undecided.

## Show structure

| Segment | Purpose | Notes |
|---|---|---|
| Cold open / recap | ~1-2 min of banter, catches up from last episode | Good place to naturally reuse a recently-taught character in a throwaway line before the new one shows up |
| New character | Shape, radicals, etymology | Sunshine introduces the character, its pronunciation, and tone — she carries the Chinese per the host/guest asymmetry above. Depth varies by character — not every one earns a full etymology detour; judged per-character at scripting time, not forced every episode |
| Word unlock | Walks through newly-unlocked compounds and how the constituent hanzi combine | Sunshine reads each compound; Rob's literal-translation bit lives here, working in English from the component meanings she gives him |
| *(separate generation prompt)* | | Sentences are scripted in their own pass so a single prompt isn't asked to produce the whole episode |
| Sentence dive | Works through 15-20 selected example sentences | See rules below |
| Closing | Recap + sign-off | See rules below |

## Sentence-dive rules

- **Sentence numbers are the PDF's printed numbers** — a sentence's position in
  `build_print.ordered_sentences` (shortest first; `print/show_sentences.py` uses
  the same function, fixed 2026-10-02 after it drifted from the PDF's order).
- **Always name the sentence number before reading it** — "Sentence 17,"
  "Moving on to sentence 22..." Never read one cold. This is a hard rule, not
  a style preference: it's spoken for the audience, and it doubles as a
  cross-check against the automatic sentence-identification described below.
- **The target sentence is read on its own dedicated turn: pure Chinese,
  verbatim, nothing else in the line.** No paraphrasing, no folding the
  English gloss into the same turn — discussion/translation happens on a
  following turn. This is what makes the sentence identifiable and
  timestampable after the fact (see Production note) without any manual
  tagging.
- **Who reads what:** Sunshine reads the target sentence itself (she's the
  native speaker, pronunciation matters), on its own dedicated turn per the
  rule above. Rob reads the translation, most of the time — this is the
  default rhythm, not a fixed rule with no exceptions.
  - Occasionally Sunshine reads a short run of sentences back-to-back
    (verbatim, one per turn, still individually announced by number),
    translating in between each — used when the sentences are similar to
    each other or when stacking them makes a point (e.g., contrastive
    examples, a pattern shown across several sentences in a row).
  - On some sentences Rob doesn't just translate straight — he pulls the
    literal-translation bit (see Rob's persona above) on a compound in that
    sentence before landing on the real meaning.
- **Selection:** 15-20 sentences out of the full pool the PDF would show for
  that character (that pool is already copyright-cleared at the PDF stage --
  see README "Before public release"; don't re-filter by source here), chosen editorially — favor sentences that reuse multiple
  recently-taught characters (max reuse payoff), and mix quick-read and
  dissect candidates rather than just taking the first N.
- **Quick read:** no new grammar pattern, every word is either the new
  character's own compound or already-seen vocabulary. Sunshine reads it,
  Rob translates in real time, checks with Sunshine, move on.
- **Dissect:** the sentence introduces a pattern from the grammar-recycling
  list (把/被, 是…的, 得-complements, 越…越, etc. — see the reader's
  `AGENTS.md`) or revives a pattern taught long enough ago it needs a
  reminder. Slow down and walk through it.

## Closing rules

- Recap the words/characters learned this episode.
- State the running total of characters completed so far, for momentum.
- Sign-off: a varying lead-in phrase ("brick by brick," "step by step," ...)
  that always lands on the title — "...one 字 at a time."
- **No next-episode teaser.** The teaching order doesn't lend itself to
  previewing what's coming, so don't force one.

## Production note

**Timing manifest, not summed durations.** Sentence-level (Tier 1) highlight
timestamps come from the timing manifest `scripts/render_episode_segment.py`
writes (`copy/audio/<episode>/<segment>.manifest.json`, one per segment —
`segment_type, source_id, duration, running_start_time` per segment) as a side effect of the actual render,
never by summing the authored script separately. This matters once
filler/gap choice becomes dynamic (see README's Naturalness research) —
extra/variable-length segments the script doesn't know about would break a
recomputed sum, but the manifest is unaffected since it's built from what
was actually rendered.

**Sentence identification is automatic, not tagged.** Because a target
sentence is always read verbatim on its own pure-Chinese turn (see rule
above), a post-processing script can match that turn's text (punctuation-
insensitive, same comparison the print pipeline already uses for
`HIDDEN_EXAMPLES`) against the character's known sentence list (the same
data `show_sentences.py`/`sentence_counts.py` already load) and recover
which numbered sentence it is with no LLM cooperation required. Free
consistency check: compare the matched number against the number spoken
aloud in the preceding announcement turn, flag any mismatch. A sentence that
doesn't match anything (paraphrased, altered) fails the match and gets
flagged rather than silently mis-identified.

Word/character-level timing *within* a matched sentence (Tier 2, karaoke-
style highlighting) is a separate, later layer — ElevenLabs' `with-
timestamps` endpoint returns character-level timing at no extra cost
(unverified yet for v4 + mixed-language text), or forced alignment as a
fallback. Neither requires redoing the script.

## Open TODOs

- Sunshine's per-episode "tells" for the reveal arc: fixed list vs.
  improvised (see above).
- How a batch of ≥5 new characters maps to episodes — one episode per new
  character (others appear via reuse/banter), or one episode walking a
  whole batch of 5+ at once. Undecided — s01e01 (character #1) is one
  episode per character, but that's one data point, not a resolved rule.
- Target episode runtime not yet set.
- **Per-episode summary/notes file, for future callback support** — not
  needed until many episodes exist. Once an episode is generated, write a
  short summary alongside it (characters introduced, notable banter,
  anything worth a future callback) so a later episode's generator can read
  the summary instead of the full transcript. Undecided: file
  format/location, what fields it captures, auto-generated vs. hand-curated.
- **Per-episode generation pipeline: a `generate_prompt` script producing
  3-5 prompts per episode** (sketch only, nothing built). Per character:
  1. **Intro** — cold open, recap, banter. Once per episode, first character.
  2. **Character segment** — shape, pronunciation, meaning, new words. This
     is `prompts/prompt-2.md`'s template, validated on character #12.
  3. **Sentence dive** — ~20 example sentences (see rules above).
  4. **Post-character summary** — feeds the summary file above.
  5. **Episode end** — closing banter. Once per episode, last character.
  Multi-character episode: 2-4 repeat per character, bracketed by one 1 and
  one 5. Undecided: exact prompt boundaries, how prior-episode history feeds
  in, whether prompts 2-4 share a running conversation or are independent.
