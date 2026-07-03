# Pragmatics-Preserving Machine Translation for Indian Dialogue

## 1. Research Idea

Machine translation systems are usually evaluated on whether they preserve the literal or semantic meaning of a sentence. However, in real conversations, meaning also depends on factors such as politeness, social relationships, tone, indirectness, emotion, humor, and code-switching.

This project studies **pragmatic failure in machine translation for Indian dialogue**.

A pragmatic failure occurs when a translation preserves the basic content of an utterance but fails to preserve its intended social meaning in context.

For example, a translation may:

* preserve the literal words but remove politeness,
* convert an indirect request into a direct command,
* change teasing into an insult,
* remove sarcasm or emotional tone,
* use the wrong honorific or pronoun,
* remove meaningful code-switching,
* misunderstand a refusal, warning, suggestion, or joke.

The goal of the project is to build a benchmark that measures whether machine translation systems preserve these pragmatic features when translating Indian conversational dialogue.

---

## 2. Problem Definition

Given a dialogue context, a source-language utterance, and its machine-generated translation, determine whether the translation preserves:

1. the propositional meaning of the utterance,
2. the intended speech act,
3. the relationship between the speakers,
4. the politeness and formality level,
5. the speaker's emotion and stance,
6. the degree of directness or indirectness,
7. the discourse function of code-switching.

The central research question is:

> Can current machine translation systems preserve the intended social and pragmatic meaning of Indian-language dialogue, and how can such preservation be measured reliably?

---

## 3. Motivation

Most machine translation benchmarks use isolated sentences and automatic metrics such as BLEU, chrF, COMET, or BERTScore.

These evaluation methods are useful for measuring lexical and semantic similarity, but they may fail to detect socially important translation errors.

For example, two translations may express similar literal content while differing significantly in politeness:

```text
Source meaning:
Could you please sit down?

Pragmatically appropriate translation:
Please sit down.

Pragmatically incorrect translation:
Sit down.
```

The second translation preserves the action being requested but changes the speaker's tone and relationship with the listener.

This problem is especially important for Indian languages because many of them encode social meaning through:

* pronoun selection,
* honorifics,
* verb forms,
* kinship terms,
* discourse particles,
* indirect expressions,
* regional variation,
* code-switching between English and Indian languages.

A translation system that ignores these signals may produce grammatically correct but socially inappropriate dialogue.

---

## 4. Research Objectives

The project has five main objectives.

### Objective 1: Define pragmatic failure for dialogue translation

Develop a practical definition of pragmatic failure that can be consistently applied during dataset annotation and evaluation.

### Objective 2: Build a pragmatics-focused translation benchmark

Create a benchmark containing short Indian-language dialogue snippets where pragmatic meaning is essential for correct translation.

### Objective 3: Evaluate existing translation systems

Test strong machine translation systems and multilingual language models to identify the pragmatic phenomena they handle well and the phenomena they frequently fail to preserve.

### Objective 4: Compare evaluation methods

Compare human judgments with automatic metrics, classifiers, rule-based checks, and LLM-based evaluators.

### Objective 5: Test simple methods for improving pragmatic preservation

Evaluate whether context, speaker information, pragmatic labels, prompting, or reranking can improve translation quality.

---

## 5. Initial Scope

The initial version of the project should remain focused enough to support careful annotation and reliable evaluation.

### Languages

A practical starting point is:

* Hindi-English or Hinglish-English
* Telugu-English

The project may initially focus on one language pair and later expand to a second language.

### Dataset Size

The first benchmark should contain approximately:

* 300 to 800 dialogue items,
* one source utterance per item,
* one to three previous dialogue turns as context.

A smaller, carefully annotated dataset is preferable to a large but inconsistent dataset.

### Pragmatic Categories

The first version should focus on three to five categories.

Recommended initial categories:

1. Politeness and formality
2. Speech acts
3. Indirectness
4. Stance and emotion
5. Code-switching

---

## 6. Pragmatic Phenomena

### 6.1 Politeness and Formality

This category measures whether the translation preserves:

* formal or informal address,
* respectful pronouns,
* honorific expressions,
* deferential verb forms,
* social distance,
* familiarity between speakers.

Possible labels:

```text
FORMAL
INFORMAL
RESPECTFUL
FAMILIAR
DEFERENTIAL
```

Example:

```text
Context:
A student is speaking to a professor.

Source:
Aap kal available honge kya?

Pragmatically appropriate translation:
Would you be available tomorrow?

Pragmatically weaker translation:
Are you free tomorrow?
```

Both translations express similar content, but the second may reduce the level of deference.

---

### 6.2 Speech Acts

This category measures whether the translation preserves the communicative function of an utterance.

Possible speech acts include:

```text
REQUEST
COMMAND
WARNING
SUGGESTION
REFUSAL
APOLOGY
COMPLAINT
TEASING
INSULT
JOKE
INVITATION
```

Example:

```text
Source:
Tum ek baar check kar lete toh accha hota.

Possible intended speech act:
A mild complaint or indirect criticism.

Incorrect interpretation:
A neutral suggestion.
```

---

### 6.3 Stance and Emotion

This category measures whether the speaker's attitude is preserved.

Possible labels:

```text
WARM
CARING
IRRITATED
SARCASTIC
DISMISSIVE
ANGRY
PLAYFUL
SYMPATHETIC
ENTHUSIASTIC
RELUCTANT
```

The literal meaning may remain correct even when the speaker's attitude changes.

---

### 6.4 Indirectness

Indian dialogue frequently uses indirect wording to soften requests, criticism, refusals, or disagreement.

Possible labels:

```text
INDIRECT_REQUEST
INDIRECT_REFUSAL
SOFTENED_CRITICISM
HINT
IMPLIED_WARNING
POLITE_DISAGREEMENT
```

Example:

```text
Source:
Abhi thoda kaam hai.

Literal translation:
I have some work right now.

Possible pragmatic meaning:
I cannot come with you right now.
```

A translation system may preserve the literal statement but fail to preserve the implied refusal.

---

### 6.5 Code-Switching

Code-switching should not automatically be treated as noise.

Speakers may switch languages for:

* emphasis,
* humor,
* intimacy,
* identity,
* authority,
* technical terminology,
* emotional expression,
* sarcasm.

Possible labels:

```text
CODE_SWITCH_EMPHASIS
CODE_SWITCH_HUMOR
CODE_SWITCH_IDENTITY
CODE_SWITCH_INTIMACY
CODE_SWITCH_TECHNICAL
```

Example:

```text
Source:
Bro, seriously, tu ye mat kar.

The English words may add emphasis and emotional intensity.

A fully monolingual translation may preserve the content but lose the original conversational style.
```

---

## 7. Dataset Construction

The benchmark can be created using three complementary methods.

### 7.1 Naturally Occurring Dialogue

Collect short conversational examples from sources such as:

* openly licensed subtitles,
* public conversational datasets,
* social media datasets with suitable licenses,
* dialogue corpora,
* publicly available code-mixed datasets.

Only data with appropriate licensing and privacy conditions should be used.

### 7.2 Native-Speaker Elicitation

Ask native speakers to create short dialogues illustrating specific pragmatic phenomena.

Each contributor may be given a prompt such as:

```text
Write a two-turn dialogue where a younger speaker politely refuses a request from an older speaker without explicitly saying no.
```

This method provides better control over category coverage.

### 7.3 Minimal Pairs

Create pairs of dialogue items where the literal content remains similar but one pragmatic property changes.

Example:

```text
Formal:
Aap zara idhar aa sakte hain?

Informal:
Tum zara idhar aa sakte ho?
```

Minimal pairs are useful because they test whether translation systems respond to small but socially meaningful changes.

---

## 8. Dataset Structure

Each benchmark item should contain fields similar to the following:

```json
{
  "item_id": "HIN_POL_001",
  "language": "Hindi",
  "context": [
    {
      "speaker": "A",
      "text": "Professor abhi office mein hain?"
    }
  ],
  "source_utterance": "Haan, lekin aap thodi der baad miliye.",
  "source_translation_gloss": "Yes, but please meet them after some time.",
  "speaker_role": "Office assistant",
  "listener_role": "Student",
  "relationship": "Institutional",
  "pragmatic_category": [
    "POLITENESS",
    "FORMAL"
  ],
  "speech_act": "SUGGESTION",
  "stance": "RESPECTFUL",
  "indirectness": "MEDIUM",
  "code_switch_function": null,
  "preservation_requirement": "The translation should retain respectful address and should not sound like a command.",
  "reference_translation": "Yes, but please meet them a little later.",
  "contrastive_incorrect_translation": "Yes, meet them later."
}
```

---

## 9. Annotation Schema

Each item should be annotated along several dimensions.

### Core Annotation Fields

| Field                | Description                                           |
| -------------------- | ----------------------------------------------------- |
| Language             | Source language or code-mixed language                |
| Dialogue context     | One to three preceding turns                          |
| Speaker role         | Role of the current speaker                           |
| Listener role        | Role of the listener                                  |
| Relationship         | Formal, informal, familial, professional, unfamiliar  |
| Pragmatic category   | Main phenomenon being tested                          |
| Speech act           | Request, refusal, warning, joke, complaint, etc.      |
| Politeness level     | Informal, neutral, polite, highly respectful          |
| Stance               | Warm, irritated, sarcastic, playful, dismissive, etc. |
| Indirectness         | Direct, moderately indirect, highly indirect          |
| Code-switch function | Emphasis, identity, humor, technical meaning, etc.    |
| Preservation note    | Explanation of what the translation must preserve     |
| Severity             | Minor, major, or critical pragmatic failure           |

### Translation Evaluation Labels

Each translation may be assigned one of the following labels:

```text
PRESERVED
PARTIALLY_PRESERVED
NOT_PRESERVED
UNCERTAIN
```

A more detailed scoring scale may also be used:

```text
3 = Fully preserved
2 = Mostly preserved
1 = Partially preserved
0 = Not preserved
```

---

## 10. Annotation Process

### Step 1: Create annotation guidelines

Prepare a document containing:

* definitions of every category,
* positive and negative examples,
* difficult cases,
* instructions for handling ambiguity,
* severity guidelines.

### Step 2: Conduct a pilot annotation

Select approximately 30 to 50 items and ask at least two native speakers to annotate them independently.

### Step 3: Measure agreement

Calculate inter-annotator agreement using:

* Cohen's kappa for two annotators,
* Fleiss' kappa for multiple annotators,
* Krippendorff's alpha for flexible annotation settings.

### Step 4: Revise the schema

Identify categories with poor agreement and revise:

* definitions,
* labels,
* examples,
* annotation instructions.

### Step 5: Annotate the complete dataset

Each item should ideally be reviewed by at least two annotators. Disagreements should be resolved through discussion or adjudication by a third annotator.

---

## 11. Translation Systems to Evaluate

The benchmark should include several types of systems.

### Indian-Language Machine Translation Systems

* IndicTrans2
* available Indic translation APIs or open-source models
* language-specific translation systems where available

### Multilingual Machine Translation Systems

* NLLB
* M2M100
* mBART-based translation systems

### Large Language Models

Where access permits, evaluate multilingual LLMs using consistent prompts.

Possible prompting conditions:

```text
Sentence-only translation
Context-aware translation
Role-aware translation
Pragmatics-aware translation
```

The exact systems used should be documented with:

* model name,
* model version,
* decoding settings,
* prompt,
* date of access,
* language direction.

---

## 12. Experimental Conditions

Each system can be tested under multiple conditions.

### Condition 1: Sentence-Only Translation

The system receives only the source utterance.

```text
Translate the following sentence into English:
[utterance]
```

### Condition 2: Context-Aware Translation

The system receives the previous dialogue turns and the current utterance.

```text
Translate the final utterance into English while considering the dialogue context.

Context:
[previous turns]

Utterance:
[current turn]
```

### Condition 3: Speaker-Role-Aware Translation

The system receives information about the speakers.

```text
Speaker A is a student.
Speaker B is a professor.
Preserve the level of respect and social relationship in the translation.
```

### Condition 4: Pragmatic-Label-Aware Translation

The system receives an explicit pragmatic constraint.

```text
Translate the sentence while preserving:
Politeness: highly respectful
Speech act: indirect request
Stance: deferential
```

### Condition 5: Reranking

Generate multiple translations and select the one that receives the highest pragmatic-preservation score.

---

## 13. Evaluation Framework

No single metric is likely to capture pragmatic preservation. The evaluation should combine several methods.

### 13.1 Standard Translation Metrics

Use standard metrics as semantic-quality baselines:

* BLEU
* chrF
* COMET
* BERTScore

These metrics should not be treated as the primary measure of pragmatic correctness.

### 13.2 Rule-Based Evaluation

Rule-based checks can identify visible linguistic cues.

Examples include:

* respectful pronoun preservation,
* honorific retention,
* presence of politeness markers,
* retention of English tokens in code-switched text,
* verb-form consistency,
* preservation of discourse particles.

### 13.3 Classifier-Based Evaluation

Where reliable classifiers are available, measure:

* formality,
* politeness,
* sentiment,
* emotion,
* toxicity,
* stance.

The classifier output for the source or reference can be compared with the output for the generated translation.

### 13.4 Contrastive Evaluation

For each source item, provide:

1. a pragmatically appropriate translation,
2. a minimally modified but pragmatically incorrect translation.

The system or evaluator must rank the appropriate translation higher.

Example:

```text
Correct:
Would you mind waiting for a few minutes?

Incorrect:
Wait for a few minutes.
```

This method isolates pragmatic differences while keeping semantic content similar.

### 13.5 Human Evaluation

Native speakers should judge each translation on:

```text
Semantic correctness
Politeness preservation
Speech-act preservation
Stance preservation
Indirectness preservation
Code-switching preservation
Overall pragmatic appropriateness
```

A possible rating scale is:

```text
1 = Completely incorrect
2 = Mostly incorrect
3 = Partially correct
4 = Mostly correct
5 = Fully correct
```

Human evaluation should remain the primary reference because pragmatic interpretation depends strongly on cultural and conversational context.

### 13.6 LLM-Based Evaluation

LLMs may be tested as automatic evaluators using a structured rubric.

However, their scores should be compared against human judgments before they are considered reliable.

The analysis should measure:

* correlation with human scores,
* performance across pragmatic categories,
* systematic evaluator biases,
* sensitivity to subtle minimal-pair differences.

---

## 14. Main Experiments

### Experiment 1: Baseline Evaluation

Evaluate existing translation systems using sentence-only input.

Research question:

> How often do current systems preserve pragmatic meaning without explicit context?

### Experiment 2: Effect of Dialogue Context

Compare sentence-only translation with context-aware translation.

Research question:

> Does access to previous dialogue turns improve pragmatic preservation?

### Experiment 3: Effect of Speaker Information

Provide speaker roles, relationship, age, or relative status.

Research question:

> Does social information improve politeness, honorific, and formality choices?

### Experiment 4: Pragmatic Side Constraints

Provide explicit labels such as:

```text
FORMAL
INDIRECT_REQUEST
PLAYFUL
RESPECTFUL
```

Research question:

> Can simple pragmatic constraints improve translation without retraining the model?

### Experiment 5: Contrastive Evaluation

Test whether systems and automatic evaluators prefer pragmatically correct translations over minimally incorrect alternatives.

Research question:

> Can automatic methods reliably distinguish semantic correctness from pragmatic correctness?

### Experiment 6: Human and Automatic Metric Agreement

Compare human scores with:

* BLEU,
* chrF,
* COMET,
* classifier scores,
* rule-based scores,
* LLM judge scores.

Research question:

> Which automatic evaluation methods best correlate with native-speaker judgments?

### Experiment 7: Error Analysis

Group failures by:

* language,
* phenomenon,
* social relationship,
* system,
* sentence length,
* context requirement,
* code-switching pattern.

Research question:

> Which pragmatic phenomena remain difficult even for strong translation systems?

---

## 15. Expected Contributions

The project is expected to produce the following contributions.

### 15.1 A Working Definition of Pragmatic Failure

A clear operational definition of pragmatic failure for Indian dialogue translation.

### 15.2 A New Benchmark

A manually curated benchmark containing context-sensitive Indian dialogue examples.

### 15.3 A Pragmatic Annotation Schema

A reusable annotation framework for:

* politeness,
* speech acts,
* stance,
* indirectness,
* code-switching.

### 15.4 Evaluation of Existing Systems

A comparison of major Indian-language MT systems, multilingual translation models, and LLM-based translation systems.

### 15.5 Analysis of Evaluation Metrics

Evidence showing which automatic metrics detect pragmatic failures and which fail to align with human judgments.

### 15.6 Pragmatic Error Taxonomy

A structured classification of common pragmatic translation errors.

### 15.7 Improvement Strategies

Results showing whether context, role information, prompting, side constraints, or reranking improve pragmatic preservation.

---

## 16. Research Questions

The project will investigate the following research questions.

### RQ1

How frequently do current machine translation systems preserve literal meaning while changing pragmatic meaning?

### RQ2

Which pragmatic categories are most difficult for Indian-language translation systems?

### RQ3

How much does dialogue context improve pragmatic preservation?

### RQ4

Does speaker-role and relationship information improve honorific, pronoun, and formality choices?

### RQ5

Can contrastive examples reliably measure pragmatic translation quality?

### RQ6

How well do automatic metrics correlate with native-speaker judgments of pragmatic preservation?

### RQ7

Can simple interventions such as pragmatic prompting, side constraints, or reranking reduce pragmatic failure?

---

## 17. Hypotheses

### H1

Sentence-level translation systems will perform worse than context-aware systems on indirectness, honorifics, and ambiguous speech acts.

### H2

Standard semantic metrics will assign similar scores to pragmatically correct and pragmatically incorrect translations.

### H3

Speaker-role information will improve politeness and formality preservation.

### H4

Code-switching will frequently be normalized or removed even when it performs a meaningful discourse function.

### H5

Human evaluators will identify pragmatic differences that automated metrics and LLM judges fail to detect consistently.

### H6

Minimal-pair and contrastive evaluation will reveal pragmatic failures more clearly than aggregate corpus-level translation metrics.

---

## 18. Proposed Timeline

## Phase 1: Literature Review and Scope Definition

### Week 1

* Finalize the definition of pragmatic failure.
* Review foundational work on cross-cultural pragmatic failure.
* Study politeness and formality control in machine translation.
* Review context-aware and dialogue-level MT evaluation.
* Review Indian-language and code-mixed translation datasets.
* Select the initial language pair.
* Select three to five pragmatic categories.

### Deliverables

```text
literature_review.md
project_scope.md
research_questions.md
initial_bibliography.bib
```

---

## Phase 2: Annotation Framework

### Week 2

* Define annotation categories.
* Create label descriptions.
* Define severity levels.
* Create example items.
* Design the dataset schema.
* Write the first version of the annotation guidelines.

### Deliverables

```text
annotation_schema.md
annotation_guidelines.md
dataset_schema.json
examples.jsonl
```

---

## Phase 3: Pilot Dataset

### Week 3

* Collect or create 30 to 50 dialogue examples.
* Ensure balanced coverage across categories.
* Create reference translations.
* Create contrastive incorrect translations.
* Ask at least two native speakers to annotate the pilot.
* Record disagreements and difficult cases.

### Deliverables

```text
pilot_dataset.jsonl
pilot_annotations.csv
annotation_issues.md
```

---

## Phase 4: Schema Revision and Data Collection

### Week 4

* Calculate inter-annotator agreement.
* Revise ambiguous labels.
* Improve annotation guidelines.
* Begin collecting the complete benchmark.
* Create data validation scripts.
* Remove duplicate and low-quality examples.

### Deliverables

```text
annotation_guidelines_v2.md
agreement_report.md
data_validation.py
dataset_v1.jsonl
```

---

## Phase 5: Benchmark Completion

### Weeks 5 and 6

* Expand the benchmark to approximately 300 to 800 items.
* Balance the dataset by phenomenon.
* Complete reference translations.
* Create contrastive negative translations.
* Conduct annotation and adjudication.
* Create train, development, and test splits if needed.

### Deliverables

```text
benchmark.jsonl
benchmark_metadata.json
dataset_statistics.md
test_split.jsonl
```

---

## Phase 6: Baseline Translation Experiments

### Week 7

* Run IndicTrans2.
* Run one or more multilingual MT models.
* Run selected LLM-based translation systems where available.
* Store model outputs in a standardized format.
* Record all prompts and system configurations.

### Deliverables

```text
model_outputs/
experiment_config.yaml
baseline_results.csv
```

---

## Phase 7: Evaluation Pipeline

### Week 8

* Implement BLEU and chrF evaluation.
* Add COMET or another learned metric where possible.
* Implement rule-based pragmatic checks.
* Test formality, politeness, sentiment, or stance classifiers.
* Design the human evaluation form.
* Design the LLM evaluator prompt.

### Deliverables

```text
evaluation/
automatic_scores.csv
human_evaluation_form.md
llm_judge_prompt.md
```

---

## Phase 8: Context and Role Experiments

### Week 9

* Compare sentence-only and context-aware translation.
* Add speaker-role information.
* Add relationship information.
* Add pragmatic labels to prompts.
* Test translation reranking.

### Deliverables

```text
context_results.csv
role_aware_results.csv
pragmatic_prompt_results.csv
```

---

## Phase 9: Human Evaluation

### Week 10

* Recruit native-speaker evaluators.
* Conduct blind evaluation.
* Measure evaluator agreement.
* Compare human scores with automatic metrics.
* Identify systematic disagreements.

### Deliverables

```text
human_scores.csv
human_agreement_report.md
metric_correlation_report.md
```

---

## Phase 10: Analysis and Writing

### Weeks 11 and 12

* Conduct category-level error analysis.
* Compare systems and experimental conditions.
* Analyze qualitative examples.
* Document limitations.
* Write the research report or paper.
* Prepare benchmark documentation and repository release.

### Deliverables

```text
error_analysis.md
results.md
paper_draft.pdf
README.md
dataset_card.md
```

## 19. Risks and Limitations

### Annotation Subjectivity

Pragmatic interpretation may vary across speakers, regions, age groups, and social backgrounds.

Mitigation:

* use multiple annotators,
* collect demographic and language-background information where appropriate,
* report disagreement rather than hiding it,
* include adjudication procedures.

### Scope Expansion

Attempting to cover too many languages and phenomena may reduce annotation quality.

Mitigation:

* begin with one or two language pairs,
* focus on three to five pragmatic phenomena,
* expand only after validating the pilot dataset.

### Artificial Data

Elicited examples may not fully represent natural conversation.

Mitigation:

* combine elicited examples with naturally occurring dialogue,
* ask native speakers to review naturalness,
* report the source type for each item.

### Automatic Metric Reliability

Existing metrics may not detect pragmatic failure.

Mitigation:

* treat human evaluation as the main reference,
* use automatic metrics only as complementary signals,
* report correlations separately for each pragmatic category.

### LLM Evaluator Bias

LLM judges may prefer fluent or formal translations even when those translations change the intended tone.

Mitigation:

* compare LLM scores against human judgments,
* use contrastive minimal pairs,
* analyze evaluator errors qualitatively.

### Language and Regional Variation

A sentence may have different pragmatic interpretations across dialects or communities.

Mitigation:

* document dialect and region,
* avoid claiming that one interpretation represents all speakers,
* include multiple native-speaker perspectives.