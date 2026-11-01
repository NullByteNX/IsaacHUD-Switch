#!/usr/bin/env python3
"""Import only collectible ID/quality pairs from the user's local game XML.

No downloads. Does not copy game XML, artwork, names, descriptions or tags.
Use metadata files in base-to-override order; explicit items.xml qualities win.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from generate_quality import ROOT, render


def parse_source(path, expected, kind):
    raw = path.read_bytes()
    # Game data does not require entities/DTDs. Reject them before parsing.
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise ValueError(f"DTDs/entities not supported: {path.name}")
    tree = ET.fromstring(raw)
    if tree.tag != "items":
        raise ValueError(f"Expected an <items> root: {path.name}")
    allowed = {"item"} if kind == "metadata" else {"active", "passive", "familiar", "item"}
    values = {}
    for element in tree:
        # In metadata XML, <trinket> shares many numeric IDs with <item>.
        # NEVER merge those namespaces or use craftquality as quality.
        if element.tag not in allowed or "quality" not in element.attrib:
            continue
        item_id = int(element.attrib["id"])
        quality = int(element.attrib["quality"])
        if not 0 <= quality <= 4:
            raise ValueError(f"Quality outside 0-4 in {path.name}, ID {item_id}")
        if item_id not in expected:
            continue
        if item_id in values:
            raise ValueError(f"Duplicate collectible ID {item_id} in {path.name}")
        values[item_id] = quality
    provenance = {
        "file": path.name,
        "kind": kind,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "matched_collectibles": len(values),
    }
    return values, provenance


def prepare_import(sources, expected, game_version, allow_partial=False):
    if not game_version.strip():
        raise ValueError("Declare the source game version/build")
    qualities, inputs = {}, []
    for kind, path in sources:
        values, provenance = parse_source(path, expected, kind)
        qualities.update(values)
        inputs.append(provenance)
    missing = sorted(expected - qualities.keys())
    if not qualities:
        raise ValueError("No explicit collectible qualities found; no files changed")
    if missing and not allow_partial:
        raise ValueError(f"Missing {len(missing)} collectible qualities: {missing}. "
                         "Supply the remaining matching metadata/override XML; no files changed")
    tsv = "# Collectible ID\tquality (0-4). Source: quality_source.json\n"
    tsv += "".join(f"{item_id}\t{quality}\n" for item_id, quality in sorted(qualities.items()))
    provenance = {
        "format": "isaac-hud-quality-source-v1",
        "status": "partial" if missing else "complete",
        "source_kind": "local_game_metadata",
        "collectibles": len(qualities),
        "expected_collectibles": len(expected),
        "game_version": game_version.strip(),
        "game_version_verification": "Version/build supplied with the input; metadata file hashes recorded",
        "inputs": inputs,
        "missing_ids": missing,
    }
    return tsv, provenance, render(qualities)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, action="append", default=[],
                        help="Local items_metadata*.xml, in base-to-override order (repeatable)")
    parser.add_argument("--items", type=Path, action="append", default=[],
                        help="Local items.xml containing explicit quality overrides (repeatable)")
    parser.add_argument("--game-version", required=True, help="Actual source game version/build")
    parser.add_argument("--allow-partial", action="store_true",
                        help="Explicitly permit missing tiers; missing items show no badge")
    args = parser.parse_args()
    if not args.metadata and not args.items:
        parser.error("Supply at least one local --metadata or --items XML")
    index = json.loads((ROOT / "catalog/id_names.json").read_text(encoding="utf-8"))
    expected = {e["id"] for e in index["entries"] if e["variant"] == 100}
    sources = [("metadata", p) for p in args.metadata] + [("items", p) for p in args.items]
    try:
        tsv, provenance, external = prepare_import(sources, expected, args.game_version, args.allow_partial)
    except (OSError, ValueError, ET.ParseError, KeyError) as error:
        raise SystemExit(str(error)) from error
    # Validate ALL inputs/coverage before touching any repository outputs.
    outputs = {
        ROOT / "catalog/collectible_quality.tsv": tsv,
        ROOT / "catalog/quality_source.json": json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
        ROOT / "runtime/collectible_quality.tsv": external,
    }
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    print(f"Imported {provenance['collectibles']}/{len(expected)} collectible qualities. "
          "No source XML copied into the repository.")
    if provenance["missing_ids"]:
        print("Partial import: missing qualities will have NO badge.", file=sys.stderr)


if __name__ == "__main__":
    main()
