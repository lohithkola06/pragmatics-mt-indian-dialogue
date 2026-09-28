#!/usr/bin/env python3
"""Build the data bundle for the pilot annotation web app.

Reads the pilot JSONL, the app config and the annotator-facing guideline docs,
and writes the files that the React app in annotation-app/ consumes:

    annotation-app/src/generated/items.json         items for display
    annotation-app/src/generated/stage2_units.json  the 94 Stage 2 candidates
    annotation-app/src/generated/meta.json          fingerprint, config, columns
    annotation-app/src/generated/guidelines/*.md    copies of the synced docs

The generated files are committed, so each deploy freezes exactly what
annotators see. Re-run this after changing pilot items, guideline docs, or the
app config, then commit the result. ``--check`` fails if the committed files
are stale, and the test suite runs it.

Before writing anything the script checks that no annotator-facing doc quotes a
pilot item. Annotators read those docs before rating, so a quoted item would
hand them its intended answer.

Usage:
    python scripts/build_annotation_app_data.py
    python scripts/build_annotation_app_data.py --check
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from create_annotation_sheet import (  # noqa: E402
    CONTEXT_COLUMNS,
    EVALUATION_COLUMNS,
    build_rows,
    read_items,
)

DEFAULT_JSONL = REPO_ROOT / "benchmark" / "pilot" / "pilot_items_v1.jsonl"
DEFAULT_CONFIG = REPO_ROOT / "benchmark" / "pilot" / "annotation_app_config.json"
DEFAULT_OUT_DIR = REPO_ROOT / "annotation-app" / "src" / "generated"
REVIEW_TEMPLATE = REPO_ROOT / "benchmark" / "pilot" / "pilot_item_review_template.csv"

# Stage 1 (item review) export columns. The review template CSV must match.
REVIEW_COLUMNS = [
    "item_id",
    "reviewer_id",
    "source_is_natural",
    "intended_interpretation_is_clear",
    "reference_is_valid",
    "contrastive_is_semantically_close",
    "contrastive_is_pragmatically_wrong",
    "primary_label_is_correct",
    "context_label_is_correct",
    "no_undocumented_cultural_assumption",
    "reviewer_severity",
    "recommended_action",
    "suggested_indian_english_reference",
    "notes",
]

# Stage 2 (blind rating) export columns: exactly the blind annotation sheet.
STAGE2_COLUMNS = CONTEXT_COLUMNS + EVALUATION_COLUMNS

# Fields shipped to the app for display. Severity and creator notes are left
# out on purpose: Stage 1 re-rates severity blind, and the notes carry the
# author's reasoning.
DISPLAY_FIELDS = [
    "item_id",
    "language",
    "language_variety",
    "source_type",
    "context",
    "source_utterance",
    "literal_gloss",
    "listener_role",
    "relationship",
    "relative_status",
    "familiarity",
    "primary_phenomenon",
    "secondary_phenomena",
    "speech_act",
    "politeness_level",
    "formality_level",
    "stance",
    "emotion",
    "indirectness",
    "code_switch_function",
    "context_status",
    "context_explanation",
    "preservation_requirement",
    "reference_translations",
    "acceptable_variants",
    "contrastive_translation",
    "contrastive_error",
    "contrastive_error_category",
]

ITEM_ID_PATTERN = re.compile(r"\b(?:HIN|HNG)_(?:POL|IND|STA|CSW)_\d{3}\b")

# Priming guard window sizes. Hindi-side strings (utterances and context turns)
# are matched on any run of this many consecutive words, so a lightly edited
# quote is still caught. English translations are matched whole, because short
# English word runs recur too often by chance.
SOURCE_WINDOW = 4
MIN_TRANSLATION_TOKENS = 4


# --------------------------------------------------------------------------
# Priming guard
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class PrimingHit:
    """A pilot item's text (or ID) found inside an annotator-facing doc."""

    item_id: str
    field: str
    doc: str
    snippet: str
    line: int | None

    def __str__(self) -> str:
        where = f"{self.doc}:{self.line}" if self.line else self.doc
        return f"  {where}  [{self.item_id} {self.field}]  \"{self.snippet}\""


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens, ignoring punctuation and quote styles."""
    return re.findall(r"[^\W_]+", text.lower())


def _contains(haystack_tokens: str, needle: list[str]) -> bool:
    return f" {' '.join(needle)} " in haystack_tokens


def _windows(tokens: list[str], size: int) -> list[list[str]]:
    if len(tokens) < 2:
        return []
    if len(tokens) <= size:
        return [tokens]
    return [tokens[i : i + size] for i in range(len(tokens) - size + 1)]


def _lines_of(doc_text: str, needle: list[str]) -> list[int | None]:
    """Every line containing the needle, or [None] if it only spans lines."""
    lines = [
        number
        for number, line in enumerate(doc_text.splitlines(), start=1)
        if _contains(f" {' '.join(tokenize(line))} ", needle)
    ]
    return lines or [None]


def find_priming(items: list[dict], docs: dict[str, str]) -> list[PrimingHit]:
    """Return every place an annotator-facing doc quotes or cites a pilot item."""
    hits: list[PrimingHit] = []
    doc_tokens = {name: f" {' '.join(tokenize(text))} " for name, text in docs.items()}

    for item in items:
        item_id = item["item_id"]

        hindi_side: list[tuple[str, str]] = [
            ("source_utterance", item["source_utterance"]["text"]),
        ]
        hindi_side += [
            (f"context[{i}]", turn["text"]) for i, turn in enumerate(item.get("context") or [])
        ]
        english_side: list[tuple[str, str]] = [
            (f"reference_translations[{i}]", text)
            for i, text in enumerate(item.get("reference_translations") or [])
        ]
        english_side += [
            (f"acceptable_variants[{i}]", text)
            for i, text in enumerate(item.get("acceptable_variants") or [])
        ]
        english_side.append(("contrastive_translation", item["contrastive_translation"]))

        for name, tokens in doc_tokens.items():
            seen: set[tuple[str, int | None]] = set()

            def record(field: str, needle: list[str]) -> None:
                for line in _lines_of(docs[name], needle):
                    if (field, line) not in seen:
                        seen.add((field, line))
                        hits.append(PrimingHit(item_id, field, name, " ".join(needle), line))

            for field, text in hindi_side:
                for window in _windows(tokenize(text), SOURCE_WINDOW):
                    if _contains(tokens, window):
                        record(field, window)
            for field, text in english_side:
                words = tokenize(text)
                if len(words) >= MIN_TRANSLATION_TOKENS and _contains(tokens, words):
                    record(field, words)

    pilot_ids = {item["item_id"] for item in items}
    for name, text in docs.items():
        for number, line in enumerate(text.splitlines(), start=1):
            for match in ITEM_ID_PATTERN.findall(line):
                if match in pilot_ids:
                    hits.append(PrimingHit(match, "item_id", name, match, number))

    return hits


# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------


def load_config(path: Path) -> dict:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_config(config: dict, items: list[dict]) -> list[str]:
    """Return a list of problems with the app config (empty when valid)."""
    problems: list[str] = []
    by_id = {item["item_id"]: item for item in items}

    if not isinstance(config.get("stage2_enabled"), bool):
        problems.append("stage2_enabled must be true or false")

    calibration = config.get("calibration_items")
    if not isinstance(calibration, list) or not calibration:
        problems.append("calibration_items must be a non-empty list")
        calibration = []
    if len(set(calibration)) != len(calibration):
        problems.append("calibration_items contains duplicates")

    chosen = []
    for item_id in calibration:
        item = by_id.get(item_id)
        if item is None:
            problems.append(f"calibration item {item_id} is not in the pilot set")
            continue
        if item["source_type"] == "MINIMAL_PAIR":
            problems.append(
                f"calibration item {item_id} is a minimal pair; discussing it "
                "would prime its partner"
            )
        chosen.append(item)

    if chosen:
        if not any(i["primary_phenomenon"] == "CODE_SWITCHING" for i in chosen):
            problems.append("calibration items must include a code-switching item")
        if not any(i["context_status"] == "NOT_REQUIRED" for i in chosen):
            problems.append("calibration items must include a NOT_REQUIRED item")
        if {i["language"] for i in chosen} != {"Hindi", "Hinglish"}:
            problems.append("calibration items must cover both Hindi and Hinglish")

    docs = config.get("synced_docs")
    if not isinstance(docs, list) or not docs:
        problems.append("synced_docs must be a non-empty list")
    else:
        for doc in docs:
            if not (REPO_ROOT / doc).is_file():
                problems.append(f"synced doc not found: {doc}")
        names = [Path(doc).name for doc in docs]
        if len(set(names)) != len(names):
            problems.append("synced_docs must have unique file names")

    if not isinstance(config.get("contact_instructions"), str) or not config[
        "contact_instructions"
    ].strip():
        problems.append("contact_instructions must be a non-empty string")

    return problems


# --------------------------------------------------------------------------
# Export format (reference implementation)
# --------------------------------------------------------------------------
#
# The app writes its CSVs in TypeScript. These functions define the exact bytes
# it must produce: Python's csv module defaults (minimal quoting, CRLF line
# endings) and no byte-order mark. The committed fixtures under
# scripts/tests/fixtures/ are rendered by these functions, and the app's own
# tests must reproduce them byte for byte.

STAGE2_RATING_COLUMNS = [
    c for c in EVALUATION_COLUMNS if c not in ("annotator_id", "uncertainty_label", "notes")
]


def _render_csv(columns: list[str], rows: list[dict]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\r\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def render_stage2_csv(units: list[dict], ratings: dict[str, dict], annotator_id: str) -> str:
    """One row per unit, in the given order; unrated fields are left empty."""
    rows = []
    for unit in units:
        given = ratings.get(unit["candidate_id"], {})
        row = dict(unit["sheet"])
        row["annotator_id"] = annotator_id
        for column in STAGE2_RATING_COLUMNS + ["uncertainty_label", "notes"]:
            row[column] = given.get(column, "")
        rows.append(row)
    return _render_csv(STAGE2_COLUMNS, rows)


def render_review_csv(item_ids: list[str], reviews: dict[str, dict], reviewer_id: str) -> str:
    """One row per item, in the given order; unanswered fields are left empty."""
    rows = []
    for item_id in item_ids:
        given = reviews.get(item_id, {})
        row = {column: given.get(column, "") for column in REVIEW_COLUMNS}
        row["item_id"] = item_id
        row["reviewer_id"] = reviewer_id
        rows.append(row)
    return _render_csv(REVIEW_COLUMNS, rows)


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def item_hash(item: dict) -> str:
    """Stable content hash of one item, used to flag responses to revised items."""
    return _hash(json.dumps(item, sort_keys=True, ensure_ascii=False))


def doc_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _dump(data) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def render_outputs(
    items: list[dict], config: dict, jsonl_text: str, docs: dict[str, str]
) -> dict[str, str]:
    """Produce every generated file as {relative path: contents}. Deterministic."""
    display_items = []
    for item in items:
        shown = {field: item.get(field) for field in DISPLAY_FIELDS}
        shown["minimal_pair"] = item["source_type"] == "MINIMAL_PAIR"
        shown["hash"] = item_hash(item)
        display_items.append(shown)

    hashes = {item["item_id"]: item_hash(item) for item in items}
    units = []
    for row in build_rows(items, blind=True)[0]:
        units.append(
            {
                "candidate_id": row["candidate_id"],
                "item_id": row["item_id"],
                "item_hash": hashes[row["item_id"]],
                "sheet": {column: row[column] for column in CONTEXT_COLUMNS},
            }
        )

    doc_entries = []
    outputs: dict[str, str] = {}
    for rel_path in config["synced_docs"]:
        name = Path(rel_path).name
        text = docs[name]
        doc_entries.append(
            {"file": name, "title": doc_title(text, name), "source_path": rel_path}
        )
        outputs[f"guidelines/{name}"] = text

    meta = {
        "dataset_fingerprint": _hash(jsonl_text),
        "dataset_path": "benchmark/pilot/pilot_items_v1.jsonl",
        "item_count": len(items),
        "unit_count": len(units),
        "stage2_enabled": config["stage2_enabled"],
        "calibration_items": config["calibration_items"],
        "contact_instructions": config["contact_instructions"],
        "review_columns": REVIEW_COLUMNS,
        "stage2_columns": STAGE2_COLUMNS,
        "stage2_context_columns": CONTEXT_COLUMNS,
        "stage2_evaluation_columns": EVALUATION_COLUMNS,
        "docs": doc_entries,
    }

    outputs["items.json"] = _dump(display_items)
    outputs["stage2_units.json"] = _dump(units)
    outputs["meta.json"] = _dump(meta)
    return outputs


def load_docs(config: dict) -> dict[str, str]:
    return {
        Path(rel).name: (REPO_ROOT / rel).read_text(encoding="utf-8")
        for rel in config["synced_docs"]
    }


def check_outputs(outputs: dict[str, str], out_dir: Path) -> list[str]:
    """Differences between freshly rendered outputs and the files on disk."""
    problems = []
    for rel, contents in sorted(outputs.items()):
        path = out_dir / rel
        if not path.is_file():
            problems.append(f"missing: {rel}")
        elif path.read_text(encoding="utf-8") != contents:
            problems.append(f"stale: {rel}")
    if out_dir.is_dir():
        for path in sorted(out_dir.rglob("*")):
            if path.is_file() and path.relative_to(out_dir).as_posix() not in outputs:
                problems.append(f"unexpected: {path.relative_to(out_dir).as_posix()}")
    return problems


def write_outputs(outputs: dict[str, str], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(out_dir.rglob("*"), reverse=True):
        rel = path.relative_to(out_dir).as_posix()
        if path.is_file() and rel not in outputs:
            path.unlink()
    for rel, contents in outputs.items():
        path = out_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(contents)


def build(
    jsonl: Path = DEFAULT_JSONL, config_path: Path = DEFAULT_CONFIG
) -> tuple[dict[str, str], list[str]]:
    """Validate inputs and render outputs. Returns (outputs, problems)."""
    from validate_jsonl import validate_file

    report = validate_file(jsonl)
    if not report.ok:
        return {}, ["pilot dataset fails validation; run scripts/validate_jsonl.py"]

    items = read_items(jsonl)
    config = load_config(config_path)
    problems = validate_config(config, items)
    if problems:
        return {}, problems

    docs = load_docs(config)
    hits = find_priming(items, docs)
    if hits:
        return {}, ["annotator-facing docs quote pilot items:"] + [str(h) for h in hits]

    jsonl_text = Path(jsonl).read_text(encoding="utf-8")
    return render_outputs(items, config, jsonl_text, docs), []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="Fail if the committed generated files are stale")
    parser.add_argument("--jsonl", type=Path, default=DEFAULT_JSONL)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args(argv)

    try:
        outputs, problems = build(args.jsonl, args.config)
    except ImportError:
        print("ERROR: the 'jsonschema' package is required "
              "(python -m pip install -r requirements.txt)", file=sys.stderr)
        return 1

    if problems:
        print("ERROR: cannot build the annotation app data.", file=sys.stderr)
        for problem in problems:
            print(problem if problem.startswith("  ") else f"  {problem}", file=sys.stderr)
        return 1

    if args.check:
        stale = check_outputs(outputs, args.out_dir)
        if stale:
            print("ERROR: generated app data is out of date. Run:", file=sys.stderr)
            print("  python scripts/build_annotation_app_data.py", file=sys.stderr)
            for line in stale:
                print(f"  {line}", file=sys.stderr)
            return 1
        print(f"OK: {args.out_dir.relative_to(REPO_ROOT)} is up to date.")
        return 0

    write_outputs(outputs, args.out_dir)
    print(f"Wrote {len(outputs)} files to {args.out_dir.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
