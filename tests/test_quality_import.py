#!/usr/bin/env python3
"""Importer regressions: namespace collisions, zero, overrides and bad inputs."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_quality import load_qualities, render
from import_quality import prepare_import
from isaac_test_fixture import synthetic_qualities


class ImportQualityTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="isaac_quality_")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def source(self, content, name="metadata.xml"):
        path = self.root / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_zero_is_valid_and_trinket_namespace_is_ignored(self):
        path = self.source('<items><item id="1" quality="0"/><trinket id="1" quality="4"/>'
                           '<item id="2" quality="2" craftquality="4"/></items>')
        tsv, provenance, _ = prepare_import([("metadata", path)], {1, 2}, "test fixture")
        self.assertIn("1\t0\n", tsv)
        self.assertIn("2\t2\n", tsv)
        self.assertEqual(provenance["status"], "complete")
        self.assertNotIn(str(path.parent), json.dumps(provenance))
        self.assertEqual(len(provenance["inputs"][0]["sha256"]), 64)

    def test_explicit_overrides_win_without_max_quality_merge(self):
        base = self.source('<items><item id="1" quality="4"/></items>')
        patch = self.source('<items><item id="1" quality="2"/></items>', "metadata2.xml")
        item = self.source('<items><passive id="1" quality="1"/><trinket id="1" quality="4"/></items>',
                           "items.xml")
        tsv, _, _ = prepare_import([("metadata", base), ("metadata", patch), ("items", item)], {1}, "fixture")
        self.assertIn("1\t1\n", tsv)

    def test_incomplete_is_rejected_unless_explicit(self):
        path = self.source('<items><item id="1" quality="0"/></items>')
        with self.assertRaisesRegex(ValueError, "Missing 1"):
            prepare_import([("metadata", path)], {1, 2}, "fixture")
        _, provenance, _ = prepare_import([("metadata", path)], {1, 2}, "fixture", True)
        self.assertEqual(provenance["missing_ids"], [2])
        self.assertEqual(provenance["status"], "partial")

    def test_malformed_and_duplicate_values_are_rejected(self):
        for xml in ['<items><item id="1" quality="5"/></items>',
                    '<items><item id="1" quality="-1"/></items>',
                    '<items><item id="1" quality="0"/><item id="1" quality="4"/></items>',
                    '<items><item id="1" quality="x"/></items>',
                    '<items><item id="1" craftquality="4"/></items>',
                    '<trinkets><item id="1" quality="4"/></trinkets>',
                    '<!DOCTYPE items [<!ENTITY a "4">]><items/>']:
            with self.subTest(xml=xml), self.assertRaises(ValueError):
                prepare_import([("metadata", self.source(xml))], {1}, "fixture")

    def test_full_synthetic_import_builds_every_lookup(self):
        fixtures = synthetic_qualities(ROOT)
        path = self.source('<items>' + ''.join(f'<item id="{i}" quality="{q}"/>'
                            for i, q in fixtures.items()) + '</items>')
        tsv, provenance, header = prepare_import([("metadata", path)], set(fixtures), "SYNTHETIC TEST ONLY")
        self.assertEqual(provenance["collectibles"], 719)
        data = self.source(tsv, "table.tsv")
        self.assertEqual(load_qualities(data, set(fixtures)), fixtures)
        self.assertEqual(header, render(fixtures))
        quality_file = self.root / "runtime-quality.tsv"
        quality_file.write_text(header,encoding="utf-8")
        binary = self.root / "quality-test"
        subprocess.run(["g++", "-std=c++20", "-O2", "-Wall", "-Wextra", "-Wpedantic", "-Werror",
                        "-I" + str(ROOT / "include"), str(ROOT / "tests/test_quality.cpp"),
                        "-o", str(binary)], check=True)
        subprocess.run([str(binary),str(quality_file)],check=True,timeout=10)



if __name__ == "__main__":
    unittest.main()
