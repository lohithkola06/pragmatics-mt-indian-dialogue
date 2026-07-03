# Research Takeaways and Implementation Decisions

## 1. Definition to Use

A pragmatic failure occurs when a translation preserves enough literal content to appear semantically acceptable, but changes how the utterance is socially interpreted in context.

This definition should be operationalized through separate labels rather than one broad score.

---

## 2. Annotation Dimensions

Recommended fields:

```text
semantic_adequacy
politeness
formality
speech_act
stance
emotion
indirectness
code_switch_function
speaker_role
listener_role
relationship
context_required
preservation_note
```

Politeness and formality should remain separate.

---

## 3. Benchmark Item Structure

```json
{
  "item_id": "LANG_CATEGORY_001",
  "language": "",
  "context": [],
  "source_utterance": "",
  "speaker_role": "",
  "listener_role": "",
  "relationship": "",
  "primary_phenomenon": "",
  "secondary_phenomena": [],
  "speech_act": "",
  "politeness_level": "",
  "formality_level": "",
  "stance": "",
  "indirectness": "",
  "code_switch_function": null,
  "context_required": true,
  "relevant_context_turns": [],
  "preservation_requirement": "",
  "reference_translation": "",
  "contrastive_translation": "",
  "contrastive_error": ""
}
```

---

## 4. Contrastive Construction Rules

A contrastive negative should:

1. preserve most propositional content,
2. remain grammatical,
3. remain plausible in isolation,
4. fail in the supplied social or dialogue context,
5. differ in one primary pragmatic property,
6. avoid introducing unrelated semantic errors,
7. be validated by at least two native speakers.

Examples of controlled changes:

- respectful pronoun to familiar pronoun,
- indirect refusal to literal statement,
- request to command,
- teasing to insult,
- warm concern to neutral observation,
- meaningful code-switching to flattened monolingual text.

---

## 5. Context Design

Store one to three preceding turns.

For each item, annotate:

```text
context_required = true / false
minimum_context_window = 0 / 1 / 2 / 3
relevant_turn_ids = [...]
context_type = source / target / both / speaker-role
```

Do not assume longer context is always better.

---

## 6. Human Evaluation

Use native speakers as the primary reference.

Recommended questions:

1. Is the translation semantically correct?
2. Does it preserve the intended speech act?
3. Does it preserve politeness and formality?
4. Does it preserve stance and emotion?
5. Does it preserve indirectness?
6. Does it preserve the function of code-switching?
7. Is it appropriate for the relationship between the speakers?
8. Is it natural in the target language?

Recommended scale:

```text
3 = fully preserved
2 = mostly preserved
1 = partially preserved
0 = not preserved
```

Include:

```text
UNCERTAIN
MULTIPLE_VALID_INTERPRETATIONS
```

Measure inter-annotator agreement and keep disagreement data.

---

## 7. Automatic Evaluation

Use automatic signals as supporting evidence.

### Semantic Baselines

- chrF,
- COMET or another learned metric,
- reference-based LLM comparison if necessary.

### Pragmatic Signals

- pronoun and honorific rules,
- formality or politeness classifiers where validated,
- contrastive candidate accuracy,
- structured LLM judgment.

### Required Validation

For every automatic evaluator, report correlation or agreement with human judgments by phenomenon.

---

## 8. Baseline Experiments

### Translation Conditions

```text
A. Source utterance only
B. Source utterance plus previous turns
C. Context plus speaker roles
D. Context plus preservation labels
```

### Evaluation Conditions

```text
A. Standard metric without context
B. Context-aware automatic metric
C. LLM judge without context
D. LLM judge with context
E. Native-speaker human evaluation
```

---

## 9. Pilot Deliverables

The pilot should produce:

```text
pilot_items.jsonl
annotation_guidelines.md
annotator_form.md
pilot_annotations.csv
agreement_report.md
contrastive_validation.md
baseline_outputs/
pilot_results.md
```

---

## 10. Decision Rules After the Pilot

Continue with a category only if:

1. native speakers agree sufficiently,
2. the pragmatic difference is explainable,
3. the contrastive negative is semantically close,
4. at least one tested system exhibits failures,
5. the category is not reducible to a trivial lexical check.

Revise or remove a category if:

- annotators consistently disagree,
- examples require excessive explanation,
- negatives introduce semantic changes,
- the phenomenon is too region-specific for the available annotator pool.

---

## 11. Main Risks

### Over-Broad Scope

Mitigation: begin with three categories and one primary language setting.

### Artificial Examples

Mitigation: mix natural, elicited, and minimal-pair data.

### English-Centric Framing

Mitigation: begin from Indian-language-original dialogue where possible.

### Automatic-Judge Overconfidence

Mitigation: validate against humans and report uncertainty.

### Pragmatic Normalization

Mitigation: distinguish consistency from legitimate speaker variation.

### Multiple Valid Translations

Mitigation: allow multiple references and annotate acceptable variation.

---

## 12. Final Implementation Principle

The benchmark should test not only whether the translation says the same thing, but whether the target-language listener would understand the speaker's intention, relationship, and attitude in the same way.
