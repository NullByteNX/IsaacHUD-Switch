#!/usr/bin/env python3
"""Neutralize the local build pathname stored beside stb_truetype.h.

This changes a single NUL-terminated *data string*, never instruction bytes.
Preserves file length and does not contain the original author's PC pathname.
Use on your own newly compiled OVL; inspect and test the output on console.
"""
import argparse
import hashlib
from pathlib import Path

MARKER = b"libs/libtesla/include/stb_truetype.h"


def sanitize(raw: bytes) -> bytes:
    if raw.count(MARKER) != 1:
        raise ValueError("Expected precisely one stb_truetype.h build-path marker")
    pos = raw.index(MARKER)
    preceding_nul = raw.rfind(b"\0", 0, pos)
    terminating_nul = raw.find(b"\0", pos + len(MARKER))
    if preceding_nul < 0 or terminating_nul < 0:
        raise ValueError("Build-path string boundaries not found")
    start = preceding_nul + 1
    previous = raw[start:terminating_nul]
    if not previous.endswith(MARKER) or not all(32 <= b < 127 for b in previous):
        raise ValueError("Unexpected build-path encoding")
    replacement = MARKER + b"\0" * (len(previous) - len(MARKER))
    updated = raw[:start] + replacement + raw[terminating_nul:]
    if len(updated) != len(raw):
        raise AssertionError("OVL size changed unexpectedly")
    return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Original devkitPro OVL")
    parser.add_argument("output", type=Path, help="Separate path-neutral OVL")
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Input and output must be different; do not overwrite your tested build")
    data = sanitize(args.input.read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print("Written:", args.output)
    print("SHA-256:", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
