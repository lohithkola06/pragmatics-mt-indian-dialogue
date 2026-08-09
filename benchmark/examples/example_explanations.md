# Example Items Explained

This document walks through four benchmark items field by field, one from each
pragmatic category. It is the worked companion to
[annotation_schema.md](../schema/annotation_schema.md), which gives the formal
field definitions.

**Files in this directory**

| File | Contents |
|---|---|
| `example_items.jsonl` | Four complete items, copied verbatim from the pilot set. Validates against `item_schema.json`. |
| `contrastive_examples.jsonl` | Ten focused contrastive examples — five valid, five deliberately invalid — used for training. **This is a teaching extract, not benchmark items, and does not follow `item_schema.json`.** |
| `example_explanations.md` | This document. |

> All four items carry `review_status: NEEDS_NATIVE_REVIEW`. They illustrate the
> schema; they are not validated ground truth.

To check the example items:

```bash
python scripts/validate_jsonl.py benchmark/examples/example_items.jsonl
```

---

## Example 1 — `HIN_POL_001` (politeness and formality)

```text
Context   1. A (Professor): Yeh assignment kal shaam tak jama kar dijiye.
Source    2. B (Student):   Sir, kya mujhe do din aur mil sakte hain?
```

A student asks a professor for a deadline extension.

### Identity and provenance

| Field | Value | Why |
|---|---|---|
| `schema_version` | `0.1.0` | The schema this item was written against |
| `item_id` | `HIN_POL_001` | `HIN` = Hindi, `POL` = politeness/formality, `001` = first in that group |
| `language` | `Hindi` | The utterance is entirely Hindi, written in Latin script |
| `language_variety` | `Standard Hindi (romanized)` | Not regionally marked |
| `translation_direction` | `Hindi-English` | Must agree with `language` |
| `source_type` | `ELICITED` | Written to target politeness, not drawn from a corpus |
| `source_reference` | `null` | Required to be null for elicited items — there is no source to cite |
| `license` | `TO_BE_CONFIRMED` | Nothing has been licence-checked yet, and saying otherwise would be false |
| `review_status` | `NEEDS_NATIVE_REVIEW` | Drafted during repository construction; no native speaker has seen it |

### Dialogue structure

`context` holds one turn; `source_utterance` is turn 2, one after the last context
turn, as validation requires. Speaker IDs are `A` and `B` — never real names.

| Field | Value | Why |
|---|---|---|
| `listener_role` | `Professor` | The addressee |
| `relationship` | `ACADEMIC` | The coarse type; the specific roles live in `speaker_role` / `listener_role` |
| `relative_status` | `SPEAKER_LOWER` | The **speaker** (student) is the junior party |
| `familiarity` | `LOW` | They are not close |
| `literal_gloss` | "Sir, can I get two more days?" | Deliberately flat. Note it does *not* say "could I please" — that is translation work, not glossing |

### Pragmatic labels

| Field | Value | Why |
|---|---|---|
| `primary_phenomenon` | `POLITENESS_FORMALITY` | Matches the `POL` code in the item ID |
| `secondary_phenomena` | `["FORMALITY", "SPEECH_ACT"]` | Also at stake, but not what the item tests |
| `speech_act` | `REQUEST` | If the professor responded appropriately they would grant or refuse |
| `politeness_level` | `RESPECTFUL` | `Sir` plus the `kya … sakte hain` interrogative frame |
| `formality_level` | `FORMAL` | Institutional setting, careful phrasing |
| `stance` | `DEFERENTIAL` | The speaker yields to the professor's judgement |
| `emotion` | `WORRIED` | Distinct from stance: deference points outward, worry is felt inward |
| `indirectness` | `MODERATELY_INDIRECT` | The request is visible but softened; not a bare "give me two days" |
| `code_switch_function` | `null` | `null`, not `NOT_APPLICABLE` — this is monolingual Hindi, so there is no switch to judge |

### Context metadata

| Field | Value | Why |
|---|---|---|
| `context_status` | `HELPFUL` | Cover the context: the utterance still reads as a polite request. Confidence drops, the reading does not change |
| `context_required` | `false` | The boolean form of the same judgement |
| `minimum_context_window` | `1` | One turn is worth supplying |
| `relevant_context_turns` | `[1]` | Turn 1 establishes the deadline being negotiated |

Contrast this with `HIN_IND_003` below, which is `REQUIRED`.

### Translation data

`preservation_requirement` names the property at risk, not the content:

> "The translation must remain a deferential request from a student to a professor.
> It must not become a demand or a statement of intent."

`reference_translations` holds two acceptable renderings and `acceptable_variants`
a third. At least one reference is required.

`contrastive_translation` is **"I need two more days."** — same facts, grammatical,
unremarkable on its own, but in context a deferential request has become a flat
statement of need to a superior. `contrastive_error_category` is
`POLITENESS_ERROR`; `severity` is `MAJOR` because the professor would form a
materially different impression of the student without the exchange breaking down.

### Annotation metadata

Every field is at its unannotated default: `annotator_ids` is `[]`,
`adjudicator_id` is `null`, `agreement_status` is `NOT_ANNOTATED`,
`annotator_notes` is empty. `creator_notes` records where the politeness load sits.

**Nothing here is fabricated.** No annotator has rated this item, and the fields say
so.

---

## Example 2 — `HIN_IND_003` (indirect requests and refusals)

```text
Context   1. A (Manager):  Weekend pe office aa sakte ho?
Source    2. B (Employee): Sir, weekend pe ghar pe kuch program hai.
```

An employee declines weekend work without ever saying no.

### What makes this item different from Example 1

| Field | Value | Why it differs |
|---|---|---|
| `primary_phenomenon` | `INDIRECT_REQUEST_REFUSAL` | Matches the `IND` code |
| `speech_act` | `INDIRECT_REFUSAL` | The employee never states a refusal; the previous turn makes it one |
| `indirectness` | `HIGHLY_INDIRECT` | The words never name the act being performed |
| `context_status` | **`REQUIRED`** | Cover the context and this is a neutral fact about a family event. The pragmatic reading genuinely changes |
| `context_required` | `true` | Must be `true` whenever `context_status` is `REQUIRED` |
| `source_type` | `MINIMAL_PAIR` | Paired with `HIN_IND_004`, which performs the same refusal directly between friends |

The `REQUIRED` label is the one to study. The test is not "does context help" — it
is "does the reading change without it". Here it does: refusal becomes a
scheduling remark.

Because `context_status` is `REQUIRED`, the schema also enforces that `context` has
at least one turn, `relevant_context_turns` is non-empty, `minimum_context_window`
is at least 1, and `context_explanation` is non-empty.

### The minimal pair

`HIN_IND_003` and `HIN_IND_004` differ in exactly one dimension — how much is left
implied:

| | `HIN_IND_003` | `HIN_IND_004` |
|---|---|---|
| Source | `Sir, weekend pe ghar pe kuch program hai.` | `Nahi yaar, nahi aa paunga.` |
| `indirectness` | `HIGHLY_INDIRECT` | `DIRECT` |
| `relationship` | `WORKPLACE` | `FRIEND` |
| Contrastive breaks it by | making the refusal explicit | making a clear refusal vague |

The two contrastive translations fail in **opposite directions**. That is
deliberate: a benchmark containing only "too direct" errors could be beaten by a
system that always hedges.

Minimal-pair partners are recorded in `creator_notes` and must be kept in the same
data split to avoid leakage.

---

## Example 3 — `HIN_STA_001` (stance and emotion)

```text
Context   1. A (Close friend): Main aaj phir late ho gaya.
Source    2. B (Close friend): Tumse toh yahi ummeed thi.
```

One friend teases another for being late again.

### Why the labels are what they are

| Field | Value | Why |
|---|---|---|
| `speech_act` | `TEASING` | Not `CRITICISM`: the previous turn is a self-deprecating admission, and you tease people about things they have just admitted |
| `stance` | `PLAYFUL` | The attitude taken toward the listener |
| `emotion` | `NEUTRAL` | The speaker is not themselves feeling anything strong. Stance and emotion genuinely come apart here |
| `politeness_level` | `FAMILIAR` | `tum` between close friends. **Not `DISRESPECTFUL`** — the closeness licenses it |
| `context_status` | `REQUIRED` | Without the admission, this could be a genuine reproach |
| `severity` | `CRITICAL` | The contrastive **reverses** the social meaning, from solidarity to insult |

### The hardest judgement in the schema

The teasing/insult boundary cannot be settled from the words. It depends on
`relationship`, `familiarity`, and the previous turn — which is exactly why the
schema records all three.

`creator_notes` says so explicitly, and flags the item for particular scrutiny. If
two annotators split between `TEASING` and `INSULT`, that disagreement is recorded
as `REGIONAL_VARIATION` or `LABEL_DISAGREEMENT` and **preserved**, not averaged
away. See [../guidelines/adjudication_guidelines.md](../guidelines/adjudication_guidelines.md).

### Why `CRITICAL`

The contrastive is *"That's exactly what I expect from someone like you."* — a
three-word edit. Apply the severity test: could this cause offence or reverse the
intent? Yes to both. Affection becomes contempt, and a friendship could be damaged.

Compare `HNG_STA_004`, where an embarrassed apology is flattened into a routine one.
That is `MINOR`: the apology still lands.

---

## Example 4 — `HNG_CSW_004` (code-switching)

```text
Context   1. A (Colleague): Everything okay? Meeting mein tum kaafi quiet the.
Source    2. B (Colleague): Arre kuch nahi yaar, bas thoda ghar ki tension hai.
```

A colleague answers a concerned question by shifting out of workplace English into
Hindi.

### What makes the switch meaningful

| Field | Value | Why |
|---|---|---|
| `language` | `Hinglish` | Enforced: `CODE_SWITCHING` items must be Hinglish |
| `code_switch_function` | `INTIMACY` | Must name a real function — `NOT_APPLICABLE` and `null` are both rejected for this category |
| `context_status` | `REQUIRED` | **The context turn is in English.** Without it there is no switch to perceive |
| `severity` | `MAJOR` | A confiding reply becomes a distant, formal one |

This item shows why the context field carries more than reference resolution. The
English opener is what makes the Hindi reply *a switch*. Remove it and the
utterance is simply Hindi — the phenomenon disappears entirely.

### Applying the substitution test

Would replacing the Hindi with English equivalents change the social meaning?
Yes — answering a friendly enquiry in the same workplace English keeps the exchange
professional, while switching signals a move to a personal footing. So the switch
carries a discourse function, and the label is `INTIMACY`.

Now compare `HNG_POL_001`:

```text
Sir almost done hai, bas ek slide baaki hai.
```

`presentation`, `slide` and `almost done` are ordinary workplace vocabulary.
Substituting Hindi equivalents changes nothing socially, so
`code_switch_function` is `NOT_APPLICABLE` and the item's real subject is the
deference in `Sir`.

**These two items exist as a pair on purpose.** One shows switching that matters;
the other shows switching that does not. A benchmark with only the first would
teach systems to over-read every English token.

### The honest limitation

`creator_notes` records an open problem: the target language is English, so the
switch itself cannot survive translation. What the benchmark can test is whether
the *footing shift* survives — whether the reply still reads as confiding rather
than formal.

Whether that is a fair test is listed as an open question in
[../schema/schema_version.md](../schema/schema_version.md) and needs native-speaker
and supervisor input. It is recorded rather than resolved.

---

## Three distinctions worth carrying away

**1. `null` versus `NOT_APPLICABLE` for `code_switch_function`.**
`null` = monolingual Hindi, no switch exists (Examples 1–3).
`NOT_APPLICABLE` = Hinglish with English tokens that do no pragmatic work.
A named function = the switch carries meaning (Example 4).

**2. `HELPFUL` versus `REQUIRED` context.**
`HELPFUL` (Example 1): confidence drops without context, the reading holds.
`REQUIRED` (Examples 2–4): the reading itself changes.

**3. Stance versus emotion.**
Example 1 is `DEFERENTIAL` in stance and `WORRIED` in emotion. Example 3 is
`PLAYFUL` in stance and `NEUTRAL` in emotion. Two fields, two facts.

---

## Regenerating this subset

`example_items.jsonl` is extracted verbatim from the pilot set so the two cannot
drift apart:

```bash
python3 -c "
import json
keep = ['HIN_POL_001', 'HIN_IND_003', 'HIN_STA_001', 'HNG_CSW_004']
out = []
with open('benchmark/pilot/pilot_items_v1.jsonl', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            item = json.loads(line)
            if item['item_id'] in keep:
                out.append(item)
out.sort(key=lambda i: keep.index(i['item_id']))
with open('benchmark/examples/example_items.jsonl', 'w', encoding='utf-8') as f:
    for item in out:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
"
python scripts/validate_jsonl.py benchmark/examples/example_items.jsonl
```

If a pilot item changes, re-run this so the examples stay in step.
