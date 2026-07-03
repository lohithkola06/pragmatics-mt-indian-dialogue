````markdown
# Research Questions

## Project Title

**Pragmatics-Preserving Machine Translation for Indian Dialogue**

## 1. Research Objective

The objective of this project is to determine whether current machine translation systems preserve the pragmatic and social meaning of Indian conversational dialogue.

The project focuses on cases where a translation retains the basic propositional meaning of an utterance but changes how the utterance is interpreted socially.

The benchmark will initially study:

- politeness and formality,
- indirect requests and refusals,
- stance and emotion,
- discourse-motivated code-switching, where feasible.

The project will compare sentence-level translation with context-aware, speaker-aware, and pragmatics-aware translation conditions.

---

## 2. Primary Research Question

### RQ1

> To what extent do current machine translation systems preserve the intended pragmatic and social meaning of Indian conversational dialogue?

This question examines whether a translated utterance preserves not only its factual content, but also:

- the intended speech act,
- politeness,
- formality,
- social distance,
- stance,
- emotion,
- indirectness,
- code-switching function,
- relationship between the speakers.

---

## 3. Pragmatic Failure Detection

### RQ2

> How often do machine translation systems produce translations that are semantically acceptable but pragmatically inappropriate?

A translation will be considered semantically acceptable when it preserves the basic propositional content of the source utterance.

It will be considered pragmatically inappropriate when it changes one or more of the following:

- the speaker's intention,
- the level of politeness,
- the degree of formality,
- the speech act,
- the level of indirectness,
- the emotional tone,
- the speaker's stance,
- the social relationship implied by the utterance.

### Measurement

For each translation, annotators will separately score:

```text
semantic_adequacy
pragmatic_preservation
````

A pragmatic failure will be recorded when:

```text
semantic_adequacy >= acceptable threshold
and
pragmatic_preservation < acceptable threshold
```

---

## 4. Phenomenon-Level Difficulty

### RQ3

> Which pragmatic phenomena are most difficult for current translation systems to preserve?

The initial comparison will include:

1. Politeness and formality
2. Indirect requests and refusals
3. Stance and emotion
4. Code-switching function, where included

### Subquestions

#### RQ3.1

Which systems most frequently change respectful language into neutral or informal language?

#### RQ3.2

Which systems fail to recognize indirect requests and refusals?

#### RQ3.3

Which systems flatten emotional or attitudinal distinctions such as warmth, irritation, playfulness, or dismissiveness?

#### RQ3.4

Which systems normalize code-switched dialogue even when the switch carries emphasis, humor, intimacy, identity, or emotional force?

### Measurement

Results will be reported separately by:

```text
primary_phenomenon
secondary_phenomenon
language
model
context_condition
speaker_relationship
```

---

## 5. Effect of Dialogue Context

### RQ4

> Does access to previous dialogue turns improve pragmatic preservation?

This question compares:

```text
Condition A: Current source utterance only
Condition B: Current source utterance plus dialogue context
```

### Subquestions

#### RQ4.1

Which pragmatic phenomena benefit most from dialogue context?

#### RQ4.2

How many previous turns are needed to resolve the intended meaning?

#### RQ4.3

Does irrelevant or excessive context reduce translation quality?

#### RQ4.4

Do short and ambiguous utterances benefit more from context than longer, self-contained utterances?

### Measurement

Each benchmark item will contain:

```text
context_required
minimum_context_window
relevant_context_turns
```

Performance will be compared for context windows of:

```text
0 previous turns
1 previous turn
2 previous turns
3 previous turns
```

---

## 6. Effect of Speaker Roles and Relationships

### RQ5

> Does providing speaker-role and relationship information improve pragmatic preservation?

Possible metadata includes:

* speaker role,
* listener role,
* relative status,
* familiarity,
* institutional relationship,
* familial relationship,
* professional relationship.

### Experimental Conditions

```text
Condition A: Source utterance only
Condition B: Source utterance plus dialogue context
Condition C: Dialogue context plus speaker-role information
```

### Subquestions

#### RQ5.1

Does speaker-role information improve pronoun and honorific selection?

#### RQ5.2

Does relationship information improve the preservation of politeness and formality?

#### RQ5.3

Can speaker metadata help when the textual context does not contain explicit social cues?

#### RQ5.4

Does incorrect or incomplete role information harm translation quality?

---

## 7. Contrastive Evaluation

### RQ6

> Can contrastive evaluation reliably distinguish pragmatically correct translations from semantically similar but pragmatically incorrect translations?

Each contrastive item will contain:

1. dialogue context,
2. source utterance,
3. pragmatically appropriate translation,
4. minimally different pragmatic failure,
5. explanation of the targeted difference.

### Example Structure

```text
Context:
A student is speaking to a professor.

Source:
Aap kal available honge kya?

Pragmatically appropriate:
Would you be available tomorrow?

Contrastive:
Are you free tomorrow?

Targeted difference:
The contrastive version reduces the original formality and deference.
```

### Subquestions

#### RQ6.1

Can MT models assign a higher likelihood to the pragmatically correct candidate?

#### RQ6.2

Can LLM evaluators select the correct candidate reliably?

#### RQ6.3

Can native speakers consistently identify the intended candidate?

#### RQ6.4

Which pragmatic categories are easiest or hardest to evaluate contrastively?

#### RQ6.5

Does contrastive accuracy correlate with open-ended translation quality?

---

## 8. Automatic Metrics and Human Judgments

### RQ7

> How well do automatic translation metrics agree with native-speaker judgments of pragmatic preservation?

The project will compare:

* BLEU,
* chrF,
* COMET,
* BERTScore,
* rule-based checks,
* pragmatic classifiers,
* context-aware metrics,
* LLM-based evaluators.

### Subquestions

#### RQ7.1

Can standard semantic metrics detect pragmatic failures?

#### RQ7.2

Do context-aware metrics perform better on context-dependent items?

#### RQ7.3

Do LLM evaluators identify subtle pragmatic errors more reliably than conventional metrics?

#### RQ7.4

Does evaluator performance vary by pragmatic category?

#### RQ7.5

Do reference-free metrics benefit more from dialogue context than reference-based metrics?

### Measurement

Automatic scores will be compared with human judgments using:

```text
Spearman correlation
Pearson correlation
classification accuracy
macro F1
Cohen's kappa
Krippendorff's alpha
```

The exact measure will depend on whether the annotation is numerical, categorical, or pairwise.

---

## 9. Effect of Explicit Pragmatic Instructions

### RQ8

> Can explicit pragmatic instructions improve translation quality?

The system may receive labels such as:

```text
POLITE
FORMAL
INDIRECT_REFUSAL
PLAYFUL
IRRITATED
DEFERENTIAL
CODE_SWITCH_EMPHASIS
```

### Experimental Conditions

```text
Condition A: No pragmatic instruction
Condition B: Pragmatic category label
Condition C: Natural-language preservation instruction
Condition D: Context plus pragmatic instruction
Condition E: Context plus speaker roles plus pragmatic instruction
```

### Subquestions

#### RQ8.1

Do categorical labels improve preservation?

#### RQ8.2

Are natural-language instructions more effective than short labels?

#### RQ8.3

Does explicit control improve pragmatic quality without reducing semantic adequacy?

#### RQ8.4

Which pragmatic properties are easiest to control?

#### RQ8.5

Can a model preserve an existing pragmatic feature, rather than only generate a requested style?

---

## 10. Candidate Generation and Reranking

### RQ9

> Can pragmatic reranking improve translation selection without retraining the translation model?

The system will generate multiple candidate translations.

Each candidate may receive:

```text
semantic_score
pragmatic_score
fluency_score
overall_score
```

A combined score may be defined as:

```text
overall_score =
alpha * semantic_score
+
beta * pragmatic_score
+
gamma * fluency_score
```

### Subquestions

#### RQ9.1

Does pragmatic reranking outperform selecting the highest-probability translation?

#### RQ9.2

How should semantic and pragmatic scores be weighted?

#### RQ9.3

Does reranking help only when the candidate set already contains a pragmatically suitable option?

#### RQ9.4

Can reranking introduce semantic errors while improving style?

#### RQ9.5

Which evaluator is most suitable for pragmatic reranking?

---

## 11. Language and Source-Type Effects

### RQ10

> How does pragmatic preservation vary across language varieties and dataset construction methods?

Possible source types include:

```text
naturally occurring dialogue
native-speaker elicitation
minimal pairs
code-mixed dialogue
```

### Subquestions

#### RQ10.1

Are failures more frequent in code-mixed dialogue than in monolingual dialogue?

#### RQ10.2

Do systems perform differently on natural and elicited examples?

#### RQ10.3

Are minimal pairs more effective than naturally occurring examples for isolating pragmatic differences?

#### RQ10.4

Does performance vary between Hindi, Hinglish, Telugu, or other included language settings?

#### RQ10.5

Do different language varieties require different annotation categories?

---

## 12. Human Annotation Reliability

### RQ11

> Can native speakers reliably agree on pragmatic preservation judgments?

This question evaluates whether the annotation framework is sufficiently clear and reproducible.

### Subquestions

#### RQ11.1

Which pragmatic categories have the highest inter-annotator agreement?

#### RQ11.2

Which categories produce frequent disagreement?

#### RQ11.3

Does providing dialogue context improve annotator agreement?

#### RQ11.4

Does providing preservation notes bias annotators?

#### RQ11.5

How much variation is caused by dialect, region, age, or language background?

### Measurement

Possible agreement statistics include:

```text
Cohen's kappa
Fleiss' kappa
Krippendorff's alpha
percentage agreement
```

Disagreements will be retained and analysed rather than removed automatically.

---

## 13. Error Severity

### RQ12

> Which pragmatic failures are minor stylistic differences, and which cause meaningful changes in social interpretation?

Proposed severity levels:

```text
MINOR
MAJOR
CRITICAL
```

### Definitions

#### Minor

The translation is slightly less natural or stylistically weaker, but the intended relationship and communicative act remain clear.

#### Major

The translation changes the intended tone, politeness, speech act, or level of indirectness.

#### Critical

The translation can cause substantial misunderstanding, offense, escalation, or reversal of the speaker's intention.

### Subquestions

#### RQ12.1

Which phenomena produce the most severe failures?

#### RQ12.2

Do automatic metrics distinguish minor and major pragmatic errors?

#### RQ12.3

Do context-aware systems reduce severe errors more than minor errors?

---

## 14. Primary Hypotheses

### H1

Sentence-level translation systems will produce semantically acceptable but pragmatically incorrect translations on a measurable proportion of benchmark items.

### H2

Dialogue context will improve pragmatic preservation, especially for:

* indirect requests,
* indirect refusals,
* ambiguous speech acts,
* politeness choices,
* stance interpretation.

### H3

Speaker-role and relationship metadata will improve politeness and formality preservation beyond raw dialogue context alone.

### H4

Standard semantic metrics will show weak sensitivity to pragmatic failures when the literal content remains similar.

### H5

Contrastive evaluation will reveal pragmatic differences more clearly than corpus-level semantic metrics.

### H6

Native-speaker judgments will detect failures that automatic metrics and LLM judges miss.

### H7

Explicit pragmatic instructions will improve preservation but may occasionally reduce semantic adequacy or naturalness.

### H8

Code-switching will frequently be normalized or removed even when it serves a discourse or social function.

### H9

Short, ambiguous utterances will benefit more from context than longer, self-contained utterances.

### H10

Automatic evaluator performance will vary substantially across pragmatic categories.

---

## 15. Null Hypotheses

### H0.1

Dialogue context does not significantly improve pragmatic preservation.

### H0.2

Speaker-role metadata does not provide additional improvement beyond dialogue context.

### H0.3

Pragmatic instructions do not significantly improve translation quality.

### H0.4

Automatic metrics correlate with pragmatic human judgments as strongly as they correlate with semantic judgments.

### H0.5

Contrastive evaluation does not provide additional information beyond standard metrics.

### H0.6

There is no significant difference in pragmatic failure rate across translation systems.

---

## 16. Operational Variables

### Independent Variables

```text
translation system
language
source type
context window
speaker-role information
pragmatic instruction
evaluation method
pragmatic category
```

### Dependent Variables

```text
semantic adequacy score
pragmatic preservation score
contrastive accuracy
politeness preservation score
formality preservation score
speech-act preservation score
stance preservation score
indirectness preservation score
code-switch preservation score
human preference
automatic metric score
```

### Control Variables

Where possible, the experiments will control for:

```text
source length
target length
decoding settings
prompt format
model version
reference availability
context length
item difficulty
```

---

## 17. Mapping Research Questions to Experiments

| Research Question | Main Experiment                       | Primary Output                     |
| ----------------- | ------------------------------------- | ---------------------------------- |
| RQ1               | Overall benchmark evaluation          | Pragmatic preservation rate        |
| RQ2               | Semantic versus pragmatic comparison  | Pragmatic failure rate             |
| RQ3               | Category-level analysis               | Per-phenomenon performance         |
| RQ4               | Sentence-only versus context-aware    | Context improvement                |
| RQ5               | Context versus role-aware translation | Role-information improvement       |
| RQ6               | Contrastive ranking                   | Contrastive accuracy               |
| RQ7               | Metric and human comparison           | Correlation and agreement          |
| RQ8               | Pragmatic prompting                   | Controlled-translation improvement |
| RQ9               | Candidate reranking                   | Reranking gain                     |
| RQ10              | Language and source comparison        | Cross-group performance            |
| RQ11              | Pilot annotation                      | Inter-annotator agreement          |
| RQ12              | Severity analysis                     | Error-severity distribution        |

---

## 18. Primary Questions for the Initial Pilot

The pilot will prioritize the following questions:

### Pilot RQ1

Can native speakers consistently distinguish semantic adequacy from pragmatic preservation?

### Pilot RQ2

Are the selected categories sufficiently clear and distinct?

### Pilot RQ3

Can valid contrastive negative translations be created without changing the core semantics?

### Pilot RQ4

Does dialogue context change how annotators judge the translation?

### Pilot RQ5

Do current translation systems exhibit enough pragmatic failures to justify a larger benchmark?

### Pilot RQ6

What context window is sufficient for most items?

### Pilot RQ7

Which categories should be retained, revised, merged, or removed?

---

## 19. Questions Outside the Initial Scope

The first phase will not attempt to answer:

* whether a newly trained large translation model can outperform existing systems,
* whether all Indian languages exhibit the same pragmatic failure patterns,
* whether speech prosody improves pragmatic translation,
* whether visual context improves dialogue translation,
* whether pragmatic failures can be eliminated completely,
* whether one universal pragmatic taxonomy applies across all Indian communities,
* whether automatic metrics can fully replace human judgment.

These questions may be considered in later work.

---

## 20. Expected Research Outcome

The project should produce evidence about:

1. how frequently pragmatic failure occurs,
2. which phenomena are most difficult,
3. when context is useful,
4. whether speaker roles provide additional information,
5. whether contrastive evaluation is reliable,
6. how well automatic metrics align with humans,
7. whether lightweight interventions reduce failure.

The final objective is not only to determine whether a translation is semantically correct, but whether the target-language listener would understand the speaker's intention, attitude, and relationship in the intended way.

```
```
