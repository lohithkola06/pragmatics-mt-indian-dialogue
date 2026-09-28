#!/usr/bin/env python3
"""Measure inter-annotator agreement on a completed annotation CSV.

Computes, per rated dimension:

  * percentage agreement, averaged over annotator pairs within each unit;
  * Cohen's kappa, when exactly two annotators rated the dimension;
  * Krippendorff's alpha for nominal data, which tolerates missing ratings and
    any number of annotators.

The script never invents a score. When there is not enough data to compute a
statistic it says so and explains what is missing.

Pass one CSV holding every annotator's rows, or one CSV per annotator (the
annotation app exports one file each). Files are combined; their headers must
match exactly.

Usage:
    python scripts/calculate_agreement.py ann_01.csv ann_02.csv
    python scripts/calculate_agreement.py combined.csv --out agreement_report.md
    python scripts/calculate_agreement.py <files> --where primary_phenomenon=CODE_SWITCHING
    python scripts/calculate_agreement.py review_*.csv \
        --unit-column item_id --annotator-column reviewer_id
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

# Columns that are recorded but never scored for agreement. Uncertainty flags
# are reported as usage counts instead: agreement computed only where both
# annotators happened to set a flag would say nothing. Suggestions are free text.
UNSCORED_COLUMNS = {
    "uncertainty_label",
    "suggested_indian_english_reference",
}

UNCERTAINTY_COLUMN = "uncertainty_label"


def is_missing(value) -> bool:
    """True when a cell carries no usable rating."""
    return value is None or str(value).strip().lower() in MISSING_VALUES


def read_rows(csv_path: Path) -> tuple[list[dict], list[str]]:
    """Read a CSV into a list of dicts, returning the rows and the header.

    Opened as utf-8-sig so a file re-saved by Excel ("CSV UTF-8", which adds a
    byte-order mark) still yields a clean first column name.
    """
    with Path(csv_path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def read_many(csv_paths: list[Path]) -> tuple[list[dict], list[str]]:
    """Read and concatenate several CSVs that share one header.

    Raises ValueError naming the first file whose header differs.
    """
    all_rows: list[dict] = []
    header: list[str] = []
    for index, path in enumerate(csv_paths):
        rows, this_header = read_rows(path)
        if index == 0:
            header = this_header
        elif this_header != header:
            missing = [c for c in header if c not in this_header]
            extra = [c for c in this_header if c not in header]
            detail = []
            if missing:
                detail.append(f"missing {', '.join(missing)}")
            if extra:
                detail.append(f"extra {', '.join(extra)}")
            if not detail:
                detail.append("same columns in a different order")
            raise ValueError(
                f"{path} has a different header from {csv_paths[0]} "
                f"({'; '.join(detail)})"
            )
        all_rows.extend(rows)
    return all_rows, header


def detect_rating_columns(header: list[str], exclude: tuple[str, ...] = ()) -> list[str]:
    """Columns treated as ratings: everything that is not metadata or unscored.

    The unit and annotator columns in use are always excluded, so an identifier
    such as reviewer_id is never scored as if it were a rating.
    """
    skipped = METADATA_COLUMNS | UNSCORED_COLUMNS | set(exclude)
    return [column for column in header if column not in skipped]


def find_duplicate_ratings(
    rows: list[dict], unit_column: str, annotator_column: str
) -> list[tuple[str, str, int]]:
    """(unit, annotator, count) for every unit an annotator rated more than once.

    Two files exported under the same annotator ID would otherwise silently
    collapse into one annotator.
    """
    counts: dict[tuple[str, str], int] = defaultdict(int)
    for row in rows:
        unit = (row.get(unit_column) or "").strip()
        annotator = (row.get(annotator_column) or "").strip()
        if unit and annotator:
            counts[(unit, annotator)] += 1
    return sorted((u, a, n) for (u, a), n in counts.items() if n > 1)


def apply_where(rows: list[dict], header: list[str], conditions: list[str]) -> list[dict]:
    """Keep only rows matching every COLUMN=VALUE condition (exact, trimmed).

    Raises ValueError for a malformed condition or an unknown column.
    """
    parsed = []
    for condition in conditions:
        column, sep, value = condition.partition("=")
        column, value = column.strip(), value.strip()
        if not sep or not column:
            raise ValueError(f"--where expects COLUMN=VALUE, got '{condition}'")
        if column not in header:
            raise ValueError(f"--where column '{column}' is not in the CSV header")
        parsed.append((column, value))
    return [
        row
        for row in rows
        if all((row.get(column) or "").strip() == value for column, value in parsed)
    ]


def uncertainty_usage(rows: list[dict], annotator_column: str) -> dict[str, dict[str, int]]:
    """{annotator: {flag: count}} for every non-empty uncertainty flag."""
    usage: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        flag = row.get(UNCERTAINTY_COLUMN)
        annotator = (row.get(annotator_column) or "").strip()
        if annotator and not is_missing(flag):
            usage[annotator][str(flag).strip()] += 1
    return {a: dict(sorted(f.items())) for a, f in sorted(usage.items())}


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


def format_report_text(
    results: list[dict],
    source_label: str,
    annotators: list[str],
    uncertainty: dict[str, dict[str, int]] | None = None,
) -> str:
    """Render the agreement results as a plain-text console report."""
    width = max([32] + [len(r["dimension"]) + 2 for r in results])
    lines = [
        "=" * 78,
        f"Inter-annotator agreement: {source_label}",
        "=" * 78,
        f"Annotators found: {len(annotators)} ({', '.join(annotators) if annotators else 'none'})",
        "",
        f"{'Dimension':<{width}}{'Units':>7}{'Pair%':>9}{'Kappa':>9}{'Alpha':>9}",
        "-" * 78,
    ]

    for result in results:
        lines.append(
            f"{result['dimension']:<{width}}"
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

    if uncertainty is not None:
        lines.extend(["", "Uncertainty flags (counted, not scored for agreement)", "-" * 78])
        if uncertainty:
            for annotator, flags in uncertainty.items():
                rendered = ", ".join(f"{flag}={count}" for flag, count in flags.items())
                lines.append(f"  {annotator}: {rendered}")
        else:
            lines.append("  none used")

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
    results: list[dict],
    source_label: str,
    annotators: list[str],
    uncertainty: dict[str, dict[str, int]] | None = None,
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

    if uncertainty is not None:
        lines.extend(["", "## Uncertainty flags", "",
                      "Counted rather than scored for agreement.", ""])
        if uncertainty:
            lines.extend(["| Annotator | Flags |", "|---|---|"])
            for annotator, flags in uncertainty.items():
                rendered = ", ".join(f"`{flag}` × {count}" for flag, count in flags.items())
                lines.append(f"| {annotator} | {rendered} |")
        else:
            lines.append("None used.")

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
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv_paths", type=Path, nargs="+",
                        help="Completed annotation CSV(s); one per annotator is fine")
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
    parser.add_argument(
        "--where",
        action="append",
        default=[],
        metavar="COLUMN=VALUE",
        help="Keep only rows where COLUMN equals VALUE. Repeatable.",
    )
    parser.add_argument("--out", type=Path, default=None, help="Optional Markdown output path")
    args = parser.parse_args(argv)

    for path in args.csv_paths:
        if not path.is_file():
            print(f"ERROR: file not found: {path}", file=sys.stderr)
            return 1

    try:
        rows, header = read_many(args.csv_paths)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not header:
        print(f"ERROR: {args.csv_paths[0]} has no header row.", file=sys.stderr)
        return 1

    unit_column = args.unit_column or (
        "candidate_id" if "candidate_id" in header else "item_id"
    )
    for label, column in (("unit", unit_column), ("annotator", args.annotator_column)):
        if column not in header:
            print(
                f"ERROR: {label} column '{column}' not found. Available columns: "
                f"{', '.join(header)}",
                file=sys.stderr,
            )
            return 1

    if args.where:
        try:
            rows = apply_where(rows, header, args.where)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

    source_label = ", ".join(str(path) for path in args.csv_paths)
    if args.where:
        source_label += f" (where {' and '.join(args.where)})"

    if not rows:
        print(f"No annotation rows found in {source_label}.")
        print(
            "This looks like an empty template or an over-narrow --where. Agreement "
            "cannot be computed until at least two annotators have rated the same items."
        )
        return 0

    duplicates = find_duplicate_ratings(rows, unit_column, args.annotator_column)
    if duplicates:
        print("ERROR: some units were rated more than once by the same annotator.",
              file=sys.stderr)
        print("Two files exported under one annotator ID would do this.", file=sys.stderr)
        for unit, annotator, count in duplicates[:10]:
            print(f"  {annotator} rated {unit} {count} times", file=sys.stderr)
        if len(duplicates) > 10:
            print(f"  ... and {len(duplicates) - 10} more", file=sys.stderr)
        return 1

    annotators = sorted(
        {
            (row.get(args.annotator_column) or "").strip()
            for row in rows
            if (row.get(args.annotator_column) or "").strip()
        }
    )

    if len(annotators) < 2:
        print(f"Read {len(rows)} row(s) from {source_label}.")
        print(
            f"Insufficient data: agreement requires at least 2 annotators, but "
            f"found {len(annotators)}."
        )
        print("No agreement statistics have been computed. No scores are being estimated.")
        return 0

    rating_columns = detect_rating_columns(
        header, exclude=(unit_column, args.annotator_column)
    )
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
        print(f"Read {len(rows)} row(s) from {source_label}.")
        print("Insufficient data: no rating columns contained any values.")
        return 0

    uncertainty = (
        uncertainty_usage(rows, args.annotator_column)
        if UNCERTAINTY_COLUMN in header
        else None
    )

    print(format_report_text(results, source_label, annotators, uncertainty))

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            format_report_markdown(results, source_label, annotators, uncertainty),
            encoding="utf-8",
        )
        print(f"Wrote Markdown report to {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
