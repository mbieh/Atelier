#!/usr/bin/env python3
"""Generate atelier-ui.rtl.css from atelier-ui.css deterministically."""

from __future__ import annotations

import argparse
import difflib
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "atelier-ui.css"
TARGET = ROOT / "atelier-ui.rtl.css"

# The source contains only a small number of physical direction declarations.
# Exact block replacements make every intentional RTL difference reviewable and
# fail loudly when the LTR source changes instead of silently guessing.
TRANSFORMS = (
    ("\tpadding-right: 2.75rem;", "\tpadding-left: 2.75rem;"),
    ("\tmargin: 4px 0 0 -2.5rem;", "\tmargin: 4px -2.5rem 0 0;"),
    (
        "\tborder-right: 1px solid var(--grey-medium-light);",
        "\tborder-left: 1px solid var(--grey-medium-light);",
    ),
    ("\ttransform: translateX(2px);", "\ttransform: translateX(-2px);"),
    (
        ".aside .stick .btn:first-child {\n"
        "\tborder-radius: var(--at-radius-m) 0 0 var(--at-radius-m);\n"
        "}\n\n"
        ".aside .stick .btn:last-child {\n"
        "\tborder-radius: 0 var(--at-radius-m) var(--at-radius-m) 0;\n"
        "}",
        ".aside .stick .btn:first-child {\n"
        "\tborder-radius: 0 var(--at-radius-m) var(--at-radius-m) 0;\n"
        "}\n\n"
        ".aside .stick .btn:last-child {\n"
        "\tborder-radius: var(--at-radius-m) 0 0 var(--at-radius-m);\n"
        "}",
    ),
    ("\tborder-right-width: 0;", "\tborder-left-width: 0;"),
    (
        "\tmargin: 0.75rem 1rem 1rem 0.5rem;",
        "\tmargin: 0.75rem 0.5rem 1rem 1rem;",
    ),
    (
        ".flux:not(.current) .flux_header:hover {\n"
        "\tbox-shadow: inset 2px 0 0 var(--grey-medium);\n"
        "}\n\n"
        ".flux.not_read:not(.current) .flux_header:hover {\n"
        "\tbox-shadow: inset 2px 0 0 var(--main-first);\n"
        "}",
        ".flux:not(.current) .flux_header:hover {\n"
        "\tbox-shadow: inset -2px 0 0 var(--grey-medium);\n"
        "}\n\n"
        ".flux.not_read:not(.current) .flux_header:hover {\n"
        "\tbox-shadow: inset -2px 0 0 var(--main-first);\n"
        "}",
    ),
    ("\tpadding-right: 14px;", "\tpadding-left: 14px;"),
    ("\tbox-shadow: -12px 0 32px", "\tbox-shadow: 12px 0 32px"),
    (
        "\tborder-radius: var(--at-radius-l) 0 0 var(--at-radius-l);",
        "\tborder-radius: 0 var(--at-radius-l) var(--at-radius-l) 0;",
    ),
    (
        "\tpadding: 0.75rem 3rem 0.75rem 1.25rem;",
        "\tpadding: 0.75rem 1.25rem 0.75rem 3rem;",
    ),
    (
        "\ttext-align: left;\n\tanimation: at-toast",
        "\ttext-align: right;\n\tanimation: at-toast",
    ),
    ("\tmargin-right: 0.6rem;", "\tmargin-left: 0.6rem;"),
    (
        ".notification .close {\n\tright: 6px;",
        ".notification .close {\n\tleft: 6px;\n\tright: auto;",
    ),
)


def generate(source: str) -> str:
    result = source
    for before, after in TRANSFORMS:
        count = result.count(before)
        if count != 1:
            raise ValueError(
                f"expected exactly one RTL transform match, found {count}: {before!r}"
            )
        result = result.replace(before, after, 1)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if atelier-ui.rtl.css differs instead of updating it",
    )
    args = parser.parse_args()

    expected = generate(SOURCE.read_text(encoding="utf-8"))
    current = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""

    if args.check:
        if current == expected:
            print("atelier-ui.rtl.css is up to date")
            return 0
        diff = difflib.unified_diff(
            current.splitlines(keepends=True),
            expected.splitlines(keepends=True),
            fromfile=str(TARGET.relative_to(ROOT)),
            tofile="generated",
        )
        sys.stderr.writelines(diff)
        return 1

    TARGET.write_text(expected, encoding="utf-8")
    print(f"generated {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
