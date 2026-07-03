# Paper Groups

## Theme 1: Explicit Control of Politeness and Formality

### Sennrich, Haddow, and Birch (2016)

The paper treats politeness as a target-side linguistic feature that can be controlled using a special source token. Its central contribution is the side-constraint method.

### Niu, Martindale, and Carpuat (2017)

The paper treats formality as a continuous stylistic property. It uses a sentence-level formality model to rerank translation hypotheses toward a requested formality level.

### Niu and Carpuat (2020)

The paper moves formality-sensitive translation to a neural multitask setting and generates synthetic formality supervision when bilingual data does not have formality labels.

### Shared Lesson

Pragmatic attributes can be made explicit through control labels or scoring functions. However, all three papers assume that the desired style is known or can be inferred. They primarily control output style rather than evaluate whether a system independently preserved the source speaker's intended social meaning.

---

## Theme 2: Context-Aware Translation and Contextual Consistency

### Bawden et al. (2018)

The paper evaluates whether NMT models use the preceding source or target sentence for coreference, lexical cohesion, and lexical disambiguation.

### Voita, Sennrich, and Titov (2019), Context-Aware Translation

The paper identifies frequent cases where individually acceptable translations become incorrect in context. It constructs large contrastive test sets for deixis, ellipsis, and lexical cohesion.

### Voita, Sennrich, and Titov (2019), DocRepair

The paper proposes a separate post-editing model that repairs contextual inconsistencies using only target-language document data.

### Shared Lesson

A context-aware model cannot be evaluated reliably using only aggregate BLEU. Targeted test sets are needed to determine whether the model uses the relevant context and preserves discourse-level constraints.

---

## Theme 3: Context-Aware Translation Evaluation

### Agrawal et al. (2024)

The paper studies automatic quality metrics rather than translation models. It asks whether existing metrics can evaluate machine-translated chat and whether adding dialogue context improves agreement with human MQM judgments.

### Shared Lesson

Context is not uniformly helpful. It improves evaluation under particular conditions, especially for short, ambiguous segments and reference-free evaluation into non-English languages. Irrelevant or corrupted context can reduce metric quality.

---

## Methodological Relationships

| Methodological Question | Most Relevant Papers |
|---|---|
| Can a style label control MT output? | Sennrich 2016; Niu 2020 |
| Can output formality be represented continuously? | Niu 2017 |
| Can formality supervision be synthesized? | Niu and Carpuat 2020 |
| How should context-sensitive errors be isolated? | Bawden 2018; Voita context 2019 |
| How can a black-box MT system be repaired? | Voita DocRepair 2019 |
| When does context improve metric correlation? | Agrawal 2024 |
| Why is BLEU insufficient? | Niu 2017; Bawden 2018; Voita context 2019; Agrawal 2024 |

---

## Relationship to the Proposed Research

The proposed benchmark combines ideas that are separated across these papers:

1. Explicit pragmatic labels from politeness and formality control.
2. Short dialogue context from discourse-aware MT.
3. Minimally different contrastive candidates from discourse test suites.
4. Human judgments as the main reference.
5. Context-aware automatic evaluation as a secondary signal.
6. Analysis of whether context, role information, and pragmatic instructions improve translation.

The research gap is not simply context-aware MT or formality control. The gap is the systematic evaluation of whether Indian dialogue translation preserves socially interpreted meaning across multiple pragmatic dimensions.
