# Language Scope Decision

**Decided:** Week 2
**Status:** finalized for the first benchmark release
**Supersedes:** the open question recorded in
[week_1_summary.md §15](../planning/week_01/week_1_summary.md) — "Should I use
Hindi, Hinglish, or both in the first benchmark?"

---

## 1. The decision

```text
Primary setting: Hindi and naturally occurring Hinglish to English
```

Hindi and Hinglish are treated as **related but distinct values** in the dataset,
not as one merged category:

```text
Hindi
Hinglish
```

Every item records exactly one of these in its `language` field, and the item ID
carries the corresponding prefix (`HIN_` or `HNG_`). This makes it possible to
report results separately for monolingual and code-mixed input, which is a
research question in its own right rather than a bookkeeping detail.

Telugu → English remains a **possible second-stage extension** and is not part of
the first release.

### The target variety: Indian English

The benchmark translates **into Indian English** (supervisor decision, made after
the pilot was drafted). This matters because the benchmark judges social meaning in
the output, and Indian English has its own conventions for politeness, address, and
formality. A translation that is natural in Indian English can read as odd in
British or American English, and the reverse, so leaving the target variety
unstated would make evaluators disagree for the wrong reason.

Consequences:

- Evaluators judge translation naturalness against **Indian English**, not a
  generic or British/American standard. This is stated in
  [../../benchmark/guidelines/human_evaluation_guidelines.md](../../benchmark/guidelines/human_evaluation_guidelines.md)
  and [../../benchmark/guidelines/annotation_guidelines.md](../../benchmark/guidelines/annotation_guidelines.md).
- The 47 pilot references were drafted by a single non-native author in a general
  informal register **before** this decision. They are **not** assumed to already
  be Indian English. Conforming them is an explicit criterion in Stage 1 native
  review, not a mechanical rewrite done in advance, because producing authentic
  Indian English without lapsing into caricature is a native-speaker task. See
  Issue 10 in [../../benchmark/pilot/pilot_issues.md](../../benchmark/pilot/pilot_issues.md).
- "Indian English" here means the standard educated register used in Indian
  professional and everyday settings, not any single regional variety. Where a
  reference could plausibly differ by region, that is recorded rather than resolved,
  consistent with the disagreement-preserving stance in section 7.

---

## 2. An important limitation, stated up front

**This choice is not universally representative of Indian languages.**

India has many languages with different politeness systems, different honorific
morphology, and different conventions for indirectness. Hindi is one of them. It
is not a proxy for Telugu, Tamil, Bengali, Marathi, Kannada, Malayalam, Punjabi,
Gujarati, Odia, Assamese or any other language.

Findings from this benchmark should be described as findings about **Hindi and
Hinglish conversational translation**, never as findings about "Indian language
MT" in general. Where the project title uses "Indian Dialogue", that reflects the
long-term ambition, not the coverage of the first release.

This limitation is deliberate and is preferable to the alternative: covering many
languages shallowly, without native-speaker validation in any of them.

---

## 3. Why this setting was selected

### A large pool of potential annotators

The single hardest constraint on this project is access to native speakers who can
make reliable pragmatic judgements. Pragmatic annotation cannot be crowdsourced
cheaply or done by non-native speakers. Hindi has the largest such pool available
to this project, and Hinglish is used by most of the same speakers, so one pool
serves both settings.

### Strong relevance to Indian conversational translation

Hindi and Hinglish are heavily used in exactly the settings this benchmark models:
workplace chat, customer support, education, and family conversation. Machine
translation is already deployed in these settings, so pragmatic failures here have
practical consequences.

### Frequent politeness and formality distinctions

Hindi marks politeness grammatically and pervasively:

| Level | Pronoun | Imperative | Example |
|---|---|---|---|
| Respectful | `aap` | `-iye` / `-jiye` | `Aap baith jaiye.` |
| Familiar | `tum` | `-o` | `Tum baith jao.` |
| Intimate | `tu` | bare stem | `Tu baith ja.` |

Because this three-way distinction is obligatory — a speaker must choose one — and
English has no direct equivalent, every translation is forced to make a decision
that the source language made explicitly. That is precisely the kind of
information-losing choice this benchmark is designed to measure.

This also connects the work to the existing literature. Sennrich, Haddow & Birch
(2016) controlled the German T–V distinction with side constraints; Voita, Sennrich
& Titov (2019) found that forms of address were the largest single source of
context-dependent errors in English–Russian. Hindi's system is richer than either,
with honorific verb agreement and `-ji` suffixation layered on top of pronoun
choice.

### Availability of code-mixed dialogue

Hinglish is one of the most widely used code-mixed varieties, which makes the
discourse-motivated code-switching category tractable in a way it would not be for
most language pairs.

### Compatibility with the proposed pragmatic categories

All four categories are well attested in Hindi and Hinglish:

| Category | Realisation |
|---|---|
| Politeness and formality | pronoun choice, imperative morphology, honorifics, `-ji`, kinship address terms |
| Indirect requests and refusals | conventionalised deflections; explicit refusal to a senior is strongly dispreferred |
| Stance and emotion | discourse particles (`toh`, `na`, `hi`, `arre`), solidarity markers (`yaar`), rhetorical questions |
| Code-switching | Hindi–English switching with functions including authority, intimacy, sarcasm and quotation |

---

## 4. What counts as Hindi

`language: "Hindi"` — the utterance is **entirely in Hindi**, with no English
material carrying content.

Included:

- Standard Hindi as used in education, media and formal settings.
- Colloquial spoken Hindi, including reduced and contracted forms.
- Utterances containing English loanwords so thoroughly nativised that they are
  simply Hindi vocabulary for the speaker.

Examples:

```text
Sir, kya mujhe do din aur mil sakte hain?
Haan tu gyarah baje aa ja.
Koi baat nahi, ho jata hai.
```

The first contains the English-origin `Sir`, but as a fully nativised address term
with no alternation into English. It is Hindi.

### Script

**All source text is written in romanized Latin script**, following the convention
already used in the worked examples of
[benchmark_blueprint.md §7](benchmark_blueprint.md).

Reasons:

- it matches how Hindi is typically typed in chat and messaging, which is the
  register this benchmark models;
- it makes Hindi and Hinglish directly comparable, since Hinglish is almost always
  written in Latin script;
- it avoids introducing a script variable that would confound the pragmatic
  comparisons.

**The known cost:** romanization is not standardised, and many MT systems are
trained primarily on Devanagari. Spellings here may not match what a given system
expects, and results may therefore understate system quality. Adding an optional
`source_devanagari` field is recorded as a candidate change in
[../../benchmark/schema/schema_version.md](../../benchmark/schema/schema_version.md)
and as issue 9 in
[../../benchmark/pilot/pilot_issues.md](../../benchmark/pilot/pilot_issues.md).

---

## 5. What counts as Hinglish

`language: "Hinglish"` — the utterance **alternates between Hindi and English**,
with English material carrying content, in a way that reflects how the speaker
would actually talk.

Examples:

```text
Sir almost done hai, bas ek slide baaki hai.
Arre kuch nahi yaar, bas thoda ghar ki tension hai.
Dekho, this is the final deadline. Iske baad extension nahi milega.
```

### Naturally occurring, not constructed

The decision specifies *naturally occurring* Hinglish. Included:

- switching at clause boundaries (`Dekho, this is the final deadline.`)
- switching within a clause (`main teen baar already revise kar chuka hoon`)
- English technical or workplace vocabulary in a Hindi frame
- English discourse markers in a Hindi frame

Excluded:

- **Word-substitution exercises.** Taking a Hindi sentence and swapping random
  words for English is not Hinglish; it is a construction. Every switch must be one
  a speaker would plausibly produce.
- **English sentences with a Hindi word attached** for flavour.
- **Switching invented to create a code-switching item.** If a switch would not
  occur naturally, the item is invalid regardless of how neatly it illustrates a
  function.

### Code-mixing is not automatically pragmatic

An item being Hinglish does **not** mean its code-switching is pragmatically
meaningful. Most English in everyday Hinglish is unmarked borrowing. The
`code_switch_function` field is set to `NOT_APPLICABLE` in those cases, and only to
a named function when a switch does discourse work. See
[label_definitions.md §8](../../benchmark/schema/label_definitions.md).

The distinction between the two fields:

| | `language` | `code_switch_function` |
|---|---|---|
| Monolingual Hindi | `Hindi` | `null` — no switch exists |
| Hinglish, switching unmarked | `Hinglish` | `NOT_APPLICABLE` |
| Hinglish, switching meaningful | `Hinglish` | a named function |

---

## 6. What is excluded

**Other languages.** Telugu, Tamil, Bengali, Marathi, Urdu and every other language
are outside the first release. Urdu is excluded despite its close relationship to
Hindi, because the register and script conventions differ enough to be a separate
decision.

**Regional Hindi varieties as separate categories.** Bhojpuri, Haryanvi, Awadhi,
Braj and other varieties are not treated as distinct values. Utterances influenced
by them may appear, but the benchmark does not systematically cover them and makes
no claim about them.

**English → Hindi.** The direction is Hindi/Hinglish → English only. The reverse
direction raises different questions — chiefly *generating* honorific distinctions
that the English source never made — and deserves its own design.

**Devanagari-script source text**, for the reasons in section 4.

**Non-conversational text.** News, literature, documentation and formal writing are
out of scope. The benchmark is about dialogue.

**Constructed or unnatural code-mixing**, per section 5.

---

## 7. Known regional and dialect limitations

These are limitations of the resource and must be reported alongside any results.

**Regional variation in politeness norms is real and is not systematically
covered.** Whether `tu` reads as intimate or rude varies by region, community and
generation. An item whose reading depends on one regional norm may be judged
differently by a speaker from elsewhere, and the benchmark cannot currently say
which reading is more widely held.

**The annotator pool determines the coverage.** With two annotators, whatever
regional varieties those two speak is the coverage the benchmark has. If both share
a background, region-dependence becomes undetectable. Annotators are asked to state
their regional background so this can at least be reported.

**Hinglish varies by city, age and setting.** The Hinglish used in a Bangalore tech
workplace differs from Delhi student speech and from Mumbai service interactions.
The pilot leans toward urban, workplace-and-education Hinglish.

**Register coverage is narrow.** The pilot clusters around workplace, academic and
service interactions, with limited family content and no formal institutional
settings such as government offices or banks.

**Mitigations in place:**

1. `language_variety` records the variety per item.
2. Annotators are asked to flag region-dependent judgements.
3. Adjudication has an explicit `REGIONAL_VARIATION` type, and such disagreements
   are **preserved rather than resolved**. See
   [adjudication_guidelines.md](../../benchmark/guidelines/adjudication_guidelines.md).
4. [annotation_guidelines.md §15](../../benchmark/guidelines/annotation_guidelines.md)
   instructs annotators to judge naturalness for *some substantial group of
   speakers*, not for themselves.

None of these solves the problem. They make it visible.

---

## 8. How Telugu may be added later

Telugu → English remains the intended second setting. It is a good complement
because it is Dravidian rather than Indo-Aryan, has its own honorific system, and
would test whether the schema generalises beyond one language family.

**Adding it is deferred until the schema and protocol have been validated on Hindi
and Hinglish.** Expanding an unvalidated schema to a second language would risk
having to redo both.

Preconditions:

1. The pilot has been annotated and agreement is acceptable.
2. Schema `0.2.0` incorporates the pilot's findings.
3. At least two Telugu native-speaker annotators are available. **This is the
   binding constraint**, not the schema work.

The schema is mostly ready. What a Telugu extension would need:

| Change | Detail |
|---|---|
| `language` | add `Telugu` |
| `translation_direction` | add `Telugu-English` |
| `item_id` pattern | add a `TEL` prefix |
| `code_switch_function` | decide whether Telugu–English mixing is in scope |
| `label_definitions.md` | Telugu examples for every label |
| Politeness levels | check whether Telugu's system maps onto the five values, or needs its own |

That last row is the substantive research question. Telugu's honorific system does
not map one-to-one onto Hindi's `aap`/`tum`/`tu`. If the politeness scale needs to
differ by language, that is a finding about the schema's generality and should be
reported as one, not hidden by forcing a shared vocabulary.

**No Telugu work should begin before the pilot findings are in.**

---

## 9. Consequences for the current release

1. `language` accepts exactly `Hindi` and `Hinglish`.
2. `translation_direction` accepts exactly `Hindi-English` and `Hinglish-English`.
3. Item IDs use `HIN_` and `HNG_` prefixes, checked against `language` during
   validation.
4. The pilot contains 26 Hindi and 21 Hinglish items.
5. All seven code-switching items are Hinglish, which the schema enforces.
6. Results must be reported separately for Hindi and Hinglish where the counts
   support it.
7. Every write-up must state that the benchmark covers one language pair and does
   not generalise to other Indian languages.
