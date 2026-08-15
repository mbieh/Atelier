#!/usr/bin/env python3
"""Run dependency-free release checks for the Atelier theme."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import NamedTuple
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
    "--frss-dragdrop-color",
    "--frss-dragdrop-color-transparent",
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
DESKTOP = "@media (min-width: 841px)"
DARK = "@media (prefers-color-scheme: dark)"
SETTINGS_CONTAINER = "@container at-settings"


class LayoutRule(NamedTuple):
    """A layout invariant, anchored to the rule that is meant to carry it.

    `selector` has to equal one entry of a parsed rule's selector list, and
    `declaration` has to match a declaration of that same rule, both after
    whitespace normalisation; `context` matches as a substring of one of the
    rule's enclosing at-rule preludes. Anchoring matters twice over: bare
    declarations such as "flex-direction: column" occur all over the file, and
    a short selector like ".btn" is a substring of a dozen others, so neither
    guards anything on its own.

    Set `partial` for the handful of anchors that are deliberately a fragment
    of a longer selector -- a descendant tail, or a selector nested inside
    :has(). Those match as a substring instead.
    """

    selector: str
    declaration: str | None = None
    context: str | None = None
    partial: bool = False


REQUIRED_LAYOUT_RULES = (
    # Desktop shell: sidebar column and content card.
    LayoutRule("#global", "grid-template-rows: auto minmax(min-content, 1fr)", DESKTOP),
    LayoutRule("#global > .aside", "grid-row: 1 / -1", DESKTOP),
    LayoutRule("#global > .nav_menu ~ main", context=DESKTOP),
    LayoutRule("body", "flex-direction: column", DESKTOP),
    # The row carries its own leading inset, so the feed eyebrow stays flush
    # with the title even when the topline hides the read and favorite
    # controls and .item.website becomes the first child.
    LayoutRule(".flux .flux_header", "margin-inline: 0.5rem"),
    LayoutRule(".flux .flux_header", "inline-size: calc(100% - 1rem)"),
    LayoutRule(".flux .flux_header > .item:first-child", "padding-inline-start: 0"),
    LayoutRule(".flux.current", "border-inline-start-width: 0"),
    LayoutRule(".flux_header", "border-top: 0"),
    # The feed popover is a compact command menu. Its item geometry must
    # override Mapco's inherited 2.5em line height without changing markup.
    LayoutRule(
        ".aside_feed .tree-folder-items .feed > .dropdown > .dropdown-menu",
        "min-inline-size: 15rem",
    ),
    LayoutRule(
        ".aside_feed .tree-folder-items .feed > .dropdown > .dropdown-menu .item > :is( a, button, .as-link )",
        "min-block-size: 2.25rem",
    ),
    # Article rows and their subgrid cells.
    LayoutRule(
        ".flux_header",
        'grid-template-areas: "read favorite thumbnail content labels share link"',
        DESKTOP,
    ),
    LayoutRule(
        ".flux_header.websiteicon",
        'grid-template-areas: "read favorite thumbnail website content labels share'
        ' link"',
        DESKTOP,
    ),
    LayoutRule(
        ".flux_header:is(.websitename, .websitefull) > .item.titleAuthorSummaryDate",
        "grid-template-columns: subgrid",
        DESKTOP,
    ),
    LayoutRule(
        ".flux_header:is(.websitename, .websitefull) > .item.titleAuthorSummaryDate",
        "grid-template-rows: subgrid",
        DESKTOP,
    ),
    LayoutRule(
        ".flux_header:is(.websitename, .websitefull) > .item.manage:has(.read)",
        "grid-row: 1 / var(--at-article-row-end)",
        DESKTOP,
    ),
    LayoutRule(
        ".flux_header:is(.websitename, .websitefull) > .item.thumbnail",
        "grid-row: 1 / var(--at-article-row-end)",
        DESKTOP,
    ),
    LayoutRule(
        ".flux_header:is(.websitename, .websitefull) > .item.titleAuthorSummaryDate",
        "grid-row: 1 / var(--at-article-row-end)",
        DESKTOP,
    ),
    LayoutRule(".flux_header:not(.has-thumbnail)", context=DESKTOP),
    LayoutRule(".flux_header.websiteicon:not(.has-thumbnail)", context=DESKTOP),
    LayoutRule(
        ".flux_header:is(.websitename, .websitefull):not(.has-summary)", context=DESKTOP
    ),
    LayoutRule(
        ".flux_header:is(.websitename, .websitefull).has-summary >",
        context=DESKTOP,
        partial=True,
    ),
    LayoutRule(
        ".flux_header > :is(.item.manage, .item.labels, .item.share, .item.link)",
        context=DESKTOP,
    ),
    LayoutRule("#stream .flux .flux_header:hover .item.titleAuthorSummaryDate > .title"),
    LayoutRule(
        ".item.titleAuthorSummaryDate > .title .author::before",
        context=DESKTOP,
        partial=True,
    ),
    LayoutRule(
        ".item.titleAuthorSummaryDate > .summary", context=DESKTOP, partial=True
    ),
    LayoutRule(
        ".flux .flux_content > footer > .bottom > .item.date",
        "margin-inline-start: auto",
        DESKTOP,
    ),
    LayoutRule(".flux_content .content > header h1.title"),
    # Header and sidebar.
    LayoutRule(
        ".header",
        "grid-template-columns: var(--width-aside, 300px) minmax(0, 1fr) auto",
        DESKTOP,
    ),
    LayoutRule(".header", "block-size: var(--at-header-height)", DESKTOP),
    LayoutRule(".nav_menu.nav_mobile", context=DESKTOP),
    LayoutRule(
        ".aside_feed .tree-folder-items .item > .item-title",
        "grid-template-columns: auto minmax(0, 1fr) auto",
    ),
    LayoutRule(".aside_feed .tree-folder.category[data-unread]"),
    LayoutRule(".tree-folder-title[data-unread]:not([data-unread=", partial=True),
    LayoutRule("#sidebar .tree-folder > .tree-folder-title > button.dropdown-toggle"),
    # Configuration sidebar: the duplicated back link and its empty section.
    LayoutRule(".item.nav-section:first-child:not(", partial=True),
    LayoutRule('a[href*="c=index"][href*="a=index"]', partial=True),
    LayoutRule(
        ".aside.nav-list > ul:has( > .item.nav-section:first-child > ul >"
        " .item:nth-child(2) )",
        "flex-direction: column",
    ),
    # Forms, dashboards and controls.
    LayoutRule(":root", "--at-form-label-width: 13rem"),
    LayoutRule(":root", "--at-dashboard-width: 96rem"),
    LayoutRule(".prompt .form-group:not([hidden])"),
    LayoutRule(".post .form-group:not([hidden]):not(.hidden)"),
    LayoutRule("main.post.content"),
    LayoutRule("html.controller_stats main.post"),
    LayoutRule(
        ".post .form-group",
        "grid-template-columns: var(--at-form-label-width) minmax(0, 1fr)",
        SETTINGS_CONTAINER,
    ),
    LayoutRule(".post .group-controls > .stick"),
    LayoutRule(".post .form-group.form-actions", "backdrop-filter: none"),
    LayoutRule(".btn", "padding-block: 0"),
    LayoutRule(".btn", "block-size: var(--at-control-size)"),
    LayoutRule(".header .item.search input", "max-inline-size: none"),
    # One shared control size and uniform boundaries. Inputs remain easier to
    # identify through --input; toolbar groups use the quieter --border token.
    LayoutRule(":root", "--at-control-size: 2.5rem"),
    LayoutRule(":root", "--at-field-border: var(--input)"),
    LayoutRule(":root", "--at-button-border: var(--border)"),
    LayoutRule(".btn", "border: 1px solid var(--at-button-border)"),
    LayoutRule("input", "border: 1px solid var(--at-field-border)"),
    LayoutRule(
        ".header .item.search input", "border: 1px solid var(--at-field-border)"
    ),
    # Each segmented toolbar group owns exactly one bordered card surface.
    LayoutRule(".nav_menu .stick", "background: var(--card)"),
    LayoutRule(".nav_menu .stick", "border: 1px solid var(--at-button-border)"),
    LayoutRule(".nav_menu .stick", "overflow: visible"),
    LayoutRule(
        ".nav_menu :is(.stick, .group) > .dropdown",
        "block-size: 100%",
    ),
    LayoutRule(
        ".nav_menu :is(.stick, .group) .dropdown:not(#dropdown-search-wrapper) > a.dropdown-toggle",
        "background-image: none",
    ),
    LayoutRule(
        ".nav_menu :is(.stick, .group) .dropdown:not(#dropdown-search-wrapper) > a.dropdown-toggle::before",
        'mask: url("icons/more.svg") center / 1rem 1rem no-repeat',
    ),
    LayoutRule("#nav_menu_sort #toggle-order::before", "content: none"),
    LayoutRule("#nav_menu_sort #toggle-order > .icon", "display: block"),
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
OBSOLETE_FORM_SUBGRID = re.compile(
    r"\.post\s+:is\(form,\s*fieldset\)\s*>\s*\.form-group\s*\{"
    r"[^}]*grid-template-columns:\s*subgrid;",
    re.DOTALL,
)
REQUIRED_DARK_ICON_RULES = (
    LayoutRule('#sidebar img.icon:not([src$="/starred.svg"])', context=DARK),
)

# Every stylesheet Atelier owns. All of them have to stay direction-neutral,
# whether FreshRSS requests them by name or atelier.css pulls them in.
DIRECTION_NEUTRAL_FILES = (
    "_components.css",
    "_palette.css",
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
    "atelier.css",
    "atelier-ui.css",
)

# FreshRSS rewrites only the filenames listed in metadata.json to ".rtl.css",
# with no existence check and no fallback (app/FreshRSS.php), so exactly these
# two need a mirror on disk. The partials above are reached through atelier.css
# @import rules, which resolve relative to the sheet, so they need none.
RTL_MIRRORED_FILES = ("atelier.css", "atelier-ui.css")

# Because the sources stay direction-neutral, each mirror is a verbatim copy.
# Every construct the direction check rejects either has a logical-property
# equivalent or needs a hand-written mirror, so it has to live in a :dir(...)
# rule or carry an "rtl-safe:" comment stating why it already reads correctly
# in both directions. The marker is accepted on the declaration's own line, the
# line above it, or the rule's selector line.
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


def check_css_syntax(path: Path, css: str) -> list[str]:
    """Report the first structural defect the parser trips over, if any."""
    try:
        parse_rules(css)
    except ValueError as error:
        return [f"{path}: {error}"]
    return []


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


class Declaration(NamedTuple):
    text: str
    """Whitespace-normalised source text, strings intact."""
    sanitized: str
    """Same declaration with string literals blanked, for pattern matching."""
    line: int


class Rule(NamedTuple):
    selector: str
    line: int
    context: tuple[str, ...]
    """Enclosing selectors and at-rule preludes, outermost first."""
    declarations: tuple[Declaration, ...]

    @property
    def dir_scoped(self) -> bool:
        """True when the rule only applies to one writing direction."""
        return any(":dir(" in part for part in (*self.context, self.selector))


def normalize(text: str) -> str:
    return " ".join(text.split()).rstrip(";").rstrip()


def parse_rules(css: str) -> list[Rule]:
    """Return a Rule for every brace-delimited block, nesting and at-rules alike.

    Comments are skipped and string literals are consumed whole, so neither can
    hide a brace or a semicolon from the block structure. Line numbers refer to
    the original source.
    """
    rules: list[Rule] = []
    stack: list[tuple[str, int, list[Declaration]]] = []
    buffer: list[str] = []
    sanitized: list[str] = []
    start_line = 1
    line = 1
    index = 0
    length = len(css)

    def take() -> tuple[str, str]:
        nonlocal buffer, sanitized
        pending = ("".join(buffer), "".join(sanitized))
        buffer = []
        sanitized = []
        return pending

    while index < length:
        char = css[index]
        following = css[index + 1] if index + 1 < length else ""
        if char == "/" and following == "*":
            end = css.find("*/", index + 2)
            end = length if end == -1 else end + 2
            line += css.count("\n", index, end)
            index = end
            continue
        if char in {'"', "'"}:
            end = index + 1
            while end < length:
                if css[end] == "\\":
                    end += 2
                    continue
                if css[end] == char:
                    end += 1
                    break
                end += 1
            else:
                raise ValueError("unterminated CSS string")
            if not buffer:
                start_line = line
            buffer.append(css[index:end])
            sanitized.append(" " * (end - index))
            line += css.count("\n", index, end)
            index = end
            continue
        if char == "{":
            selector_text, _ = take()
            stack.append((normalize(selector_text), start_line, []))
        elif char in {"}", ";"}:
            raw, clean = take()
            text = normalize(raw)
            if text and stack:
                stack[-1][2].append(Declaration(text, normalize(clean), start_line))
            if char == "}":
                if not stack:
                    raise ValueError(f"unmatched closing brace on line {line}")
                selector, selector_line, declarations = stack.pop()
                rules.append(
                    Rule(
                        selector,
                        selector_line,
                        tuple(entry[0] for entry in stack),
                        tuple(declarations),
                    )
                )
        elif buffer or not char.isspace():
            # Leading whitespace is dropped so start_line marks the first real
            # character of the selector or declaration.
            if not buffer:
                start_line = line
            buffer.append(char)
            sanitized.append(char)
        if char == "\n":
            line += 1
        index += 1

    if stack:
        raise ValueError(f"unmatched opening brace on line {stack[-1][1]}")
    return rules


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
        rules = parse_rules(css)
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
    for rule in rules:
        if rule.dir_scoped:
            continue
        for declaration in rule.declarations:
            risk = describe_direction_risk(declaration.sanitized)
            if risk is None:
                continue
            if marked(declaration.line, rule.line):
                continue
            errors.append(
                f"{path}:{declaration.line}: {risk}; use a logical property, "
                f"mirror it in a :dir(rtl) rule, or add an "
                f"/* {RTL_SAFE_MARKER}: ... */ comment"
            )
    return sorted(errors, key=lambda entry: int(entry.split(":")[1]))


def check_required_rules(
    path: Path, rules: list[Rule], required: tuple[LayoutRule, ...], label: str
) -> list[str]:
    """Report every invariant that no parsed rule satisfies."""
    errors: list[str] = []
    for wanted in required:
        for rule in rules:
            if wanted.partial:
                if wanted.selector not in rule.selector:
                    continue
            elif wanted.selector not in split_top_level(rule.selector, ","):
                continue
            if wanted.context is not None and not any(
                wanted.context in part for part in rule.context
            ):
                continue
            if wanted.declaration is not None and not any(
                wanted.declaration == declaration.text
                for declaration in rule.declarations
            ):
                continue
            break
        else:
            detail = wanted.selector
            if wanted.declaration is not None:
                detail += f" {{ {wanted.declaration}; }}"
            if wanted.context is not None:
                detail += f" inside {wanted.context}"
            errors.append(f"{path}: missing {label}: {detail}")
    return errors


def released_version(changelog: str) -> str | None:
    """Return the newest released version heading from the changelog."""
    for match in re.finditer(r"(?m)^##\s+(\d+\.\d+\.\d+)\b", changelog):
        return match.group(1)
    return None


# The neutral ramp every color scheme has to provide, plus the two rungs
# Atelier derives from it. Roles pick a step by the contrast they need, so a
# scheme that skips a step would silently shift whatever role points at it.
SCALE_STEPS = (50, 100, 200, 300, 400, 500, 600, 700, 750, 800, 900, 950)
SCALE_EXTRA = ("--at-scale-white",)

# WCAG 2.2: 4.5:1 for body text (1.4.3), 3:1 for the boundary of a control
# and for focus indicators (1.4.11). Each entry is a role painted on a
# surface it actually meets in the UI. This is what keeps a new palette
# honest -- the ramp guarantees nothing on its own.
CONTRAST_PAIRS = (
    ("--foreground", "--card", 4.5),
    ("--foreground", "--background", 4.5),
    ("--foreground", "--accent", 4.5),
    ("--card-foreground", "--card", 4.5),
    ("--popover-foreground", "--popover", 4.5),
    ("--muted-foreground", "--card", 4.5),
    ("--muted-foreground", "--background", 4.5),
    ("--muted-foreground", "--muted", 4.5),
    ("--muted-foreground", "--accent", 4.5),
    ("--secondary-foreground", "--secondary", 4.5),
    ("--accent-foreground", "--accent", 4.5),
    ("--primary-foreground", "--primary", 4.5),
    ("--destructive-foreground", "--destructive", 4.5),
    ("--sidebar-foreground", "--sidebar", 4.5),
    ("--sidebar-accent-foreground", "--sidebar-accent", 4.5),
    ("--sidebar-primary-foreground", "--sidebar-primary", 4.5),
    # Control boundaries and focus rings against the surfaces they sit on.
    ("--input", "--card", 3.0),
    ("--input", "--background", 3.0),
    ("--input", "--muted", 3.0),
    ("--ring", "--card", 3.0),
    ("--ring", "--background", 3.0),
    ("--sidebar-ring", "--sidebar", 3.0),
    # Accent hues, in the roles they are actually painted in. Alert text sits
    # on its own tint; --destructive doubles as error text; --favorite is the
    # star that marks a favorited article and has to read as a graphical
    # indicator on every row background it can land on.
    ("--success-foreground", "--success-muted", 4.5),
    ("--warning-foreground", "--warning-muted", 4.5),
    ("--info-foreground", "--info-muted", 4.5),
    ("--destructive", "--card", 4.5),
    ("--destructive", "--background", 4.5),
    ("--favorite", "--card", 3.0),
    ("--favorite", "--background", 3.0),
    ("--favorite", "--favorite-muted", 3.0),
)

# Deliberately not checked: the border of an alert against its own tint. The
# alert is identified by that tint and its text, both of which are checked
# above, so the border is a delimiter rather than the carrier of the state.
# Likewise --at-button-border: a button is identified by its label or icon,
# which are checked as text on --card, and by a raised surface and a focus
# ring that is checked. Only fields, whose empty boundary is the whole
# affordance, are held to 3:1 through --input.

# The favorite star is an external SVG, which cannot inherit currentColor and
# is excluded from the dark-mode icon filter on purpose. Its color therefore
# lives in the asset, out of reach of the contrast pairs above, and would
# drift away from the token without anyone noticing.
FAVORITE_ICON = Path("icons") / "starred.svg"
SVG_COLOR = re.compile(r'(?:fill|stroke)="(#[0-9a-fA-F]{3,6})"')

HEX_COLOR = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
COLOR_MIX = re.compile(
    r"^color-mix\(\s*in\s+srgb\s*,\s*(.+?)\s+([\d.]+)%\s*,\s*(.+?)\s*\)$",
    re.IGNORECASE | re.DOTALL,
)
VAR_REFERENCE = re.compile(r"^var\(\s*(--[\w-]+)\s*\)$")


def parse_hex(value: str) -> tuple[float, float, float]:
    digits = value.lstrip("#")
    if len(digits) == 3:
        digits = "".join(channel * 2 for channel in digits)
    return tuple(int(digits[i : i + 2], 16) for i in (0, 2, 4))


def resolve_color(
    name: str, declarations: dict[str, str], seen: frozenset[str] = frozenset()
) -> tuple[float, float, float] | None:
    """Resolve a custom property to sRGB, following var() and color-mix().

    Returns None for anything outside that subset -- `transparent`, a gradient,
    a color function the theme does not use -- so the caller can report it
    rather than pass a role through unchecked.
    """
    if name in seen:
        return None
    value = declarations.get(name)
    if value is None:
        return None
    return resolve_value(value, declarations, seen | {name})


def resolve_value(
    value: str, declarations: dict[str, str], seen: frozenset[str]
) -> tuple[float, float, float] | None:
    value = value.strip()
    if HEX_COLOR.match(value):
        return parse_hex(value)
    reference = VAR_REFERENCE.match(value)
    if reference:
        return resolve_color(reference.group(1), declarations, seen)
    mix = COLOR_MIX.match(value)
    if mix:
        first = resolve_value(mix.group(1), declarations, seen)
        second = resolve_value(mix.group(3), declarations, seen)
        if first is None or second is None:
            return None
        weight = float(mix.group(2)) / 100
        return tuple(first[i] * weight + second[i] * (1 - weight) for i in range(3))
    return None


def relative_luminance(color: tuple[float, float, float]) -> float:
    def channel(value: float) -> float:
        value /= 255
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    red, green, blue = (channel(part) for part in color)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(
    first: tuple[float, float, float], second: tuple[float, float, float]
) -> float:
    lighter, darker = sorted(
        (relative_luminance(first), relative_luminance(second)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


def scheme_declarations(rules: list[Rule], dark: bool) -> dict[str, str]:
    """Collect :root custom properties for one color scheme.

    Later declarations win, and the dark scheme is layered on top of the light
    one exactly as the cascade applies it.
    """
    values: dict[str, str] = {}
    for rule in rules:
        if ":root" not in split_top_level(rule.selector, ","):
            continue
        in_dark = any("prefers-color-scheme: dark" in part for part in rule.context)
        if in_dark and not dark:
            continue
        for declaration in rule.declarations:
            if not declaration.text.startswith("--"):
                continue
            name, _, value = declaration.text.partition(":")
            values[name.strip()] = value.strip()
    return values


def check_contrast(rules: list[Rule]) -> list[str]:
    errors: list[str] = []
    for dark in (False, True):
        scheme = "dark" if dark else "light"
        declarations = scheme_declarations(rules, dark)
        for step in SCALE_STEPS:
            name = f"--at-scale-{step}"
            if name not in declarations:
                errors.append(f"{scheme} scheme: palette is missing {name}")
        for name in SCALE_EXTRA:
            if name not in declarations:
                errors.append(f"{scheme} scheme: palette is missing {name}")
        for foreground, background, minimum in CONTRAST_PAIRS:
            front = resolve_color(foreground, declarations)
            back = resolve_color(background, declarations)
            if front is None or back is None:
                errors.append(
                    f"{scheme} scheme: cannot resolve {foreground} on {background}; "
                    "the contrast guard needs both to reduce to sRGB"
                )
                continue
            ratio = contrast_ratio(front, back)
            if ratio + 0.005 < minimum:
                errors.append(
                    f"{scheme} scheme: {foreground} on {background} is "
                    f"{ratio:.2f}:1, below the required {minimum}:1"
                )

    light = scheme_declarations(rules, dark=False)
    token = resolve_color("--favorite", light)
    icon = (ROOT / FAVORITE_ICON).read_text(encoding="utf-8")
    painted = {match.lower() for match in SVG_COLOR.findall(icon)}
    if token is None:
        errors.append("--favorite must reduce to sRGB so the star can be checked")
    elif len(painted) != 1:
        errors.append(
            f"{FAVORITE_ICON}: expected a single color, found "
            + (", ".join(sorted(painted)) or "none")
        )
    else:
        expected = "#%02x%02x%02x" % tuple(round(part) for part in token)
        actual = painted.pop()
        if len(actual) == 4:
            actual = "#" + "".join(channel * 2 for channel in actual[1:])
        if actual != expected:
            errors.append(
                f"{FAVORITE_ICON} is {actual} but --favorite is {expected}; the "
                "star cannot inherit currentColor, so the two have to agree"
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
            errors.extend(check_css_syntax(relative, content))
        if path.suffix == ".md":
            errors.extend(check_local_markdown_links(path, content))

    try:
        metadata = json.loads((ROOT / "metadata.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"metadata.json: {error}")
        metadata = {}

    # The changelog is the single source of truth for the released version, so
    # cutting a release does not mean editing this script as well.
    expected_version = released_version(
        (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    )
    if expected_version is None:
        errors.append("CHANGELOG.md: no released version heading found")
    if metadata.get("name") != "Atelier":
        errors.append("metadata.json: name must be Atelier")
    if expected_version is not None and metadata.get("version") != expected_version:
        errors.append(
            f"metadata.json: version must be the string {expected_version!r} to match "
            "the newest CHANGELOG release"
        )
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
    # A palette ships the whole ramp on purpose: a scheme that only defined
    # the steps today's roles happen to use would break the next role change.
    # check_contrast() enforces completeness instead.
    scale = {name for name in definitions if name.startswith("--at-scale-")}
    unused = definitions - uses - EXTERNAL_OR_COMPAT_PROPERTIES - scale
    if unused:
        errors.append("unused custom properties: " + ", ".join(sorted(unused)))

    expected_mirrors = set()
    for filename in RTL_MIRRORED_FILES:
        source = ROOT / filename
        mirror = source.with_name(f"{source.stem}.rtl{source.suffix}")
        expected_mirrors.add(mirror.name)
        if not mirror.is_file():
            errors.append(f"{mirror.name}: missing generated RTL counterpart")
        elif source.read_bytes() != mirror.read_bytes():
            errors.append(f"{mirror.name} must be identical to {filename}")

    # Only the sheets FreshRSS requests by name need a mirror. Partials are
    # reached through @import, so a mirror there is dead weight that has to be
    # kept in sync by hand.
    for path in css_paths:
        if path.name.endswith(".rtl.css") and path.name not in expected_mirrors:
            errors.append(
                f"{path.name}: stray RTL mirror; only "
                f"{', '.join(sorted(expected_mirrors))} are loaded by FreshRSS"
            )

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
    for filename in DIRECTION_NEUTRAL_FILES:
        path = ROOT / filename
        errors.extend(
            check_direction_neutral(Path(filename), path.read_text(encoding="utf-8"))
        )

    try:
        ui_rules = parse_rules(ui_css)
    except ValueError:
        ui_rules = []
    errors.extend(
        check_required_rules(
            Path("atelier-ui.css"), ui_rules, REQUIRED_LAYOUT_RULES, "layout rule"
        )
    )

    token_rules: list[Rule] = []
    for filename in ("_palette.css", "_variables.css", "atelier-ui.css"):
        try:
            token_rules.extend(
                parse_rules((ROOT / filename).read_text(encoding="utf-8"))
            )
        except ValueError:
            pass
    errors.extend(check_contrast(token_rules))
    errors.extend(
        check_required_rules(
            Path("atelier-ui.css"),
            ui_rules,
            REQUIRED_DARK_ICON_RULES,
            "dark-mode icon rule",
        )
    )
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
    ):
        if obsolete_layout in ui_css:
            errors.append(
                "atelier-ui.css: obsolete fixed layout remains: "
                + obsolete_layout
            )
    if OBSOLETE_FORM_SUBGRID.search(ui_css):
        errors.append("atelier-ui.css: obsolete form subgrid layout remains")

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
