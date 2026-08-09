#!/usr/bin/env python3
"""Measure inter-annotator agreement on a completed annotation CSV.

Computes, per rated dimension:

  * percentage agreement, averaged over annotator pairs within each unit;
  * Cohen's kappa, when exactly two annotators rated the dimension;
  * Krippendorff's alpha for nominal data, which tolerates missing ratings and
    any number of annotators.

The script never invents a score. When there is not enough data to compute a
statistic it says so and explains what is missing.

Usage:
    python scripts/calculate_agreement.py completed_annotations.csv
    python scripts/calculate_agreement.py <file.csv> --unit-column item_id
    python scripts/calculate_agreement.py <file.csv> --out agreement_report.md
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

# Cell values that mean "no rating given".
MISSING_VALUES = {"", "-", "na", "n/a", "none", "null"}

# Columns that identify a row rather than carry a rating.
METADATA_COLUMNS = {
    "item_id",
    "candidate_id",
    "candidate_type",
    "annotator_id",
    "adjudicator_id",
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
    "notes",
}


def is_missing(value) -> bool:
    """True when a cell carries no usable rating."""
    return value is None or str(value).strip().lower() in MISSING_VALUES


def read_rows(csv_path: Path) -> tuple[list[dict], list[str]]:
    """Read a CSV into a list of dicts, returning the rows and the header."""
    with Path(csv_path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def detect_rating_columns(header: list[str]) -> list[str]:
    """Every column that is not obviously metadata is treated as a rating."""
    return [column for column in header if column not in METADATA_COLUMNS]


def percentage_agreement(units: list[list]) -> float | None:
    """Mean pairwise exact-match rate across units with at least two ratings.

    Each unit contributes equally, regardless of how many annotators rated it.
    """
    per_unit = []
    for ratings in units:
        if len(ratings) < 2:
            continue
        pairs = list(combinations(ratings, 2))
        matches = sum(1 for left, right in pairs if left == right)
        per_unit.append(matches / len(pairs))
    if not per_unit:
        return None
    return sum(per_unit) / len(per_unit)


def cohens_kappa(pairs: list[tuple]) -> float | None:
    """Cohen's kappa for two annotators on nominal categories.

    Returns None when kappa is undefined, which happens when both annotators
    used exactly one category and expected agreement is therefore 1.0.
    """
    total = len(pairs)
    if total == 0:
        return None

    observed = sum(1 for left, right in pairs if left == right) / total

    categories = {value for pair in pairs for value in pair}
    expected = 0.0
    for category in categories:
        left_share = sum(1 for left, _ in pairs if left == category) / total
        right_share = sum(1 for _, right in pairs if right == category) / total
        expected += left_share * right_share

    if expected >= 1.0:
        return None
    return (observed - expected) / (1.0 - expected)


def krippendorff_alpha_nominal(units: list[list]) -> float | None:
    """Krippendorff's alpha for nominal data.

    Built from the coincidence matrix over units rated at least twice, following
    the standard nominal-difference formulation. Returns None when alpha is
    undefined (no usable units, or every rating falls in a single category).
    """
    usable = [ratings for ratings in units if len(ratings) >= 2]
    if not usable:
        return None

    coincidence: dict[tuple, float] = defaultdict(float)
    for ratings in usable:
        weight = 1.0 / (len(ratings) - 1)
        for i, left in enumerate(ratings):
            for j, right in enumerate(ratings):
                if i != j:
                    coincidence[(left, right)] += weight

    categories = sorted({value for ratings in usable for value in ratings}, key=str)
    marginals = {
        category: sum(coincidence.get((category, other), 0.0) for other in categories)
        for category in categories
    }
    grand_total = sum(marginals.values())
    if grand_total <= 1:
        return None

    observed_disagreement = sum(
        coincidence.get((left, right), 0.0)
        for left in categories
        for right in categories
        if left != right
    )
    expected_disagreement = sum(
        marginals[left] * marginals[right]
        for left in categories
        for right in categories
        if left != right
    ) / (grand_total - 1)

    if expected_disagreement == 0:
        return None
    return 1.0 - (observed_disagreement / expected_disagreement)


def analyse_dimension(
    rows: list[dict],
    dimension: str,
    unit_column: str,
    annotator_column: str,
) -> dict:
    """Collect ratings for one dimension and compute every applicable statistic."""
    # unit -> {annotator: rating}
    by_unit: dict[str, dict[str, str]] = defaultdict(dict)
    annotators: set[str] = set()

    for row in rows:
        rating = row.get(dimension)
        if is_missing(rating):
            continue
        unit = (row.get(unit_column) or "").strip()
        annotator = (row.get(annotator_column) or "").strip()
        if not unit or not annotator:
            continue
        by_unit[unit][annotator] = str(rating).strip()
        annotators.add(annotator)

    units = [list(ratings.values()) for ratings in by_unit.values()]
    multi_rated = [ratings for ratings in units if len(ratings) >= 2]

    result = {
        "dimension": dimension,
        "annotators": sorted(annotators),
        "units_with_any_rating": len(units),
        "units_with_two_or_more": len(multi_rated),
        "percentage_agreement": None,
        "cohens_kappa": None,
        "krippendorff_alpha": None,
        "note": "",
    }

    if not multi_rated:
        result["note"] = (
            "insufficient data: no unit was rated by two or more annotators"
        )
        return result

    result["percentage_agreement"] = percentage_agreement(multi_rated)
    result["krippendorff_alpha"] = krippendorff_alpha_nominal(multi_rated)

    if len(annotators) == 2:
        first, second = sorted(annotators)
        pairs = [
            (ratings[first], ratings[second])
            for ratings in by_unit.values()
            if first in ratings and second in ratings
        ]
        result["cohens_kappa"] = cohens_kappa(pairs)
        if result["cohens_kappa"] is None and pairs:
            result["note"] = (
                "Cohen's kappa is undefined: both annotators used a single category"
            )
    else:
        result["note"] = (
            f"Cohen's kappa not computed: it requires exactly 2 annotators, found "
            f"{len(annotators)}"
        )

    return result


def _format_score(value) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def format_report_text(results: list[dict], source_label: str, annotators: list[str]) -> str:
    """Render the agreement results as a plain-text console report."""
    lines = [
        "=" * 78,
        f"Inter-annotator agreement: {source_label}",
        "=" * 78,
        f"Annotators found: {len(annotators)} ({', '.join(annotators) if annotators else 'none'})",
        "",
        f"{'Dimension':<32}{'Units':>7}{'Pair%':>9}{'Kappa':>9}{'Alpha':>9}",
        "-" * 78,
    ]

    for result in results:
        lines.append(
            f"{result['dimension']:<32}"
            f"{result['units_with_two_or_more']:>7}"
            f"{_format_score(result['percentage_agreement']):>9}"
            f"{_format_score(result['cohens_kappa']):>9}"
            f"{_format_score(result['krippendorff_alpha']):>9}"
        )

    notes = [r for r in results if r["note"]]
    if notes:
        lines.extend(["", "Notes", "-" * 78])
        for result in notes:
            lines.append(f"  {result['dimension']}: {result['note']}")

    lines.extend(
        [
            "",
            "'Units' counts items rated by two or more annotators; only those",
            "contribute to the statistics. Pair% is mean pairwise exact agreement.",
            "",
        ]
    )
    return "\n".join(lines)


def format_report_markdown(
    results: list[dict], source_label: str, annotators: list[str]
) -> str:
    """Render the agreement results as a Markdown document."""
    lines = [
        "# Inter-Annotator Agreement Report",
        "",
        f"Generated by `scripts/calculate_agreement.py` from `{source_label}`.",
        "",
        f"**Annotators:** {len(annotators)}"
        + (f" ({', '.join(annotators)})" if annotators else ""),
        "",
        "| Dimension | Units rated 2+ times | Pairwise agreement | Cohen's kappa | Krippendorff's alpha |",
        "|---|---:|---:|---:|---:|",
    ]
    for result in results:
        lines.append(
            f"| `{result['dimension']}` | {result['units_with_two_or_more']} | "
            f"{_format_score(result['percentage_agreement'])} | "
            f"{_format_score(result['cohens_kappa'])} | "
            f"{_format_score(result['krippendorff_alpha'])} |"
        )

    notes = [r for r in results if r["note"]]
    if notes:
        lines.extend(["", "## Notes", ""])
        for result in notes:
            lines.append(f"- `{result['dimension']}`: {result['note']}")

    lines.extend(
        [
            "",
            "Only units rated by two or more annotators contribute to these statistics.",
            "`n/a` means the statistic could not be computed from the available data.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path, help="Completed annotation CSV")
    parser.add_argument(
        "--unit-column",
        default=None,
        help="Column identifying the rated unit (default: candidate_id, else item_id)",
    )
    parser.add_argument(
        "--annotator-column",
        default="annotator_id",
        help="Column identifying the annotator (default: annotator_id)",
    )
    parser.add_argument("--out", type=Path, default=None, help="Optional Markdown output path")
    args = parser.parse_args(argv)

    if not args.csv_path.is_file():
        print(f"ERROR: file not found: {args.csv_path}", file=sys.stderr)
        return 1

    rows, header = read_rows(args.csv_path)

    if not header:
        print(f"ERROR: {args.csv_path} has no header row.", file=sys.stderr)
        return 1

    unit_column = args.unit_column or (
        "candidate_id" if "candidate_id" in header else "item_id"
    )
    if unit_column not in header:
        print(
            f"ERROR: unit column '{unit_column}' not found. Available columns: "
            f"{', '.join(header)}",
            file=sys.stderr,
        )
        return 1
    if args.annotator_column not in header:
        print(
            f"ERROR: annotator column '{args.annotator_column}' not found. "
            f"Available columns: {', '.join(header)}",
            file=sys.stderr,
        )
        return 1

    if not rows:
        print(f"No annotation rows found in {args.csv_path}.")
        print(
            "This looks like an empty template. Agreement cannot be computed until "
            "at least two annotators have rated the same items."
        )
        return 0

    annotators = sorted(
        {
            (row.get(args.annotator_column) or "").strip()
            for row in rows
            if (row.get(args.annotator_column) or "").strip()
        }
    )

    if len(annotators) < 2:
        print(f"Read {len(rows)} row(s) from {args.csv_path}.")
        print(
            f"Insufficient data: agreement requires at least 2 annotators, but "
            f"found {len(annotators)}."
        )
        print("No agreement statistics have been computed. No scores are being estimated.")
        return 0

    rating_columns = detect_rating_columns(header)
    if not rating_columns:
        print("ERROR: no rating columns detected in the CSV header.", file=sys.stderr)
        return 1

    results = [
        analyse_dimension(rows, dimension, unit_column, args.annotator_column)
        for dimension in rating_columns
    ]
    # Report only dimensions that actually carry ratings.
    results = [r for r in results if r["units_with_any_rating"] > 0]

    if not results:
        print(f"Read {len(rows)} row(s) from {args.csv_path}.")
        print("Insufficient data: no rating columns contained any values.")
        return 0

    try:
        source_label = str(args.csv_path.resolve().relative_to(Path.cwd()))
    except ValueError:
        source_label = str(args.csv_path)

    print(format_report_text(results, source_label, annotators))

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            format_report_markdown(results, source_label, annotators), encoding="utf-8"
        )
        print(f"Wrote Markdown report to {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
