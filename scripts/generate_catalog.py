#!/usr/bin/env python3
"""Build the Italian HUD catalog from minimal item names and Italian summaries.

This script does not download or contain wiki articles, translated article text,
HTML captures or English descriptions of gameplay effects.
The required attribution is maintained in catalog/ATTRIBUZIONE.md.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "catalog"


def translations(filename, fields):
    result = {}
    for number, line in enumerate((CAT / filename).read_text(encoding="utf-8").splitlines(), 1):
        parts = line.split("\t")
        if len(parts) != fields or not all(parts):
            raise ValueError(f"Malformed Italian entry in {filename}:{number}")
        key = int(parts[0])
        if key in result:
            raise ValueError(f"Duplicate ID {key} in {filename}")
        result[key] = parts[1:]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    index = json.loads((CAT / "id_names.json").read_text(encoding="utf-8"))
    if index.get("format") != "isaac-hud-names-v1":
        raise ValueError("Unsupported names format")
    entries = index["entries"]
    pills = index["pills"]
    if len(entries) != 1004 or len(pills) != 50:
        raise ValueError("Unexpected item or pill coverage")
    translations_by_variant = {
        100: translations("it_collectibles.tsv", 2),
        350: translations("it_trinkets.tsv", 2),
        300: translations("it_cards.tsv", 2),
    }
    if len({(e["variant"], e["id"]) for e in entries}) != len(entries):
        raise ValueError("Duplicate variant/item ID")
    if [(e["variant"], e["id"]) for e in entries] != sorted((e["variant"],e["id"]) for e in entries):
        raise ValueError("Item entries not ordered")
    for variant, descriptions in translations_by_variant.items():
        expected = {e["id"] for e in entries if e["variant"] == variant}
        if set(descriptions) != expected:
            raise ValueError(f"Incorrect Italian translation coverage for variant {variant}")
    effects = translations("it_pills.tsv", 3)
    if set(effects) != {e["id"] for e in pills}:
        raise ValueError("Incorrect Italian pill-effect coverage")
    if [e["id"] for e in pills] != sorted(e["id"] for e in pills):
        raise ValueError("Pill IDs not sorted")
    rows = [
        "# isaac-hud-catalog-v1",
        "# Data/Italian summaries: CC-BY-SA-4.0; see catalog/ATTRIBUZIONE.md.",
        "# D: variant, ID, name, description. P: 70, effect ID, name, normal, horse.",
        r"# Escapes: backslash, tab, LF, CR use \\, \t, \n, \r.",
    ]
    def escape(value):
        if not isinstance(value, str) or not value:
            raise ValueError("Missing name or description")
        return value.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")
    for e in entries:
        value = translations_by_variant[e["variant"]][e["id"]][0]
        rows.append("\t".join(["D",str(e["variant"]),str(e["id"]),escape(e["name"]),escape(value)]))
    for e in pills:
        normal, horse = effects[e["id"]]
        if horse == "=":
            horse = normal
        rows.append("\t".join(["P","70",str(e["id"]),escape(e["name"]),escape(normal),escape(horse)]))
    generated = "\n".join(rows) + "\n"
    output = ROOT / "runtime/catalog_it.tsv"
    if args.check:
        if output.read_text(encoding="utf-8") != generated:
            raise SystemExit("Stale runtime catalog: run python3 scripts/generate_catalog.py")
    else:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(generated,encoding="utf-8")
    print(f"External catalog: {len(entries)} items and {len(pills)} pill effects {'verified' if args.check else 'generated'}")

if __name__ == "__main__":
    main()
