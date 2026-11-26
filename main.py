#!/usr/bin/env python3
"""Funniest Sign on a Haunted Server Room Door.

Writes the sign -- one line, at most 120 characters -- to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The sign itself is a plain constant: a warning taped to the door of a
server room whose ghost has root access and has never once filed a
ticket. Pure standard library, deterministic, no network, no input
read from anywhere outside this file.
"""

import os
import sys

SIGN = "WARNING: This server room is haunted. The ghost has root access and has never filed a single ticket."

MAX_CHARS = 120


def valid_sign(text):
    """A sign is valid when it is 1-120 characters of real text."""
    return isinstance(text, str) and 1 <= len(text) <= MAX_CHARS and text.strip() != ""


def main():
    if not valid_sign(SIGN):
        print("sign fails the gate: %r (%d chars)" % (SIGN, len(SIGN)), file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    staging = target + ".staging"
    with open(staging, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(SIGN)
    os.replace(staging, target)

    with open(target, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != SIGN or not valid_sign(written):
        print("written entry does not match the sign", file=sys.stderr)
        return 1

    print("wrote %d chars to %s" % (len(written), target))
    print(written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
