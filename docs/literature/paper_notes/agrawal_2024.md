# Assessing the Role of Context in Chat Translation Evaluation

## Citation

Sweta Agrawal, Amin Farajian, Patrick Fernandes, Ricardo Rei, and André F. T. Martins. 2024. *Assessing the Role of Context in Chat Translation Evaluation: Is Context Helpful and Under What Conditions?* Transactions of the Association for Computational Linguistics, volume 12, pages 1250 to 1267.

Source file: `2024.tacl-1.69.pdf`

## One-Sentence Summary

The paper evaluates MT metrics on bilingual customer-support chats and finds that context helps mainly in reference-free, out-of-English evaluation of short and ambiguous turns, while irrelevant or noisy context can hurt.

## Research Problem

Most MT metrics are developed and validated on structured domains such as news. Chat differs because it is:

- short,
- synchronous,
- informal or mixed-register,
- noisy,
- participant-dependent,
- highly contextual.

The paper asks whether existing metrics accurately evaluate chat translation and whether adding conversational history improves correlation with human judgments.

## Main Research Questions

1. How do translation errors in chat differ from errors in news?
2. Which existing metrics correlate best with human MQM judgments on chat?
3. Does conversational context improve sentence-level quality estimation?
4. Which direction, context type, and segment type benefit?
5. Can an LLM-based evaluator use bilingual context effectively?

## Dataset

### Primary Evaluation Data

WMT 2022 Chat Shared Task MQM annotations.

The data contains genuine bilingual customer-support conversations translated by shared-task MT systems.

### Language Directions

Agent messages originate in English:

- English to German,
- English to French,
- English to Portuguese.

Customer messages originate in the other language:

- German to English,
- French to English,
- Portuguese to English.

### Instance Counts

| Direction | Instances |
|---|---:|
| English to German | 2,715 |
| German to English | 2,720 |
| English to French | 1,868 |
| French to English | 1,020 |
| English to Portuguese | 1,318 |
| Portuguese to English | 1,016 |

### Domain Comparison Sample

For English-German, the paper compares:

- 7,120 conversational translation pairs,
- 4,800 news translation pairs.

## Human Evaluation Reference

Professional MQM annotations mark minor, major, and critical errors at the token level.

The turn-level score is:

```text
MQM = -(minor + 5 × major + 10 × critical)
```

Dialogue quality is approximated by averaging turn-level MQM scores.

## Chat Versus News Findings

### Error Frequency

Perfect MQM scores:

```text
News: 46.4 percent
Conversation: 57.8 percent
```

Chat contains fewer detected errors, partly because messages are shorter.

### Error Type

Chat has relatively more issues involving:

- fluency,
- spelling,
- consistency,
- register.

News has relatively more accuracy and mistranslation errors.

This shows that a metric validated on news may not capture the same failure distribution in conversation.

## Metrics Evaluated

### Lexical and Embedding Metrics

- BLEU
- chrF
- BERTScore

### Learned Reference-Based Metrics

- BLEURT
- COMET-22
- XCOMET-XL
- MetricX-23-XL

### Reference-Free Metrics

- COMET-20-QE
- COMETKiwi-22-QE
- XCOMET-QE-XL
- MetricX-23-QE-XL

### Dialogue-Level Metrics

- dialogue BLEU,
- averaged COMET scores,
- SLIDE.

### Meta-Evaluation Measure

Spearman rank correlation with human MQM scores.

The paper reports results for:

- all translations,
- imperfect translations with MQM below zero.

## Context-Aware Metric Design

The authors extend COMET-based models by prepending previous conversational turns before the current source, hypothesis, and reference.

Only the current turn's token representations are pooled for the final score.

### Context Types

#### Within-Participant Context

Previous utterances from the same participant.

#### Across-Participant Context

Previous turns from the other participant, arranged so each model input remains in the appropriate language.

### Context Sources

- reference translations,
- machine-translated hypotheses.

### Window Size

Up to nine previous sentences are tested for COMET experiments.

## Main Results

### Existing Metrics

COMET-22 is the strongest average reference-based metric across the main settings.

Reference-free metrics generally lag behind reference-based metrics, especially for translation out of English.

Learned neural metrics generally outperform lexical metrics.

### Effect of Context

#### Reference-Based Evaluation

Adding context does not improve COMET-22 on average and can reduce correlation.

A strong reference may already resolve the ambiguity, while additional context can add noise.

#### Reference-Free Evaluation Into English

Context generally hurts or fails to help.

#### Reference-Free Evaluation Out of English

Context improves COMET-20-QE. Correlation increases as useful context is added.

The best setting uses complete information from both speakers.

#### Segment Length

Short segments, especially source length at or below 20 characters, benefit most.

#### Ambiguity

Turns marked as containing discourse-sensitive phenomena benefit more than non-contextual turns.

### Context Quality

Corrupting context through swapping or dropping information reduces performance.

Representative average Agent-direction result:

| Setting | Correlation |
|---|---:|
| No context | 0.379 |
| Correct context | 0.420 |
| Swapped source context | 0.364 |
| Swapped translation context | 0.296 |
| Swapped both | 0.299 |

This demonstrates that context must be relevant and complete.

## LLM-Based Evaluation

### CONTEXT-MQM

The paper adds:

- eight previous bilingual source sentences,
- one in-domain example,
- an MQM-style error-analysis prompt.

The experiment uses GPT-4 on 1,000 English-German items.

### Results

| Metric | All | Imperfect |
|---|---:|---:|
| LLM-MQM without context | 0.642 | 0.512 |
| CONTEXT-MQM | 0.655 | 0.560 |
| COMET-22 | 0.564 | 0.453 |

Context gives a larger improvement on imperfect translations.

## Recommended Practices from the Paper

### When References Are Available

Use COMET-22 as the primary metric and use error-predicting metrics for finer-grained analysis.

### When References Are Unavailable

- For translation into English, use COMET-20-QE without added context.
- For translation out of English, use context-aware COMET-20-QE.
- At dialogue level, use SLIDE among the evaluated reference-free options.
- Context-aware LLM MQM is promising but expensive and only tested at limited scale.

## Strengths

1. Evaluates metrics in a real conversational domain.
2. Uses professional MQM judgments as the reference.
3. Covers multiple translation directions.
4. Distinguishes reference-based and reference-free use cases.
5. Studies context type, context length, direction, and source length.
6. Tests noisy and incomplete context.
7. Includes learned, lexical, dialogue-level, and LLM metrics.
8. Produces practical metric recommendations.

## Limitations

1. The domain is customer support, not open social conversation.
2. Only German, French, and Portuguese are included.
3. Context effects are direction-dependent and not fully explained.
4. The LLM evaluation is limited to 1,000 English-German examples.
5. The GPT-4 experiment is expensive and not reproducible with all open models.
6. Correlation with MQM does not directly measure preservation of politeness, stance, indirectness, or code-switching.
7. Dialogue quality is approximated through averaged turn-level scores.
8. Added context can contain source noise and previous MT errors.
9. Context-aware metric improvements do not prove that a translation model itself used context.
10. Results may not transfer directly to Indian languages.

## Assumptions

- MQM judgments are a reliable gold standard for chat quality.
- Correlation is an appropriate measure of metric usefulness.
- Previous turns contain relevant information for the current turn.
- Context can be represented through simple input concatenation.
- Agent and customer directions are comparable enough for aggregate analysis.

## Relevance to My Project

This paper directly informs the evaluation layer of the proposed benchmark.

The benchmark should not assume that more context always improves automatic evaluation.

A suitable evaluation plan is:

```text
human pragmatic judgment
standard reference metric
reference-free metric
context-aware metric
LLM-based structured judgment
```

Results should be reported separately for:

- source-to-English,
- English-to-source-language if included,
- short versus long turns,
- context-required versus context-independent items,
- each pragmatic phenomenon.

## Methods I Can Reuse

1. Annotate whether context is required.
2. Store both speakers' previous turns.
3. Test several context windows.
4. Compare correct, incomplete, and irrelevant context.
5. Report results separately for short ambiguous items.
6. Compare automatic metrics with native-speaker judgments.
7. Use structured MQM-like prompts instead of asking an LLM only for a score.
8. Evaluate imperfect outputs separately from the full set.
9. Distinguish turn-level and dialogue-level evaluation.

## Methods I Should Not Copy Directly

1. Do not assume COMET results transfer directly to Indian languages.
2. Do not treat aggregate MQM as a complete pragmatic score.
3. Do not use an LLM judge without human-correlation analysis.
4. Do not add long context indiscriminately.
5. Do not average across translation directions without separate analysis.
6. Do not equate improved metric correlation with improved translation.

## Questions Raised by the Paper

1. Which Indian-language direction benefits from context-aware evaluation?
2. Does context help detect politeness and indirectness errors specifically?
3. How should prior code-switched turns be represented?
4. Can speaker-role metadata outperform raw context?
5. What is the smallest useful context window?
6. Can an open multilingual LLM perform structured pragmatic evaluation reliably?
7. How should dialogue-level pragmatic failure be aggregated across turns?

## Final Takeaway

Context can improve chat translation evaluation, but only under identifiable conditions. The proposed project should annotate context necessity, evaluate metrics against native-speaker judgments, and avoid assuming that longer context or an LLM judge is automatically better.
