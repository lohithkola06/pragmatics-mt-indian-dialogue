"""Tests for scripts/validate_jsonl.py.

Run from the repository root with:
    python -m unittest discover scripts/tests
"""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_jsonl import validate_file  # noqa: E402

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def load_fixture(name: str) -> dict:
    """Read a fixture item from scripts/tests/fixtures/."""
    with (FIXTURES_DIR / name).open(encoding="utf-8") as handle:
        return json.load(handle)


class ValidateJsonlTestCase(unittest.TestCase):
    """Base class providing a scratch directory and a JSONL writer."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.valid_item = load_fixture("valid_item.json")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write_jsonl(self, items: list[dict], name: str = "items.jsonl") -> Path:
        """Write items to a JSONL file inside the scratch directory."""
        path = self.tmp_path / name
        with path.open("w", encoding="utf-8") as handle:
            for item in items:
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")
        return path

    def assertHasError(self, report, fragment: str) -> None:
        """Assert that some reported error message contains the given fragment."""
        messages = [error.message for error in report.errors]
        self.assertTrue(
            any(fragment in message for message in messages),
            msg=f"expected an error containing {fragment!r}, got: {messages}",
        )


class TestValidItems(ValidateJsonlTestCase):
    def test_valid_item_is_accepted(self) -> None:
        path = self.write_jsonl([self.valid_item])
        report = validate_file(path)

        self.assertTrue(report.ok, msg=f"unexpected errors: {report.errors}")
        self.assertEqual(report.total_lines, 1)
        self.assertEqual(report.valid_count, 1)
        self.assertEqual(report.invalid_count, 0)

    def test_multiple_distinct_items_are_accepted(self) -> None:
        second = copy.deepcopy(self.valid_item)
        second["item_id"] = "HIN_POL_002"
        path = self.write_jsonl([self.valid_item, second])
        report = validate_file(path)

        self.assertTrue(report.ok, msg=f"unexpected errors: {report.errors}")
        self.assertEqual(report.valid_count, 2)

    def test_blank_lines_are_ignored(self) -> None:
        path = self.tmp_path / "with_blanks.jsonl"
        with path.open("w", encoding="utf-8") as handle:
            handle.write(json.dumps(self.valid_item) + "\n")
            handle.write("\n")
        report = validate_file(path)

        self.assertTrue(report.ok)
        self.assertEqual(report.total_lines, 1)


class TestSchemaViolations(ValidateJsonlTestCase):
    def test_invalid_enum_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["severity"] = "SEVERE"  # not one of MINOR / MAJOR / CRITICAL
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertEqual(report.invalid_count, 1)
        self.assertHasError(report, "severity")

    def test_invalid_politeness_enum_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["politeness_level"] = "VERY_POLITE"
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "politeness_level")

    def test_missing_required_field_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        del item["preservation_requirement"]
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "preservation_requirement")

    def test_empty_reference_translations_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["reference_translations"] = []
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "reference_translations")

    def test_empty_source_utterance_text_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["source_utterance"]["text"] = ""
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)

    def test_malformed_item_id_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["item_id"] = "HINDI_POLITE_1"
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "item_id")

    def test_more_than_three_context_turns_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["context"] = [
            {"turn_id": n, "speaker_id": "A", "speaker_role": "Professor", "text": "Kuch to hai."}
            for n in range(1, 5)
        ]
        item["source_utterance"]["turn_id"] = 5
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "context")

    def test_invalid_fixture_file_is_rejected(self) -> None:
        """The committed invalid fixture must fail on several counts at once."""
        invalid_item = load_fixture("invalid_item.json")
        path = self.write_jsonl([invalid_item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertEqual(report.valid_count, 0)
        self.assertGreaterEqual(len(report.errors), 3)


class TestCrossFieldChecks(ValidateJsonlTestCase):
    def test_duplicate_item_id_is_rejected(self) -> None:
        duplicate = copy.deepcopy(self.valid_item)
        path = self.write_jsonl([self.valid_item, duplicate])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "duplicate item_id")

    def test_invalid_context_reference_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["relevant_context_turns"] = [3]  # only turn 1 exists
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "relevant_context_turns references turn 3")

    def test_context_window_larger_than_context_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["minimum_context_window"] = 3  # only one context turn present
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "minimum_context_window")

    def test_item_id_language_mismatch_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["item_id"] = "HNG_POL_001"  # prefix says Hinglish, language says Hindi
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "implies language")

    def test_item_id_category_mismatch_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["item_id"] = "HIN_STA_001"  # code says stance, phenomenon says politeness
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "implies primary_phenomenon")

    def test_non_sequential_context_turn_ids_are_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["context"][0]["turn_id"] = 2
        item["relevant_context_turns"] = [2]
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "not sequential")

    def test_code_switching_requires_a_real_function(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["item_id"] = "HNG_CSW_001"
        item["language"] = "Hinglish"
        item["translation_direction"] = "Hinglish-English"
        item["primary_phenomenon"] = "CODE_SWITCHING"
        item["code_switch_function"] = "NOT_APPLICABLE"
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "code_switch_function")

    def test_contrastive_identical_to_reference_is_rejected(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["contrastive_translation"] = item["reference_translations"][0]
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "identical to an accepted translation")

    def test_natural_source_requires_provenance(self) -> None:
        item = copy.deepcopy(self.valid_item)
        item["source_type"] = "NATURAL"
        item["source_reference"] = None
        path = self.write_jsonl([item])
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "source_reference")


class TestMalformedInput(ValidateJsonlTestCase):
    def test_unparseable_line_is_reported(self) -> None:
        path = self.tmp_path / "broken.jsonl"
        path.write_text('{"item_id": "HIN_POL_001",\n', encoding="utf-8")
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "invalid JSON")

    def test_non_object_line_is_reported(self) -> None:
        path = self.tmp_path / "array.jsonl"
        path.write_text("[1, 2, 3]\n", encoding="utf-8")
        report = validate_file(path)

        self.assertFalse(report.ok)
        self.assertHasError(report, "not a JSON object")


class TestPilotDataset(unittest.TestCase):
    """The committed pilot dataset must always validate."""

    def test_pilot_items_are_valid(self) -> None:
        pilot = SCRIPTS_DIR.parent / "benchmark" / "pilot" / "pilot_items_v1.jsonl"
        if not pilot.is_file():
            self.skipTest("pilot dataset not present")

        report = validate_file(pilot)
        self.assertTrue(
            report.ok,
            msg="pilot dataset failed validation: "
            + "; ".join(str(error) for error in report.errors[:5]),
        )
        self.assertEqual(report.invalid_count, 0)


if __name__ == "__main__":
    unittest.main()
