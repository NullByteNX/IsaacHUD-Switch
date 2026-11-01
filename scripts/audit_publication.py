#!/usr/bin/env python3
"""Verify source notices, preserved texts, runtime data and documentation links."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
for item in ["catalog/wiki_repentance.json", "catalog/catalog_it.json",
             "include/isaac/catalog_data.hpp", "include/isaac/collectible_quality_data.hpp"]:
    if (root / item).exists():
        raise SystemExit("Obsolete or unwanted generated dataset: " + item)
index = json.loads((root / "catalog/id_names.json").read_text(encoding="utf-8"))
assert len(index["entries"]) == 1004 and len(index["pills"]) == 50
for kind in ("entries", "pills"):
    for e in index[kind]:
        assert set(e) == ({"id", "name", "variant"} if kind == "entries" else {"id", "name"})
for rel in ["catalog/ATTRIBUZIONE.md", "catalog/ATTRIBUZIONE_TIER.md", "catalog/quality_source.json",
            "LICENSES/CC-BY-SA-4.0.txt", "LICENSES/ISC-libnx.txt", "LICENSES/MIT-original.txt",
            "NOTICE.md", "LICENSE", "third_party/SHA256SUMS.json", "docs/RIEPILOGO_MODIFICHE.md"]:
    assert (root / rel).is_file(), "Missing required file: " + rel
for manifest in ["third_party/SHA256SUMS.json", "docs/PRESERVED_SHA256.json"]:
    expected = json.loads((root / manifest).read_text(encoding="utf-8"))
    if "files" in expected:
        expected = expected["files"]
    for rel, digest in expected.items():
        assert hashlib.sha256((root / rel).read_bytes()).hexdigest() == digest, "Preserved file changed: " + rel
for script in ("generate_catalog.py", "generate_quality.py"):
    subprocess.run([sys.executable, str(root / "scripts" / script), "--check"], check=True)
for item in json.loads((root / "LICENSES/RUNTIME_SOURCES.json").read_text(encoding="utf-8")):
    assert hashlib.sha256((root / item["file"]).read_bytes()).hexdigest() == item["sha256"], "Runtime notice changed: " + item["file"]
sys.path.insert(0, str(root / "scripts"))
from package_sd import SOFTWARE_LICENSES
for rel in [*SOFTWARE_LICENSES, "docs/SOFTWARE_NOTICES.txt"]:
    assert (root / rel).is_file(), "Missing release notice: " + rel
# Project documentation is checked for broken relative Markdown links. Upstream
# vendored docs/notices remain byte-identical and are covered by their hashes.
documents = [root / "README.md", root / "NOTICE.md", root / "RELEASE_NOTES.md"]
documents += sorted((root / "docs").glob("*.md")) + sorted((root / "catalog").glob("*.md"))
for doc in documents:
    text = doc.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = target.strip("<>")
        if "://" in target or target.startswith("#"):
            continue
        path = target.split("#", 1)[0]
        if path:
            assert (doc.parent / path).is_file(), f"Broken documentation link: {doc.relative_to(root)} -> {target}"
print(f"Publication audit PASS: preserved licenses/texts, dependencies, runtime catalogs, {len(documents)} documentation files")
