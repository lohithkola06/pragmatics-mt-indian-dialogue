# Annotator Training

**Before you start:** read
[annotation_guidelines.md](annotation_guidelines.md) and
[label_definitions.md](../schema/label_definitions.md) once through. This document
gives you practice.

> **Important.** The examples below were written during repository construction to
> illustrate the distinctions in the guidelines. **They have not been validated by
> native speakers.** The "answers" are the intended readings, not confirmed ground
> truth. If you disagree with one, you may well be right — write down why, because
> that disagreement is useful information about the guidelines.

Work through the ten exercises, write your answer before reading the explanation,
then check the common mistakes and the readiness checklist at the end.

---

## Part 1: The core idea

Machine translation is usually judged on whether the facts survive. This project
asks a different question: **does the social meaning survive?**

Consider a student asking a professor for more time:

```text
Sir, kya mujhe do din aur mil sakte hain?
```

Two translations:

- "Sir, could I please have two more days?"
- "I need two more days."

Both are factually perfect. Both mention two days. Neither invents anything. But
the second one makes a respectful student sound like they are issuing a demand to
a professor.

That gap — accurate content, wrong social meaning — is a **pragmatic failure**, and
finding it is the entire purpose of your work here.

Three things follow, and they are the habits this training is meant to build:

1. **Rate accuracy and social meaning separately.** A translation can score 3 on
   accuracy and 0 on politeness. When that happens, you have found what we are
   looking for. Do not lower the accuracy score because the translation was rude.
2. **Read the context before the translation.** Decide what the speaker is doing
   first. Otherwise the translation tells you what to think.
3. **Say when you are unsure.** An honest `UNCERTAIN` is worth more than a guess,
   because guesses look like agreement or disagreement when they are neither.

---

## Part 2: Ten training examples

### Example 1 — Accuracy versus social meaning

```text
Context   Professor: Yeh assignment kal shaam tak jama kar dijiye.
Source    Student:   Sir, kya mujhe do din aur mil sakte hain?
Candidate "Give me two more days."
```

**Rate `semantic_adequacy` and `politeness_preservation` (0–3 each).**

<details><summary>Answer</summary>

`semantic_adequacy` = **3**. `politeness_preservation` = **0**.

Every fact is right: two days, more time, the student wants it. Nothing has been
added or lost. So accuracy is full marks.

But an imperative to a professor removes all deference. `Sir` is gone and the
interrogative frame has become an order.

**The trap:** scoring accuracy at 1 or 2 "because it's wrong". It is not
inaccurate. It is impolite. Those are different columns.
</details>

---

### Example 2 — Politeness versus formality

```text
Bhaiya, thoda discount kar dijiye na.
```
*(customer to shopkeeper)*

**Label `politeness_level` and `formality_level`.**

<details><summary>Answer</summary>

`politeness_level` = **RESPECTFUL**. `formality_level` = **INFORMAL**.

The `-iye` imperative form and the address term `bhaiya` mark respect toward the
listener. But the setting is street bargaining and the coaxing particle `na` is
thoroughly casual — the register is not formal at all.

**The trap:** assuming polite implies formal. They are separate fields precisely
because combinations like this are common. A shopkeeper's `Rate fixed hai` is the
opposite pairing: formal in register, not especially deferential.
</details>

---

### Example 3 — Stance versus emotion

```text
Context   Manager:  Yeh report phir se banani padegi.
Source    Employee: Sir, main teen baar already revise kar chuka hoon.
```

**Label `stance` and `emotion`.**

<details><summary>Answer</summary>

`stance` = **DISAPPROVING**. `emotion` = **FRUSTRATED**.

The employee is pushing back against the instruction — that outward position is
the stance. What they are feeling inside is frustration at having done the work
three times already.

**The trap:** choosing one and leaving the other `NEUTRAL`. Both fields carry real
information here, and the schema wants both.

Note the stance is not `IRRITATED`: the employee is disapproving of the *instruction*
rather than showing annoyance at the manager. Either is arguable — if you chose
`IRRITATED`, note why.
</details>

---

### Example 4 — Judging indirectness

```text
Context   Manager:  Weekend pe office aa sakte ho?
Source    Employee: Sir, weekend pe ghar pe kuch program hai.
```

**Label `speech_act` and `indirectness`.**

<details><summary>Answer</summary>

`speech_act` = **INDIRECT_REFUSAL**. `indirectness` = **HIGHLY_INDIRECT**.

The employee never says no. They state a fact about their weekend and leave the
manager to draw the conclusion. That is what makes it highly indirect.

**Apply the test:** cover the context. `Sir, weekend pe ghar pe kuch program hai`
alone is just information about a family event. Only with the manager's request
does it become a refusal. The reading changes, so the item would also be
`context_status: REQUIRED`.

**The trap:** labelling it `INFORMATION` because that is the surface form. Label
what the utterance *does*.
</details>

---

### Example 5 — Context requirement

```text
Context   Classmate: Maine poora syllabus ek din mein khatam kar liya.
Source    Classmate: Achha? Poora?
```

**Label `context_status` and `stance`.**

<details><summary>Answer</summary>

`context_status` = **REQUIRED**. `stance` = **SKEPTICAL**.

Read `Achha? Poora?` on its own and it is a neutral request for confirmation. Read
it after an implausible boast and it is open disbelief. The pragmatic reading
genuinely changes, which is the bar for `REQUIRED`.

`emotion` would be `SURPRISED` — surprise is what is felt, scepticism is the
position taken. Record both.

**The trap:** marking everything `REQUIRED` because context always feels useful.
The bar is that the reading *changes*, not that context is nice to have. If you
would reach the same reading with slightly less confidence, that is `HELPFUL`.
</details>

---

### Example 6 — Is the code-switching meaningful?

```text
Context   Manager: Kal ka presentation ready hai?
Source    Intern:  Sir almost done hai, bas ek slide baaki hai.
```

**Label `code_switch_function`.**

<details><summary>Answer</summary>

`code_switch_function` = **NOT_APPLICABLE**.

`presentation`, `ready`, `almost done` and `slide` are ordinary workplace
vocabulary for these speakers. Apply the substitution test: swap in Hindi
equivalents and the social meaning does not change at all. The switch is doing no
discourse work.

What this item is actually about is `Sir` — the deference marker. Its primary
phenomenon is politeness, not code-switching.

**The trap:** treating every English token in Hinglish as pragmatically loaded. If
you did that, the category would apply to nearly every Hinglish utterance and would
tell us nothing.

Compare with a switch that *is* meaningful: `Dekho, this is the final deadline.`
Here the shift into English marks the statement as official policy rather than
personal opinion — function `AUTHORITY`.
</details>

---

### Example 7 — Teasing or insult?

```text
Context   Close friend: Main aaj phir late ho gaya.
Source    Close friend: Tumse toh yahi ummeed thi.
```

**Label `speech_act` and `stance`. How confident are you?**

<details><summary>Answer</summary>

Intended: `speech_act` = **TEASING**, `stance` = **PLAYFUL**.

Two things support the teasing reading: the relationship is `FRIEND` with `HIGH`
familiarity, and the previous turn is a self-deprecating admission. You generally
do not tease someone about something they have not just admitted themselves.

**But this is the hardest boundary in the whole schema**, and it is entirely
context-dependent. The same sentence between distant colleagues is a reproach.
Some speakers find the construction sharper than others.

If you labelled `CRITICISM`, or marked `MULTIPLE_VALID_INTERPRETATIONS`, that is a
defensible answer — write down what would settle it. When two annotators split
here, we record the disagreement rather than resolving it away.
</details>

---

### Example 8 — Is this contrastive translation valid?

```text
Source        Sir, weekend pe ghar pe kuch program hai.
Reference     "Sir, there's a family function at home this weekend."
Contrastive   "Sir, I have a wedding at home this weekend."
```

**Is this a valid contrastive translation? Why or why not?**

<details><summary>Answer</summary>

**No — reject it.**

A "function" has become a "wedding". That is a **semantic** change: information was
added that the source does not contain.

Why this matters: a translation system could reject this candidate purely by
comparing content words, without any understanding of politeness or indirectness.
The item would then look like it tests pragmatics while actually testing word
overlap.

A valid contrastive keeps the facts identical and changes only the social meaning:

> "Sir, I can't come on the weekend."

Same facts, grammatical, plausible alone — but it states outright the refusal the
employee deliberately left implied.
</details>

---

### Example 9 — The most important check

```text
Context       Customer: Aaj hi delivery ho sakti hai kya?
Source        Support:  Ma'am aaj toh thoda difficult hoga, kal try karte hain.
Reference     "That'll be a bit difficult today, ma'am — we'll try for tomorrow."
Contrastive   "It might be hard to manage today, ma'am; let's aim for tomorrow."
```

**Is this a valid contrastive translation?**

<details><summary>Answer</summary>

**No — reject it, and this is the most valuable rejection you can make.**

The contrastive is simply *another good translation*. It hedges as much as the
reference, it is equally polite to the customer, and you would happily send either.
There is no pragmatic error to detect.

An item built on this measures nothing — worse, it penalises a system for producing
a perfectly acceptable translation.

A working contrastive for the same item:

> "That's not possible today, ma'am. We'll do it tomorrow."

The hedge is replaced by a flat statement of impossibility, which lands very
differently with a customer.

**Whenever you would accept the contrastive after reading the context, say so.**
This single judgement invalidates the item, and catching it is worth more than
confirming ten sound ones.
</details>

---

### Example 10 — Assigning severity

```text
Context       Manager:  Yeh kaam aaj hi poora ho jaye.
Source        Employee: Sir, koshish karta hoon, lekin thoda mushkil lag raha hai.
Reference     "I'll try, sir, but it does look a bit difficult."
Contrastive   "I'll try, sir, but that's not going to happen."
```

**Assign `severity`: MINOR, MAJOR or CRITICAL.**

<details><summary>Answer</summary>

**CRITICAL.**

Work down the checklist:

1. *Could this cause offence, escalation, or a reversal of intent?* Yes. The
   employee was signalling difficulty while leaving the manager room to respond.
   The contrastive has them flatly contradicting a superior. That can damage a
   working relationship and could escalate.

So it stops at `CRITICAL` without needing the later questions.

**The trap:** reserving `CRITICAL` for rudeness. There is nothing rude in "that's
not going to happen" — the politeness marking and the offer to try are both intact.
What makes it critical is the change in what the employee is *doing*: hedging has
become contradiction.

Compare a `MINOR` case: dropping `Sir` from an otherwise correct sentence. The
manager understands exactly the same thing and takes no offence; only the polish is
lost.

If you answered `MAJOR`, that is defensible — this is a judgement call, and the
severity labels in the pilot dataset are exactly what we need reviewed. Note your
reasoning.
</details>

---

## Part 3: Common mistakes

**1. Letting social judgement leak into the accuracy score.**
The most damaging error. If a rude translation gets marked semantically inadequate,
the benchmark can no longer find the cases it exists to find. Rate
`semantic_adequacy` on facts alone.

**2. Reading the translation before the context.**
Once you have read the candidate, it shapes how you read the source. Decide what
the speaker is doing first.

**3. Collapsing politeness into formality, or stance into emotion.**
These are separate fields because they come apart. Filling one and leaving the
other `NEUTRAL` throws away information.

**4. Over-applying `REQUIRED` to context.**
The bar is that the reading *changes* without context, not that context helps.

**5. Over-applying code-switching functions.**
Most English in Hinglish is unmarked borrowing. Use the substitution test and use
`NOT_APPLICABLE` freely.

**6. Guessing instead of using `UNCERTAIN`.**
A guess is indistinguishable from a confident judgement in the data, and it
corrupts the agreement statistics. Uncertainty is information.

**7. Treating your own regional usage as the standard.**
Ask whether the utterance is natural *for some substantial group of speakers*, not
whether it is what you would say. Note when your judgement is region-dependent.

**8. Writing notes that do not say anything.**
"Sounds odd" cannot be acted on. "I'd expect `bata dijiyega` rather than
`bata denge` from a junior to a senior" can.

**9. Rating dimensions that do not apply.**
Scoring `3` for code-switch preservation on a monolingual Hindi item inflates the
result. Use `NOT_APPLICABLE`.

**10. Discussing specific items with the other annotator.**
Calibrate on the guidelines, never on particular answers. Coordination inflates
agreement and makes the reliability estimate meaningless.

---

## Part 4: Readiness checklist

You are ready to begin annotating when you can answer yes to all of these.

**Concepts**

- [ ] I can explain the difference between semantic and pragmatic meaning.
- [ ] I can give an example of a translation that is fully accurate and
      pragmatically wrong.
- [ ] I understand why accuracy is rated independently of social meaning.

**Distinctions**

- [ ] I can distinguish politeness from formality, and give an example that is
      polite but informal.
- [ ] I can distinguish stance from emotion, and give an utterance that has both.
- [ ] I can apply the cover-the-context test for indirectness.
- [ ] I can apply the substitution test for meaningful code-switching.
- [ ] I know the bar for `context_status: REQUIRED`.

**Scales**

- [ ] I know what 3, 2, 1 and 0 mean on the preservation scale.
- [ ] I know the difference between `UNCERTAIN`,
      `MULTIPLE_VALID_INTERPRETATIONS` and `NOT_APPLICABLE`.
- [ ] I can distinguish `MINOR`, `MAJOR` and `CRITICAL` severity.

**Items**

- [ ] I can say why a contrastive translation that changes the facts is invalid.
- [ ] I can say why a contrastive translation that is still acceptable is invalid,
      and I know this is the most valuable thing I can catch.

**Practice**

- [ ] I have worked through all ten examples above.
- [ ] I have written down every point where I disagreed with an intended answer.
- [ ] I have annotated three or four real items and compared with the other
      annotator to calibrate.
- [ ] I understand that I must not discuss individual items during annotation.

If any box is unticked, re-read the relevant section of
[annotation_guidelines.md](annotation_guidelines.md) before starting. If a box
stays unticked after that, the guidelines are unclear — tell us, because that is a
result we need.
