# Atelier

A modern, light theme for [FreshRSS](https://freshrss.org/) inspired by
contemporary shadcn/ui interfaces.

Atelier combines the structure of FreshRSS's official Mapco theme with a
separate visual override layer, a cool neutral Mist color palette, soft active
states, subtle motion, and Lucide icons. It does not load web fonts, scripts,
or other runtime assets from external services.

![Atelier theme preview](thumbs/original.png)

## Features

- Light, neutral interface designed for comfortable feed reading
- Responsive desktop and mobile layouts
- Animated sidebar collapse without content reflow
- Clear primary, outline, and ghost button hierarchy
- Accessible focus states and reduced-motion support
- Locally bundled SVG icons with no CDN dependency
- Generated RTL stylesheet kept in sync with the main UI layer
- Centralized color tokens for straightforward customization

## Compatibility

Atelier 1.0 has been tested with FreshRSS 1.29.1 in Chromium.

The following areas were verified:

- short and extended list views;
- an opened article;
- the configuration dropdown;
- search-field focus behavior;
- sidebar collapse and expansion;
- configuration pages; and
- a mobile viewport.

The following areas have not yet been explicitly verified:

- global and reader views with the desktop grid layout;
- View Transitions in Firefox;
- the `#actualizeProgress` feed-update indicator;
- the generated RTL layout in an RTL language; and
- FreshRSS versions other than 1.29.1.

## Installation

### Manual installation

1. Download or clone this repository.
2. Ensure that the theme directory is named `Atelier`.
3. Copy the complete directory to `<FreshRSS>/p/themes/Atelier`.
4. Open FreshRSS and select **Configuration → Display → Theme → Atelier**.

The repository root is also the theme root. No build or copy step is required
before installation.

### Docker Compose bind mount

Replace the host path with the absolute path to your checkout:

```yaml
services:
  freshrss:
    volumes:
      - /absolute/path/to/Atelier:/var/www/FreshRSS/p/themes/Atelier:ro
```

Select Atelier in FreshRSS after starting or restarting the container. The
read-only mount prevents the container from modifying the checkout.

## Customization

Theme colors are defined centrally in [`_variables.css`](_variables.css). The
commented Mist values can be replaced with another neutral palette without
changing the component rules. Run the RTL generator after changing these
tokens instead of editing `_variables.rtl.css` manually.

FreshRSS loads the theme layers in this order:

1. `_frss.css` — FreshRSS base styles;
2. `atelier.css` — the Mapco-derived structural layer; and
3. `atelier-ui.css` — Atelier's visual override layer.

For substantial UI changes, prefer adding or updating rules in
`atelier-ui.css` instead of modifying the Mapco-derived modules.

## Repository layout

| Path | Purpose |
| --- | --- |
| `metadata.json` | FreshRSS theme manifest and load order |
| `_variables.css` | Color palette and shared theme tokens |
| `atelier.css` | Mapco-derived structural entry point |
| `atelier-ui.css` | Main Atelier UI implementation |
| `atelier-ui.rtl.css` | Generated RTL counterpart |
| `icons/` | Local FreshRSS assets and 44 adapted Lucide SVGs |
| `thumbs/original.png` | Theme preview used by FreshRSS and this README |
| `scripts/` | Dependency-free validation and RTL generation |

## Development

Do not edit `_fonts.rtl.css`, `_variables.rtl.css`, or `atelier-ui.rtl.css`
manually. Generate these direction-neutral counterparts from their canonical
sources:

```console
python3 scripts/generate_rtl.py
```

Verify that the generated files are current:

```console
python3 scripts/generate_rtl.py --check
```

Run all dependency-free release checks:

```console
python3 scripts/check_theme.py
python3 scripts/generate_rtl.py --check
```

The checks validate formatting, CSS brace balance, the FreshRSS manifest,
custom-property usage, Lucide license headers, and the documented CSS
safeguards. The same checks run in CI for pushes and pull requests.

## Design implementation notes

- The header intentionally does not use `backdrop-filter`. Applying it creates
  a containing block and breaks the absolutely positioned configuration
  dropdown. Dropdowns themselves can safely use the effect.
- The desktop layout uses CSS Grid so the sidebar forms a real stretching
  column and leaves no background strip while collapsing. A painted gradient
  on `body` is avoided because inherited FreshRSS backgrounds would redraw it
  relative to their own boxes.
- The sidebar overrides the base theme's `display: none` behavior with width
  and opacity transitions. Its feed tree retains a fixed width during the
  animation to prevent content wrapping.
- The absolutely positioned date column is 195 px wide and receives spacing
  on the date element itself. The base width of 155 px is too narrow for long
  German date strings.
- `#bigMarkAsRead` uses a `2rem` bottom margin instead of the base theme's
  `100vh`, and `#global` is not stretched artificially to the viewport height.
- Dropdown links require `width: auto !important` because the FreshRSS base
  style otherwise forces `width: 100%` and clips the right-hand rounding.

These safeguards are also documented next to the relevant rules in
`atelier-ui.css` and should remain intact during refactoring.

## License and credits

Atelier is derived from the official
[Mapco theme](https://github.com/FreshRSS/FreshRSS/tree/1.29.1/p/themes/Mapco)
by Thomas Guesnon and the FreshRSS project. The theme is distributed under the
[GNU Affero General Public License version 3](LICENSE).

The 44 Lucide UI icons retain their `lucide-static` 1.31.0 ISC headers. The
complete Lucide and Feather license notices are available in
[`icons/LICENSE`](icons/LICENSE). The remaining logo assets are derived from
FreshRSS and Mapco. See [`THIRD-PARTY.md`](THIRD-PARTY.md) for detailed
attribution.

Credits:

- Thomas Guesnon and the FreshRSS project for Mapco and the theme foundation
- Lucide Contributors for the Lucide icon set
- Cole Bemis and Feather Contributors for icons inherited through Lucide
- shadcn/ui and Tailwind CSS as design and color references
