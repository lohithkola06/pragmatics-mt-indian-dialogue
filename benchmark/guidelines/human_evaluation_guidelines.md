# Human Evaluation Guidelines

**For:** native-speaker evaluators rating machine-translation output against
benchmark items.

This document covers the **evaluation** protocol — rating translations produced by
translation systems. It is distinct from
[annotation_guidelines.md](annotation_guidelines.md), which covers validating the
benchmark items themselves. The rating scale and label definitions are shared
between them.

Native-speaker evaluation is the primary measure in this benchmark. Automatic
metrics and LLM judges are validated *against* these judgements, never the other
way round.

---

## 1. What the evaluator sees

For each judgement you are shown:

- the dialogue context (0 to 3 previous turns),
- the source utterance,
- the speaker and listener roles, relationship, relative status and familiarity,
- one candidate translation,
- the literal gloss, for evaluators who do not read the source language.

You are **not** shown:

- which system produced the candidate,
- whether the candidate is a reference translation or a contrastive one,
- the other evaluator's ratings,
- the item's own pragmatic labels.

These are withheld deliberately. Knowing that a candidate is the "correct" one
would make the evaluation worthless.

---

## 2. The rating scale

Every dimension is rated 0 to 3:

```text
3 = fully preserved
2 = mostly preserved
1 = partially preserved
0 = not preserved
```

| Score | Meaning |
|---|---|
| **3** | A listener would take exactly the intended meaning |
| **2** | Slightly weaker or less natural; intent and relationship still clear |
| **1** | Noticeably changed; a listener could form a different impression |
| **0** | Lost or reversed |

Three non-numeric labels are available in the `uncertainty_label` column:

```text
UNCERTAIN
MULTIPLE_VALID_INTERPRETATIONS
NOT_APPLICABLE
```

Use `NOT_APPLICABLE` where a dimension does not apply — code-switch preservation on
a monolingual Hindi item, for example. **Do not score `3` for a dimension that does
not exist**; that inflates system scores.

---

## 3. The ten evaluation questions

Rate each candidate on all ten dimensions.

| # | Question | Column |
|---|---|---|
| 1 | Is the translation semantically correct? | `semantic_adequacy` |
| 2 | Is the speech act preserved? | `speech_act_preservation` |
| 3 | Is politeness preserved? | `politeness_preservation` |
| 4 | Is formality preserved? | `formality_preservation` |
| 5 | Is stance preserved? | `stance_preservation` |
| 6 | Is emotional tone preserved? | `emotion_preservation` |
| 7 | Is indirectness preserved? | `indirectness_preservation` |
| 8 | Is the social relationship preserved? | `relationship_appropriateness` |
| 9 | Is code-switching function preserved? | `code_switch_preservation` |
| 10 | Is the translation natural? | `translation_naturalness` |

Two further columns are recorded:

- `source_naturalness` — is the **source utterance** something a real speaker would
  say? This rates the benchmark item, not the system.
- `overall_pragmatic_preservation` — your holistic judgement of whether the
  speaker's social meaning survived. This is not the average of the others; it is
  your overall reading.

---

## 4. Rate semantic adequacy independently

This is the most important instruction in this document.

**Question 1 must be answered without regard to questions 2 to 9.**

The benchmark exists to find translations that are semantically fine and
pragmatically wrong. If you lower semantic adequacy because a translation was rude,
that signal disappears and the benchmark stops measuring what it is for.

```text
Context   Professor: Yeh assignment kal shaam tak jama kar dijiye.
Source    Student:   Sir, kya mujhe do din aur mil sakte hain?
Candidate "I need two more days."
```

Correct ratings:

| Dimension | Score | Why |
|---|---|---|
| `semantic_adequacy` | **3** | Every fact is correct: two days, more time, the speaker wants it |
| `speech_act_preservation` | 1 | A request became a statement of need |
| `politeness_preservation` | 0 | All deference marking is gone |
| `relationship_appropriateness` | 0 | Sounds like a peer, not a student to a professor |
| `overall_pragmatic_preservation` | 0 | The social meaning did not survive |

A common error is to give `semantic_adequacy` a 1 or 2 here "because it's wrong".
It is not semantically wrong. It is pragmatically wrong. Score it as such.

---

## 5. Judging each dimension

**Speech act.** Does the translation do the same thing? A request that becomes an
order, or an offer that becomes an instruction, scores low even if every word is
accurate.

**Politeness.** Would the listener feel the same level of respect? Check address
terms, hedges, imperative forms. Dropping the only deference marker in an utterance
is a real loss even when it is a single word.

**Formality.** Is the register the same? Both directions count: casual speech
rendered as bureaucratic English fails just as surely as formal speech rendered as
slang.

**Stance.** Does the speaker hold the same attitude toward the listener? Teasing
that becomes contempt, or reassurance that becomes indifference, scores 0.

**Emotion.** Is the same affect expressed, at roughly the same intensity? Frustration
flattened into cheerful compliance is a reversal, not a weakening.

**Indirectness.** Is the same amount left implied? A hint stated outright and a
clear refusal turned vague are both failures.

**Relationship.** Would a reader infer the same relationship — same relative status,
same closeness — from the translation alone?

**Code-switching.** Only applies where the source has a meaningful switch. Since the
target is English, the switch itself cannot survive; judge whether the *function*
does — the authority, intimacy, irony or quotative framing it carried. Where the
source has no meaningful switch, use `NOT_APPLICABLE`.

**Naturalness.** Would a fluent speaker of **Indian English** produce this? Rate the
English, not the fidelity. The benchmark targets Indian English, so judge against
the standard educated register used in Indian professional and everyday settings,
not a British or American standard. A rendering that is natural in Indian English
scores high even if it would sound slightly unusual elsewhere, and one that sounds
foreign in Indian English scores lower even if it is impeccable British or American
English. See
[../../docs/project/language_scope_decision.md](../../docs/project/language_scope_decision.md).

---

## 6. Practical procedure

1. Read the context and the source. Decide what the speaker is doing *before*
   reading the candidate.
2. Read the candidate once, at normal speed. Note your immediate reaction.
3. Rate `semantic_adequacy` first, on its own.
4. Rate the pragmatic dimensions.
5. Rate naturalness.
6. Give `overall_pragmatic_preservation` as a holistic judgement.
7. Write a note whenever you score 0 or 1, or use an uncertainty label.

**Rate in the order the sheet gives you.** Do not read ahead to compare candidates
for the same item: each candidate is rated on its own terms. Comparative judgement
happens in the separate contrastive-ranking task, not here.

**Take breaks.** Rating drifts when tired, and drift shows up as inconsistency
between the start and end of a session. Twenty to thirty candidates in a sitting is
a reasonable maximum.

---

## 7. Calibration

Before the first full session, all evaluators rate the same five items and compare.
The aim is not identical numbers — it is a shared understanding of what separates a
2 from a 1.

Recalibrate if:

- one evaluator's mean rating is consistently more than half a point from another's,
- evaluators disagree on what `NOT_APPLICABLE` covers,
- agreement on any single dimension is much lower than on the others.

Calibrate on the **guidelines and the scale**, never by agreeing what to say about
particular items. Agreeing on specific answers destroys the independence that makes
the agreement statistics meaningful.

---

## 8. Independence

- Do not discuss individual items with other evaluators during a session.
- Do not look at another evaluator's completed sheet.
- Do not revise earlier ratings after learning what someone else gave.

Agreement is computed on independent judgements. Any coordination inflates it and
makes the reliability estimate wrong.

---

## 9. Recording notes

Write a note whenever you:

- score any dimension 0 or 1,
- use `UNCERTAIN` or `MULTIPLE_VALID_INTERPRETATIONS`,
- think the source utterance is unnatural (also lower `source_naturalness`),
- think the candidate is acceptable despite an obvious difference from the source,
- notice your judgement depends on region, age or setting.

Specific notes are worth far more than general ones:

| Weak | Useful |
|---|---|
| "too rude" | "drops 'Sir', which is the only thing marking this as student-to-professor" |
| "unnatural" | "'kindly do the needful' is not how a colleague of the same rank would phrase this" |
| "not sure" | "unsure if this is teasing or a genuine complaint; depends how close they are and the context does not say" |

Notes in English or Hindi are both fine.

---

## 10. After evaluation

Completed sheets are analysed with:

```bash
python scripts/calculate_agreement.py <completed annotation CSV>
```

This reports percentage agreement, Cohen's kappa where there are exactly two
evaluators, and Krippendorff's alpha, per dimension. It reports `n/a` where a
statistic cannot be computed rather than estimating one.

Low agreement on a dimension is a finding about the **dimension**, not a failure by
the evaluators. It usually means the definition needs sharpening, and that is
recorded in [../pilot/pilot_issues.md](../pilot/pilot_issues.md).
