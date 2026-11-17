# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Few false accusations on my own writing

Of 10 pieces I wrote myself, at least 3 of them written plainly (short
sentences, everyday words, no unusual vocabulary), at most 1
is labelled high-confidence AI, in every one of the three trials.

**Why this target:** Being wrongly accused of using AI can really hurt a
writer, while a bit of AI text slipping through costs the site much less. So I
allow at most 1 mistake in 10. I'm including plain writing on purpose, because
that's the kind my first signal struggles with, and I'd rather see the problem
than hide it behind my most polished work.

---

## 2. Clear gap between AI and human scores

The average combined score of 5 clearly AI-generated texts is at least 0.30
higher than the average of 5 clearly human-written texts, in every trial.

**Why this target:** If clearly human and clearly AI writing end up with
similar scores, wherever I draw the line is basically a guess. A gap of 0.30
is about the width of my unsure band (0.35 to 0.65), so the clear cases should
land comfortably on either side of it.

---

## 3. All three labels are reachable

Across my label-coverage inputs, each of the three labels (human, unsure,
AI) is produced at least once, in every trial.

**Why this target:** A label that never shows up isn't doing anything, and it
usually means my score ranges have a gap. I especially want to see the human
label, because without it an honest writer could never be fully cleared, only
told "we're not sure" at best.

---

## 4. Every appeal is recorded

10 of 10 appeals on real `content_id`s return 200, change the status to
`under_review` and add an appeal entry to the log. An appeal with an unknown
`content_id` returns 404 and the log's entry count doesn't change.

**Why this target:** When the system gets it wrong, an appeal is the only way
a writer can speak up. Losing even one would mean someone asked to be heard and
nobody listened, so every single appeal needs to be recorded.

---

## 5. Bad input never crashes the service

Of 5 bad requests (missing `text`, empty `text`, `text` under 50 characters,
`text` over 10,000 characters, `text` set to null), 5 of 5 return a 400
with an error message and 0 return a 500.

**Why this target:** If the service crashes, the writer is left with no idea
what went wrong, and so am I. Mistakes like an empty box or a huge paste are
easy to make, so each one should get a clear, friendly answer instead.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone criteria

---

## 1. A failed model still gives an answer, and never an accusation

With each of the faults `crash`, `nan` and `range`, 3 submissions (9 in total): 9 of 9 return 200 with `degraded: true` and the matching `model_status` (`error` for crash, `bad_score` for nan and range), and 0 of 9 are labelled AI.

**Why this target:** Before this extension, a crash gave the writer a 500 and nothing else, so every single one should now get an answer. None may say AI, because that answer only has the style check behind it, and one weak check isn't enough to accuse someone. One wrong accusation costs a writer far more than a missed AI text costs the site. It can't be 8 of 9, because the one that failed would be a writer who got a 500, or an accusation backed by a single weak check: exactly what this extension exists to stop.

---

## 2. Every request leaves a log line with its timing

20 requests, each from a different `creator_id`: 10 normal submissions, 5 with bad input (missing, empty or too-short text), then 5 more after restarting with the `crash` fault. 20 of 20 add exactly one log line with a `timestamp` and
`duration_ms`. The 15 that got a result also have `model_status` and `text_chars`, and the 5 rejected ones have a `reason`. Each `duration_ms` is within 100 ms of the time measured by the client.

**Why this target:** The log is the only record of what happened, so it's how I'd find a problem later, and it's where my cost number comes from. A request with no log line is invisible, so it has to be all 20, including the failures. I allow 100 ms because the client also counts sending and receiving the request, which the service can't see. A normal run takes about 180 ms, so a gap bigger than 100 ms would mean `duration_ms` is missing a real part of the work, and my cost number would be wrong.

---

## 3. After 3 failures, answers come straight back

With the `hang` fault, after 3 timed-out submissions, the next 5 submissions (sent within 60 seconds, each from a different `creator_id` so the rate limit doesn't get in the way) each return 200 with `model_status: "skipped"` in
under 1 second. The first submission sent more than 60 seconds later tries the model again: its `model_status` is `timeout`, not `skipped`.

**Why this target:** A normal run takes about 0.18 seconds, so 1 second leaves plenty of room while still being 10 times faster than waiting out the time limit. The second part matters just as much: if the model were never tried
again, one bad minute would turn the model off for good, and every writer after that would only get the weaker style-only answer.

---

## 4. A result that can't be saved is never handed out

With the `log` fault, 5 submissions and 1 appeal (on a `content_id` saved earlier): 6 of 6 return 503 with `log_unavailable`, 0 return a label or `under_review`, and the number of lines in `logs/audit.jsonl` doesn't change.

**Why this target:** `/appeal` finds a submission through the log. A result that wasn't saved can never be appealed, so a writer labelled AI would have no way to argue back. An appeal that wasn't saved would never be reviewed. Both
have to be 6 of 6, because one unsaved result is one writer with no way out.

---

## 5. Many writers at once while the model is stuck

With the `hang` fault, after one warm-up submission so the model is already loaded, 8 submissions sent at the same moment (each from a different `creator_id`): 8 of 8 return 200 with a style-only answer, each in no more than 12 seconds.

**Why this target:** The model runs on only 4 worker threads, so 8 at once is twice what it can handle. If the model breaks while the site is busy, everyone is hit at the same time, not one at a time. The time limit is 10 seconds, and I allow 2 more for the style check and the reply. A writer shouldn't wait longer than that just because others submitted at the same moment. I haven't tested this case, and it's the one most likely to miss.
