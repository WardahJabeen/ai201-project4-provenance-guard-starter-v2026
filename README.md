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
  is kept between 0.35 and 0.65, the unsure band)

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



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
