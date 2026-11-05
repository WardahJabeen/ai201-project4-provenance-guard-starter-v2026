# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 16:54
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `a0f64093-4f20-496c-bc65-bb57e9fb4ee7` | unsure | 0.413 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `e7e7f191-34ab-46b2-9c07-0dadb6fde81c` | unsure | 0.385 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c50e95e4-6394-46ce-9639-13797df80ae1` | unsure | 0.473 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `50b9debf-fc0d-40ad-b96e-da3fd6a174bb` | unsure | 0.637 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `80c9612f-27ff-476d-85ec-ea5537046942` | human | 0.240 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `7a44566f-a6ec-4da7-8bec-97c146545d3d` | unsure | 0.409 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `5195c0ec-9a05-49fe-a759-bdc0f55209f7` | unsure | 0.459 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `db02773e-08a5-47d4-87ef-b832f89c479a` | unsure | 0.421 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `bcf14150-7b29-4c80-a182-3d3e4f9cd18f` | unsure | 0.504 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `3762b9a4-ff1e-4855-a70e-b1cdff2bf1ec` | ai | 0.868 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `8931750e-5c4d-4f78-b531-3e0bd1804f19` | unsure | 0.568 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `5777f794-3ec5-44c8-bf8d-3d865e0f4c2b` | ai | 0.792 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `ae0629b7-8a14-4f29-bdd2-a247aa75590d` | ai | 0.733 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `53a7e51a-d686-412c-b744-856466b6164a` | ai | 0.722 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `c9d2b2b3-1fd8-4f1b-94cc-7a07a9b46eca` | ai | 0.842 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `f8877eae-022a-49a8-b499-d055166298df` | unsure | 0.640 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `12d296a7-d859-49f8-aa55-0bcb8068a7e9` | unsure | 0.640 | HELD |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `90030b24-36cc-4754-8cbd-5e207ac0369f` | human | 0.331 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `375936fd-c33e-4b0e-8920-5bd53f0052ff` | human | 0.172 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `55f6dce6-f6ae-4a8e-8fcb-44cd2901f0a1` | unsure | 0.515 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `84303dd3-1024-4b2c-9189-83bfef36560f` | unsure | 0.434 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `0e97bf8a-db05-4f55-aec0-fa93c0de692e` | unsure | 0.400 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `09546170-917d-4f25-8bce-bd2b22bcd524` | unsure | 0.541 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 200 | `c034697f-fbda-4fba-9bd7-2c63ff0b0050` | unsure | 0.640 | HELD |
| MF06 | malformed | text is emoji only | 200 | `7d325469-086d-40d8-9768-9c8df03a0373` | ai | 0.874 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `1ae27cfc-338d-4125-b09d-de8955cc23a7` | ai | 0.828 | BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a5dfbb21-22e5-44c6-a236-7787ee1b891f` | unsure | 0.360 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b19c9b18-c90e-4e6a-8d8f-c5c8c5462ad9` | unsure | 0.360 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c873607a-770f-43c3-8c10-c022be719d5c` | unsure | 0.360 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e03da122-105b-427d-90e9-85f8912c1f05` | unsure | 0.360 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e45986cb-e8fe-4963-b0ec-f01cf4fde296` | unsure | 0.360 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "a0f64093-4f20-496c-bc65-bb57e9fb4ee7",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4127,
  "model_score": 0.1635,
  "style_score": 0.6618,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "e7e7f191-34ab-46b2-9c07-0dadb6fde81c",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3853,
  "model_score": 0.5943,
  "style_score": 0.1762,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c50e95e4-6394-46ce-9639-13797df80ae1",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4735,
  "model_score": 0.6662,
  "style_score": 0.2807,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "50b9debf-fc0d-40ad-b96e-da3fd6a174bb",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6371,
  "model_score": 0.6114,
  "style_score": 0.6628,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "80c9612f-27ff-476d-85ec-ea5537046942",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2399,
  "model_score": 0.3212,
  "style_score": 0.1585,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "7a44566f-a6ec-4da7-8bec-97c146545d3d",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4089,
  "model_score": 0.5727,
  "style_score": 0.2452,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "5195c0ec-9a05-49fe-a759-bdc0f55209f7",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4591,
  "model_score": 0.5862,
  "style_score": 0.3319,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "db02773e-08a5-47d4-87ef-b832f89c479a",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4208,
  "model_score": 0.2452,
  "style_score": 0.5964,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "bcf14150-7b29-4c80-a182-3d3e4f9cd18f",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5036,
  "model_score": 0.7042,
  "style_score": 0.303,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "3762b9a4-ff1e-4855-a70e-b1cdff2bf1ec",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8684,
  "model_score": 0.9792,
  "style_score": 0.7576,
  "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "8931750e-5c4d-4f78-b531-3e0bd1804f19",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5681,
  "model_score": 0.6175,
  "style_score": 0.5187,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "5777f794-3ec5-44c8-bf8d-3d865e0f4c2b",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7919,
  "model_score": 0.7387,
  "style_score": 0.8451,
  "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "ae0629b7-8a14-4f29-bdd2-a247aa75590d",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7329,
  "model_score": 0.8051,
  "style_score": 0.6606,
  "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "53a7e51a-d686-412c-b744-856466b6164a",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7215,
  "model_score": 0.8329,
  "style_score": 0.6101,
  "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c9d2b2b3-1fd8-4f1b-94cc-7a07a9b46eca",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8415,
  "model_score": 0.8005,
  "style_score": 0.8825,
  "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "f8877eae-022a-49a8-b499-d055166298df",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.8814,
  "style_score": 0.517,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "12d296a7-d859-49f8-aa55-0bcb8068a7e9",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.8816,
  "style_score": 0.4653,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "90030b24-36cc-4754-8cbd-5e207ac0369f",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.3313,
  "model_score": 0.4625,
  "style_score": 0.2,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "375936fd-c33e-4b0e-8920-5bd53f0052ff",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1716,
  "model_score": 0.2044,
  "style_score": 0.1389,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "55f6dce6-f6ae-4a8e-8fcb-44cd2901f0a1",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5146,
  "model_score": 0.5943,
  "style_score": 0.4348,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "84303dd3-1024-4b2c-9189-83bfef36560f",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4339,
  "model_score": 0.4998,
  "style_score": 0.368,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "0e97bf8a-db05-4f55-aec0-fa93c0de692e",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4004,
  "model_score": 0.6401,
  "style_score": 0.1607,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "09546170-917d-4f25-8bce-bd2b22bcd524",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5414,
  "model_score": 0.5583,
  "style_score": 0.5245,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c034697f-fbda-4fba-9bd7-2c63ff0b0050",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.9976,
  "style_score": 0.45,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "7d325469-086d-40d8-9768-9c8df03a0373",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.8735,
  "model_score": 0.9969,
  "style_score": 0.75,
  "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "1ae27cfc-338d-4125-b09d-de8955cc23a7",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.8282,
  "model_score": 0.9064,
  "style_score": 0.75,
  "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "a5dfbb21-22e5-44c6-a236-7787ee1b891f",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "b19c9b18-c90e-4e6a-8d8f-c5c8c5462ad9",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c873607a-770f-43c3-8c10-c022be719d5c",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "e03da122-105b-427d-90e9-85f8912c1f05",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "e45986cb-e8fe-4963-b0ec-f01cf4fde296",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We can't tell whether this was written by a person or with help from AI. Lots of people's own writing lands here, so this isn't a judgment about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
