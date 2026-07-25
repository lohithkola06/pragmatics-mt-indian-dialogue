#!/usr/bin/env python3
"""Summarise the composition of a benchmark JSONL file.

Reports totals and distributions across language, pragmatic category, source
type, context status, context window, severity, and review status, plus counts
of missing or empty fields.

Usage:
    python scripts/generate_dataset_statistics.py benchmark/pilot/pilot_items_v1.jsonl
    python scripts/generate_dataset_statistics.py <file.jsonl> --out benchmark/pilot/pilot_statistics.md
    python scripts/generate_dataset_statistics.py <file.jsonl> --out stats.json

The output format is inferred from the --out extension (.md or .json).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA_PATH = REPO_ROOT / "benchmark" / "schema" / "item_schema.json"

# (field name, human-readable heading) pairs reported as simple distributions.
DISTRIBUTIONS = [
    ("language", "Language"),
    ("primary_phenomenon", "Pragmatic category"),
    ("source_type", "Source type"),
    ("context_status", "Context status"),
    ("minimum_context_window", "Minimum context window"),
    ("severity", "Severity"),
    ("review_status", "Review status"),
    ("contrastive_error_category", "Contrastive error category"),
    ("speech_act", "Speech act"),
    ("politeness_level", "Politeness level"),
    ("formality_level", "Formality level"),
    ("relationship", "Relationship type"),
    ("code_switch_function", "Code-switch function"),
]


def read_items(jsonl_path: Path) -> list[dict]:
    """Load every JSON object from a JSONL file."""
    items: list[dict] = []
    with Path(jsonl_path).open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                items.append(json.loads(line))
    return items


def _is_empty(value) -> bool:
    """True when a field is present but carries no information."""
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, (list, dict)) and len(value) == 0:
        return True
    return False


def distribution(items: list[dict], field_name: str) -> dict:
    """Count values of one field, sorted by descending count then by value."""
    counter = Counter(
        "(null)" if item.get(field_name) is None else item.get(field_name)
        for item in items
    )
    return dict(sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0]))))


def cross_tabulate(items: list[dict], row_field: str, column_field: str) -> dict:
    """Build a nested {row: {column: count}} table."""
    table: dict = {}
    for item in items:
        row = str(item.get(row_field))
        column = str(item.get(column_field))
        table.setdefault(row, Counter())[column] += 1
    return {row: dict(sorted(counts.items())) for row, counts in sorted(table.items())}


def missing_field_counts(items: list[dict], required_fields: list[str]) -> dict:
    """Count, per required field, how many items omit it or leave it empty."""
    missing: dict[str, dict[str, int]] = {}
    for name in required_fields:
        absent = sum(1 for item in items if name not in item)
        empty = sum(1 for item in items if name in item and _is_empty(item[name]))
        if absent or empty:
            missing[name] = {"absent": absent, "empty": empty}
    return missing


def load_required_fields(schema_path: Path) -> list[str]:
    """Read the required-field list out of the item schema."""
    try:
        with Path(schema_path).open(encoding="utf-8") as handle:
            return json.load(handle).get("required", [])
    except (OSError, json.JSONDecodeError):
        return []


def collect_statistics(items: list[dict], required_fields: list[str]) -> dict:
    """Assemble every statistic reported by this script."""
    context_turn_counts = Counter(len(item.get("context") or []) for item in items)

    return {
        "total_items": len(items),
        "distributions": {
            field: distribution(items, field) for field, _label in DISTRIBUTIONS
        },
        "context_turns_present": dict(sorted(context_turn_counts.items())),
        "language_by_category": cross_tabulate(items, "language", "primary_phenomenon"),
        "category_by_source_type": cross_tabulate(
            items, "primary_phenomenon", "source_type"
        ),
        "missing_fields": missing_field_counts(items, required_fields),
    }


def _percentage(count: int, total: int) -> str:
    return f"{(100.0 * count / total):.1f}%" if total else "n/a"


def format_report_text(stats: dict, source_label: str) -> str:
    """Render the statistics as a plain-text console report."""
    total = stats["total_items"]
    lines = [
        "=" * 62,
        f"Dataset statistics: {source_label}",
        "=" * 62,
        f"Total items: {total}",
    ]

    for field, label in DISTRIBUTIONS:
        counts = stats["distributions"].get(field, {})
        if not counts:
            continue
        lines.append("")
        lines.append(f"{label} ({field})")
        lines.append("-" * 62)
        for value, count in counts.items():
            lines.append(f"  {str(value):<32} {count:>4}  {_percentage(count, total):>7}")

    lines.append("")
    lines.append("Context turns present per item")
    lines.append("-" * 62)
    for turns, count in stats["context_turns_present"].items():
        lines.append(f"  {turns} turn(s){'':<24} {count:>4}  {_percentage(count, total):>7}")

    lines.append("")
    lines.append("Language x category")
    lines.append("-" * 62)
    for language, row in stats["language_by_category"].items():
        rendered = ", ".join(f"{k}={v}" for k, v in row.items())
        lines.append(f"  {language:<12} {rendered}")

    lines.append("")
    lines.append("Missing or empty required fields")
    lines.append("-" * 62)
    if not stats["missing_fields"]:
        lines.append("  None. Every required field is present and non-empty.")
    else:
        for name, counts in sorted(stats["missing_fields"].items()):
            lines.append(
                f"  {name:<32} absent={counts['absent']} empty={counts['empty']}"
            )

    lines.append("")
    return "\n".join(lines)


def format_report_markdown(stats: dict, source_label: str) -> str:
    """Render the statistics as a Markdown document."""
    total = stats["total_items"]
    lines = [
        "# Pilot Dataset Statistics",
        "",
        f"Generated by `scripts/generate_dataset_statistics.py` from `{source_label}`.",
        "",
        "> These counts describe **draft, machine-generated items that have not been "
        "reviewed by a native speaker**. No inter-annotator agreement has been "
        "measured, because no annotation has taken place yet.",
        "",
        f"**Total items:** {total}",
        "",
    ]

    for field, label in DISTRIBUTIONS:
        counts = stats["distributions"].get(field, {})
        if not counts:
            continue
        lines.extend([f"## {label}", "", "| Value | Items | Share |", "|---|---:|---:|"])
        for value, count in counts.items():
            lines.append(f"| `{value}` | {count} | {_percentage(count, total)} |")
        lines.append("")

    lines.extend(
        ["## Context turns present per item", "", "| Context turns | Items | Share |", "|---|---:|---:|"]
    )
    for turns, count in stats["context_turns_present"].items():
        lines.append(f"| {turns} | {count} | {_percentage(count, total)} |")
    lines.append("")

    lines.extend(["## Language by category", "", "| Language | Category | Items |", "|---|---|---:|"])
    for language, row in stats["language_by_category"].items():
        for category, count in row.items():
            lines.append(f"| {language} | `{category}` | {count} |")
    lines.append("")

    lines.extend(
        ["## Category by source type", "", "| Category | Source type | Items |", "|---|---|---:|"]
    )
    for category, row in stats["category_by_source_type"].items():
        for source_type, count in row.items():
            lines.append(f"| `{category}` | `{source_type}` | {count} |")
    lines.append("")

    lines.extend(["## Missing or empty required fields", ""])
    if not stats["missing_fields"]:
        lines.append("None. Every required field is present and non-empty in every item.")
    else:
        lines.extend(
            [
                "An **absent** field is missing from the item and is always a defect. A field "
                "that is **present but empty** is often expected rather than wrong: "
                "`annotator_ids`, `annotator_notes` and `adjudicator_id` stay empty until "
                "annotation happens, `source_reference` is null for elicited items, "
                "`code_switch_function` is null for monolingual Hindi items, and `context` "
                "is empty for items that are interpretable without any previous turn.",
                "",
                "| Field | Absent | Present but empty |",
                "|---|---:|---:|",
            ]
        )
        for name, counts in sorted(stats["missing_fields"].items()):
            lines.append(f"| `{name}` | {counts['absent']} | {counts['empty']} |")
    lines.append("")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path, help="Path to the JSONL file to summarise")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional output file. Format inferred from the extension (.md or .json).",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help="Item schema, used to determine the required-field list",
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

    try:
        source_label = str(args.jsonl.resolve().relative_to(REPO_ROOT))
    except ValueError:
        source_label = str(args.jsonl)

    required_fields = load_required_fields(args.schema)
    stats = collect_statistics(items, required_fields)

    print(format_report_text(stats, source_label))

    if args.out:
        suffix = args.out.suffix.lower()
        if suffix == ".json":
            payload = json.dumps(stats, indent=2, ensure_ascii=False) + "\n"
        else:
            payload = format_report_markdown(stats, source_label)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
        print(f"Wrote {suffix.lstrip('.') or 'markdown'} report to {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
