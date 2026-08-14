# Atelier

Atelier ist ein modernes, helles Theme für [FreshRSS](https://freshrss.org/).
Es verbindet die Struktur des offiziellen Mapco-Themes mit einer eigenständigen
Override-Schicht im Stil von shadcn/ui und der kühlen Tailwind-Farbpalette Mist.
Das Theme lädt keine Webfonts, Skripte oder sonstigen Laufzeitabhängigkeiten aus
dem Netz.

![Vorschau des Atelier-Themes](thumbs/original.png)

## Kompatibilität

Atelier 1.0 wurde mit FreshRSS 1.29.1 und Chromium getestet. Geprüft wurden die
kurze und lange Listenansicht, ein geöffneter Artikel, das
Konfigurations-Dropdown, der Suchfokus, das Ein- und Ausklappen der Sidebar,
Konfigurationsseiten und ein mobiler Viewport.

Noch nicht ausdrücklich visuell geprüft sind:

- Global- und Reader-Ansicht mit dem Grid-Layout,
- View Transitions in Firefox,
- der Fortschrittsbalken `#actualizeProgress`,
- die RTL-Darstellung in einer RTL-Sprache und
- andere FreshRSS-Versionen als 1.29.1.

## Installation

### Manuell

1. Das Repository als Ordner `Atelier` herunterladen oder klonen.
2. Den vollständigen Ordner nach `FreshRSS/p/themes/Atelier` kopieren.
3. In FreshRSS unter **Konfiguration → Anzeige → Theme** „Atelier“ auswählen.

Der Repository-Inhalt liegt bewusst direkt in der Theme-Wurzel. Dadurch kann
der Checkout ohne Kopier- oder Build-Schritt als FreshRSS-Theme verwendet
werden.

### Docker-Bind-Mount

Den absoluten Host-Pfad an die eigene Installation anpassen:

```yaml
services:
  freshrss:
    volumes:
      - /absoluter/pfad/zu/Atelier:/var/www/FreshRSS/p/themes/Atelier:ro
```

Anschließend das Theme in FreshRSS auswählen. Der Read-only-Mount verhindert,
dass ein Container-Update den Checkout verändert.

## Anpassung

Die Farben werden zentral in [`_variables.css`](_variables.css) definiert. Die
kommentierten Mist-Werte können dort beispielsweise gegen eine andere neutrale
Palette ausgetauscht werden. Die zugehörige `_variables.rtl.css` muss dabei
denselben Variablenstand behalten.

Die Theme-Schichten werden in dieser Reihenfolge geladen:

1. `_frss.css` als FreshRSS-Basis,
2. `atelier.css` als von Mapco abgeleitete Struktur und
3. `atelier-ui.css` als Atelier-Override.

`atelier-ui.rtl.css` ist generiert und soll nicht von Hand bearbeitet werden:

```console
python3 scripts/generate_rtl.py
python3 scripts/generate_rtl.py --check
```

Alle lokalen Release-Prüfungen laufen ohne zusätzliche Pakete:

```console
python3 scripts/check_theme.py
python3 scripts/generate_rtl.py --check
```

## Design notes

- Der Header verwendet absichtlich keinen `backdrop-filter`: Der Filter erzeugt
  einen neuen Containing Block und beschädigt das absolut positionierte
  Konfigurations-Dropdown. Dropdowns selbst können den Effekt gefahrlos nutzen.
- Das Desktop-Layout ist ein CSS-Grid. So ist die Sidebar eine echte,
  gestreckte Spalte und hinterlässt beim animierten Einklappen keinen Streifen.
  Ein Verlauf auf `body` wird vermieden, weil geerbte FreshRSS-Hintergründe ihn
  relativ zu ihren eigenen Boxen erneut zeichnen würden.
- Die Sidebar überschreibt das `display: none` der Basis mit einer
  Breiten-/Opacity-Transition. Der Feed-Baum behält währenddessen seine Breite,
  damit sein Inhalt nicht umbricht.
- Die absolut positionierte Datumsspalte ist 195 px breit und erhält ihren
  Abstand direkt im Datumselement; 155 px reichen für längere deutsche
  Datumsangaben nicht.
- `#bigMarkAsRead` erhält nur `2rem` unteren Abstand statt `100vh`, und `#global`
  wird nicht künstlich auf Viewporthöhe gestreckt.
- Links in Dropdown-Menüs benötigen `width: auto !important`, da die
  FreshRSS-Basis sonst `width: 100%` erzwingt und die rechte Rundung abschneidet.

Diese Schutzkommentare stehen zusätzlich direkt in `atelier-ui.css` und dürfen
beim Aufräumen nicht entfernt werden.

## Herkunft und Lizenz

Atelier ist ein Fork des offiziellen
[Mapco-Themes](https://github.com/FreshRSS/FreshRSS/tree/1.29.1/p/themes/Mapco)
von Thomas Guesnon aus dem FreshRSS-Projekt. Das Haupt-Theme steht deshalb unter
der [GNU Affero General Public License Version 3](LICENSE).

44 UI-SVGs stammen aus `lucide-static` 1.31.0 und behalten ihren jeweiligen
ISC-Lizenzheader. Für Lucide und die daraus übernommenen Feather-Icons gelten
die Texte in [`icons/LICENSE`](icons/LICENSE). Die übrigen Logo-Assets stammen
aus der FreshRSS-/Mapco-Basis. Vollständige Zuordnungen stehen in
[`THIRD-PARTY.md`](THIRD-PARTY.md).

## Credits

- Thomas Guesnon und das FreshRSS-Projekt für Mapco und die Theme-Basis
- Lucide Contributors für das Lucide-Iconset
- Cole Bemis und die Feather Contributors für in Lucide enthaltene
  Feather-Ursprungsicons
- shadcn/ui und Tailwind CSS als Design- und Farbreferenz
