# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 16:24
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `c38b6673-db34-412c-9986-78439160013e` | unsure | 0.413 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `b8c621d6-4881-419e-a159-b9d8bb048176` | unsure | 0.385 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c9c73224-eff3-455b-82ac-c73cdf85dd90` | unsure | 0.473 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `346b38bc-8d1d-486d-833a-d8e3db281ef9` | unsure | 0.637 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `0b122f52-f5c1-461c-b3d5-913bafa96e0f` | human | 0.240 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `29369bca-cbf7-4997-bd94-0d9f39acfc35` | unsure | 0.409 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `e8924cb0-1951-4840-a1f1-e8acc353960e` | unsure | 0.459 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `530a8925-7879-42f1-a35c-4352261bfdc0` | unsure | 0.421 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `bc9b5b88-62f3-421c-ad80-c1daf92bc4a8` | unsure | 0.504 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `841897ee-3de7-44a9-b3ea-07924bf4012d` | ai | 0.868 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `fb8a255f-4872-403e-8864-797b4e8c1fa6` | unsure | 0.568 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `aea43523-251b-4023-9f9c-b9b105d857df` | ai | 0.792 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `4f3a9c57-cc71-45b4-911e-811bafeb4308` | ai | 0.733 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `b8094cee-4040-4426-a43e-5b111fa535d7` | ai | 0.722 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `59041020-7f03-418c-9bc9-afeb563d6438` | ai | 0.842 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `4154f02c-2499-452c-8049-21748f645640` | ai | 0.650 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `87a7f7ed-083b-4579-8234-945b85798622` | ai | 0.650 | BROKE |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `d630ba16-09d2-41e1-a8ba-606764de9764` | human | 0.331 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `4d9bcaf9-b07f-4dbf-b57a-87893be83c65` | human | 0.172 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `dd32bccf-c96f-4fac-a976-070be28a34a4` | unsure | 0.515 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `ee3f1c0d-6cb9-446d-8c62-7a6d4f4c99af` | unsure | 0.434 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `92393782-846b-4bc6-8979-ca1cc554d0e5` | unsure | 0.400 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `f442b7e1-ec65-442b-814e-d0eae5c86df0` | unsure | 0.541 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 200 | `ecbb0f65-e680-4a12-bb9c-1f7dc299ec8f` | ai | 0.650 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `16e88f83-4400-447c-80f6-82cdf847c79d` | ai | 0.874 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `b90db6d6-fe9c-4324-866f-787fd5115295` | ai | 0.828 | BROKE |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4a2f4a73-0670-49ec-b80d-d7ea108e4a49` | human | 0.350 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `45c2e65e-7ab8-43db-80be-6a98de9ee967` | human | 0.350 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fe2fc06a-7818-4456-bf85-d16ef935bffd` | human | 0.350 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d1aef779-e7b7-407e-8f24-0c160a5e5ba2` | human | 0.350 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3dfe253d-147f-41d8-b7a7-b8dcbae4d943` | human | 0.350 | HELD |
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
  "content_id": "c38b6673-db34-412c-9986-78439160013e",
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
  "content_id": "b8c621d6-4881-419e-a159-b9d8bb048176",
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
  "content_id": "c9c73224-eff3-455b-82ac-c73cdf85dd90",
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
  "content_id": "346b38bc-8d1d-486d-833a-d8e3db281ef9",
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
  "content_id": "0b122f52-f5c1-461c-b3d5-913bafa96e0f",
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
  "content_id": "29369bca-cbf7-4997-bd94-0d9f39acfc35",
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
  "content_id": "e8924cb0-1951-4840-a1f1-e8acc353960e",
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
  "content_id": "530a8925-7879-42f1-a35c-4352261bfdc0",
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
  "content_id": "bc9b5b88-62f3-421c-ad80-c1daf92bc4a8",
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
  "content_id": "841897ee-3de7-44a9-b3ea-07924bf4012d",
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
  "content_id": "fb8a255f-4872-403e-8864-797b4e8c1fa6",
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
  "content_id": "aea43523-251b-4023-9f9c-b9b105d857df",
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
  "content_id": "4f3a9c57-cc71-45b4-911e-811bafeb4308",
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
  "content_id": "b8094cee-4040-4426-a43e-5b111fa535d7",
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
  "content_id": "59041020-7f03-418c-9bc9-afeb563d6438",
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
  "content_id": "4154f02c-2499-452c-8049-21748f645640",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.65,
  "model_score": 0.8814,
  "style_score": 0.517,
  "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
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
  "content_id": "87a7f7ed-083b-4579-8234-945b85798622",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.65,
  "model_score": 0.8816,
  "style_score": 0.4653,
  "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
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
  "content_id": "d630ba16-09d2-41e1-a8ba-606764de9764",
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
  "content_id": "4d9bcaf9-b07f-4dbf-b57a-87893be83c65",
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
  "content_id": "dd32bccf-c96f-4fac-a976-070be28a34a4",
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
  "content_id": "ee3f1c0d-6cb9-446d-8c62-7a6d4f4c99af",
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
  "content_id": "92393782-846b-4bc6-8979-ca1cc554d0e5",
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
  "content_id": "f442b7e1-ec65-442b-814e-d0eae5c86df0",
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
  "content_id": "ecbb0f65-e680-4a12-bb9c-1f7dc299ec8f",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.65,
  "model_score": 0.9976,
  "style_score": 0.45,
  "label": "We think this was probably written with help from AI. Our check can get this wrong, especially with plain or simple writing. If you wrote it yourself, you can ask for a person to review it.",
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
  "content_id": "16e88f83-4400-447c-80f6-82cdf847c79d",
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
  "content_id": "b90db6d6-fe9c-4324-866f-787fd5115295",
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
  "content_id": "4a2f4a73-0670-49ec-b80d-d7ea108e4a49",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.35,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We think this was probably written by a person.",
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
  "content_id": "45c2e65e-7ab8-43db-80be-6a98de9ee967",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.35,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We think this was probably written by a person.",
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
  "content_id": "fe2fc06a-7818-4456-bf85-d16ef935bffd",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.35,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We think this was probably written by a person.",
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
  "content_id": "d1aef779-e7b7-407e-8f24-0c160a5e5ba2",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.35,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We think this was probably written by a person.",
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
  "content_id": "3dfe253d-147f-41d8-b7a7-b8dcbae4d943",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.35,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We think this was probably written by a person.",
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
