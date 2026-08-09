# Pilot Study Plan

**Pilot version:** `v1`
**Dataset:** [pilot_items_v1.jsonl](pilot_items_v1.jsonl) — 47 draft items
**Schema:** `0.1.0`
**Status:** items drafted and schema-validated; **no human annotation has taken
place**

---

## 1. Objectives

The pilot exists to test the *instrument*, not to produce results. Its questions
are:

1. **Can annotators separate semantic adequacy from pragmatic preservation?** This
   is the assumption the whole benchmark rests on. If annotators cannot hold the
   two apart, the design fails.
2. **Do the four categories divide the space cleanly**, or do they overlap so much
   that annotators cannot assign a primary phenomenon?
3. **Is agreement high enough to be usable**, and on which dimensions is it worst?
4. **Are the contrastive translations valid** — semantically close, grammatical,
   plausible alone, and genuinely wrong in context?
5. **Does context matter as much as the items claim?** Items marked `REQUIRED`
   should be ones annotators genuinely misread without context.
6. **Are the source utterances natural** to speakers other than their author?
7. **Which schema decisions need revising** before the full 300–500 item build?

The pilot is judged a success if it produces clear answers, including negative
ones. Discovering that a category does not work is a result.

---

## 2. Dataset composition

47 items, distributed as follows. Counts are from
[pilot_statistics.md](pilot_statistics.md), generated from the dataset.

### By category

| Category | Code | Items | Share |
|---|---|---:|---:|
| Politeness and formality | `POL` | 14 | 29.8% |
| Indirect requests and refusals | `IND` | 14 | 29.8% |
| Stance and emotion | `STA` | 12 | 25.5% |
| Code-switching | `CSW` | 7 | 14.9% |

### By language

| Language | Items | Share |
|---|---:|---:|
| Hindi | 26 | 55.3% |
| Hinglish | 21 | 44.7% |

All seven code-switching items are Hinglish by necessity.

### By source type

| Source type | Items | Share |
|---|---:|---:|
| `ELICITED` | 35 | 74.5% |
| `MINIMAL_PAIR` | 12 | 25.5% |
| `NATURAL` | 0 | — |
| `ADAPTED` | 0 | — |

**There are no `NATURAL` or `ADAPTED` items.** Those types require documented
provenance and a verified licence, and neither exists yet. Adding items whose
provenance could not be cited would have been fabrication. Sourcing naturally
occurring dialogue is Week 3 work.

The 12 minimal-pair items form 6 pairs that differ in exactly one pragmatic
feature. Pair partners are named in `creator_notes` and **must be kept in the same
data split** to avoid leakage.

### By context status

| Context status | Items | Share |
|---|---:|---:|
| `REQUIRED` | 22 | 46.8% |
| `HELPFUL` | 17 | 36.2% |
| `NOT_REQUIRED` | 8 | 17.0% |

The eight `NOT_REQUIRED` items are the **control group**: each is interpretable
without any previous turn, so they carry no context turns at all. Comparing
performance on them against the `REQUIRED` items is what separates a genuine
context benefit from general system capability.

`REQUIRED` may still be over-applied at 46.8%, and reviewers should re-check every
such label against the cover-the-context test. See
[pilot_issues.md](pilot_issues.md), issue 1.

### By severity

| Severity | Items | Share |
|---|---:|---:|
| `MAJOR` | 37 | 78.7% |
| `MINOR` | 7 | 14.9% |
| `CRITICAL` | 3 | 6.4% |

This distribution is skewed and needs independent re-rating — see
[pilot_issues.md](pilot_issues.md), issue 2.

---

## 3. Annotator requirements

**Number:** at least 2 independent annotators per item, plus 1 adjudicator who did
not annotate.

**Each annotator must:**

- be a native or near-native speaker of Hindi, and comfortable with Hinglish as
  used in urban conversation,
- be fluent enough in English to judge whether a translation is natural,
- have read [annotation_guidelines.md](../guidelines/annotation_guidelines.md) and
  worked through [annotator_training.md](../guidelines/annotator_training.md),
- be able to state their regional background, so region-dependent judgements can
  be interpreted.

**No linguistics background is required.** Confident intuitions about how an
utterance would land socially are what the task needs.

**Recording annotators:** pseudonymous identifiers only (`ANN_01`, `ANN_02`,
`ADJ_01`). The mapping to real people is kept outside this repository. Real names
must never appear in `annotator_ids` or `adjudicator_id`.

**Regional diversity is desirable.** If both annotators share one regional variety,
the pilot cannot detect region-dependence, and that limitation must be reported.

---

## 4. Annotation procedure

### Stage 1 — Item review (before rating)

Both annotators independently review all 47 items using
[pilot_item_review_template.csv](pilot_item_review_template.csv), judging:

1. Is the source utterance natural?
2. Is the intended interpretation clear?
3. Is the reference translation acceptable?
4. Is the contrastive translation semantically close?
5. Is the contrastive translation pragmatically wrong in context?
6. Is the primary label correct?
7. Is the context label correct?

Question 5 is the most important. An item whose contrastive translation both
reviewers would accept measures nothing and must be rejected.

### Stage 2 — Translation rating

Generate the annotation sheet:

```bash
python scripts/create_annotation_sheet.py benchmark/pilot/pilot_items_v1.jsonl --blind
```

This produces 94 rows — the reference and contrastive candidate for each of the 47
items — with the candidate type withheld and an answer key written to a separate
file. Annotators must not see the key.

Each annotator rates every candidate on the twelve dimensions in
[pilot_annotation_template.csv](pilot_annotation_template.csv), following
[human_evaluation_guidelines.md](../guidelines/human_evaluation_guidelines.md).

**Calibration:** both annotators rate the same 5 items first and compare, before
completing the rest. Calibrate on the guidelines and the scale, never on specific
answers.

**Independence:** no discussion of individual items during annotation. Agreement is
computed on independent judgements, and any coordination invalidates it.

### Stage 3 — Agreement measurement

```bash
python scripts/calculate_agreement.py <completed annotation CSV> --out agreement_report.md
```

Computed on the **pre-adjudication** annotations. Adjudicating first and then
measuring agreement would be misreporting.

### Stage 4 — Adjudication

The adjudicator resolves disagreements per
[adjudication_guidelines.md](../guidelines/adjudication_guidelines.md), recording
each decision in [pilot_adjudication_template.csv](pilot_adjudication_template.csv).

Genuinely valid alternative readings are **preserved**, not resolved away.

### Stage 5 — Item disposition

Each item is marked `APPROVED`, `REVISED` or `REJECTED`, and `review_status` is
updated in the dataset.

---

## 5. Agreement measures

| Statistic | When used |
|---|---|
| Percentage agreement | Always. Mean pairwise exact match across annotators |
| Cohen's kappa | Exactly two annotators |
| Krippendorff's alpha (nominal) | Any number of annotators; tolerates missing ratings |

Reported **per dimension**, not only overall, because a single overall figure would
hide the fact that some dimensions are far harder than others.

Interpretation, following common convention and treated as indicative rather than
authoritative:

| Kappa / alpha | Reading |
|---|---|
| > 0.80 | Strong |
| 0.60 – 0.80 | Acceptable for a subjective task |
| 0.40 – 0.60 | Marginal; the dimension needs sharper definitions |
| < 0.40 | Not usable as-is |

Niu & Carpuat (2020) report human agreement on formality at Krippendorff's alpha
around 0.5, on a task narrower than this one. **Agreement in the 0.4–0.6 range on
the harder dimensions should therefore be expected rather than treated as
failure** — the response is to sharpen definitions, not to abandon the dimension.

**No agreement figure will be reported until annotation actually happens.**
`calculate_agreement.py` reports insufficient data rather than estimating.

---

## 6. Item acceptance criteria

An item is accepted only when **all seven** hold:

1. **The source is natural** — both reviewers judge it something a real speaker
   would say.
2. **The intended interpretation is clear** — both reviewers recover it from the
   context.
3. **The reference is acceptable** — both would be comfortable sending it on the
   speaker's behalf.
4. **The contrastive candidate is semantically close** — same facts, grammatical,
   plausible alone.
5. **The contrastive candidate is pragmatically wrong in context** — neither
   reviewer would accept it after reading the context.
6. **Label agreement is acceptable** — annotators agree on the primary phenomenon,
   and are within one point on the preservation dimensions.
7. **No undocumented cultural assumption is required** — any assumption the reading
   depends on is either supplied in the context or recorded in
   `context_explanation`.

Accepted items get `review_status: APPROVED`. **Only a native speaker may set
this.**

---

## 7. Revision criteria

Revise when the item tests something real but its current form gets in the way:

- the context is too thin to support the intended reading → add a turn,
- the intended act is ambiguous → adjust the context, not the utterance,
- the contrastive breaks more than one feature → narrow it,
- the primary label is wrong but the item is sound → relabel,
- `context_status` is wrong — an item marked `REQUIRED` that both annotators read
  correctly without context is `HELPFUL`,
- the severity is misjudged.

After revision: set `review_status: REVISED`, bump `annotation_version`, and
**re-annotate from scratch**.

---

## 8. Rejection criteria

Reject when the item cannot be fixed without becoming a different item:

- **the contrastive translation is acceptable in context** — the most common fatal
  defect,
- the source utterance is not natural,
- the intended reading needs an undocumented cultural assumption,
- the pragmatic difference is imperceptible to native speakers even once explained,
- the item duplicates another too closely,
- provenance or licensing cannot be established (`NATURAL` / `ADAPTED` only).

Set `review_status: REJECTED` and **keep the item in the repository** with the
reason recorded. Rejected items document what was tried.

---

## 9. Pilot-level decision rules

After annotation, decide whether to proceed to the full benchmark.

**Proceed if:**

1. annotators demonstrably separate semantic and pragmatic correctness,
2. agreement is acceptable on most dimensions,
3. contrastive negatives are semantically close and genuinely wrong,
4. at least some translation systems show measurable pragmatic failures,
5. context improves results on at least a subset of items,
6. the four categories are sufficiently distinct.

**Revise the design if:**

- category overlap is high,
- annotators disagree consistently on the same dimension,
- context turns out to be unnecessary for most items,
- contrastive negatives introduce semantic errors,
- the elicited examples sound artificial to reviewers.

A revision outcome is not a failure of the pilot. It is the pilot working.

---

## 10. Timeline

Sequenced rather than dated, since it depends on annotator availability.

| Step | Work | Depends on |
|---|---|---|
| 1 | Recruit 2 annotators + 1 adjudicator | — |
| 2 | Annotators read guidelines, complete training | 1 |
| 3 | Stage 1 item review, all 47 items | 2 |
| 4 | Fix or reject items failing review | 3 |
| 5 | Calibration on 5 items, compare | 4 |
| 6 | Stage 2 rating, remaining candidates | 5 |
| 7 | Compute agreement | 6 |
| 8 | Adjudicate | 7 |
| 9 | Update `review_status`, revalidate | 8 |
| 10 | Write up findings and schema changes | 9 |

Steps 3 and 4 come **before** rating on purpose: rating items that are going to be
rejected wastes annotator effort, which is the scarcest resource here.

---

## 11. Deliverables

**Complete (repository work):**

- [x] 47 draft items, schema-validated
- [x] JSON Schema `0.1.0` and field documentation
- [x] Annotation, contrastive, adjudication, evaluation and training guidelines
- [x] Annotation, review and adjudication CSV templates
- [x] Validation, statistics, annotation-sheet and agreement scripts, with tests
- [x] [pilot_statistics.md](pilot_statistics.md), generated from the dataset

**Outstanding (requires people):**

- [ ] Recruit annotators
- [ ] Stage 1 item review
- [ ] Stage 2 translation rating
- [ ] Agreement report
- [ ] Adjudication record
- [ ] Item dispositions
- [ ] Schema `0.2.0` revision
- [ ] Baseline translation runs across the context conditions

Everything in the second list needs native speakers. None of it can be produced by
drafting tools, and none of it has been.

---

## 12. What this pilot cannot establish

Stated up front so results are not over-read:

- **Not a measure of any MT system.** No translation systems have been run yet.
- **Not representative of Indian languages generally.** One language pair, and
  Hindi/Hinglish is not a proxy for Telugu, Tamil, Bengali or any other language.
  See [language_scope_decision.md](../../docs/project/language_scope_decision.md).
- **Not regionally representative.** With two annotators, regional coverage is
  whatever those two people bring.
- **Not sufficient for statistical claims.** 47 items across four categories gives
  7–14 items per category — enough to find problems, not to measure effect sizes.
- **Not a validated set of severity weights.** The `MINOR`/`MAJOR`/`CRITICAL`
  labels are drafting judgements awaiting review.
