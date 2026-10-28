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

**What it measures:** The shape and tone of the text, without reading it. It
looks at how much sentence lengths vary, how often words repeat (type-token
ratio: unique words divided by total words), how much punctuation is used and
the tone: how bossy or how warm the text sounds (bare commands with no "you"
or "I", short fragments, and softening words like "maybe" or "I think"). These
combine into a `style_score` (higher = more AI).

**Why that might differ between human and AI writing:** AI often writes even,
medium-length sentences with a narrower vocabulary, because picking the most
likely word keeps landing on the same common ones. Its tone also tends to sit
at one of two extremes: clipped and instructional, like it's giving orders, or
overly warm and polite. Human writing is more uneven, in both sentence shape
and tone.

**What it can't see:** What the text actually says or who wrote it. It only
counts surface features, so cheap edits like adding typos, mixing very short
and long sentences or throwing in "I think" can make AI text look human. Tone
is also a matter of what kind of writing something is: a teacher's handout or
a recipe sounds bossy and was written by a person, and some AI writes in a
lively, uneven style. My own AI sample ("Two rules. Public only...") had very
uneven sentences, so sentence length alone would have called it human.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



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
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Pick one public community with lots of text and real variation in quality. Sports forums, music discussion boards, film communities, and gaming subreddits all work. You need to be able to collect 200 public posts from it.", "creator_id": "wardah"}'
```

```json
{
  "confidence": null,
  "content_id": "31992622-7747-4c98-827b-0cf644da8778",
  "guess": "unsure",
  "label": "PLACEHOLDER label",
  "model_score": 0.2389,
  "style_score": null
}
```

<!-- Milestone 3: only signal one is wired in. confidence, label and
     style_score are placeholders until Milestones 4 and 5. -->

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

<!-- /appeal is built in Milestone 5. -->

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": null,
      "content_id": "326bb046-83dd-40cc-aa44-6913f6d75f79",
      "creator_id": "wardah",
      "guess": "unsure",
      "label": "PLACEHOLDER label",
      "model_score": 0.1605,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-10-28T14:10:20+00:00"
    },
    {
      "combined_score": null,
      "content_id": "31992622-7747-4c98-827b-0cf644da8778",
      "creator_id": "wardah",
      "guess": "unsure",
      "label": "PLACEHOLDER label",
      "model_score": 0.2389,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-10-28T14:15:57+00:00"
    }
  ]
}
```

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

- *What I asked for:* Help running signal one on three texts I picked as AI,
  human and in between, and understanding the results.
- *What came back:* All three leaned human (AI 0.23, human 0.43, in between
  0.17, where higher means more AI). The AI text even scored more human than my
  real human text. The explanation was that signal one only measures
  predictability: short fragments, dashes and specific details are hard for
  gpt2 to predict, so lively AI writing looks human. The starter code's idea for
  signal two was that AI writes even, medium-length sentences, but my AI sample
  had very uneven ones, so that wouldn't have caught it either.
- *What I changed:* I noticed the AI text gave itself away through tone, not
  sentence shape: instructions written as bare commands with no "you" or "I"
  and no warmth, or, in chatbot replies, the opposite extreme of being overly
  warm and polite. I added tone as a fourth measure for signal two and updated
  its blind spots, since bossy human writing like a recipe would also get
  flagged.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

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
