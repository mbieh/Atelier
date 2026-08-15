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
    # Menu items must keep overriding Mapco's width: 100%, which would overflow
    # the menu by their inline margins. The explicit calc() also stretches
    # button entries, which stay content-sized under width: auto.
    "width: calc(100% - 8px) !important",
)
REQUIRED_LAYOUT_RULES = (
    "grid-template-rows: auto minmax(min-content, 1fr);",
    "grid-row: 1 / -1;",
    "#global > .nav_menu ~ main",
    'grid-template-areas: "read favorite website thumbnail content labels share link";',
    "--at-form-label-width: 13rem;",
    "--at-dashboard-width: 96rem;",
    ".prompt .form-group:not([hidden])",
    ".post .form-group:not([hidden]):not(.hidden)",
    "main.post.content",
    "html.controller_stats main.post",
    "grid-template-columns: var(--at-form-label-width) minmax(0, 1fr);",
    ".post .group-controls > .stick",
    ".post .form-group.form-actions",
    "backdrop-filter: none;",
    "block-size: var(--at-header-height);",
    "grid-template-columns: var(--width-aside, 300px) minmax(0, 1fr) auto;",
    "grid-template-columns: auto minmax(0, 1fr) auto;",
    ".aside_feed .tree-folder.category[data-unread]",
    ".tree-folder-title[data-unread]:not([data-unread=",
    "#sidebar .tree-folder > .tree-folder-title > button.dropdown-toggle",
    "padding-block: 0;",
    "max-inline-size: none;",
)
COLLAPSED_SIDEBAR_STATE = re.compile(
    r"#global\s*>\s*\.aside\.is-hidden\s*\{"
    r"(?=[^}]*display:\s*block;)"
    r"(?=[^}]*width:\s*0;)"
    r"(?=[^}]*visibility:\s*hidden;)"
    r"[^}]*\}",
    re.DOTALL,
)
FOCUS_GATED_SIDEBAR_TRANSITION = re.compile(
    r"#global:has\([^{}]*#nav_menu_toggle_aside\s+button:focus[^{}]*\)"
    r"\s*>\s*\.aside(?:\.is-hidden)?\s*\{[^}]*transition:",
    re.DOTALL,
)
REQUIRED_DARK_ICON_SELECTORS = (
    '#sidebar img.icon:not([src$="/starred.svg"])',
)
RTL_SOURCE_FILES = (
    "_components.css",
    "_configuration.css",
    "_divers.css",
    "_fonts.css",
    "_forms.css",
    "_global-view.css",
    "_layout.css",
    "_list-view.css",
    "_logs.css",
    "_mobile.css",
    "_reader-view.css",
    "_sidebar.css",
    "_stats.css",
    "_tables.css",
    "_variables.css",
    "atelier-ui.css",
)

# Atelier ships byte-identical RTL counterparts, which is only correct while
# these sources stay direction-neutral. Every construct below either has a
# logical-property equivalent or needs a hand-written mirror, so it has to live
# in a :dir(...) rule or carry an "rtl-safe:" comment stating why it already
# reads correctly in both directions. The marker is accepted on the
# declaration's own line, the line above it, or the rule's selector line.
RTL_SAFE_MARKER = "rtl-safe"

# CSS property names are case-insensitive, so every pattern below has to be.
PHYSICAL_PROPERTY = re.compile(
    r"(?<![\w-])(?:"
    r"(?:padding|margin|scroll-margin|scroll-padding)-(?:left|right)"
    r"|border-(?:left|right)(?:-(?:width|style|color))?"
    r"|border-(?:top|bottom)-(?:left|right)-radius"
    r"|left|right"
    r")(?![\w-])\s*:",
    re.IGNORECASE,
)
PHYSICAL_KEYWORD = re.compile(
    r"(?<![\w-])(?:text-align|float|clear|background|background-position"
    r"|object-position|transform-origin|perspective-origin)"
    r"(?![\w-])\s*:[^;]*?(?<![\w-])(?:left|right)(?![\w-])",
    re.IGNORECASE,
)
HORIZONTAL_TRANSLATE = re.compile(
    r"(?<![\w-])(?:translate(?:X|3d)?\s*\(|translate\s*:)", re.IGNORECASE
)
BOX_SHORTHAND = re.compile(
    r"(?<![\w-])(padding|margin|inset|scroll-margin|scroll-padding)"
    r"(?![\w-])\s*:\s*(.+)",
    re.DOTALL | re.IGNORECASE,
)
RADIUS_SHORTHAND = re.compile(
    r"(?<![\w-])border-radius(?![\w-])\s*:\s*(.+)", re.DOTALL | re.IGNORECASE
)
# Shadow values also reach the page through --*-shadow-* custom properties,
# which no box-shadow declaration would reveal to this check.
SHADOW_SHORTHAND = re.compile(
    r"(?<![\w-])(?:(?:box|text)-shadow|--[\w-]*shadow[\w-]*)(?![\w-])\s*:\s*(.+)",
    re.DOTALL | re.IGNORECASE,
)
IMPORTANT_SUFFIX = re.compile(r"\s*!\s*important\s*$", re.IGNORECASE)
LENGTH_TOKEN = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)")
ZERO_LENGTH = re.compile(r"^[+-]?0*\.?0*(?:[a-z%]*)$", re.IGNORECASE)


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


def split_top_level(value: str, separator: str = " ") -> list[str]:
    """Split on a separator that is not nested inside parentheses."""
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for char in value:
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif depth == 0 and (char == separator or (separator == " " and char.isspace())):
            parts.append("".join(current))
            current = []
            continue
        current.append(char)
    parts.append("".join(current))
    return [part.strip() for part in parts if part.strip()]


def iter_declarations(stripped: str):
    """Yield (line, text, inside_dir_rule, selector_line) for each declaration.

    Works on comment- and string-stripped CSS, so line numbers still line up
    with the original file. Nesting and at-rules are handled by treating every
    brace-delimited block the same way.
    """
    buffer: list[str] = []
    start_line = 1
    line = 1
    blocks: list[tuple[bool, int]] = []
    for char in stripped:
        if char == "{":
            selector = "".join(buffer)
            inherited = bool(blocks and blocks[-1][0])
            blocks.append((inherited or ":dir(" in selector, start_line))
            buffer = []
        elif char in {"}", ";"}:
            text = "".join(buffer).strip()
            if text and blocks:
                yield start_line, text, blocks[-1][0], blocks[-1][1]
            buffer = []
            if char == "}" and blocks:
                blocks.pop()
        elif buffer or not char.isspace():
            # Leading whitespace is dropped so start_line marks the first real
            # character of the selector or declaration.
            if not buffer:
                start_line = line
            buffer.append(char)
        if char == "\n":
            line += 1


def describe_direction_risk(declaration: str) -> str | None:
    """Return why a declaration needs a mirror, or None if it is neutral."""
    # An !important suffix is an extra value token that would otherwise hide
    # asymmetric shorthands from the arity checks below.
    declaration = IMPORTANT_SUFFIX.sub("", declaration)
    if PHYSICAL_PROPERTY.search(declaration):
        return "physical property without a logical equivalent"
    if PHYSICAL_KEYWORD.search(declaration):
        return "left/right keyword value"
    if HORIZONTAL_TRANSLATE.search(declaration):
        return "translate() with a horizontal component"

    box = BOX_SHORTHAND.match(declaration)
    if box:
        values = split_top_level(box.group(2))
        if len(values) == 4 and values[1] != values[3]:
            return f"asymmetric {box.group(1)} shorthand"

    radius = RADIUS_SHORTHAND.match(declaration)
    if radius:
        value = radius.group(1)
        if "/" in value:
            return "elliptical border-radius shorthand"
        corners = split_top_level(value)
        if len(corners) == 2:
            corners = [corners[0], corners[1], corners[0], corners[1]]
        elif len(corners) == 3:
            corners = [corners[0], corners[1], corners[2], corners[1]]
        if len(corners) == 4 and (
            corners[0] != corners[1] or corners[2] != corners[3]
        ):
            return "horizontally asymmetric border-radius"

    shadow = SHADOW_SHORTHAND.match(declaration)
    if shadow:
        for layer in split_top_level(shadow.group(1), ","):
            for token in split_top_level(layer):
                if not LENGTH_TOKEN.match(token):
                    continue
                if not ZERO_LENGTH.match(token):
                    return "shadow with a horizontal offset"
                break
    return None


def check_direction_neutral(path: Path, css: str) -> list[str]:
    try:
        stripped = strip_css_comments_and_strings(css)
    except ValueError as error:
        return [f"{path}: {error}"]
    raw_lines = css.splitlines()

    def marked(*anchors: int) -> bool:
        """Look for the marker on an anchor line or in the comment above it."""
        for anchor in anchors:
            number = anchor
            while 1 <= number <= len(raw_lines):
                text = raw_lines[number - 1]
                if RTL_SAFE_MARKER in text:
                    return True
                stripped_line = text.strip()
                comment_like = (
                    not stripped_line
                    or stripped_line.startswith(("/*", "*"))
                    or stripped_line.endswith("*/")
                )
                if number != anchor and not comment_like:
                    break
                number -= 1
        return False

    errors: list[str] = []
    for line, declaration, inside_dir, selector_line in iter_declarations(stripped):
        if inside_dir:
            continue
        risk = describe_direction_risk(declaration)
        if risk is None:
            continue
        if marked(line, selector_line):
            continue
        errors.append(
            f"{path}:{line}: {risk}; use a logical property, mirror it in a "
            f":dir(rtl) rule, or add an /* {RTL_SAFE_MARKER}: ... */ comment"
        )
    return errors


def check_local_markdown_links(path: Path, content: str) -> list[str]:
    errors: list[str] = []
    for raw_target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
        parts = raw_target.split(maxsplit=1)
        if not parts:
            errors.append(f"{path.relative_to(ROOT)}: empty link target")
            continue
        target = parts[0]
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

    for filename in RTL_SOURCE_FILES:
        source = ROOT / filename
        mirror = source.with_name(f"{source.stem}.rtl{source.suffix}")
        if not mirror.is_file():
            errors.append(f"{mirror.name}: missing generated RTL counterpart")
        elif source.read_bytes() != mirror.read_bytes():
            errors.append(f"{mirror.name} must be identical to {filename}")

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
    for filename in RTL_SOURCE_FILES:
        path = ROOT / filename
        errors.extend(
            check_direction_neutral(Path(filename), path.read_text(encoding="utf-8"))
        )

    for rule in REQUIRED_LAYOUT_RULES:
        if rule not in ui_css:
            errors.append("atelier-ui.css: missing desktop grid rule: " + rule)
    if not COLLAPSED_SIDEBAR_STATE.search(ui_css):
        errors.append(
            "atelier-ui.css: collapsed sidebar must have a hidden zero-width state"
        )
    if not FOCUS_GATED_SIDEBAR_TRANSITION.search(ui_css):
        errors.append(
            "atelier-ui.css: sidebar transition must be gated by toggle focus"
        )
    if "grid-row: 1 / span" in ui_css:
        errors.append("atelier-ui.css: do not use an arbitrary sidebar row span")
    for obsolete_layout in (
        "margin-inline-start: -2.5rem",
        "width: 195px",
        ".tree-folder-title:not([data-unread=",
        "transition: width 0.25s ease",
        "grid-template-columns: fit-content(14rem) minmax(0, 1fr);",
        "grid-template-columns: subgrid;",
    ):
        if obsolete_layout in ui_css:
            errors.append(
                "atelier-ui.css: obsolete fixed layout remains: "
                + obsolete_layout
            )

    for selector in REQUIRED_DARK_ICON_SELECTORS:
        if selector not in ui_css:
            errors.append(
                "atelier-ui.css: missing dark-mode icon selector: " + selector
            )

    svg_files = sorted((ROOT / "icons").glob("*.svg"))
    lucide_files = [path for path in svg_files if path.name not in NON_LUCIDE_SVGS]
    if len(lucide_files) != 55:
        errors.append(f"expected 55 Lucide SVGs, found {len(lucide_files)}")
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
