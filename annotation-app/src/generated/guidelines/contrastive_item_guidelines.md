# Contrastive Item Guidelines

**For:** anyone writing or reviewing the `contrastive_translation` field.

A contrastive translation is a deliberately wrong translation used to test whether
a system can tell pragmatic correctness from semantic similarity. The design
follows the contrastive test-suite method used by Bawden et al. (2018) and Voita,
Sennrich & Titov (2019): if the wrong candidate is semantically as plausible as the
right one, a system that ignores context and social meaning is reduced to chance.

That only works if the contrastive translation is built correctly. A sloppy one
lets a system score well without understanding anything.

---

## 1. The eight requirements

A contrastive negative must satisfy **all** of these.

### 1. Preserve most propositional content

The same facts, entities, quantities and time references. If the reference says
"two days", so does the contrastive.

*Why:* if the facts change, a system can reject it on semantics alone and never
engage with pragmatics.

### 2. Be grammatical

Fluent, well-formed English. No agreement errors, no broken syntax.

*Why:* an ungrammatical candidate is rejected by any competent language model
without pragmatic reasoning.

### 3. Be plausible in isolation

Read on its own, without the dialogue context, it should look like a perfectly
reasonable translation. A reader should not be able to flag it without the context.

*Why:* this is what forces the system to actually use the context. It is the whole
mechanism of the test.

### 4. Become inappropriate in context

Given the dialogue context and the speaker relationship, it misrepresents the
speaker — their respect, intent, attitude, or directness.

*Why:* without this there is no error to detect.

### 5. Target one main pragmatic feature

Exactly one of politeness, formality, speech act, stance, emotion, indirectness,
code-switch function, or relationship.

*Why:* if two things break at once, a correct rejection tells us nothing about
which capability the system has.

### 6. Avoid unrelated semantic errors

No added or removed information, no changed referents, no invented detail.

*Why:* same as requirement 1 — it makes the item detectable for the wrong reason.

### 7. Remain minimally different

Change as little as possible. Ideally one phrase, one construction, one address
term.

*Why:* the smaller the difference, the more precisely the item isolates the
phenomenon. Large differences confound.

### 8. Be independently reviewed by native speakers

At least two native speakers must confirm that the intended difference is real and
that the contrastive is genuinely unacceptable in context.

*Why:* a contrastive that a native speaker finds acceptable is not a negative at
all. **No item is accepted without this step.**

---

## 2. Valid contrastive negatives

### 2.1 Politeness removed

```text
Context       Manager:  Is hafte project ki deadline hai.
Source        Employee: Sir, kya main kal chhutti le sakta hoon?
Reference     "Sir, could I please take tomorrow off?"
Contrastive   "I need tomorrow off."
```

Same facts. Grammatical. Fine in isolation. In context, a deferential employee
request becomes a flat demand on a manager. One feature: politeness. ✅

### 2.2 Indirectness removed

```text
Context       Flatmate: Aaj toh bahut thand hai.
Source        Flatmate: Haan, AC abhi bhi chal raha hai.
Reference     "Yeah, the AC's still running."
Contrastive   "Yes, switch the AC off."
```

Closely related content. Grammatical. Reasonable alone. In context, a hint the
speaker deliberately left implicit becomes a direct instruction. One feature:
indirectness. ✅

### 2.3 Indirectness *added*

```text
Context       Close friend: Aaj raat movie chalega?
Source        Close friend: Nahi bhai, main nahi aa raha.
Reference     "No bro, I'm not coming."
Contrastive   "I might be busy tonight, let's see."
```

The error direction is reversed: a clear refusal becomes a vague hedge, leaving the
listener still expecting the speaker. Failures in **both** directions are needed, or
systems can score well by always being maximally indirect. ✅

### 2.4 Stance reversed

```text
Context       Close friend: Chabi phir se ghar pe reh gayi yaar.
Source        Close friend: Wah, kya naya hai isme.
Reference     "Ha, so what else is new?"
Contrastive   "So what else is new with someone like you?"
```

Almost identical wording. `someone like you` turns affectionate teasing into
contempt. Minimal difference, large social consequence. One feature: stance. ✅

### 2.5 Register inflated

```text
Context       Colleague: Kal client ke saath meeting hai.
Source        Colleague: Tum mujhe kal ka agenda bhej doge?
Reference     "Can you send me tomorrow's agenda?"
Contrastive   "Would you be so kind as to forward me tomorrow's agenda?"
```

Over-politeness is a pragmatic failure too. Between close peers this projects a
distance the source does not encode. One feature: formality. ✅

---

## 3. Invalid: semantic changes

```text
Source        Sir, aaj shaam mujhe cousin ko station se lena hai.
Reference     "Sir, I have to pick my cousin up from the station this evening."
Contrastive   "Sir, I have to pick my cousin up from the airport this evening."   ❌
```

**Why it fails:** the station became the airport. Requirement 1 and 6 are broken. A
system can reject this by comparing content words, learning nothing about
indirectness.

```text
Contrastive   "Sir, I have to pick my cousin up from the station tomorrow evening."   ❌
```

**Why it fails:** *this* evening became *tomorrow* evening. A time-reference change is
a semantic error, however small it looks.

---

## 4. Invalid: ungrammatical negatives

```text
Source        Aap mujhe kal ka agenda bhej denge?
Reference     "Could you send me tomorrow's agenda?"
Contrastive   "You will sending me agenda tomorrow the?"   ❌
```

**Why it fails:** requirement 2. Any fluent system rejects this on form alone. It
measures grammaticality, which is not what this benchmark is for.

```text
Contrastive   "Send to me the agenda of tomorrow."   ❌
```

**Why it fails:** subtler, but still a grammatical error rather than a pragmatic
one. If a native speaker would call it *wrong English* rather than *the wrong
thing to say*, it is invalid.

---

## 5. Invalid: targeting multiple phenomena

```text
Context       Manager:  Yeh report aaj hi submit honi chahiye.
Source        Employee: Ma'am, aaj hi khatam karna thoda tight rahega.
Reference     "Ma'am, finishing it today is going to be a bit tight."
Contrastive   "Nah, not today."   ❌
```

**Why it fails:** requirement 5 and 7. This breaks politeness *and* indirectness
*and* formality *and* the speech act, all at once. If a system prefers the
reference, we cannot say which capability it demonstrated.

**The fix** is to change one thing:

```text
Contrastive   "Ma'am, it won't be finished today."   ✅
```

The address term and the sentence shape are retained; only the hedge itself
becomes a flat prediction. One feature moves.

---

## 6. Invalid: still socially acceptable

This is the most dangerous failure because it is invisible without a native
speaker.

```text
Context       Customer: Kya aaj hi refund mil sakta hai?
Source        Support:  Sir, aaj toh mushkil hoga, do din lag sakte hain.
Reference     "That'll be difficult today, sir; it may take a couple of days."
Contrastive   "Today might be hard, sir; it could take two days."   ❌
```

**Why it fails:** requirement 4. This is simply another acceptable translation. It
hedges just as much and is equally polite. There is no error, so an item built on
it measures nothing — and worse, it *penalises* a system for choosing a perfectly
good translation.

**A working contrastive for the same item:**

```text
Contrastive   "That's not possible today, sir. It will take two days."   ✅
```

The hedge is replaced with a flat statement of impossibility. Now there is a real
difference in how the refusal lands with a customer.

**Reviewers: this is the check we most need from you.** If you would accept the
contrastive translation as a reasonable rendering after reading the context, say
so. That single judgement invalidates the item, and finding it is worth more than
confirming ten good ones.

---

## 7. Construction procedure

1. Write the reference translation first, and make it genuinely good.
2. Decide which **one** pragmatic feature to break. Record it in
   `contrastive_error_category`.
3. Make the **smallest** change to the reference that breaks that feature.
4. Re-read the contrastive without the context. Does it look fine? If it looks
   wrong already, the change was too large.
5. Re-read it with the context. Is it clearly inappropriate? If it still seems
   acceptable, the change was too small.
6. Check nothing else moved: same facts, same grammar, same register except where
   intended.
7. Write `contrastive_error` explaining precisely what breaks and why.
8. Assign `severity` using
   [severity_guidelines.md](../schema/severity_guidelines.md).
9. Send it for independent native-speaker review.

Steps 4 and 5 are a pair, and they pull against each other. That tension is what
makes a good contrastive item: **wrong in context, unremarkable outside it.**

---

## 8. Review checklist

For each contrastive translation, answer yes or no:

| # | Check |
|---|---|
| 1 | Same facts, entities, quantities and times as the reference? |
| 2 | Grammatical and natural English? |
| 3 | Looks acceptable when read without the context? |
| 4 | Clearly inappropriate when read with the context? |
| 5 | Breaks exactly one pragmatic feature? |
| 6 | Free of added or removed information? |
| 7 | As close to the reference as the error allows? |
| 8 | Confirmed by at least two native speakers? |

Any `no` in rows 1 to 7 means the item needs revision. A `no` in row 8 means it is
not yet accepted, whatever its other merits.

Record the outcome in the Stage 1 review form of the annotation app, which exports
the columns of
[../pilot/pilot_item_review_template.csv](../pilot/pilot_item_review_template.csv).

---

## 9. Automated checks

`scripts/validate_jsonl.py` catches only the mechanical problems:

- a contrastive translation identical to an accepted translation,
- an empty contrastive translation or missing explanation,
- a `contrastive_error_category` outside the controlled vocabulary.

**Everything that matters here — semantic closeness, plausibility in isolation,
inappropriateness in context, and single-feature targeting — requires human
judgement.** Passing validation says nothing about whether an item is any good.
