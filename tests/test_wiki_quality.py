#!/usr/bin/env python3
"""Regression tests for version selection and refusal of an unreviewed export."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_quality import load_qualities
from import_wiki_quality import EXPECTED_SHA256, extract, import_snapshot


class WikiQualityTests(unittest.TestCase):
    def test_versioned_rows_use_repentance_first_and_preserve_zero(self):
        fixture = [{"gameId": 1, "qualityRaw": "0", "quality": 0},
                   {"gameId": 2, "qualityRaw": "2 3", "quality": 2},
                   {"gameId": 3, "qualityRaw": "4 3", "quality": 4}]
        values, versioned = extract(fixture, {1, 2, 3})
        self.assertEqual(values, {1: 0, 2: 2, 3: 4})
        self.assertEqual(versioned, 2)

    def test_unreviewed_snapshot_hash_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            import_snapshot(b"[]", set())

    def test_ambiguous_duplicate_and_incomplete_exports_are_rejected(self):
        for fixture in [
            [{"gameId": 1, "qualityRaw": "2 3 4", "quality": 2}],
            [{"gameId": 1, "qualityRaw": "2 3", "quality": 3}],
            [{"gameId": 1, "qualityRaw": "unknown", "quality": None}],
            [{"gameId": 1, "qualityRaw": "4", "quality": 4}]*2,
            [{"gameId": 2, "qualityRaw": "4", "quality": 4}], []]:
            with self.subTest(fixture=fixture), self.assertRaises(ValueError):
                extract(fixture, {1})

    def test_distributed_snapshot_profile_and_provenance(self):
        names = json.loads((ROOT / "catalog/id_names.json").read_text())
        expected = {e["id"] for e in names["entries"] if e["variant"] == 100}
        values = load_qualities(ROOT / "catalog/collectible_quality.tsv", expected)
        p = json.loads((ROOT / "catalog/quality_source.json").read_text())
        self.assertEqual(set(values), expected)
        self.assertEqual(p["inputs"][0]["sha256"], EXPECTED_SHA256)
        self.assertEqual(p["versioned_rows_selected"], 143)
        self.assertEqual(p["license"], "CC-BY-SA-4.0")
        self.assertEqual({i:values[i] for i in [234,292,562,706]}, {234:3,292:4,562:3,706:4})
        self.assertIn("not Repentance+", p["game_version"])


if __name__ == "__main__":
    unittest.main()
