# Benchmark Blueprint

## Project Title

**Pragmatics-Preserving Machine Translation for Indian Dialogue**

## 1. Benchmark Purpose

This benchmark is designed to evaluate whether machine translation systems preserve the pragmatic and social meaning of Indian conversational dialogue.

The benchmark focuses on cases where a translation may preserve the literal or propositional content of an utterance while changing one or more of the following:

- politeness,
- formality,
- speech act,
- stance,
- emotion,
- indirectness,
- social relationship,
- discourse function of code-switching.

The benchmark is intended to make these failures measurable through a combination of:

1. context-sensitive dialogue items,
2. pragmatic annotations,
3. reference translations,
4. contrastive incorrect translations,
5. human evaluation,
6. automatic and LLM-based evaluation.

The primary contribution is an evaluation resource and protocol rather than a new translation model.

---

## 2. Benchmark Goals

The benchmark should support the following goals:

### Goal 1: Identify Pragmatic Failures

Detect cases where a translation is semantically acceptable but pragmatically inappropriate.

### Goal 2: Measure Context Sensitivity

Determine whether dialogue context improves translation quality.

### Goal 3: Evaluate Speaker Awareness

Test whether speaker-role and relationship information improves pragmatic preservation.

### Goal 4: Compare Translation Systems

Evaluate Indian-language MT systems, multilingual MT models, and multilingual LLMs under the same conditions.

### Goal 5: Compare Evaluation Methods

Measure how well automatic metrics, classifiers, rules, and LLM judges agree with native-speaker judgments.

### Goal 6: Support Intervention Experiments

Test whether prompting, pragmatic labels, speaker metadata, candidate reranking, or repair methods reduce pragmatic failure.

---

## 3. Initial Benchmark Scope

### 3.1 Initial Language Direction

Recommended starting point:

```text
Hindi or Hinglish to English
```

Possible second phase:

```text
Telugu to English
```

The first release should focus on one primary language setting. Expansion should happen only after the annotation schema and evaluation protocol have been validated.

### 3.2 Pilot Size

```text
30 to 50 items
```

### 3.3 Full Benchmark Size

```text
300 to 500 items
```

A later extension may increase the benchmark to approximately 800 items if annotation quality and project time allow.

### 3.4 Context Window

Each item should contain:

```text
0 to 3 previous dialogue turns
```

The benchmark should explicitly record the minimum context needed to interpret the utterance correctly.

### 3.5 Primary Pragmatic Categories

The initial version should include:

1. Politeness and formality
2. Indirect requests and refusals
3. Stance and emotion

Optional fourth category:

4. Discourse-motivated code-switching

---

## 4. Benchmark Tasks

The benchmark should support multiple evaluation tasks.

## 4.1 Open-Ended Translation

### Input

- dialogue context,
- current source utterance,
- optional speaker metadata.

### Output

- target-language translation.

### Purpose

Evaluate real translation behaviour under different context conditions.

---

## 4.2 Contrastive Ranking

### Input

- dialogue context,
- source utterance,
- one pragmatically correct translation,
- one minimally different pragmatic failure.

### Output

- preferred translation.

### Purpose

Test whether a system or evaluator can distinguish pragmatic correctness from semantic similarity.

---

## 4.3 Pragmatic Error Classification

### Input

- dialogue context,
- source utterance,
- generated translation.

### Output

One or more labels:

```text
PRESERVED
PARTIALLY_PRESERVED
NOT_PRESERVED
UNCERTAIN
```

Optional error categories:

```text
POLITENESS_ERROR
FORMALITY_ERROR
SPEECH_ACT_ERROR
STANCE_ERROR
EMOTION_ERROR
INDIRECTNESS_ERROR
CODE_SWITCH_ERROR
RELATIONSHIP_ERROR
```

---

## 4.4 Severity Classification

### Input

- source,
- context,
- translation,
- identified pragmatic error.

### Output

```text
MINOR
MAJOR
CRITICAL
```

### Definitions

#### Minor

The translation is slightly less natural or less socially precise, but the intended relationship and communicative act remain understandable.

#### Major

The translation changes the intended tone, politeness, speech act, or indirectness in a meaningful way.

#### Critical

The translation can cause substantial misunderstanding, offense, escalation, or reversal of the speaker's intended meaning.

---

## 4.5 Context Necessity Classification

### Input

- source utterance,
- optional previous turns.

### Output

```text
CONTEXT_NOT_REQUIRED
CONTEXT_HELPFUL
CONTEXT_REQUIRED
```

### Purpose

Identify which items genuinely test contextual interpretation.

---

## 5. Pragmatic Category Definitions

## 5.1 Politeness

Politeness captures the degree of respect, deference, familiarity, or social distance encoded in the utterance.

Possible labels:

```text
HIGHLY_RESPECTFUL
RESPECTFUL
POLITE
NEUTRAL
FAMILIAR
DISRESPECTFUL
```

Indicative signals may include:

- pronoun choice,
- honorifics,
- titles,
- verb agreement,
- request softeners,
- kinship terms,
- respectful particles.

---

## 5.2 Formality

Formality captures the register or situational style of the utterance.

Possible labels:

```text
FORMAL
NEUTRAL
INFORMAL
HIGHLY_INFORMAL
```

Politeness and formality should remain separate.

A sentence may be polite but informal, or formal without being particularly polite.

---

## 5.3 Speech Act

Speech act captures the intended communicative function.

Possible labels:

```text
REQUEST
COMMAND
SUGGESTION
REFUSAL
WARNING
APOLOGY
COMPLAINT
INVITATION
TEASING
INSULT
JOKE
AGREEMENT
DISAGREEMENT
REASSURANCE
CRITICISM
```

---

## 5.4 Indirectness

Indirectness captures whether the utterance communicates meaning explicitly or through implication.

Possible labels:

```text
DIRECT
MODERATELY_INDIRECT
HIGHLY_INDIRECT
```

Functional labels may include:

```text
INDIRECT_REQUEST
INDIRECT_REFUSAL
SOFTENED_CRITICISM
HINT
POLITE_DISAGREEMENT
IMPLIED_WARNING
```

---

## 5.5 Stance

Stance captures the speaker's position or attitude toward the listener, proposition, or situation.

Possible labels:

```text
WARM
CARING
PLAYFUL
IRRITATED
DISMISSIVE
DEFERENTIAL
RELUCTANT
SYMPATHETIC
SKEPTICAL
APPROVING
DISAPPROVING
```

---

## 5.6 Emotion

Emotion captures the affective state expressed by the speaker.

Possible labels:

```text
NEUTRAL
HAPPY
ANGRY
SAD
WORRIED
EXCITED
FRUSTRATED
EMBARRASSED
AFRAID
SURPRISED
```

Emotion and stance should be separated where possible.

---

## 5.7 Code-Switching Function

Code-switching should only be annotated when the language switch has a meaningful discourse function.

Possible labels:

```text
EMPHASIS
HUMOR
IDENTITY
INTIMACY
AUTHORITY
TECHNICAL_TERMINOLOGY
EMOTIONAL_INTENSITY
SARCASM
QUOTATION
```

The benchmark should not assume that every foreign-language token is pragmatically meaningful.

---

## 6. Dataset Construction Strategy

The benchmark should combine three complementary sources.

## 6.1 Naturally Occurring Dialogue

Possible sources:

- openly licensed subtitle corpora,
- conversational datasets,
- public code-mixed corpora,
- public dialogue resources.

Requirements:

- verify licensing,
- remove personally identifying information,
- document the original source,
- retain enough context for interpretation,
- record whether the utterance was originally produced in the source language.

---

## 6.2 Native-Speaker Elicitation

Native speakers may create short dialogues using prompts designed to target specific pragmatic phenomena.

Example elicitation prompt:

```text
Write a two-turn Hinglish dialogue where a younger person politely refuses a request from an older person without explicitly saying no.
```

Each elicited item should be reviewed for:

- naturalness,
- plausibility,
- regional appropriateness,
- clarity of pragmatic intent,
- category fit.

---

## 6.3 Minimal Pairs

Minimal pairs should differ in one targeted pragmatic feature.

Example:

```text
Respectful:
Aap thodi der wait kar sakte hain?

Familiar:
Tum thodi der wait kar sakte ho?
```

Minimal pairs are useful for:

- controlled evaluation,
- contrastive testing,
- isolating one pragmatic difference,
- testing sensitivity to small changes.

---

## 7. Benchmark Item Schema

Each benchmark item should follow a structured JSON format.

```json
{
  "item_id": "HIN_POL_001",
  "language": "Hindi",
  "language_variety": "Standard Hindi",
  "translation_direction": "Hindi-English",
  "source_type": "elicited",
  "source_reference": null,
  "context": [
    {
      "turn_id": 1,
      "speaker_id": "A",
      "speaker_role": "Student",
      "text": "Professor abhi office mein hain?"
    }
  ],
  "source_utterance": {
    "turn_id": 2,
    "speaker_id": "B",
    "speaker_role": "Office assistant",
    "text": "Haan, lekin aap thodi der baad miliye."
  },
  "literal_gloss": "Yes, but meet them after some time.",
  "listener_role": "Student",
  "relationship": "Institutional",
  "relative_status": "Neutral",
  "familiarity": "Low",
  "primary_phenomenon": "POLITENESS",
  "secondary_phenomena": [
    "FORMALITY"
  ],
  "speech_act": "SUGGESTION",
  "politeness_level": "RESPECTFUL",
  "formality_level": "FORMAL",
  "stance": "DEFERENTIAL",
  "emotion": "NEUTRAL",
  "indirectness": "MODERATELY_INDIRECT",
  "code_switch_function": null,
  "context_required": true,
  "minimum_context_window": 1,
  "relevant_context_turns": [
    1
  ],
  "preservation_requirement": "The translation must remain respectful and must not sound like a direct command.",
  "reference_translations": [
    "Yes, but please meet them a little later."
  ],
  "acceptable_variants": [
    "Yes, but could you meet them a little later?"
  ],
  "contrastive_translation": "Yes, meet them later.",
  "contrastive_error": "The translation changes a respectful suggestion into a direct instruction.",
  "contrastive_error_category": "POLITENESS_ERROR",
  "severity": "MAJOR",
  "annotator_notes": ""
}
```

---

## 8. Required Metadata Fields

### Identity and Provenance

```text
item_id
language
language_variety
translation_direction
source_type
source_reference
license
```

### Dialogue Structure

```text
context
source_utterance
speaker_id
speaker_role
listener_role
relationship
relative_status
familiarity
```

### Pragmatic Labels

```text
primary_phenomenon
secondary_phenomena
speech_act
politeness_level
formality_level
stance
emotion
indirectness
code_switch_function
```

### Context Labels

```text
context_required
minimum_context_window
relevant_context_turns
```

### Translation Labels

```text
literal_gloss
preservation_requirement
reference_translations
acceptable_variants
contrastive_translation
contrastive_error
contrastive_error_category
severity
```

### Annotation Metadata

```text
annotator_ids
adjudicator_id
agreement_status
annotation_version
annotator_notes
```

---

## 9. Annotation Workflow

## 9.1 Stage 1: Item Creation

The item creator provides:

- context,
- source utterance,
- literal gloss,
- intended pragmatic interpretation,
- provisional labels,
- reference translation,
- contrastive translation.

---

## 9.2 Stage 2: Independent Validation

At least two native speakers independently judge:

1. whether the source dialogue is natural,
2. whether the intended interpretation is plausible,
3. whether the reference preserves the pragmatic meaning,
4. whether the contrastive translation is pragmatically wrong,
5. whether the contrastive translation remains semantically close,
6. whether the assigned labels are correct.

---

## 9.3 Stage 3: Agreement Measurement

Recommended statistics:

```text
Cohen's kappa
Krippendorff's alpha
percentage agreement
```

Use the statistic appropriate to the number of annotators and label type.

---

## 9.4 Stage 4: Adjudication

A third annotator or project lead resolves disagreements.

The adjudication record should include:

```text
original labels
annotator disagreement
final decision
reason for decision
```

---

## 9.5 Stage 5: Item Acceptance

An item is accepted only if:

- the dialogue is natural,
- the pragmatic interpretation is sufficiently clear,
- the reference is acceptable,
- the contrastive negative isolates the intended error,
- the item does not depend on undocumented regional assumptions,
- the source can be legally included.

---

## 10. Human Evaluation Protocol

Human evaluators should see:

- dialogue context,
- source utterance,
- candidate translation,
- optional literal gloss for non-source-language evaluators.

Native-speaker evaluation should remain primary.

### Evaluation Questions

Rate each dimension from 0 to 3.

```text
3 = fully preserved
2 = mostly preserved
1 = partially preserved
0 = not preserved
```

Questions:

1. Is the translation semantically correct?
2. Is the speech act preserved?
3. Is politeness preserved?
4. Is formality preserved?
5. Is stance preserved?
6. Is emotional tone preserved?
7. Is indirectness preserved?
8. Is the social relationship preserved?
9. Is code-switching function preserved?
10. Is the translation natural?

Additional labels:

```text
UNCERTAIN
MULTIPLE_VALID_INTERPRETATIONS
NOT_APPLICABLE
```

---

## 11. Contrastive Negative Construction

A contrastive negative should satisfy all of the following.

### Semantic Constraint

It must preserve most of the propositional meaning.

### Grammaticality Constraint

It must remain grammatical and natural.

### Isolation Constraint

It should appear plausible when read without the relevant context.

### Pragmatic Failure Constraint

It should fail under the supplied dialogue context.

### Minimality Constraint

It should differ from the correct translation only as much as necessary.

### Category Constraint

It should target one primary pragmatic category.

### Validation Constraint

At least two native speakers should confirm the intended difference.

---

## 12. Benchmark Splits

Recommended split strategy:

```text
train or development: 60 percent
validation: 20 percent
test: 20 percent
```

If the benchmark is evaluation-only, use:

```text
development: 30 percent
test: 70 percent
```

### Split Constraints

Avoid placing closely related minimal pairs across different splits.

Group together:

- paraphrases,
- same dialogue source,
- same template,
- same elicitation prompt,
- same named entities,
- same source scene.

This prevents leakage.

---

## 13. Balance Requirements

The benchmark should be balanced across:

- pragmatic categories,
- source types,
- context lengths,
- speaker relationships,
- sentence lengths,
- language varieties,
- code-mixed and monolingual items,
- easy and difficult examples.

Suggested pilot distribution:

| Category | Items |
|---|---:|
| Politeness and formality | 15 |
| Indirect requests and refusals | 15 |
| Stance and emotion | 10 |
| Code-switching | 10 |

For a 40-item pilot, reduce proportionally.

---

## 14. Baseline Translation Conditions

## 14.1 Sentence-Only

```text
Translate the following utterance into English:

[source utterance]
```

## 14.2 Context-Aware

```text
Translate the final utterance into English while considering the dialogue context.

Context:
[previous turns]

Utterance:
[current turn]
```

## 14.3 Speaker-Aware

```text
Translate the final utterance into English.

Speaker role:
[speaker role]

Listener role:
[listener role]

Relationship:
[relationship]

Preserve the social relationship and level of respect.
```

## 14.4 Pragmatics-Aware

```text
Translate the final utterance while preserving:

Speech act:
[speech act]

Politeness:
[politeness label]

Formality:
[formality label]

Stance:
[stance label]

Indirectness:
[indirectness label]
```

## 14.5 Full Context Condition

```text
dialogue context
+
speaker metadata
+
pragmatic preservation instructions
```

---

## 15. Translation Systems to Evaluate

Possible systems:

### Indian-Language MT

- IndicTrans2
- other open Indic models
- language-specific systems

### Multilingual MT

- NLLB
- M2M100
- mBART-based systems

### Multilingual LLMs

- selected instruction-tuned multilingual LLMs
- commercial LLM APIs where permitted
- open-source LLM baselines

For every run, record:

```text
model_name
model_version
access_date
prompt
temperature
top_p
beam_size
max_tokens
context_condition
random_seed
```

---

## 16. Automatic Evaluation

## 16.1 Semantic Metrics

Recommended baseline metrics:

```text
BLEU
chrF
COMET
BERTScore
```

These should not be treated as sufficient evidence of pragmatic preservation.

---

## 16.2 Rule-Based Checks

Possible checks:

- honorific retention,
- pronoun level,
- politeness markers,
- verb agreement,
- discourse particles,
- code-switched token retention.

Rules should only be used where they have been validated for the language variety.

---

## 16.3 Contrastive Accuracy

For each item:

```text
accuracy = 1 if correct candidate is preferred
accuracy = 0 otherwise
```

Report:

- overall accuracy,
- accuracy by phenomenon,
- accuracy by context length,
- accuracy by model,
- accuracy by source type.

---

## 16.4 LLM-Based Evaluation

Use structured prompts that ask the evaluator to identify:

- semantic errors,
- politeness errors,
- formality errors,
- speech-act errors,
- stance errors,
- indirectness errors,
- code-switching errors.

The LLM should produce:

```json
{
  "semantic_score": 0,
  "pragmatic_score": 0,
  "error_categories": [],
  "severity": "",
  "explanation": ""
}
```

LLM judgments must be compared against human judgments before use as a benchmark metric.

---

## 17. Main Benchmark Metrics

### Translation Quality

```text
semantic adequacy
naturalness
reference metric score
```

### Pragmatic Quality

```text
pragmatic preservation score
phenomenon-specific score
contrastive accuracy
severity-weighted error rate
```

### Context Benefit

```text
context gain =
context-aware score
-
sentence-only score
```

### Speaker-Metadata Benefit

```text
role gain =
speaker-aware score
-
context-only score
```

### Instruction Benefit

```text
instruction gain =
pragmatics-aware score
-
context-aware score
```

### Metric Reliability

```text
correlation with human judgments
classification accuracy
macro F1
agreement score
```

---

## 18. Severity-Weighted Error Score

A severity-weighted pragmatic error score may be defined as:

```text
MINOR = 1
MAJOR = 5
CRITICAL = 10
```

For a system:

```text
severity_weighted_error =
sum(error_weight)
/
number_of_items
```

This score should be reported alongside raw error counts.

---

## 19. Pilot Study Plan

### Step 1

Create 30 to 50 items.

### Step 2

Use two independent native-speaker annotators.

### Step 3

Measure agreement.

### Step 4

Run at least two translation systems.

### Step 5

Evaluate sentence-only and context-aware conditions.

### Step 6

Check whether the contrastive negatives are valid.

### Step 7

Identify categories with:

- low agreement,
- unclear labels,
- weak system differentiation,
- excessive regional dependence.

### Step 8

Revise the schema before full data collection.

---

## 20. Pilot Acceptance Criteria

Proceed to full benchmark construction if:

1. annotators can distinguish semantic and pragmatic correctness,
2. agreement is acceptable,
3. contrastive negatives remain semantically close,
4. at least some systems show measurable pragmatic failures,
5. context improves at least a subset of items,
6. the selected categories are sufficiently distinct.

Revise the pilot if:

- category overlap is high,
- annotators disagree consistently,
- context is unnecessary for most items,
- negatives introduce semantic errors,
- examples sound artificial.

---

## 21. Full Benchmark Construction Plan

### Phase 1: Pilot

```text
30 to 50 items
```

### Phase 2: Schema Revision

- revise labels,
- update guidelines,
- remove weak categories,
- add missing metadata.

### Phase 3: Main Collection

```text
300 to 500 items
```

### Phase 4: Independent Annotation

- at least two annotators per item,
- third-person adjudication for disagreements.

### Phase 5: Baseline Evaluation

- sentence-only,
- context-aware,
- role-aware,
- pragmatics-aware.

### Phase 6: Metric Evaluation

- semantic metrics,
- contrastive accuracy,
- rule-based checks,
- LLM judge,
- human correlation.

### Phase 7: Release Preparation

- dataset card,
- annotation guidelines,
- benchmark script,
- baseline outputs,
- licensing documentation.

---

## 22. Required Release Files

```text
benchmark.jsonl
development.jsonl
test.jsonl
item_schema.json
annotation_guidelines.md
label_definitions.md
severity_guidelines.md
dataset_card.md
baseline_outputs.jsonl
baseline_results.csv
human_scores.csv
agreement_report.md
metric_correlation_report.md
error_analysis.md
README.md
```

---

## 23. Ethics and Data Governance

The benchmark should follow these principles:

1. Use only data with appropriate licensing.
2. Do not include private conversations.
3. Remove personally identifying information.
4. Document dialect and regional limitations.
5. Avoid presenting one interpretation as universal.
6. Preserve annotator disagreement where relevant.
7. Avoid harmful stereotypes in elicited examples.
8. Document potentially offensive or sensitive content.
9. Compensate annotators fairly where applicable.
10. Clearly state that pragmatic judgments are community-dependent.

---

## 24. Known Limitations

The first benchmark release will likely be limited by:

- one primary language pair,
- a small annotator pool,
- regional variation,
- subjective interpretation,
- limited natural dialogue data,
- imperfect automatic metrics,
- possible English-centric reference translations,
- limited coverage of humor and sarcasm,
- difficulty validating code-switching functions,
- reliance on short context windows.

These limitations should be reported explicitly.

---

## 25. Success Criteria

The benchmark is successful if it produces:

1. a clear pragmatic annotation schema,
2. validated context-sensitive items,
3. acceptable inter-annotator agreement,
4. contrastive examples that isolate pragmatic failures,
5. measurable differences between translation systems,
6. evidence about the value of dialogue context,
7. evidence about the value of speaker metadata,
8. comparison between human and automatic evaluation,
9. reproducible baseline scripts and prompts,
10. a dataset that can support later intervention experiments.

---

## 26. Final Benchmark Principle

The benchmark should evaluate not only whether a translation communicates the same factual content, but whether a target-language listener would understand the speaker's intention, attitude, level of respect, and social relationship in the intended way.
