# Controlling Neural Machine Translation Formality with Synthetic Supervision

## Citation

Xing Niu and Marine Carpuat. 2020. *Controlling Neural Machine Translation Formality with Synthetic Supervision*. Proceedings of the Thirty-Fourth AAAI Conference on Artificial Intelligence, pages 8568 to 8574.

Source file: `AAAI_NiuX-4350.pdf`

## One-Sentence Summary

The paper trains a neural formality-sensitive MT model using synthetic labels inferred from bilingual data and shows that output formality can be controlled while preserving meaning.

## Research Problem

An ideal formality-sensitive MT dataset would contain triplets:

```text
source sentence
target formality label
reference translation
```

Such data is generally unavailable. Existing resources usually provide either:

- bilingual translation pairs without formality labels, or
- monolingual formal-informal rewrite pairs.

The paper asks whether these incomplete resources can be combined to simulate direct supervision for formality-sensitive MT.

## Main Research Questions

1. Can synthetic formality labels turn zero-shot formality-sensitive MT into a more directly supervised task?
2. Do source-side and target-side style tags improve formality control?
3. Can stronger formality differences be generated without losing source meaning?
4. Which synthetic supervision strategy is more reliable?

## Motivation

Formality-sensitive translation requires the model to preserve content while independently controlling style. A model trained only on ordinary translation and monolingual style transfer must generalize across tasks without seeing true bilingual style-labelled examples.

The paper argues that synthetic supervision can bridge this gap.

## Task Definition

Given a French source sentence and a desired English target formality:

```text
informal
formal
```

generate an English translation with the requested style.

The model must support both:

- formality transfer, such as informal to formal,
- formality preservation, such as informal to informal.

## Dataset

### Language Pair

French to English for translation.

English to English for bidirectional formality transfer.

### Formality Transfer Dataset

GYAFC:

- approximately 105,000 informal-formal training pairs,
- approximately 10,000 development examples,
- approximately 5,000 test examples for each direction.

### Machine Translation Corpora

| Corpus | Sentence Pairs | English Tokens |
|---|---:|---:|
| Europarl v7 | 1,670,324 | 39,789,959 |
| News Commentary v14 | 276,358 | 6,386,435 |
| OpenSubtitles2016 | 16,000,000 | 171,034,255 |

### MT Evaluation Sets

- WMT newstest2014, predominantly written news.
- Microsoft Speech Language Translation, abbreviated MSLT, conversational speech.

## Model or Method

### Multitask Base Model

The system jointly learns:

1. French-to-English translation.
2. English formal-to-informal transfer.
3. English informal-to-formal transfer.

A shared attentional recurrent encoder-decoder is used.

### Style Tags

The paper compares:

- no style tags,
- source-side style tags,
- source-side tags with blocked encoder visibility,
- tags on both source and target sequences.

The preferred method is `TAG-SRC-TGT`, where the requested formality is represented on both sides during training.

### Why Tags on Both Sides Matter

Source-side tags influence encoder states and attention. Target-side tags provide a direct signal to the decoder.

This makes it easier for one model to:

- change formality,
- preserve formality when no change is required.

## Synthetic Supervision

### Online Style Inference, OSI

For a bilingual pair `(X, Y)`:

1. Generate an informal translation of `X`.
2. Generate a formal translation of `X`.
3. Compare the reference `Y` with both outputs using cross-entropy difference.
4. Label `Y` as formal, informal, or unknown.
5. Train on the synthetic triplet `(X, inferred style, Y)`.

The threshold is determined dynamically within each minibatch.

### Online Target Inference, OTI

Instead of inferring a label, OTI generates a synthetic target sequence for a randomly selected desired style.

The paper expects OTI to be noisier because it synthesizes a complete sentence rather than a single style label.

## Evaluation Method

### Formality Transfer and Preservation

The model is evaluated on:

- informal to formal,
- formal to informal,
- informal to informal,
- formal to formal.

BLEU is used because GYAFC provides style-specific references.

### Surface Difference Metric

The paper introduces LEPOD, combining:

- lexical difference,
- positional difference.

LEPOD measures how much formal and informal outputs differ. It does not directly establish whether the changes are correct.

### Human Evaluation

The authors sample approximately 150 WMT examples and 150 MSLT examples.

Thirty native or near-native English speakers compare system outputs.

Each comparison receives five independent judgments unless the first three judgments agree.

Annotators evaluate:

1. which output better preserves meaning,
2. which output is more formal or informal as requested.

Krippendorff's alpha is approximately 0.5, indicating moderate disagreement about formality. MACE is used to aggregate judgments while estimating annotator competence.

## Main Results

### Style-Tagging Results

| Model | I to F | F to I | I to I | F to F |
|---|---:|---:|---:|---:|
| No tags | 70.63 | 37.00 | 54.54 | 58.98 |
| Source tag | 72.16 | 37.67 | 66.87 | 78.78 |
| Source and target tags | 72.29 | 37.62 | 67.81 | 79.34 |

Source and target tags give the best overall results, especially for preserving an existing formality level.

### Output-Difference Results

Online Style Inference produces the largest formal-informal surface differences among the reported systems.

Representative LEPOD components:

| System | WMT LED | WMT POD | MSLT LED | MSLT POD |
|---|---:|---:|---:|---:|
| Multi-Task | 10.89 | 7.76 | 11.97 | 1.41 |
| Synthetic Style / OSI | 14.53 | 12.58 | 14.52 | 2.19 |

### Human Evaluation

Compared with the multitask baseline:

- OSI informal translations are judged more informal.
- OSI formal translations are judged more formal.
- OSI also receives more judgments indicating better meaning preservation.

The synthetic-style approach therefore improves control without merely producing larger but incorrect changes.

## Qualitative Findings

The model learns diverse transformation types, including:

- contractions,
- filler words,
- quotation changes,
- possessive changes,
- question-form changes,
- sentence-length changes,
- lexical substitution,
- structural reordering.

This is important because formality is not only a word-choice phenomenon.

## Strengths

1. Addresses the lack of style-labelled bilingual data.
2. Uses a single multitask model for translation and formality transfer.
3. Separately evaluates formality control and meaning preservation.
4. Tests both transfer and preservation.
5. Uses automatic and human evaluation.
6. Demonstrates that style tags can influence both encoder and decoder representations.
7. Analyses the kinds of transformations produced.

## Limitations

1. The style distinction is binary: formal versus informal.
2. English monolingual rewrite data is still required.
3. Synthetic labels can be noisy.
4. LEPOD measures difference, not correctness.
5. Human agreement on formality is only moderate.
6. The translation task is limited to French to English.
7. The model does not infer the socially appropriate style from a dialogue context.
8. It does not model speaker relationship, speech act, stance, sarcasm, or indirectness.
9. Formality labels may not transfer cleanly across cultures.
10. The recurrent architecture is not representative of current large multilingual models, although the conceptual method remains relevant.

## Assumptions

- Formality can be represented using two classes.
- Monolingual style-transfer supervision is transferable to bilingual generation.
- Cross-entropy differences provide useful pseudo-labels.
- Meaning preservation can be assessed through pairwise human comparison.

## Relevance to My Project

The paper provides a concrete design for pragmatic control when fully annotated bilingual data is unavailable.

Potential adaptation:

```text
translation task
+
pragmatic classification or rewriting task
+
synthetic pragmatic labels
```

For example, a model could be trained or prompted with labels such as:

```text
RESPECTFUL
INFORMAL
INDIRECT_REFUSAL
PLAYFUL
IRRITATED
```

However, the primary project should first evaluate preservation before attempting synthetic training.

## Methods I Can Reuse

1. Use explicit tags on both the input and generated-output interface.
2. Test whether the system can preserve as well as change an attribute.
3. Evaluate meaning and pragmatic quality separately.
4. Use pairwise human comparisons for subtle style differences.
5. Measure annotator agreement and model annotator reliability.
6. Generate synthetic labels only after validating them against native-speaker judgments.
7. Analyse the surface operations associated with pragmatic changes.

## Methods I Should Not Copy Directly

1. Do not treat all pragmatics as binary style transfer.
2. Do not assume synthetic labels are ground truth.
3. Do not use output difference as evidence of pragmatic success.
4. Do not build the first benchmark around model training rather than evaluation.
5. Do not rely on English-only formality resources for Indian-language phenomena without validation.

## Questions Raised by the Paper

1. Can synthetic supervision work for indirectness or speech acts?
2. Can pragmatic labels be inferred from speaker roles and context?
3. How much native-speaker data is required to validate pseudo-labels?
4. Should an Indian-language benchmark include preservation and controlled transformation tasks?
5. How should disagreements about formality be represented?
6. Can current instruction-tuned LLMs perform the control task without fine-tuning?

## Final Takeaway

Synthetic supervision can improve explicit style control, but it does not solve the central preservation problem automatically. The most reusable ideas are multi-attribute conditioning, separate meaning evaluation, and human validation of synthetic labels.
