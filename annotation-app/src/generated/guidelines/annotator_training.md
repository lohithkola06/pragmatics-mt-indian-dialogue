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

Consider an employee asking a manager for a day off:

```text
Sir, kya main kal chhutti le sakta hoon?
```

Two translations:

- "Sir, could I please take tomorrow off?"
- "I need tomorrow off."

Both are factually perfect. Both mention a day off tomorrow. Neither invents
anything. But the second one makes a respectful employee sound like they are
issuing a demand to a manager.

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
Context   Manager:  Is hafte project ki deadline hai.
Source    Employee: Sir, kya main kal chhutti le sakta hoon?
Candidate "Give me tomorrow off."
```

**Rate `semantic_adequacy` and `politeness_preservation` (0–3 each).**

<details><summary>Answer</summary>

`semantic_adequacy` = **3**. `politeness_preservation` = **0**.

Every fact is right: a day off, tomorrow, the employee wants it. Nothing has been
added or lost. So accuracy is full marks.

But an imperative to a manager removes all deference. `Sir` is gone and the
interrogative frame has become an order.

**The trap:** scoring accuracy at 1 or 2 "because it's wrong". It is not
inaccurate. It is impolite. Those are different columns.
</details>

---

### Example 2 — Politeness versus formality

```text
Bhaiya, yahin rok dijiye na.
```
*(passenger to an auto-rickshaw driver)*

**Label `politeness_level` and `formality_level`.**

<details><summary>Answer</summary>

`politeness_level` = **RESPECTFUL**. `formality_level` = **INFORMAL**.

The `-iye` imperative form and the address term `bhaiya` mark respect toward the
listener. But the setting is a quick word in an auto-rickshaw and the particle
`na` is thoroughly casual — the register is not formal at all.

**The trap:** assuming polite implies formal. They are separate fields precisely
because combinations like this are common. A clerk's `Counter paanch baje band hota
hai` is the opposite pairing: formal in register, not especially deferential.
</details>

---

### Example 3 — Stance versus emotion

```text
Context   Manager:  Slides mein thode aur changes chahiye.
Source    Employee: Ma'am, yeh already paanchva version hai.
```

**Label `stance` and `emotion`.**

<details><summary>Answer</summary>

`stance` = **DISAPPROVING**. `emotion` = **FRUSTRATED**.

The employee is pushing back against yet another round of changes — that outward
position is the stance. What they are feeling inside is frustration at having
redone the slides five times already.

**The trap:** choosing one and leaving the other `NEUTRAL`. Both fields carry real
information here, and the schema wants both.

Note the stance is not `IRRITATED`: the employee is disapproving of the *request*
rather than showing annoyance at the manager. Either is arguable — if you chose
`IRRITATED`, note why.
</details>

---

### Example 4 — Judging indirectness

```text
Context   Manager:  Aaj thoda der tak ruk sakte ho?
Source    Employee: Sir, aaj shaam mujhe cousin ko station se lena hai.
```

**Label `speech_act` and `indirectness`.**

<details><summary>Answer</summary>

`speech_act` = **INDIRECT_REFUSAL**. `indirectness` = **HIGHLY_INDIRECT**.

The employee never says no. They state a fact about their evening and leave the
manager to draw the conclusion. That is what makes it highly indirect.

**Apply the test:** cover the context. `Sir, aaj shaam mujhe cousin ko station se
lena hai` alone is just information about an errand. Only with the manager's request
does it become a refusal. The reading changes, so the item would also be
`context_status: REQUIRED`.

**The trap:** labelling it `INFORMATION` because that is the surface form. Label
what the utterance *does*.
</details>

---

### Example 5 — Context requirement

```text
Context   Classmate: Maine kal raat pachaas pages padh liye.
Source    Classmate: Sach mein? Pachaas?
```

**Label `context_status` and `stance`.**

<details><summary>Answer</summary>

`context_status` = **REQUIRED**. `stance` = **SKEPTICAL**.

Read `Sach mein? Pachaas?` on its own and it is a neutral request for confirmation. Read
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
Context   Manager: Report ka kya status hai?
Source    Intern:  Sir report almost ready hai, bas conclusion likhna hai.
```

**Label `code_switch_function`.**

<details><summary>Answer</summary>

`code_switch_function` = **NOT_APPLICABLE**.

`report`, `almost ready` and `conclusion` are ordinary workplace vocabulary for
these speakers. Apply the substitution test: swap in Hindi
equivalents and the social meaning does not change at all. The switch is doing no
discourse work.

What this item is actually about is `Sir` — the deference marker. Its primary
phenomenon is politeness, not code-switching.

**The trap:** treating every English token in Hinglish as pragmatically loaded. If
you did that, the category would apply to nearly every Hinglish utterance and would
tell us nothing.

Compare with a switch that *is* meaningful: `Suno, attendance is compulsory from
Monday. Koi exception nahi hoga.` Here the shift into English marks the rule as
official policy rather than personal preference — function `AUTHORITY`.
</details>

---

### Example 7 — Teasing or insult?

```text
Context   Close friend: Chabi phir se ghar pe reh gayi yaar.
Source    Close friend: Wah, kya naya hai isme.
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
Source        Sir, aaj shaam mujhe cousin ko station se lena hai.
Reference     "Sir, I have to pick my cousin up from the station this evening."
Contrastive   "Sir, I have to pick my cousin up from the airport this evening."
```

**Is this a valid contrastive translation? Why or why not?**

<details><summary>Answer</summary>

**No — reject it.**

The "station" has become the "airport". That is a **semantic** change: the
contrastive states something the source does not say.

Why this matters: a translation system could reject this candidate purely by
comparing content words, without any understanding of politeness or indirectness.
The item would then look like it tests pragmatics while actually testing word
overlap.

A valid contrastive keeps the facts identical and changes only the social meaning:

> "Sir, I can't stay late today."

Same facts, grammatical, plausible alone — but it states outright the refusal the
employee deliberately left implied.
</details>

---

### Example 9 — The most important check

```text
Context       Customer: Kya aaj hi refund mil sakta hai?
Source        Support:  Sir, aaj toh mushkil hoga, do din lag sakte hain.
Reference     "That'll be difficult today, sir; it may take a couple of days."
Contrastive   "Today might be hard, sir; it could take two days."
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

> "That's not possible today, sir. It will take two days."

The hedge is replaced by a flat statement of impossibility, which lands very
differently with a customer.

**Whenever you would accept the contrastive after reading the context, say so.**
This single judgement invalidates the item, and catching it is worth more than
confirming ten sound ones.
</details>

---

### Example 10 — Assigning severity

```text
Context       Manager:  Yeh report aaj hi submit honi chahiye.
Source        Employee: Ma'am, aaj hi khatam karna thoda tight rahega.
Reference     "Ma'am, finishing it today is going to be a bit tight."
Contrastive   "Ma'am, it won't be finished today."
```

**Assign `severity`: MINOR, MAJOR or CRITICAL.**

<details><summary>Answer</summary>

**CRITICAL.**

Work down the checklist:

1. *Could this cause offence, escalation, or a reversal of intent?* Yes. The
   employee was signalling difficulty while leaving the manager room to respond.
   The contrastive has them flatly announcing failure to a superior. That can damage a
   working relationship and could escalate.

So it stops at `CRITICAL` without needing the later questions.

**The trap:** reserving `CRITICAL` for rudeness. There is nothing rude in "it
won't be finished today" — the address term is intact. What makes it critical is
the change in what the employee is *doing*: a hedge has become a flat refusal.

Compare a `MINOR` case: dropping `Ma'am` from an otherwise correct sentence. The
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
"Sounds odd" cannot be acted on. "I'd expect `bhej dijiyega` rather than
`bhej denge` from a junior to a senior" can.

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
