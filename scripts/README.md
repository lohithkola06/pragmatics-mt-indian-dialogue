# Scripts

Validation, statistics and annotation tooling for the benchmark.

All scripts are run **from the repository root** and locate the schema relative to
their own file, so they work regardless of the current directory.

---

## Requirements

```bash
python -m pip install -r requirements.txt
```

`jsonschema>=4.0` is the only hard dependency. Everything else uses the standard
library, so the annotation and agreement tooling runs on a bare Python install.

**Python version.** The project targets Python 3.11+, but the scripts use
`from __future__ import annotations` throughout and run correctly on **3.9 and
later**. Whichever interpreter you use, `jsonschema` must be installed for *that*
interpreter — if `python3 --version` and the interpreter with `jsonschema` differ,
the validation scripts will report the missing dependency and exit non-zero.

---

## Quick reference

```bash
python scripts/validate_schema.py
python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl
python scripts/generate_dataset_statistics.py benchmark/pilot/pilot_items_v1.jsonl
python scripts/create_annotation_sheet.py benchmark/pilot/pilot_items_v1.jsonl
python -m unittest discover scripts/tests
```

---

## `validate_schema.py`

Checks that `benchmark/schema/item_schema.json` is itself a valid JSON Schema
(draft 2020-12). Validates the *schema*, not any data. Run it after editing the
schema.

```bash
python scripts/validate_schema.py
python scripts/validate_schema.py --schema path/to/other_schema.json
```

Exits non-zero if the schema is malformed or unparseable.

---

## `validate_jsonl.py`

Validates every item in a JSONL file. This is the main quality gate.

```bash
python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl
python scripts/validate_jsonl.py <file.jsonl> --schema <schema.json>
```

Two layers of checking:

**JSON Schema** — structure, required fields, controlled vocabularies, nested
context turns, non-empty source utterances, at least one reference translation,
0–3 context turns, valid item-ID pattern, plus four conditional rules
(context-status coherence, code-switching coherence, provenance requirements).

**Cross-field checks** — expressed in Python because they read more clearly there:

- the item-ID language prefix agrees with `language`
- the item-ID category code agrees with `primary_phenomenon`
- `translation_direction` agrees with `language`
- `relevant_context_turns` only references turns that exist
- `minimum_context_window` does not exceed the number of context turns
- context turn IDs are sequential from 1
- `source_utterance.turn_id` follows the last context turn
- `context_required` agrees with `context_status`
- `CODE_SWITCHING` items name a real `code_switch_function`
- `NATURAL` / `ADAPTED` items have a `source_reference`
- required string fields are not present-but-blank
- **duplicate item IDs** across the file
- the contrastive translation is not identical to an accepted translation

Errors are reported with line number and item ID:

```text
Validating benchmark/pilot/pilot_items_v1.jsonl
  items read:  47
  valid:       47
  invalid:     0

OK: all items conform to the schema.
```

Exits non-zero when any item fails.

**Importable.** `load_schema`, `validate_item`, `check_cross_fields` and
`validate_file` can be imported; `validate_file` returns a `ValidationReport` with
`total_lines`, `valid_count`, `invalid_count` and `errors`.

---

## `generate_dataset_statistics.py`

Reports the composition of a dataset.

```bash
python scripts/generate_dataset_statistics.py <file.jsonl>
python scripts/generate_dataset_statistics.py <file.jsonl> --out report.md
python scripts/generate_dataset_statistics.py <file.jsonl> --out stats.json
```

Covers total count, and distributions over language, pragmatic category, source
type, context status, context window, severity, review status, contrastive error
category, speech act, politeness, formality, relationship and code-switch function;
plus context-turn counts, language × category and category × source-type
cross-tabs, and counts of missing or empty required fields.

Output format is inferred from the `--out` extension (`.md` or `.json`). Always
prints a readable report to the console.

Used to generate
[../benchmark/pilot/pilot_statistics.md](../benchmark/pilot/pilot_statistics.md).

**Reading the missing-fields table:** an *absent* field is always a defect. A field
that is *present but empty* is often expected — `annotator_ids` stays empty until
annotation happens, `source_reference` is null for elicited items,
`code_switch_function` is null for monolingual Hindi items.

---

## `create_annotation_sheet.py`

Turns a JSONL dataset into a CSV annotation sheet.

```bash
python scripts/create_annotation_sheet.py <file.jsonl>
python scripts/create_annotation_sheet.py <file.jsonl> --out sheet.csv
python scripts/create_annotation_sheet.py <file.jsonl> --blind
```

Each item produces **two rows** — the reference translation (`-A`) and the
contrastive translation (`-B`) — so annotators rate both on the same dimensions.
That is what makes it possible to check afterwards whether they separated semantic
adequacy from pragmatic preservation.

Dialogue context is rendered as readable turn text, not raw JSON:

```text
1. A (Professor): Yeh assignment kal shaam tak jama kar dijiye.
2. B (Student): Sir, kya mujhe do din aur mil sakte hain?
```

Items with no context get an explicit placeholder rather than a blank cell.

**`--blind`** omits the `candidate_type` column and writes the mapping to a
separate `.key.csv`. Use it for real annotation: an annotator who knows which
candidate is the intended-correct one is not making an independent judgement.
**Keep the key file away from annotators.**

---

## `calculate_agreement.py`

Measures inter-annotator agreement on a completed annotation CSV.

```bash
python scripts/calculate_agreement.py completed.csv
python scripts/calculate_agreement.py completed.csv --out agreement_report.md
python scripts/calculate_agreement.py completed.csv --unit-column item_id
python scripts/calculate_agreement.py completed.csv --annotator-column rater
```

Per dimension, it computes:

- **percentage agreement** — mean pairwise exact match, each unit weighted equally
- **Cohen's kappa** — when exactly two annotators rated the dimension
- **Krippendorff's alpha (nominal)** — any number of annotators, tolerates missing
  ratings

The unit defaults to `candidate_id` when present, otherwise `item_id`. Blank cells
and `NA`, `N/A`, `none`, `-` are treated as missing and excluded.

**This script does not invent scores.** Where a statistic is undefined it prints
`n/a` and explains why:

- fewer than two annotators → reports insufficient data and computes nothing
- no unit rated twice → the dimension is skipped with a note
- both annotators used a single category → kappa is undefined, not 1.0
- an empty template → says so rather than producing an empty report

Running it against the un-annotated pilot sheet correctly reports insufficient
data. That is the expected output until annotation happens.

---

## Tests

```bash
python -m unittest discover scripts/tests
```

41 tests across two modules.

**`test_validate_jsonl.py`** — valid item acceptance, invalid enum rejection,
missing required field rejection, duplicate item ID rejection, invalid context
reference rejection, plus malformed item IDs, over-long context, empty reference
lists, non-sequential turn IDs, ID-to-label mismatches, code-switching coherence,
provenance requirements, unparseable lines, and a check that the committed pilot
dataset still validates.

**`test_calculate_agreement.py`** — percentage agreement, Cohen's kappa and
Krippendorff's alpha against hand-computed values, including a three-observer
worked example with missing ratings whose expected alpha is derived in the test
docstring rather than copied from a library.

Fixtures live in `scripts/tests/fixtures/`: `valid_item.json` mirrors a real pilot
item, and `invalid_item.json` is deliberately broken in several ways at once (two
bad enum values, an empty reference list, and a context reference pointing at a
turn that does not exist).

---

## Adding a script

- Put shared logic in importable functions; keep `main()` thin and guard it with
  `if __name__ == "__main__":`.
- Resolve paths from `Path(__file__).resolve().parent.parent` so the script works
  from any directory.
- Return a non-zero exit code on failure, so the scripts compose in a shell.
- Prefer the standard library. Add a dependency only when it materially simplifies
  the implementation, and record it in `requirements.txt`.
- Add tests under `scripts/tests/`.
- **Never fabricate a statistic.** If there is not enough data, say so.
