#!/usr/bin/env python3
"""Check that benchmark/schema/item_schema.json is itself a valid JSON Schema.

This validates the *schema*, not any data. Run it after editing the schema and
before running validate_jsonl.py.

Usage:
    python scripts/validate_schema.py
    python scripts/validate_schema.py --schema path/to/item_schema.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA_PATH = REPO_ROOT / "benchmark" / "schema" / "item_schema.json"


def load_schema(schema_path: Path) -> dict:
    """Read and parse a JSON Schema file."""
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def check_schema(schema: dict) -> None:
    """Raise jsonschema.SchemaError if the schema is not a valid draft 2020-12 schema."""
    from jsonschema import Draft202012Validator

    Draft202012Validator.check_schema(schema)


def describe_schema(schema: dict) -> str:
    """Build a one-line summary of what the schema covers."""
    required = schema.get("required", [])
    enum_fields = [
        name
        for name, spec in schema.get("properties", {}).items()
        if "enum" in spec or "oneOf" in spec
    ]
    conditionals = len(schema.get("allOf", []))
    return (
        f"{len(schema.get('properties', {}))} properties, "
        f"{len(required)} required, "
        f"{len(enum_fields)} controlled-vocabulary fields, "
        f"{conditionals} conditional rules"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help="Path to the item schema (default: benchmark/schema/item_schema.json)",
    )
    args = parser.parse_args(argv)

    if not args.schema.is_file():
        print(f"ERROR: schema not found: {args.schema}", file=sys.stderr)
        return 1

    try:
        schema = load_schema(args.schema)
    except json.JSONDecodeError as exc:
        print(f"ERROR: {args.schema} is not valid JSON: {exc}", file=sys.stderr)
        return 1

    try:
        check_schema(schema)
    except ImportError:
        print(
            "ERROR: the 'jsonschema' package is required.\n"
            "       Install it with: python -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1
    except Exception as exc:  # jsonschema.SchemaError and friends
        print(f"ERROR: {args.schema} is not a valid JSON Schema:\n{exc}", file=sys.stderr)
        return 1

    version = schema.get("properties", {}).get("schema_version", {})
    print(f"OK: {args.schema.relative_to(REPO_ROOT)} is a valid draft 2020-12 JSON Schema.")
    print(f"    {describe_schema(schema)}")
    if version:
        print("    Schema version is recorded per item in the 'schema_version' field.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
