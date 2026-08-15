# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## Unreleased

### Added

- Added a system-controlled dark color scheme using the existing semantic
  shadcn/ui token layer and locally bundled dark variants for CSS background
  icons.

### Changed

- Replaced direction-specific spacing, borders, and radii in the Atelier UI
  layer with CSS logical properties.
- Simplified RTL generation now that the UI source handles both directions.
- Consolidated duplicate alert rules and centralized their palette tokens.
- Added a semantic shadcn/ui token layer while preserving Mapco compatibility
  aliases and the existing Mist palette.
- Applied consistent shadcn-style states to native FreshRSS controls, forms,
  cards, tables, pagination, overlays, feedback, and utility surfaces.
- Standardized project-owned documentation, metadata, and code comments in
  English.

### Fixed

- Preserved the intended information-alert colors that were previously
  overwritten by a later generic alert rule.
- Prevented toast notifications from exceeding very narrow viewports.
- Replaced an invalid `rgba(var(--main-first), ...)` log-row color with a valid
  semantic error surface.
- Removed nested frames from search and toolbar groups, balanced the outer
  gutters, aligned the header controls, centered the toolbar rhythm,
  standardized control heights, increased outline contrast, standardized
  configuration select widths, and restored spacing around the sign-out icon.
- Replaced the folder-shaped sidebar toggle with the conventional Lucide
  `PanelLeft` icon.
- Centered button labels and replaced inconsistent native select arrows with a
  locally bundled Lucide chevron.
- Mapped the shared FreshRSS base-theme colors to Atelier's semantic tokens and
  corrected the current FreshRSS article-title selector so list titles remain
  legible in dark mode, with a matching adaptive surface for theme metadata.
- Softened dark outline controls and toolbar groups with translucent borders
  and a lighter control shadow while preserving the light-theme contrast.
- Restored dark-mode contrast for the main-stream, important-feed, category,
  label, and feed-action icons in the sidebar while preserving feed favicons
  and the gold favorite state.
- Replaced the sidebar's arbitrary grid-row span with an explicit two-row
  desktop layout so short article lists remain directly below the toolbar.
- Replaced inherited table, float, absolute-position, and fixed-width layout
  assumptions in the header, article rows, settings forms, sidebar rows, and
  global feed cards with intrinsic CSS Grid and container-query layouts.
- Kept the tick visible on disabled checkboxes and radios, whose muted fill
  previously covered the checked state.
- Rounded only the outer edges of button groups again, so middle segments no
  longer render as pills between flat end caps.
- Removed the sidebar dropdown toggle's inherited negative margins and inline
  padding, which pushed the button out of its grid row and off-center.
- Made the mobile sidebar's close icon visible. Its bundled SVG stroke is
  `#394447`, the exact light-theme `--primary` that Mapco paints the close bar
  with, so the icon was invisible against its own background; in dark mode the
  global icon inversion left it at 1.17:1 on the inverted bar. It now uses the
  primary foreground in light mode and its native stroke in dark mode.
- Restored sidebar feed names below 840px, where the hidden `.no-mobile`
  dropdown left the title auto-placed in the intrinsic grid column and
  collapsed it to a few characters. Feed rows in the global view had the same
  defect whenever favicons were disabled. Both now place their children
  explicitly.

### Development

- Expanded local checks for manifest order, imports, local Markdown links,
  runtime asset URLs, SVG validity, RTL token parity, and license files.
- Replaced the RTL blocklist with a parser-based direction check that flags
  physical properties, left/right keywords, horizontal translations and
  shadows, and asymmetric box and radius shorthands, exempting `:dir()` rules
  and declarations marked `rtl-safe`. The check ignores a trailing
  `!important`, matches property names case-insensitively, and covers shadow
  values held in custom properties.
- Converted the inherited Mapco partials to logical properties, so all 15
  stylesheets are direction-neutral and every RTL counterpart is generated
  rather than hand-maintained. RTL parity is now asserted for all of them
  instead of only `_variables.css`.
- Added a FreshRSS 1.29.1 component coverage matrix and enforced the required
  semantic token contract in local checks.

## 1.0.0 - 2026-08-14

### Added

- Reproducible RTL generation and dependency-free local release checks.
- Public documentation, license attribution, and CI verification.
- Initial Atelier release based on the official Mapco theme.
- A dedicated shadcn/ui-inspired override layer using the Mist color palette.
- 44 adapted Lucide icons and a local system-font stack.
- An RTL counterpart for the Atelier override layer.

### Changed

- Reworked the desktop layout with CSS Grid so the sidebar stretches to the
  bottom of the page and animates cleanly when collapsed or expanded.
- Widened the date column for longer German date strings.
- Removed excessive whitespace below the “mark all as read” control.
