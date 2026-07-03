# Controlling Politeness in Neural Machine Translation via Side Constraints

## Citation

Rico Sennrich, Barry Haddow, and Alexandra Birch. 2016. *Controlling Politeness in Neural Machine Translation via Side Constraints*. Proceedings of NAACL-HLT 2016, pages 35 to 40.

Source file: `N16-1005.pdf`

## One-Sentence Summary

The paper shows that a neural MT system can be made to produce polite or informal German translations by adding a politeness tag to the English source sentence.

## Research Problem

Many target languages grammatically distinguish familiar and polite forms of address, while the source language may not provide enough information to determine the correct form. English does not encode the German T-V distinction directly. The English pronoun *you* may need to become informal *du/ihr* or polite *Sie* in German.

A standard sentence-level MT model must guess this distinction. The authors instead ask whether the desired politeness level can be supplied as an explicit control variable.

## Main Research Questions

1. Can the production of honorific forms be controlled in NMT using side constraints?
2. Does choosing the correct T-V form materially affect translation quality?
3. Can one model support multiple politeness settings without building separate systems?

## Motivation

Honorific and address choices express:

- politeness,
- social distance,
- relative social status,
- familiarity,
- register.

These properties are not decorative. A wrong choice can make a translation socially inappropriate even when the propositional content remains understandable.

The paper also frames politeness control as one example of a broader problem: target-language features may be absent, underspecified, or distributed differently in the source language.

## Task Definition

The system performs English-to-German translation under one of three test-time conditions:

- no politeness constraint,
- polite constraint,
- informal constraint.

An oracle condition supplies the constraint that matches the reference translation.

## Dataset

### Language Pair

English to German.

### Domain

Movie and television subtitles.

### Training Data

OpenSubtitles2012.

The training corpus contains approximately 5.58 million sentence pairs. Automatic target-side annotation labels approximately:

- 0.48 million pairs as polite,
- 1.09 million pairs as informal,
- the remaining pairs as neutral.

### Test Data

Random samples from OpenSubtitles2013.

The paper reports results for:

1. 2,000 source sentences containing an English second-person pronoun.
2. 2,000 randomly sampled source sentences.

## Politeness Annotation

The target-side German sentence is automatically classified using morphosyntactic rules.

### Informal Indicators

- informal second-person pronouns,
- imperative verb forms.

### Polite Indicators

- capitalized German polite pronouns,
- relevant morphological analyses.

### Neutral Class

Sentences that do not match polite or informal rules are treated as neutral.

### Important Design Choice

Annotation is sentence-level rather than token-level because the target honorific may not have a direct word-level correspondence in the source.

### Annotation Weakness

Some forms are ambiguous, especially sentence-initial *Sie*. The annotation procedure therefore uses English-side evidence such as the presence of *you* or *your* in certain cases.

## Model or Method

### Base Architecture

An attentional encoder-decoder NMT model using bidirectional gated recurrent units.

### Side Constraint

A special token is appended to the source sentence:

```text
<T>
<V>
```

`<T>` represents informal address and `<V>` represents polite address.

The token becomes part of the encoder input. The model learns to condition target generation on the tag.

### Training Strategy

Only a subset of labelled examples is tagged during each training epoch. The marking probability is 0.5.

Neutral sentences are also randomly marked with polite or informal tags at the same probability. This prevents the system from assuming that every tagged sentence must contain an address form and reduces overproduction of pronouns or honorifics.

### Test-Time Control

The user provides the desired politeness tag. The same trained model generates polite or informal output depending on the selected tag.

## Evaluation Method

### Automatic Politeness Labelling

Generated German output is passed through the same rule-based polite, informal, or neutral classifier.

### BLEU

BLEU measures similarity to the single reference translation.

### Oracle Evaluation

The oracle condition selects the side constraint that matches the reference label. This estimates the potential benefit when the desired politeness level is known.

## Main Results

### Pronoun-Containing Test Set

For 2,000 English sentences containing a second-person pronoun:

| Condition | BLEU | Main Behaviour |
|---|---:|---|
| No constraint | 20.7 | Strong informal bias |
| Polite | 17.9 | Output overwhelmingly polite or neutral |
| Informal | 20.2 | Output overwhelmingly informal or neutral |
| Oracle | 23.9 | Correct reference-side constraint |

The polite setting produced polite or neutral output for about 96 percent of items. The informal setting produced informal or neutral output for about 98 percent.

The oracle setting improved BLEU by 3.2 points over the unconstrained baseline.

### Random Test Set

For 2,000 random sentences:

| Condition | BLEU |
|---|---:|
| No constraint | 22.6 |
| Polite | 21.7 |
| Informal | 22.5 |
| Oracle | 24.0 |

The control remained effective without causing widespread overproduction of address pronouns.

## Qualitative Findings

The system can generate direct polite and informal variants of the same source sentence.

However, the constraint is soft. Strong lexical clues in the source can override it. For example, an insulting sentence such as *You foolish boy* remains informal even when the polite constraint is supplied.

This is useful evidence that pragmatic control interacts with semantic and lexical compatibility. A label does not guarantee that every output can naturally express the requested style.

## Strengths

1. Simple method with minimal architectural modification.
2. One model supports multiple politeness settings.
3. Target-side linguistic annotation is converted into a source-side control signal.
4. The paper demonstrates that politeness is measurable and controllable.
5. The method can potentially generalize to register, dialect, participant gender, participant number, and other target-side features.

## Limitations

1. The politeness distinction is binary and centred on German T-V forms.
2. The desired level is supplied by the user rather than inferred from discourse.
3. No speaker-role or conversational-context information is modelled.
4. The automatic annotation rules contain ambiguity and noise.
5. BLEU rewards matching the reference politeness, but it is not a direct measure of social appropriateness.
6. The subtitle domain contains alignment noise and free translations.
7. The method controls visible forms of address but does not evaluate indirectness, speech acts, sarcasm, warmth, teasing, or other pragmatic dimensions.
8. The evaluation does not establish whether the selected politeness is correct for the real speaker relationship.

## Assumptions

- The desired politeness class is known at test time.
- The target-side class can be annotated reliably enough during training.
- A sentence-level tag is sufficient for the intended control.
- Politeness can be represented by the T-V distinction for the selected language pair.

## Relevance to My Project

This paper provides direct support for treating pragmatic information as an explicit variable rather than as an accidental property of MT output.

For Indian languages, analogous control dimensions may include:

- Hindi `tu`, `tum`, and `aap`,
- respectful verb agreement,
- Telugu honorific pronouns and verbal forms,
- titles and kinship terms,
- formal versus familiar register.

The paper also motivates an experiment comparing:

```text
No pragmatic instruction
Politeness label
Speaker-role information
Dialogue context
Dialogue context plus politeness label
```

## Methods I Can Reuse

1. Add categorical pragmatic tags as source-side control tokens or prompt fields.
2. Annotate visible target-side politeness markers using rules.
3. Test a neutral class so labels are not forced onto irrelevant examples.
4. Compare uncontrolled, controlled, and oracle conditions.
5. Measure whether requested pragmatic labels actually change output.
6. Separate semantic quality from control accuracy.

## Methods I Should Not Copy Directly

1. Do not reduce Indian politeness to a single binary T-V label.
2. Do not assume the correct style is externally known in the main preservation task.
3. Do not rely on BLEU as the main evaluation signal.
4. Do not treat visible pronouns as a complete representation of politeness.
5. Do not evaluate isolated sentences when the correct choice depends on speaker relations.

## Questions Raised by the Paper

1. Can speaker roles predict the correct politeness label automatically?
2. How should multi-level politeness be annotated?
3. Can a system preserve politeness without an explicit label?
4. What happens when the source contains conflicting cues?
5. Can side constraints control indirectness or teasing, or only visible morphology?
6. How should control accuracy be measured when multiple translations are socially acceptable?

## Final Takeaway

The paper proves that politeness can be represented as an explicit control signal in MT. For the proposed research, its main value is not the German-specific model. Its value is the experimental principle that socially meaningful translation properties should be annotated, controlled, and evaluated separately from general semantic quality.
