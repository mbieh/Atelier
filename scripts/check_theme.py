#!/usr/bin/env python3
"""Run dependency-free release checks for the Atelier theme."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
LUCIDE_HEADER = "<!-- @license lucide-static v1.31.0 - ISC -->"
NON_LUCIDE_SVGS = {"FreshRSS-logo.svg", "icon.svg"}
EXTERNAL_OR_COMPAT_PROPERTIES = {
    # Retained from Mapco's palette contract even though Atelier does not
    # currently consume them directly.
    "--unread-bg-light",
    "--warning-bg",
}
PROTECTED_NOTES = (
    "Kein backdrop-filter",
    "Desktop-Layout als CSS-Grid",
    "Basis hängt 100vh Leerraum an",
    "width: auto !important",
    "195px",
)


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)


def strip_css_comments_and_strings(css: str) -> str:
    output: list[str] = []
    index = 0
    state = "code"
    quote = ""
    while index < len(css):
        char = css[index]
        following = css[index + 1] if index + 1 < len(css) else ""
        if state == "code" and char == "/" and following == "*":
            output.extend("  ")
            index += 2
            state = "comment"
            continue
        if state == "comment":
            if char == "*" and following == "/":
                output.extend("  ")
                index += 2
                state = "code"
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
            continue
        if state == "code" and char in {'"', "'"}:
            quote = char
            output.append(" ")
            index += 1
            state = "string"
            continue
        if state == "string":
            if char == "\\" and following:
                output.extend("  ")
                index += 2
            elif char == quote:
                output.append(" ")
                index += 1
                state = "code"
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
            continue
        output.append(char)
        index += 1
    if state != "code":
        raise ValueError(f"unterminated CSS {state}")
    return "".join(output)


def check_balanced_braces(path: Path, css: str) -> list[str]:
    errors: list[str] = []
    try:
        stripped = strip_css_comments_and_strings(css)
    except ValueError as error:
        return [f"{path}: {error}"]
    stack: list[int] = []
    for line_number, line in enumerate(stripped.splitlines(), start=1):
        for character in line:
            if character == "{":
                stack.append(line_number)
            elif character == "}":
                if not stack:
                    errors.append(f"{path}:{line_number}: unmatched closing brace")
                else:
                    stack.pop()
    for line_number in stack:
        errors.append(f"{path}:{line_number}: unmatched opening brace")
    return errors


def main() -> int:
    errors: list[str] = []
    text_files = sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix in {".css", ".json", ".md", ".py", ".yml", ".yaml"}
    )

    for path in text_files:
        content = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if "\r" in content:
            errors.append(f"{relative}: CRLF line endings")
        if content and not content.endswith("\n"):
            errors.append(f"{relative}: missing final newline")
        if content.endswith("\n\n"):
            errors.append(f"{relative}: extra blank line at end of file")
        for line_number, line in enumerate(content.splitlines(), start=1):
            if line.rstrip() != line:
                errors.append(f"{relative}:{line_number}: trailing whitespace")
        if path.suffix == ".css":
            errors.extend(check_balanced_braces(relative, content))

    try:
        metadata = json.loads((ROOT / "metadata.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"metadata.json: {error}")
        metadata = {}

    if metadata.get("name") != "Atelier":
        errors.append("metadata.json: name must be Atelier")
    if metadata.get("version") != 1.0:
        errors.append("metadata.json: version must match release 1.0")
    for filename in metadata.get("files", []):
        if filename == "_frss.css":
            continue
        path = ROOT / filename
        if not path.is_file():
            errors.append(f"metadata.json: missing CSS file {filename}")
        rtl_path = path.with_name(f"{path.stem}.rtl{path.suffix}")
        if not rtl_path.is_file():
            errors.append(f"metadata.json: missing RTL counterpart {rtl_path.name}")

    css = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.glob("*.css"))
    definitions = set(re.findall(r"(?m)^\s*(--[\w-]+)\s*:", css))
    uses = set(re.findall(r"var\(\s*(--[\w-]+)", css))
    unused = definitions - uses - EXTERNAL_OR_COMPAT_PROPERTIES
    if unused:
        errors.append("unused custom properties: " + ", ".join(sorted(unused)))

    svg_files = sorted((ROOT / "icons").glob("*.svg"))
    lucide_files = [path for path in svg_files if path.name not in NON_LUCIDE_SVGS]
    if len(lucide_files) != 44:
        errors.append(f"expected 44 Lucide SVGs, found {len(lucide_files)}")
    for path in lucide_files:
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        if first_line != LUCIDE_HEADER:
            errors.append(f"{path.relative_to(ROOT)}: missing exact Lucide license header")

    ui_css = (ROOT / "atelier-ui.css").read_text(encoding="utf-8")
    for note in PROTECTED_NOTES:
        if note not in ui_css:
            errors.append(f"atelier-ui.css: protected design note missing: {note}")

    if errors:
        for error in errors:
            fail(error)
        return 1

    print(f"checked {len(text_files)} text files and {len(svg_files)} SVG files")
    print("CSS braces, formatting, metadata, custom properties, and licenses are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
