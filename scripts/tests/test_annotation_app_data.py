"""Tests for scripts/build_annotation_app_data.py and the app's export contract.

Run from the repository root with:
    python -m unittest discover scripts/tests
"""

from __future__ import annotations

import copy
import csv
import json
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_annotation_app_data as app_data  # noqa: E402
from create_annotation_sheet import read_items  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
REPO_ROOT = SCRIPTS_DIR.parent


def load_items() -> list[dict]:
    return read_items(app_data.DEFAULT_JSONL)


def load_config() -> dict:
    return app_data.load_config(app_data.DEFAULT_CONFIG)


class TestGuidelinesNotPrimed(unittest.TestCase):
    """Annotators read these docs before rating; none may quote a pilot item."""

    def test_synced_docs_do_not_quote_pilot_items(self) -> None:
        hits = app_data.find_priming(load_items(), app_data.load_docs(load_config()))
        self.assertEqual(
            hits,
            [],
            msg="annotator-facing docs quote pilot items:\n" + "\n".join(map(str, hits)),
        )

    def test_guard_catches_a_quoted_source_utterance(self) -> None:
        items = load_items()
        quoted = items[0]["source_utterance"]["text"]
        hits = app_data.find_priming(items, {"planted.md": f"Example: `{quoted}`"})
        self.assertTrue(any(h.item_id == items[0]["item_id"] for h in hits))

    def test_guard_catches_a_lightly_edited_quote(self) -> None:
        """A four-word run is enough; editing the start of the sentence doesn't hide it."""
        items = load_items()
        words = items[0]["source_utterance"]["text"].split()
        edited = "Well " + " ".join(words[1:])
        hits = app_data.find_priming(items, {"planted.md": edited})
        self.assertTrue(any(h.item_id == items[0]["item_id"] for h in hits))

    def test_guard_catches_a_quoted_contrastive_translation(self) -> None:
        items = load_items()
        text = next(i for i in items if len(i["contrastive_translation"].split()) >= 4)
        hits = app_data.find_priming(items, {"planted.md": text["contrastive_translation"]})
        self.assertTrue(any(h.field == "contrastive_translation" for h in hits))

    def test_guard_catches_a_cited_item_id(self) -> None:
        items = load_items()
        hits = app_data.find_priming(items, {"planted.md": f"See ({items[3]['item_id']})."})
        self.assertTrue(any(h.field == "item_id" for h in hits))

    def test_unrelated_text_is_not_flagged(self) -> None:
        hits = app_data.find_priming(
            load_items(), {"planted.md": "Sir, kya main kal chhutti le sakta hoon?"}
        )
        self.assertEqual(hits, [])


class TestGeneratedData(unittest.TestCase):
    def test_generated_app_data_is_up_to_date(self) -> None:
        outputs, problems = app_data.build()
        self.assertEqual(problems, [])
        stale = app_data.check_outputs(outputs, app_data.DEFAULT_OUT_DIR)
        self.assertEqual(
            stale,
            [],
            msg="run: python scripts/build_annotation_app_data.py\n" + "\n".join(stale),
        )

    def test_stage2_has_two_candidates_per_item_in_canonical_order(self) -> None:
        items = load_items()
        units = json.loads((app_data.DEFAULT_OUT_DIR / "stage2_units.json").read_text())
        self.assertEqual(len(units), 2 * len(items))
        expected = [f"{i['item_id']}-{s}" for i in items for s in ("A", "B")]
        self.assertEqual([u["candidate_id"] for u in units], expected)

    def test_display_items_omit_severity_and_creator_notes(self) -> None:
        shown = json.loads((app_data.DEFAULT_OUT_DIR / "items.json").read_text())
        for item in shown:
            self.assertNotIn("severity", item)
            self.assertNotIn("creator_notes", item)

    def test_item_hash_changes_when_an_item_changes(self) -> None:
        item = load_items()[0]
        edited = copy.deepcopy(item)
        edited["reference_translations"][0] += " (revised)"
        self.assertNotEqual(app_data.item_hash(item), app_data.item_hash(edited))


class TestConfig(unittest.TestCase):
    def test_committed_config_is_valid(self) -> None:
        self.assertEqual(app_data.validate_config(load_config(), load_items()), [])

    def test_minimal_pair_calibration_item_is_rejected(self) -> None:
        items = load_items()
        config = load_config()
        pair = next(i["item_id"] for i in items if i["source_type"] == "MINIMAL_PAIR")
        config["calibration_items"] = config["calibration_items"][:-1] + [pair]
        problems = app_data.validate_config(config, items)
        self.assertTrue(any("minimal pair" in p for p in problems))

    def test_unknown_calibration_item_is_rejected(self) -> None:
        config = load_config()
        config["calibration_items"] = ["HIN_POL_999"]
        problems = app_data.validate_config(config, load_items())
        self.assertTrue(any("not in the pilot set" in p for p in problems))

    def test_calibration_must_cover_code_switching(self) -> None:
        items = load_items()
        config = load_config()
        config["calibration_items"] = [
            i for i in config["calibration_items"]
            if not i.startswith("HNG_CSW")
        ]
        problems = app_data.validate_config(config, items)
        self.assertTrue(any("code-switching" in p for p in problems))


class TestExportContract(unittest.TestCase):
    """The committed fixture CSVs are exactly what the app must write."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads((FIXTURES / "app_export_fixture.json").read_text())

    def test_review_template_header_matches_review_columns(self) -> None:
        template = REPO_ROOT / "benchmark" / "pilot" / "pilot_item_review_template.csv"
        with template.open(encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle))
        self.assertEqual(header, app_data.REVIEW_COLUMNS)

    def test_stage2_fixtures_match_the_reference_renderer(self) -> None:
        units = self.fixture["stage2_units"]
        for annotator, ratings in self.fixture["stage2_ratings"].items():
            expected = app_data.render_stage2_csv(units, ratings, annotator).encode("utf-8")
            actual = (FIXTURES / f"app_export_stage2_{annotator}.csv").read_bytes()
            self.assertEqual(actual, expected, msg=f"stage 2 fixture for {annotator}")

    def test_stage1_fixtures_match_the_reference_renderer(self) -> None:
        items = self.fixture["review_items"]
        for reviewer, reviews in self.fixture["reviews"].items():
            expected = app_data.render_review_csv(items, reviews, reviewer).encode("utf-8")
            actual = (FIXTURES / f"app_export_stage1_{reviewer}.csv").read_bytes()
            self.assertEqual(actual, expected, msg=f"stage 1 fixture for {reviewer}")

    def test_fixtures_have_no_bom_and_use_crlf(self) -> None:
        for path in FIXTURES.glob("app_export_stage*.csv"):
            data = path.read_bytes()
            self.assertFalse(data.startswith(b"\xef\xbb\xbf"), msg=path.name)
            self.assertTrue(data.endswith(b"\r\n"), msg=path.name)

    def test_stage2_fixture_header_is_the_blind_sheet(self) -> None:
        with (FIXTURES / "app_export_stage2_ANN_01.csv").open(encoding="utf-8", newline="") as h:
            header = next(csv.reader(h))
        self.assertEqual(header, app_data.STAGE2_COLUMNS)
        self.assertNotIn("candidate_type", header)


if __name__ == "__main__":
    unittest.main()
