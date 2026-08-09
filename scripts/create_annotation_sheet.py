#!/usr/bin/env python3
"""Build a CSV annotation sheet from a benchmark JSONL file.

Each benchmark item produces one row per candidate translation: the reference
translation and the contrastive translation. Annotators rate every candidate on
the same dimensions, which is what makes it possible to check afterwards whether
they separate semantic adequacy from pragmatic preservation.

Dialogue context is rendered as readable turn-by-turn text rather than raw JSON.

Usage:
    python scripts/create_annotation_sheet.py benchmark/pilot/pilot_items_v1.jsonl
    python scripts/create_annotation_sheet.py <file.jsonl> --out sheet.csv
    python scripts/create_annotation_sheet.py <file.jsonl> --blind

With --blind the sheet does not say which candidate is the reference and which
is the contrastive, and a separate key file is written alongside it.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "benchmark" / "pilot" / "pilot_annotation_sheet.csv"

# Columns describing the item. Filled in by this script.
CONTEXT_COLUMNS = [
    "item_id",
    "candidate_id",
    "language",
    "primary_phenomenon",
    "dialogue_context",
    "source_utterance",
    "literal_gloss",
    "speaker_role",
    "listener_role",
    "relationship",
    "relative_status",
    "familiarity",
    "context_status",
    "preservation_requirement",
    "candidate_translation",
]

# Columns the annotator fills in. Left empty by this script.
EVALUATION_COLUMNS = [
    "annotator_id",
    "source_naturalness",
    "semantic_adequacy",
    "speech_act_preservation",
    "politeness_preservation",
    "formality_preservation",
    "stance_preservation",
    "emotion_preservation",
    "indirectness_preservation",
    "code_switch_preservation",
    "relationship_appropriateness",
    "translation_naturalness",
    "overall_pragmatic_preservation",
    "uncertainty_label",
    "notes",
]


def read_items(jsonl_path: Path) -> list[dict]:
    """Load every JSON object from a JSONL file."""
    items: list[dict] = []
    with Path(jsonl_path).open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                items.append(json.loads(line))
    return items


def format_context(item: dict) -> str:
    """Render the dialogue context as readable turn-by-turn text.

    Produces lines like "1. A (Professor): Yeh assignment kal ...". Returns a
    clear placeholder when the item deliberately carries no context.
    """
    turns = item.get("context") or []
    if not turns:
        return "(no previous turns - this item is interpretable on its own)"

    lines = []
    for turn in turns:
        lines.append(
            f"{turn.get('turn_id')}. {turn.get('speaker_id')} "
            f"({turn.get('speaker_role')}): {turn.get('text')}"
        )
    return "\n".join(lines)


def format_source_utterance(item: dict) -> str:
    """Render the source utterance in the same style as the context turns."""
    utterance = item.get("source_utterance") or {}
    return (
        f"{utterance.get('turn_id')}. {utterance.get('speaker_id')} "
        f"({utterance.get('speaker_role')}): {utterance.get('text')}"
    )


def candidates_for(item: dict) -> list[tuple[str, str, str]]:
    """Return (candidate_id, candidate_type, translation) for one item.

    The reference is always suffixed -A and the contrastive -B, so the mapping
    stays stable across regenerations of the sheet.
    """
    item_id = item.get("item_id", "UNKNOWN")
    references = item.get("reference_translations") or []
    reference = references[0] if references else ""
    contrastive = item.get("contrastive_translation", "")

    return [
        (f"{item_id}-A", "reference", reference),
        (f"{item_id}-B", "contrastive", contrastive),
    ]


def build_rows(items: list[dict], blind: bool) -> tuple[list[dict], list[dict]]:
    """Build the annotation rows and, for blind sheets, the answer key rows."""
    rows: list[dict] = []
    key_rows: list[dict] = []

    for item in items:
        utterance = item.get("source_utterance") or {}
        for candidate_id, candidate_type, translation in candidates_for(item):
            row = {
                "item_id": item.get("item_id", ""),
                "candidate_id": candidate_id,
                "language": item.get("language", ""),
                "primary_phenomenon": item.get("primary_phenomenon", ""),
                "dialogue_context": format_context(item),
                "source_utterance": format_source_utterance(item),
                "literal_gloss": item.get("literal_gloss", ""),
                "speaker_role": utterance.get("speaker_role", ""),
                "listener_role": item.get("listener_role", ""),
                "relationship": item.get("relationship", ""),
                "relative_status": item.get("relative_status", ""),
                "familiarity": item.get("familiarity", ""),
                "context_status": item.get("context_status", ""),
                "preservation_requirement": item.get("preservation_requirement", ""),
                "candidate_translation": translation,
            }
            if not blind:
                row["candidate_type"] = candidate_type
            for column in EVALUATION_COLUMNS:
                row[column] = ""
            rows.append(row)

            key_rows.append(
                {
                    "candidate_id": candidate_id,
                    "item_id": item.get("item_id", ""),
                    "candidate_type": candidate_type,
                    "contrastive_error_category": item.get(
                        "contrastive_error_category", ""
                    ),
                    "severity": item.get("severity", ""),
                }
            )

    return rows, key_rows


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    """Write rows to a UTF-8 CSV file with the given column order."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path, help="Path to the benchmark JSONL file")
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output CSV path (default: benchmark/pilot/pilot_annotation_sheet.csv)",
    )
    parser.add_argument(
        "--blind",
        action="store_true",
        help="Omit the candidate_type column and write a separate answer key",
    )
    args = parser.parse_args(argv)

    if not args.jsonl.is_file():
        print(f"ERROR: file not found: {args.jsonl}", file=sys.stderr)
        return 1

    try:
        items = read_items(args.jsonl)
    except json.JSONDecodeError as exc:
        print(f"ERROR: {args.jsonl} contains invalid JSON: {exc}", file=sys.stderr)
        return 1

    if not items:
        print(f"ERROR: {args.jsonl} contains no items.", file=sys.stderr)
        return 1

    rows, key_rows = build_rows(items, blind=args.blind)

    columns = list(CONTEXT_COLUMNS)
    if not args.blind:
        columns.append("candidate_type")
    columns.extend(EVALUATION_COLUMNS)

    write_csv(args.out, rows, columns)
    print(f"Wrote {len(rows)} candidate rows for {len(items)} items to {args.out}")

    if args.blind:
        key_path = args.out.with_suffix(".key.csv")
        write_csv(
            key_path,
            key_rows,
            [
                "candidate_id",
                "item_id",
                "candidate_type",
                "contrastive_error_category",
                "severity",
            ],
        )
        print(f"Wrote the answer key to {key_path} (keep this away from annotators)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
