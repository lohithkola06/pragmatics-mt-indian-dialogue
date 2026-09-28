"""Tests for scripts/calculate_agreement.py.

These check the agreement statistics against hand-computable cases and against
Krippendorff's own published worked example, so the alpha implementation is not
taken on trust.

Run from the repository root with:
    python -m unittest discover scripts/tests
"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import calculate_agreement  # noqa: E402
from calculate_agreement import (  # noqa: E402
    apply_where,
    cohens_kappa,
    detect_rating_columns,
    find_duplicate_ratings,
    is_missing,
    krippendorff_alpha_nominal,
    percentage_agreement,
    read_many,
    read_rows,
    uncertainty_usage,
)


class TestPercentageAgreement(unittest.TestCase):
    def test_perfect_agreement(self) -> None:
        units = [["3", "3"], ["2", "2"], ["0", "0"]]
        self.assertAlmostEqual(percentage_agreement(units), 1.0)

    def test_total_disagreement(self) -> None:
        units = [["3", "0"], ["2", "1"]]
        self.assertAlmostEqual(percentage_agreement(units), 0.0)

    def test_half_agreement(self) -> None:
        units = [["3", "3"], ["2", "1"]]
        self.assertAlmostEqual(percentage_agreement(units), 0.5)

    def test_three_annotators_partial_agreement(self) -> None:
        # Pairs are (3,3), (3,2), (3,2): one of three pairs matches.
        units = [["3", "3", "2"]]
        self.assertAlmostEqual(percentage_agreement(units), 1 / 3)

    def test_single_rating_units_are_ignored(self) -> None:
        self.assertIsNone(percentage_agreement([["3"], ["2"]]))


class TestCohensKappa(unittest.TestCase):
    def test_perfect_agreement_is_one(self) -> None:
        pairs = [("a", "a"), ("b", "b"), ("a", "a"), ("b", "b")]
        self.assertAlmostEqual(cohens_kappa(pairs), 1.0)

    def test_chance_level_agreement_is_near_zero(self) -> None:
        # Both annotators split 50/50 and agree exactly half the time.
        pairs = [("a", "a"), ("a", "b"), ("b", "a"), ("b", "b")]
        self.assertAlmostEqual(cohens_kappa(pairs), 0.0)

    def test_known_value(self) -> None:
        # 2x2 table: both agree 'a' 20 times, both 'b' 15 times,
        # A says 'a' while B says 'b' 5 times, and the reverse 10 times.
        # p_o = 0.70, p_e = 0.25*0.30 + 0.75*0.70 ... computed below.
        pairs = (
            [("a", "a")] * 20 + [("b", "b")] * 15 + [("a", "b")] * 5 + [("b", "a")] * 10
        )
        total = len(pairs)
        observed = 35 / total
        a_left = 25 / total
        b_left = 25 / total
        a_right = 30 / total
        b_right = 20 / total
        expected = a_left * a_right + b_left * b_right
        self.assertAlmostEqual(
            cohens_kappa(pairs), (observed - expected) / (1 - expected)
        )

    def test_single_category_is_undefined(self) -> None:
        self.assertIsNone(cohens_kappa([("a", "a"), ("a", "a")]))

    def test_empty_input_is_undefined(self) -> None:
        self.assertIsNone(cohens_kappa([]))


class TestKrippendorffAlpha(unittest.TestCase):
    def test_perfect_agreement_is_one(self) -> None:
        units = [["a", "a"], ["b", "b"], ["a", "a"], ["b", "b"]]
        self.assertAlmostEqual(krippendorff_alpha_nominal(units), 1.0)

    def test_three_observer_example_with_missing_values(self) -> None:
        """A three-observer, twelve-unit example with missing ratings.

        The reliability matrix is:

            unit:  1  2  3  4  5  6  7  8  9 10 11 12
            A:     1  2  3  3  2  1  4  1  2  .  .  .
            B:     1  2  3  3  2  2  4  1  2  5  .  .
            C:     .  3  3  3  2  3  4  2  2  5  1  3

        Units 11 and 12 carry a single rating each and are dropped, as the
        method requires. The expected value below is derived by hand from the
        coincidence matrix rather than copied from a library:

            marginals   n1=5, n2=10, n3=8, n4=3, n5=2, n=28
            observed    D_o = 7
            expected    D_e = (28^2 - (25+100+64+9+4)) / 27 = 582/27 = 21.5556
            alpha       1 - 7/21.5556 = 0.6753
        """
        units = [
            ["1", "1"],
            ["2", "2", "3"],
            ["3", "3", "3"],
            ["3", "3", "3"],
            ["2", "2", "2"],
            ["1", "2", "3"],
            ["4", "4", "4"],
            ["1", "1", "2"],
            ["2", "2", "2"],
            ["5", "5"],
            ["1"],
            ["3"],
        ]
        alpha = krippendorff_alpha_nominal(units)
        self.assertIsNotNone(alpha)
        self.assertAlmostEqual(alpha, 1 - 7 / (582 / 27), places=6)
        self.assertAlmostEqual(alpha, 0.6753, places=4)

    def test_balanced_two_by_two_matches_hand_computation(self) -> None:
        """Two annotators, 50% agreement, balanced marginals.

            o[a,a]=2, o[b,b]=2, o[a,b]=2, o[b,a]=2 -> n_a = n_b = 4, n = 8
            D_o = 4;  D_e = (8^2 - (16+16))/7 = 32/7
            alpha = 1 - 4/(32/7) = 0.125

        The small positive value is the expected small-sample behaviour of the
        (n-1) correction; alpha tends to 0 as the number of units grows.
        """
        units = [["a", "a"], ["b", "b"], ["a", "b"], ["b", "a"]]
        self.assertAlmostEqual(krippendorff_alpha_nominal(units), 1 - 4 / (32 / 7))

    def test_single_category_is_undefined(self) -> None:
        # Every rating identical: expected disagreement is zero, so alpha is undefined.
        self.assertIsNone(krippendorff_alpha_nominal([["a", "a"], ["a", "a"]]))

    def test_no_multiply_rated_units_is_undefined(self) -> None:
        self.assertIsNone(krippendorff_alpha_nominal([["a"], ["b"]]))

    def test_empty_input_is_undefined(self) -> None:
        self.assertIsNone(krippendorff_alpha_nominal([]))


class TestMissingValues(unittest.TestCase):
    def test_recognised_missing_markers(self) -> None:
        for value in ("", "  ", "NA", "n/a", "None", "-", None):
            with self.subTest(value=value):
                self.assertTrue(is_missing(value))

    def test_real_ratings_are_not_missing(self) -> None:
        for value in ("0", "1", "2", "3", "UNCERTAIN"):
            with self.subTest(value=value):
                self.assertFalse(is_missing(value))


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class TestMultipleFilesAndFilters(unittest.TestCase):
    """Features needed for per-annotator exports from the annotation app."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, name: str, text: str, bom: bool = False) -> Path:
        path = self.tmp / name
        data = text.encode("utf-8")
        path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + data)
        return path

    def test_bom_from_excel_does_not_corrupt_the_first_column(self) -> None:
        path = self.write("bom.csv", "item_id,annotator_id,score\r\nX,ANN_01,3\r\n", bom=True)
        rows, header = read_rows(path)
        self.assertEqual(header[0], "item_id")
        self.assertEqual(rows[0]["item_id"], "X")

    def test_read_many_concatenates_files(self) -> None:
        a = self.write("a.csv", "item_id,annotator_id,score\nX,ANN_01,3\n")
        b = self.write("b.csv", "item_id,annotator_id,score\nX,ANN_02,2\n")
        rows, header = read_many([a, b])
        self.assertEqual(len(rows), 2)
        self.assertEqual(header, ["item_id", "annotator_id", "score"])

    def test_read_many_rejects_mismatched_headers(self) -> None:
        a = self.write("a.csv", "item_id,annotator_id,score\n")
        b = self.write("b.csv", "item_id,annotator_id,other\n")
        with self.assertRaises(ValueError):
            read_many([a, b])

    def test_duplicate_unit_annotator_pairs_are_found(self) -> None:
        rows = [
            {"u": "X", "a": "ANN_01"},
            {"u": "X", "a": "ANN_01"},
            {"u": "X", "a": "ANN_02"},
        ]
        self.assertEqual(find_duplicate_ratings(rows, "u", "a"), [("X", "ANN_01", 2)])

    def test_unit_and_annotator_columns_are_never_rated(self) -> None:
        header = ["item_id", "reviewer_id", "source_is_natural", "notes"]
        rated = detect_rating_columns(header, exclude=("item_id", "reviewer_id"))
        self.assertEqual(rated, ["source_is_natural"])

    def test_uncertainty_and_suggestions_are_not_rated(self) -> None:
        header = ["candidate_id", "annotator_id", "semantic_adequacy",
                  "uncertainty_label", "suggested_indian_english_reference"]
        self.assertEqual(detect_rating_columns(header), ["semantic_adequacy"])

    def test_where_keeps_matching_rows(self) -> None:
        rows = [{"lang": "Hindi"}, {"lang": "Hinglish"}, {"lang": " Hinglish "}]
        kept = apply_where(rows, ["lang"], ["lang=Hinglish"])
        self.assertEqual(len(kept), 2)

    def test_where_rejects_unknown_column_and_bad_syntax(self) -> None:
        with self.assertRaises(ValueError):
            apply_where([], ["lang"], ["nope=1"])
        with self.assertRaises(ValueError):
            apply_where([], ["lang"], ["lang"])

    def test_uncertainty_usage_counts_flags_per_annotator(self) -> None:
        rows = [
            {"annotator_id": "ANN_01", "uncertainty_label": "UNCERTAIN"},
            {"annotator_id": "ANN_01", "uncertainty_label": ""},
            {"annotator_id": "ANN_02", "uncertainty_label": "UNCERTAIN"},
            {"annotator_id": "ANN_02", "uncertainty_label": "UNCERTAIN"},
        ]
        self.assertEqual(
            uncertainty_usage(rows, "annotator_id"),
            {"ANN_01": {"UNCERTAIN": 1}, "ANN_02": {"UNCERTAIN": 2}},
        )


class TestAppExportFixtures(unittest.TestCase):
    """End to end: the app's exact export format runs through the script."""

    def run_main(self, args: list[str]) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = calculate_agreement.main(args)
        return code, out.getvalue()

    def test_stage2_exports_from_two_annotators(self) -> None:
        code, output = self.run_main([
            str(FIXTURES / "app_export_stage2_ANN_01.csv"),
            str(FIXTURES / "app_export_stage2_ANN_02.csv"),
        ])
        self.assertEqual(code, 0)
        self.assertIn("Annotators found: 2", output)
        self.assertIn("semantic_adequacy", output)
        self.assertIn("Uncertainty flags", output)
        dimension_lines = [l for l in output.splitlines() if l.startswith("uncertainty_label")]
        self.assertEqual(dimension_lines, [], msg="uncertainty_label must not be scored")

    def test_stage1_exports_with_reviewer_column(self) -> None:
        code, output = self.run_main([
            str(FIXTURES / "app_export_stage1_ANN_01.csv"),
            str(FIXTURES / "app_export_stage1_ANN_02.csv"),
            "--unit-column", "item_id",
            "--annotator-column", "reviewer_id",
        ])
        self.assertEqual(code, 0)
        self.assertIn("recommended_action", output)
        for line in output.splitlines():
            self.assertFalse(line.startswith(("reviewer_id", "suggested_indian")), msg=line)

    def test_same_file_twice_is_rejected_as_duplicate(self) -> None:
        path = str(FIXTURES / "app_export_stage2_ANN_01.csv")
        code, _ = self.run_main([path, path])
        self.assertEqual(code, 1)

    def test_where_restricts_code_switch_scoring(self) -> None:
        code, output = self.run_main([
            str(FIXTURES / "app_export_stage2_ANN_01.csv"),
            str(FIXTURES / "app_export_stage2_ANN_02.csv"),
            "--where", "primary_phenomenon=CODE_SWITCHING",
        ])
        self.assertEqual(code, 0)
        self.assertIn("insufficient data", output)


if __name__ == "__main__":
    unittest.main()
