#!/usr/bin/env python3
"""Import only ID/quality pairs from a pinned CC BY-SA wiki-derived snapshot.

The original wiki page is not directly downloadable in every environment.
This known snapshot preserves qualityRaw before Repentance+ filtering. Do not
replace it with current/main: that export retains only Repentance+ values.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import urllib.request

from generate_quality import ROOT, render

COMMIT = "0026f8343069f689582176cf7b061743ea7decb6"
REPOSITORY = "https://github.com/lubna-ishaq/binding-of-isaac-oracle"
SOURCE_PATH = "frontend/src/data/items.generated.json"
URL = f"https://raw.githubusercontent.com/lubna-ishaq/binding-of-isaac-oracle/{COMMIT}/{SOURCE_PATH}"
EXPECTED_SHA256 = "fd4cd09b981b41e5543331ce7f175b0dadc7d49968f0c2d48543fb6e2e982c54"
WIKI = "https://bindingofisaacrebirth.wiki.gg/wiki/Items"
POLICY_COMMIT = "5845596d8038c924871979a439b6d5e3ac588cc9"
POLICY_URL = f"{REPOSITORY}/blob/{POLICY_COMMIT}/SOURCES.md"


def extract(snapshot, expected):
    if not isinstance(snapshot, list):
        raise ValueError("Expected a JSON list")
    qualities, versioned = {}, 0
    for entry in snapshot:
        item_id = entry["gameId"]
        raw = entry["qualityRaw"]
        if type(item_id) is not int or item_id not in expected or item_id in qualities:
            raise ValueError("Unknown/duplicate collectible in wiki snapshot")
        if not isinstance(raw, str) or not re.fullmatch(r"[0-4](?:\s+[0-4])?", raw):
            raise ValueError(f"Ambiguous or missing quality for {item_id}")
        values = [int(value) for value in raw.split()]
        if type(entry["quality"]) is not int or entry["quality"] != values[0]:
            raise ValueError(f"Unexpected qualityRaw ordering for {item_id}")
        # In this EXACT pinned snapshot, first=Repentance and, when present,
        # second=Repentance+. Attribution documents the version checks.
        qualities[item_id] = values[0]
        versioned += len(values) > 1
    if set(qualities) != expected:
        raise ValueError("Incomplete wiki collectible coverage")
    return qualities, versioned


def import_snapshot(raw, expected):
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("Snapshot hash mismatch: only the reviewed pinned revision is accepted")
    qualities, versioned = extract(json.loads(raw), expected)
    if versioned != 143:
        raise ValueError("Unexpected number of versioned quality rows")
    provenance = {
        "format": "isaac-hud-quality-source-v1", "status": "complete",
        "source_kind": "wiki_export", "license": "CC-BY-SA-4.0",
        "collectibles": len(qualities), "expected_collectibles": len(expected),
        "game_version": "Repentance (not Repentance+), wiki snapshot profile",
        "game_version_verification": "Repentance values selected from the cited wiki snapshot; runtime compatibility is documented separately",
        "wiki_page": WIKI,
        "wiki_revision": None,
        "wiki_revision_note": "The acquired source is identified by the pinned intermediate commit, path and SHA-256",
        "wiki_contributors": "https://bindingofisaacrebirth.wiki.gg/index.php?title=Items&action=history",
        "wiki_license_policy": "https://bindingofisaacrebirth.wiki.gg/wiki/The_Binding_of_Isaac_Rebirth_Wiki:Copyrights",
        "intermediate_repository": REPOSITORY,
        "intermediate_commit": COMMIT, "intermediate_data_license_notice": POLICY_URL,
        "retrieved_date": "2026-11-01",
        "selection": "gameId plus first value of qualityRaw from the exact pinned snapshot; no other fields retained",
        "versioned_rows_selected": versioned,
        "inputs": [{"url": URL, "kind": "wiki-derived-export", "sha256": digest,
                    "matched_collectibles": len(qualities)}],
        "missing_ids": [],
        "profile_spot_checks": {
            "706": {"quality": 4, "source": "https://bindingofisaacrebirth.wiki.gg/wiki/Abyss"},
            "562": {"quality": 3, "source": "https://bindingofisaacrebirth.wiki.gg/wiki/Rock_Bottom"},
            "292": {"quality": 4, "source": "https://bindingofisaacrebirth.wiki.gg/wiki/Satanic_Bible"},
            "234": {"quality": 3, "source": "https://bindingofisaacrebirth.wiki.gg/wiki/Infestation_2"},
        },
    }
    for item_id, check in provenance["profile_spot_checks"].items():
        if qualities[int(item_id)] != check["quality"]:
            raise ValueError("Reviewed version spot check does not match")
    return qualities, provenance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path, help="Local copy of the exact pinned JSON (keep it outside the repo)")
    source.add_argument("--download", action="store_true", help="Explicitly download the pinned snapshot, keeping it only in memory")
    args = parser.parse_args()
    names = json.loads((ROOT / "catalog/id_names.json").read_text(encoding="utf-8"))
    expected = {e["id"] for e in names["entries"] if e["variant"] == 100}
    if args.input:
        raw = args.input.read_bytes()
    else:
        with urllib.request.urlopen(URL, timeout=30) as response:
            raw = response.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise SystemExit("Oversized wiki snapshot")
    try:
        qualities, provenance = import_snapshot(raw, expected)
    except (ValueError, KeyError, TypeError) as error:
        raise SystemExit(str(error)) from error
    tsv = "# Collectible ID\tquality. Source and applicable license: ATTRIBUZIONE_TIER.md\n"
    tsv += "".join(f"{item_id}\t{quality}\n" for item_id,quality in sorted(qualities.items()))
    (ROOT / "catalog/collectible_quality.tsv").write_text(tsv, encoding="utf-8")
    (ROOT / "catalog/quality_source.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "runtime").mkdir(exist_ok=True)
    (ROOT / "runtime/collectible_quality.tsv").write_text(render(qualities), encoding="utf-8")
    print(f"Imported {len(qualities)} attributed Repentance qualities; {provenance['versioned_rows_selected']} versioned rows selected")


if __name__ == "__main__":
    main()
