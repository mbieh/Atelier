#!/usr/bin/env python3
"""Generate direction-neutral RTL counterparts from their canonical sources."""

from __future__ import annotations

import argparse
import difflib
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    ROOT / "_fonts.css",
    ROOT / "_variables.css",
    ROOT / "atelier-ui.css",
)


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
    # load byte-identical counterparts for these project-owned stylesheets.
    for source in SOURCES:
        target = rtl_target(source)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"generated {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
