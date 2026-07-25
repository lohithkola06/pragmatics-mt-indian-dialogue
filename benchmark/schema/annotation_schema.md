# Annotation Schema

**Schema version:** `0.1.0`
**Machine-readable form:** [item_schema.json](item_schema.json)
**Label meanings:** [label_definitions.md](label_definitions.md)
**Severity meanings:** [severity_guidelines.md](severity_guidelines.md)
**Change history:** [schema_version.md](schema_version.md)

This document defines every field of a benchmark item. It is the human-readable
companion to `item_schema.json`; where the two disagree, the JSON Schema is what
validation actually enforces, and the disagreement is a bug to be fixed.

Every item is one line of JSON in a `.jsonl` file, encoded in UTF-8.

---

## How to read this document

Each field table gives:

- **Field** — the JSON key.
- **Type** — the JSON type.
- **Req.** — whether the field must be present. Every field in this schema is
  required to be *present*; some may legitimately be empty or `null`, which is
  noted per field.
- **Allowed values** — the controlled vocabulary, where one applies.

A field being required does not mean it must be filled in. `annotator_ids`, for
example, must be present but is an empty array until annotation happens.

---

## 1. Item identity and provenance

| Field | Type | Req. | Allowed values |
|---|---|---|---|
| `schema_version` | string | yes | semantic version, e.g. `0.1.0` |
| `item_id` | string | yes | `^(HIN\|HNG)_(POL\|IND\|STA\|CSW)_[0-9]{3}$` |
| `language` | string | yes | `Hindi`, `Hinglish` |
| `language_variety` | string | yes | free text, non-empty |
| `translation_direction` | string | yes | `Hindi-English`, `Hinglish-English` |
| `source_type` | string | yes | `NATURAL`, `ELICITED`, `MINIMAL_PAIR`, `ADAPTED` |
| `source_reference` | string or null | yes | `null` when provenance cannot be documented |
| `license` | string | yes | free text, non-empty |
| `review_status` | string | yes | `DRAFT`, `NEEDS_NATIVE_REVIEW`, `REVISED`, `APPROVED`, `REJECTED` |

### `item_id`

The identifier encodes the language and the pragmatic category:

```text
HIN_POL_001
│   │   └── zero-padded three-digit serial, unique within its language+category
│   └────── category code
└────────── language code
```

| Language code | `language` | Category code | `primary_phenomenon` |
|---|---|---|---|
| `HIN` | Hindi | `POL` | `POLITENESS_FORMALITY` |
| `HNG` | Hinglish | `IND` | `INDIRECT_REQUEST_REFUSAL` |
| | | `STA` | `STANCE_EMOTION` |
| | | `CSW` | `CODE_SWITCHING` |

`validate_jsonl.py` checks that the prefix agrees with `language` and that the
category code agrees with `primary_phenomenon`. An item whose ID contradicts its
own labels is rejected.

Example: `HIN_POL_001`, `HNG_CSW_004`.

### `source_type`

- `NATURAL` — taken from naturally occurring dialogue. **Requires a non-null
  `source_reference`.**
- `ELICITED` — written to target a specific pragmatic phenomenon.
- `MINIMAL_PAIR` — one half of a controlled pair that differs in exactly one
  pragmatic feature. Record the partner item in `creator_notes`.
- `ADAPTED` — modified from an existing source. **Requires a non-null
  `source_reference`.**

*Annotation note:* do not label an item `NATURAL` or `ADAPTED` unless the source
can actually be cited and its licence checked. Unverifiable provenance is worse
than an honestly elicited item.

### `review_status`

| Value | Meaning |
|---|---|
| `DRAFT` | Written, not yet ready for review |
| `NEEDS_NATIVE_REVIEW` | Awaiting native-speaker judgement |
| `REVISED` | Changed in response to review, needs re-checking |
| `APPROVED` | Accepted by native-speaker review |
| `REJECTED` | Will not be used; keep the item and record why |

*Annotation note:* only a native speaker may move an item to `APPROVED`. Items
produced by drafting tools start at `NEEDS_NATIVE_REVIEW`, never higher.

### `license`

Use `TO_BE_CONFIRMED` until the licensing position has actually been checked.
Do not write a licence name you have not verified.

---

## 2. Dialogue structure

| Field | Type | Req. | Allowed values |
|---|---|---|---|
| `context` | array of turn objects | yes | 0 to 3 turns |
| `source_utterance` | turn object | yes | — |
| `literal_gloss` | string | yes | non-empty |
| `listener_role` | string | yes | non-empty free text |
| `relationship` | string | yes | `FAMILY`, `FRIEND`, `ACADEMIC`, `WORKPLACE`, `SERVICE`, `INSTITUTIONAL`, `STRANGER`, `OTHER` |
| `relative_status` | string | yes | `SPEAKER_HIGHER`, `EQUAL`, `SPEAKER_LOWER`, `UNKNOWN` |
| `familiarity` | string | yes | `LOW`, `MEDIUM`, `HIGH` |

### Turn objects

Both `context` entries and `source_utterance` use the same shape:

| Field | Type | Req. | Notes |
|---|---|---|---|
| `turn_id` | integer ≥ 1 | yes | 1-based position in the dialogue |
| `speaker_id` | string | yes | short anonymous label such as `A` or `B` |
| `speaker_role` | string | yes | social role, e.g. `Student`, `Manager` |
| `text` | string | yes | non-empty; romanized Hindi or Hinglish |

Constraints enforced by validation:

- `context` holds between 0 and 3 turns. Zero is allowed only for items that are
  genuinely interpretable on their own.
- `context` turn IDs must be `1, 2, 3, …` in order, with no gaps or repeats.
- `source_utterance.turn_id` must be exactly `len(context) + 1`.
- `source_utterance.text` must be non-empty.

Example:

```json
"context": [
  {"turn_id": 1, "speaker_id": "A", "speaker_role": "Professor",
   "text": "Yeh assignment kal shaam tak jama kar dijiye."}
],
"source_utterance": {"turn_id": 2, "speaker_id": "B", "speaker_role": "Student",
   "text": "Sir, kya mujhe do din aur mil sakte hain?"}
```

*Annotation note on `speaker_id`:* the speaker of the utterance being translated
lives inside `source_utterance`, not as a separate top-level field. The top level
records the *addressee* (`listener_role`) and the relationship between them.

### `literal_gloss`

A deliberately flat English rendering of the source, written so that a reader who
does not know Hindi can follow the propositional content. It is **not** a
reference translation: it is allowed to sound stilted, and it should not attempt
to reproduce politeness or tone.

Example: for `"Haan, lekin aap thodi der baad miliye."` the gloss is
`"Yes, but you please meet after a little while."` — not
`"Yes, but please do come back a bit later."`, which is a translation.

### `relationship`, `relative_status`, `familiarity`

`relationship` is a coarse type; the specific roles are in `speaker_role` and
`listener_role`. A student addressing a professor is `relationship: ACADEMIC`,
`speaker_role: Student`, `listener_role: Professor`.

`relative_status` is the **speaker's** status relative to the listener:
`SPEAKER_LOWER` means the speaker is the junior party.

`familiarity` is how well the two parties know each other, which is independent of
status: colleagues of equal rank may be `LOW` or `HIGH` familiarity.

---

## 3. Pragmatic labels

| Field | Type | Req. | Allowed values |
|---|---|---|---|
| `primary_phenomenon` | string | yes | `POLITENESS_FORMALITY`, `INDIRECT_REQUEST_REFUSAL`, `STANCE_EMOTION`, `CODE_SWITCHING` |
| `secondary_phenomena` | array of strings | yes | `POLITENESS`, `FORMALITY`, `INDIRECTNESS`, `STANCE`, `EMOTION`, `CODE_SWITCHING`, `SPEECH_ACT`, `RELATIONSHIP`; may be empty |
| `speech_act` | string | yes | 18 values, see below |
| `politeness_level` | string | yes | `HIGHLY_RESPECTFUL`, `RESPECTFUL`, `NEUTRAL`, `FAMILIAR`, `DISRESPECTFUL`, `NOT_APPLICABLE` |
| `formality_level` | string | yes | `FORMAL`, `NEUTRAL`, `INFORMAL`, `HIGHLY_INFORMAL`, `NOT_APPLICABLE` |
| `stance` | string | yes | 12 values, see below |
| `emotion` | string | yes | 10 values, see below |
| `indirectness` | string | yes | `DIRECT`, `MODERATELY_INDIRECT`, `HIGHLY_INDIRECT`, `NOT_APPLICABLE` |
| `code_switch_function` | string or null | yes | 10 values, see below, or `null` |

`speech_act`: `REQUEST`, `COMMAND`, `SUGGESTION`, `REFUSAL`, `INDIRECT_REFUSAL`,
`WARNING`, `APOLOGY`, `COMPLAINT`, `INVITATION`, `TEASING`, `INSULT`, `JOKE`,
`AGREEMENT`, `DISAGREEMENT`, `REASSURANCE`, `CRITICISM`, `INFORMATION`, `QUESTION`.

`stance`: `NEUTRAL`, `WARM`, `CARING`, `PLAYFUL`, `IRRITATED`, `DISMISSIVE`,
`DEFERENTIAL`, `RELUCTANT`, `SYMPATHETIC`, `SKEPTICAL`, `APPROVING`, `DISAPPROVING`.

`emotion`: `NEUTRAL`, `HAPPY`, `ANGRY`, `SAD`, `WORRIED`, `EXCITED`, `FRUSTRATED`,
`EMBARRASSED`, `AFRAID`, `SURPRISED`.

`code_switch_function`: `EMPHASIS`, `HUMOR`, `IDENTITY`, `INTIMACY`, `AUTHORITY`,
`TECHNICAL_TERMINOLOGY`, `EMOTIONAL_INTENSITY`, `SARCASM`, `QUOTATION`,
`NOT_APPLICABLE`.

Full definitions with examples are in [label_definitions.md](label_definitions.md).

*Annotation notes:*

- `primary_phenomenon` is the single category the item was built to test. It must
  match the item ID's category code. Everything else that is also at stake goes in
  `secondary_phenomena`.
- **Politeness and formality are separate fields on purpose.** An utterance can be
  polite but informal (`"Bhaiya, thoda discount kar dijiye na."`) or formal without
  being especially polite (`"Rate fixed hai."`).
- **Stance and emotion are separate fields on purpose.** Stance is the speaker's
  position toward the listener or situation; emotion is the speaker's own affective
  state. A speaker can be `DEFERENTIAL` in stance while `WORRIED` in emotion.
- `code_switch_function` uses `null` for monolingual Hindi items where no switch
  exists at all, and `NOT_APPLICABLE` for Hinglish items where English words appear
  but carry no discourse function. That distinction is deliberate and is checked
  against `language` during review.
- When `primary_phenomenon` is `CODE_SWITCHING`, `language` must be `Hinglish` and
  `code_switch_function` must name a real function — not `NOT_APPLICABLE` or `null`.

---

## 4. Context metadata

| Field | Type | Req. | Allowed values |
|---|---|---|---|
| `context_required` | boolean | yes | `true`, `false` |
| `context_status` | string | yes | `NOT_REQUIRED`, `HELPFUL`, `REQUIRED` |
| `minimum_context_window` | integer | yes | 0 to 3 |
| `relevant_context_turns` | array of integers | yes | turn IDs present in `context` |
| `context_explanation` | string | yes | may be empty only when `NOT_REQUIRED` |

`context_status` is the primary judgement:

| Value | Meaning |
|---|---|
| `NOT_REQUIRED` | The utterance is fully interpretable on its own |
| `HELPFUL` | Context resolves references or adds confidence, but the pragmatic reading survives without it |
| `REQUIRED` | Without the context the intended pragmatic reading is not recoverable |

`context_required` is the boolean form of the same judgement: `true` exactly when
`context_status` is `REQUIRED`.

`minimum_context_window` is the smallest number of preceding turns that should be
supplied for the intended reading to be available. It is `0` when
`context_status` is `NOT_REQUIRED`, and at least `1` when it is `REQUIRED`. It may
never exceed the number of turns actually present in `context`.

`relevant_context_turns` names which turns carry the disambiguating information.
It must be non-empty when `context_status` is `REQUIRED`, and every entry must be a
`turn_id` that exists in `context`.

*Annotation note:* the honest test for `REQUIRED` is to cover the context and read
the source utterance alone. If a competent speaker would arrive at a different
pragmatic reading, the item is `REQUIRED`. If they would arrive at the same reading
but with less confidence, it is `HELPFUL`.

---

## 5. Translation data

| Field | Type | Req. | Allowed values |
|---|---|---|---|
| `preservation_requirement` | string | yes | non-empty |
| `reference_translations` | array of strings | yes | at least one, each non-empty |
| `acceptable_variants` | array of strings | yes | may be empty |
| `contrastive_translation` | string | yes | non-empty |
| `contrastive_error` | string | yes | non-empty |
| `contrastive_error_category` | string | yes | `POLITENESS_ERROR`, `FORMALITY_ERROR`, `SPEECH_ACT_ERROR`, `STANCE_ERROR`, `EMOTION_ERROR`, `INDIRECTNESS_ERROR`, `CODE_SWITCH_ERROR`, `RELATIONSHIP_ERROR` |
| `severity` | string | yes | `MINOR`, `MAJOR`, `CRITICAL` |

### `preservation_requirement`

A plain statement of what an acceptable translation must preserve, written so that
it could be handed to a translator as an instruction. It should name the pragmatic
property at risk, not restate the propositional content.

Good: *"The translation must remain a deferential request from a student to a
professor. It must not become a demand."*

Bad: *"The translation must say that the student wants two more days."* — that is
semantic content, which is not what this benchmark measures.

### `reference_translations` and `acceptable_variants`

`reference_translations` holds translations judged pragmatically correct; at least
one is required. `acceptable_variants` holds further renderings that are also
acceptable but are not the primary reference. Both are used when scoring
open-ended translation output; only `reference_translations[0]` is used when
building contrastive pairs.

### `contrastive_translation`

A semantically close but pragmatically wrong translation. Full construction rules
are in [contrastive_item_guidelines.md](../guidelines/contrastive_item_guidelines.md).
Validation rejects a contrastive translation that is identical to any accepted
translation.

### `contrastive_error` and `contrastive_error_category`

`contrastive_error` explains in prose exactly what social or communicative meaning
breaks. `contrastive_error_category` names the single dimension that breaks. If
more than one dimension breaks, the contrastive item is targeting too much at once
and should be narrowed.

---

## 6. Annotation metadata

| Field | Type | Req. | Allowed values |
|---|---|---|---|
| `creator_notes` | string | yes | may be empty |
| `annotator_notes` | string | yes | may be empty |
| `annotator_ids` | array of strings | yes | may be empty |
| `adjudicator_id` | string or null | yes | `null` when no adjudication has happened |
| `agreement_status` | string | yes | `NOT_ANNOTATED`, `IN_PROGRESS`, `AGREED`, `DISAGREED`, `ADJUDICATED` |
| `annotation_version` | string | yes | non-empty, e.g. `"1"` |

**Never put real personal information in these fields.** `annotator_ids` and
`adjudicator_id` take pseudonymous identifiers only, such as `ANN_01` or `ADJ_01`,
and the mapping from identifier to person is kept outside this repository.

| `agreement_status` | Meaning |
|---|---|
| `NOT_ANNOTATED` | No annotator has rated this item |
| `IN_PROGRESS` | Fewer than the required number of annotators have finished |
| `AGREED` | Annotators agreed within tolerance |
| `DISAGREED` | Annotators disagreed and adjudication is pending |
| `ADJUDICATED` | A disagreement was resolved or explicitly preserved |

*Annotation note:* `creator_notes` is the right place to record uncertainty at
drafting time — a suspected regional dependence, a minimal-pair partner ID, or a
severity judgement the creator is unsure about. It is read during review.

---

## 7. Complete example

```json
{
  "schema_version": "0.1.0",
  "item_id": "HIN_POL_001",
  "language": "Hindi",
  "language_variety": "Standard Hindi (romanized)",
  "translation_direction": "Hindi-English",
  "source_type": "ELICITED",
  "source_reference": null,
  "license": "TO_BE_CONFIRMED",
  "review_status": "NEEDS_NATIVE_REVIEW",
  "context": [
    {"turn_id": 1, "speaker_id": "A", "speaker_role": "Professor",
     "text": "Yeh assignment kal shaam tak jama kar dijiye."}
  ],
  "source_utterance": {"turn_id": 2, "speaker_id": "B", "speaker_role": "Student",
     "text": "Sir, kya mujhe do din aur mil sakte hain?"},
  "literal_gloss": "Sir, can I get two more days?",
  "listener_role": "Professor",
  "relationship": "ACADEMIC",
  "relative_status": "SPEAKER_LOWER",
  "familiarity": "LOW",
  "primary_phenomenon": "POLITENESS_FORMALITY",
  "secondary_phenomena": ["FORMALITY", "SPEECH_ACT"],
  "speech_act": "REQUEST",
  "politeness_level": "RESPECTFUL",
  "formality_level": "FORMAL",
  "stance": "DEFERENTIAL",
  "emotion": "WORRIED",
  "indirectness": "MODERATELY_INDIRECT",
  "code_switch_function": null,
  "context_required": false,
  "context_status": "HELPFUL",
  "minimum_context_window": 1,
  "relevant_context_turns": [1],
  "context_explanation": "The professor's instruction establishes that the student is asking to move a deadline the professor has just set.",
  "preservation_requirement": "The translation must remain a deferential request from a student to a professor. It must not become a demand or a statement of intent.",
  "reference_translations": ["Sir, could I please have two more days?"],
  "acceptable_variants": ["Sir, may I have two more days?"],
  "contrastive_translation": "I need two more days.",
  "contrastive_error": "A deferential request becomes a flat statement of need addressed to a superior.",
  "contrastive_error_category": "POLITENESS_ERROR",
  "severity": "MAJOR",
  "creator_notes": "Politeness load sits in 'Sir' plus the interrogative frame.",
  "annotator_notes": "",
  "annotator_ids": [],
  "adjudicator_id": null,
  "agreement_status": "NOT_ANNOTATED",
  "annotation_version": "1"
}
```

A field-by-field walkthrough of real items is in
[../examples/example_explanations.md](../examples/example_explanations.md).

---

## 8. Validating an item

```bash
python scripts/validate_schema.py
python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl
```

`validate_jsonl.py` enforces the JSON Schema plus the cross-field rules described
above: item-ID coherence, context turn references, context-status coherence,
provenance requirements, duplicate IDs, and contrastive translations that are not
actually different from the reference.
