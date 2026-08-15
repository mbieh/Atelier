# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## Unreleased

### Added

- `_palette.css` holds the neutral ramp on its own, as the eleven canonical
  Tailwind 4.3 "Mist" steps plus a derived rung for dark raised surfaces. It is
  the only file a color scheme changes; semantic roles, component rules and the
  accent hues for success, warning and destructive are shared. Steps 50 to 700
  were already exactly Mist, so the light scheme keeps its values.
- `check_theme.py` verifies WCAG contrast. It resolves every semantic role
  through `var()` and `color-mix()` down to sRGB and checks it against the
  surfaces it is painted on, separately for the light and the dark scheme —
  4.5:1 for text, 3:1 for control boundaries and focus rings. A role that
  cannot be reduced to sRGB is reported rather than skipped. The palette must
  also be complete, so a scheme cannot omit a step that a role depends on.

### Fixed

- Secondary text now uses ramp step 600 instead of 500. Step 500 met 4.5:1 only
  on the white card and missed it on `--background` (4.14:1) and `--muted`
  (4.44:1). This was not specific to Mist: step 500 misses the mark in eight of
  the nine Tailwind neutrals, step 600 clears it in all nine.
- Control boundaries meet the 3:1 of WCAG 1.4.11. `--input` was ramp step 300,
  which reached 1.47:1 against a white card. Since no step lands near 3:1 — 400
  gives 2.19:1, 500 jumps to 4.14:1 and reads as a hard outline — the role is
  mixed from the two and lands at 3.16 to 3.52:1.
- The dark scheme no longer overrides the control boundary with a 20% blend of
  the foreground, which composited to 1.89:1 against a card and was the worst
  contrast in the theme. Both schemes share one contrast-checked value: a
  mid-grey works as the darker element on light surfaces and as the lighter one
  on dark surfaces.

- The favorite star is legible on a light row. `icons/starred.svg` was
  `#d99e04`, which reached only 2.13 to 2.37:1 against the row backgrounds it
  can land on — below the 3:1 that WCAG 1.4.11 asks of a graphical indicator.
  It is `#ad7d09` now, the one gold that clears the bar on light and dark rows
  alike; an external SVG cannot inherit `currentColor` and the star is
  deliberately exempt from the dark-mode icon filter, so a single value has to
  serve both. `--favorite` matches the asset and no longer differs per scheme,
  and the contrast guard compares the two so they cannot drift apart.
- `--frss-switch-accent-color` named `--success`, but Atelier paints
  `.switch.active` with `--primary` and has done all along. The token now names
  the color that is actually rendered.

### Changed

- Dark surfaces walk down the ramp instead of using hand-picked values: page
  900, cards 800, raised states between 800 and 700, separators 600. The two
  values that were tuned by hand are derived now, so a new scheme does not have
  to supply them.
- The contrast guard covers the accent hues in the roles they are painted in:
  alert text on its own tint, `--destructive` as error text, and the favorite
  star on every row background. The border of an alert against its own tint is
  deliberately excluded — the tint and the text identify the alert, so the
  border delimits rather than informs.

- The feed eyebrow above an article title is flush with the title again. Mapco
  insets the first item of every horizontal list, which is a row inset only as
  long as that item sits in a column of its own. With the read and favorite
  controls switched off in the topline settings, the first item is
  `.item.website`, which shares its grid column with the title, so the eyebrow
  was indented by 7px against the title and summary. The row now carries the
  inset itself, where it shifts every column alike; layouts that do show those
  controls render identically to before.
- Notification toasts now derive their status marker from `--success` and
  `--destructive` instead of two literal colors. The toast paints itself in
  `--foreground`, so it inverts with the color scheme; the literals only held
  up in light mode and dropped the success dot to 1.68:1 and the failure dot
  to 2.66:1 against a dark-mode toast, which left the two variants — otherwise
  identical in background and text color — practically indistinguishable. The
  failure marker is now a diamond as well, so state no longer rests on hue
  alone.
- Fixed the hover state of a toast's close button, which used a near-white
  overlay and disappeared on the light dark-mode toast. It is now mixed from
  `--background`, the toast's own text color, so it inverts along with it.
- Removed a stray yellow fallback from the sidebar scrollbar. Every browser
  that supports the `:dir()`, `:has()` and subgrid rules this theme relies on
  also supports `color-mix()`, so the fallback only ever shadowed the intended
  value.
- The unread counter of the active feed no longer keeps the base theme's
  border, which made it the only pill in the tree with an outline.
- Drag-and-drop feedback follows the palette instead of the base theme's
  literal `#ff0`, which clashed with the Mist neutrals when reordering feeds.

### Changed

- `metadata.json` now carries the version as the semver string `1.1.0`.
  FreshRSS accepts a string or a number, but a JSON number cannot express a
  patch release and made `1.1` and a future `1.10` the same value.
- Dropped the 15 `_*.rtl.css` partial mirrors. FreshRSS rewrites only the
  filenames listed in `metadata.json` to `.rtl.css`, so the partials — reached
  through `@import`, which resolves relative to the importing sheet — never
  needed a mirror. `atelier.rtl.css` now imports the same partials as
  `atelier.css` and is a verbatim copy of it.
- Removed the leftover `lato` font stack from `atelier.css` and `_forms.css`.
  Nothing has declared an `@font-face` for it since `_fonts.css` was emptied,
  and both declarations were already overridden by `--at-sans`.
- Removed the `.form-group::after` clearfix, which declared no `content` and
  so never generated a box.
- The release checks now anchor each layout invariant to the selector and
  at-rule context that is meant to carry it, rather than testing for a raw
  substring anywhere in the file. Declarations such as `flex-direction:
  column` occur up to eight times and a selector as short as `.btn` is a
  substring of a dozen others, so a third of the assertions passed no matter
  which rule was deleted.
- `check_theme.py` reads the expected theme version from the changelog, guards
  `atelier.css` for direction neutrality as well, and rejects partial RTL
  mirrors if they reappear.

## 1.1.0 - 2026-08-15

### Added

- Aligned the sidebar's category rows with its feed rows. The control column is
  now pinned, so a category's collapse button no longer widens it and staggers
  the chevrons and titles against the rows above.
- Added leading Lucide icons to every entry of the settings dropdown, the
  settings sidebar and the subscription sidebar, statistics included. FreshRSS
  emits no icons there, so each entry is keyed off its target URL and drawn as
  a mask tinted with `currentColor`, which follows the hover, active and
  dark-theme foreground without a second asset. Nine new icons join the
  bundle; the rest reuse existing glyphs.
- Added a system-controlled dark color scheme using the existing semantic
  shadcn/ui token layer and locally bundled dark variants for CSS background
  icons.

### Changed

- Refined fully populated article rows into a dense, predictable desktop grid.
  Optional controls now share one action rhythm, feed names truncate cleanly,
  thumbnails retain their configured footprint including borders and a stable
  text gutter, and right-edge actions use a deliberate outer inset. Title,
  author, summary, and date retain a clear hierarchy without animating favicons
  on row hover. Feed names now sit above the title, giving every thumbnail a
  stable shared axis regardless of source-name length, while icon-only sources
  retain their compact inline placement. Rows without thumbnails keep the same
  separation between their actions and textual content, and source metadata
  shares one type scale with publication dates. Image rows without summaries
  no longer reserve an empty content line, keeping their thumbnails and text
  blocks vertically centered; rows with summaries align publication dates with
  their source metadata instead. Expanded article footers now anchor their
  publication date to the trailing edge instead of distributing it across
  FreshRSS's empty fixed-width option cells.
- Removed the redundant “Back to your RSS feeds” action from configuration,
  subscription, statistics, and authenticated error views. The FreshRSS logo
  remains the consistent route back to the feed list. Advanced Search now
  follows the subscription and statistics sections as the final sidebar entry.
- Unified article typography with Atelier's sans-serif hierarchy, including
  linked headings inherited from Mapco. Article titles now wrap predictably,
  keep a stable foreground color, and use a restrained underline on hover.
- Removed Mapco's nested title-only hover fill, which appeared as a second
  rectangle inside the article row. Hovered and open rows now retain their
  subtle full-row state without an additional color behind the title.
- Added a smooth, direction-aware sidebar reveal for explicit toggle actions.
  Persisted collapsed-state restoration remains transition-free, preventing the
  sidebar from flashing open during reloads and feed refreshes. Child controls
  retain their native sizing and spacing throughout the open state.
- Reworked statistics into a responsive full-width dashboard grid and gave
  informational text views a wide, readable content measure instead of fixed
  legacy box widths.
- Replaced direction-specific spacing, borders, and radii in the Atelier UI
  layer with CSS logical properties.
- Replaced view-specific form and fieldset sizing with unified responsive form
  systems for authentication, settings, administration, subscription, profile,
  search, and slider views, including consistent field widths, sections, help
  text, compound controls, and non-sticky action rows.
- Simplified RTL generation now that the UI source handles both directions.
- Consolidated duplicate alert rules and centralized their palette tokens.
- Added a semantic shadcn/ui token layer while preserving Mapco compatibility
  aliases and the existing Mist palette.
- Applied consistent shadcn-style states to native FreshRSS controls, forms,
  cards, tables, pagination, overlays, feedback, and utility surfaces.
- Standardized project-owned documentation, metadata, and code comments in
  English.

### Fixed

- Kept FreshRSS's mobile-only sidebar opener hidden on desktop configuration
  and subscription pages. The generic toolbar layout had exposed it outside
  its intended breakpoint, causing inconsistent placement and styling while
  requiring a first click merely to synchronize its mobile state.
- Prevented the About and Terms content column from collapsing to its
  min-content width or centering itself vertically when combined with the form
  container-query system.
- Fixed the desktop application header to one shared block size and normalized
  its item padding, so the sidebar and main content no longer shift vertically
  between views.
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
- Gave dropdown menus the settings sidebar's inset, so entries, section labels
  and icons share one rhythm across both. Mapco's 2rem left every entry
  indented past its own heading, and a second, redundant 2rem rule scoped to
  `.dropdown-section` restated the same value at a higher specificity; it was
  removed. Sort menus now draw their ✓ in a reserved slot instead of a
  negative margin, which at the smaller inset would have placed the glyph
  outside the entry's hover surface.
- Extended dropdown hover surfaces across the full menu width for button
  entries such as logout and the mark-as-read choices. A button stays
  content-sized at `display: block`, so the previous `width: auto` stretched
  only the link and span entries.
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
