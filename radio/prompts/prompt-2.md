# Prompt 2 — character, shape, tone, meaning, new words

Part of a planned per-episode sequence of 3-5 prompts (see `bible.md`'s Open
TODOs, "Per-episode generation pipeline" — undecided/not built yet). This is
the template for the segment that introduces one new character: its shape,
pronunciation/tone, meaning, and the new compound words it unlocks. No
sentences (that's prompt 3), no intro/recap/banter (that's prompt 1, and
only runs once per episode for the first character).

**Status:** hand-run twice against Opus 5.5 via `claude -p` (2026-09-28,
character #12, 们) to sanity-check content/personality before building any
generation tooling. First run omitted the character's shape (see "Known
gap" below); the DATA block and instructions below already have that fix,
and a **second run confirmed it works** — see "Worked example" below,
which is now the post-fix, verified output. Both runs checked mechanically
(not just by eye) for zero hanzi/pinyin in any `Rob:` line: pass both
times.

**Known gap this version fixes (already applied below):** the first real
run omitted the character's visual shape/component description entirely
(bible.md's "New character" segment calls for "shape, radicals,
etymology"), because the DATA block simply didn't include that information
for the model to work with. Fixed by adding a `Shape:` line to DATA and an
explicit instruction to describe it — confirmed working on the second run.

---

```
You are writing one segment of a scripted two-host episode for "One 字
at a Time," a Chinese-learning radio show built from a graded reader.

HOSTS:
- Rob: fictionalized version of the creator, the show's host. He does NOT
  read, pronounce, or repeat any Chinese -- not hanzi, not pinyin/romanized
  syllables -- under any circumstance in this segment. HARD CONSTRAINT: no
  line spoken by Rob may contain a Chinese character or a romanized Chinese
  word. When Rob refers to the word under discussion, he refers to it only
  by its English meaning/translation, never by naming or repeating the
  Chinese form Sunshine just said.
  His running bit: after Sunshine presents a new word (already fully
  combined, in hanzi), Rob works backward IN ENGLISH from the component
  meanings she's given him to guess the real meaning -- either he bridges it
  himself, or he admits he can't and asks Sunshine. Vary whether he nails
  it, half-gets it, or punts.
  EXCEPTION -- visual shape description: describing what the character
  looks like is not Chinese-language content (it's a visual observation,
  and Rob can see the character same as the audience watching the
  read-along video), so Rob is not restricted to only asking Sunshine about
  shape. Vary who leads on it: sometimes Rob breaks down the shape visually
  himself unprompted (e.g. "looks like a gate with a person next to it"),
  sometimes he asks Sunshine to describe it, sometimes she leads without
  being asked. Sunshine still confirms/corrects and adds anything Rob
  wouldn't know (radical names, etymology).
- Sunshine: native Mandarin co-host. She introduces each new character --
  including a brief, natural description of its visual shape/component
  radicals (depth varies by character; not every one earns a full
  etymology detour, but always at least a one-line shape description) --
  and presents each newly-unlocked word already combined, in hanzi. Rob
  never does the combining. Confirms/corrects Rob's guesses, explains when
  he punts. This is an early episode -- no hint yet that her realness is
  ambiguous; play her completely straight.
  Never echo the character's pinyin back as a spoken aside immediately
  after pronouncing it (e.g. "This one is 们, 'men,' and it's neutral
  tone" -- that's just saying the same sound twice in a row for no
  reason). The pinyin given in DATA guides how Sunshine pronounces the
  character correctly; it is not additional text for her to speak aloud
  as a separate echo. If there's ever a real reason to say the
  pronunciation again in English-letter form (genuinely clarifying an
  ambiguous sound, setting up Rob's literal-translation bit), that's a
  deliberate choice earning its own justification, not a reflex.

CONTENT RULES: everyday concrete language only; no chengyu, dialect,
swearing, or romance content.

THIS SEGMENT ONLY covers: introducing the new character (number,
pronunciation, tone, shape/component description) and walking through the
new compound words it unlocks. Do NOT include a cold open, recap, callback
to prior episodes, or any example sentences -- those are separate segments
generated separately. Start the transcript directly with Sunshine
announcing the character.

DATA:
- Character #<N>: <char>, pinyin "<pinyin>", <tone>. Meaning: <meaning>.
- Shape: <component radicals and a plain description of what they look
  like combined -- e.g. "亻(person radical, a standing figure) on the left
  + 门 (a two-leaf door/gate) on the right">.
- Newly unlocked words (every other character in these is already taught):
  <word> (<pinyin>) "<meaning>" | <word> (<pinyin>) "<meaning>" | ...

Write the segment as a plain dialogue transcript, "Rob:" / "Sunshine:"
labels, no stage directions or audio markup -- this pass is about content,
personality, and the Chinese/English split, not TTS production.

Before finalizing, re-check every line labeled "Rob:" and confirm it
contains zero Chinese characters and zero romanized/pinyin Chinese words.
Output ONLY the transcript, nothing else.
```

---

## Worked example (character #12, 们) — the actual run this template is based on

DATA used:
```
- Character #12: 们, pinyin "men", neutral tone. Meaning: plural marker
  suffix for pronouns/people-nouns -- not a standalone word.
- Shape: 亻 (person radical, a standing figure) on the left + 门 (a
  two-leaf door/gate) on the right -- a person standing beside a gate.
- Newly unlocked words: 他们 (tamen) "they/them" | 他们的 (tamen de)
  "their/theirs" | 你们 (nimen) "you (plural)" | 她们 (tamen) "they/them
  (female)" | 我们 (women) "we/us" | 我们的 (women de) "our/ours"
```
Ran via: `claude -p "<prompt above>" --model claude-opus-5-5
--output-format json --max-budget-usd 1` (same one-shot pattern
reading_lab's `call_claude_one_shot` uses -- billed against the
subscription, not a metered API key).

Output (2026-09-28, post-shape-fix, verified):

    Sunshine: Character number twelve! This one is 们, "men," and it's
    neutral tone, so it's light and quick with no real pitch of its own.
    Say it softly, almost like a little tail on the word before it.

    Rob: A tail. So it doesn't get to stand on its own?

    Sunshine: Never. 们 isn't a word by itself. It attaches to pronouns and
    to words for people, and it makes them plural. It turns one person
    into a group.

    Rob: Okay, what does it look like?

    Sunshine: On the left there's the person radical, the skinny standing
    figure we've already seen a few times. On the right is 门, which means
    door or gate. It's drawn like a two-leaf door, with a post on each side
    and an opening in the middle. So picture a person standing beside a
    gate.

    Rob: A person at the gate. And behind that gate are all their friends
    waiting to come in.

    Sunshine: I love that. It's a good way to remember it. One person at
    the door, and 们 lets the whole crowd in.

    Rob: Great. So what does it unlock?

    Sunshine: Six words today. First, 他们.

    Rob: Okay, the first part is the one you gave me for "him." Add the
    crowd and it's a bunch of guys. The guys. The dudes?

    Sunshine: Half right. 他们 means "they" or "them." It does cover a
    group of males, but it's also the default for any mixed group. Five
    women and one man? Still 他们. And if you don't know who's in the
    group, you use 他们 too.

    Rob: So it's the general-purpose "they." Got it.

    Sunshine: Next is 他们的.

    Rob: That's the same thing plus the little possessive piece at the
    end. "Their." Or "theirs."

    Sunshine: Exactly right. 他们的 is "their" or "theirs." Easy one.

    Rob: I'll take the easy ones. Keep them coming.

    Sunshine: 你们.

    Rob: "You," and then the gate opens and more of them walk in. So "you
    all." Y'all. You guys.

    Sunshine: Perfect. 你们 is plural "you." Use it when you're talking to
    more than one person. English uses the same "you" for one person or a
    whole room, but Chinese makes you choose.

    Rob: Honestly, English could use that.

    Sunshine: Now 她们.

    Rob: Okay, this one has the "her" piece in front, so it's a group of
    women. But wait, didn't the "her" character sound exactly like the
    "him" one? So how does anyone tell this apart from the first word when
    you say it out loud?

    Sunshine: They can't! 她们 and 他们 sound exactly the same. The
    difference only shows up in writing. 她们 means "they" or "them" when
    the group is all female. Out loud, you figure it out from context.

    Rob: So it's a spelling thing, not a sound thing.

    Sunshine: Right. Next, 我们.

    Rob: "Me," plus the crowd. So I'm the one at the gate, and everybody's
    with me. "We." "Us."

    Sunshine: Nailed it. 我们 is "we" or "us."

    Rob: And I'm guessing the last one is that plus the possessive tail.

    Sunshine: It is. 我们的.

    Rob: "Our." "Ours."

    Sunshine: Exactly. 我们的 means "our" or "ours." So with one little
    character, we got "they," "their," plural "you," the all-female
    "they," "we," and "our."

    Rob: Six words from one small tail. Not bad for something that can't
    stand on its own.

Verified (2026-09-28): shape/component description present (person radical
+ door/gate, "a person standing beside a gate" -- and Rob built his own
mnemonic on top of it, unprompted). Zero hanzi/pinyin in any `Rob:` line,
checked mechanically both runs. Personality keeps coming through unforced
(this run's own addition: Rob's "gate" mnemonic, and the recurring
他们/她们 homophone bit from the first run).

**First run (pre-shape-fix, 2026-09-28), for history:** identical prompt
minus the `Shape:` DATA line and shape instruction. Sunshine's intro
skipped shape entirely and went straight to pronunciation + meaning --
otherwise the same content/quality. Not reproduced here; superseded by the
run above.
