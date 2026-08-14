# Third-party notices

## FreshRSS / Mapco

Atelier is based on the official Mapco theme by Thomas Guesnon, distributed as
part of the FreshRSS project.

- Source: <https://github.com/FreshRSS/FreshRSS/tree/1.29.1/p/themes/Mapco>
- Verified upstream tag: `1.29.1`
- Tag commit: `b2c50115baa36c217e939ee3ea8ecfae52f91abd`
- License: GNU Affero General Public License version 3 (`AGPL-3.0`)
- License text: [`LICENSE`](LICENSE)

The Mapco structural modules remain the foundation. A comparison against the
tag above shows the following intentional differences outside Atelier's
override layer:

- `_components.css` and `_components.rtl.css` cover nested `.as-link` elements
  and add `.alert-info`.
- `_forms.css` and `_forms.rtl.css` use `:user-invalid` instead of `:invalid`
  so fields are not presented as invalid before user interaction.
- `_fonts.css` and `_fonts.rtl.css` do not load Mapco web fonts.
- `_logs.css` and `_logs.rtl.css` use a valid semantic error background instead
  of passing a hexadecimal custom property to `rgba()`.
- `_variables.css` and `_variables.rtl.css` contain Atelier's color palette.
- `atelier.css` and `atelier.rtl.css` are the renamed Mapco entry points.

These differences remain identical between each LTR and RTL pair. The visual
redesign itself lives in `atelier-ui.css` and `atelier-ui.rtl.css`.

## Lucide

The 46 SVG files under `icons/` are adapted copies from `lucide-static` 1.31.0.
Each file retains the `@license lucide-static v1.31.0 - ISC` header.

- Source: <https://github.com/lucide-icons/lucide>
- Copyright holders: Lucide Icons and Contributors
- License: ISC; some included icons originate from Feather and remain under
  the MIT License
- Complete notices: [`icons/LICENSE`](icons/LICENSE)

`icons/FreshRSS-logo.svg` and `icons/icon.svg` are not Lucide icons. They are
adapted FreshRSS/Mapco assets covered by the main AGPL-3.0 license.

## Design references

The visual system draws on shadcn/ui theming and Tailwind CSS colors. No code,
fonts, scripts, or runtime dependencies from either project are bundled or
loaded over the network.

- shadcn/ui theming: <https://ui.shadcn.com/docs/theming>
- Tailwind CSS colors: <https://tailwindcss.com/docs/colors>
