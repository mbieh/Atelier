# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## Unreleased

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

### Development

- Expanded local checks for manifest order, imports, local Markdown links,
  runtime asset URLs, SVG validity, RTL token parity, and license files.
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
