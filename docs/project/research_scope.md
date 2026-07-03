````markdown
# Research Scope

## Project Title

**Pragmatics-Preserving Machine Translation for Indian Dialogue**

## 1. Project Overview

This project studies pragmatic failure in machine translation for Indian conversational dialogue.

A translation may preserve the literal or propositional meaning of an utterance while changing how the utterance is socially interpreted. It may alter the speaker's politeness, formality, attitude, intention, degree of indirectness, or relationship with the listener.

For example, a system may correctly translate the basic meaning of a sentence but:

- replace respectful language with familiar language,
- turn an indirect request into a command,
- interpret an indirect refusal as a neutral statement,
- remove irritation, warmth, sarcasm, or playfulness,
- convert teasing into an insult,
- remove meaningful code-switching,
- choose language that is inappropriate for the relationship between the speakers.

The project will build a context-sensitive benchmark to identify and measure these failures in Indian-language and code-mixed dialogue.

The primary contribution will be an evaluation benchmark and annotation framework rather than a new large translation model.

---

## 2. Definition of Pragmatic Failure

For this project, pragmatic failure is defined as follows:

> Pragmatic failure in machine translation occurs when a translation preserves the basic semantic content of an utterance but fails to preserve its intended social or communicative meaning in context.

Pragmatic meaning includes:

- the intended speech act,
- politeness,
- formality,
- social distance,
- speaker stance,
- emotional tone,
- directness or indirectness,
- discourse function of code-switching,
- relationship between the speakers.

A translation will therefore be evaluated not only on whether it communicates the same factual content, but also on whether a target-language listener would interpret the speaker's intention and social position in the same way.

---

## 3. Core Research Problem

Most machine translation systems and evaluation benchmarks focus primarily on sentence-level semantic correctness.

However, conversational utterances often depend on information outside the current sentence, including:

- previous dialogue turns,
- speaker identity,
- social role,
- age or status difference,
- familiarity between speakers,
- previous translation choices,
- conversational tone,
- cultural norms.

Standard metrics may assign a high score to a translation that is semantically similar to the reference even when it changes these socially important properties.

The project addresses the following problem:

> How can pragmatic failures in Indian dialogue translation be systematically identified, annotated, and evaluated?

---

## 4. Primary Research Question

> Can current machine translation systems preserve the intended pragmatic and social meaning of Indian conversational dialogue?

---

## 5. Supporting Research Questions

### RQ1

How often do translation systems produce outputs that are semantically acceptable but pragmatically inappropriate?

### RQ2

Which pragmatic phenomena are most difficult for current translation systems?

### RQ3

Does access to previous dialogue turns improve pragmatic preservation?

### RQ4

Does speaker-role and relationship information improve politeness, formality, and speech-act preservation?

### RQ5

Can contrastive evaluation distinguish pragmatically correct translations from semantically similar but socially incorrect translations?

### RQ6

How well do automatic translation metrics agree with native-speaker judgments of pragmatic preservation?

### RQ7

Can explicit pragmatic instructions, control labels, or reranking improve translation quality?

---

## 6. Initial Language Scope

The initial benchmark will focus on one primary Indian-language setting.

Potential starting options are:

1. Hindi or Hinglish to English
2. Telugu to English

The final selection will depend on:

- availability of native-speaker annotators,
- access to suitable dialogue data,
- availability of baseline translation systems,
- feasibility of validating pragmatic interpretations.

The first version should use one main language pair. A second language may be added only after the annotation process has been validated.

### Potential Initial Direction

```text
Hindi or Hinglish to English
````

This direction is suitable for the initial study because it provides access to both monolingual and code-mixed conversational examples and can support analysis of politeness, indirectness, and code-switching.

---

## 7. Initial Pragmatic Categories

The first benchmark will focus on three primary categories.

### 7.1 Politeness and Formality

This category evaluates whether the translation preserves:

* respectful or familiar address,
* honorific usage,
* formal or informal pronouns,
* deferential verb forms,
* social distance,
* institutional or casual register.

Possible labels include:

```text
HIGHLY_RESPECTFUL
POLITE
NEUTRAL
INFORMAL
FAMILIAR
DISRESPECTFUL
```

Politeness and formality will be stored as separate fields because they are related but not identical.

A sentence may be formal without being especially polite, or polite while remaining conversational and informal.

---

### 7.2 Indirect Requests and Refusals

This category evaluates whether the translation preserves implied communicative intent.

Examples include:

* indirect requests,
* indirect refusals,
* softened criticism,
* polite disagreement,
* hints,
* implied warnings.

Example:

```text
Context:
A friend asks the speaker to attend an event.

Source:
Aaj thoda kaam hai.

Literal meaning:
I have some work today.

Pragmatic meaning:
The speaker is indirectly declining the invitation.
```

A literal translation may preserve the words but fail to communicate the refusal.

---

### 7.3 Stance and Emotion

This category evaluates whether the speaker's attitude toward the listener or situation is preserved.

Possible labels include:

```text
WARM
CARING
PLAYFUL
IRRITATED
ANGRY
SARCASTIC
DISMISSIVE
RELUCTANT
SYMPATHETIC
DEFERENTIAL
```

The benchmark will distinguish emotion from stance where possible.

Emotion describes an affective state such as anger or sadness. Stance describes the speaker's position or attitude toward the listener, statement, or situation.

---

## 8. Optional Additional Category

### Code-Switching

Code-switching may be included as a fourth category if sufficient reliable examples are available.

The benchmark will focus only on cases where language mixing has a clear discourse or social function.

Possible functions include:

```text
EMPHASIS
HUMOR
IDENTITY
INTIMACY
AUTHORITY
TECHNICAL_TERMINOLOGY
EMOTIONAL_INTENSITY
SARCASM
```

The project will not treat every English word inside an Indian-language sentence as pragmatically meaningful code-switching.

Annotators must explain why the switch matters in the specific dialogue.

---

## 9. Phenomena Outside the Initial Scope

The first version will not attempt to cover every form of pragmatic meaning.

The following areas are outside the initial benchmark scope unless they emerge naturally during the pilot:

* full sarcasm detection,
* complex humor translation,
* metaphor translation,
* long-document discourse,
* regional dialect translation,
* multimodal dialogue,
* speech prosody,
* gesture and facial-expression interpretation,
* real-time speech translation,
* automatic pragmatic model training from scratch,
* all Indian languages,
* all code-mixed language combinations.

These may be considered in later extensions.

---

## 10. Benchmark Size

### Pilot Dataset

```text
30 to 50 items
```

The pilot will be used to test:

* annotation clarity,
* category overlap,
* annotator agreement,
* contrastive example quality,
* context requirements,
* feasibility of human evaluation.

### Full Benchmark

```text
300 to 500 items
```

The benchmark may later be expanded toward 800 items if annotation quality and project time permit.

A smaller, carefully validated dataset is preferred over a larger but inconsistent dataset.

---

## 11. Dialogue Context

Each benchmark item will contain:

```text
One to three previous dialogue turns
```

The exact amount of context will depend on the item.

Each item will record:

```text
context_required
minimum_context_window
relevant_context_turns
```

Example:

```json
{
  "context_required": true,
  "minimum_context_window": 2,
  "relevant_context_turns": [1, 2]
}
```

The project will not assume that longer context always improves translation or evaluation.

Context may be useful, irrelevant, incomplete, or misleading. This will be tested experimentally.

---

## 12. Dataset Construction Methods

The benchmark will combine three methods.

### 12.1 Naturally Occurring Dialogue

Possible sources include:

* openly licensed subtitle data,
* public conversational corpora,
* existing code-mixed datasets,
* publicly available dialogue resources with appropriate licenses.

All data sources must be documented.

Private conversations and personally identifiable content will not be collected.

---

### 12.2 Native-Speaker Elicitation

Native speakers may be asked to create short dialogues targeting specific pragmatic phenomena.

Example prompt:

```text
Write a two-turn dialogue in which a younger speaker politely refuses a request from an older speaker without explicitly saying no.
```

Elicited examples will be reviewed for naturalness.

---

### 12.3 Minimal Pairs

Minimal pairs will differ in one primary pragmatic feature while keeping propositional content as similar as possible.

Example:

```text
Respectful:
Aap thodi der wait kar sakte hain?

Familiar:
Tum thodi der wait kar sakte ho?
```

Minimal pairs will help isolate the feature being tested.

---

## 13. Benchmark Item Structure

Each item will contain fields similar to the following:

```json
{
  "item_id": "HIN_POL_001",
  "language": "Hindi",
  "source_type": "elicited",
  "context": [
    {
      "turn_id": 1,
      "speaker": "A",
      "text": "Professor abhi office mein hain?"
    }
  ],
  "source_utterance": "Haan, lekin aap thodi der baad miliye.",
  "literal_gloss": "Yes, but meet them after some time.",
  "speaker_role": "Office assistant",
  "listener_role": "Student",
  "relationship": "Institutional",
  "relative_status": "Neutral",
  "primary_phenomenon": "POLITENESS",
  "secondary_phenomena": [
    "FORMALITY"
  ],
  "speech_act": "SUGGESTION",
  "politeness_level": "RESPECTFUL",
  "formality_level": "FORMAL",
  "stance": "DEFERENTIAL",
  "emotion": "NEUTRAL",
  "indirectness": "MEDIUM",
  "code_switch_function": null,
  "context_required": true,
  "minimum_context_window": 1,
  "relevant_context_turns": [
    1
  ],
  "preservation_requirement": "The translation must remain respectful and must not sound like a direct command.",
  "reference_translation": "Yes, but please meet them a little later.",
  "contrastive_translation": "Yes, meet them later.",
  "contrastive_error": "The contrastive version changes a respectful suggestion into a direct instruction."
}
```

---

## 14. Annotation Framework

### Core Annotation Dimensions

| Field                      | Description                                                  |
| -------------------------- | ------------------------------------------------------------ |
| `semantic_adequacy`        | Whether the factual meaning is preserved                     |
| `speech_act`               | Request, refusal, warning, suggestion, complaint, joke, etc. |
| `politeness_level`         | Degree of respect or familiarity                             |
| `formality_level`          | Formal, neutral, informal                                    |
| `stance`                   | Warm, irritated, playful, dismissive, deferential, etc.      |
| `emotion`                  | Anger, concern, reluctance, sympathy, etc.                   |
| `indirectness`             | Direct, moderately indirect, highly indirect                 |
| `code_switch_function`     | Function of language mixing                                  |
| `speaker_role`             | Role of the speaker                                          |
| `listener_role`            | Role of the listener                                         |
| `relationship`             | Familial, professional, friendly, unfamiliar, etc.           |
| `context_required`         | Whether context is necessary for interpretation              |
| `preservation_requirement` | Explanation of what the translation must preserve            |

### Translation Judgment Labels

```text
FULLY_PRESERVED
MOSTLY_PRESERVED
PARTIALLY_PRESERVED
NOT_PRESERVED
UNCERTAIN
MULTIPLE_VALID_INTERPRETATIONS
```

### Numerical Scale

```text
3 = Fully preserved
2 = Mostly preserved
1 = Partially preserved
0 = Not preserved
```

---

## 15. Contrastive Evaluation

Each contrastive item will include:

1. dialogue context,
2. current source utterance,
3. pragmatically appropriate translation,
4. semantically similar but pragmatically incorrect translation,
5. explanation of the failure.

A valid contrastive negative must:

* preserve most literal content,
* remain grammatically natural,
* remain plausible when viewed alone,
* fail when interpreted in the supplied context,
* differ mainly in one pragmatic feature,
* avoid unrelated semantic errors,
* be validated by native speakers.

Example:

```text
Context:
A student is speaking to a professor.

Correct:
Would you be available tomorrow?

Contrastive:
Are you free tomorrow?

Targeted difference:
The contrastive version reduces the original level of formality and deference.
```

---

## 16. Translation Systems

The project will evaluate multiple types of systems.

### Indian-Language Translation Models

Possible systems include:

* IndicTrans2,
* other open Indian-language MT models,
* language-specific models where available.

### Multilingual Translation Models

Possible systems include:

* NLLB,
* M2M100,
* multilingual sequence-to-sequence models.

### Large Language Models

Selected multilingual LLMs may be evaluated using controlled prompts.

All experiments must record:

```text
model name
model version
date accessed
prompt
decoding settings
context condition
language direction
```

---

## 17. Experimental Conditions

### Condition A: Sentence-Only Translation

The system receives only the current source utterance.

```text
Translate the following utterance into English:

[source utterance]
```

### Condition B: Context-Aware Translation

The system receives previous dialogue turns.

```text
Translate the final utterance into English while considering the dialogue context.

Context:
[previous turns]

Utterance:
[current turn]
```

### Condition C: Speaker-Role-Aware Translation

The system receives role and relationship information.

```text
Speaker A is a student.
Speaker B is a professor.
Preserve the level of respect and social distance in the translation.
```

### Condition D: Pragmatics-Aware Translation

The system receives explicit preservation requirements.

```text
Preserve the following properties:

Politeness: respectful
Speech act: indirect request
Stance: deferential
```

### Condition E: Candidate Reranking

The system generates multiple translations. The candidates are reranked using semantic and pragmatic criteria.

---

## 18. Evaluation Framework

No single metric will be treated as sufficient.

### 18.1 Semantic Evaluation

Possible semantic-quality baselines include:

* chrF,
* BLEU,
* COMET,
* BERTScore.

These metrics will be used as supporting measures rather than as the main evidence of pragmatic correctness.

---

### 18.2 Rule-Based Evaluation

Rule-based checks may be used for visible features such as:

* respectful pronoun preservation,
* honorific retention,
* politeness markers,
* verb agreement,
* retained code-switched terms,
* discourse particles.

Rule-based evaluation will only be used where the rule has been validated for the language.

---

### 18.3 Contrastive Evaluation

The system must prefer the pragmatically appropriate translation over the minimally incorrect alternative.

Possible scoring methods include:

* model likelihood,
* forced-choice prompting,
* pairwise LLM judgment,
* human pairwise judgment.

---

### 18.4 LLM-Based Evaluation

An LLM evaluator may receive:

* dialogue context,
* source utterance,
* generated translation,
* pragmatic labels,
* structured evaluation instructions.

The evaluator should identify specific errors rather than provide only one overall score.

LLM evaluation will be validated against native-speaker judgments.

---

### 18.5 Human Evaluation

Human evaluation will be the primary reference.

Native speakers will judge:

1. semantic correctness,
2. speech-act preservation,
3. politeness preservation,
4. formality preservation,
5. stance preservation,
6. emotional-tone preservation,
7. indirectness preservation,
8. code-switching preservation,
9. relationship appropriateness,
10. overall naturalness.

---

## 19. Annotation Procedure

### Step 1: Prepare Guidelines

The annotation guidelines will include:

* category definitions,
* positive examples,
* negative examples,
* ambiguous cases,
* severity definitions,
* instructions for uncertainty.

### Step 2: Pilot Annotation

Two or more native speakers will independently annotate 30 to 50 items.

### Step 3: Measure Agreement

Possible agreement measures include:

* Cohen's kappa,
* Fleiss' kappa,
* Krippendorff's alpha.

### Step 4: Revise the Schema

Categories with low agreement will be:

* redefined,
* merged,
* divided,
* removed from the initial scope.

### Step 5: Adjudication

Disagreements will be resolved through:

* discussion,
* a third annotator,
* documented adjudication notes.

Disagreement will not be hidden. It will be treated as evidence about the ambiguity of the phenomenon.

---

## 20. Main Experiments

### Experiment 1: Baseline Pragmatic Failure Rate

Measure how often sentence-level systems preserve semantics but fail pragmatically.

### Experiment 2: Effect of Context

Compare sentence-only translation with translation using previous turns.

### Experiment 3: Effect of Speaker Information

Measure whether speaker roles and relationships improve socially appropriate translation.

### Experiment 4: Effect of Pragmatic Instructions

Test whether explicit labels improve preservation.

### Experiment 5: Contrastive Evaluation

Measure whether systems and evaluators prefer pragmatically appropriate candidates.

### Experiment 6: Metric and Human Agreement

Compare automatic scores with native-speaker judgments.

### Experiment 7: Error Analysis

Analyse errors by:

* phenomenon,
* language,
* system,
* context length,
* source type,
* speaker relationship,
* sentence length.

---

## 21. Expected Contributions

The project is expected to produce:

### 21.1 Operational Definition

A practical definition of pragmatic failure for Indian dialogue translation.

### 21.2 Pragmatic Error Taxonomy

A structured taxonomy covering the initial selected phenomena.

### 21.3 Annotated Benchmark

A context-sensitive benchmark containing dialogue items, pragmatic labels, references, and contrastive negatives.

### 21.4 Annotation Guidelines

A documented annotation process that can be reused or extended.

### 21.5 Baseline Evaluation

A comparison of existing translation systems under sentence-only and context-aware conditions.

### 21.6 Metric Analysis

Evidence showing which automatic evaluation methods align with native-speaker judgments.

### 21.7 Intervention Results

An analysis of whether context, role information, pragmatic labels, or reranking improve preservation.

---

## 22. Risks and Mitigation

### Risk 1: Annotation Subjectivity

Pragmatic interpretation may vary across annotators.

Mitigation:

* use multiple annotators,
* measure agreement,
* record uncertainty,
* preserve disagreement,
* use adjudication.

### Risk 2: Excessive Scope

Covering many languages and pragmatic categories may reduce quality.

Mitigation:

* begin with one language pair,
* begin with three categories,
* expand only after pilot validation.

### Risk 3: Artificial Examples

Elicited examples may not reflect natural conversation.

Mitigation:

* combine natural, elicited, and minimal-pair examples,
* perform naturalness review,
* record item source.

### Risk 4: English-Centric Framing

Starting from English may flatten Indian-language pragmatic distinctions.

Mitigation:

* prefer Indian-language-original dialogue,
* avoid translating English examples outward as the main data source,
* involve native speakers in item creation.

### Risk 5: Weak Contrastive Negatives

A negative may accidentally change semantic content rather than only pragmatics.

Mitigation:

* require native-speaker validation,
* document the intended difference,
* reject items with unrelated semantic changes.

### Risk 6: Automatic Metric Overconfidence

Metrics or LLM judges may miss subtle pragmatic errors.

Mitigation:

* treat human judgment as primary,
* validate every evaluator against humans,
* report results by category.

### Risk 7: Regional Variation

Interpretation may vary by dialect, region, age, or community.

Mitigation:

* record language background,
* avoid claiming one universal interpretation,
* include multiple native-speaker perspectives.