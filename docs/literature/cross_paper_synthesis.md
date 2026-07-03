# Cross-Paper Synthesis

## Central Finding

Across the seven papers, the same broad conclusion appears in different forms:

> A translation can be semantically plausible at the sentence level while failing to preserve socially or contextually important meaning.

The politeness and formality papers show that style must be represented explicitly. The context papers show that sentence-level evaluation hides discourse errors. The chat-evaluation paper shows that even automatic metrics need carefully selected context.

---

## What the Literature Already Establishes

### 1. Politeness and Formality Can Be Controlled

Sennrich et al. show that categorical side constraints can control polite versus informal address forms.

Niu et al. show that formality can be represented as a continuous property and used for reranking.

Niu and Carpuat show that synthetic supervision and style tags can improve neural formality control.

### 2. Context Is Required for Some Translation Decisions

Bawden et al. show that previous source and target sentences are necessary for controlled discourse cases.

Voita et al. show that 7 percent of sampled sentence pairs can be individually acceptable yet incorrect together.

DocRepair shows that many contextual inconsistencies can be corrected after sentence-level translation.

### 3. Standard Metrics Are Insufficient

BLEU may remain unchanged while contextual accuracy changes substantially.

BLEU can penalize a legitimate stylistic rewrite or reward an inappropriate reference-matching choice.

Reference-free metrics may benefit from context, but only in certain language directions and item types.

### 4. Human Evaluation Remains Necessary

Formality judgments have moderate disagreement.

Contextual acceptability depends on interpretation.

Automatic metrics and LLM judges must be validated against native-speaker judgments.

---

## Main Methodological Patterns

## Pattern A: Explicit Control

```text
source + attribute label → controlled translation
```

Used for:

- politeness,
- formality.

Potential project use:

- respectful,
- informal,
- indirect refusal,
- playful,
- irritated.

## Pattern B: Candidate Reranking

```text
generate several translations
→ score semantic quality
→ score pragmatic match
→ select best candidate
```

Potential project use:

- compare semantic-only and pragmatic-aware reranking.

## Pattern C: Contrastive Evaluation

```text
context
source
correct candidate
minimally wrong candidate
```

Potential project use:

- primary automatic benchmark format.

## Pattern D: Two-Stage Contextual Refinement

```text
sentence-level translation
→ context-aware correction
```

Potential project use:

- later intervention after benchmark construction.

## Pattern E: Context-Aware Metric

```text
context + source + translation
→ quality or error judgment
```

Potential project use:

- automatic evaluator compared against humans.

---

## Major Gaps Across the Seven Papers

### Phenomenon Gap

The papers cover:

- T-V politeness,
- formality,
- coreference,
- deixis,
- ellipsis,
- lexical cohesion,
- chat-level quality estimation.

They do not jointly cover:

- speech acts,
- indirect requests,
- indirect refusals,
- teasing versus insult,
- sarcasm,
- warmth and care,
- dismissiveness,
- discourse-motivated code-switching.

### Language Gap

The studies focus on:

- English-German,
- French-English,
- English-French,
- English-Russian,
- English-German/French/Portuguese chat.

Indian languages and Indian code-mixed dialogue are absent.

### Social-Context Gap

Most models receive:

- a style label,
- previous text,
- prior translations.

They rarely model:

- relative status,
- age relationship,
- kinship,
- institutional role,
- familiarity,
- community-specific norms.

### Evaluation Gap

Contrastive evaluation is strong but narrow. Human evaluation is richer but expensive. Existing automatic metrics are not specifically trained to detect pragmatic preservation.

---

## Research Positioning

The proposed project should not claim that context-aware MT is new. It should claim that existing work has not sufficiently combined:

1. Indian conversational language.
2. Explicit dialogue context.
3. Multiple pragmatic categories.
4. Native-speaker social interpretation.
5. Contrastive minimally wrong translations.
6. Comparison between automatic and human evaluation.
7. Simple pragmatic interventions.

---

## Recommended Research Questions

### RQ1

How often do current MT systems preserve semantic content while changing pragmatic meaning in Indian dialogue?

### RQ2

Which pragmatic categories are most vulnerable?

### RQ3

How much does dialogue context improve preservation?

### RQ4

Does speaker-role information provide additional benefit beyond raw context?

### RQ5

Can contrastive evaluation reliably detect pragmatic failures?

### RQ6

Which automatic metric or LLM evaluator best agrees with native speakers?

### RQ7

Can labels, prompting, or reranking reduce pragmatic failure?

---

## Recommended Pilot Design

### Scope

- One primary language or code-mixed variety.
- 30 to 50 pilot items.
- Three core phenomena.
- One to three previous turns.
- Two native-speaker annotators plus adjudication.

### Initial Phenomena

1. Politeness and formality.
2. Indirect requests and refusals.
3. Stance and emotion.

Optional fourth:

4. Discourse-motivated code-switching.

### Item Types

- naturally sourced items,
- elicited items,
- minimal pairs.

### Evaluation Conditions

1. Sentence-only translation.
2. Context-aware translation.
3. Context plus speaker roles.
4. Context plus pragmatic preservation instruction.

### Output Judgments

- semantic adequacy,
- pragmatic preservation,
- naturalness,
- overall social appropriateness.

---

## Final Synthesis

The strongest contribution is likely to be the benchmark and evaluation protocol rather than a new translation architecture.

The literature supports a staged project:

1. Discover and define pragmatic failures.
2. Validate an annotation scheme.
3. Build contrastive and generative evaluation items.
4. Benchmark current systems.
5. compare human, metric, and LLM judgments.
6. test simple context and control interventions.
7. consider repair or fine-tuning only after the benchmark is stable.
