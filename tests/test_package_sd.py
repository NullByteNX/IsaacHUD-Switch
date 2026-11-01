#!/usr/bin/env python3
"""Verify real packaging, credits, preservation and rejection before writes."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from package_sd import SOFTWARE_LICENSES, package


class PackageTests(unittest.TestCase):
    def test_data_only_then_binary_then_data_only_removes_stale_binary(self):
        with tempfile.TemporaryDirectory(prefix="isaac_package_") as directory:
            output = Path(directory) / "sdcard"
            status = package(output)
            self.assertFalse(status["binary_included"])
            data = output / "switch/IsaacHUD"
            for name in ["catalog_it.tsv", "collectible_quality.tsv"]:
                self.assertEqual((data / name).read_bytes(), (ROOT / "runtime" / name).read_bytes())
            self.assertEqual((data / "licenses/CC-BY-SA-4.0.txt").read_bytes(),
                             (ROOT / "LICENSES/CC-BY-SA-4.0.txt").read_bytes())
            self.assertIn("ATTRIBUZIONE", (data / "CREDITI.txt").read_text().upper())
            for source, name in SOFTWARE_LICENSES.items():
                self.assertEqual((ROOT / source).read_bytes(), (data / "licenses" / name).read_bytes())
            self.assertEqual((ROOT / "docs/SOFTWARE_NOTICES.txt").read_bytes(),
                             (data / "SOFTWARE_NOTICES.txt").read_bytes())
            self.assertEqual((ROOT / "NOTICE.md").read_bytes(), (data / "NOTICE.md").read_bytes())
            self.assertIn("releases/tag/v0.6.0", (data / "SOFTWARE_NOTICES.txt").read_text())
            fixture = Path(directory) / "fixture.ovl"
            fixture.write_bytes(b"SYNTHETIC PACKAGING FIXTURE, NOT A SWITCH BINARY\0"
                                b"/home/davem/projects/devkitpro/pacman-packages/devkita64/"
                                b"newlib/src/newlib-4.6.0.20260123/newlib/libc/stdlib/example.c\0")
            status = package(output, fixture, require_quality=True)
            self.assertTrue(status["binary_included"])
            binary = output / "switch/.overlays/IsaacHUD.ovl"
            self.assertEqual(binary.read_bytes(), fixture.read_bytes())
            package(output)
            self.assertFalse(binary.exists())
            for name,digest in json.loads((output / "SHA256SUMS.json").read_text()).items():
                self.assertEqual(hashlib.sha256((output / name).read_bytes()).hexdigest(),digest)

    def test_invalid_binary_or_unowned_output_is_rejected_without_changes(self):
        with tempfile.TemporaryDirectory(prefix="isaac_package_") as directory:
            output = Path(directory) / "sdcard"
            with self.assertRaises(ValueError):
                package(output, Path(directory) / "missing.ovl")
            self.assertFalse(output.exists())
            output.mkdir()
            keep = output / "keep.txt"
            keep.write_text("user file")
            with self.assertRaises(ValueError):
                package(output)
            self.assertEqual(keep.read_text(), "user file")

    def test_private_paths_block_packaging_without_modifying_binary_or_package(self):
        with tempfile.TemporaryDirectory(prefix="isaac_package_") as directory:
            output = Path(directory) / "sdcard"
            fixture = Path(directory) / "fixture.ovl"
            unsafe = b"SYNTHETIC\0E:/Users/Example/project/stb_truetype.h\0"
            fixture.write_bytes(unsafe)
            with self.assertRaisesRegex(ValueError, "Build privacy check FAILED"):
                package(output, fixture, require_quality=True)
            self.assertFalse(output.exists())
            self.assertEqual(fixture.read_bytes(), unsafe)
            package(output)
            before = {str(p.relative_to(output)): p.read_bytes()
                      for p in output.rglob("*") if p.is_file()}
            with self.assertRaisesRegex(ValueError, "Build privacy check FAILED"):
                package(output, fixture, require_quality=True)
            after = {str(p.relative_to(output)): p.read_bytes()
                     for p in output.rglob("*") if p.is_file()}
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
