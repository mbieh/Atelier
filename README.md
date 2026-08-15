# Atelier

A calm light and dark theme for [FreshRSS](https://freshrss.org/), inspired by
shadcn/ui.

![Atelier preview: sidebar beside a card of article rows](thumbs/original.png)

Atelier gives FreshRSS a cool neutral palette, a clear reading hierarchy, soft
radii, and subtle motion. It follows your operating system's light or dark
setting on its own, and everything it needs ships with the theme — no web
fonts, no scripts, nothing loaded from an external service while you read.

## Features

- Light and dark interfaces that follow your system preference automatically
- Layouts for desktop and mobile, including a collapsible sidebar
- Locally bundled Lucide icons, so nothing is fetched from a CDN
- Visible focus states and support for reduced-motion settings
- Right-to-left layout support

## Requirements

**FreshRSS 1.29.1.** That is the version Atelier is built and tested against.
Other versions will most likely work, but the theme follows FreshRSS's markup
closely, so a larger FreshRSS update may need a matching theme update.

**A browser from 2024 or later.** Atelier uses modern CSS — nesting, `:has()`,
subgrid, `color-mix()` and `:dir()` — which in practice means Chrome or Edge
120+, Firefox 121+, or Safari 17.2+. Older browsers will render the page, but
parts of the layout will look wrong.

## Installation

Atelier installs like any other FreshRSS theme: put the folder into
`p/themes/` inside your FreshRSS installation and pick it in the settings.
The repository root *is* the theme, so there is nothing to build first.

### Download as a ZIP

1. Download the repository as a ZIP archive and unpack it.
2. **Rename the unpacked folder to `Atelier`.** Archives usually unpack to a
   name like `Atelier-main`. FreshRSS stores the folder name as the theme's
   identity, so renaming it later resets your theme selection.
3. Move the folder to `<FreshRSS>/p/themes/Atelier`.

### Clone with Git

```console
cd /path/to/FreshRSS/p/themes
git clone https://github.com/mbieh/Atelier.git Atelier
```

### Docker Compose

Mount your checkout into the container. Read-only (`:ro`) keeps the container
from writing to it:

```yaml
services:
  freshrss:
    volumes:
      - /absolute/path/to/Atelier:/var/www/FreshRSS/p/themes/Atelier:ro
```

Restart the container afterwards.

### Activate it

Open FreshRSS and choose **Configuration → Display → Theme → Atelier**.

### Updating

Pull the latest version, or download and unpack it over the existing folder:

```console
cd /path/to/FreshRSS/p/themes/Atelier
git pull
```

Then reload FreshRSS. If the page still looks unchanged, force-reload it with
`Ctrl`/`Cmd` + `Shift` + `R`.

### Removing

Switch to another theme under **Configuration → Display**, then delete
`<FreshRSS>/p/themes/Atelier`.

## Light and dark mode

Atelier follows your operating system's appearance setting. Switch your system
to dark mode and FreshRSS turns dark on the next page load. There is no
separate switch inside FreshRSS, and no preference is stored.

## Changing the colors

All colors live in one place: [`_variables.css`](_variables.css). The values
are grouped by role — background, foreground, borders, accents, sidebar — so
you can swap the palette without touching any component rules.

After editing a stylesheet, regenerate the right-to-left copies that FreshRSS
loads for RTL languages:

```console
python3 scripts/generate_rtl.py
```

## Troubleshooting

**Atelier does not show up in the theme list.** Check that
`<FreshRSS>/p/themes/Atelier/metadata.json` exists, and that your web server
user is allowed to read the folder.

**The page looks unstyled or the layout is broken.** Usually an outdated
browser — see [Requirements](#requirements). Otherwise force-reload the page.

**Dark mode does not turn on.** Atelier follows the system setting, not a
FreshRSS setting. Check your operating system's appearance preference.

**Some pages still look like the previous theme.** Force-reload the page;
browsers hold on to stylesheets aggressively.

## Development

`python3 scripts/check_theme.py` runs the same checks as CI: CSS structure,
metadata, links, icon licenses, and a guard that rejects direction-sensitive
CSS before it can reach a right-to-left copy.

See [`CHANGELOG.md`](CHANGELOG.md) for release notes and
[`docs/component-coverage.md`](docs/component-coverage.md) for the component
matrix.

## License and credits

Atelier is derived from the official
[Mapco theme](https://github.com/FreshRSS/FreshRSS/tree/1.29.1/p/themes/Mapco)
by Thomas Guesnon and the FreshRSS project, and is distributed under the
[GNU Affero General Public License v3](LICENSE).

The bundled Lucide icons keep their `lucide-static` 1.31.0 ISC headers; the
full Lucide and Feather notices are in [`icons/LICENSE`](icons/LICENSE). See
[`THIRD-PARTY.md`](THIRD-PARTY.md) for detailed attribution.

Thanks to Thomas Guesnon and the FreshRSS project for Mapco, to the Lucide
contributors and to Cole Bemis and the Feather contributors for the icons, and
to shadcn/ui and Tailwind CSS as design and color references.
