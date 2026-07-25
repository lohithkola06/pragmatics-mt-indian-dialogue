# Pragmatics-Preserving Machine Translation for Indian Dialogue

This project studies **pragmatic failure in machine translation for Indian dialogue** and
builds a benchmark to measure it. The focus is not only whether a translation preserves the
literal or propositional content of an utterance, but whether it also preserves the
speaker's **intended social and communicative meaning in context** — politeness,
formality, speech act, indirectness, stance, emotion, speaker relationships, and
discourse-motivated code-switching.

The main contribution is a **benchmark and evaluation framework**, not a new translation
model.

## Working Definition

> Pragmatic failure in machine translation occurs when a translation preserves the basic
> semantic content of an utterance but fails to preserve its intended social or
> communicative meaning in context.

## Primary Research Question

> To what extent do current machine translation systems preserve the intended pragmatic and
> social meaning of Indian conversational dialogue?

This is investigated by comparing sentence-only, context-aware, speaker-role-aware, and
pragmatics-aware translation conditions. See [docs/project/research_questions.md](docs/project/research_questions.md)
for the full set of research questions and hypotheses.

## Initial Scope

- **Language direction:** Hindi and naturally occurring Hinglish → English, treated as two
  distinct dataset values (Telugu → English kept as a possible second-stage extension).
  Finalized in Week 2 — see
  [docs/project/language_scope_decision.md](docs/project/language_scope_decision.md). This
  setting is **not** representative of Indian languages generally.
- **Pilot size:** 30–50 items
- **Full benchmark target:** 300–500 items
- **Context window:** 1–3 previous dialogue turns per item, each item recording whether
  context is *not required*, *helpful*, or *required*
- **Initial pragmatic categories:**
  1. Politeness and formality
  2. Indirect requests and refusals
  3. Stance and emotion
  4. Discourse-motivated code-switching *(optional fourth)*

Full detail in [docs/project/research_scope.md](docs/project/research_scope.md).

## Evaluation Principle

Semantic correctness and pragmatic preservation are evaluated **separately**. The benchmark
combines open-ended translation, contrastive minimal-pair evaluation, and native-speaker
human judgment, with automatic metrics (BLEU, chrF, COMET, BERTScore), rule-based checks,
and LLM judges validated against human scores. See
[docs/project/benchmark_blueprint.md](docs/project/benchmark_blueprint.md).

## Repository Structure

```text
docs/
  project/         Research scope, research questions, blueprint, language decision
  planning/        Weekly plans and summaries (week_01/, week_02/)
  literature/      Paper notes, groupings, cross-paper synthesis, takeaways
references/
  papers/          Source PDFs for the reviewed literature
benchmark/
  schema/          JSON Schema, field reference, label and severity definitions
  guidelines/      Annotation, contrastive-item, adjudication, evaluation, training
  examples/        Worked example items with field-by-field explanations
  pilot/           47 draft pilot items, templates, plan, issues, statistics
  data/            Dataset splits (empty until the pilot is validated)
scripts/           Validation, statistics, annotation-sheet and agreement tooling
experiments/       Prompts, configs, model outputs, logs (scaffold)
evaluation/        Semantic/pragmatic/contrastive metrics, human & LLM judging (scaffold)
results/           Tables, figures, reports, error analysis (scaffold)
paper/             Report/paper sections and figures (scaffold)
```

Folders marked *(scaffold)* are placeholders (tracked via `.gitkeep`) that will be filled in
future weeks.

## Reviewed Literature

Seven papers underpin the benchmark design (notes in
[docs/literature/paper_notes/](docs/literature/paper_notes/), PDFs in
[references/papers/](references/papers/)):

- Sennrich, Haddow & Birch (2016) — Controlling Politeness in NMT via Side Constraints
- Niu, Martindale & Carpuat (2017) — Controlling the Formality of MT Output
- Niu & Carpuat (2020) — Controlling NMT Formality with Synthetic Supervision
- Bawden et al. (2018) — Evaluating Discourse Phenomena in NMT
- Voita, Sennrich & Titov (2019) — When a Good Translation Is Wrong in Context
- Voita, Sennrich & Titov (2019) — Context-Aware Monolingual Repair (DocRepair)
- Agrawal et al. (2024) — Assessing the Role of Context in Chat Translation Evaluation

See [docs/literature/cross_paper_synthesis.md](docs/literature/cross_paper_synthesis.md) and
[docs/literature/paper_groups.md](docs/literature/paper_groups.md) for how they connect, and
[docs/literature/research_takeaways.md](docs/literature/research_takeaways.md) for the
implementation decisions drawn from them.

## Status

**Week 1 complete:** research direction, scope, research questions, literature review, and
the benchmark blueprint are finalized (see
[docs/planning/week_01/week_1_summary.md](docs/planning/week_01/week_1_summary.md)).

**Week 2 complete — pilot benchmark constructed, not yet validated.**

| Delivered | |
|---|---|
| Language decision | Hindi and Hinglish → English, finalized and documented |
| Annotation schema | Version `0.1.0` as JSON Schema draft 2020-12, plus full field and label documentation |
| Guidelines | Annotation, contrastive-item, adjudication, human-evaluation and training documents |
| Pilot dataset | 47 draft items — 14 politeness/formality, 14 indirect request/refusal, 12 stance/emotion, 7 code-switching; 26 Hindi, 21 Hinglish. 8 are context-independent controls |
| Templates | Annotation, item-review and adjudication CSVs |
| Tooling | Schema/JSONL validation, dataset statistics, annotation-sheet generation, inter-annotator agreement |
| Tests | 41, covering validation and the agreement statistics |

> **Nothing in the pilot dataset has been validated by a human.** Every item carries
> `review_status: NEEDS_NATIVE_REVIEW`. No annotation has taken place, no inter-annotator
> agreement has been measured, and no translation systems have been run. Known problems with
> the draft items are recorded in
> [benchmark/pilot/pilot_issues.md](benchmark/pilot/pilot_issues.md).

### Running the tooling

```bash
python -m pip install -r requirements.txt

python scripts/validate_schema.py
python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl
python scripts/generate_dataset_statistics.py benchmark/pilot/pilot_items_v1.jsonl
python scripts/create_annotation_sheet.py benchmark/pilot/pilot_items_v1.jsonl
python -m unittest discover scripts/tests
```

Requires Python 3.9+ with `jsonschema`. See [scripts/README.md](scripts/README.md).

**Next:** recruit native-speaker annotators, run pilot Stage 1 item review followed by
Stage 2 rating, measure agreement, revise the schema to `0.2.0` in light of the findings,
and only then run translation baselines. Details in
[benchmark/pilot/pilot_plan.md](benchmark/pilot/pilot_plan.md) and
[docs/planning/week_02/](docs/planning/week_02/).
