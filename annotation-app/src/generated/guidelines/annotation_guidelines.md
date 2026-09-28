# Annotation Guidelines

**For:** native or near-native speakers of Hindi and Hinglish annotating the
pragmatics-preserving MT benchmark.
**You do not need a linguistics background.** You need to be a confident speaker
who can say how an utterance would land socially.

**Related documents:**
[label definitions](../schema/label_definitions.md) ·
[severity guidelines](../schema/severity_guidelines.md) ·
[annotator training](annotator_training.md) ·
[human evaluation protocol](human_evaluation_guidelines.md)

---

## 1. What this benchmark is for

Machine translation systems are usually judged on whether they preserve *what was
said*. This benchmark measures something else: whether they preserve *what was
meant socially*.

A translation can be word-for-word accurate and still be wrong. If an employee
respectfully asks a manager for a day off and the translation makes it sound like a
demand, no fact has been changed — but the employee now sounds rude. We call
that a **pragmatic failure**:

> A pragmatic failure occurs when a translation preserves the basic semantic
> content of an utterance but fails to preserve its intended social or
> communicative meaning in context.

Your job is to judge these two things **separately**, and that separation is the
whole point of the exercise. A translation can score full marks for accuracy and
zero for politeness. When that happens, you have found exactly what we are looking
for.

Existing work supports this split. Voita, Sennrich & Titov (2019) found that
around 7% of English–Russian sentence pairs were individually good translations yet
wrong when read together, with forms of address the single largest source. Bawden
et al. (2018) showed that translation quality scores can improve while discourse
accuracy stays at chance. Agrawal et al. (2024) found that context helps evaluation
most for short and ambiguous turns. This benchmark applies that logic to Indian
conversational dialogue.

---

## 2. Semantic meaning versus pragmatic meaning

| | Semantic meaning | Pragmatic meaning |
|---|---|---|
| Question it answers | What information was conveyed? | What was the speaker *doing*, and how do they stand toward the listener? |
| Changes when | facts, entities, quantities change | respect, register, attitude, directness, relationship change |
| Example | "tomorrow" becomes "Friday" | "could I please" becomes "I need" |

Worked example:

```text
Context   Manager:  Is hafte project ki deadline hai.
Source    Employee: Sir, kya main kal chhutti le sakta hoon?
```

| Candidate | Semantically correct? | Pragmatically correct? |
|---|---|---|
| "Sir, could I please take tomorrow off?" | yes | yes |
| "Sir, could I please take Friday off?" | **no** — wrong day | yes |
| "I need tomorrow off." | yes | **no** — a request became a demand |
| "Give me tomorrow off." | yes | **no** — a request became an order |

Rows three and four are the cases this benchmark exists to catch. Rate semantic
adequacy high and politeness preservation low. Do not average them together.

---

## 3. How to read the dialogue context

Each item gives you up to three previous turns, then the utterance being
translated. Read them in order and, before looking at any translation, answer for
yourself:

1. Who is speaking, and to whom?
2. What is the relationship — status, familiarity?
3. What has just happened in the conversation?
4. What is the speaker trying to achieve with this turn?

Only then look at the candidate translation.

**Read the context as binding.** If the context says the speakers are close
friends, judge the utterance as speech between close friends, even if you would
personally use different words with your own friends.

**Some items deliberately have no context.** When the context field says there are
no previous turns, that is not an omission — the item is testing whether the
utterance stands alone.

---

## 4. Identifying the main speech act

The speech act is **what the speaker is doing**: requesting, refusing, warning,
teasing, apologising, complaining.

Ask: *if the listener responded appropriately, what would they do?*

- If they would hand something over → `REQUEST`
- If they would drop the topic → `INDIRECT_REFUSAL`
- If they would feel better → `REASSURANCE`
- If they would laugh → `TEASING` or `JOKE`
- If they would just now know something → `INFORMATION`

**Grammatical form is not the speech act.** `Aur kitni der lagaoge?` ("How much
longer are you going to take?") is a question in form and a complaint in function.
Label the function.

**One utterance, one main act.** If several apply, choose the one the speaker most
wants to accomplish. Said to a manager who wants a report today,
`Ma'am, aaj hi khatam karna thoda tight rahega` ("Ma'am, finishing it today is going to be a bit tight")
looks like information; what the speaker is really doing is disagreeing, gently.
Label `DISAGREEMENT`.

---

## 5. Politeness versus formality

These are **two different fields** and they move independently.

- **Politeness** = how much respect and deference is shown *to the listener*.
  Carried by `aap` / `tum` / `tu`, `-iye` imperatives, honorifics, `ji`, address
  terms, softening particles.
- **Formality** = the register of the *situation*. Carried by vocabulary choice,
  full versus reduced forms, how careful the phrasing is.

Four combinations, all real:

| | Formal | Informal |
|---|---|---|
| **Polite** | `Aapki application review mein hai.` (an office clerk) | `Bhaiya, yahin rok dijiye na.` (to an auto driver) |
| **Not polite** | `Counter paanch baje band hota hai.` (flat, official) | `Abe, jaldi aa na.` (close friends) |

The bottom-left cell is the one people get wrong. A clerk saying "the counter closes
at five" is being formal without being especially deferential.

**A test:** could you keep the same words but say them to someone of very different
status? If not, politeness is doing the work. Could you keep the same words in a
very different setting — a court, a chat with friends? If not, formality is doing
the work.

---

## 6. Stance versus emotion

- **Stance** points *outward*: how the speaker positions themselves toward the
  listener or the situation. Warm, dismissive, sceptical, deferential.
- **Emotion** points *inward*: what the speaker is feeling. Worried, frustrated,
  embarrassed, excited.

They are recorded separately because they genuinely come apart:

| Utterance | Stance | Emotion |
|---|---|---|
| `Ma'am, yeh already paanchva version hai.` | `DISAPPROVING` (toward the request for more changes) | `FRUSTRATED` |
| `Ma'am, aaj hi khatam karna thoda tight rahega.` | `RELUCTANT` | `WORRIED` |
| `Sach mein? Pachaas?` | `SKEPTICAL` | `SURPRISED` |
| `Chinta mat karo, pehli baar mein aisa hota hai.` | `SYMPATHETIC` | `NEUTRAL` |

The last row matters: a speaker can take a sympathetic stance while feeling
nothing much themselves. That is normal and is not a contradiction.

**Do not infer emotion from the topic.** An utterance about a failed exam is not
automatically `SAD`. Label what the utterance *expresses*, not what the situation
might make someone feel.

---

## 7. Judging indirectness

Indirectness is how much of the intent is left to implication.

The test: **cover the context and read the utterance alone.**

- You can say immediately what the speaker wants → `DIRECT`
- You can guess with the context but not without it → `HIGHLY_INDIRECT`
- The intent is visible but softened or hedged → `MODERATELY_INDIRECT`

```text
DIRECT               Nahi, main nahi ruk sakta.                  "No, I can't stay."
MODERATELY_INDIRECT  Aaj rukna thoda mushkil hoga.               "Staying today would be a bit hard."
HIGHLY_INDIRECT      Aaj shaam cousin ko station se lena hai.   "I have to pick my cousin up from the station this evening."
```

All three can be refusals. They differ in how much the speaker made the listener do
the work.

**Indirectness is not politeness.** `Kripya yeh kaam kal tak poora kijiye` is very
polite and completely direct. Keep the two judgements apart.

---

## 8. Identifying meaningful code-switching

Most English words in Hinglish are ordinary vocabulary. `office`, `meeting`,
`submit`, `report`, `refund`, `agenda` are simply how people speak. They are **not**
pragmatic code-switching, and marking them as such would make the category
meaningless.

**The substitution test.** Replace the English item with its closest Hindi
equivalent. *Does the social meaning change?*

- If no → the switch carries no discourse function. Label `NOT_APPLICABLE`.
- If yes → identify the function: authority, intimacy, emotional intensity,
  sarcasm, quotation, humour, identity, emphasis, technical terminology.

Good example of a meaningful switch:

```text
Colleague:  You look a bit tired today, all okay?
Speaker:    Haan yaar, bas raat ko neend nahi aayi.
```

The reply switches out of workplace English into Hindi. That shift signals a move
from professional to personal footing. Function: `INTIMACY`.

Good example of a switch that is **not** meaningful:

```text
Sir report almost ready hai, bas conclusion likhna hai.
```

`report`, `almost ready` and `conclusion` are unmarked borrowings. Function:
`NOT_APPLICABLE`. The item is really about the deference in `Sir`.

---

## 9. Labelling the context requirement

Each item records how much the context matters.

| Label | Use when |
|---|---|
| `NOT_REQUIRED` | The utterance is fully interpretable on its own |
| `HELPFUL` | Context resolves a reference or raises your confidence, but the pragmatic reading survives without it |
| `REQUIRED` | Without the context, the intended pragmatic reading is not recoverable |

**The honest test:** cover the context. Read the source utterance alone.

- Would a competent speaker arrive at a *different* pragmatic reading?
  → `REQUIRED`
- Would they arrive at the *same* reading with less confidence? → `HELPFUL`
- Would nothing change? → `NOT_REQUIRED`

Example of `REQUIRED`:

```text
Context:  Maine kal raat pachaas pages padh liye.
Source:   Sach mein? Pachaas?
```

Alone, `Sach mein? Pachaas?` is a neutral request for confirmation. With the boastful
claim before it, it is open disbelief. The reading genuinely changes, so this is
`REQUIRED`.

Be strict here. It is tempting to mark everything `REQUIRED` because context always
feels useful. Only use it when the reading actually *changes*.

---

## 10. Judging reference translations

A reference translation should be one you would be comfortable sending on the
speaker's behalf.

Ask, in this order:

1. **Is it accurate?** Same facts, entities, quantities.
2. **Does it perform the same act?** A request stays a request.
3. **Does it project the same relationship?** Same level of respect and distance.
4. **Does it carry the same attitude?** Same warmth, irritation, reluctance.
5. **Does it sound like something a person would say in Indian English?**

**Target variety: Indian English.** The benchmark translates into Indian English,
so judge the references against the standard educated register used in Indian
professional and everyday settings, not a British or American standard. The pilot
references were drafted before this was decided, and many lean toward a generic
informal register, so expect to adjust them. When a reference is not natural Indian
English, **write an Indian-English alternative in the suggested reference box**
(the `suggested_indian_english_reference` column) rather than only flagging it. Conforming the reference set to Indian English is one of the main
things this review pass is for.

A reference can be acceptable without being the only good option. If you would
have translated it differently but the version given is defensible, accept it and
put your alternative in the suggested reference box. We collect those.

**Reject a reference** when it changes the speech act, flips the politeness level,
reverses the stance, or is not natural Indian English. Say which of those it is.

---

## 11. Judging contrastive translations

Every item has a **contrastive translation**: one that is deliberately close in
meaning but wrong in social meaning. Your job is to confirm it actually is that.

A good contrastive translation is:

1. **semantically close** — the same facts,
2. **grammatical and natural** — not broken English,
3. **plausible on its own** — you would not flag it without the context,
4. **wrong in context** — given the dialogue, it misrepresents the speaker,
5. **narrow** — it breaks one pragmatic property, not several.

Check each. The two failures we most need you to catch:

**It is still fine.** If, having read the context, you would accept the contrastive
translation as a reasonable rendering, the item does not test anything. Say so.
This is the single most valuable judgement you can give us.

**It is wrong for the wrong reason.** If it changes the facts, or is ungrammatical,
then a system could reject it without understanding pragmatics at all. Say so.

Example of a good contrastive translation:

```text
Context       Manager: Aaj thoda der tak ruk sakte ho?
Source        Sir, aaj shaam mujhe cousin ko station se lena hai.
Reference     "Sir, I have to pick my cousin up from the station this evening."
Contrastive   "Sir, I can't stay late today."
```

Same facts, perfectly grammatical, fine in isolation — but it states a refusal the
employee deliberately left implied. That is exactly right.

Example of a bad contrastive translation:

```text
Contrastive   "Sir, I have to pick my cousin up from the airport this evening."
```

This changes the facts (the station became the airport). A system could catch it
without any pragmatic understanding. Reject it.

---

## 12. The preservation scale

Rate each dimension on this scale:

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

Three non-numeric labels are also available in the `uncertainty_label` column:

```text
UNCERTAIN
MULTIPLE_VALID_INTERPRETATIONS
NOT_APPLICABLE
```

Use `NOT_APPLICABLE` when the dimension does not apply — code-switch preservation
on a monolingual Hindi item, for example. Do not score `3` for a dimension that
does not exist; that inflates the results.

---

## 13. Using the uncertainty labels

These three mean different things. Please keep them apart.

**`UNCERTAIN`** — *you* cannot decide, and more information would not obviously
help. Use it freely. An honest `UNCERTAIN` is far more useful than a guess, because
guesses look like agreement or disagreement when they are neither.

**`MULTIPLE_VALID_INTERPRETATIONS`** — the *item* genuinely supports more than one
reading. This is a claim about the item, not about your confidence. Use it when you
can articulate two readings and defend both.

**`NOT_APPLICABLE`** — the dimension does not apply to this item at all.

Whenever you use `UNCERTAIN` or `MULTIPLE_VALID_INTERPRETATIONS`, write one line in
the notes saying why. That line is the most valuable thing in the row.

---

## 14. Handling multiple valid interpretations

Pragmatic meaning is not always determinate, and we are not trying to force it to
be.

When an utterance genuinely supports two readings:

1. Label `MULTIPLE_VALID_INTERPRETATIONS`.
2. In the notes, state both readings in one sentence each.
3. Say which you find more likely, and why.
4. Say what in the context would settle it.

Example:

```text
Source:  Wah, kya naya hai isme.
Notes:   Between close friends after a self-deprecating admission this is
         affectionate teasing. Between colleagues who are not close it is a
         genuine reproach. The context says close friends, so I read it as
         teasing, but with lower confidence than usual.
```

We would rather have this than a confident label. Disagreement that reflects real
ambiguity is a finding, and the adjudication process is designed to preserve it
rather than average it away.

---

## 15. Avoiding one regional interpretation

Hindi and Hinglish vary a great deal by region, city, community, age and setting.
The benchmark must not silently encode one variety as the correct one.

**Please do:**

- Judge whether the utterance is natural **for some substantial group of
  speakers**, not whether it is what *you* would say.
- Note when your judgement depends on region, age, or setting.
- Flag items that only work in one variety.

**Please do not:**

- Mark an utterance unnatural only because it is not your own usage.
- Assume the politeness norms you grew up with are universal.
- Resolve a regional difference by picking the "standard" form.

Example of a note we want:

```text
"'Tu' here reads as intimate and friendly to me (Delhi). I know speakers for whom
'tu' is markedly rude regardless of closeness. The item's reading holds for my
variety but a reviewer from a different region should check it."
```

When two annotators disagree because of regional norms, we record it as
`REGIONAL_VARIATION` and keep both readings. Nobody is wrong.

---

## 16. Recording notes

The notes column is not optional decoration. It is where the information that
improves the schema lives.

**Always write a note when you:**

- use `UNCERTAIN` or `MULTIPLE_VALID_INTERPRETATIONS`,
- score any dimension `0` or `1`,
- think the source utterance sounds unnatural,
- think the contrastive translation is actually acceptable,
- think the labels on the item are wrong,
- notice your judgement depends on region, age, or setting.

**Useful notes are specific:**

| Weak note | Useful note |
|---|---|
| "sounds odd" | "'bhej denge' is fine but I'd expect 'bhej dijiyega' from a junior to a senior in an office" |
| "wrong politeness" | "the reference drops 'Sir', which is the only deference marker in the source" |
| "not sure" | "unsure whether this is teasing or a real complaint; depends on how close they are, and the context does not say" |

Notes in English or Hindi are both fine. Mixing is fine.

---

## 17. Before you start

- Read [label_definitions.md](../schema/label_definitions.md) once through.
- Work through [annotator_training.md](annotator_training.md) and check your
  answers.
- Annotate three or four items, then stop and compare with the other annotator to
  calibrate. Do not annotate the whole set before comparing.

**Do not discuss individual items with the other annotator while annotating.**
Independent judgements are what make agreement measurement meaningful. Calibrate
on the guidelines, not on specific answers.

If you find yourself unsure about the same thing repeatedly, that is a gap in these
guidelines. Tell us — that is a result, not a failure.
