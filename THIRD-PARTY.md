# Third-party notices

## FreshRSS / Mapco

Atelier is based on the official Mapco theme by Thomas Guesnon, distributed as part of the FreshRSS project.

- Source: <https://github.com/FreshRSS/FreshRSS/tree/1.29.1/p/themes/Mapco>
- Verified upstream tag: `1.29.1`
- Tag commit: `b2c50115baa36c217e939ee3ea8ecfae52f91abd`
- License: GNU Affero General Public License version 3 (`AGPL-3.0`)
- License text: [`LICENSE`](LICENSE)

The Mapco structural modules remain the foundation. A comparison against the tag above shows the following intentional differences outside Atelier's override layer:

- `_components.css` covers nested `.as-link` elements and adds `.alert-info`.
- `_forms.css` uses `:user-invalid` instead of `:invalid` so fields are not presented as invalid before user interaction, and drops Mapco's `lato` font stack together with the empty `.form-group::after` clearfix.
- `_fonts.css` does not load Mapco web fonts.
- `_logs.css` uses a valid semantic error background instead of passing a hexadecimal custom property to `rgba()`.
- `_sidebar.css` routes the sidebar scrollbar through the palette instead of Mapco's literal fallback pair.
- `_variables.css` maps shadcn/ui semantic roles onto the neutral ramp in `_palette.css`, which holds Tailwind 4.3 "Mist" and is the only file a color scheme changes.
- `atelier.css` is the renamed Mapco entry point.

Every module above is direction-neutral, so `atelier.rtl.css` and `atelier-ui.rtl.css` are verbatim copies of their sources rather than hand-mirrored variants. The visual redesign itself lives in `atelier-ui.css`.

## Lucide

The 57 SVG files under `icons/` are adapted copies from `lucide-static` 1.31.0. Each file retains the `@license lucide-static v1.31.0 - ISC` header.

- Source: <https://github.com/lucide-icons/lucide>
- Copyright holders: Lucide Icons and Contributors
- License: ISC; some included icons originate from Feather and remain under the MIT License
- Complete notices: [`icons/LICENSE`](icons/LICENSE)

`icons/FreshRSS-logo.svg` and `icons/icon.svg` are not Lucide icons. They are adapted FreshRSS/Mapco assets covered by the main AGPL-3.0 license.

## Design references

The visual system draws on shadcn/ui theming and Tailwind CSS colors. No code, fonts, scripts, or runtime dependencies from either project are bundled or loaded over the network.

- shadcn/ui theming: <https://ui.shadcn.com/docs/theming>
- Tailwind CSS colors: <https://tailwindcss.com/docs/colors>
