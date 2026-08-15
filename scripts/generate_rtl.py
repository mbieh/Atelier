#!/usr/bin/env python3
"""Generate direction-neutral RTL counterparts from their canonical sources."""

from __future__ import annotations

import argparse
import difflib
from pathlib import Path
import sys


from check_theme import (
    DIRECTION_NEUTRAL_FILES,
    RTL_MIRRORED_FILES,
    check_direction_neutral,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCES = tuple(ROOT / name for name in RTL_MIRRORED_FILES)
GUARDED = tuple(ROOT / name for name in DIRECTION_NEUTRAL_FILES)


def rtl_target(source: Path) -> Path:
    return source.with_name(f"{source.stem}.rtl{source.suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if a generated RTL counterpart differs instead of updating it",
    )
    args = parser.parse_args()

    # A verbatim copy is only a valid RTL sheet while the source is
    # direction-neutral, and unlike the old transform table this copy cannot
    # fail on its own when the source changes. Guard it explicitly instead --
    # across every stylesheet, because the mirrored sheets pull the partials in
    # by @import and inherit whatever direction bugs those carry.
    direction_errors: list[str] = []
    for source in GUARDED:
        direction_errors.extend(
            check_direction_neutral(
                source.relative_to(ROOT), source.read_text(encoding="utf-8")
            )
        )
    if direction_errors:
        for error in direction_errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    if args.check:
        stale = False
        for source in SOURCES:
            target = rtl_target(source)
            expected = source.read_text(encoding="utf-8")
            current = target.read_text(encoding="utf-8") if target.exists() else ""
            if current == expected:
                continue
            stale = True
            diff = difflib.unified_diff(
                current.splitlines(keepends=True),
                expected.splitlines(keepends=True),
                fromfile=str(target.relative_to(ROOT)),
                tofile=f"generated/{target.name}",
            )
            sys.stderr.writelines(diff)
        if stale:
            return 1
        print("generated RTL files are up to date")
        return 0

    # Logical properties handle spacing, borders, and radii. The few
    # direction-sensitive transforms and shadows use :dir(rtl), so FreshRSS can
    # load byte-identical counterparts for the two sheets it requests by name.
    for source in SOURCES:
        target = rtl_target(source)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"generated {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
