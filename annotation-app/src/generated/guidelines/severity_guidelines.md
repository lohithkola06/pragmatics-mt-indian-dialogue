# Severity Guidelines

**Schema version:** `0.1.0`
**Field:** `severity`
**Allowed values:** `MINOR`, `MAJOR`, `CRITICAL`

Severity records **how damaging the pragmatic error in the contrastive
translation would be** if a real system produced it in a real conversation. It
describes the error, not the item and not the difficulty of the translation.

> Severity judgements in the pilot dataset were assigned during drafting and have
> **not** been confirmed by native speakers. Reviewing them is part of the pilot.

---

## 1. The three levels

### `MINOR`

The style becomes weaker, flatter or less natural, but the communicative intent
and the social relationship remain understandable. A listener would notice
something slightly off, and would not misread the speaker.

**Test:** would the listener still correctly identify what the speaker wanted and
how they felt about the listener? If yes, and only the polish is lost, it is
`MINOR`.

### `MAJOR`

Politeness, speech act, stance, indirectness or relationship meaning changes
substantially. A listener would draw a different conclusion about what the speaker
meant or how they regard the listener, but the exchange would probably not break
down.

**Test:** would the listener form a materially different impression of the
speaker's intent or attitude? If yes, it is at least `MAJOR`.

### `CRITICAL`

The translation can cause offence, escalation, serious misunderstanding, or a
reversal of the speaker's intent. A listener could reasonably be insulted, or act
on the opposite of what was meant.

**Test:** could this plausibly damage the relationship, provoke a confrontation, or
lead the listener to act on a reversed meaning? If yes, it is `CRITICAL`.

---

## 2. `MINOR` examples

**2.1 — A dropped address term.**

| | |
|---|---|
| Source | `Sir report almost ready hai, bas conclusion likhna hai.` |
| Reference | "It's almost ready, sir, just the conclusion left." |
| Contrastive | "It's almost ready, just the conclusion left." |
| Error | The only deference marker, `Sir`, is dropped. |

An intern sounds slightly less deferential to a manager. The status update is
accurate, nothing is being requested, and no manager would take offence. The
loss is real but cosmetic.

**2.2 — A flattened apology.**

| | |
|---|---|
| Source | `Sorry yaar, dimaag se hi nikal gaya.` |
| Reference | "Sorry man, it went right out of my head." |
| Contrastive | "Sorry, I forgot." |
| Error | The solidarity marker and the vivid idiom are lost; visible embarrassment becomes routine. |

The apology still lands. The friend still understands that the speaker forgot and
is sorry. Only the emotional weight is reduced.

**2.3 — Quotation converted to reported speech.**

| | |
|---|---|
| Source | `Madam ne bola, 'submit it by Friday', aur class khatam.` |
| Reference | "She said, 'submit it by Friday', and that was the end of class." |
| Contrastive | "She said to submit it by Friday and class ended." |
| Error | A verbatim quotation becomes indirect reported speech. |

The reported content survives intact. What is lost is that the speaker was
reproducing the teacher's exact words. A listener is not misled about the facts.

**2.4 — An over-polite peer request.**

| | |
|---|---|
| Source | `Tum mujhe kal ka agenda bhej doge?` |
| Reference | "Can you send me tomorrow's agenda?" |
| Contrastive | "Would you be so kind as to forward me tomorrow's agenda?" |
| Error | Casual peer register is inflated into elaborate deference. |

Between close colleagues this sounds odd, possibly arch. But nothing is
misunderstood and no offence is likely, so it stays `MINOR`.

---

## 3. `MAJOR` examples

**3.1 — A respectful request becomes a command.**

| | |
|---|---|
| Source | `Aap mujhe kal ka agenda bhej denge?` |
| Reference | "Could you send me tomorrow's agenda?" |
| Contrastive | "Send me tomorrow's agenda." |
| Error | A respectful `aap` interrogative becomes a bare imperative. |

A junior colleague now appears to be issuing instructions to a senior. The
propositional request is identical; the relationship it projects is not. A senior
colleague would notice and could reasonably think the junior was being brusque.

**3.2 — An implied refusal made explicit.**

| | |
|---|---|
| Context | Manager: `Aaj thoda der tak ruk sakte ho?` |
| Source | `Sir, aaj shaam mujhe cousin ko station se lena hai.` |
| Reference | "Sir, I have to pick my cousin up from the station this evening." |
| Contrastive | "Sir, I can't stay late today." |
| Error | A refusal the employee deliberately left implied is stated outright. |

Both versions decline. But the source lets the manager withdraw the request
without either party losing face, and the contrastive forces a direct refusal on
record. That is a substantial change in what the employee did.

**3.3 — A hint becomes a demand.**

| | |
|---|---|
| Context | Flatmate: `Aaj toh bahut thand hai.` |
| Source | `Haan, AC abhi bhi chal raha hai.` |
| Reference | "Yeah, the AC's still running." |
| Contrastive | "Yes, switch the AC off." |
| Error | An observation that implies a request becomes a direct imperative. |

The speaker chose not to ask. The contrastive asks. The listener now receives an
instruction they were never given.

**3.4 — Reassurance becomes indifference.**

| | |
|---|---|
| Source | `Chinta mat karo, pehli baar mein aisa hota hai.` |
| Reference | "Don't worry, it happens the first time." |
| Contrastive | "Doesn't matter. First time." |
| Error | Warm reassurance is flattened into indifference. |

A junior who has just made their first mistake is comforted in one version and
brushed off in the other. The words are close; the effect on the listener is not.

---

## 4. `CRITICAL` examples

**4.1 — Teasing becomes contempt.**

| | |
|---|---|
| Context | Close friend: `Chabi phir se ghar pe reh gayi yaar.` |
| Source | `Wah, kya naya hai isme.` |
| Reference | "Ha, so what else is new?" |
| Contrastive | "So what else is new with someone like you?" |
| Error | `someone like you` introduces categorical contempt. |

This is `CRITICAL` because the social meaning **reverses**: an expression of
solidarity between close friends becomes an insult about the listener's character.
A listener could reasonably be hurt and the friendship could be damaged.

**4.2 — A face-saving hedge becomes a flat refusal.**

| | |
|---|---|
| Context | Manager: `Yeh report aaj hi submit honi chahiye.` |
| Source | `Ma'am, aaj hi khatam karna thoda tight rahega.` |
| Reference | "Ma'am, finishing it today is going to be a bit tight." |
| Contrastive | "Ma'am, it won't be finished today." |
| Error | A deliberately soft hedge becomes a blunt announcement of failure. |

An employee who was signalling difficulty now appears to flatly refuse a manager's
deadline. This is the kind of error that damages a working relationship, and it
could escalate into a formal disagreement.

**4.3 — An embarrassed deflection becomes a blunt refusal.**

| | |
|---|---|
| Context | Close friend: `Yaar, teri bike ek din ke liye mil sakti hai?` |
| Source | `Woh... kal mujhe khud office jaana hai.` |
| Reference | "Well... I actually need it for office tomorrow myself." |
| Contrastive | "No, I'm not lending you my bike." |
| Error | A face-saving deflection becomes an explicit refusal to lend. |

Both parties were protecting each other's face. The contrastive strips that away
and puts a refusal on record between friends, which is markedly more wounding than
what was said.

---

## 5. Deciding between levels

Work down this list and stop at the first `yes`:

1. Could the listener be offended, or act on a reversed meaning, or could the
   relationship be damaged? → `CRITICAL`
2. Would the listener form a materially different impression of the speaker's
   intent, attitude, or standing? → `MAJOR`
3. Is only naturalness, polish or emotional weight reduced? → `MINOR`

**Common calibration errors:**

- *Inflating everything to `MAJOR`.* If the listener would understand the speaker
  correctly and simply find the phrasing a little flat, it is `MINOR`.
- *Reserving `CRITICAL` for rudeness only.* Reversal of intent is equally critical.
  A hedged refusal rendered as agreement is `CRITICAL` even though nothing rude is
  said.
- *Rating the translation's quality instead of the error's consequence.* A clumsy
  but socially harmless translation is `MINOR`. An elegant translation that
  reverses the speaker's stance is `CRITICAL`.
- *Letting the source's difficulty drive the rating.* Severity is about the
  consequence of the error, not how hard the item was to translate.

**When two annotators disagree by one level** (`MINOR` versus `MAJOR`, or `MAJOR`
versus `CRITICAL`), that is ordinary scale variation; record it and let
adjudication settle it. **When they disagree by two levels** (`MINOR` versus
`CRITICAL`), the item or the guidelines are unclear and the item should be
reviewed.

---

## 6. How severity is used

Severity feeds the severity-weighted error score defined in the benchmark
blueprint:

```text
MINOR    = 1
MAJOR    = 5
CRITICAL = 10

severity_weighted_error = sum(error_weight) / number_of_items
```

This is always reported **alongside** raw error counts, never instead of them, so
that a system making many small errors and a system making a few severe ones stay
distinguishable.

Because severity is weighted this heavily, mis-assigned `CRITICAL` labels distort
results more than any other annotation error. When in doubt between `MAJOR` and
`CRITICAL`, choose `MAJOR` and record the doubt in the notes.
