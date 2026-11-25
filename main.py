#!/usr/bin/env python3
"""The Meeting That Should Have Been One Line.

Writes a single one-line sentence that could have replaced an entire
pointless meeting to /output/entry.txt (the make.fun program/v1 harness
output path), falling back to a local ./output/entry.txt when /output is
not writable (local testing).

Pure standard library only.
"""

import os

# v2 (revised): "I'll read it out loud" makes the speaker perform the
# meeting's job on the spot -- the line doesn't describe killing the
# meeting, it kills it. Tighter verb, 78 characters total.
LINE = (
    "Nobody read the email, so I'll read it out loud: "
    "approved, done, meeting over."
)

MAX_CHARS = 200


def main() -> None:
    line = LINE.strip()
    if not (1 <= len(line) <= MAX_CHARS):
        raise ValueError(
            f"line must be 1-{MAX_CHARS} characters, got {len(line)}"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")

    try:
        os.makedirs("/output", exist_ok=True)
        out_path = "/output/entry.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(line)
    except OSError:
        os.makedirs("output", exist_ok=True)
        out_path = os.path.join("output", "entry.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(line)

    print(f"Wrote {len(line)} characters to {out_path}")

    # Self-check: read the file back and confirm it round-trips exactly,
    # is valid UTF-8, a single line, and within the 200-character gate.
    with open(out_path, encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt does not match the line"
    assert written.strip() and len(written) <= MAX_CHARS
    assert "\n" not in written and "\r" not in written
    print(f"Verified: {len(written)} chars, single line, valid UTF-8")


if __name__ == "__main__":
    main()
