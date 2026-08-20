# Week 2 Deliverables

## Project Title

**Pragmatics-Preserving Machine Translation for Indian Dialogue**

This is the checklist of what Week 2 was meant to produce, what exists, and what
still needs a person. Repository work is separated from work that requires native
speakers, because conflating the two is exactly the mistake that would make this
project look further along than it is.

---

## 1. Language decision

| # | Deliverable | Path | Status |
|---|---|---|---|
| 1.1 | Language scope decision | [../../project/language_scope_decision.md](../../project/language_scope_decision.md) | Complete |

Covers the selected direction, the reasoning, what counts as Hindi, what counts as
Hinglish, exclusions, regional limitations, and how Telugu could be added. States
explicitly that the choice is **not** representative of Indian languages generally.

---

## 2. Schema

| # | Deliverable | Path | Status |
|---|---|---|---|
| 2.1 | Machine-readable schema | [../../../benchmark/schema/item_schema.json](../../../benchmark/schema/item_schema.json) | Complete |
| 2.2 | Field documentation | [../../../benchmark/schema/annotation_schema.md](../../../benchmark/schema/annotation_schema.md) | Complete |
| 2.3 | Label definitions | [../../../benchmark/schema/label_definitions.md](../../../benchmark/schema/label_definitions.md) | Complete |
| 2.4 | Severity guidelines | [../../../benchmark/schema/severity_guidelines.md](../../../benchmark/schema/severity_guidelines.md) | Complete |
| 2.5 | Version history | [../../../benchmark/schema/schema_version.md](../../../benchmark/schema/schema_version.md) | Complete |

Schema `0.1.0`: JSON Schema draft 2020-12, 43 properties, all required, 19
controlled-vocabulary fields, 4 conditional rules. Every deviation from the Week 1
blueprint is recorded in 2.5 with a reason.

---

## 3. Guidelines

| # | Deliverable | Path | Status |
|---|---|---|---|
| 3.1 | Annotation guidelines | [../../../benchmark/guidelines/annotation_guidelines.md](../../../benchmark/guidelines/annotation_guidelines.md) | Complete |
| 3.2 | Contrastive item guidelines | [../../../benchmark/guidelines/contrastive_item_guidelines.md](../../../benchmark/guidelines/contrastive_item_guidelines.md) | Complete |
| 3.3 | Adjudication guidelines | [../../../benchmark/guidelines/adjudication_guidelines.md](../../../benchmark/guidelines/adjudication_guidelines.md) | Complete |
| 3.4 | Human evaluation guidelines | [../../../benchmark/guidelines/human_evaluation_guidelines.md](../../../benchmark/guidelines/human_evaluation_guidelines.md) | Complete |
| 3.5 | Annotator training | [../../../benchmark/guidelines/annotator_training.md](../../../benchmark/guidelines/annotator_training.md) | Complete |

3.1 covers all fifteen required topics and the 0–3 preservation scale with the
three uncertainty labels. 3.5 contains ten training exercises, and states clearly
that its examples are **not validated**.

---

## 4. Pilot dataset

| # | Deliverable | Path | Status |
|---|---|---|---|
| 4.1 | 47 draft pilot items | [../../../benchmark/pilot/pilot_items_v1.jsonl](../../../benchmark/pilot/pilot_items_v1.jsonl) | Complete, unvalidated by humans |
| 4.2 | Pilot plan | [../../../benchmark/pilot/pilot_plan.md](../../../benchmark/pilot/pilot_plan.md) | Complete |
| 4.3 | Issues log | [../../../benchmark/pilot/pilot_issues.md](../../../benchmark/pilot/pilot_issues.md) | Complete for construction-stage issues |
| 4.4 | Statistics report | [../../../benchmark/pilot/pilot_statistics.md](../../../benchmark/pilot/pilot_statistics.md) | Generated |

Achieved distribution:

| Target | Achieved |
|---|---|
| 12 politeness/formality | 14 |
| 12 indirect request/refusal | 14 |
| 10 stance/emotion | 12 |
| 6 code-switching | 7 |
| ~22 Hindi | 26 |
| ~18 Hinglish | 21 |
| `ELICITED` majority | 35 (74.5%) |
| `MINIMAL_PAIR` substantial minority | 12 (25.5%) |
| `NATURAL` / `ADAPTED` only with provenance | 0 — provenance could not be documented |

All 47 items carry `review_status: NEEDS_NATIVE_REVIEW`, `source_reference: null`,
`license: "TO_BE_CONFIRMED"`, `annotator_ids: []`, `adjudicator_id: null`,
`agreement_status: "NOT_ANNOTATED"`.

---

## 5. Templates

| # | Deliverable | Path | Status |
|---|---|---|---|
| 5.1 | Annotation template | [../../../benchmark/pilot/pilot_annotation_template.csv](../../../benchmark/pilot/pilot_annotation_template.csv) | Complete |
| 5.2 | Item review template | [../../../benchmark/pilot/pilot_item_review_template.csv](../../../benchmark/pilot/pilot_item_review_template.csv) | Complete |
| 5.3 | Adjudication template | [../../../benchmark/pilot/pilot_adjudication_template.csv](../../../benchmark/pilot/pilot_adjudication_template.csv) | Complete |

Each carries two clearly marked demonstration rows to be deleted before use.

---

## 6. Examples

| # | Deliverable | Path | Status |
|---|---|---|---|
| 6.1 | Example items | [../../../benchmark/examples/example_items.jsonl](../../../benchmark/examples/example_items.jsonl) | Complete |
| 6.2 | Contrastive examples | [../../../benchmark/examples/contrastive_examples.jsonl](../../../benchmark/examples/contrastive_examples.jsonl) | Complete |
| 6.3 | Field-by-field explanations | [../../../benchmark/examples/example_explanations.md](../../../benchmark/examples/example_explanations.md) | Complete |

6.1 is extracted verbatim from the pilot set so the two cannot drift apart. 6.2
contains five valid and five deliberately invalid contrastive examples for
training.

---

## 7. Scripts and tests

| # | Deliverable | Path | Status |
|---|---|---|---|
| 7.1 | Schema validator | [../../../scripts/validate_schema.py](../../../scripts/validate_schema.py) | Complete |
| 7.2 | JSONL validator | [../../../scripts/validate_jsonl.py](../../../scripts/validate_jsonl.py) | Complete |
| 7.3 | Statistics generator | [../../../scripts/generate_dataset_statistics.py](../../../scripts/generate_dataset_statistics.py) | Complete |
| 7.4 | Annotation sheet builder | [../../../scripts/create_annotation_sheet.py](../../../scripts/create_annotation_sheet.py) | Complete |
| 7.5 | Agreement calculator | [../../../scripts/calculate_agreement.py](../../../scripts/calculate_agreement.py) | Complete |
| 7.6 | Tests | [../../../scripts/tests/](../../../scripts/tests/) | Complete — 41 tests |
| 7.7 | Dependencies | [../../../requirements.txt](../../../requirements.txt) | Complete |

7.5 computes percentage agreement, Cohen's kappa and Krippendorff's alpha, and
**reports insufficient data rather than estimating** when there is not enough to
work with — which is its current state.

---

## 8. Documentation

| # | Deliverable | Path | Status |
|---|---|---|---|
| 8.1 | Benchmark README | [../../../benchmark/README.md](../../../benchmark/README.md) | Complete |
| 8.2 | Pilot README | [../../../benchmark/pilot/README.md](../../../benchmark/pilot/README.md) | Complete |
| 8.3 | Scripts README | [../../../scripts/README.md](../../../scripts/README.md) | Complete |
| 8.4 | Root README Week 2 status | [../../../README.md](../../../README.md) | Complete |

---

## 9. Week 2 planning documents

| # | Deliverable | Path | Status |
|---|---|---|---|
| 9.1 | Week 2 plan | [week_2_plan.md](week_2_plan.md) | Complete |
| 9.2 | Week 2 deliverables | [week_2_deliverables.md](week_2_deliverables.md) | This document |
| 9.3 | Week 2 progress | [week_2_progress.md](week_2_progress.md) | Complete |
| 9.4 | Week 2 summary template | [week_2_summary_template.md](week_2_summary_template.md) | Template, to be completed |

---

## 10. Not delivered, and why

| Not delivered | Reason |
|---|---|
| Natural or adapted items | Provenance could not be documented and licensing could not be verified. Inventing sources would be fabrication |
| Native-speaker validation | Requires native speakers. None involved yet |
| Inter-annotator agreement | Requires annotation. None has happened |
| Baseline translation runs | Deferred to Week 3. Baselines against an unvalidated benchmark would not mean anything |
| Telugu items | Deliberately deferred until the schema is validated on one language pair |
| Data splits | Deferred until items are validated. Splitting unvalidated items would waste the work |

---

## 11. What still needs a person

In priority order. None of this can be produced by drafting tools.

**Needs native speakers:**

1. Confirm the 47 source utterances are natural.
2. Confirm each contrastive translation is genuinely wrong in context — and flag
   any that are still acceptable, which would invalidate the item.
3. Re-rate severity independently; the current distribution is skewed toward
   `MAJOR`.
4. Re-check every `context_status: REQUIRED` label against the cover-the-context
   test.
5. Conform the reference translations to **Indian English**, supplying alternatives
   where the current wording is not natural in that variety.
6. Complete Stage 2 rating so agreement can be measured. Agreement on
   `code_switch_preservation` is now the test of whether the code-switching category
   is well-posed against an English target.

**Supervisor decisions (now made):**

7. Code-switching category: **kept.** Testability becomes a pilot measurement
   rather than a precondition. See `pilot_issues.md` Issue 4.
8. Target English variety: **Indian English.** Recorded in
   `language_scope_decision.md`; evaluators judge naturalness against it. See
   `pilot_issues.md` Issue 10.

**Still needs a supervisor decision:**

9. Whether to source naturally occurring dialogue, and from where.
10. Whether five politeness levels is the right granularity (or measure it in the
    pilot).

**Needs recruitment:**

11. Two native-speaker annotators plus one adjudicator, ideally with different
    regional backgrounds.

---

## 12. Verification

Run from the repository root:

```bash
python scripts/validate_schema.py
python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl
python scripts/validate_jsonl.py benchmark/examples/example_items.jsonl
python scripts/generate_dataset_statistics.py benchmark/pilot/pilot_items_v1.jsonl
python scripts/create_annotation_sheet.py benchmark/pilot/pilot_items_v1.jsonl
python -m unittest discover scripts/tests
```

Results are recorded in [week_2_progress.md](week_2_progress.md).
