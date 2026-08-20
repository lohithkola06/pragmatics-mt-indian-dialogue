# Schema Version History

The schema version is recorded on every item in the `schema_version` field, so a
dataset file always states which schema it was written against.

Versioning follows `MAJOR.MINOR.PATCH`:

- **MAJOR** — a change that invalidates existing items (a field removed or
  renamed, an enum value removed, a field made required).
- **MINOR** — a backward-compatible addition (a new optional field, a new enum
  value).
- **PATCH** — documentation or description changes only; no validation behaviour
  changes.

---

## `0.1.0` — Week 2, first machine-readable schema

**Status:** current. Used by `benchmark/pilot/pilot_items_v1.jsonl`.

The first version expressed as a JSON Schema (draft 2020-12). It turns the prose
item schema in [benchmark_blueprint.md §7](../../docs/project/benchmark_blueprint.md)
into something validation can enforce, and settles several questions the blueprint
had left open.

### Decisions taken relative to the blueprint

The blueprint remains the design authority. Where this schema differs, it is
because Week 2 had to resolve an open question in order to produce a validating
dataset. Each difference is listed so the divergence is deliberate and traceable.

| Field | Blueprint | `0.1.0` | Reason |
|---|---|---|---|
| `primary_phenomenon` | fine-grained (`POLITENESS`) | four category values: `POLITENESS_FORMALITY`, `INDIRECT_REQUEST_REFUSAL`, `STANCE_EMOTION`, `CODE_SWITCHING` | Makes the field align one-to-one with the four benchmark categories and with the `item_id` category codes, so the two can be cross-checked |
| `source_type` | lowercase `elicited` | uppercase enum | Consistency with every other controlled vocabulary in the schema |
| `politeness_level` | 6 values including `POLITE` | `HIGHLY_RESPECTFUL`, `RESPECTFUL`, `NEUTRAL`, `FAMILIAR`, `DISRESPECTFUL`, `NOT_APPLICABLE` | `POLITE` and `RESPECTFUL` were not reliably separable. Week 1 recorded the number of politeness levels as an open question; this is the provisional answer, to be tested in the pilot |
| `formality_level` | 4 values | + `NOT_APPLICABLE` | Needed for utterances whose register cannot be judged |
| `stance` | 11 values | + `NEUTRAL` | The blueprint had no way to record the absence of a stance |
| `indirectness` | 3 values | + `NOT_APPLICABLE` | Needed for utterances that perform no act whose directness can be judged |
| `code_switch_function` | 9 values | + `NOT_APPLICABLE`, and `null` permitted | Distinguishes monolingual items (`null`) from code-mixed items whose switching is not pragmatic (`NOT_APPLICABLE`) |
| `speech_act` | 15 values | + `INDIRECT_REFUSAL`, `INFORMATION`, `QUESTION` (18) | Indirect refusals are a headline category and needed their own value; `INFORMATION` and `QUESTION` were needed for ordinary turns |
| context necessity | `context_required` boolean | boolean retained, plus `context_status` (`NOT_REQUIRED` / `HELPFUL` / `REQUIRED`) and `context_explanation` | The three-way judgement was specified in the blueprint's task list but had no field. The boolean is kept for compatibility and is required to agree with the enum |
| — | — | added `schema_version`, `review_status`, `license`, `creator_notes`, `agreement_status`, `annotation_version`, `adjudicator_id`, `annotator_ids` | Provenance and review state had to be machine-readable to keep unvalidated items from being mistaken for approved ones |

### Structural decisions

- **Source-speaker fields live inside `source_utterance`.** The blueprint's own
  example nests `speaker_id` and `speaker_role` in the utterance object, and
  duplicating them at item level would create two places to disagree. The item
  level carries `listener_role`, `relationship`, `relative_status` and
  `familiarity`.
- **`context` holds 0 to 3 turns.** Zero is permitted for genuinely
  context-independent items; the blueprint's stated range is 0 to 3.
- **Cross-field rules are split between two layers.** The JSON Schema carries four
  conditional rules (context-status coherence, code-switching coherence, provenance
  requirements). Rules that read more clearly as code — turn-reference validity,
  ID-to-label coherence, duplicate detection — live in
  `scripts/validate_jsonl.py`. This keeps the schema readable, as the blueprint
  asks, without losing the checks.

### Known open questions carried into the pilot

These are recorded rather than resolved. The pilot exists partly to answer them.

1. Are five politeness levels the right granularity, or should `HIGHLY_RESPECTFUL`
   and `RESPECTFUL` be merged?
2. Are `stance` and `emotion` separable reliably enough by two annotators to
   justify two fields?
3. Is `CODE_SWITCHING` testable at all when the target language is English, given
   that the switch cannot survive into a monolingual English translation? Several
   pilot items depend on preserving the *footing shift* rather than the switch
   itself. **Supervisor decision: keep the category.** The question is not closed
   so much as converted into a measurement: agreement on `code_switch_preservation`
   in the pilot is the test, and poor agreement there would reopen it for `0.2.0`.
   See [../pilot/pilot_issues.md](../pilot/pilot_issues.md), Issue 4.
4. Does the `TEASING` / `INSULT` boundary produce usable agreement?
5. Is `relationship` as a coarse enum sufficient, or does it need to be free text?

**Resolved outside the schema.** The target English variety is now **Indian
English** (supervisor decision). It does not change any schema field, but it sets
the standard evaluators judge naturalness against; see
[../../docs/project/language_scope_decision.md](../../docs/project/language_scope_decision.md)
and Issue 10 in the issues log.

Findings go to [../pilot/pilot_issues.md](../pilot/pilot_issues.md), and any
resulting change is released as `0.2.0`.

---

## Changing the schema

1. Edit `item_schema.json`.
2. Run `python scripts/validate_schema.py` to confirm the schema is still valid.
3. Update this file with the new version and what changed.
4. Update [annotation_schema.md](annotation_schema.md) and
   [label_definitions.md](label_definitions.md) to match.
5. Bump `schema_version` on every affected item.
6. Re-run `python scripts/validate_jsonl.py` on every dataset file.
7. Run `python -m unittest discover scripts/tests`.

A schema change that is not accompanied by a re-validation of the datasets is not
finished.
