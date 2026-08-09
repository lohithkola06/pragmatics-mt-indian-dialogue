# Adjudication Guidelines

**For:** the adjudicator — a third annotator or the project lead — resolving
disagreements between annotators.

**Template:** [../pilot/pilot_adjudication_template.csv](../pilot/pilot_adjudication_template.csv)

The guiding principle of this document:

> **Do not force consensus where multiple interpretations are genuinely valid.**

Pragmatic meaning is often indeterminate. A disagreement can be a fact about the
language rather than a mistake by an annotator. Averaging those away would make the
benchmark look more reliable than it is and would hide exactly the phenomena we
are trying to study.

---

## 1. When adjudication is required

Adjudicate when:

- annotators differ by **two or more points** on the 0–3 preservation scale,
- annotators assign **different categorical labels** (different speech act,
  different politeness level, different stance),
- annotators differ on **severity by two levels** (`MINOR` versus `CRITICAL`),
- one annotator marks `MULTIPLE_VALID_INTERPRETATIONS` and the other gives a
  confident label,
- either annotator judges the item itself defective — unnatural source, acceptable
  contrastive, wrong primary label.

Do **not** adjudicate when:

- annotators differ by **one point** on the 0–3 scale. That is ordinary scale
  variation. Record it and move on.
- both marked `UNCERTAIN`. That is agreement — they agree the item is unclear.
  It is a signal about the item, not a disagreement to resolve.

---

## 2. How to compare annotator reasoning

Read the **notes before the scores.** The scores tell you that people differed; the
notes tell you why, and the why determines what to do.

For each disagreement, work out which kind it is:

| Type | Signature | Usual action |
|---|---|---|
| `LABEL_DISAGREEMENT` | Different categorical labels, both defensible | Decide, or preserve if both hold |
| `SCALE_DISTANCE` | Same direction, different magnitude | Take the middle or the better-argued value |
| `SCOPE_DISAGREEMENT` | Annotators judged different things — one rated the utterance, the other the whole exchange | Clarify the guidelines; re-annotate |
| `REGIONAL_VARIATION` | Notes cite different regional or community norms | **Preserve both.** Do not pick a standard |
| `GUIDELINE_GAP` | Neither annotator had a rule to apply | Fix the guidelines, then re-annotate |
| `ITEM_DEFECT` | The item is ambiguous, unnatural, or mislabelled | Revise or reject the item |

Record the type in the `disagreement_type` column. The distribution of types across
the pilot is itself a finding: many `GUIDELINE_GAP` entries mean the guidelines
need work, while many `ITEM_DEFECT` entries mean the item-creation process does.

**Judge the reasoning, not the annotator.** A well-argued minority reading beats a
confidently asserted majority one. Never resolve a disagreement by seniority or by
who annotated more items.

---

## 3. How to preserve disagreement

When both readings are genuinely valid, do not choose. Record:

- `item_action` = `KEEP_WITH_DISAGREEMENT`
- `adjudicator_decision` = the reading used as the primary label
- `final_labels` = the primary labels
- `reason` = both readings, stated explicitly, and what distinguishes them

The item stays in the benchmark with its disagreement documented. Downstream
analysis can then either exclude these items or report them separately, which is
only possible because the disagreement was kept.

Example:

```text
item_id                HIN_STA_001
annotator_1_decision   speech_act=TEASING
annotator_2_decision   speech_act=INSULT
disagreement_type      REGIONAL_VARIATION
adjudicator_decision   speech_act=TEASING
final_labels           speech_act=TEASING; stance=PLAYFUL
item_action            KEEP_WITH_DISAGREEMENT
reason                 Annotator 1 (Delhi) reads this as affectionate teasing
                       licensed by the close friendship in the context.
                       Annotator 2 reads it as a genuine reproach, noting that
                       the construction is sharper in their variety. Both are
                       defensible. TEASING is primary because the context
                       specifies close friends and a self-deprecating prior
                       turn, but the disagreement is real and is retained.
```

**Preserve disagreement especially for** teasing versus insult, sarcasm, warmth
versus dismissiveness, and any judgement whose notes mention region, age or
community. The blueprint commits the project to documenting dialect limitations and
to not presenting one interpretation as universal; this is where that commitment is
actually kept.

---

## 4. When to revise an item

Revise (`item_action` = `REVISE`) when the item tests something real but the
current form gets in the way:

- the context is too thin to support the intended reading — add a turn,
- the source utterance is natural but the intended act is ambiguous — adjust the
  context, not the utterance,
- the contrastive translation breaks more than one feature — narrow it,
- the primary label is wrong but the item is otherwise sound — relabel,
- the `context_status` is wrong — an item marked `REQUIRED` that both annotators
  read correctly without context is `HELPFUL`.

After revising: set `review_status` to `REVISED`, bump `annotation_version`, and
**re-annotate from scratch**. Do not reuse the ratings that prompted the revision;
they were made against a different item.

---

## 5. When to reject an item

Reject (`item_action` = `REJECT`) when the item cannot be fixed without becoming a
different item:

- **the contrastive translation is acceptable in context** — both annotators would
  send it. There is no error to detect.
- **the source utterance is not natural** — no native speaker would say it.
- **the intended reading requires an undocumented cultural assumption** that the
  context does not supply.
- **the pragmatic difference is not perceptible** to native speakers, even after
  the intent is explained.
- **the item duplicates another** so closely that it adds nothing.
- **provenance or licensing cannot be established** for a `NATURAL` or `ADAPTED`
  item.

Set `review_status` to `REJECTED`. **Keep the item in the repository** with the
rejection reason recorded. Rejected items document what was tried and stop the same
mistake being repeated; deleting them loses that.

---

## 6. Documenting the final decision

Every adjudication produces one row in the adjudication CSV:

| Column | Contents |
|---|---|
| `item_id` | The item |
| `annotator_1_decision` | The first annotator's label or rating, as `field=value` |
| `annotator_2_decision` | The second annotator's label or rating |
| `disagreement_type` | One of the six types in section 2 |
| `adjudicator_decision` | The resolved value, or the primary reading when preserving |
| `final_labels` | Every label that changes on the item, semicolon-separated |
| `item_action` | `KEEP`, `REVISE`, `REJECT`, or `KEEP_WITH_DISAGREEMENT` |
| `reason` | Why. Not optional |

**The `reason` must be able to stand on its own.** Someone reading it in six months,
without the conversation, should understand why the decision went the way it did.

Weak reason:

> "Annotator 1 was right."

Adequate reason:

> "Annotator 2 rated politeness_preservation=3 but the reference drops 'Sir',
> which is the only deference marker in the source. Annotator 1's rating of 1 is
> better supported by the text. Resolved to 1. No item change: the item is testing
> exactly this and is working as intended."

---

## 7. What the adjudicator must not do

- **Do not re-annotate the whole item.** You are resolving specific disagreements,
  not adding a third opinion to everything.
- **Do not resolve toward the item's original labels** because they are the
  creator's. If both annotators disagree with the creator, the creator was probably
  wrong.
- **Do not use adjudication to raise agreement statistics.** Agreement is measured
  on the *original independent* annotations, before adjudication. Adjudicating
  aggressively does not improve the reported figure, and treating it as if it did
  would be misreporting.
- **Do not adjudicate items you created**, where that can be avoided. Where it
  cannot, note it in the `reason`.

---

## 8. After adjudication

1. Update `agreement_status` on each adjudicated item to `ADJUDICATED`.
2. Set `adjudicator_id` to your pseudonymous identifier, never a real name.
3. Bump `annotation_version` on revised items.
4. Re-run validation:

   ```bash
   python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl
   ```

5. Recompute agreement on the **pre-adjudication** annotations:

   ```bash
   python scripts/calculate_agreement.py <completed annotation CSV>
   ```

6. Summarise the patterns in [../pilot/pilot_issues.md](../pilot/pilot_issues.md):
   which categories produced the most disagreement, which types dominated, and what
   should change in the schema or guidelines before the full benchmark is built.

Step 6 is the point of the pilot. The individual decisions matter less than what
the pattern of disagreement tells us about the design.
