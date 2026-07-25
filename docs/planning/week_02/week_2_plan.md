# Week 2 Plan

## Project Title

**Pragmatics-Preserving Machine Translation for Indian Dialogue**

---

## 1. What I Want to Achieve This Week

In Week 1 I settled the research direction, wrote the scope and research
questions, reviewed seven papers, and produced the benchmark blueprint. All of
that was planning. Nothing in the repository could actually be run.

This week I want to move from planning into **pilot benchmark construction**. By
the end of the week I want a repository where the schema is machine-readable, a
draft pilot dataset exists and validates, and a native speaker could be handed the
guidelines and start annotating without me explaining anything in person.

My one hard rule for the week: **I will not fabricate anything that requires a
human.** No invented agreement scores, no items marked as approved, no claimed
provenance for data I did not source. Where human input is missing, the repository
should say so plainly.

---

## 2. Day 1 — Finalize the Hindi and Hinglish language scope

Week 1 left the language question open. I need to close it before anything else,
because the schema, the item IDs and the pilot data all depend on it.

- Decide the language setting and write it up properly.
- Decide whether Hindi and Hinglish are one value or two. I am treating them as
  two, so that I can report on monolingual and code-mixed input separately.
- Define what counts as Hindi and what counts as Hinglish, precisely enough to
  label an item without guessing.
- Decide the script convention.
- Write down what is excluded and what the regional limitations are.
- Record how Telugu could be added later, and what would have to be true first.

**Deliverable:** `docs/project/language_scope_decision.md`

I must be careful not to claim that Hindi is representative of Indian languages
generally. It is not, and overclaiming here would undermine the whole project.

---

## 3. Day 2 — Finalize the annotation schema and labels

Turn the prose schema in the blueprint into something a machine can enforce.

- Write `benchmark/schema/item_schema.json` as a JSON Schema.
- Settle the controlled vocabularies. Week 1 left the politeness granularity open,
  so I need at least a provisional answer.
- Document every field: type, whether it is required, allowed values, an example,
  and a note on how to annotate it.
- Define every label with an example, the labels it gets confused with, and when
  not to use it.
- Write the severity guidelines with worked examples at each level.
- Record every place where I deviate from the blueprint, and why.

**Deliverables:** `item_schema.json`, `annotation_schema.md`,
`label_definitions.md`, `severity_guidelines.md`, `schema_version.md`

The schema must express the cross-field constraints, not just field types — for
example that a code-switching item has to actually name a switch function.

---

## 4. Day 3 — Write the annotation and contrastive-item guidelines

Write the documents a native speaker will actually work from. These have to stand
on their own, because I will not be sitting next to the annotator.

- Annotation guidelines covering the full task: semantic versus pragmatic meaning,
  reading context, identifying speech acts, separating politeness from formality
  and stance from emotion, judging indirectness and code-switching, labelling
  context requirement, judging references and contrastive translations, using the
  uncertainty labels, handling multiple valid readings, avoiding regional bias, and
  writing notes.
- Contrastive-item guidelines with the requirements and, importantly, examples of
  **invalid** contrastive items — including the one that is hardest to spot, where
  the contrastive translation is still perfectly acceptable.
- Adjudication guidelines that preserve genuine disagreement instead of forcing
  consensus.
- Human evaluation protocol using the 0–3 preservation scale.
- Training material with exercises.

**Deliverables:** the five files in `benchmark/guidelines/`

---

## 5. Day 4 — Create the first half of the pilot items

Write roughly the first 20 items, concentrating on politeness/formality and
indirect requests/refusals.

- Target 12 politeness/formality and 12 indirect request/refusal items overall.
  (Revised upward to 14 each on Day 7 — see the Day 7 note below.)
- Build minimal pairs where they isolate one feature cleanly — the `aap`/`tum`
  contrast, and the direct/indirect refusal contrast.
- For each item: context turns, source utterance, literal gloss, labels,
  preservation requirement, reference translation, contrastive translation,
  explanation, severity.
- Keep to ordinary, safe settings: student and professor, employee and manager,
  customer and support, family, friends, shopkeeper and customer. Doctor settings
  only for scheduling, never medical advice.
- Mark everything `NEEDS_NATIVE_REVIEW`, with `source_reference` null,
  `license: TO_BE_CONFIRMED`, empty annotator fields.

I want failures in **both directions** — items where the contrastive is too blunt
and items where it is too formal — so that a system cannot score well by always
being maximally polite.

---

## 6. Day 5 — Create the second half of the pilot items

Write the remaining items: stance and emotion, and code-switching.

- 10 stance/emotion items and 6 code-switching items.
- Give each code-switching item a distinct function, so the category is not just
  six copies of one phenomenon.
- Include at least one item where the English is ordinary borrowing and the correct
  label is `NOT_APPLICABLE`. If I only include meaningful switches, I will train
  annotators to over-read every English word.
- Check the totals against the target distribution: 40 items, about 22 Hindi and
  18 Hinglish, mostly elicited with a substantial minority of minimal pairs.
  (Revised to 47 items on Day 7 — see the Day 7 note below.)

**Deliverable:** `benchmark/pilot/pilot_items_v1.jsonl` with 40 items, revised to 47

---

## 7. Day 6 — Validate, prepare annotation sheets, and review internally

Build the tooling and use it to check my own work.

- `validate_schema.py` — confirm the schema is itself valid.
- `validate_jsonl.py` — validate every item, catch duplicate IDs, bad context
  references, empty fields, and items whose ID contradicts their labels.
- `generate_dataset_statistics.py` — check the distribution actually matches what
  I intended.
- `create_annotation_sheet.py` — produce a readable CSV, with a blind mode so
  annotators cannot see which candidate is the reference.
- `calculate_agreement.py` — percentage agreement, Cohen's kappa, Krippendorff's
  alpha. It must report insufficient data rather than inventing a number, because
  that is exactly the state it will be in this week.
- Tests for all of it.
- The three CSV templates.

Then review my own items critically and write down what is wrong with them. I
expect to find real problems, and recording them is more useful than pretending
the dataset is clean.

**Deliverables:** `scripts/`, `scripts/tests/`, CSV templates,
`pilot_statistics.md`

---

## 8. Day 7 — Prepare for native-speaker review, document open issues, summarize

- Write the pilot plan: objectives, annotator requirements, procedure, agreement
  measures, acceptance/revision/rejection criteria, timeline, deliverables.
- Write the issues log honestly, including the problems I already know about.
- Write the READMEs so someone can pick this up without me.
- Write the example walkthroughs.
- Update the root README with Week 2 status.
- Run the full verification pass and record the results.
- Write the Week 2 summary as a **template**, with completed repository work
  clearly separated from pending human annotation.

**Deliverables:** `pilot_plan.md`, `pilot_issues.md`, READMEs,
`example_explanations.md`, Week 2 planning documents

---

## 9. What I Am Explicitly Not Doing This Week

- **Running translation systems.** Baselines are Week 3 or later. Without a
  validated benchmark, baseline numbers would be meaningless.
- **Sourcing natural dialogue.** I cannot document provenance or verify licensing
  this week, so every pilot item will be elicited or a minimal pair. I would rather
  have zero natural items than items with invented sources.
- **Annotating my own items as if I were an independent annotator.** I wrote them;
  my agreement with myself measures nothing.
- **Adding Telugu.** The schema has to be validated on one language pair first.
- **Reporting any agreement figure.** No annotation will have happened.

---

## 10. How I Will Know the Week Succeeded

1. The language decision is written down and closed.
2. `python scripts/validate_schema.py` passes.
3. `python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl` passes
   for every item.
4. `python -m unittest discover scripts/tests` passes.
5. The statistics report confirms the intended distribution.
6. A native speaker could be handed `benchmark/guidelines/` and start work without
   me explaining anything verbally.
7. Every unvalidated claim in the repository is marked as unvalidated.
8. I have a written list of what still needs a human.

Point 7 matters as much as the rest. The value of this week is a repository that is
honest about its own state.

---

## 11. Risks I Am Watching

| Risk | Mitigation |
|---|---|
| I write items that sound artificial | Record it as a known limitation; native review is Stage 1 of the pilot |
| My contrastive translations all fail the same way | Record the risk explicitly; ask reviewers to check specifically for it |
| Code-switching turns out to be untestable with an English target | Record it as an open question rather than pretending it works |
| I over-apply `context_status: REQUIRED` | Define a strict test and check the distribution afterwards |
| I mark severity `MAJOR` by default | Check the distribution and flag the skew if it appears |

Every one of these is a case where the honest response is to document the problem
rather than paper over it.
