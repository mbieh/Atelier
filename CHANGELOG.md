# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

## 1.4.0 - 2026-08-18

### Changed

- The Neutral palette ships as Atelier itself. Its folder is `Atelier` rather than `Atelier-Neutral`, and the theme picker lists it as **Atelier**, with the palette named in the description underneath — it is the theme, and the other eight are the palettes it also comes in. Nothing about the design changed: the folder holds the same ramp, grey without a hue, and the same rules as before. **Anyone using Atelier-Neutral has to pick the theme again after updating.** FreshRSS stores the folder name as the identity of a selection, so a renamed folder reads as a theme that is no longer installed and the account falls back to the default. Copy the new `Atelier` folder into `p/themes/`, select it once, and remove the old folder.
- The folder a scheme is built into is stated in `palettes/ramps.json` instead of derived from its title, and both scripts read it through one function. A folder name is what FreshRSS remembers about a user's choice, so it is a fact the repository states once rather than a string two scripts each rebuild from the palette's name.
- The assets in `src/` are authored in Neutral, the palette Atelier ships as itself, rather than in Mist. The build re-renders every icon into the ramp of the folder it writes, so this is invisible in all nine — but the folder most people install is now the one whose icons are carried over verbatim, with no conversion between an authored color and a shipped one.

### Fixed

- An alert fills the width it is given. The base theme sizes every alert at `width: 90%` with automatic side margins, so each one sat a tenth narrower than whatever held it, and the gap grew with the window. Where Atelier had replaced those margins with a fixed inset, the whole leftover tenth collected on one side — visibly lopsided in a wide stream card. Alerts size to their container now, which also settles a subtler case: a loose alert inside a settings row is a grid item spanning both columns, and an automatic margin suppresses the stretch such an item would otherwise get, so an alert that asked for no particular width would have shrunk to the length of its own sentence.
- An empty stream reads as a state rather than a warning. FreshRSS renders "There are no articles to show" with the same alert component it uses for problems, which made an unread list that is simply empty — or a favourites list nobody has filled yet — the loudest surface on the page. Inside the stream that box now drops the alert's tint, border and shadow and becomes an empty state: an inbox icon, one line of text in the page's own voice, and the room around them. It stays an alert everywhere else, because everywhere else it is one.

## 1.3.2 - 2026-08-17

### Fixed

- The preview card holds its own edge. A screenshot of an interface brings its own pale margins, so a light preview dissolved into a white card, which in turn sat on a page barely darker than itself. The picture fills the card to the edge now — leaving no card around the margins is what keeps them from dissolving — and the card is bounded by `--input` rather than `--border`, the same tone a field's boundary uses and for the same reason: it has to hold against the surfaces on both sides. That edge reads at 3.18:1 against the page at worst across the nine palettes, where the old one reached 1.11:1. The card lifts on the shadow every other card in the theme uses, and the caption sits on one even inset.
- The caption under the preview is a solid plate in the palette's dark tone rather than a pale strip: `--primary`, the darkest solid the theme fills with, carrying the light foreground that belongs to it. It is a role and not a step, so in the dark scheme, where `--primary` inverts to a light neutral, the plate becomes the page's own surface — a step below the card, with a hairline, because that step alone is a quiet boundary. The description sits one dimming below the title on that plate, 6.74:1 at worst across the nine palettes, and the gate carries the pairing.
- The preview in the theme picker is no longer distorted. FreshRSS pins that box to 640 by 320 and stretches each image across it, so any preview that is not exactly 2:1 is squeezed — Atelier's are 701 by 427. The image keeps its own proportions now and the card takes the height it asks for, which also means the description sits under the picture instead of covering its lower third.
- The Display page fetches one preview instead of nine. FreshRSS renders an entry per installed theme, stacked in that one box, and marks the saved one `.picked`; no script in 1.29.1 ever moves that class, so the other eight were downloaded and painted to be invisible — with hand-drawn previews that is over a megabyte for a picture nobody sees. Only the picked entry renders. Should a later FreshRSS switch previews on selection, it toggles the same class and this follows, as a swap rather than a cross-fade.
- A theme that is no longer on disk says so. FreshRSS renders its alert into the same caption, whose tone would have swallowed it; it keeps the alert pairing instead — a folder renamed or removed is a live possibility with nine of them.

### Changed

- The preview in the theme picker belongs to the palette, not to the build. Each folder's `thumbs/original.png` is drawn by hand now, and the build neither writes nor prunes it — it had been generated by re-tinting one canonical screenshot along the ramp, which approximates what a palette looks like rather than showing it, and that is the one question a preview exists to answer. `check_theme.py` still insists every folder has one. With it went the PNG decoder and encoder the re-tinting needed, and with those the question of whether two zlib versions pack a preview identically.

## 1.3.1 - 2026-08-17

### Changed

- The side panel slides in instead of shooting in. FreshRSS animates it by growing it from zero to 750px in 100ms on an ease-in curve — the same 100ms its mobile sidebar uses for a drawer that covers a fraction of the distance — so a panel seven times as wide crossed the screen at the same speed and accelerated into its stop. Two things changed. It keeps its width from the start and arrives by transform, which means the form inside is laid out once instead of being re-wrapped on every frame of the way in. And it enters over 0.32s on a decelerating curve and leaves over 0.24s on an accelerating one, since a surface that size should settle into place and then get out of the way briskly. The page behind it darkens with it rather than in one step: the base layer paints that scrim at `#0007` in the same frame it moves it under the panel, which lands as a jolt and is a harder value than anything else in the theme dims with, so it carries the tint and blur of the mobile overlay and fades over the panel's own duration — on the way out the fade runs first and the scrim steps aside only once it is invisible. The closed panel rests a little further out than its own width, far enough that its shadow clears the edge instead of resting against it. Reduced motion still removes all of it.

### Fixed

- A feed that failed to refresh reads on its own row. FreshRSS writes that feed's name in the error color on a tint mixed from the same color, and the pair had never been checked against each other: it fell to 4.63:1 on Slate and 4.36:1 on Olive's dark row, below the 4.5:1 of WCAG 1.4.3. The tint carries less of the accent now — 5% in light, 12% in dark — and the pair clears 4.84:1 and 4.82:1 at worst. The alert surfaces that share the tint keep more than 8:1 either way.
- Every theme folder describes the palette it actually ships. The override layer's file header still read `Tailwind 4.3 "Mist"` from before the split, so eight of the nine folders introduced themselves as Mist.
- The theme picker shows a real em dash in each description instead of two hyphens. The `--` convention belongs in source comments, not in a sentence FreshRSS renders to a reader.
- A segment inside a toolbar group keeps its label too. The same trap sat one rule deeper: segments were held to a fixed 40px, and extensions put their own controls into these groups, so a segment pairing an icon with a label would have been clipped exactly like the error filter was. The comment above the rule had described the minimum it was supposed to use since 1.2.3, while the rule set a fixed width. An icon-only segment measures the same 40px as before.
- The error filter above the subscription list keeps its label. "Show only feeds in error" was cut to a 40px square showing the three letters that happened to fall in the middle. It is the bug 1.2.3 fixed for the statistics toolbar, one rule further up: `:only-child` counts elements and not text, so a button pairing an icon with a label matches the icon-only selector, and that selector set a fixed width. The square is a minimum now wherever a button carries an icon, not only inside the toolbar — an icon-only button still measures exactly 40px, since a 1rem icon between two 0.5rem flanks stays under the floor. The toolbar's own rule for that case was the same geometry stated twice and is gone.

### Development

- The contrast gate covers the surfaces that were only assumed to be fine. It ran 33 pairings; it runs 42, or 756 checks across the nine palettes and both schemes. The new ones are the pairs that exist in the interface but had never been stated: text on the tint a row takes under the pointer, the sidebar's active entry, and each feedback state's text on the stronger of its two tints — including the error row that this release fixes. Three further pairings were measured and deliberately left out, because the surfaces they would guard do not meet: `--secondary` carries only the sidebar's segmented button and a badge, so no star and no field boundary ever lands on it.
- An `@import` is recognised in both spellings CSS allows. The scripts read only `@import "…"`, so `@import url(…)` was copied by no one and reported by no one — the same silent 404 the release had just closed, reachable by writing a valid import a different way. Both scripts share one reader now, which requires quotes or `url()` and refuses a bare word, since matching one would find the `@import` in a sentence about imports — as it did, briefly, while this was being written. The check inside a folder walks every stylesheet rather than the three FreshRSS names, so a partial that imports a partial is followed too.
- The list of partials a theme folder ships is read from `atelier.css` instead of restated in the build. It had been a second copy, and a copy that nobody would have noticed going stale: a partial added to `atelier.css` was imported by every shipped theme and copied into none of them, and both scripts stayed green while the folders 404ed. As a second line, each folder's `@import` chain is now resolved inside the folder it ships in, which is the file FreshRSS actually loads.
- A value the theme does not own has to say what it is worth without FreshRSS. `--frss-padding-top-bottom` and `--frss-padding-flux-items` are defined in FreshRSS's own `frss.css`, which this repository does not contain, and eight of their uses sit inside `calc()` — where an undefined property does not fall back to nothing but invalidates the whole expression, dropping the declaration and the layout it carried. They carry the upstream values now, 0.5rem and 0.75rem, the way `--width-aside` already carried 300px, and a check holds every reference to a foreign property to that. It counts references and not names, because one call site losing its fallback is the entire failure and a sibling that still has one says nothing about it.
- A preview is compared by what it shows, not by how it was packed. `--check` held the generated PNGs to byte equality, and deflate output is not identical across zlib versions — the folders are built on one machine and verified by CI on another, so the first mismatch would have been reported as a stale preview with nothing stale about it.
- A comment holding one line is checked now, not just intended. The convention 1.2.3 established was one nobody could see being broken, and the palette header generated in 1.3.0 promptly came back hand-wrapped across nineteen lines. `check_theme.py` rejects a `/* */` comment that spans lines in any stylesheet, a run of consecutive `#` lines in any script, and a docstring that spans lines — a docstring is a string to the parser and a comment to the reader, and the reader is who the rule is for, so the fourteen that were still wrapped hold a line each now. The one exception is a banner at the very start of a file — it introduces the whole sheet and is a structure rather than a wrapped sentence, which is what the twenty-section table of contents at the top of the override layer is. The generated palettes are held to it too, since no source file stands in for them.
- Explanations do not stack either. Unwrapping the palette header left three of them under each other, which is the same wall of text with the wrapping moved, so a second check rejects consecutive comment lines that carry an explanation rather than a label. Length is what tells the two apart: a section banner and its rule of equals signs are short and stack legitimately, an explanation runs past 80 columns. The header is one comment now, and the paragraph on how roles pick their step is gone from it — `_variables.css` states that at the declaration it applies to, which is where it belonged.

## 1.3.0 - 2026-08-17

### Added

- Atelier ships in nine neutral palettes — slate, gray, zinc, neutral, stone, taupe, mauve, mist and olive, the full set of Tailwind 4.3 neutrals. Each is its own folder, `Atelier-Slate` through `Atelier-Olive`, and each is a complete theme: FreshRSS has no notion of a variant inside a theme, so a palette can only be a folder of its own. They are identical apart from the ramp, which means installing several and switching between them in the settings costs nothing but disk.
- Every palette is held to the same contrast bars as the one that came before it. The 33 role pairings the theme guarantees now run against all nine ramps in both schemes — 594 checks — which is what turned three roles from "correct" into "correct on a cool grey": see the note on `--input`, `--at-quiet-foreground` and the dark error red under Fixed.

### Changed

- **Installing means copying a folder, not the repository.** The repository root is no longer a theme; it holds the nine, plus the shared source they are built from. Copy the `Atelier-*` folders you want into `p/themes/` and pick one in the settings.
- The quiet surface of every feedback state follows the folder's neutral. The tints and borders behind an error, a warning, a success or a favorited article were picked by hand against a cool grey, which reads as a foreign body on a warm one; they are mixed from their accent and the ramp now, so they take the hue of whichever neutral the folder ships. The accent hues themselves stay literal — an error is the same red in all nine, because that is what carries the meaning.
- The rows of an extension column join into one list. Each extension was its own card, so a column of twenty read as twenty separate objects; the rows share their hairline now, and only the top and bottom of a column are rounded. Columns keep their gap, so they stay legible as columns. Which tiles carry the rounding follows from the column count — the first n children open the columns, the last n close them — which holds for any number of extensions, including an incomplete last row.

### Fixed

- A field boundary stays visible in every palette. `--input` mixed step 500 into step 400 at 60%, which clears the 3:1 of WCAG 1.4.11 on a cool grey and lands at 2.99:1 on Olive, whose step 500 is the lightest of the nine. It mixes at 70% now, worst case 3.18:1.
- The quiet label tone clears WCAG AA in every palette. It fades `--muted-foreground` toward the surface, and at 90% four of the nine dropped below 4.5:1 on their accent surface — 4.35:1 at worst. It fades at 94% now, worst case 4.62:1.
- Error text stays readable on a dark card. `--destructive` is painted on step 800, and against Olive's — the lightest of the nine — the dark red read at 4.48:1. It is a shade lighter now, and clears 4.81:1 at worst.

### Development

- The shared stylesheets live in `src/`, and the nine theme folders are generated from them by `scripts/build_themes.py`. They are committed rather than built on install, because a FreshRSS theme is installed by copying a folder, not by running a build — so the repository holds the artifact people actually use. `--check` rebuilds into memory and compares, which is what CI runs; editing a theme folder by hand is caught there and overwritten by the next build.
- A palette is data now. `palettes/ramps.json` holds the nine ramps as the OKLCH triples Tailwind publishes, and the build converts them to sRGB hex — the space WCAG contrast is defined in — writing the source beside each step so the conversion stays auditable. The conversion is verified against the eleven Mist values 1.2.3 shipped by hand: it reproduces all eleven exactly.
- The icons and the theme picker's preview are re-rendered per palette. Neither can hold a token — an external SVG cannot inherit the page's `currentColor`, and a PNG has no tokens at all — so both are authored in Mist and translated step by step into each folder's ramp, the star's gold and the preview's white excepted. The build refuses any asset color that is neither a step of the canonical ramp nor one of those fixed colors, rather than guessing what it should become.
- `scripts/generate_rtl.py` is gone. It existed to copy two direction-neutral sheets to their `.rtl.css` names; the build writes those mirrors into each folder, and the direction guard that made the copy safe was always `check_theme.py`'s. CI runs `build_themes.py --check` in its place.
- The override layer is navigable again. Its section 9 had grown to 178 rules and a third of the file, holding everything the first eight sections did not cover; it is nine sections now — segmented groups, disclosures, sign-in, settings forms, cards and tables, manage lists, panels, statistics, article typography — and the table of contents lists all twenty.
- Comments hold one line each, in every CSS, Python and Markdown file. They had been wrapped by hand at anything between 60 and 81 columns, which reads as arbitrary breaks on top of whatever the editor wraps itself. Four pairs of comment blocks that had drifted apart from their rule were merged back, and three labels the new section headings already carry were dropped.
- `check_theme.py` recognises whole comment blocks when it looks for an `rtl-safe:` marker. It used to decide line by line — "starts with `/*` or ends with `*/`" — and stopped one line short of a marker whenever a comment wrapped, which is how re-wrapping a comment could fail the direction check for a rule that had not changed.

## 1.2.3 - 2026-08-16

### Added

- `--at-quiet-foreground`, one step greyer than `--muted-foreground`, for a label whose state is carried by a control next to it. It is mixed 90% toward the surface, which is where the ramp stops: 4.75:1 on a card and 4.71:1 on that card's hover surface, with the next step down falling below the 4.5:1 of WCAG 1.4.3 in both schemes. The contrast guard covers it on both surfaces.

### Fixed

- Pointing at a switch no longer fades a glyph in behind its knob. FreshRSS paints the state as a background image on the track and resets it inside an `@supports selector(.switch::before)` block — but only for the resting states, so both hover states kept theirs. Here the knob carries the state, in every state.
- A toolbar button keeps its label. `:only-child` counts elements and not text, so a button pairing an icon with a label — "Manage" on the statistics filter bar — matched the icon-only rule and was cut to a 40px square with its label clipped. Segments inside a group keep the exact square; a standalone button treats it as a minimum.
- The statistics filter bar starts on the page's text axis instead of floating centred above the title. It says which feed the numbers are about, so it belongs with them.
- The zoom toggle of a statistics card sits in its title row as a square button. The base layer pins it to the card's right edge with `position: absolute`, at the 17px width of its own "+" glyph, where it landed on the scrollbar of the content below.
- Charts are no longer wrapped in scrollbars. The base layer caps every card's content at 260 or 520px and scrolls the overflow, which is right for a list of feeds and wrong for a canvas; the chart cards size to their chart.
- Every page starts on the same rhythm. FreshRSS opens these views differently — Manage users with a section heading, Reading with a form, About with text — and each brought its own margin, so the same page title sat 7px, 14px or 17.5px above its content. One gap of 1.5rem below the title, whatever follows it, including the Shortcuts page, where a `<datalist>` of key names sits between the two and defeats a rule that goes by adjacency alone.
- About and Terms sit on the page inset like every other view, and in the interface size. They carry `class="post content"`, and `.content` is the article body elsewhere in FreshRSS, so they inherited its 10px inset and its 1.125rem reading size — 18px closer to the sidebar than the settings pages under the same sidebar, in a different voice.
- Section headings in forms are headings again. Rewriting the collapsible headers in 1.2.2 left `legend` attached to their selector, so every `<legend>` — the sections of Reading, Advanced Search, Sharing, Shortcuts and the feed, category and query forms — turned into a tinted bar spanning the form.
- A `<legend>` and an `<h2>` now read the same. FreshRSS uses both for the same thing, and several pages carry both: the feed configuration has seven legends beside two headings. They share one size, weight and rhythm, instead of a small uppercase idiom from the base layer on one side and a section heading on the other.
- An inactive switch stays identifiable while its row is hovered. The track is `--input`, and on `--accent` it read at 2.83:1 in the light scheme, below the 3:1 WCAG 1.4.11 asks of a control. Those rows hover on the softer row tint now, where it holds 3.20:1, and the contrast guard covers that pairing so it cannot slip again.

### Changed

- The extension list reads as a settings list and follows the width it is given. FreshRSS emits each row as switch, gear, name, which left the names behind a ragged column of controls. Each extension is its own surface now, the name on the reading edge and the controls collected on the trailing one, so the switches line up in a column of their own. The list takes two columns from 40rem and three from 64rem of container width, measured on the settings container rather than the viewport. Every list on the page shares that grid, so a section holding a single extension shows a tile the same width as the others rather than one stretched across the row. An enabled extension carries its name in semibold, a disabled one in `--at-quiet-foreground` at regular weight rather than in italics, since the switch beside it already carries that state.

## 1.2.2 - 2026-08-16

### Fixed

- The two places FreshRSS opens with `<details>` share one header. The environment block on About was a card holding a second framed list, padded by 2rem on three sides from the base layer, and the advanced sections when adding a feed were a pair of hairlines that barely registered. Both carry the same header now — a surfaced row with a chevron that turns when the section opens — while what the header sits on still follows the content: a card around the environment list, nothing around the advanced sections, whose rows have to keep the form's label axis.
- The end of the stream closes the card instead of trailing off into it. FreshRSS separates the status line from the mark-as-read action with `<br>`, and the base layer adds 5em below the footer plus 100vh below the big button, which left roughly 60px of empty card under the last line. It is one centred column now, with the status as a quiet caption above the action, bounded padding, and a tick that matches its label in the small variant instead of overrunning it.
- The settings popover opens with a balanced inset. Every section header carries a margin that separates it from the section above, which the first one does not have — it stacked with the header's own padding into 30px of empty space above the first label, against 14px below the last entry. The first header sits 13px from the edge now, and the space between sections is unchanged.
- The QuickCollapse toggle no longer looks disabled. The extension ships one fixed-color asset per state, both drawn in `#bebebe`, and an external SVG cannot inherit `currentColor` — so its control sat greyed out between icons that follow the color scheme. The glyph is painted from a mask now, in the same foreground as its neighbours, with a bundled Lucide pair: chevrons meeting for "collapse", parting for "expand".

## 1.2.1 - 2026-08-16

### Fixed

- Updating the theme no longer leaves a browser with styling from the previous release. FreshRSS cache-busts only the sheets named in `metadata.json`, by their mtime; the partials `atelier.css` pulls in through `@import` keep their URL forever. That was harmless while the override layer only added rules, but 1.2.0 moved several controls into a single layer by *removing* rules from those partials — so a cached partial brought the old mark-as-read surface and the old search-field states back, next to an override layer that no longer counteracts them. Every `@import` now carries the release version, and `check_theme.py` fails a release whose imports do not.

## 1.2.0 - 2026-08-16

### Added

- `_palette.css` holds the neutral ramp on its own, as the eleven canonical Tailwind 4.3 "Mist" steps plus a derived rung for dark raised surfaces. It is the only file a color scheme changes; semantic roles, component rules and the accent hues for success, warning and destructive are shared. Steps 50 to 700 were already exactly Mist, so the light scheme keeps its values.
- `check_theme.py` verifies WCAG contrast. It resolves every semantic role through `var()` and `color-mix()` down to sRGB and checks it against the surfaces it is painted on, separately for the light and the dark scheme — 4.5:1 for text, 3:1 for control boundaries and focus rings. A role that cannot be reduced to sRGB is reported rather than skipped. The palette must also be complete, so a scheme cannot omit a step that a role depends on.

### Fixed

- The mark-as-read segment carries the toolbar's own surface. A rule left over from the structural layer outranked it and painted the segment in `--muted` instead of the group's card, with 16px of inline padding where every other segment uses 12.25px — a visibly greyer, wider control in an otherwise white toolbar. Its hover came from the same rule and diverged from `--accent` in the dark scheme.
- Below 840px the mark-as-read menu trigger keeps the theme's end-cap radius. A mobile rule from the structural layer set 5px through an ID selector and outranked the 7px inner radius of the group.
- Text typed into the header search uses the page foreground instead of the sidebar foreground, which the structural layer applied to that one field.
- A group an extension nests inside a toolbar group stays a wrapper instead of drawing a second card. QuickCollapse wraps the sort trigger and its own button in another `.stick`, which took the group styling: a hairline and an 8px radius mid-group, and a height 2px taller than the space between its parent's borders. Such a wrapper now stretches without a surface, and the segments at its ends carry the group's end caps.
- Extension buttons in the toolbar's hook group sit in the row like every other segment. Extensions fill `#nav_menu_hooks` with their own markup, and a control there often lacks FreshRSS' `.btn` class, so it kept its intrinsic size and height inside a group sized for 40px segments. Any interactive direct child of a toolbar group now gets the segment geometry, surface, and end-cap corners.
- The sidebar button on the mobile subscription view is the same 40px square as every other toolbar control. FreshRSS wraps it in a `.group` on the configuration view but in a plain `<div>` on the subscription view, so its `block-size: 100%` resolved against an auto height and the button collapsed to 16px tall. Standalone toolbar controls state the control height themselves now.
- That button also sits on the page's text axis. FreshRSS emits its own bar for it, which the base layer keeps at `display: block`, so it followed neither the centred toolbar nor the heading below it.
- The toolbar keeps its layout below 840px. The flex row was scoped to the desktop breakpoint, so the mobile bar fell back to centred inline blocks whose 8px margins collapsed differently per row, and kept the 3.75rem indent the desktop sidebar toggle used to need. It is the same row now, allowed to wrap, with one gap value and one set of edges.
- The header search keeps one silhouette across its states. The base layer greyed the field on hover and filled its submit button with the accent colour whenever the field was hovered or focused, so one control read as three; the button's white icon also kept its brightness filter on the light hover surface and nearly disappeared. The field now keeps its surface, focus is the only state the field itself shows, and the button takes a surface only under its own pointer.
- Settings rows that read out plain text — the version, the last update check, the article count under Maintenance — align their value with their label. The label carries an optical offset for the text inside a control, and a row without a control had nothing to offset against, so the label sat a third of a line below its own value.
- Toolbar and category menus open below their trigger instead of over it. FreshRSS leaves `.dropdown-menu` without a block offset and relies on its static position, which this theme invalidated by turning the wrapper into a flex or grid container.
- "Mark all as read" and its menu trigger fill their group. FreshRSS wraps that pair in the `<form>` that submits the action, and the toolbar treated the wrapper as a segment, so both controls sized to their text and floated in the middle of the group with a hover surface visibly shorter than the control.
- The hover and active surface of a segmented control follows the rounded corner of its group. End caps were rounded at `--at-radius-s`, one pixel short of the group's inner corner, which left a sliver of the surface visible; an end-cap dropdown trigger was not rounded at all, because the toolbar's flattening rule outweighed the cap rule.
- Enabled add and overflow-menu icons retain the same foreground weight as their neighboring controls in dark mode instead of resembling disabled actions.
- The sort menu retains FreshRSS' directional up/down glyph instead of replacing its state with a generic three-dot overflow icon.
- Toolbar overflow no longer clips dropdown menus, and ellipsis toggles keep a full 40px hit target with an explicitly rendered three-dot icon instead of appearing as an empty segment.
- Inset news rows subtract both horizontal margins from their actual width, so hover and current-state surfaces retain matching rounded corners on both sides instead of overflowing the trailing edge of the stream.
- Secondary text now uses ramp step 600 instead of 500. Step 500 met 4.5:1 only on the white card and missed it on `--background` (4.14:1) and `--muted` (4.44:1). This was not specific to Mist: step 500 misses the mark in eight of the nine Tailwind neutrals, step 600 clears it in all nine.
- Control boundaries meet the 3:1 of WCAG 1.4.11. `--input` was ramp step 300, which reached 1.47:1 against a white card. Since no step lands near 3:1 — 400 gives 2.19:1, 500 jumps to 4.14:1 and reads as a hard outline — the role is mixed from the two and lands at 3.16 to 3.52:1.
- The dark scheme no longer overrides the control boundary with a 20% blend of the foreground, which composited to 1.89:1 against a card and was the worst contrast in the theme. Both schemes share one contrast-checked value: a mid-grey works as the darker element on light surfaces and as the lighter one on dark surfaces.
- The favorite star is legible on a light row. `icons/starred.svg` was `#d99e04`, which reached only 2.13 to 2.37:1 against the row backgrounds it can land on — below the 3:1 that WCAG 1.4.11 asks of a graphical indicator. It is `#ad7d09` now, the one gold that clears the bar on light and dark rows alike; an external SVG cannot inherit `currentColor` and the star is deliberately exempt from the dark-mode icon filter, so a single value has to serve both. `--favorite` matches the asset and no longer differs per scheme, and the contrast guard compares the two so they cannot drift apart.
- `--frss-switch-accent-color` named `--success`, but Atelier paints `.switch.active` with `--primary` and has done all along. The token now names the color that is actually rendered.

### Changed

- The structural layer no longer styles the header search, the mark-as-read segment, or the toolbar's mobile spacing. Those rules only survived because the override layer restated them; both sides are gone, so each control is described in one place. No rendering changes from this, verified by comparing computed styles across five rebuilt FreshRSS pages.
- Dark-mode separators and decorative outlines now use a quieter neutral step across the header, toolbar, sidebar, stream, cards, and menus. Inputs and focus indicators retain their stronger, contrast-checked boundaries.
- Feed action popovers now use a compact command-menu layout with a stable icon column, solid popover surface, 36px rows, and a semantic divider before refresh and mark-as-read actions. The styling follows FreshRSS link targets and classes, so it remains independent of the selected interface language.
- Article rows read as rounded chips inset from the card. Hover and current state use one continuous, softly tinted surface; the former leading marker, Mapco's current-row border, its compensating negative margin, and the rules between rows are gone. Unread rows remain distinguished typographically.
- Toolbar actions are true segmented controls: every group owns one card surface and one quiet outer boundary, while its actions are separated by hairlines and active state is communicated by fill. Icon-only actions are square at 40px; labelled buttons use the same height and grow inline.
- Inputs, selects, search, and buttons share a 40px control contract, aligned content, consistent radii, and the same focus-ring behavior. Input boundaries use `--at-field-border` uniformly on all four sides instead of combining a hairline box with a heavier bottom edge; toolbar and button boundaries use the quieter `--at-button-border` token.
- Date separators are compact full-width section headers. Their subtle surface and bottom divider replace the decorative trailing rule and establish a stable start edge for the first news row.
- Dark surfaces walk down the ramp instead of using hand-picked values: page 900, cards 800, raised states between 800 and 700, separators 700. The two values that were tuned by hand are derived now, so a new scheme does not have to supply them.
- The contrast guard covers the accent hues in the roles they are painted in: alert text on its own tint, `--destructive` as error text, and the favorite star on every row background. The border of an alert against its own tint is deliberately excluded — the tint and the text identify the alert, so the border delimits rather than informs.
- The feed eyebrow above an article title is flush with the title again. Mapco insets the first item of every horizontal list, which is a row inset only as long as that item sits in a column of its own. With the read and favorite controls switched off in the topline settings, the first item is `.item.website`, which shares its grid column with the title, so the eyebrow was indented by 7px against the title and summary. The row now carries the inset itself, where it shifts every column alike; layouts that do show those controls render identically to before.
- Notification toasts now derive their status marker from `--success` and `--destructive` instead of two literal colors. The toast paints itself in `--foreground`, so it inverts with the color scheme; the literals only held up in light mode and dropped the success dot to 1.68:1 and the failure dot to 2.66:1 against a dark-mode toast, which left the two variants — otherwise identical in background and text color — practically indistinguishable. The failure marker is now a diamond as well, so state no longer rests on hue alone.
- Fixed the hover state of a toast's close button, which used a near-white overlay and disappeared on the light dark-mode toast. It is now mixed from `--background`, the toast's own text color, so it inverts along with it.
- Removed a stray yellow fallback from the sidebar scrollbar. Every browser that supports the `:dir()`, `:has()` and subgrid rules this theme relies on also supports `color-mix()`, so the fallback only ever shadowed the intended value.
- The unread counter of the active feed no longer keeps the base theme's border, which made it the only pill in the tree with an outline.
- Drag-and-drop feedback follows the palette instead of the base theme's literal `#ff0`, which clashed with the Mist neutrals when reordering feeds.
- `metadata.json` now carries the version as the semver string `1.1.0`. FreshRSS accepts a string or a number, but a JSON number cannot express a patch release and made `1.1` and a future `1.10` the same value.
- Dropped the 15 `_*.rtl.css` partial mirrors. FreshRSS rewrites only the filenames listed in `metadata.json` to `.rtl.css`, so the partials — reached through `@import`, which resolves relative to the importing sheet — never needed a mirror. `atelier.rtl.css` now imports the same partials as `atelier.css` and is a verbatim copy of it.
- Removed the leftover `lato` font stack from `atelier.css` and `_forms.css`. Nothing has declared an `@font-face` for it since `_fonts.css` was emptied, and both declarations were already overridden by `--at-sans`.
- Removed the `.form-group::after` clearfix, which declared no `content` and so never generated a box.
- The release checks now anchor each layout invariant to the selector and at-rule context that is meant to carry it, rather than testing for a raw substring anywhere in the file. Declarations such as `flex-direction: column` occur up to eight times and a selector as short as `.btn` is a substring of a dozen others, so a third of the assertions passed no matter which rule was deleted.
- `check_theme.py` reads the expected theme version from the changelog, guards `atelier.css` for direction neutrality as well, and rejects partial RTL mirrors if they reappear.

## 1.1.0 - 2026-08-15

### Added

- Aligned the sidebar's category rows with its feed rows. The control column is now pinned, so a category's collapse button no longer widens it and staggers the chevrons and titles against the rows above.
- Added leading Lucide icons to every entry of the settings dropdown, the settings sidebar and the subscription sidebar, statistics included. FreshRSS emits no icons there, so each entry is keyed off its target URL and drawn as a mask tinted with `currentColor`, which follows the hover, active and dark-theme foreground without a second asset. Nine new icons join the bundle; the rest reuse existing glyphs.
- Added a system-controlled dark color scheme using the existing semantic shadcn/ui token layer and locally bundled dark variants for CSS background icons.

### Changed

- Refined fully populated article rows into a dense, predictable desktop grid. Optional controls now share one action rhythm, feed names truncate cleanly, thumbnails retain their configured footprint including borders and a stable text gutter, and right-edge actions use a deliberate outer inset. Title, author, summary, and date retain a clear hierarchy without animating favicons on row hover. Feed names now sit above the title, giving every thumbnail a stable shared axis regardless of source-name length, while icon-only sources retain their compact inline placement. Rows without thumbnails keep the same separation between their actions and textual content, and source metadata shares one type scale with publication dates. Image rows without summaries no longer reserve an empty content line, keeping their thumbnails and text blocks vertically centered; rows with summaries align publication dates with their source metadata instead. Expanded article footers now anchor their publication date to the trailing edge instead of distributing it across FreshRSS's empty fixed-width option cells.
- Removed the redundant “Back to your RSS feeds” action from configuration, subscription, statistics, and authenticated error views. The FreshRSS logo remains the consistent route back to the feed list. Advanced Search now follows the subscription and statistics sections as the final sidebar entry.
- Unified article typography with Atelier's sans-serif hierarchy, including linked headings inherited from Mapco. Article titles now wrap predictably, keep a stable foreground color, and use a restrained underline on hover.
- Removed Mapco's nested title-only hover fill, which appeared as a second rectangle inside the article row. Hovered and open rows now retain their subtle full-row state without an additional color behind the title.
- Added a smooth, direction-aware sidebar reveal for explicit toggle actions. Persisted collapsed-state restoration remains transition-free, preventing the sidebar from flashing open during reloads and feed refreshes. Child controls retain their native sizing and spacing throughout the open state.
- Reworked statistics into a responsive full-width dashboard grid and gave informational text views a wide, readable content measure instead of fixed legacy box widths.
- Replaced direction-specific spacing, borders, and radii in the Atelier UI layer with CSS logical properties.
- Replaced view-specific form and fieldset sizing with unified responsive form systems for authentication, settings, administration, subscription, profile, search, and slider views, including consistent field widths, sections, help text, compound controls, and non-sticky action rows.
- Simplified RTL generation now that the UI source handles both directions.
- Consolidated duplicate alert rules and centralized their palette tokens.
- Added a semantic shadcn/ui token layer while preserving Mapco compatibility aliases and the existing Mist palette.
- Applied consistent shadcn-style states to native FreshRSS controls, forms, cards, tables, pagination, overlays, feedback, and utility surfaces.
- Standardized project-owned documentation, metadata, and code comments in English.

### Fixed

- Kept FreshRSS's mobile-only sidebar opener hidden on desktop configuration and subscription pages. The generic toolbar layout had exposed it outside its intended breakpoint, causing inconsistent placement and styling while requiring a first click merely to synchronize its mobile state.
- Prevented the About and Terms content column from collapsing to its min-content width or centering itself vertically when combined with the form container-query system.
- Fixed the desktop application header to one shared block size and normalized its item padding, so the sidebar and main content no longer shift vertically between views.
- Preserved the intended information-alert colors that were previously overwritten by a later generic alert rule.
- Prevented toast notifications from exceeding very narrow viewports.
- Replaced an invalid `rgba(var(--main-first), ...)` log-row color with a valid semantic error surface.
- Removed nested frames from search and toolbar groups, balanced the outer gutters, aligned the header controls, centered the toolbar rhythm, standardized control heights, increased outline contrast, standardized configuration select widths, and restored spacing around the sign-out icon.
- Replaced the folder-shaped sidebar toggle with the conventional Lucide `PanelLeft` icon.
- Centered button labels and replaced inconsistent native select arrows with a locally bundled Lucide chevron.
- Mapped the shared FreshRSS base-theme colors to Atelier's semantic tokens and corrected the current FreshRSS article-title selector so list titles remain legible in dark mode, with a matching adaptive surface for theme metadata.
- Softened dark outline controls and toolbar groups with translucent borders and a lighter control shadow while preserving the light-theme contrast.
- Restored dark-mode contrast for the main-stream, important-feed, category, label, and feed-action icons in the sidebar while preserving feed favicons and the gold favorite state.
- Replaced the sidebar's arbitrary grid-row span with an explicit two-row desktop layout so short article lists remain directly below the toolbar.
- Replaced inherited table, float, absolute-position, and fixed-width layout assumptions in the header, article rows, settings forms, sidebar rows, and global feed cards with intrinsic CSS Grid and container-query layouts.
- Kept the tick visible on disabled checkboxes and radios, whose muted fill previously covered the checked state.
- Rounded only the outer edges of button groups again, so middle segments no longer render as pills between flat end caps.
- Removed the sidebar dropdown toggle's inherited negative margins and inline padding, which pushed the button out of its grid row and off-center.
- Gave dropdown menus the settings sidebar's inset, so entries, section labels and icons share one rhythm across both. Mapco's 2rem left every entry indented past its own heading, and a second, redundant 2rem rule scoped to `.dropdown-section` restated the same value at a higher specificity; it was removed. Sort menus now draw their ✓ in a reserved slot instead of a negative margin, which at the smaller inset would have placed the glyph outside the entry's hover surface.
- Extended dropdown hover surfaces across the full menu width for button entries such as logout and the mark-as-read choices. A button stays content-sized at `display: block`, so the previous `width: auto` stretched only the link and span entries.
- Made the mobile sidebar's close icon visible. Its bundled SVG stroke is `#394447`, the exact light-theme `--primary` that Mapco paints the close bar with, so the icon was invisible against its own background; in dark mode the global icon inversion left it at 1.17:1 on the inverted bar. It now uses the primary foreground in light mode and its native stroke in dark mode.
- Restored sidebar feed names below 840px, where the hidden `.no-mobile` dropdown left the title auto-placed in the intrinsic grid column and collapsed it to a few characters. Feed rows in the global view had the same defect whenever favicons were disabled. Both now place their children explicitly.

### Development

- Expanded local checks for manifest order, imports, local Markdown links, runtime asset URLs, SVG validity, RTL token parity, and license files.
- Replaced the RTL blocklist with a parser-based direction check that flags physical properties, left/right keywords, horizontal translations and shadows, and asymmetric box and radius shorthands, exempting `:dir()` rules and declarations marked `rtl-safe`. The check ignores a trailing `!important`, matches property names case-insensitively, and covers shadow values held in custom properties.
- Converted the inherited Mapco partials to logical properties, so all 15 stylesheets are direction-neutral and every RTL counterpart is generated rather than hand-maintained. RTL parity is now asserted for all of them instead of only `_variables.css`.
- Added a FreshRSS 1.29.1 component coverage matrix and enforced the required semantic token contract in local checks.

## 1.0.0 - 2026-08-14

### Added

- Reproducible RTL generation and dependency-free local release checks.
- Public documentation, license attribution, and CI verification.
- Initial Atelier release based on the official Mapco theme.
- A dedicated shadcn/ui-inspired override layer using the Mist color palette.
- 44 adapted Lucide icons and a local system-font stack.
- An RTL counterpart for the Atelier override layer.

### Changed

- Reworked the desktop layout with CSS Grid so the sidebar stretches to the bottom of the page and animates cleanly when collapsed or expanded.
- Widened the date column for longer German date strings.
- Removed excessive whitespace below the “mark all as read” control.
