# Week 2 Summary — TEMPLATE

## Project Title

**Pragmatics-Preserving Machine Translation for Indian Dialogue**

---

> **This is a template, not a completed summary.**
>
> Section A records repository work that is finished and verified. Sections B
> onward are placeholders to be filled in **after** native-speaker review and pilot
> annotation have actually taken place.
>
> The separation is deliberate. Week 2 produced a benchmark instrument; it did not
> produce validated data. Writing this up as though annotation had happened would
> misrepresent the state of the project. **Do not fill in Sections B–E with
> estimates.** If a number is not measured, leave the placeholder in place.
>
> Compare with [week_1_summary.md](../week_01/week_1_summary.md) for the intended
> voice and structure.

---

# Section A — Completed repository work

*This section is factual and complete as of the end of Week 2. It can be used
as-is.*

## A1. What I set out to do this week

I set out to move the project from planning into pilot benchmark construction: to
close the language question left open in Week 1, turn the blueprint's prose schema
into something a machine can enforce, draft a pilot dataset, and build the tooling
and guidelines a native speaker would need in order to start annotating.

## A2. What I finalized

**The language setting.** Hindi and naturally occurring Hinglish to English, with
Hindi and Hinglish kept as two distinct values so that monolingual and code-mixed
input can be reported separately. Romanized Latin script throughout. Telugu
deferred until the schema has been validated on one language pair. I stated
explicitly that this choice is not representative of Indian languages generally.

**The annotation schema.** Version `0.1.0`, as JSON Schema draft 2020-12: 43
properties, all required, 19 controlled-vocabulary fields, 4 conditional rules.
Every deviation from the Week 1 blueprint is recorded with its reason in
`schema_version.md`.

**The label set.** Four primary phenomena, 18 speech acts, 5 politeness levels, 4
formality levels, 3 indirectness levels, 12 stance values, 10 emotion values, 10
code-switching functions, 8 contrastive error categories, 3 severity levels — each
defined with an example, the labels it is confused with, and when not to use it.

## A3. What I built

| Component | Detail |
|---|---|
| Pilot dataset | 47 draft items, all `NEEDS_NATIVE_REVIEW` |
| Guidelines | 5 documents: annotation, contrastive items, adjudication, human evaluation, training |
| Schema docs | Field reference, label definitions, severity guidelines, version history |
| Templates | Annotation, item review, adjudication CSVs |
| Scripts | Schema validation, JSONL validation, statistics, annotation sheets, agreement |
| Tests | 41, covering validation and the agreement statistics |

**Pilot composition:** 14 politeness/formality, 14 indirect request/refusal, 12
stance/emotion, 7 code-switching; 26 Hindi and 21 Hinglish; 35 `ELICITED` and 12
`MINIMAL_PAIR`; no `NATURAL` or `ADAPTED` items, because provenance could not be
documented and inventing sources would have been fabrication. Eight items are
context-independent controls.

## A4. Decisions I made and why

- **Hindi and Hinglish as separate values**, so that code-mixing effects can be
  measured rather than averaged away.
- **Romanized script**, matching the blueprint's own examples and how Hindi is
  typed in chat — at the known cost that most MT systems are trained on Devanagari.
- **Dropped `POLITE` from the politeness scale**, because it was not reliably
  separable from `RESPECTFUL`. This is provisional and the pilot should test it.
- **Contrastive failures in both directions** — some too blunt, some too formal —
  so a system cannot score well by always maximising politeness.
- **A negative control for code-switching**, where the correct answer is that the
  English does no pragmatic work.
- **Adjudication preserves disagreement** rather than forcing consensus, so that
  regional variation is documented instead of hidden.

## A5. Verification

| Command | Result |
|---|---|
| `python scripts/validate_schema.py` | Pass |
| `python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl` | Pass — 47/47 valid |
| `python scripts/validate_jsonl.py benchmark/examples/example_items.jsonl` | Pass — 4/4 valid |
| `python -m unittest discover scripts/tests` | Pass — 41 tests |
| `python scripts/generate_dataset_statistics.py …` | Pass — distribution as intended |
| `python scripts/create_annotation_sheet.py …` | Pass — 94 rows from 47 items |
| `python scripts/calculate_agreement.py <un-annotated sheet>` | Correctly reports insufficient data |

## A6. Problems I found in my own work

Recorded in full in `benchmark/pilot/pilot_issues.md`. The most significant:

1. **The context-independent control group was too thin** — one item out of 40 as
   first drafted. I added seven more, bringing it to 8 of 47. The related worry is
   unresolved: `REQUIRED` is still the largest class and may be over-applied.
2. **Code-switching may not be testable with an English target**, since the switch
   cannot survive into monolingual English.
3. **Severity is skewed** — 37 of 47 items are `MAJOR`.
4. **Every item has a single author**, so systematic blind spots would be invisible
   within the dataset.
5. **The target variety of English has never been decided**, though it affects
   every reference translation.

## A7. What this week did not produce

No native-speaker validation, no annotation, no agreement figures, no baseline
translation runs, no natural-source items, no data splits. All of these require
either people or decisions that were not mine to make alone.

---

# Section B — Pilot annotation results

> **PLACEHOLDER — requires completed annotation. Do not fill in with estimates.**

## B1. Annotators

- Number of annotators: `[to be recorded]`
- Regional backgrounds: `[to be recorded]`
- Adjudicator: `[to be recorded]`

## B2. Stage 1 item review outcomes

| Outcome | Items |
|---|---|
| Accepted | `[ ]` |
| Revised | `[ ]` |
| Rejected | `[ ]` |

Most common reason for rejection: `[to be recorded]`

Number of items where a reviewer judged the contrastive translation still
acceptable: `[to be recorded]` — this is the figure I most want, because it tells
me what proportion of my contrastive items were not testing anything.

## B3. Agreement

> Report only measured values, produced by `scripts/calculate_agreement.py` on
> pre-adjudication annotations. Leave cells blank if not computed.

| Dimension | Units | Pairwise agreement | Cohen's kappa | Krippendorff's alpha |
|---|---|---|---|---|
| `semantic_adequacy` | | | | |
| `speech_act_preservation` | | | | |
| `politeness_preservation` | | | | |
| `formality_preservation` | | | | |
| `stance_preservation` | | | | |
| `emotion_preservation` | | | | |
| `indirectness_preservation` | | | | |
| `code_switch_preservation` | | | | |
| `relationship_appropriateness` | | | | |
| `translation_naturalness` | | | | |
| `overall_pragmatic_preservation` | | | | |

Dimension with the **highest** agreement: `[ ]`
Dimension with the **lowest** agreement: `[ ]`

## B4. Did annotators separate semantic from pragmatic judgement?

> The central assumption of the benchmark. Check whether `semantic_adequacy` stayed
> high on contrastive candidates while pragmatic dimensions dropped. If annotators
> lowered semantic adequacy for socially wrong translations, the design has a
> problem.

`[to be recorded]`

---

# Section C — Answers to the pilot's questions

> **PLACEHOLDER — requires completed annotation.**

| # | Question | Answer |
|---|---|---|
| 1 | Can annotators separate semantic adequacy from pragmatic preservation? | `[ ]` |
| 2 | Do the four categories divide the space cleanly? | `[ ]` |
| 3 | Is agreement high enough to be usable? | `[ ]` |
| 4 | Are the contrastive translations valid? | `[ ]` |
| 5 | Does context matter as much as the items claim? | `[ ]` |
| 6 | Are the source utterances natural? | `[ ]` |
| 7 | Is the code-switching category well-posed with an English target? | `[ ]` |
| 8 | Are five politeness levels the right granularity? | `[ ]` |
| 9 | Are stance and emotion separable in practice? | `[ ]` |

---

# Section D — Schema changes for `0.2.0`

> **PLACEHOLDER — requires pilot findings.**

| Change | Reason | Source |
|---|---|---|
| `[ ]` | `[ ]` | `[ ]` |

Candidate changes already identified during construction, to be confirmed or
dropped in light of the findings:

- Add a `pair_id` field so minimal-pair partners cannot be split across data
  splits.
- Consider an optional `source_devanagari` field.
- Merge `HIGHLY_RESPECTFUL` and `RESPECTFUL` if agreement on `politeness_level` is
  poor.
- Reconsider the code-switching category depending on the answer to question 7.

---

# Section E — Decision: proceed or revise

> **PLACEHOLDER — requires pilot findings.**

Against the criteria in `benchmark/pilot/pilot_plan.md §9`:

| Criterion | Met? |
|---|---|
| Annotators separate semantic and pragmatic correctness | `[ ]` |
| Agreement acceptable on most dimensions | `[ ]` |
| Contrastive negatives semantically close and genuinely wrong | `[ ]` |
| Systems show measurable pragmatic failures | `[ ]` (requires baseline runs) |
| Context improves results on a subset of items | `[ ]` (requires baseline runs) |
| The four categories are sufficiently distinct | `[ ]` |

**Decision:** `[proceed to full benchmark / revise design and re-pilot]`

**Reasoning:** `[to be recorded]`

A decision to revise is not a failure. It is the pilot doing its job.

---

# Section F — Final Week 2 statement

> **PLACEHOLDER — write once Sections B–E are complete.**

Two or three paragraphs, first person, covering: what the pilot established, what
it did not, what changes to the design followed, and what happens in Week 3.

**Until Sections B–E are filled in, the accurate statement of where this project
stands is Section A: the benchmark instrument exists, it validates, and it has not
yet been tested on a single human judgement.**
