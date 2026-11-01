"""SYNTHETIC tiers for host tests ONLY. These are NOT game item qualities."""
import json


def synthetic_qualities(root):
    names = json.loads((root / "catalog/id_names.json").read_text(encoding="utf-8"))
    return {e["id"]: e["id"] % 5 for e in names["entries"] if e["variant"] == 100}
