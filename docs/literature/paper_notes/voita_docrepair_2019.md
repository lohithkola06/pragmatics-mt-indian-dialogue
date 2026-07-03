# Context-Aware Monolingual Repair for Neural Machine Translation

## Citation

Elena Voita, Rico Sennrich, and Ivan Titov. 2019. *Context-Aware Monolingual Repair for Neural Machine Translation*. Proceedings of EMNLP-IJCNLP 2019, pages 877 to 886.

Source file: `D19-1081.pdf`

## One-Sentence Summary

The paper trains a separate target-language model to repair contextual inconsistencies in sentence-level MT output using synthetic errors generated from monolingual document data.

## Research Problem

Context-aware MT usually requires document-level parallel data, which is limited. Sentence-level systems can produce individually plausible translations that become inconsistent when read together.

The paper asks whether a second model can repair these inconsistencies using only document-level monolingual data in the target language.

## Main Research Questions

1. Can a monolingual post-editing model correct contextual MT errors?
2. Can round-trip translation create realistic inconsistency training examples?
3. Which discourse phenomena can be learned from monolingual target-language data?
4. Can repair improve targeted consistency and BLEU?
5. How does repair compare with a context-aware model trained on parallel data?

## Motivation

A repair architecture is attractive because:

- the original MT system may be a black box,
- document-level parallel data may be scarce,
- target-language document data is easier to obtain,
- the repair model can operate after sentence-level translation.

## Task Definition

The system translates a fragment in two stages:

1. Translate each sentence independently using a context-agnostic MT model.
2. Apply DocRepair to the group of target-language translations.

DocRepair maps an inconsistent target-language fragment to a consistent one.

## Dataset

### Language Pair

English to Russian.

### Domain

OpenSubtitles2018.

### Sentence-Level Parallel Data

Six million sentence pairs are used to train the baseline translation systems.

### Monolingual Document Data

Thirty million groups of four consecutive Russian sentences are collected.

Smaller experiments use 2.5 million and 5 million fragments.

### Context Length

Four-sentence target-language fragments.

## Synthetic Training Data

For each genuine Russian sentence group:

1. Translate each Russian sentence to English independently.
2. Translate the English sentence back to Russian independently.
3. Sample round-trip translations.
4. Combine these sentence-level outputs into an inconsistent fragment.
5. Use the original Russian fragment as the target.

The procedure intentionally uses sentence-level translation so the input contains the kinds of inconsistency the repair model must learn to fix.

## Model or Method

### Baseline MT

Transformer-base models in both translation directions.

### DocRepair

A monolingual Transformer-base sequence-to-sequence model.

Sentences are concatenated using a reserved separator token.

### Test-Time Pipeline

```text
English document fragment
→ sentence-level Russian translations
→ DocRepair
→ contextually corrected Russian fragment
```

### Important Property

DocRepair does not use hidden states from the original MT system. In principle, it can repair output from a black-box translator.

## Evaluated Phenomena

The paper uses contrastive test sets for:

1. Deixis, especially T-V form consistency.
2. Lexical cohesion.
3. Ellipsis affecting noun-phrase inflection.
4. Verb-phrase ellipsis.

## Evaluation Method

### BLEU

BLEU is measured on four-sentence fragments.

### Contrastive Accuracy

The system must rank the contextually correct fragment above minimally altered inconsistent alternatives.

### Human Evaluation

Seven hundred examples are sampled where DocRepair changed the baseline output.

Annotators receive:

- the English source fragment,
- the baseline Russian translation,
- the repaired Russian translation.

They choose:

- first is better,
- second is better,
- equal quality.

The presentation order is randomized.

## Main Results

### BLEU

| System | BLEU |
|---|---:|
| Sentence-level baseline | 33.91 |
| CADec | 33.86 |
| Sentence-level repair | 34.12 |
| DocRepair | 34.60 |

Most of the gain beyond sentence-level repair comes from extra-sentential correction.

### Contrastive Results

| System | Deixis | Lexical Cohesion | Ellipsis, Inflection | Ellipsis, VP |
|---|---:|---:|---:|---:|
| Baseline | 50.0 | 45.9 | 53.0 | 28.4 |
| CADec | 81.6 | 58.1 | 72.2 | 80.0 |
| DocRepair | 91.8 | 80.6 | 86.4 | 75.2 |

DocRepair substantially improves deixis, lexical cohesion, and inflectional ellipsis. It is weaker than CADec on verb-phrase ellipsis.

### Human Evaluation

Of 700 items:

- 52 percent are judged equal.
- 35 percent favour DocRepair.
- 13 percent favour the baseline.

Among non-ties, DocRepair is preferred in approximately 73 percent of cases.

### Data Scale

Increasing monolingual data improves performance, but 5 million fragments already approach the performance of the 30 million-fragment model.

## Qualitative Findings

DocRepair can correct:

- pronoun gender to agree with an earlier antecedent,
- speaker gender marked on Russian verbs,
- noun-phrase inflection determined by an elided verb,
- inconsistent lexical choices.

The model is conservative:

- it leaves more than 20 percent of fragments completely unchanged,
- it changes only one sentence in nearly 40 percent,
- it modifies more than half of a fragment in only about 14 percent.

This conservative behaviour reduces unnecessary rewriting.

## Why VP Ellipsis Is Hard

Round-trip translation does not reliably reproduce English VP ellipsis. When Russian is translated into English, a full Russian verb is unlikely to become only the auxiliary *do*. Therefore the synthetic training input does not contain enough realistic VP-ellipsis errors.

This is a critical general lesson: synthetic corruption only teaches errors that the corruption process can generate.

## Strengths

1. Requires only target-language document data for the repair model.
2. Can be applied after a black-box translator.
3. Uses targeted, general, and human evaluation.
4. Separates contextual repair from base translation.
5. Demonstrates conservative post-editing.
6. Analyses which synthetic errors are not learned.
7. Works with much less document-level parallel supervision than end-to-end contextual MT.

## Limitations

1. Round-trip errors do not cover every real contextual failure.
2. The repair model sees only target-language output and not the original source.
3. A fluent repair could potentially change source meaning.
4. Evaluation is limited to English-Russian subtitles.
5. The context window is fixed to four sentences.
6. The phenomena are discourse consistency phenomena, not a broad pragmatic taxonomy.
7. The human study only includes items where the model changed the output.
8. A repair system may propagate or reinforce errors already present in the target fragment.
9. Synthetic data scale is large and computationally expensive.
10. The approach does not infer social relationships or communicative intent.

## Assumptions

- Target-language document data contains the desired consistency patterns.
- Round-trip translation produces useful approximations of real MT errors.
- Contextual corrections can be learned without seeing the source.
- Four-sentence fragments contain enough evidence.

## Relevance to My Project

DocRepair is relevant as a later improvement baseline, not as the first benchmark method.

A pragmatic repair experiment could take machine-generated dialogue translations and attempt to restore:

- respectful address,
- consistent formality,
- speaker-specific style,
- stance continuity,
- discourse-motivated code-switching.

However, such a repair model should also receive the source dialogue or explicit preservation notes, because target-only repair may erase legitimate pragmatic variation.

## Methods I Can Reuse

1. Separate the benchmark from the improvement method.
2. Create synthetic pragmatic corruptions from correct translations.
3. Train or prompt a repair stage to reverse those corruptions.
4. Measure whether the repair system is conservative.
5. Evaluate performance by phenomenon rather than only aggregate quality.
6. Analyse which error generators fail to produce realistic examples.
7. Compare target-only repair with source-aware repair.

## Methods I Should Not Copy Directly

1. Do not rely only on round-trip translation to create pragmatic failures.
2. Do not repair social meaning without consulting the source and context.
3. Do not assume all target consistency is desirable.
4. Do not equate more consistent wording with better pragmatics.
5. Do not begin the project with a large repair model before validating the benchmark.

## Questions Raised by the Paper

1. Can synthetic pragmatic failures be generated reliably?
2. Which failures require human-authored negative examples?
3. Can target-only repair distinguish intentional code-switching from inconsistency?
4. Should repair preserve speaker-specific variation rather than normalize it?
5. Can an LLM reranker act as a repair model without fine-tuning?
6. How should semantic faithfulness be checked after pragmatic repair?

## Final Takeaway

Context-aware repair is a practical intervention when the base translator is fixed. Its strongest lesson for the proposed project is methodological: synthetic errors must be validated carefully because a repair model cannot learn failure types that the corruption process does not reproduce.
