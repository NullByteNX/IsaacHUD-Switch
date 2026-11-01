#!/usr/bin/env python3
"""Generate the external collectible-only table from the attributed local TSV.

No network, descriptions, sprites, or crafting-quality overrides.
"""
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]


def load_qualities(path, expected):
    result = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            raise ValueError(f"Malformed quality row {number}")
        item_id, quality = map(int, parts)
        if item_id in result or item_id not in expected or not 0 <= quality <= 4:
            raise ValueError(f"Invalid/duplicate collectible quality on row {number}")
        result[item_id] = quality
    return result


def render(qualities):
    rows = [
        "# isaac-hud-quality-v1",
        "# Collectibles only: ID<TAB>quality (0-4). Missing is not zero.",
        "# Source/attribution: catalog/ATTRIBUZIONE_TIER.md and catalog/quality_source.json.",
        "# Dataset rights where applicable: CC-BY-SA-4.0; LICENSES/CC-BY-SA-4.0.txt.",
    ]
    rows.extend(f"{item_id}\t{quality}" for item_id,quality in sorted(qualities.items()))
    return "\n".join(rows) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the generated external table is stale")
    args = parser.parse_args()
    names = json.loads((ROOT / "catalog/id_names.json").read_text(encoding="utf-8"))
    expected = {e["id"] for e in names["entries"] if e["variant"] == 100}
    qualities = load_qualities(ROOT / "catalog/collectible_quality.tsv", expected)
    provenance = json.loads((ROOT / "catalog/quality_source.json").read_text(encoding="utf-8"))
    if provenance.get("format") != "isaac-hud-quality-source-v1":
        raise ValueError("Unsupported quality provenance format")
    if provenance.get("collectibles") != len(qualities) or provenance.get("expected_collectibles") != len(expected):
        raise ValueError("Quality provenance/coverage mismatch")
    if provenance.get("status") == "complete" and set(qualities) != expected:
        raise ValueError("A complete quality catalog must cover every collectible")
    if qualities and (provenance.get("source_kind") not in ("local_game_metadata", "wiki_export")
                      or not provenance.get("inputs") or not provenance.get("game_version")):
        raise ValueError("Missing quality-data provenance")
    if not qualities and provenance.get("status") not in ("awaiting-local-game-metadata", "awaiting-verified-wiki-data"):
        raise ValueError("Empty quality catalog must be explicitly marked as pending")
    generated = render(qualities)
    target = ROOT / "runtime/collectible_quality.tsv"
    if args.check:
        if target.read_text(encoding="utf-8") != generated:
            raise SystemExit("Stale external quality table: run python3 scripts/generate_quality.py")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(generated, encoding="utf-8")
    print(f"{len(qualities)} collectible qualities: {'verified' if args.check else 'generated'}")


if __name__ == "__main__":
    main()
