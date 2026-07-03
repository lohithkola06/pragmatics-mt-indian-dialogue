# When a Good Translation Is Wrong in Context

## Citation

Elena Voita, Rico Sennrich, and Ivan Titov. 2019. *When a Good Translation Is Wrong in Context: Context-Aware Machine Translation Improves on Deixis, Ellipsis, and Lexical Cohesion*. Proceedings of ACL 2019, pages 1198 to 1212.

Source file: `P19-1116.pdf`

## One-Sentence Summary

The paper identifies frequent cases where acceptable sentence-level translations fail in context, builds 6,000 contrastive tests, and introduces a two-pass context-aware model that improves discourse consistency without reducing BLEU.

## Research Problem

Two obstacles limit progress in context-aware MT:

1. Standard metrics are not sensitive to contextual consistency.
2. Most available bilingual data is sentence-level rather than document-level.

The paper addresses both by:

- analysing real contextual failures,
- building targeted contrastive benchmarks,
- training a second-pass model on a smaller document-level subset.

## Main Research Questions

1. Which linguistic phenomena make good isolated translations fail in context?
2. Can targeted test sets quantify these failures?
3. Can a model use a small amount of document-level parallel data while retaining a strong sentence-level base system?
4. Does context improve consistency without reducing general translation quality?

## Dataset

### Language Pair

English to Russian.

### Domain

OpenSubtitles2018.

### Human Analysis Sample

The authors translate 2,000 pairs of consecutive sentences using a context-agnostic Transformer.

### Training Data

- Six million sentence pairs in total.
- Approximately 1.5 million instances have three preceding context sentences.
- The test sets are constructed from 400,000 held-out instances from unseen movies.

### Context Window

Up to three preceding sentences.

## Human Error Analysis

The analysis has two stages.

### Stage 1: Sentence-Level Evaluation

Annotators mark whether each sentence translation is:

- fluent,
- a reasonable translation in at least some context.

### Stage 2: Context Evaluation

For pairs where both translations are individually good, annotators determine whether they are also good together.

Annotators only mark a pair bad when no plausible additional context could make it acceptable. This conservative rule reduces personal preference effects.

### Results

| Category | Count | Percentage |
|---|---:|---:|
| Both individually good and good together | 1,649 | 82% |
| One or both bad at sentence level | 211 | 11% |
| Individually good but bad together | 140 | 7% |

The 7 percent category demonstrates that sentence-level evaluation misses a meaningful class of errors.

## Error Taxonomy

Among context failures:

| Phenomenon | Frequency |
|---|---:|
| Deixis | 37% |
| Ellipsis | 29% |
| Lexical cohesion | 14% |
| Ambiguity | 9% |
| Anaphora | 6% |
| Other | 5% |

The three main targeted categories account for approximately 80 percent of observed contextual inconsistencies.

### Deixis Details

Most deixis errors involve:

- inconsistent formal versus informal second-person forms,
- inconsistent speaker gender,
- inconsistent addressee gender.

Within the deixis category, T-V inconsistency is the dominant subtype.

### Ellipsis Details

Errors include:

- wrong noun-phrase inflection because an omitted verb must be recovered,
- incorrect reconstruction of a verb in English VP ellipsis.

### Lexical Cohesion Details

Errors include:

- inconsistent translation of names,
- failure to repeat a lexical choice used for emphasis or clarification.

## Contrastive Test Sets

Total size:

```text
6,000 examples
```

| Test Set | Size |
|---|---:|
| Deixis | 3,000 |
| Lexical cohesion | 2,000 |
| Ellipsis, inflection | 500 |
| Ellipsis, VP | 500 |

Each example contains:

1. a genuine sequence of sentences,
2. a true translation,
3. one or more contrastive translations,
4. a controlled difference in the targeted phenomenon.

All contrastive translations are plausible in isolation. Only the context reveals the error.

### Distance Control

For deixis, relevant context is evenly distributed across one, two, and three sentences back.

For lexical cohesion, the test set records the distance to the latest relevant occurrence.

## Model or Method

### Base Model

A sentence-level Transformer-base model trained on all six million sentence pairs.

### CADec

A context-aware decoder refines the base model's first-pass translation.

Inputs include:

- current source representation,
- previous source representations,
- first-pass current translation,
- previous target translations,
- sentence-distance embeddings.

The base model is fixed. CADec is trained only on the document-level subset.

### Training Noise

The second-pass model receives either:

- a sampled base-model translation,
- a corrupted reference translation.

This teaches the model to correct errors while remaining close to a strong first-pass output.

## Baselines

1. Sentence-level Transformer.
2. Concatenation model.
3. Hierarchical multi-encoder model.
4. CADec.

## Evaluation Method

### BLEU

Used for general translation quality.

### Contrastive Accuracy

Used for contextual consistency.

### Context-Aware Stopping

Training is monitored using both BLEU and consistency accuracy. The paper shows that consistency can continue improving after BLEU has converged.

## Main Results

### BLEU

| Model | BLEU |
|---|---:|
| Baseline trained on 1.5M | 29.10 |
| Baseline trained on 6M | 32.40 |
| Concatenation | 31.56 |
| Hierarchical model | 26.68 |
| CADec | 32.38 |

CADec is statistically comparable to the full sentence-level baseline in BLEU.

### Targeted Results

| Model | Deixis | Lexical Cohesion | Ellipsis, Inflection | Ellipsis, VP |
|---|---:|---:|---:|---:|
| Baseline | 50.0 | 45.9 | 53.0 | 28.4 |
| Concatenation | 83.5 | 47.5 | 76.2 | 76.6 |
| CADec | 81.6 | 58.1 | 72.2 | 80.0 |

CADec provides strong gains without sacrificing BLEU.

### Important Evaluation Finding

The baseline and CADec have nearly identical BLEU scores but very different contextual accuracies. This directly demonstrates that BLEU cannot serve as the only metric for context-sensitive translation.

### Training-Criterion Finding

BLEU stabilizes before lexical-cohesion accuracy. A model selected only by BLEU may be stopped before it learns to use context effectively.

## Qualitative Findings

### Deixis

The same interlocutor can be addressed formally in one sentence and informally in the next. Each sentence is plausible alone, but the dialogue is inconsistent.

### Gender

Russian verbs can mark speaker gender. Separate sentence translation can assign different genders to the same speaker.

### Ellipsis

English allows omission that Russian does not. Correct reconstruction requires previous sentences.

### Lexical Cohesion

Different translations of the same name or repeated phrase may all be locally correct, but inconsistent in the dialogue.

## Strengths

1. Begins with empirical human error analysis.
2. Converts observed failures into targeted benchmarks.
3. Creates large, controlled contrastive suites.
4. Models a realistic imbalance between sentence-level and document-level data.
5. Separates general translation quality from contextual consistency.
6. Includes distance-controlled context.
7. Shows why model selection needs phenomenon-specific metrics.

## Limitations

1. The analysis is limited to English-Russian subtitles.
2. The taxonomy reflects discourse consistency more than interpersonal pragmatics.
3. Contrastive test construction uses controlled perturbations.
4. The test assumes a single correct contextual choice.
5. The model uses previous target translations, which may contain their own errors.
6. Context is limited to three previous sentences.
7. The human annotation sample is modest relative to the training corpus.
8. Some phenomena, such as sarcasm, indirectness, speech acts, and code-switching, are not studied.
9. The benchmark tests preference ranking rather than open-ended generation quality.

## Assumptions

- Contextual inconsistency can be isolated through minimal target-side changes.
- Relevant context occurs within three previous sentences.
- The reference translation is contextually correct.
- A context-aware second pass can correct the first pass without harming adequacy.

## Relevance to My Project

This paper is the closest methodological model for the proposed benchmark.

The proposed research can reproduce its pipeline:

1. Translate naturally occurring or elicited dialogues.
2. Ask native speakers whether outputs are acceptable in isolation.
3. Re-evaluate individually acceptable outputs in context.
4. Categorize the failures.
5. Construct contrastive examples from frequent categories.
6. Compare sentence-only and context-aware translation.
7. Report semantic and pragmatic scores separately.

The main extension is replacing discourse-only categories with a broader pragmatic taxonomy:

```text
politeness and formality
speech act
stance and emotion
indirectness
code-switching function
```

## Methods I Can Reuse

1. Two-stage human analysis: isolated judgment followed by contextual judgment.
2. Conservative annotation instructions that exclude uncertain cases.
3. Error-frequency analysis before finalizing benchmark categories.
4. Contrastive candidates that remain plausible in isolation.
5. Context-distance metadata.
6. Separate general-quality and phenomenon-specific evaluation.
7. Context-aware early stopping or model selection.
8. A strong sentence-level baseline plus a context-aware second pass.

## Methods I Should Not Copy Directly

1. Do not define context failure only as inconsistency.
2. Do not limit pragmatic categories to visible morphology.
3. Do not assume one reference determines the only acceptable social interpretation.
4. Do not use target perturbations without native-speaker validation.
5. Do not rely on subtitle data alone.

## Questions Raised by the Paper

1. What percentage of Indian dialogue translations are acceptable alone but inappropriate in context?
2. Which pragmatic categories dominate the errors?
3. How often is one previous turn sufficient?
4. Can speaker-role metadata substitute for longer dialogue history?
5. How should uncertain or multi-valid cases be represented?
6. Can black-box LLM translation be evaluated contrastively without token likelihoods?

## Final Takeaway

The paper provides a complete blueprint for discovering context-sensitive errors and converting them into a benchmark. The proposed project should adopt this empirical pipeline while extending the phenomenon inventory from discourse consistency to social and pragmatic meaning.
