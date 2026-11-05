# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. Arrives at `POST /submit` in `app.py` with `text` and `creator_id`.
2. Checked and given an ID *(I build: `app.py::submit`)*: reject missing,
   empty or huge text with a 400; give valid text a `content_id`.
3. Predictability score *(given: `detector.model_signal`)*: a local model
   rates how predictable the text is → `model_score` (0–1, higher = more AI).
4. Style score *(I build: `stylometry.style_signal`)*: sentence-length
   variety, word repetition and punctuation → `style_score` (0–1, higher =
   more AI).
5. Combined *(I build: `scoring.combine_signals`)*: the two scores become
   one, and my rule decides what happens when they disagree.
6. Labelled *(I build: `scoring.score_to_label`)*: the score becomes one of
   three plain-English labels: human, unsure or AI.
7. Logged and returned *(I build the calls: `audit.log_decision` + the
   response)*: the decision is saved, and the writer gets the label plus a
   `content_id` they can use to appeal.

### Tracing a false positive

<!-- Milestone 1: a real writer submits real work and the system calls it AI.
     The scores below are expected values worked out from the code, not a
     real run yet. -->

**Who:** a second-language writer submits their own work, written in simple
words and short, even sentences.

**Their score:** about 0.8. Plain writing is easy to predict and evenly
shaped, so both signals call it AI, and together they're even more sure.

**What the label says:** high-confidence AI, with no reason given.

**What they can do:** appeal with their `content_id`. A person has to review
it; nothing re-checks the text.

**What this means for my thresholds:** the AI label should start higher than
0.65, or the unsure band should be wider, so honest plain writing doesn't get
called AI.


### The two endpoints

All requests and responses are JSON. Every error has the same shape:
`{"error": "<short_code>", "message": "<sentence for a person>"}`.

#### `POST /submit`

**In:**

| Field | Type | Rules |
|---|---|---|
| `text` | string | Required. 50 to 10,000 characters after trimming spaces. |
| `creator_id` | string | Required. Not empty. |

**Out (200):**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | New UUID for this submission. Needed to appeal. |
| `guess` | string | `"human"`, `"unsure"` or `"ai"`. |
| `confidence` | number | The combined score, 0 to 1. Higher means more likely AI. |
| `label` | string | The sentence the writer sees. |
| `model_score` | number | Signal one, 0 to 1. Higher means more likely AI. |
| `style_score` | number | Signal two, 0 to 1. Higher means more likely AI. |

**Errors:** `400 missing_text`, `400 text_too_short`, `400 text_too_long`,
`400 missing_creator_id`.

#### `POST /appeal`

**In:**

| Field | Type | Rules |
|---|---|---|
| `content_id` | string | Required. Must match a past submission. |
| `reasoning` | string | Required. Not empty. Why the writer thinks the label is wrong. |

**Out (200):**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | The submission being appealed. |
| `status` | string | Always `"under_review"`. |
| `message` | string | Confirms the appeal was received and a person will review it. |

**Errors:** `400 missing_content_id`, `400 missing_reasoning`,
`404 unknown_content_id`.

Appealing the same item again is allowed; each appeal is logged. The
`creator_id` for the appeal log entry comes from the original submission.

**Read-back check:** could someone build against this without asking me? I
filled the gaps I'd have asked about: the text length limits, what
`confidence` means, which way the scores point, the error format, what happens
with an unknown `content_id`, and whether you can appeal twice.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model (gpt2,
running locally). This is called perplexity: low perplexity means the model
could have guessed each next word. The more predictable the text, the higher
the `model_score` (more likely AI).

**Why that might differ between human and AI writing:** AI writes by picking
the most likely next word again and again, so its text is easy for a model to
predict. People make more surprising choices: unusual words, sudden changes of
direction and specific personal details.

**What it can't see:** Who actually wrote the text. It only knows whether the
words were predictable, and plain writing is predictable no matter who wrote
it. So a person who writes simply, such as someone writing in a second
language, a younger writer or anyone keeping it plain on purpose, can score as
AI. The reverse also happens: AI text with rarer words swapped in can score as
human.

### Signal two — the style signal

**What it measures:** The shape of the text, without reading it. It looks at
three things: how much sentence lengths vary, how often words repeat
(type-token ratio: unique words divided by total words) and how much
punctuation is used. These combine into a `style_score` (higher = more AI).
I'd also like to add tone as a fourth measure later: how bossy or how warm
the text sounds (bare commands with no "you" or "I", short fragments, and
softening words like "maybe" or "I think"). It isn't built yet.

**Why that might differ between human and AI writing:** AI often writes even,
medium-length sentences with a narrower vocabulary, because picking the most
likely word keeps landing on the same common ones. Human writing is more
uneven: short and long sentences mixed together, more varied words, and
punctuation like dashes and semicolons. In my tests AI tone also stood out,
sitting at one of two extremes: clipped and instructional, like it's giving
orders, or overly warm and polite. That's what the planned tone measure is for.

**What it can't see:** What the text actually says or who wrote it. It only
counts surface features, so cheap edits like adding typos or mixing very short
and long sentences can make AI text look human. My own AI sample ("Two rules.
Public only...") had very uneven sentences, so this signal called it human.
A tone measure would have the same kind of blind spot: a teacher's handout or
a recipe sounds bossy and was written by a person, and adding "I think" to AI
text would make it sound warmer.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Take a weighted average of the two signals, counting them
equally, since each one fails on a different kind of writing and neither has
earned more trust. If the two disagree by more than a set gap, keep the
result inside the unsure band. A big split means the two methods are reading
the text differently, and the honest answer then is "not sure". That way a
split alone can never lead to an AI accusation, or a confident all-clear.

**The numbers:**

- Model signal weight: 0.5
- Style signal weight: 0.5
- Disagreement gap: 0.30 (the signals differ by more than this → the score
  is kept between 0.36 and 0.64, just inside the unsure band)

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

My lightly-edited AI test text is the detector's built-in AI sample with
small human-style edits: contractions, one typo and one sentence cut short
("Thats important."). The model signal gave 0.65 (leaning AI), because the
wording underneath is still predictable. The style signal gave 0.23 (human),
because that one short sentence made the sentence lengths uneven. They differ
by 0.42, more than my 0.30 gap, so my rule keeps the result in the unsure
band. The average, 0.44, already sits there, so here the rule confirms the
average rather than changing it. Without the rule, a slightly bigger split
could have tipped the score into a confident label either way.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 to 0.35 | "We think this was probably written by a person." |
| unsure | above 0.35 and below 0.65 | "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work." |
| high-confidence AI | 0.65 to 1.00 | "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it." |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The person reading it may well have written every word themselves, so it
says plainly that we can't tell, then reassures them straight away that this
happens to plenty of real writers and isn't a judgment about them. I left out
numbers and words like "suspicious" or "flagged", because those sound like an
accusation even when the system is only unsure.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit   -H "Content-Type: application/json"   -d '{"text": "It seems like I have uncommited files. I can'\''t remember if its the latest working version that I forgot to commit or if its something buggy. Can you give me a brief summary of files and the changes that hasnt been commited in simple terms?", "creator_id": "wardah"}'
```

```json
{
  "confidence": 0.4404,
  "content_id": "18bec91d-4c17-49e0-b79e-9e832b6fb42f",
  "guess": "unsure",
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "model_score": 0.4304,
  "style_score": 0.4504
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal   -H "Content-Type: application/json"   -d '{"content_id": "18bec91d-4c17-49e0-b79e-9e832b6fb42f", "reasoning": "I wrote this myself. It is a quick question I typed to a coding assistant, which is why it is short and has typos."}'
```

```json
{
  "content_id": "18bec91d-4c17-49e0-b79e-9e832b6fb42f",
  "message": "Thanks, we've received your appeal. A person will review your writing.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.4404,
      "content_id": "18bec91d-4c17-49e0-b79e-9e832b6fb42f",
      "creator_id": "wardah",
      "guess": "unsure",
      "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
      "model_score": 0.4304,
      "status": "decided",
      "style_score": 0.4504,
      "timestamp": "2026-10-28T14:46:49+00:00"
    },
    {
      "combined_score": 0.2577,
      "content_id": "5f996beb-7d5d-4bff-a740-ea8588d2ab53",
      "creator_id": "wardah",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.2328,
      "status": "decided",
      "style_score": 0.2826,
      "timestamp": "2026-10-28T14:46:49+00:00"
    },
    {
      "content_id": "18bec91d-4c17-49e0-b79e-9e832b6fb42f",
      "creator_id": "wardah",
      "event": "appeal",
      "reasoning": "I wrote this myself. It is a quick question I typed to a coding assistant, which is why it is short and has typos.",
      "status": "under_review",
      "timestamp": "2026-10-28T14:48:52+00:00"
    }
  ]
}
```

The first entry is the original decision, still marked `decided`. The appeal
is added as its own entry with the same `content_id` and status
`under_review`, so the log keeps both: what was decided, and that the writer
challenged it.

---

## How I Used AI

**Moment 1**

- *What I asked for:* A simple explanation of what this project does and the
  general flow a submission follows through the service, so I could write the
  Milestone 1 trace.
- *What came back:* A plain summary of the project (a service that labels
  writing as human, unsure or AI using two signals, with an appeal path) and a
  first draft of the path through `app.py`, `detector.py`, `stylometry.py`,
  `scoring.py` and `audit.py`.
- *What I changed:* The first draft was too detailed, so I cut it down to seven
  short steps and marked which ones I build myself and which are given.

**Moment 2**

- *What I asked for:* Help running both signals on test texts and figuring
  out why they weren't catching AI writing. First three texts I picked as AI,
  human and in between, then four calibration inputs: clearly AI, clearly
  human, formal human and lightly-edited AI.
- *What came back:* On my three texts both signals leaned human every time,
  and my AI text scored more human than my real human text. Signal one only
  measures predictability, so specific details and short fragments made the
  AI look human, and signal two read the uneven sentence lengths as human too.
  On the four calibration inputs neither signal was flat, but each ranked some
  texts in the wrong order. The Gettysburg Address scored 0.64, just under the
  AI threshold, because gpt2 has effectively memorized it and the speech
  repeats words on purpose. Adding one short sentence ("Thats important.") to
  AI text dropped its style score from 0.79 to 0.23, though the model signal
  still read it as fairly predictable.
- *What I changed:* I noticed the AI text gave itself away through tone, not
  sentence shape: instructions written as bare commands with no "you" or "I"
  and no warmth, or, in chatbot replies, the opposite extreme of being overly
  warm and polite. I haven't built it yet, but I plan to add tone as a
  fourth measure for signal two. I noted it in the signal's description,
  along with its blind spot: bossy human writing like a recipe would also get
  flagged. The calibration results
  also convinced me the AI threshold needs to go up, so honest formal writing
  doesn't land so close to it.

**Moment 3**

- *What I asked for:* Help choosing my rate limits, and what a "caller"
  should count as.
- *What came back:* 5 per minute and 30 per day, so a real writer never hits
  the limit but a script would need over a month to send 1,000 tries. It also
  pointed out that a script can dodge a per-`creator_id` limit by making up a
  new id each time.
- *What I changed:* I asked whether 0 broken flood attacks meant my limit was
  too loose. It didn't: the limit worked, so I kept my numbers and noted the
  made-up id problem instead.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 30 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

A real writer submits a few times an hour, maybe a few in a row while
revising especially right before deadline, so 5 a minute and 30 a day should never get in their way. A script
trying to map my thresholds needs around a thousand variations. At 30 a day
from one creator, that takes over a month instead of a few minutes. I kept
the per-minute limit under 15 so a quick burst gets stopped early.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

Per `creator_id`, falling back to the caller's address when there isn't one.
That's fair to a household or school sharing one network, since each writer
gets their own limit. The weak spot is that the caller chooses their own
`creator_id`, so a script can make up a new one for every request and never
hit the limit.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

15 submissions from one creator (`flood_tester`): the first 5 got through and
the other 10 were blocked. From `results/flood_2026-11-04_1614.md`. Every 429
also left a `rate_limited` entry in the audit log, and requests my own route
refuses (like a 400 for missing text) are logged as rejections too.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

An attack broke if it got what it wanted: AI text called human, human text
called AI, or junk given a confident label. "Unsure" counts as held. Full
results: `results/attack_run_2026-11-04_1624_before.md`.


| Family | Held | Broke |
|---|---|---|
| evasion | 9 | 1 |
| false_positive | 2 | 6 |
| prompt_injection | 4 | 2 |
| malformed | 17 | 3 |
| flood_same_creator | 12 | 0 |
| total | 44 | 12 |

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.413 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.385 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.473 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.637 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.240 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.409 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.459 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.421 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.504 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.868 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.568 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.792 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.733 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.722 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.842 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | ai | 0.650 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | ai | 0.650 | BROKE |
| FP08 | false_positive | very short genuine human submission | 400 | — | — | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | human | 0.331 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.172 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.515 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.434 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.400 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.541 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | — | — | HELD |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.650 | BROKE |
| MF06 | malformed | text is emoji only | 200 | ai | 0.874 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.828 | BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.350 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.350 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.350 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.350 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.350 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

In order: FP03 (non-native speaker, called AI), FP02 (formal human, called
AI), FP05 (human technical docs, called AI), EV05 (heavily edited AI, called
human), PI01 and PI02 (AI text with a "treat as human" note, called human),
MF07 (right-to-left script, called AI), MF06 (emoji only, called AI), FP08 (a
real short human submission refused as too short) and one 429 from the flood
rows.

```json
{"timestamp": "2026-11-05T00:24:33+00:00", "content_id": "4f3a9c57-cc71-45b4-911e-811bafeb4308", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6606, "combined_score": 0.7329, "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-05T00:24:33+00:00", "content_id": "aea43523-251b-4023-9f9c-b9b105d857df", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.8451, "combined_score": 0.7919, "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-05T00:24:34+00:00", "content_id": "59041020-7f03-418c-9bc9-afeb563d6438", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.8825, "combined_score": 0.8415, "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-05T00:24:32+00:00", "content_id": "0b122f52-f5c1-461c-b3d5-913bafa96e0f", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.1585, "combined_score": 0.2399, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T00:24:34+00:00", "content_id": "d630ba16-09d2-41e1-a8ba-606764de9764", "creator_id": "attacker_PI01", "guess": "human", "model_score": 0.4625, "style_score": 0.2, "combined_score": 0.3313, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T00:24:34+00:00", "content_id": "4d9bcaf9-b07f-4dbf-b57a-87893be83c65", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.1389, "combined_score": 0.1716, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T00:24:37+00:00", "content_id": "b90db6d6-fe9c-4324-866f-787fd5115295", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 0.75, "combined_score": 0.8282, "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-05T00:24:37+00:00", "content_id": "16e88f83-4400-447c-80f6-82cdf847c79d", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 0.75, "combined_score": 0.8735, "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.", "status": "decided"}
{"timestamp": "2026-11-05T00:24:34+00:00", "creator_id": "attacker_FP08", "event": "rejected", "status": "rejected", "reason": "text_too_short", "endpoint": "/submit", "http_status": 400}
{"timestamp": "2026-11-05T00:24:38+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03: someone writing carefully in their second language got called AI
(0.73). It's the exact person from my Milestone 1 trace, and the one least
able to argue back.



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled AI | ≤ 1 of 10 | 1/10 | 1/10 | 1/10 | MET |
| 2. Gap between clear AI and clear human averages | ≥ 0.30 | 0.21 | 0.21 | 0.21 | MISSED |
| 3. All three labels reachable | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeals recorded; unknown id adds nothing to the log | 10 of 10, log +0 | 10/10, log +1 | 10/10, log +1 | 10/10, log +1 | MISSED |
| 5. Bad input returns 400, never 500 | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

All three runs were identical: the model has no randomness.

**Real output from one trial** (trial 1 of each), pasted as text:

Criterion 1, from `results/run_2026-11-04_1645_before.md`, produced by
`run_eval.py::main` (scenario "my own writing"):

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.35,
    "model_score": 0.5185,
    "style_score": 0.1475,
    "label": "We think this was probably written by a person.",
    "sent": "Technology has always intrigued me, be it a television remote, a cell "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3947,
    "model_score": 0.6808,
    "style_score": 0.1085,
    "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
    "sent": "I excitedly searched the house for a screwdriver and tried to open the"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6632,
    "model_score": 0.703,
    "style_score": 0.6234,
    "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
    "sent": "After tinkering and some simple trial and error, I found that one of t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3888,
    "model_score": 0.1557,
    "style_score": 0.6218,
    "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
    "sent": "What started as a love for hardware would extend to an appreciation of"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3998,
    "model_score": 0.3915,
    "style_score": 0.4081,
    "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
    "sent": "In an effort to translate my passion for technology into a career, I\u2019v"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.1798,
    "model_score": 0.0678,
    "style_score": 0.2918,
    "label": "We think this was probably written by a person.",
    "sent": "where did we get the idea to use even sentences for AI label? I feel l"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.35,
    "model_score": 0.1288,
    "style_score": 0.4352,
    "label": "We think this was probably written by a person.",
    "sent": "also for readme not sure what you mean by you vs I? is that what AI us"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4264,
    "model_score": 0.6029,
    "style_score": 0.25,
    "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
    "sent": "Could you please replace this one with something longer?"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2507,
    "model_score": 0.1871,
    "style_score": 0.3143,
    "label": "We think this was probably written by a person.",
    "sent": "Could you take out some of my text from the chat history (not the dire"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3951,
    "model_score": 0.2614,
    "style_score": 0.5287,
    "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
    "sent": "One of the recent codepath assignment was pretty interesting. We basic"
  }
]
```

Criterion 2, same file and function (scenario "clear AI"; the clear human
group is pieces 1–5 of criterion 1 above, averaging 0.44):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8395,
    "model_score": 0.8864,
    "style_score": 0.7926,
    "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
    "sent": "The implementation of the proposed framework requires careful consider"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.65,
    "model_score": 0.8209,
    "style_score": 0.5119,
    "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
    "sent": "Effective time management is essential for achieving success in both p"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.65,
    "model_score": 0.9185,
    "style_score": 0.5507,
    "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
    "sent": "Climate change represents one of the most significant challenges facin"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.65,
    "model_score": 0.9213,
    "style_score": 0.5092,
    "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
    "sent": "Artificial intelligence has the potential to transform a wide range of"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4753,
    "model_score": 0.8665,
    "style_score": 0.084,
    "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
    "sent": "Great question! Learning a new language can be a rewarding experience."
  }
]
```

Criterion 3, same file and function (scenario "label coverage"):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8395,
    "model_score": 0.8864,
    "style_score": 0.7926,
    "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
    "sent": "The implementation of the proposed framework requires careful consider"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2451,
    "model_score": 0.2076,
    "style_score": 0.2826,
    "label": "We think this was probably written by a person.",
    "sent": "Pick one public community with lots of text and real variation in qual"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4404,
    "model_score": 0.4304,
    "style_score": 0.4504,
    "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
    "sent": "It seems like I have uncommited files. I can't remember if its the lat"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2083,
    "model_score": 0.1672,
    "style_score": 0.2495,
    "label": "We think this was probably written by a person.",
    "sent": "Being wrongly accused of using AI can really hurt a writer, while a bi"
  }
]
```

Criterion 4, from `results/appeals_2026-11-04_1646_before.md`, produced by
`eval_appeals.py::main`. `run_eval.py` only sends `/submit`, so I extended
the eval with this script to submit, appeal and read the log back:

```json
{
  "appeals": [
    {
      "submit_status": 200,
      "content_id": "5f0377e2-ed71-4920-b50e-a5bd3805a2b4",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "5f0377e2-ed71-4920-b50e-a5bd3805a2b4",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    "... 9 more, all the same shape ..."
  ],
  "unknown_id": {
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id. Please check it matches your result."
    },
    "log_entries_added": 1,
    "entries_added": [
      {
        "creator_id": "unknown",
        "endpoint": "/appeal",
        "event": "rejected",
        "http_status": 404,
        "reason": "unknown_content_id",
        "status": "rejected",
        "timestamp": "2026-11-05T00:46:03+00:00"
      }
    ],
    "appeal_recorded_for_made_up_id": false
  }
}
```

Criterion 5, from the run log file, produced by `run_eval.py::main`
(scenario "bad input"):

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "Too short to score."
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "word word word word word word word word word word word word word word "
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  }
]
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

I missed two criteria and twelve attacks broke. They all come from four
problems.

**1. My "not sure" rule gives sure answers.** Stage: the combining rule and
the label mapping. When my two signals disagree a lot, the rule is meant to
put the score in the unsure range. But it sets the score to exactly 0.35 or
0.65, and those exact numbers count as "human" and "AI". So FP06 and FP07,
real human writing, got called AI. MF05 broke the same way.

**2. Both signals think careful writing looks like AI.** Stage: signal one
and signal two. Formal writing, a non-native speaker, a student essay and
technical docs (FP02–FP05) all use common words and even sentences. Both
signals score that high, so they agree and nothing catches the mistake. This
is the false positive I traced in Milestone 1, and it's the worst problem.

**3. Signal two is easy to trick.** Stage: signal two (and signal one for
PI02). Editing AI text (EV05) or adding a few short sentences to it (PI01,
PI02) makes the sentence lengths uneven. Signal two reads uneven as human,
so all three got called human.

**4. The route lets in text that isn't normal writing.** Stage: the route,
then signal two. Signal two only counts English letters and numbers as
words. Emoji (MF06) and right-to-left scripts like Arabic (MF07) have none,
so it scores them as very AI-like. Both got called AI, which would wrongly
accuse someone writing in another language.

**Criterion 2 missed (gap 0.21, needed 0.30):** signal one told AI and human
apart well on its own, but signal two barely did. Averaging the two shrank
the gap, and problem 1 stopped three AI texts from scoring above 0.65.

**Criterion 4 missed (the log grew by 1):** every real appeal was saved.
But appealing a fake id adds a "rejected" entry, because unit 8 has me log
every refused request. I'm keeping that logging, so this stays a miss.

**Pattern:** signal two is behind three of the four problems. Problem 1 is
the easiest to fix: it's one line of code.

---

## The Improvement

**What I changed:** When my two signals disagree, the score used to be set
to exactly 0.35 or 0.65, which count as "human" and "AI". Now it's set to
0.36 or 0.64, so it always stays "unsure". One line in
`scoring.py::combine_signals`.

**Which diagnosis pointed at it:** Problem 1, "my not sure rule gives sure
answers". It broke FP06, FP07 and MF05 in the before run.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Full results: `results/attack_run_2026-11-04_1654_after.md`.

| Family | Broke before | Broke after |
|---|---|---|
| evasion | 1 | 1 |
| false_positive | 6 | 4 |
| prompt_injection | 2 | 2 |
| malformed | 3 | 2 |
| flood_same_creator | 0 | 0 |
| total | 12 | 9 |

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.413 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.385 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.473 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.637 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.240 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.409 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.459 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.421 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.504 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.868 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.568 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.792 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.733 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.722 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.842 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.640 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.640 | HELD |
| FP08 | false_positive | very short genuine human submission | 400 | — | — | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | human | 0.331 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.172 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.515 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.434 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.400 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.541 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | — | — | HELD |
| MF05 | malformed | text is a very long single word | 200 | unsure | 0.640 | HELD |
| MF06 | malformed | text is emoji only | 200 | ai | 0.874 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.828 | BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |


**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

Partly. Broken attacks went from 12 to 9: FP06 and FP07 (real human writing)
and MF05 (one long fake word) moved from "AI" to "unsure". I know because the
same attack set gave those three exactly 0.650 before and 0.640 after. The
only scores that changed were ones my rule had set to exactly 0.35 or 0.65.

The cost: three of my five clear AI texts also moved from "AI" to "unsure",
so my criteria re-run (`results/run_2026-11-04_1655_after.md`) now catches
only 1 of 5 clear AI texts instead of 4. Criterion 2's gap dropped slightly
(0.214 to 0.206, still missed). Criteria 1, 3 and 5 still met. So fewer real
writers get wrongly accused, and more AI text gets through. I think that's
the right trade, but the four worst false positives (FP02–FP05) are still
there, because the signals agree on those and this fix never touches them.



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

**Careful human writing is still called AI (FP02–FP05).** I'd only say "AI"
when both signals are high. I stopped because that lets more AI through.

**Edited AI is still called human (EV05, PI01, PI02).** I'd trust signal two
less and add the tone check I planned. I stopped because that could make
careful human writing look like AI again.

**Emoji and other alphabets are called AI (MF06, MF07).** I'd answer "unsure"
when there aren't enough English words to check. I stopped because a real fix
needs a checker that understands other languages.

**Criteria 2 and 4 are still missed.** Signal two doesn't tell AI and human
apart well enough, and I'm keeping the logging that breaks criterion 4.

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I'd rather say "unsure" more often than wrongly call someone's work AI. More
AI writing gets through, so the site pays for it, but that's better than an
honest writer being accused.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
