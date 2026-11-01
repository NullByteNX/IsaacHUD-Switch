#!/usr/bin/env python3
"""Prepare the SD layout, credits and file hashes offline."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from build_privacy import check_binary

ROOT = Path(__file__).resolve().parents[1]
SOFTWARE_LICENSES = {
    "LICENSE": "GPL-2.0.txt",
    "LICENSES/MIT-original.txt": "MIT-original.txt",
    "LICENSES/ISC-libnx.txt": "ISC-libnx.txt",
    "LICENSES/MIT-stb_truetype.txt": "MIT-stb_truetype.txt",
    "LICENSES/NEWLIB.txt": "NEWLIB.txt",
    "LICENSES/GPL-3.0-GCC-RUNTIME.txt": "GPL-3.0-GCC-RUNTIME.txt",
    "LICENSES/GCC-RUNTIME-EXCEPTION-3.1.txt": "GCC-RUNTIME-EXCEPTION-3.1.txt",
}


def package(output, ovl=None, require_quality=False):
    # Refuse invalid inputs before writing a partially prepared package.
    for script in ("generate_catalog.py", "generate_quality.py"):
        subprocess.run([sys.executable, str(ROOT / "scripts" / script), "--check"], check=True)
    provenance = json.loads((ROOT / "catalog/quality_source.json").read_text(encoding="utf-8"))
    complete = provenance["status"] == "complete" and provenance["collectibles"] == 719
    if require_quality and not complete:
        raise ValueError("Release blocked: a complete, attributed 719-item quality table is required")
    if ovl is not None and (not ovl.is_file() or ovl.suffix.lower() != ".ovl" or ovl.stat().st_size == 0):
        raise ValueError("Supply an existing nonempty compiled .ovl; this script does not compile one")
    if ovl is not None:
        check_binary(ovl) # Reject personal paths before changing the SD package.
    for name in [*SOFTWARE_LICENSES, "docs/SOFTWARE_NOTICES.txt", "NOTICE.md"]:
        if not (ROOT / name).is_file():
            raise ValueError("Missing release notice: " + name)
    marker = output / ".isaac_hud_generated"
    if output.exists() and any(output.iterdir()) and not marker.is_file():
        raise ValueError("Refusing to overwrite a non-generated output directory")
    output.mkdir(parents=True, exist_ok=True)
    marker.write_text("Isaac HUD generated SD package\n", encoding="utf-8")
    data = output / "switch/IsaacHUD"
    data.mkdir(parents=True, exist_ok=True)
    for name in ("catalog_it.tsv", "collectible_quality.tsv"):
        shutil.copyfile(ROOT / "runtime" / name, data / name)
    licenses = data / "licenses"
    licenses.mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "LICENSES/CC-BY-SA-4.0.txt", licenses / "CC-BY-SA-4.0.txt")
    for source, name in SOFTWARE_LICENSES.items():
        shutil.copyfile(ROOT / source, licenses / name)
    shutil.copyfile(ROOT / "docs/SOFTWARE_NOTICES.txt", data / "SOFTWARE_NOTICES.txt")
    shutil.copyfile(ROOT / "NOTICE.md", data / "NOTICE.md")
    credits = [
        "Isaac HUD 0.6.0 - attribuzioni dei dati\n",
        "Licenza completa: licenses/CC-BY-SA-4.0.txt\n",
        "I collegamenti relativi nei documenti riportati sotto si riferiscono al repository:\n",
        "https://github.com/NullByteNX/IsaacHUD-Switch\n\n",
    ]
    for name in ("ATTRIBUZIONE.md", "ATTRIBUZIONE_TIER.md"):
        credits.append((ROOT / "catalog" / name).read_text(encoding="utf-8") + "\n\n")
    (data / "CREDITI.txt").write_text("".join(credits), encoding="utf-8")
    binary = output / "switch/.overlays/IsaacHUD.ovl"
    if ovl is not None:
        binary.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ovl, binary)
    elif binary.exists():
        binary.unlink() # Do not leave an older OVL in a newly staged data-only package.
    status = "Contenuto: programma IsaacHUD.ovl, cataloghi e crediti." if ovl else "Contenuto: cataloghi e crediti. Per il programma usare l’OVL compilato dai sorgenti della release."
    instructions = (
        "Isaac HUD 0.6.0 - pacchetto SD\n\n" + status + "\n\n"
        "Copiare la cartella switch nella radice della SD.\n"
        "File operativi: switch/.overlays/IsaacHUD.ovl, switch/IsaacHUD/catalog_it.tsv, "
        "switch/IsaacHUD/collectible_quality.tsv.\n"
        "Conservare CREDITI.txt, SOFTWARE_NOTICES.txt, NOTICE.md e licenses/ nel pacchetto.\n"
        "Il formato dei cataloghi esterni è supportato dalla versione 0.6.0.\n"
        f"Qualita' incluse: {provenance['collectibles']}/719.\n"
        "Nessuna connessione Internet richiesta sulla console.\n"
    )
    (output / "LEGGIMI.txt").write_text(instructions, encoding="utf-8")
    hashes = {str(p.relative_to(output)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(output.rglob("*")) if p.is_file() and p.name not in ("SHA256SUMS.json", ".isaac_hud_generated")}
    (output / "SHA256SUMS.json").write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
    return {"output": str(output.resolve()), "binary_included": ovl is not None,
            "collectible_qualities": provenance["collectibles"], "complete_qualities": complete}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/sdcard")
    parser.add_argument("--ovl", type=Path)
    parser.add_argument("--require-quality", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(package(args.output, args.ovl, args.require_quality), ensure_ascii=False))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
