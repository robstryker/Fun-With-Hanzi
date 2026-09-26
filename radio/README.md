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
| `smoke/` | Throwaway voice/engine experiments: scripts + tiny input text | yes |
| `bible.md` | Show bible (personas, tone, rules) -- added in phase 0 | yes |
| `episodes/NNN.yaml` | Approved per-episode scripts (added at pilot) | yes |
| `out/` | Generated audio/video/frames | **no** (gitignored) |
| `.venv/` | Own Python env (edge-tts etc.), see `requirements.txt` | **no** |

Phases: 0 show design -> 1 translations + char facts -> 2 text pilot ->
3 audio pilot (smoke tests first) -> 4 video pilot -> 5 scale + publish.

## Before public release
- Corpus sentences include the copyrighted Chinese Harry Potter translation:
  public episodes may only read hand-written / original sentences.
- CC-CEDICT is CC BY-SA (attribution + share-alike).
- Use a TTS with commercial terms (Azure/OpenAI etc.), not edge-tts.

## Script style rules (from smoke tests)
- Say "X **means** Y", never "X is Y" when glossing -- "is" next to Chinese
  gets mangled/ambiguous by the TTS and heard-only.
- edge-tts only: synthesize per single-language run, because a long mixed
  string made it repeat/skip phrases (gap between runs ~0.12 s; 0.30 s was
  too long). Azure Multilingual does not need this.
- Write English questions as **full questions** ("Do you hear the difference?"),
  never fragments ("Hear the difference?"): Azure Xiaoxiao Multilingual reads
  fragments flat, full questions rise (tested 2026-09-25; alone and in context
  behave the same). SSML `<prosody contour>` and a following `<break>` had no
  audible effect, so don't rely on them for this.
- Female host: `zh-CN-XiaoxiaoMultilingualNeural` (Azure) is the front-runner;
  mixed English/Chinese in one request works well, no run-splitting needed.
  Creds live outside the repo (`~/Documents/codes/azure.txt`, read by
  `radio/smoke/azure_voices.py:creds()`).
- **Language switches (Azure):** put a 150 ms `<break>` on both sides of every
  Chinese run (`radio/smoke/azure_gaps.py:add_gaps`, `DEFAULT_GAP_MS`). Chosen
  by ear on Andrew, Brian and Xiaoxiao: 0/80 ms ran words together ("sobu"),
  250 ms was too long. Script-writing preference: **finish a sentence in one
  language before switching** by default; use inline switching (e.g. "so 不
  means 'not'") when necessary, or when it is intentionally preferred to make
  the conversation sound more natural or dynamic. The 150 ms gap covers it.
- Male host: Andrew (`en-US-AndrewMultilingualNeural`) is acceptable; Brian is
  the alternate.
