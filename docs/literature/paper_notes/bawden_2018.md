# Evaluating Discourse Phenomena in Neural Machine Translation

## Citation

Rachel Bawden, Rico Sennrich, Alexandra Birch, and Barry Haddow. 2018. *Evaluating Discourse Phenomena in Neural Machine Translation*. Proceedings of NAACL-HLT 2018, pages 1304 to 1313.

Source file: `N18-1118.pdf`

## One-Sentence Summary

The paper constructs hand-crafted contrastive test sets to determine whether context-aware MT models actually use previous source and target sentences for discourse-sensitive translation decisions.

## Research Problem

Standard MT metrics are weak at detecting discourse errors because:

- only a small number of words may change,
- a correct choice may depend on target-side consistency,
- reference overlap does not directly test use of context,
- aggregate BLEU gains do not show which discourse phenomena improved.

The paper therefore develops targeted evaluation sets where the correct translation cannot be selected without extra-sentential context.

## Main Research Questions

1. Can context-aware NMT models use previous sentences for coreference?
2. Can they use context for coherence, cohesion, and lexical disambiguation?
3. Is previous source context sufficient?
4. Does previous target context matter?
5. Which contextual architecture performs best under targeted evaluation?

## Motivation

A sentence can be ambiguous in isolation. Examples include:

- the gender of a translated pronoun,
- repetition of the same lexical choice across turns,
- selecting the correct sense of an ambiguous word.

The correct answer may depend on:

- the previous source sentence,
- the previous target translation,
- both source and target history.

## Dataset

### Language Pair

English to French.

### Training Domain

OpenSubtitles2016.

### Training Size

Approximately 29 million parallel subtitle sentences after cleaning.

### Targeted Evaluation Sets

Two hand-crafted test suites, inspired by real subtitle examples.

#### Coreference Set

- 50 example blocks.
- Four contrastive pairs per block.
- 200 contrastive pairs in total.
- Tests English *it* and *they* translated into gendered French forms.
- Includes correct and semi-correct target contexts.
- A context-agnostic model is structurally limited to 50 percent accuracy.

#### Coherence and Cohesion Set

- 100 example blocks.
- Two contrastive pairs per block.
- 200 contrastive pairs in total.
- Tests lexical alignment, repetition, and lexical disambiguation.

## Contrastive Evaluation Design

Each item contains:

1. a context sentence,
2. a current ambiguous source sentence,
3. a correct target translation,
4. an incorrect target translation differing in the targeted feature.

The model scores the candidate translations. Accuracy is the percentage of items where the correct candidate receives the higher score.

### Why This Design Is Strong

The current sentence alone is insufficient. The relevant antecedent or disambiguating evidence is deliberately placed in the previous sentence.

This prevents a sentence-level model from succeeding through local cues.

### Cost of the Design

The evaluation only tests the specific error perturbations that were constructed. It does not measure open-ended generation quality.

## Model or Method

### Base Architecture

Attentional recurrent encoder-decoder models implemented in Nematus.

### Baseline

Current sentence only.

### Single-Encoder Context Models

#### 2-TO-2

The previous and current source sentences are concatenated. The corresponding previous and current target sentences are also generated together.

#### 2-TO-1

The previous and current source sentences are concatenated, but the model generates only the current target sentence.

### Multi-Encoder Models

The previous sentence and current sentence are encoded separately.

The paper tests:

- concatenation of context vectors,
- gated combination,
- hierarchical attention.

Auxiliary input can be:

- previous source sentence,
- previous target sentence,
- both.

### Novel Combined Model

The best strategy combines:

- separate encoders,
- hierarchical attention,
- decoding of both previous and current target sentences.

## Evaluation Method

### General Translation Quality

Detokenized, case-sensitive BLEU on subtitle test sets from four genres:

- comedy,
- crime,
- fantasy,
- horror.

### Targeted Accuracy

Accuracy on the two 200-pair contrastive suites.

## Main Results

### Targeted Evaluation

A non-contextual baseline is at 50 percent by construction.

Several multi-encoder systems show limited gains despite BLEU improvements.

The best reported model reaches:

```text
72.5 percent on coreference
57.0 percent on coherence and cohesion
```

Some multi-encoder models remain around:

```text
50.0 percent on coreference
53.5 percent on coherence and cohesion
```

The results show that merely adding a context encoder does not guarantee effective use of context.

### Architectural Finding

Models that decode both the preceding and current target sentences perform better than models that use only previous source context.

This highlights the importance of target-side history. A translation decision may depend on how the earlier sentence was translated, not only on what the source said.

## Qualitative Findings

### Coreference

French pronoun gender must agree with the gender of the translated antecedent. The correct answer therefore depends on the previous target translation.

### Cohesion

Two synonymous target words may not be interchangeable when the dialogue establishes a pattern of repetition.

### Lexical Disambiguation

A word such as *steeper* can mean more expensive or more sharply sloped. The previous turn determines the correct meaning.

## Strengths

1. Directly tests whether context is necessary.
2. Uses a controlled 50 percent chance baseline.
3. Separates discourse performance from general BLEU.
4. Includes both source-side and target-side context.
5. Creates reusable automatic evaluation after manual test construction.
6. Demonstrates that context architecture and target-side history matter.

## Limitations

1. The test sets are hand-crafted and relatively small.
2. Only one preceding sentence is used.
3. The domain is subtitles.
4. The language pair is English to French.
5. The phenomena are limited to coreference, cohesion, and lexical disambiguation.
6. Contrastive scoring does not directly test free-form generation.
7. The model can be sensitive to artificial characteristics of the perturbations.
8. The paper evaluates discourse consistency rather than broader interpersonal pragmatics.
9. Speaker identity, role, politeness, stance, emotion, and speech acts are not explicitly annotated.

## Assumptions

- The relevant context is in the immediately previous sentence.
- One candidate is clearly correct and one is clearly incorrect.
- Model likelihood ranking reflects translation preference.
- Hand-crafted cases remain representative of real translation difficulties.

## Relevance to My Project

This paper provides the clearest methodological basis for the proposed contrastive benchmark.

A pragmatic item can follow the same structure:

```text
context
source utterance
pragmatically correct translation
minimally incorrect translation
phenomenon label
preservation requirement
```

Examples for the proposed project include:

- respectful versus overly familiar address,
- indirect refusal versus literal statement,
- teasing versus insult,
- warm concern versus neutral wording,
- meaningful code-switching versus unnecessary normalization.

## Methods I Can Reuse

1. Ensure the current utterance is ambiguous without context.
2. Put the decisive clue in a previous turn.
3. Construct minimally different contrastive candidates.
4. Balance the dataset so simple candidate bias gives chance performance.
5. Report accuracy by phenomenon.
6. Include source-only and source-plus-context conditions.
7. Test whether target-side context contributes.
8. Validate every contrastive pair with native speakers.

## Methods I Should Not Copy Directly

1. Do not restrict all context to one previous sentence without testing longer windows.
2. Do not assume candidate likelihood is available for every black-box system.
3. Do not use only automatic ranking.
4. Do not construct examples solely from English-source ambiguity.
5. Do not treat hand-crafted examples as naturally distributed dialogue.

## Questions Raised by the Paper

1. How can contrastive evaluation work for API systems that do not expose likelihoods?
2. Should evaluation use pairwise judging, candidate selection, or generation?
3. How can target-side context be supplied fairly when prior MT output may already be wrong?
4. How many previous turns are needed for Indian dialogue?
5. How can contrastive pairs isolate pragmatics without changing semantic adequacy?
6. How should multiple valid pragmatic interpretations be handled?

## Final Takeaway

Targeted contrastive evaluation reveals context sensitivity that BLEU cannot. The proposed project should use this controlled methodology, but expand the tested phenomena from discourse consistency to socially interpreted meaning.
