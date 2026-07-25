# Pilot Dataset

The first 47-item pilot for the pragmatics-preserving MT benchmark.

> **Status: draft, not validated.** Every item carries
> `review_status: NEEDS_NATIVE_REVIEW`. The items were written during repository
> construction and **no native speaker has reviewed them, no annotation has taken
> place, and no agreement has been measured.** Do not cite any number from this
> directory as a result.

---

## Files

| File | What it is | Generated? |
|---|---|---|
| [pilot_items_v1.jsonl](pilot_items_v1.jsonl) | The 47 draft items, one JSON object per line | hand-written |
| [pilot_plan.md](pilot_plan.md) | Objectives, procedure, acceptance criteria, timeline | hand-written |
| [pilot_issues.md](pilot_issues.md) | Known problems and open questions | hand-written |
| [pilot_statistics.md](pilot_statistics.md) | Composition report | **generated** |
| [pilot_annotation_template.csv](pilot_annotation_template.csv) | Column format for translation rating | hand-written |
| [pilot_item_review_template.csv](pilot_item_review_template.csv) | Column format for item review | hand-written |
| [pilot_adjudication_template.csv](pilot_adjudication_template.csv) | Column format for adjudication decisions | hand-written |
| `pilot_annotation_sheet.csv` | Ready-to-use annotation sheet, 94 candidate rows | **generated** |

Generated files can be rebuilt at any time; see [Commands](#commands). The CSV
templates each carry two clearly marked demonstration rows — delete them before
use.

---

## Composition

47 items. Full breakdown in [pilot_statistics.md](pilot_statistics.md).

| Category | Items | | Language | Items | | Source type | Items |
|---|---:|---|---|---:|---|---|---:|
| Politeness and formality | 14 | | Hindi | 26 | | `ELICITED` | 35 |
| Indirect requests/refusals | 14 | | Hinglish | 21 | | `MINIMAL_PAIR` | 12 |
| Stance and emotion | 12 | | | | | `NATURAL` | 0 |
| Code-switching | 7 | | | | | `ADAPTED` | 0 |

There are no `NATURAL` or `ADAPTED` items because provenance and licensing could
not be documented. See [pilot_issues.md](pilot_issues.md) issue 3.

### Context dependence

| Context status | Items | Share |
|---|---:|---:|
| `REQUIRED` | 22 | 46.8% |
| `HELPFUL` | 17 | 36.2% |
| `NOT_REQUIRED` | 8 | 17.0% |

The eight `NOT_REQUIRED` items are the **control group**. Each carries zero context
turns and is interpretable entirely on its own, with its pragmatic load held in
honorific morphology, discourse particles, or conventional indirectness rather than
in the surrounding dialogue. They exist so that a context-aware system's advantage
on the `REQUIRED` items can be distinguished from its general capability.

---

## Item ID scheme

```text
HIN_POL_001
│   │   └── serial, unique within language + category
│   └────── POL politeness/formality · IND indirect request/refusal
│           STA stance/emotion       · CSW code-switching
└────────── HIN Hindi · HNG Hinglish
```

The ID must agree with the item's own `language` and `primary_phenomenon` fields;
`validate_jsonl.py` rejects any item where it does not.

---

## Commands

Run all commands from the repository root.

```bash
# Check the schema itself is valid
python scripts/validate_schema.py

# Validate every pilot item
python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl

# Regenerate the statistics report
python scripts/generate_dataset_statistics.py benchmark/pilot/pilot_items_v1.jsonl \
    --out benchmark/pilot/pilot_statistics.md

# Build the annotation sheet (blind: hides which candidate is the reference)
python scripts/create_annotation_sheet.py benchmark/pilot/pilot_items_v1.jsonl --blind

# Measure agreement, once annotators have filled a sheet in
python scripts/calculate_agreement.py <completed sheet>.csv
```

`--blind` writes the answer key to a separate `.key.csv` file. **Keep it away from
annotators.**

---

## Annotation workflow

1. **Recruit** at least two native-speaker annotators and one adjudicator who does
   not annotate.
2. **Train** — annotators read
   [annotation_guidelines.md](../guidelines/annotation_guidelines.md) and work
   through [annotator_training.md](../guidelines/annotator_training.md).
3. **Review the items** using `pilot_item_review_template.csv`, *before* any
   rating. Items that fail review are fixed or rejected first, so annotator effort
   is not spent on items that will be discarded.
4. **Calibrate** on 5 items, then compare.
5. **Rate** the remaining candidates using the generated annotation sheet.
6. **Measure agreement** on the pre-adjudication annotations.
7. **Adjudicate** per
   [adjudication_guidelines.md](../guidelines/adjudication_guidelines.md).
8. **Record dispositions** — update `review_status` on each item and revalidate.

Full detail in [pilot_plan.md](pilot_plan.md).

**Annotators must work independently.** Agreement is computed on independent
judgements; discussing individual items inflates it and makes the reliability
estimate meaningless.

---

## Handling annotator identity

Use pseudonymous identifiers only — `ANN_01`, `ANN_02`, `ADJ_01`. The mapping to
real people is kept **outside this repository**. Real names must never appear in
`annotator_ids`, `adjudicator_id`, or any committed CSV.

---

## What must not be done with this data

- **Do not mark any item `APPROVED`** without native-speaker review. Only a native
  speaker may set that status.
- **Do not report agreement figures** until annotation has happened.
  `calculate_agreement.py` reports insufficient data rather than estimating, and
  that output should be taken at face value.
- **Do not treat the labels as ground truth.** They are the item author's intent,
  and the pilot exists partly to test whether that intent is recoverable.
- **Do not add `NATURAL` or `ADAPTED` items** without a real, citable source and a
  checked licence.
