# Hinweise zu Drittkomponenten

## FreshRSS / Mapco

Atelier basiert auf dem offiziellen Mapco-Theme von Thomas Guesnon, das als
Teil des FreshRSS-Projekts veröffentlicht wird.

- Quelle: <https://github.com/FreshRSS/FreshRSS/tree/1.29.1/p/themes/Mapco>
- Verifizierter Upstream-Tag: `1.29.1`
- Commit des Tags: `b2c50115baa36c217e939ee3ea8ecfae52f91abd`
- Lizenz: GNU Affero General Public License, Version 3 (`AGPL-3.0`)
- Lizenztext: [`LICENSE`](LICENSE)

Die Mapco-Strukturmodule bilden weiterhin die Basis. Der Abgleich gegen den
genannten Tag weist folgende bewusste Abweichungen außerhalb der
Atelier-Override-Schicht aus:

- `_components.css` und `_components.rtl.css` erfassen verschachtelte
  `.as-link`-Elemente und ergänzen `.alert-info`.
- `_forms.css` und `_forms.rtl.css` verwenden `:user-invalid` statt `:invalid`,
  damit Felder nicht vor einer Nutzerinteraktion als fehlerhaft erscheinen.
- `_fonts.css` und `_fonts.rtl.css` laden keine Mapco-Webfonts.
- `_variables.css` und `_variables.rtl.css` enthalten die Atelier-Farbpalette.
- `atelier.css` und `atelier.rtl.css` sind die entsprechend umbenannten
  Mapco-Einstiegsdateien.

Diese Abweichungen bleiben paarweise in LTR und RTL identisch. Die eigentliche
visuelle Umgestaltung liegt in `atelier-ui.css` und `atelier-ui.rtl.css`.

## Lucide

44 SVG-Dateien unter `icons/` sind angepasste Kopien aus `lucide-static`
1.31.0. Jede dieser Dateien behält den Header
`@license lucide-static v1.31.0 - ISC`.

- Quelle: <https://github.com/lucide-icons/lucide>
- Urheber: Lucide Icons and Contributors
- Lizenz: ISC; einige aufgeführte Icons stammen aus Feather und bleiben unter
  der MIT-Lizenz
- Vollständige Hinweise: [`icons/LICENSE`](icons/LICENSE)

`icons/FreshRSS-logo.svg` und `icons/icon.svg` sind keine Lucide-Icons. Sie sind
angepasste FreshRSS-/Mapco-Assets und fallen unter die AGPL-3.0-Hauptlizenz.

## Designreferenzen

Das visuelle System orientiert sich an shadcn/ui-Theming und den Farben von
Tailwind CSS. Von beiden Projekten werden weder Code noch Fonts, Skripte oder
Laufzeitabhängigkeiten gebündelt oder aus dem Netz geladen.

- shadcn/ui-Theming: <https://ui.shadcn.com/docs/theming>
- Tailwind-CSS-Farben: <https://tailwindcss.com/docs/colors>
