#!/usr/bin/env python3
"""Run dependency-free release checks for the Atelier theme."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote
import xml.etree.ElementTree as ElementTree


ROOT = Path(__file__).resolve().parents[1]
LUCIDE_HEADER = "<!-- @license lucide-static v1.31.0 - ISC -->"
NON_LUCIDE_SVGS = {"FreshRSS-logo.svg", "icon.svg"}
EXPECTED_THEME_FILES = ["_frss.css", "atelier.css", "atelier-ui.css"]
REQUIRED_SEMANTIC_PROPERTIES = {
    "--accent",
    "--accent-foreground",
    "--background",
    "--border",
    "--card",
    "--card-foreground",
    "--destructive",
    "--destructive-foreground",
    "--foreground",
    "--input",
    "--muted",
    "--muted-foreground",
    "--popover",
    "--popover-foreground",
    "--primary",
    "--primary-foreground",
    "--ring",
    "--secondary",
    "--secondary-foreground",
    "--sidebar",
    "--sidebar-accent",
    "--sidebar-accent-foreground",
    "--sidebar-border",
    "--sidebar-foreground",
    "--sidebar-primary",
    "--sidebar-primary-foreground",
    "--sidebar-ring",
}
EXTERNAL_OR_COMPAT_PROPERTIES = {
    # FreshRSS base-theme tokens consumed by the shared _frss.css stylesheet.
    "--frss-background-color",
    "--frss-background-color-dark",
    "--frss-background-color-error-transparent",
    "--frss-background-color-middle",
    "--frss-background-color-transparent",
    "--frss-border-color",
    "--frss-border-color-error",
    "--frss-darken-background-hover-transparent",
    "--frss-font-color-dark",
    "--frss-font-color-disabled",
    "--frss-font-color-error",
    "--frss-font-color-grey-dark",
    "--frss-font-color-grey-light",
    "--frss-noThumbnailImage-background-color",
    "--frss-scrollbar-handle",
    "--frss-scrollbar-handle-hover",
    "--frss-scrollbar-track",
    "--frss-scrollbar-track-hover",
    "--frss-switch-accent-color",
    # Retained from Mapco's palette contract even though Atelier does not
    # currently consume them directly.
    "--unread-bg-light",
    "--warning-bg",
}
PROTECTED_NOTES = (
    "Do not add backdrop-filter",
    "desktop CSS Grid",
    "base theme adds 100vh of whitespace",
    "width: auto !important",
    "195px",
)
FORBIDDEN_PHYSICAL_DECLARATIONS = (
    "padding-left:",
    "padding-right:",
    "margin-left:",
    "margin-right:",
    "border-left:",
    "border-right:",
    "text-align: left",
    "text-align: right",
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


def check_local_markdown_links(path: Path, content: str) -> list[str]:
    errors: list[str] = []
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
        target = target.split(maxsplit=1)[0]
        if target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        file_target = unquote(target.split("#", 1)[0])
        if file_target and not (path.parent / file_target).exists():
            errors.append(f"{path.relative_to(ROOT)}: broken local link: {target}")
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
        if path.suffix == ".md":
            errors.extend(check_local_markdown_links(path, content))

    try:
        metadata = json.loads((ROOT / "metadata.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"metadata.json: {error}")
        metadata = {}

    if metadata.get("name") != "Atelier":
        errors.append("metadata.json: name must be Atelier")
    if metadata.get("version") != 1.0:
        errors.append("metadata.json: version must match release 1.0")
    if metadata.get("files") != EXPECTED_THEME_FILES:
        errors.append(
            "metadata.json: files must preserve the verified FreshRSS load order"
        )
    for filename in metadata.get("files", []):
        if filename == "_frss.css":
            continue
        path = ROOT / filename
        if not path.is_file():
            errors.append(f"metadata.json: missing CSS file {filename}")
        rtl_path = path.with_name(f"{path.stem}.rtl{path.suffix}")
        if not rtl_path.is_file():
            errors.append(f"metadata.json: missing RTL counterpart {rtl_path.name}")

    css_paths = sorted(ROOT.glob("*.css"))
    css = "\n".join(path.read_text(encoding="utf-8") for path in css_paths)
    definitions = set(re.findall(r"(?m)^\s*(--[\w-]+)\s*:", css))
    uses = set(re.findall(r"var\(\s*(--[\w-]+)", css))
    missing_semantic_properties = REQUIRED_SEMANTIC_PROPERTIES - definitions
    if missing_semantic_properties:
        errors.append(
            "missing shadcn semantic properties: "
            + ", ".join(sorted(missing_semantic_properties))
        )
    unused = definitions - uses - EXTERNAL_OR_COMPAT_PROPERTIES
    if unused:
        errors.append("unused custom properties: " + ", ".join(sorted(unused)))

    if (ROOT / "_variables.css").read_bytes() != (
        ROOT / "_variables.rtl.css"
    ).read_bytes():
        errors.append("_variables.rtl.css must be identical to _variables.css")

    for path in css_paths:
        content = path.read_text(encoding="utf-8")
        for imported in re.findall(r'@import\s+["\']([^"\']+)["\']', content):
            if not (path.parent / imported).is_file():
                errors.append(f"{path.name}: missing imported stylesheet: {imported}")
        if re.search(r"url\(\s*[\"']?https?://", content, flags=re.IGNORECASE):
            errors.append(f"{path.name}: external runtime asset URL is not allowed")
        if re.search(r"rgba?\(\s*var\(", content, flags=re.IGNORECASE):
            errors.append(
                f"{path.name}: pass colors through color-mix(), not rgba(var(...))"
            )

    ui_css = (ROOT / "atelier-ui.css").read_text(encoding="utf-8")
    for declaration in FORBIDDEN_PHYSICAL_DECLARATIONS:
        if declaration in ui_css:
            errors.append(
                f"atelier-ui.css: use a logical property instead of {declaration}"
            )

    svg_files = sorted((ROOT / "icons").glob("*.svg"))
    lucide_files = [path for path in svg_files if path.name not in NON_LUCIDE_SVGS]
    if len(lucide_files) != 46:
        errors.append(f"expected 46 Lucide SVGs, found {len(lucide_files)}")
    for path in lucide_files:
        content = path.read_text(encoding="utf-8")
        first_line = content.splitlines()[0]
        if first_line != LUCIDE_HEADER:
            errors.append(
                f"{path.relative_to(ROOT)}: missing exact Lucide license header"
            )
    for path in svg_files:
        try:
            ElementTree.parse(path)
        except ElementTree.ParseError as error:
            errors.append(f"{path.relative_to(ROOT)}: invalid SVG XML: {error}")

    for note in PROTECTED_NOTES:
        if note not in ui_css:
            errors.append(f"atelier-ui.css: protected design note missing: {note}")

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if "GNU AFFERO GENERAL PUBLIC LICENSE" not in license_text:
        errors.append("LICENSE: expected the GNU AGPL license text")
    icon_license = (ROOT / "icons" / "LICENSE").read_text(encoding="utf-8")
    if "ISC License" not in icon_license or "The MIT License" not in icon_license:
        errors.append("icons/LICENSE: expected both Lucide ISC and Feather MIT notices")

    coverage_path = ROOT / "docs" / "component-coverage.md"
    if not coverage_path.is_file():
        errors.append("docs/component-coverage.md: component matrix is required")
    else:
        coverage = coverage_path.read_text(encoding="utf-8")
        for component in ("Button", "Checkbox", "Sidebar", "Table", "Sonner"):
            if f"| {component} |" not in coverage:
                errors.append(
                    "docs/component-coverage.md: missing native component row: "
                    + component
                )

    if errors:
        for error in errors:
            fail(error)
        return 1

    print(f"checked {len(text_files)} text files and {len(svg_files)} SVG files")
    print(
        "CSS, metadata, links, SVGs, custom properties, RTL tokens, "
        "and licenses are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
