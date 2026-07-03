# Week 1 Summary

## Project Title

**Pragmatics-Preserving Machine Translation for Indian Dialogue**

## 1. What I Set Out to Do This Week

My goal for Week 1 was to turn my broad idea about pragmatic failure in machine translation into a clearly defined and testable research project.

I focused on four main tasks:

1. defining what I mean by pragmatic failure,
2. reviewing the selected literature,
3. narrowing the research scope,
4. designing the first version of the benchmark.

By the end of the week, I had moved from a general research direction to a concrete benchmark-oriented plan.

---

## 2. My Final Research Direction

I decided to study cases where a machine translation system preserves the literal or propositional content of an utterance but changes its intended social or communicative meaning.

I am using the following working definition:

> Pragmatic failure in machine translation occurs when a translation preserves the basic semantic content of an utterance but fails to preserve its intended social or communicative meaning in context.

I chose Indian conversational dialogue as the setting because social meaning is often expressed through:

- pronoun choice,
- honorifics,
- verb forms,
- indirect requests and refusals,
- stance,
- emotion,
- speaker relationships,
- code-switching.

I also clarified that my main contribution will be a benchmark and evaluation framework, not a new translation model.

---

## 3. The Core Problem I Am Addressing

Most machine translation systems are evaluated using sentence-level semantic metrics.

These metrics are useful for checking whether a translation is lexically or semantically similar to a reference, but they may miss whether the translation changes:

- politeness,
- formality,
- speech act,
- indirectness,
- stance,
- emotion,
- social distance,
- code-switching function.

I therefore defined the research problem as:

> How can pragmatic failures in Indian dialogue translation be systematically identified, annotated, and evaluated?

---

## 4. My Primary Research Question

I finalized the following primary research question:

> To what extent do current machine translation systems preserve the intended pragmatic and social meaning of Indian conversational dialogue?

I plan to investigate this by comparing:

- sentence-only translation,
- context-aware translation,
- speaker-role-aware translation,
- pragmatics-aware translation.

---

## 5. The Initial Scope I Finalized

### Language Direction

For the first version of the project, I decided to begin with:

```text
Hindi or Hinglish to English
```

I kept the following as a possible second-stage extension:

```text
Telugu to English
```

I decided not to begin with multiple language pairs because that would make annotation and evaluation much harder to control.

### Pilot Size

I set the pilot size at:

```text
30 to 50 items
```

### Full Benchmark Size

I set the first full benchmark target at:

```text
300 to 500 items
```

### Context Window

I decided that each item may include:

```text
One to three previous dialogue turns
```

I also decided that every item should record whether context is:

```text
not required
helpful
required
```

### Initial Pragmatic Categories

I selected the following three primary categories:

1. Politeness and formality
2. Indirect requests and refusals
3. Stance and emotion

I kept the following as an optional fourth category:

4. Discourse-motivated code-switching

---

## 6. Papers I Reviewed

I completed notes for the following seven papers.

### 1. Controlling Politeness in Neural Machine Translation via Side Constraints

This paper showed me that politeness can be represented as an explicit control variable using source-side tags.

The main idea I took from it was:

> Socially meaningful translation properties can be modelled separately from general translation quality.

The main reusable structure is:

```text
source utterance + politeness label → controlled translation
```

---

### 2. A Study of Style in Machine Translation: Controlling the Formality of Machine Translation Output

This paper treated formality as a measurable stylistic dimension and used formality scoring to rerank translation candidates.

The main lesson I took from it was:

> Formality should be evaluated separately from semantic adequacy.

The reusable approach is:

```text
generate candidates
→ score semantic quality
→ score formality
→ rerank
```

---

### 3. Controlling Neural Machine Translation Formality with Synthetic Supervision

This paper showed how synthetic style labels can be used when bilingual data does not contain explicit formality annotations.

The main lesson I took from it was:

> Pragmatic supervision can be synthesized, but synthetic labels must be validated carefully.

The ideas I want to reuse later are:

- source and target style tags,
- separate meaning and formality evaluation,
- pairwise human comparison,
- synthetic pragmatic labels as a later experiment.

---

### 4. Evaluating Discourse Phenomena in Neural Machine Translation

This paper introduced hand-crafted contrastive test sets for context-dependent translation.

The main lesson I took from it was:

> Standard metrics are not sufficient for discourse-sensitive evaluation.

The benchmark structure I want to reuse is:

```text
dialogue context
source utterance
correct translation
minimally incorrect translation
```

---

### 5. Context-Aware Monolingual Repair for Neural Machine Translation

This paper introduced a separate repair model that corrects contextually inconsistent sentence-level translations.

The main lesson I took from it was:

> A second-stage repair system can improve contextual consistency even when the original translation system is fixed.

The reusable structure is:

```text
sentence-level translation
→ context-aware pragmatic repair
```

I decided that this is better suited as a later intervention rather than the main contribution of the first stage.

---

### 6. When a Good Translation Is Wrong in Context

This paper identified cases where translations are acceptable in isolation but incorrect when read in context.

The main lesson I took from it was:

> Context-sensitive failures should first be discovered empirically and then converted into targeted benchmark items.

The research pipeline I want to reuse is:

1. judge translations in isolation,
2. judge the same translations in context,
3. identify the failure type,
4. create contrastive examples,
5. evaluate context-aware systems.

---

### 7. Assessing the Role of Context in Chat Translation Evaluation

This paper studied whether adding conversational context improves automatic machine translation evaluation.

The main lesson I took from it was:

> Context is useful only under certain conditions and can hurt when it is irrelevant or noisy.

The decisions I took from this paper were:

- annotate whether context is required,
- test multiple context windows,
- compare reference-based and reference-free evaluation,
- validate LLM judges against human judgments,
- analyse short and ambiguous utterances separately.

---

## 7. What I Learned from the Literature as a Whole

### 7.1 Pragmatic Properties Can Be Explicitly Represented

The literature showed me that politeness and formality can be represented using:

- categorical labels,
- continuous scores,
- style tags,
- reranking features.

### 7.2 Context Can Be Necessary

I found that some translations cannot be evaluated correctly without:

- previous source turns,
- previous target translations,
- speaker information,
- social relationship information.

### 7.3 BLEU Is Not Enough

The papers showed that two systems can have similar BLEU scores but very different context-sensitive performance.

A valid stylistic rewrite can also receive a lower BLEU score than an inappropriate but reference-matching translation.

### 7.4 Human Evaluation Is Necessary

I concluded that pragmatic judgments are:

- context-sensitive,
- culturally grounded,
- sometimes ambiguous,
- not fully captured by existing metrics.

### 7.5 Contrastive Evaluation Is a Strong Fit

I decided that contrastive evaluation is especially useful because it can isolate one pragmatic difference while keeping the semantic content mostly constant.

---

## 8. The Research Gap I Identified

The existing work separately covers:

- politeness control,
- formality control,
- discourse context,
- contextual consistency,
- chat translation metrics,
- contrastive evaluation.

However, I did not find a benchmark that combines all of the following:

1. Indian or code-mixed dialogue,
2. explicit conversational context,
3. multiple pragmatic categories,
4. speaker-role and relationship metadata,
5. native-speaker social interpretation,
6. contrastive pragmatic errors,
7. comparison of human and automatic evaluation.

I decided that this combination will be the main gap my project targets.

---

## 9. Benchmark Design Decisions I Made

### Item Types

I decided that the benchmark should combine:

```text
naturally occurring dialogue
native-speaker elicitation
minimal pairs
```

### Required Item Components

I decided that each item should include:

```text
item ID
language
dialogue context
source utterance
speaker role
listener role
relationship
primary pragmatic phenomenon
secondary phenomena
speech act
politeness level
formality level
stance
emotion
indirectness
code-switching function
context requirement
preservation requirement
reference translation
contrastive translation
error explanation
severity
```

### Contrastive Negative Requirements

I decided that a valid contrastive negative must:

1. preserve most propositional content,
2. remain grammatical,
3. remain plausible in isolation,
4. fail in the supplied context,
5. target one primary pragmatic feature,
6. avoid unrelated semantic errors,
7. be validated by native speakers.

---

## 10. Annotation Decisions I Made

### Core Evaluation Dimensions

I decided that every translation should be judged on:

```text
semantic adequacy
speech-act preservation
politeness preservation
formality preservation
stance preservation
emotion preservation
indirectness preservation
code-switching preservation
relationship appropriateness
naturalness
```

### Rating Scale

I selected the following scale:

```text
3 = fully preserved
2 = mostly preserved
1 = partially preserved
0 = not preserved
```

I also decided to include:

```text
UNCERTAIN
MULTIPLE_VALID_INTERPRETATIONS
NOT_APPLICABLE
```

### Annotation Process

I defined the following annotation process:

1. create annotation guidelines,
2. run a pilot with two native-speaker annotators,
3. measure agreement,
4. revise unclear categories,
5. adjudicate disagreements,
6. retain uncertainty information.

---

## 11. Baseline Conditions I Plan to Test

### Condition A: Sentence-Only Translation

The model receives only the current utterance.

### Condition B: Context-Aware Translation

The model receives previous dialogue turns.

### Condition C: Speaker-Aware Translation

The model receives speaker roles and relationship information.

### Condition D: Pragmatics-Aware Translation

The model receives explicit preservation labels or instructions.

### Condition E: Full Condition

The model receives:

```text
dialogue context
+
speaker metadata
+
pragmatic preservation instructions
```

---

## 12. Evaluation Framework I Finalized

I decided that the benchmark should combine multiple evaluation methods.

### Semantic Metrics

Possible baselines include:

```text
BLEU
chrF
COMET
BERTScore
```

### Rule-Based Checks

Possible checks include:

- pronoun level,
- honorific retention,
- politeness markers,
- verb agreement,
- code-switched token retention.

### Contrastive Evaluation

The system should prefer the pragmatically appropriate translation over the minimally incorrect one.

### LLM-Based Evaluation

An LLM judge may classify:

- semantic errors,
- politeness errors,
- formality errors,
- speech-act errors,
- stance errors,
- indirectness errors,
- code-switching errors.

### Human Evaluation

I decided that native-speaker judgments will remain the primary reference.

---

## 13. Deliverables I Completed This Week

I completed or finalized the following project documents:

```text
research_scope.md
research_questions.md
benchmark_blueprint.md
week_1_summary.md
```

I also completed the literature notes folder containing:

```text
README.md
paper_reading_template.md
paper_groups.md
sennrich_2016.md
niu_2017.md
niu_carpuat_2020.md
bawden_2018.md
voita_context_2019.md
voita_docrepair_2019.md
agrawal_2024.md
cross_paper_synthesis.md
research_takeaways.md
```

---

## 14. Decisions I Finalized This Week

### Research Contribution

```text
Benchmark and evaluation framework
```

### Initial Language Strategy

```text
Begin with one Indian-language or code-mixed setting
```

### Initial Benchmark Size

```text
Pilot: 30 to 50 items
Full benchmark: 300 to 500 items
```

### Initial Context Window

```text
One to three previous turns
```

### Initial Categories

```text
Politeness and formality
Indirect requests and refusals
Stance and emotion
```

### Main Evaluation Principle

```text
Semantic correctness and pragmatic preservation must be evaluated separately.
```

### Main Benchmark Format

```text
Open-ended translation
+
contrastive evaluation
+
human judgment
```

---

## 15. Open Questions I Still Need to Resolve

### Language Selection

- Should I use Hindi, Hinglish, or both in the first benchmark?
- Is Telugu feasible with the available annotator pool?

### Annotation

- Should politeness use three, four, or more levels?
- Should stance and emotion remain separate in the pilot?
- Can annotators reliably distinguish formality from politeness?
- How should I represent multiple valid interpretations?

### Context

- Is one previous turn sufficient for most examples?
- Should I include target-side context?
- Should speaker-role metadata be treated as context or as a separate condition?

### Code-Switching

- Can I find enough examples where the switch has a clear pragmatic function?
- How should I score code-switching preservation without rewarding unnecessary copying?

### Evaluation

- Which automatic metric is reliable for the selected language pair?
- How can I evaluate black-box systems contrastively if they do not expose likelihood scores?
- Which LLM judge is suitable for multilingual pragmatic evaluation?

---

## 16. Risks I Identified

### Scope Expansion

The project may become too broad if I include too many languages and phenomena.

### Annotation Subjectivity

Pragmatic interpretation may vary across:

- region,
- dialect,
- age,
- social background,
- individual preference.

### Artificial Examples

Elicited dialogue may sound unnatural.

### English-Centric Design

Starting from English may remove the pragmatic distinctions I am trying to study.

### Weak Contrastive Negatives

A negative translation may accidentally introduce semantic errors.

### Metric Overconfidence

Automatic metrics or LLM judges may appear reliable while missing subtle social errors.

---

## 17. What I Will Do in Week 2

My next step is to move from planning into pilot dataset construction.

### Priority 1: Finalize Language Selection

I will choose the first language setting based on:

- annotator availability,
- data availability,
- baseline system support.

### Priority 2: Create Annotation Guidelines

I will define:

- category descriptions,
- label boundaries,
- positive examples,
- negative examples,
- ambiguity rules,
- severity levels.

### Priority 3: Create Pilot Items

I will build 30 to 50 examples with balanced category coverage.

### Priority 4: Validate Contrastive Negatives

I will check that each negative:

- remains semantically close,
- isolates one pragmatic error,
- is natural,
- is contextually inappropriate.

### Priority 5: Run Initial Translation Baselines

I will compare:

```text
sentence-only
context-aware
speaker-aware
pragmatics-aware
```

### Priority 6: Conduct Pilot Annotation

I will use at least two native speakers and measure agreement.

---

## 18. End-of-Week Status

At the end of Week 1, I now have:

- a clear research problem,
- a focused initial scope,
- defined research questions,
- a literature-backed benchmark methodology,
- a preliminary annotation structure,
- a benchmark blueprint,
- a clear set of next steps.

I am now ready to move from planning into pilot dataset construction.

---

## 19. Final Week 1 Statement

> This week, I finalized a context-sensitive benchmark direction for evaluating whether machine translation systems preserve the pragmatic and social meaning of Indian conversational dialogue. I narrowed the first version to a small number of clearly defined phenomena, designed a native-speaker annotation approach, and established sentence-level, context-aware, speaker-aware, and pragmatics-aware evaluation conditions. My next step is to build and validate the pilot dataset.
