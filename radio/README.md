# radio/ -- two-host audio/video show (exploratory)

Turns the graded reader into a podcast / read-along video series. Design notes
live in Rob's memory for now; nothing here is wired into the print pipeline
(`print/`, `data/`, `outputs/` are untouched by this directory).

Hosts: a native-English male + a bilingual (English/Mandarin) female.
Audience: public release (not the daughter -- she gets the PDF). See
"Before public release" below.

## Layout

| Path | Role | Committed? |
|---|---|---|
| `scripts/` | Voice/engine experiments and POC dialogue generators (renamed from `smoke/` 2026-09-28 -- outgrew "throwaway smoke test only") | yes |
| `bible.md` | Show bible (personas, tone, rules) -- added in phase 0 | yes |
| `prompts/prompt-N.md` | Saved per-segment prompt templates, hand-run examples included -- see bible.md's "Per-episode generation pipeline" | yes |
| `copy/text/<episode>/<segment>.yaml` | Real per-segment script (`intro`, `zi-0000-char`, `zi-0001-char`, ...), S/E-keyed episode dir (e.g. `s01e01`) -- see "Episode segment files" below; replaces the earlier planned monolithic `script.yaml` / `episodes/NNN.yaml` | yes |
| `copy/audio/<episode>/` | Rendered per-line clips (`<Speaker>-<hash>.mp3`, content-addressed) + `.json` alignment sidecars + one `<segment>.manifest.json` timing manifest per segment | yes -- persisted, not just regenerated on demand |
| `copy/final/<episode>/` | Concatenated per-segment mixes (`<segment>-compiled.mp3`); the whole-episode mix is a later assembly step | yes |
| `out/` | Throwaway smoke-test/POC output, not real episodes | **no** (gitignored) |
| `.venv/` | Own Python env (edge-tts etc.), see `requirements.txt` | **no** |

Phases: 0 show design -> 1 translations + char facts -> 2 text pilot ->
3 audio pilot (smoke tests first) -> 4 video pilot -> 5 scale + publish.

## Production pipeline (decided 2026-09-28)

**Both hosts render on ElevenLabs v4** -- Rob = James (`uh5qBlKfjqFl7XXhFnJi`),
Sunshine = Sapphire (`zmcVlqmyk3Jpn5AVYcAL`), IDs and model constant in
`scripts/eleven_creds.py`. This supersedes the original Azure split (Andrew/
Xiaoxiao); see `bible.md`'s and this file's "Script style rules" sections for
why Azure needed the CJK-run-splitting/break-tag workaround that ElevenLabs
doesn't.

**Per-line requests, not the multi-speaker Text-to-Dialogue endpoint.**
Considered and rejected 2026-09-28: bundling a whole scene into one request
would force a full-scene re-bill on any single-line edit or re-take, which
defeats iterating on a script. Every line is still its own API call, same as
the Azure-era scripts -- ElevenLabs just doesn't need the internal CJK-run
splitting Azure did (a mixed-language line goes in as one unsplit string).

**`scripts/render_episode_segment.py`** (renamed from `render_episode.py`
2026-10-02) renders ONE segment of an episode, not the whole episode. It
reads `copy/text/<episode>/<segment>.yaml` (a plain list of `{speaker, text}`
turns -- bracket emotion tags go inline in `text`, e.g.
`"[whispers] wait, really?"`), renders each line, and writes:
- `copy/audio/<episode>/<Speaker>-<hash>.mp3` -- **content-addressed**
  (decided 2026-10-02): the hash covers speaker, voice id, model id and the
  stripped line text, and nothing else -- no line number, no segment prefix.
  Adding, removing or reordering lines never renames or re-renders anything;
  only new/changed lines are synthesized (and billed). Changing a voice or
  model changes every hash, so stale clips can't be served. Order lives only
  in the manifest, rebuilt from the YAML each run. On a miss, the script
  first searches the other episodes' audio folders (and anywhere under
  `radio/`, minus `.venv`) for a same-named clip and copies it in with a
  "reused from ..." notice instead of re-billing -- clips stay isolated per
  episode, reuse is an explicit copy. Note an identical line replayed
  verbatim in another episode can be an unintended repeat (see the Sunshine
  ambiguity arc in bible.md).
- `copy/audio/<episode>/<Speaker>-<hash>.json` -- sidecar from ElevenLabs'
  `with-timestamps` endpoint (same price as plain TTS): per-input-character
  start/end times, bracket tags included at ~0 duration. Verified working on
  v4 with mixed English/Mandarin (2026-10-02). Clips rendered before the
  switch have no sidecar (manifest shows `alignment: null`).
- `copy/audio/<episode>/<segment>.manifest.json` -- the timing manifest bible.md's
  production note requires (`segment_type, source_id, duration,
  running_start_time` per segment, line and gap alike). This is the first
  real implementation of that manifest; nothing downstream should ever
  recompute timing by summing the authored script instead of reading this.
- `copy/final/<episode>/<segment>-compiled.mp3` -- that segment's concatenated
  mix.

Output paths are anchored to the script's own location, so the cwd doesn't
matter and nothing is ever written to a stray `radio/` tree. Rendered output
always goes into the repo, never scratch/tmp dirs.

Run: `radio/.venv/bin/python radio/scripts/render_episode_segment.py s01e01 intro`

**Episode assembly** (2026-10-02): `radio/.venv/bin/python radio/scripts/assemble_episode.py s01e01`
joins the episode's rendered segments, in order -- `intro`, then
`zi-NNNN-char/words/sentences/conclusion` ascending (the 4-digit NNNN is what makes
the names sort), then `outro`; segments that don't exist yet are skipped and
the list used is printed. It reads the segment manifests and clips (never calls
the TTS API), refuses to build if a segment's YAML was edited after its last
render, and writes `copy/audio/<episode>/<episode>.manifest.json` (merged,
every entry tagged with its `segment`, offsets across the whole episode) and
`copy/final/<episode>/<episode>-compiled.mp3`. Clips are joined directly in one
encode, with the usual 0.2s turn gap plus an extra `--segment-gap` (default 0.6s)
between segments.

**Manifest durations are decoded lengths, not ffprobe's** (fixed 2026-10-02):
an mp3's probed `format.duration` runs ~0.03-0.04s longer than the audio that
actually decodes (encoder padding), which drifted the manifest ~6s over a
170-line episode. `duration()` now counts decoded samples, and the segment
manifests were rebuilt (no credits). The assembler checks the mix length against
the manifest total.

**Clip backup:** `radio/.venv/bin/python radio/scripts/backup_clips.py` copies every
clip and its alignment sidecar, flat and under its hash filename (no episode
folders), to `/data/education/learnChinese/radio/`. Copy-only: never
overwrites or deletes, safe to re-run any time (already-backed-up files are
skipped). Manifests aren't backed up -- they're in git, and rebuild from the
YAML plus the clips. Run it after each render session.

## Episode segment files (decided 2026-09-28; rendering implemented 2026-10-02)

Instead of one monolithic `script.yaml`, each episode's script is authored as
one YAML file per segment in `copy/text/<episode>/`, each the same plain list
of `{speaker, text}` turns. Splitting by segment lets each piece be drafted,
prompted (see `prompts/`), revised and smoke-tested on its own, and keeps a
single-line edit from touching the rest of the episode.

Episode order:

| File | Once per | Segment (see bible.md "Show structure") |
|---|---|---|
| `intro.yaml` | episode | Welcome / cold open (recap from last episode goes here) |
| `zi-0000-char.yaml` | s01e01 only | One-off: the four sentence-ending particles 啊 呢 呀 吧 ("character 0" in the PDF), introduced by shape and pronunciation with a made-up demo sentence each. No words/sentences/conclusion files. Sits between `intro` and `zi-0001-char` |
| `zi-NNNN-char.yaml` | character | New character: shape, origin, pronunciation, tone |
| `zi-NNNN-words.yaml` | character | Word unlock: newly-unlocked compounds |
| `zi-NNNN-sentences.yaml` | character | Sentence dive for that character |
| `zi-NNNN-conclusion.yaml` | character | Short wrap-up of that character: what we learned from the character, its new words, and the sentences |
| `outro.yaml` | episode | Final outro / sign-off |

`NNNN` is the character's position within the episode, zero-padded to 4 digits
(so the filenames sort in teaching order) (`zi-0001-char`,
`zi-0001-words`, `zi-0001-sentences`, `zi-0001-conclusion`, then `zi-0002-char`, ...), repeated for as many
characters as the episode teaches ("a few times each episode" per the intro).
`intro.yaml` (renamed from `intro-draft.yaml` 2026-10-02, old `.bak` drafts
deleted) is the settled s01e01 intro.

Open questions:
- Conclusions are per character (decided 2026-09-28): a character with ~20
  sentences deserves a short recap of the character, its words and its
  sentences before moving on. Keep them short. The episode-level sign-off
  lives in `outro.yaml`; bible.md's "Closing rules" (currently one episode-level
  "Closing" segment) needs updating to split recap from sign-off.
- `render_episode_segment.py` renders one segment at a time; `assemble_episode.py`
  joins them (see "Episode assembly" below).

## Before public release
- Corpus sentences include the copyrighted Chinese Harry Potter translation.
  **Copyright pruning happens at the PDF stage, not the audio stage** (Rob,
  2026-10-02): most Harry Potter sentences were already excluded from the PDF,
  and the few that remain at early character numbers were analyzed and judged
  to be very simple sentences anyone would make by combining the first 20-50
  characters. So the audio/sentence-selection step trusts the PDF's sentence
  list as already cleared and does NOT re-filter by source -- don't duplicate
  that work here. Any further pruning belongs in the PDF data
  (`HIDDEN_EXAMPLES`, see `AGENTS.md`), after which the audio picks it up
  automatically.
- CC-CEDICT is CC BY-SA (attribution + share-alike).
- Use a TTS with commercial terms, not edge-tts -- ElevenLabs (chosen above)
  qualifies once on a paid plan; the free tier blocks API access to any
  Voice-Library-sourced voice (James and Sapphire both are), so real episode
  rendering needs at least the $6/mo Starter tier, not just the free API key
  used for smoke tests so far.

## Script generation model

**Episode scripts: Claude Opus 5.5.** Chosen over ChatGPT (better nuanced
creative direction + constraint-following against this bible's dense rule
set) and over Fable 5.1 (60% cheaper at $4/$20 vs $10/$50 per MTok, matters
at ~75+ planned episodes; pitched as fixing "Claudish" writing tics, the
exact failure mode to avoid in dialogue). Not a clear win, though -- Fable
5.1 writes sharper raw prose, and **the side-by-side pilot hasn't been run
yet.** Revisit if it favors Fable 5.1 enough to justify the cost gap.

**Everything else (pipeline code, this session): Sonnet 5** -- cheaper,
sufficient for non-creative driver work. Only script generation uses the
pricier model.

## Script style rules

Current engine is ElevenLabs v4 for both hosts (see Production pipeline
above). Azure/edge-tts-specific findings from earlier smoke tests (SSML
break-tag tuning, per-voice style lists, pinyin-diacritic handling on
Xiaoxiao) are dropped here as no longer applicable -- neither engine is in
use now.

- Say "X **means** Y", never "X is Y" when glossing -- "is" next to Chinese
  gets mangled/ambiguous by the TTS and heard-only.
- **Don't reflexively echo a character's pinyin as a spoken aside right
  after pronouncing it** (e.g. "This one is 们, 'men,' and it's neutral
  tone" -- saying the same sound twice for no reason). Hard rule in
  `prompts/prompt-2.md`: the DATA pinyin field guides pronunciation, it
  isn't additional text to speak aloud, unless a real reason earns it.
- **Sunshine's Chinese content must be written as hanzi, never
  pinyin/romanization**, for full sentences and compounds. Not a style
  preference -- it's the wrong input for the sentence-matching pipeline
  (bible.md's production note matches spoken text against the known hanzi
  sentence corpus). A script draft that comes back romanized has to be
  regenerated, not lightly edited.
- **Exception: isolated single characters can need pinyin instead.**
  ElevenLabs v4 can read a bare hanzi character as an English word rather
  than the Mandarin sound, even quoted -- happened with 字 in the show
  title ("One 字 at a Time" → "zee"). Fix: pinyin with its tone mark
  (`One "Zì" at a Time`). Proposed heuristic (validated on this one case
  only): prefer pinyin for an isolated character *with* a real tone mark;
  for a flat/neutral-tone character, bare pinyin has no diacritic to signal
  it isn't English, so fall back to quoted hanzi instead. This only applies
  to isolated single characters -- full sentences still always use hanzi
  per the rule above.

## Naturalness research (still open, not yet built)

`render_episode_segment.py`'s per-line-plus-fixed-gap approach is the pattern people
flag as sounding like "two people reading unrelated scripts in the same
room." Open ideas, priority order:

- **Vary the inter-turn gap** instead of one fixed `TURN_GAP` value. A quick
  agreeing reply lands almost instantly; a considering pause is longer.
  Cheapest single change likely to matter most.
- **Pre-generate a filler/breath bank per voice**: a couple dozen clips each
  of breath-in/out, "um," "hmm," "so...", "yeah," plus a rare cough/laugh,
  generated once per host voice, rotated in at turn boundaries instead of
  dead silence. Weight by rarity (breath near-universal, filler words ~1 in
  4-6 turns, cough/laugh once or twice an episode); track recently-used
  fillers per speaker to avoid an audible repeat within one episode (a
  repeated filler would land as an accidental version of the Sunshine
  reveal-arc "tell" -- avoid that happening by pipeline accident). Insert
  contextually, not on every line. Doesn't break the timing manifest
  (`render_episode_segment.py` already writes per-segment durations as it builds
  the file, not by summing the script -- fillers/variable gaps just add
  more segments to that same manifest).
- **Assembly tooling: ffmpeg script, not an OpenShot project.** OpenShot is
  built for a human dragging clips on a timeline, not assembling hundreds
  of generated segments with computed timings. A script that walks the
  line list, picks fillers/gaps, extends the manifest, and builds an ffmpeg
  concat list (plus a matching image-sequence duration list for video) is
  the right shape. OpenShot could still work for a one-time human polish
  pass on the finished synced file (intro/outro music, a trim).
- **Other pitfalls to watch for**: flat/metronome prosody on individual
  lines, dry/placeless sound (no room tone -- a cheap post pass can help),
  prosody drift over long stitched output (past ~10-15 min).
- **No avatar/lip-sync risk** -- the video is a highlighted PDF/HTML page,
  not a talking head. Single-voice code-switching (the hard research
  problem for bilingual TTS generally) also isn't our problem -- confirmed
  working on ElevenLabs (see Script style rules), and each host mostly
  speaks one language per turn anyway.
- **Reference point:** NotebookLM's Audio Overview is the closest existing
  thing to this format and is widely reported as convincing -- a useful
  benchmark for how much a careful script buys before audio
  post-processing is even needed.
