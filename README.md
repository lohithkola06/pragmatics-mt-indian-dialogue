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

- **Language direction:** Hindi or Hinglish → English (Telugu → English kept as a possible
  second-stage extension)
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
  project/         Research scope, research questions, benchmark blueprint
  planning/        Weekly plans and summaries (week_01/)
  literature/      Paper notes, groupings, cross-paper synthesis, takeaways
references/
  papers/          Source PDFs for the reviewed literature
benchmark/         Schema, guidelines, examples, pilot, and dataset splits (scaffold)
experiments/       Prompts, configs, model outputs, logs (scaffold)
evaluation/        Semantic/pragmatic/contrastive metrics, human & LLM judging (scaffold)
scripts/           Data processing and evaluation scripts (scaffold)
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

**Next:** pilot dataset construction — finalize the language setting, write annotation
guidelines, build 30–50 pilot items with validated contrastive negatives, run initial
translation baselines, and conduct pilot annotation with native speakers.
