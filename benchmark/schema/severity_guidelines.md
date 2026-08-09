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

**2.1 — A dropped address term.** (`HNG_POL_001`)

| | |
|---|---|
| Source | `Sir almost done hai, bas ek slide baaki hai.` |
| Reference | "It's almost done, sir — just one slide left." |
| Contrastive | "It's almost done, just one slide left." |
| Error | The only deference marker, `Sir`, is dropped. |

An intern sounds slightly less deferential to a manager. The report is accurate,
the request-free statement is unchanged, and no manager would take offence. The
loss is real but cosmetic.

**2.2 — A flattened apology.** (`HNG_STA_004`)

| | |
|---|---|
| Source | `Yaar sorry, bilkul bhool gaya tha.` |
| Reference | "Sorry man, I completely forgot." |
| Contrastive | "Sorry, it slipped my mind." |
| Error | Solidarity marker and intensifier are lost; visible embarrassment becomes routine. |

The apology still lands. The friend still understands that the speaker forgot and
is sorry. Only the emotional weight is reduced.

**2.3 — Quotation converted to reported speech.** (`HNG_CSW_006`)

| | |
|---|---|
| Source | `Usne bola, 'this is not acceptable', aur chala gaya.` |
| Reference | "He said, 'this is not acceptable', and walked off." |
| Contrastive | "He said it was not acceptable and left." |
| Error | A verbatim quotation becomes indirect reported speech. |

The reported content survives intact. What is lost is that the speaker was
reproducing the manager's exact words. A listener is not misled about the facts.

**2.4 — An over-polite peer request.** (`HIN_POL_003`)

| | |
|---|---|
| Source | `Tum mujhe naya time bata doge?` |
| Reference | "Can you tell me the new time?" |
| Contrastive | "Would you be so kind as to inform me of the new time?" |
| Error | Casual peer register is inflated into elaborate deference. |

Between close colleagues this sounds odd, possibly arch. But nothing is
misunderstood and no offence is likely, so it stays `MINOR`.

---

## 3. `MAJOR` examples

**3.1 — A respectful request becomes a command.** (`HIN_POL_002`)

| | |
|---|---|
| Source | `Aap mujhe naya time bata denge?` |
| Reference | "Could you let me know the new time?" |
| Contrastive | "Tell me the new time." |
| Error | A respectful `aap` interrogative becomes a bare imperative. |

A junior colleague now appears to be issuing instructions to a senior. The
propositional request is identical; the relationship it projects is not. A senior
colleague would notice and could reasonably think the junior was being brusque.

**3.2 — An implied refusal made explicit.** (`HIN_IND_003`)

| | |
|---|---|
| Source | `Sir, weekend pe ghar pe kuch program hai.` |
| Reference | "Sir, there's a family function at home this weekend." |
| Contrastive | "Sir, I can't come on the weekend." |
| Error | A refusal the employee deliberately left implied is stated outright. |

Both versions decline. But the source lets the manager withdraw the request
without either party losing face, and the contrastive forces a direct refusal on
record. That is a substantial change in what the employee did.

**3.3 — A hint becomes a demand.** (`HIN_IND_002`)

| | |
|---|---|
| Source | `Haan, pankha band hi hai shayad.` |
| Reference | "Yeah, I think the fan's been left off." |
| Contrastive | "Yes, turn the fan on." |
| Error | An observation that implies a request becomes a direct imperative. |

The speaker chose not to ask. The contrastive asks. The listener now receives an
instruction they were never given.

**3.4 — Reassurance becomes indifference.** (`HIN_STA_005`)

| | |
|---|---|
| Source | `Koi baat nahi, ho jata hai.` |
| Reference | "Don't worry about it — these things happen." |
| Contrastive | "It doesn't matter. It happens." |
| Error | Warm reassurance is flattened into indifference. |

A junior who has just admitted a mistake is comforted in one version and brushed
off in the other. The words are close; the effect on the listener is not.

---

## 4. `CRITICAL` examples

**4.1 — Teasing becomes contempt.** (`HIN_STA_001`)

| | |
|---|---|
| Source | `Tumse toh yahi ummeed thi.` |
| Reference | "Ha, that's exactly what I'd expect from you." |
| Contrastive | "That's exactly what I expect from someone like you." |
| Error | `someone like you` introduces categorical contempt. |

This is `CRITICAL` because the social meaning **reverses**: an expression of
solidarity between close friends becomes an insult about the listener's character.
A listener could reasonably be hurt and the friendship could be damaged.

**4.2 — A face-saving hedge becomes a flat contradiction.** (`HIN_POL_008`)

| | |
|---|---|
| Source | `Sir, koshish karta hoon, lekin thoda mushkil lag raha hai.` |
| Reference | "I'll try, sir, but it does look a bit difficult." |
| Contrastive | "I'll try, sir, but that's not going to happen." |
| Error | A deliberately vague hedge becomes a blunt prediction of failure. |

An employee who was signalling difficulty now appears to contradict a manager
outright. This is the kind of error that damages a working relationship, and it
could escalate into a formal disagreement.

**4.3 — An embarrassed deflection becomes a blunt refusal.** (`HIN_IND_008`)

| | |
|---|---|
| Source | `Abhi toh khud thoda tight chal raha hoon.` |
| Reference | "Things are a bit tight for me right now, honestly." |
| Contrastive | "I'm not lending you money right now." |
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
