#!/usr/bin/env python3
"""Validate a JSONL file of benchmark items against item_schema.json.

Runs two layers of checks:

1. JSON Schema validation (structure, required fields, controlled vocabularies).
2. Cross-field consistency checks that are clearer in Python than in JSON Schema
   (item-ID coherence, context turn references, duplicate IDs, empty fields).

Usage:
    python scripts/validate_jsonl.py benchmark/pilot/pilot_items_v1.jsonl
    python scripts/validate_jsonl.py path/to/items.jsonl --schema path/to/schema.json

Exits non-zero when any item fails.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA_PATH = REPO_ROOT / "benchmark" / "schema" / "item_schema.json"

# item_id encodes language and category; both must agree with the item's fields.
LANGUAGE_CODES = {"HIN": "Hindi", "HNG": "Hinglish"}
CATEGORY_CODES = {
    "POL": "POLITENESS_FORMALITY",
    "IND": "INDIRECT_REQUEST_REFUSAL",
    "STA": "STANCE_EMOTION",
    "CSW": "CODE_SWITCHING",
}
DIRECTION_FOR_LANGUAGE = {"Hindi": "Hindi-English", "Hinglish": "Hinglish-English"}

# Fields that must not be present-but-blank.
NON_EMPTY_STRING_FIELDS = (
    "schema_version",
    "language_variety",
    "license",
    "literal_gloss",
    "listener_role",
    "preservation_requirement",
    "contrastive_translation",
    "contrastive_error",
    "annotation_version",
)


@dataclass
class ItemError:
    """A single validation failure, tied back to its line and item."""

    line_number: int
    item_id: str
    message: str

    def __str__(self) -> str:
        return f"  line {self.line_number} [{self.item_id}] {self.message}"


@dataclass
class ValidationReport:
    """Aggregate result of validating one JSONL file."""

    path: Path
    total_lines: int = 0
    valid_count: int = 0
    invalid_count: int = 0
    errors: list[ItemError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_schema(schema_path: Path = DEFAULT_SCHEMA_PATH) -> dict:
    """Read and parse the item schema."""
    with Path(schema_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def build_validator(schema: dict):
    """Build a draft 2020-12 validator for the given schema."""
    from jsonschema import Draft202012Validator

    return Draft202012Validator(schema)


def _format_schema_error(error) -> str:
    """Turn a jsonschema ValidationError into a short, readable message."""
    location = "/".join(str(part) for part in error.absolute_path)
    where = location or "<root>"
    return f"schema: {where}: {error.message}"


def check_cross_fields(item: dict) -> list[str]:
    """Consistency checks that go beyond what the JSON Schema expresses.

    Returns a list of human-readable problem descriptions (empty when clean).
    Assumes the item is a dict, but tolerates missing or mistyped fields so it
    can run alongside schema validation rather than after it.
    """
    problems: list[str] = []

    item_id = item.get("item_id")
    language = item.get("language")
    phenomenon = item.get("primary_phenomenon")

    # --- item_id coherence -------------------------------------------------
    if isinstance(item_id, str):
        parts = item_id.split("_")
        if len(parts) == 3:
            lang_code, cat_code, _serial = parts
            expected_language = LANGUAGE_CODES.get(lang_code)
            if expected_language and language and expected_language != language:
                problems.append(
                    f"item_id prefix '{lang_code}' implies language "
                    f"'{expected_language}' but language is '{language}'"
                )
            expected_phenomenon = CATEGORY_CODES.get(cat_code)
            if expected_phenomenon and phenomenon and expected_phenomenon != phenomenon:
                problems.append(
                    f"item_id code '{cat_code}' implies primary_phenomenon "
                    f"'{expected_phenomenon}' but found '{phenomenon}'"
                )

    # --- language / direction ---------------------------------------------
    direction = item.get("translation_direction")
    if language in DIRECTION_FOR_LANGUAGE and direction:
        expected = DIRECTION_FOR_LANGUAGE[language]
        if direction != expected:
            problems.append(
                f"language '{language}' implies translation_direction "
                f"'{expected}' but found '{direction}'"
            )

    # --- empty-but-present fields -----------------------------------------
    for name in NON_EMPTY_STRING_FIELDS:
        value = item.get(name)
        if isinstance(value, str) and not value.strip():
            problems.append(f"{name} is empty")

    for name in ("reference_translations", "acceptable_variants"):
        values = item.get(name)
        if isinstance(values, list):
            for index, entry in enumerate(values):
                if isinstance(entry, str) and not entry.strip():
                    problems.append(f"{name}[{index}] is empty")

    source_utterance = item.get("source_utterance")
    if isinstance(source_utterance, dict):
        text = source_utterance.get("text")
        if isinstance(text, str) and not text.strip():
            problems.append("source_utterance.text is empty")

    # --- context turn references ------------------------------------------
    context = item.get("context")
    if isinstance(context, list):
        turn_ids: list[int] = []
        for index, turn in enumerate(context):
            if isinstance(turn, dict) and isinstance(turn.get("turn_id"), int):
                turn_ids.append(turn["turn_id"])
            if isinstance(turn, dict):
                text = turn.get("text")
                if isinstance(text, str) and not text.strip():
                    problems.append(f"context[{index}].text is empty")

        if len(turn_ids) != len(set(turn_ids)):
            problems.append("context turn_id values are not unique")

        expected_ids = list(range(1, len(context) + 1))
        if turn_ids and turn_ids != expected_ids:
            problems.append(
                f"context turn_id values {turn_ids} are not sequential from 1 "
                f"(expected {expected_ids})"
            )

        relevant = item.get("relevant_context_turns")
        if isinstance(relevant, list):
            for turn_id in relevant:
                if turn_id not in turn_ids:
                    problems.append(
                        f"relevant_context_turns references turn {turn_id}, "
                        f"which is not present in context {turn_ids or '[]'}"
                    )

        window = item.get("minimum_context_window")
        if isinstance(window, int) and window > len(context):
            problems.append(
                f"minimum_context_window is {window} but only "
                f"{len(context)} context turn(s) are present"
            )

        # The source utterance should follow the context turns.
        if isinstance(source_utterance, dict):
            source_turn_id = source_utterance.get("turn_id")
            expected_source_turn = len(context) + 1
            if (
                isinstance(source_turn_id, int)
                and source_turn_id != expected_source_turn
            ):
                problems.append(
                    f"source_utterance.turn_id is {source_turn_id} but should be "
                    f"{expected_source_turn} (one after the last context turn)"
                )

    # --- context status coherence -----------------------------------------
    status = item.get("context_status")
    required_flag = item.get("context_required")
    if status == "REQUIRED" and required_flag is False:
        problems.append("context_status is REQUIRED but context_required is false")
    if status == "NOT_REQUIRED" and required_flag is True:
        problems.append("context_status is NOT_REQUIRED but context_required is true")

    # --- code-switching coherence -----------------------------------------
    switch_function = item.get("code_switch_function")
    if phenomenon == "CODE_SWITCHING" and switch_function in (None, "NOT_APPLICABLE"):
        problems.append(
            "primary_phenomenon is CODE_SWITCHING but code_switch_function is "
            f"{switch_function!r}; a real discourse function is required"
        )

    # --- provenance --------------------------------------------------------
    source_type = item.get("source_type")
    source_reference = item.get("source_reference")
    if source_type in ("NATURAL", "ADAPTED") and not source_reference:
        problems.append(
            f"source_type is {source_type} but source_reference is missing; "
            "provenance must be documented"
        )

    # --- contrastive must actually differ from the references --------------
    contrastive = item.get("contrastive_translation")
    references = item.get("reference_translations")
    variants = item.get("acceptable_variants")
    if isinstance(contrastive, str) and contrastive.strip():
        accepted = []
        for group in (references, variants):
            if isinstance(group, list):
                accepted.extend(g for g in group if isinstance(g, str))
        normalized = contrastive.strip().casefold()
        if any(normalized == entry.strip().casefold() for entry in accepted):
            problems.append(
                "contrastive_translation is identical to an accepted translation"
            )

    return problems


def validate_item(item: dict, validator) -> list[str]:
    """Validate one item, returning all problems found (schema first, then cross-field)."""
    problems = [
        _format_schema_error(error)
        for error in sorted(validator.iter_errors(item), key=lambda e: list(e.absolute_path))
    ]
    problems.extend(check_cross_fields(item))
    return problems


def validate_file(
    jsonl_path: Path,
    schema_path: Path = DEFAULT_SCHEMA_PATH,
) -> ValidationReport:
    """Validate every line of a JSONL file and return an aggregate report."""
    jsonl_path = Path(jsonl_path)
    report = ValidationReport(path=jsonl_path)
    validator = build_validator(load_schema(schema_path))

    seen_ids: dict[str, int] = {}

    with jsonl_path.open(encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                continue  # tolerate blank separator lines

            report.total_lines += 1

            try:
                item = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                report.invalid_count += 1
                report.errors.append(
                    ItemError(line_number, "<unparseable>", f"invalid JSON: {exc}")
                )
                continue

            if not isinstance(item, dict):
                report.invalid_count += 1
                report.errors.append(
                    ItemError(line_number, "<not-an-object>", "line is not a JSON object")
                )
                continue

            item_id = item.get("item_id", "<missing-id>")
            problems = validate_item(item, validator)

            # Duplicate detection is a file-level concern, so it lives here.
            if isinstance(item_id, str) and item_id != "<missing-id>":
                if item_id in seen_ids:
                    problems.append(
                        f"duplicate item_id (first seen on line {seen_ids[item_id]})"
                    )
                else:
                    seen_ids[item_id] = line_number

            if problems:
                report.invalid_count += 1
                for problem in problems:
                    report.errors.append(ItemError(line_number, str(item_id), problem))
            else:
                report.valid_count += 1

    return report


def print_report(report: ValidationReport) -> None:
    """Print a readable summary of a validation report."""
    try:
        display_path = report.path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        display_path = report.path

    print(f"Validating {display_path}")
    print(f"  items read:  {report.total_lines}")
    print(f"  valid:       {report.valid_count}")
    print(f"  invalid:     {report.invalid_count}")

    if report.errors:
        print(f"\n{len(report.errors)} problem(s) found:")
        for error in report.errors:
            print(error)
        print("\nFAILED")
    else:
        print("\nOK: all items conform to the schema.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path, help="Path to the JSONL file to validate")
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help="Path to the item schema (default: benchmark/schema/item_schema.json)",
    )
    args = parser.parse_args(argv)

    if not args.jsonl.is_file():
        print(f"ERROR: file not found: {args.jsonl}", file=sys.stderr)
        return 1
    if not args.schema.is_file():
        print(f"ERROR: schema not found: {args.schema}", file=sys.stderr)
        return 1

    try:
        report = validate_file(args.jsonl, args.schema)
    except ImportError:
        print(
            "ERROR: the 'jsonschema' package is required.\n"
            "       Install it with: python -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1

    print_report(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
