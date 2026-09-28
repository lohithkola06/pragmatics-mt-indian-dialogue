# Pilot Issues Log

Known problems, limitations and open questions in
[pilot_items_v1.jsonl](pilot_items_v1.jsonl).

**Two kinds of entry:**

- **Issues found during construction** (sections 1–3) — recorded now, before any
  human review, so that reviewers know what is already suspected.
- **Issues found during review** (section 4) — empty, because no human review has
  taken place.

> The entire dataset carries `review_status: NEEDS_NATIVE_REVIEW`. Everything
> below is a *self-assessment by the process that wrote the items*, which is
> exactly the kind of assessment that most needs independent checking.

---

## 1. Composition issues

### Issue 1 — Thin context-independent control group

**Severity:** high → medium
**Status:** partly addressed; the `REQUIRED` half remains open

**As first recorded.** Context status was distributed 22 `REQUIRED` / 17 `HELPFUL`
/ 1 `NOT_REQUIRED` across 40 items. A single `NOT_REQUIRED` item (`HNG_POL_002`) is
too thin a control group: to show that context-aware translation helps *because of
context*, the benchmark needs items where context demonstrably does not matter,
otherwise a context-aware system's advantage cannot be separated from its general
capability.

**Action taken.** Seven context-independent items were added, bringing the pilot to
47 items and the control group to 8:

| | Before | After |
|---|---:|---:|
| `REQUIRED` | 22 (55.0%) | 22 (46.8%) |
| `HELPFUL` | 17 (42.5%) | 17 (36.2%) |
| `NOT_REQUIRED` | 1 (2.5%) | 8 (17.0%) |

The new items are `HIN_POL_009`, `HNG_POL_005`, `HIN_IND_009`, `HIN_IND_010`,
`HIN_STA_007`, `HNG_STA_005` and `HNG_CSW_007`. Category and language proportions
were preserved: 14/14/12/7 across the four categories (29.8% / 29.8% / 25.5% /
14.9%) and 26 Hindi to 21 Hinglish (55.3% / 44.7%).

**How they were built.** All seven have **zero context turns**, not merely context
that happens to be unnecessary. This follows from the definition in the annotation
guidelines: `HELPFUL` covers context that "resolves references or adds confidence",
so an utterance containing deixis pointing back at a previous turn is `HELPFUL`
by definition, not `NOT_REQUIRED`. Each new item therefore has to carry its
pragmatic load internally:

- `HIN_POL_009` — honorific morphology (`aunty ji`, `aap`, `-iye`) alone
- `HNG_POL_005` — a call-opening formula that refers to nothing prior
- `HIN_IND_009` — *conventional* indirectness: an ability question is a request by
  convention rather than by context
- `HIN_IND_010` — an agentless `padegi` construction that softens without context
- `HIN_STA_007` — discourse particles (`arre`, habitual `rakha karo`, `thoda`)
- `HNG_STA_005` — a general reassurance formula plus the solidarity marker `yaar`
- `HNG_CSW_007` — a Hindi frame around an English rule, so the switch contrast sits
  inside one utterance

`HIN_IND_009` is worth singling out: conventional indirectness is precisely the
kind of pragmatic force that does *not* need context, which makes it a good control
against the highly context-dependent indirect items.

**Still open.** The second half of this issue is untouched. `REQUIRED` remains the
largest class at 46.8%, and it may still be over-applied — the bar is that the
pragmatic reading *changes* without context, not that context is useful. Reviewers
should re-check every `REQUIRED` label against the cover-the-context test.

**Also not covered.** A distinct control type is missing: items where context is
*present but pragmatically irrelevant*, which would test whether a system is misled
by unhelpful context. Agrawal et al. (2024) found that corrupted or swapped context
degrades metric correlation, so this is a real failure mode. It is not covered here
because writing dialogue whose previous turn is genuinely irrelevant, without it
becoming artificial, needs native-speaker authorship.

### Issue 2 — Severity distribution is heavily skewed

**Severity:** medium
**Status:** open, and slightly worse after the Issue 1 additions

37 of 47 items are `MAJOR` (78.7%), with 7 `MINOR` (14.9%) and 3 `CRITICAL` (6.4%).

The seven items added to fix Issue 1 were rated on their merits — six `MAJOR`, one
`MINOR` — which nudged the skew up from 77.5% rather than down. Assigning them
`MINOR` to flatten the distribution would have been rating to a target, which is
exactly the calibration error the severity guidelines warn against. The skew is
left as an honest finding.

This gives annotators little calibration range, and it makes the
severity-weighted error score (`MINOR`=1, `MAJOR`=5, `CRITICAL`=10) insensitive:
with most items at one weight, the metric behaves close to a raw count.

The skew probably reflects a drafting habit rather than reality — `MAJOR` is the
comfortable middle choice.

**Proposed action:** reviewers should re-rate severity independently, without
seeing the assigned label. A more even spread is expected after review.

**In place:** the Stage 1 review form hides each item's assigned severity and asks
for the reviewer's own rating, exported as the `reviewer_severity` column. Comparing
that column with the assigned `severity` is the re-rating.

### Issue 3 — No naturally occurring items

**Severity:** medium
**Status:** open, deliberate

All 47 items are `ELICITED` or `MINIMAL_PAIR`. There are no `NATURAL` or `ADAPTED`
items, because their provenance could not be documented and their licensing could
not be verified. Adding them with invented sources would have been fabrication.

The consequence is real: elicited dialogue written to target a phenomenon tends to
be cleaner and more phenomenon-typical than real conversation. The blueprint's own
risk list names artificial-sounding examples as a failure mode.

**Proposed action:** Week 3 work on sourcing openly licensed conversational or
subtitle data, with licence checks recorded before any item is added.

---

## 2. Design questions the pilot should answer

### Issue 4 — Is code-switching testable with an English target?

**Severity:** high
**Status:** RESOLVED — keep the category. Testability is now a pilot measurement.

A Hindi–English switch cannot survive into a monolingual English translation. The
seven `CSW` items therefore do not test whether the *switch* is preserved — they
test whether the **footing shift the switch performed** survives: authority,
intimacy, irony, quotative framing.

That may be a fair test. It may also be asking translators to preserve something
English has no direct means of marking, in which case low scores would reflect a
limitation of the target language rather than a system failure.

`HNG_CSW_004` is the clearest case: the switch is only perceptible *because* the
context turn is in English.

**Decision (supervisor).** Keep the code-switching category. The conceptual worry
above does not go away, so it is converted from a go/no-go question into something
the pilot measures directly: the test is whether annotators can score
`code_switch_preservation` on the footing shift with acceptable agreement. If
agreement on that dimension is poor while it is acceptable elsewhere, that is
evidence the category is not well-posed against an English target, and it gets
revisited for `0.2.0` (options then would be narrowing to functions English can
express, such as sarcasm and quotation, or adding a Hindi-target condition). For
now nothing in the dataset changes; the seven items stand as written.

### Issue 5 — Politeness granularity is untested

**Severity:** medium
**Status:** open

Schema `0.1.0` dropped the blueprint's `POLITE` level, leaving five substantive
values. Week 1 recorded the number of politeness levels as an open question, and
this was a provisional answer, not a validated one.

`HIGHLY_RESPECTFUL` and `RESPECTFUL` may not be reliably separable.

**Proposed action:** measure agreement on `politeness_level` specifically. If it is
poor, merge the two.

### Issue 6 — Stance/emotion separability is untested

**Severity:** medium
**Status:** open

The schema records stance and emotion as separate fields on the argument that they
come apart. That is defensible in principle, but whether two annotators apply the
distinction *consistently* is unknown.

**Proposed action:** report per-dimension agreement for `stance` and `emotion`
separately. If either is much worse than the other, or if annotators' notes show
them being conflated, reconsider the split.

### Issue 7 — The teasing/insult boundary

**Severity:** medium
**Status:** open, may be irreducible

`HIN_STA_001` and `HNG_STA_001` both rest on the judgement that mockery between
close friends is affectionate. This depends on relationship, familiarity, region and
individual temperament.

This may be genuinely irreducible — in which case the right outcome is preserved
disagreement, not a resolved label.

**Proposed action:** treat splits here as `REGIONAL_VARIATION` or
`LABEL_DISAGREEMENT` and preserve them. If agreement is very low across the board,
consider whether the category can carry the weight the benchmark puts on it.

---

## 3. Construction limitations

### Issue 8 — Every item has a single author

**Severity:** high
**Status:** open

All 47 items — sources, glosses, references and contrastive translations — were
written by one process during repository construction. This creates several
correlated risks:

- **Naturalness is unverified.** No native speaker has confirmed that any source
  utterance is something a real person would say.
- **Systematic contrastive bias.** The same author wrote both the reference and the
  contrastive translation for every item. If that author has a consistent notion of
  what makes a translation "wrong", the contrastive set may test that notion rather
  than pragmatic failure in general.
- **Correlated blind spots.** A distinction the author does not perceive is absent
  from all 47 items, and nothing in the dataset would reveal it.

**Proposed action:** Stage 1 item review by two independent native speakers, before
any rating. For the full benchmark, items should be authored by more than one
person, and contrastive translations ideally written by someone other than the
person who wrote the reference.

### Issue 9 — Romanization only, no Devanagari

**Severity:** low
**Status:** open, deliberate

All source text is romanized Latin script, following the convention in the
benchmark blueprint and recorded in
[../../docs/project/language_scope_decision.md](../../docs/project/language_scope_decision.md).

This matches how Hindi is typically typed in chat and makes Hindi and Hinglish
directly comparable. But it excludes Devanagari input, which is what many MT
systems are actually trained on, and romanization is not standardised — spellings
here may not match what a given system expects.

**Proposed action:** consider adding an optional `source_devanagari` field in a
later schema version. Not blocking for the pilot.

### Issue 10 — The English of the reference translations is unexamined

**Severity:** medium
**Status:** RESOLVED — target variety is Indian English. References still need a
native pass to conform.

The reference translations use forms like "No man, I won't be able to make it" and
"Ha, that's exactly what I'd expect from you". These lean toward a general
informal English register.

Indian English has its own conventions for politeness, address and formality, and a
translation natural in Indian English may read as odd in British or American
English, and the reverse. Since the whole benchmark is about social meaning in
English output, this is not a cosmetic question.

**Decision (supervisor).** The benchmark targets **Indian English**. This is now
recorded as the target variety in
[../../docs/project/language_scope_decision.md](../../docs/project/language_scope_decision.md)
and evaluators are instructed to judge naturalness against it in
[../guidelines/human_evaluation_guidelines.md](../guidelines/human_evaluation_guidelines.md)
and [../guidelines/annotation_guidelines.md](../guidelines/annotation_guidelines.md).

**Still open.** The decision does not retroactively make the 47 existing references
Indian English. They were written by one non-native author in a general informal
register, and rewriting all of them into Indian English is a native-speaker task,
not something to do mechanically without risking caricature. So the references
carry forward as-is into Stage 1 review, where reviewers now have an explicit extra
criterion: is each reference natural **in Indian English**, and if not, supply an
Indian-English alternative. Conforming the reference set is expected output of the
pilot, not a precondition of it.

Alternatives are collected in their own column, `suggested_indian_english_reference`,
in the Stage 1 review export, rather than mixed into free-text notes.

### Issue 11 — Minimal pairs must not be split across data splits

**Severity:** low
**Status:** open, needs enforcement

The 12 `MINIMAL_PAIR` items form 6 pairs differing in one feature. Pair partners are
named in `creator_notes` but there is **no machine-readable pair identifier**, so
nothing stops a future split script separating them and leaking information between
development and test.

**Proposed action:** add a `pair_id` field in schema `0.2.0`, and have the split
script group on it.

### Issue 12 — Role and setting variety is narrow

**Severity:** low
**Status:** open

Settings cluster around workplace, academic and service interactions. Family
appears in only a few items, and there is little variation in age, and none in
formal institutional settings such as government offices or banks.

**Proposed action:** broaden the setting distribution in `v2`.

---

## 4. Issues found during human review

**Empty.** No human review has taken place.

This section will be filled in during pilot Stage 1 and Stage 2. Each entry should
record the item ID, the reviewer, what was found, and the disposition.

Suggested format:

```text
### Issue N - <short description>

**Items affected:** HIN_POL_003, HIN_POL_007
**Found by:** REV_01, REV_02
**Severity:** high | medium | low
**Status:** open | fixed in v2 | rejected | preserved as disagreement

<description, and what was done>
```

---

## 5. Summary of what needs human input

Ordered by how much the pilot depends on it:

| # | Needed | Who |
|---|---|---|
| 1 | Confirm the source utterances are natural | Native speakers |
| 2 | Confirm each contrastive translation is genuinely wrong in context | Native speakers |
| 3 | Conform the reference translations to Indian English (Issue 10) | Native speakers |
| 4 | Re-rate severity independently (Issue 2) | Native speakers |
| 5 | Score `code_switch_preservation`; low agreement flags Issue 4 | Measured from annotation |
| 6 | Re-check every `REQUIRED` context label (Issue 1) | Native speakers |
| 7 | Confirm or merge politeness levels (Issue 5) | Measured from annotation |
| 8 | Confirm stance/emotion separability (Issue 6) | Measured from annotation |
| 9 | Establish provenance for natural data (Issue 3) | Supervisor |

Two supervisor decisions have now been made: keep the code-switching category
(Issue 4), and target **Indian English** (Issue 10). Everything remaining above
needs people, and none of it has been done yet.
