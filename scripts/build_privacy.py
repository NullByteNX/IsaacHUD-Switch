#!/usr/bin/env python3
"""Map local compiler paths and check binaries without modifying their bytes."""
import argparse
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

# Source paths observed in the prebuilt devkitA64/newlib, libnx and libgcc
# packages. These belong to the SDK builder, not to the overlay's build host.
# Keep the exceptions narrow; current-machine prefixes below ALWAYS take
# precedence, even when they overlap one of these external SDK paths.
PREBUILT_SDK_PATHS = (
    "/home/davem/projects/devkitpro/pacman-packages/devkita64/",
    "/home/davem/projects/devkitpro/pacman-packages/libnx/",
    "/home/davem/projects/devkitpro/tool-packages/devkita64/",
)

# Runtime SD paths and neutral SDK paths are intentionally outside this pattern.
LOCAL_PATH = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    r"[A-Za-z]:[/\\][A-Za-z0-9_ .~()@%+\-]+[/\\]|"
    r"/(?:mnt/[A-Za-z]/|cygdrive/[A-Za-z]/|[A-Za-z]/)?(?:Users|home)/|"
    r"/(?:workspace|tmp)/|/private/(?:var|tmp)/|/var/(?:tmp|folders)/|"
    r"\\\\[A-Za-z0-9_.\-]+\\)", re.IGNORECASE
)


def path_spellings(path):
    """Include both MSYS and Windows spellings when cygpath is available."""
    value = str(path).replace("\\", "/").rstrip("/")
    values = {value}
    cygpath = shutil.which("cygpath")
    if cygpath:
        for mode in ("-m", "-u"):
            result = subprocess.run([cygpath, mode, value], capture_output=True,
                                    text=True, check=True)
            values.add(result.stdout.strip().replace("\\", "/").rstrip("/"))
    return {value for value in values if len(value) > 2}


def compiler_flags(project=ROOT, home=None, devkit=None):
    """Use neutral names in __FILE__, __BASE_FILE__ and debug information."""
    home = Path.home() if home is None else home
    devkit = os.environ.get("DEVKITPRO") if devkit is None else devkit
    mappings = {}
    for path, replacement in ((home, "/build-home"), (devkit, "/opt/devkitpro"),
                              (project, ".")):
        if path:
            for spelling in path_spellings(path):
                mappings[spelling] = replacement
    # GCC applies the last matching mapping: specific paths follow parent paths.
    flags = ["-gno-record-gcc-switches", "-fno-record-gcc-switches"]
    flags += [f"-ffile-prefix-map={old}={mappings[old]}"
              for old in sorted(mappings, key=lambda value: (len(value), value))]
    return flags


def private_prefixes():
    prefixes = set()
    for path in (ROOT, Path.home(), os.environ.get("DEVKITPRO")):
        if path:
            for value in path_spellings(path):
                # The conventional SDK root is a neutral path, not a user path.
                if value != "/opt/devkitpro":
                    prefixes.update((value, value.replace("/", "\\")))
    return prefixes


def find_local_paths(data, prefixes=None):
    """Find known local prefixes and common absolute paths in UTF-8/UTF-16."""
    prefixes = private_prefixes() if prefixes is None else prefixes
    reasons = set()
    streams = [data.decode("utf-8", errors="replace")]
    # Both byte alignments matter when a UTF-16 string is embedded in a binary.
    for encoding in ("utf-16-le", "utf-16-be"):
        streams += [data[offset:].decode(encoding, errors="replace")
                    for offset in (0, 1)]
    for text in streams:
        if any(not text.startswith(PREBUILT_SDK_PATHS, match.start())
               for match in LOCAL_PATH.finditer(text)):
            reasons.add("absolute local path")
        folded = text.casefold()
        if any(str(prefix).casefold() in folded for prefix in prefixes):
            reasons.add("current build/home/SDK directory")
    return sorted(reasons)


def check_binary(path):
    data = Path(path).read_bytes()
    if not data:
        raise ValueError("Empty binary")
    reasons = find_local_paths(data)
    if reasons:
        # Do not echo personal strings into logs or generated release files.
        raise ValueError("Build privacy check FAILED (" + Path(path).name + "): "
                         + ", ".join(reasons)
                         + ". Inspect the detected paths before rebuilding; "
                         "the file has not been changed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("flags")
    check = commands.add_parser("check")
    check.add_argument("binaries", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "flags":
            print(shlex.join(compiler_flags()))
        else:
            for binary in args.binaries:
                check_binary(binary)
            print("Build privacy check PASS: no current-machine or unrecognized "
                  "local paths detected (known prebuilt SDK paths allowed)")
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
