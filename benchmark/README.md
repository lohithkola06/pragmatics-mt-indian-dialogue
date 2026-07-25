# Benchmark

The pragmatics-preserving MT benchmark: schema, guidelines, examples, pilot data
and dataset splits.

> **Current status: pilot construction.** 47 draft items exist and validate
> against the schema. **No native-speaker review, annotation, or agreement
> measurement has taken place.** Nothing here is validated ground truth.

---

## What this benchmark measures

Whether a translation preserves the **social and communicative meaning** of an
utterance, not just its propositional content.

> A pragmatic failure occurs when a translation preserves the basic semantic
> content of an utterance but fails to preserve its intended social or
> communicative meaning in context.

Semantic adequacy and pragmatic preservation are scored **separately**. A
translation that scores 3 for accuracy and 0 for politeness is exactly the case
this benchmark exists to find.

**Language setting:** Hindi and Hinglish → English, treated as two distinct values.
See [../docs/project/language_scope_decision.md](../docs/project/language_scope_decision.md).

**Categories:** politeness and formality · indirect requests and refusals · stance
and emotion · discourse-motivated code-switching.

---

## Directory layout

```text
benchmark/
├── schema/        field definitions, JSON Schema, label and severity guidelines
├── guidelines/    documents given to annotators and evaluators
├── examples/      worked examples with field-by-field explanations
├── pilot/         the 47-item pilot dataset, templates, plan and issues log
└── data/          dataset splits (empty until the pilot is validated)
```

### `schema/`

| File | Contents |
|---|---|
| [item_schema.json](schema/item_schema.json) | JSON Schema draft 2020-12. What validation enforces |
| [annotation_schema.md](schema/annotation_schema.md) | Every field: type, allowed values, examples, notes |
| [label_definitions.md](schema/label_definitions.md) | Every label: definition, example, confusions, when not to use |
| [severity_guidelines.md](schema/severity_guidelines.md) | `MINOR` / `MAJOR` / `CRITICAL` with worked examples |
| [schema_version.md](schema/schema_version.md) | Version history and open questions |

### `guidelines/`

| File | For | Covers |
|---|---|---|
| [annotation_guidelines.md](guidelines/annotation_guidelines.md) | Annotators | The complete annotation task |
| [contrastive_item_guidelines.md](guidelines/contrastive_item_guidelines.md) | Item writers, reviewers | Building valid contrastive negatives |
| [adjudication_guidelines.md](guidelines/adjudication_guidelines.md) | Adjudicators | Resolving and preserving disagreement |
| [human_evaluation_guidelines.md](guidelines/human_evaluation_guidelines.md) | Evaluators | Rating system output |
| [annotator_training.md](guidelines/annotator_training.md) | Annotators | Lesson, 10 exercises, readiness checklist |

**Start with** `annotation_guidelines.md`, then `annotator_training.md`.

### `examples/`

[example_items.jsonl](examples/example_items.jsonl) holds four complete items, one
per category, extracted verbatim from the pilot set.
[example_explanations.md](examples/example_explanations.md) walks through each one
field by field. [contrastive_examples.jsonl](examples/contrastive_examples.jsonl)
gives ten contrastive examples — five valid, five deliberately invalid — as
training material.

### `pilot/`

The 47-item pilot dataset with its plan, issues log, statistics and CSV templates.
See [pilot/README.md](pilot/README.md).

### `data/`

`raw/`, `processed/`, `development/` and `test/` are empty placeholders. Splits are
created only after pilot validation. When they are, **minimal-pair partners must
stay in the same split** to prevent leakage.

---

## The item format

One JSON object per line, UTF-8. Items carry 43 fields in six groups:

| Group | Fields |
|---|---|
| Identity and provenance | `item_id`, `language`, `source_type`, `license`, `review_status`, … |
| Dialogue structure | `context` (0–3 turns), `source_utterance`, `relationship`, `relative_status`, `familiarity`, … |
| Pragmatic labels | `primary_phenomenon`, `speech_act`, `politeness_level`, `formality_level`, `stance`, `emotion`, `indirectness`, `code_switch_function` |
| Context metadata | `context_status`, `minimum_context_window`, `relevant_context_turns`, … |
| Translation data | `reference_translations`, `contrastive_translation`, `contrastive_error_category`, `severity`, … |
| Annotation metadata | `annotator_ids`, `adjudicator_id`, `agreement_status`, … |

Full reference: [schema/annotation_schema.md](schema/annotation_schema.md).

---

## Commands

Run from the repository root. Requires Python 3.9+ with `jsonschema` installed
(`python -m pip install -r requirements.txt`).

```bash
python scripts/validate_schema.py
python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl
python scripts/validate_jsonl.py benchmark/examples/example_items.jsonl
python scripts/generate_dataset_statistics.py benchmark/pilot/pilot_items_v1.jsonl
python scripts/create_annotation_sheet.py benchmark/pilot/pilot_items_v1.jsonl
python -m unittest discover scripts/tests
```

See [../scripts/README.md](../scripts/README.md) for full options.

---

## Adding an item

1. Write the source utterance and 0–3 context turns.
2. Assign an `item_id` whose language and category codes match the item's labels.
3. Fill in the pragmatic labels using
   [label_definitions.md](schema/label_definitions.md).
4. Judge `context_status` with the cover-the-context test.
5. Write the reference translation, then the contrastive translation per
   [contrastive_item_guidelines.md](guidelines/contrastive_item_guidelines.md).
6. Assign `severity` per [severity_guidelines.md](schema/severity_guidelines.md).
7. Set `review_status: NEEDS_NATIVE_REVIEW` and leave the annotation metadata at
   its unannotated defaults.
8. Run `python scripts/validate_jsonl.py <file>`.
9. Send for independent native-speaker review.

Step 9 is not optional. Validation checks structure, not quality.

---

## Rules

- **`review_status: APPROVED` may only be set by a native speaker.** Draft items
  start at `NEEDS_NATIVE_REVIEW`.
- **`NATURAL` and `ADAPTED` items require a real, citable `source_reference`** and
  a checked licence. `license` stays `TO_BE_CONFIRMED` until it has been verified.
- **Never record real personal information** in `annotator_ids` or
  `adjudicator_id`. Pseudonymous identifiers only.
- **Never report fabricated agreement figures.** The tooling reports insufficient
  data rather than estimating, and that output should be reported as-is.
- **Preserve genuine disagreement.** Where multiple readings are defensible, record
  both rather than forcing consensus.
- **Avoid offensive, stereotyped, political, religious, sexual or otherwise
  sensitive content** in elicited examples. Medical settings are limited to
  ordinary scheduling and politeness, never medical advice.

---

## Background

Design rationale is in
[../docs/project/benchmark_blueprint.md](../docs/project/benchmark_blueprint.md);
research questions in
[../docs/project/research_questions.md](../docs/project/research_questions.md).

The contrastive-pair method follows Bawden et al. (2018) and Voita, Sennrich &
Titov (2019); the separation of semantic from pragmatic scoring follows the finding
that a translation can be individually good and wrong in context. Notes on all
seven reviewed papers are in [../docs/literature/](../docs/literature/).
