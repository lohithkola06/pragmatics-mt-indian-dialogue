# Week 2 Progress

## Project Title

**Pragmatics-Preserving Machine Translation for Indian Dialogue**

A running log of what I actually did against [week_2_plan.md](week_2_plan.md), the
decisions I had to make, and the problems I ran into.

---

## Day 1 — Language scope

**Done.**

I finalized the language setting as Hindi and naturally occurring Hinglish to
English, and wrote it up in
[language_scope_decision.md](../../project/language_scope_decision.md).

**Decisions I had to make:**

- **Hindi and Hinglish are two values, not one.** I nearly merged them for
  simplicity. Keeping them separate means I can report on monolingual and
  code-mixed input separately, which is a research question rather than
  bookkeeping.
- **Romanized Latin script throughout.** This follows the worked examples already
  in the blueprint, matches how Hindi is typed in chat, and lets Hindi and Hinglish
  be compared directly. The cost is real: most MT systems are trained on
  Devanagari, so results may understate system quality. I recorded that rather than
  glossing over it.
- **Telugu deferred.** The binding constraint is not schema work — it is having two
  Telugu native-speaker annotators. I wrote down what a Telugu extension would
  need, including the open question of whether Telugu's honorific system maps onto
  the five politeness levels at all.

I made a point of stating explicitly that Hindi is not representative of Indian
languages generally. It would be easy to let the project title imply otherwise.

---

## Day 2 — Schema and labels

**Done.** Schema `0.1.0`: 43 properties, all required, 19 controlled-vocabulary
fields, 4 conditional rules.

**Decisions where I departed from the Week 1 blueprint:**

- **`primary_phenomenon` now takes the four category values** rather than
  fine-grained ones. This lets it be cross-checked against the item ID's category
  code, so an item whose ID contradicts its own labels gets rejected.
- **Dropped `POLITE` from the politeness scale.** `POLITE` and `RESPECTFUL` were
  not reliably separable. Week 1 flagged politeness granularity as open; this is a
  provisional answer, not a validated one, and the pilot should test it.
- **Added `context_status`** as a three-way enum alongside the existing boolean.
  The blueprint specified the three-way judgement in its task list but never gave
  it a field.
- **`null` versus `NOT_APPLICABLE` for `code_switch_function`.** `null` for
  monolingual Hindi where no switch exists; `NOT_APPLICABLE` for Hinglish where a
  switch exists but does no pragmatic work. That distinction turned out to matter a
  lot when writing the items.

Every deviation is recorded with its reason in
[schema_version.md](../../../benchmark/schema/schema_version.md). I did not want
silent divergence from Week 1.

**Judgement call:** I split cross-field validation between two layers. Four
conditional rules live in the JSON Schema; the rest — turn references, ID coherence,
duplicate detection — live in `validate_jsonl.py`. Expressing all of it in JSON
Schema was possible but would have made it unreadable, and the blueprint asks for
the schema to stay understandable.

---

## Day 3 — Guidelines

**Done.** Five documents in `benchmark/guidelines/`.

The annotation guidelines cover all fifteen required topics. The section I spent
most effort on is **judging contrastive translations**, because the most damaging
failure mode is invisible to automation: a contrastive translation that is simply
another acceptable rendering. An item built on one measures nothing and actively
penalises a system for translating well. I made catching that the single most
valuable judgement an annotator can give.

I also wrote the adjudication guidelines around *preserving* disagreement rather
than resolving it. Where regional norms differ, forcing consensus would make the
benchmark look more reliable than it is and would hide the variation the project is
supposed to document.

---

## Days 4 and 5 — Pilot items

**Done.** 47 items in
[pilot_items_v1.jsonl](../../../benchmark/pilot/pilot_items_v1.jsonl).

I first wrote 40 items, hitting the planned distribution exactly (12/12/10/6, 22
Hindi, 18 Hinglish). On Day 7 I added seven more to fix a control-group gap I found
during internal review — see the Day 7 note below. Final distribution:

| | Planned | First draft | Final |
|---|---|---|---|
| Politeness and formality | 12 | 12 | 14 |
| Indirect requests and refusals | 12 | 12 | 14 |
| Stance and emotion | 10 | 10 | 12 |
| Code-switching | 6 | 6 | 7 |
| Hindi | ~22 | 22 | 26 |
| Hinglish | ~18 | 18 | 21 |
| `ELICITED` | majority | 28 (70%) | 35 (74.5%) |
| `MINIMAL_PAIR` | substantial minority | 12 (30%) | 12 (25.5%) |

The additions preserved the category proportions almost exactly — 29.8% / 29.8% /
25.5% / 14.9% against a 30/30/25/15 target — and the language split moved only from
55.0/45.0 to 55.3/44.7.

**No `NATURAL` or `ADAPTED` items.** I could not document provenance or verify
licensing this week, and inventing a source would have been fabrication. Zero
natural items is an honest state; fake citations would not be.

**Things I deliberately built in:**

- **Failures in both directions.** Some contrastive translations are too blunt,
  others too formal. If every item punished bluntness, a system could score well by
  always maximising politeness.
- **A negative control for code-switching** (`HNG_CSW_003`), where the English is
  ordinary technical vocabulary and the correct label is that the switch does no
  pragmatic work. Without it I would be training annotators to over-read every
  English token.
- **Six minimal pairs** isolating one feature each — `aap`/`tum`, respectful/
  familiar imperatives, direct/indirect refusal.
- **Distinct functions for every code-switching item** — authority, emotional
  intensity, technical terminology, intimacy, sarcasm, quotation, and a second
  authority case — rather than variations on one phenomenon.

All 47 carry `review_status: NEEDS_NATIVE_REVIEW`, `source_reference: null`,
`license: "TO_BE_CONFIRMED"`, empty annotator fields, and
`agreement_status: "NOT_ANNOTATED"`.

---

## Day 6 — Tooling, validation, internal review

**Done.** Five scripts, 41 tests, three CSV templates, statistics report.

**Two problems the tooling caught in my own work:**

1. **`HNG_CSW_003`'s contrastive translation was invalid.** It differed from the
   reference only by capitalisation (`ARRAY INDEX` versus `array index`). The
   validator flagged it as effectively identical to an accepted translation, and it
   was right — a capitalisation-only difference is typographic, not pragmatic. I
   rewrote it to add `so-called` and scare quotes, which treats routine technical
   borrowing as marked usage. That is a real pragmatic error.

2. **A broken conversational flow in `HIN_STA_005`.** The senior colleague asked
   "Kya hua?" and then answered themselves two turns later without the junior
   replying. I changed turn 2 so the junior continues.

Neither would have been caught by reading the file. This is the argument for
building the validator before finishing the data.

**A correctness problem in my own test.** I wrote a test asserting Krippendorff's
alpha of 0.743 for a three-observer example, and it failed at 0.675. Rather than
adjust the implementation to match my expectation, I computed the coincidence
matrix by hand: marginals n₁=5, n₂=10, n₃=8, n₄=3, n₅=2, n=28, giving D_o = 7 and
D_e = (28² − 202)/27 = 21.556, so α = 1 − 7/21.556 = **0.675**. The implementation
was right and my recalled figure was from a different dataset. I fixed the test and
recorded the derivation in the docstring so it is verifiable rather than a magic
number.

**Environment note.** The default `python3` here is 3.9.10 and has `jsonschema`
installed; the 3.11 interpreter on this machine does not. I wrote every script with
`from __future__ import annotations` so they run on 3.9 and later, and documented
in the scripts README that `jsonschema` must be installed for whichever interpreter
is used.

---

## Day 7 — Pilot preparation, issues, documentation

**Done.** Pilot plan, issues log, READMEs, example walkthroughs, root README
update, Week 2 planning documents.

I wrote [pilot_issues.md](../../../benchmark/pilot/pilot_issues.md) before any
human review, recording twelve problems I already know about. The ones that worry
me most:

- **Only one `NOT_REQUIRED` item** out of 40. Without a decent set of
  context-independent controls, I cannot separate a context-aware system's
  advantage from its general capability. I also suspect I over-applied `REQUIRED`.
  **I fixed the first half of this** — see the revision note at the end of Day 7.
  The over-application worry is unresolved and is a job for reviewers.
- **Code-switching may not be testable with an English target.** The switch cannot
  survive into monolingual English. The six items test whether the *footing shift*
  survives, which may be a fair test or may be asking for something English cannot
  mark. I recorded it as an open question rather than pretending it works.
- **Severity is skewed** — 31 of 40 were `MAJOR` at this point, and 37 of 47 after
  the revision below, so the skew persists. That makes the severity-weighted
  score behave close to a raw count.
- **Every item has one author.** Sources, references and contrastive translations
  all came from the same process, so systematic blind spots would be invisible
  within the dataset.
- **Nobody has decided which variety of English the benchmark targets.** Indian
  English politeness conventions differ from British and American ones, and this
  affects every reference translation. I only noticed this while writing the issues
  log.

### Revision: fixing the context control group

Having written the issues log, I went back and fixed the first one rather than
leaving it for `v2`. A single context-independent item out of 40 is not a control
group, and without one the whole context-benefit comparison — which is a headline
research question — cannot be made.

I added seven items, taking the pilot to 47 and the control group to 8 (17.0%).

**The constraint that shaped them.** My own annotation guidelines define `HELPFUL`
as context that "resolves references or adds confidence". That means an utterance
containing deixis pointing back at a previous turn is `HELPFUL` by definition, not
`NOT_REQUIRED` — so I could not simply attach irrelevant context to an existing
item. Each new item has **zero context turns** and has to carry its pragmatic load
internally.

That turned out to be a useful discipline, because it forced me to find phenomena
that are self-contained by their nature:

- honorific morphology alone (`Aunty ji, aap yahan baith jaiye.`)
- an agentless construction that softens criticism without context
  (`Is report par thoda aur mehnat karni padegi.`)
- discourse particles carrying warmth (`Arre, apna khayal rakha karo thoda.`)
- **conventional indirectness** (`Kya aap khidki band kar sakte hain?`) — an
  ability question is a request by convention rather than by context, which makes
  it exactly the right control against the highly context-dependent indirect items
- a Hindi frame around an English rule, so the code-switch contrast sits inside one
  utterance rather than depending on an English context turn

I kept the category and language proportions intact, and I rated the new items'
severity on their merits rather than to correct the existing skew — six came out
`MAJOR` and one `MINOR`, which nudged the skew slightly the wrong way. Assigning
them `MINOR` to flatten the distribution would have been rating to a target, which
is the exact calibration error my own severity guidelines warn against. The skew
stays as an honest finding for reviewers.

**Still open from the same issue:** `REQUIRED` remains the largest class at 46.8%
and may still be over-applied. That half needs native speakers applying the
cover-the-context test, not more items from me.

---

## Verification results

Run from the repository root.

| Command | Result |
|---|---|
| `python scripts/validate_schema.py` | Pass — valid draft 2020-12 schema |
| `python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl` | Pass — 47 read, 47 valid, 0 invalid |
| `python scripts/validate_jsonl.py benchmark/examples/example_items.jsonl` | Pass — 4 read, 4 valid, 0 invalid |
| `python -m unittest discover scripts/tests` | Pass — 41 tests |
| `python scripts/generate_dataset_statistics.py …` | Pass — distribution matches target |
| `python scripts/create_annotation_sheet.py …` | Pass — 94 candidate rows from 47 items |
| `python scripts/calculate_agreement.py <un-annotated sheet>` | Correctly reports insufficient data |

The last row is the one I most wanted to confirm. The agreement script refuses to
estimate a figure when no annotation exists, which is the state it should be in
this week.

---

## Where the week ended up against the plan

| Planned | Status |
|---|---|
| Finalize language scope | Done |
| Finalize schema and labels | Done |
| Annotation and contrastive guidelines | Done |
| First half of pilot items | Done |
| Second half of pilot items | Done |
| Validate, annotation sheets, internal review | Done |
| Native-review preparation, issues, summary | Done |

Nothing slipped. What is *not* done is everything requiring a person, which was
never in scope for this week.

---

## What I still need

**Native speakers**, for: naturalness of the 47 sources, validity of the 47
contrastive translations, independent severity re-rating, re-checking the
`REQUIRED` context labels, and Stage 2 rating so agreement can finally be measured.

**A supervisor decision**, on: whether the code-switching category is well-posed
with an English target, which variety of English to target, whether to source
natural dialogue and from where, and whether five politeness levels is right.

**Recruitment**, of two annotators plus one adjudicator, ideally with different
regional backgrounds — otherwise region-dependence is undetectable.

---

## My next step

Recruit annotators and run Stage 1 item review before any rating. Reviewing first
means annotator effort is not spent rating items that are going to be rejected, and
annotator time is the scarcest resource on this project.

I am not running translation baselines until the benchmark has been validated.
Baseline numbers against an unvalidated benchmark would not mean anything.
