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
