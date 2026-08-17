# Atelier component coverage

This matrix maps FreshRSS 1.29.1 UI surfaces to their closest shadcn/ui counterparts. Atelier ports the visual language to FreshRSS's existing HTML; it does not bundle React, Tailwind CSS, or Radix/Base UI behavior.

Status meanings:

- `complete`: all applicable native states are styled by Atelier;
- `partial`: Atelier has a dedicated treatment, but native states are missing;
- `base`: the surface still relies primarily on Mapco or FreshRSS base styles;
- `not applicable`: FreshRSS has no matching native surface.

Status records static CSS coverage. Runtime verification is a separate release gate and is not implied by `complete`.

## Native component matrix

| shadcn/ui counterpart | FreshRSS 1.29.1 surface | Primary selectors | Status |
| --- | --- | --- | --- |
| Typography | Application and article text | `body`, `.post`, `.flux_content` | complete |
| Button | Actions and toolbar controls | `.btn`, `.btn-important`, `.btn-attention` | complete |
| Button Group | Grouped toolbar controls | `.stick`, `.group` | complete |
| Input | Text, search, URL, number, date, email, password and file inputs | `input` | complete |
| Textarea | Multiline configuration fields | `textarea` | complete |
| Native Select | Configuration and filtering choices | `select` | complete |
| Field and Label | Configuration forms and help text | `.form-group`, `.group-name`, `.group-controls`, `.help` | complete |
| Checkbox | Boolean configuration fields | `input[type="checkbox"]`, `.checkbox` | complete |
| Radio Group | Content selector choices | `input[type="radio"]` | complete |
| Switch | Extension enable/disable control | `.switch`, `.switch.active` | complete |
| Card | Global view, statistics and configuration panels | `.box`, `.box-title`, `.box-content`, `.post` | complete |
| Item | Feed, category and article rows | `.item`, `.feed`, `.flux_header` | complete |
| Badge | Labels, tags and unread counters | `.label`, `.labels`, `.tag`, `[data-unread]` | complete |
| Alert | Warning, information, success and error messages | `.alert-*`, `.alert-head` | complete |
| Empty | Empty feeds, queries and extension lists | `.prompt.alert`, `#noArticlesToShow` | complete |
| Dropdown Menu | Header, article and feed menus | `.dropdown-menu`, `.dropdown-section`, `.separator` | complete |
| Popover | Global-view feed selector | `.dropdown`, `.dropdown-menu` | complete |
| Sheet | Feed, category, tag and configuration side panels | `#slider`, `#overlay`, `.toggle_aside` | complete |
| Dialog | Embedded popup content | `#popup`, `#popup-content`, `#popup-close` | complete |
| Sonner | Global notifications and update state | `.notification`, `#actualizeProgress` | complete |
| Progress | Feed refresh status | `#actualizeProgress progress`, `.progress` | complete |
| Spinner | Loading and update actions | `.loading`, `#load_more`, `.btn-state2` | complete |
| Table | Configuration, statistics and log tables | `table`, `th`, `td`, `.table-wrapper` | complete |
| Pagination | Logs and long lists | `.pagination`, `.nav-pagination` | complete |
| Separator | Date, menu and navigation separators | `.transition`, `.separator` | complete |
| Collapsible | Advanced forms and environment details | `.form-advanced`, `.form-advanced-title`, `details`, `summary` | complete |
| Sidebar | Feed tree and configuration navigation | `.aside`, `.tree`, `.nav-list` | complete |
| Toggle Group | Reading filters and view controls | `.nav_menu .stick`, `.nav_menu .group` | complete |
| Tooltip | Native title-based hints | `[title]` | not applicable |
| Chart | Statistics visualizations rendered by Chart.js | `.jsonData-stats`, `.stat` | base |
| Drop Zone | OPML import and draggable lists | `.drop-zone`, `.dragbox`, `.draggableList` | complete |

## State contract

Every applicable component must be exercised in these states before release:

- default, hover, active or selected;
- `:focus-visible` keyboard focus;
- disabled and read-only;
- invalid where supported by native validation;
- loading and empty where applicable;
- narrow mobile viewport;
- RTL document direction; and
- reduced motion.

## Out of scope for a CSS-only FreshRSS theme

The following shadcn/ui components do not have a native FreshRSS 1.29.1 surface or require markup and interaction behavior that a theme cannot add:

- Accordion, Alert Dialog, Aspect Ratio, Avatar and Breadcrumb;
- Calendar, Carousel, Combobox, Command and Date Picker;
- Context Menu, Drawer, Hover Card and Menubar;
- Input OTP, Navigation Menu, Resizable and Scroll Area;
- Skeleton, Slider, Tabs and standalone Toggle; and
- chat-oriented Attachment, Bubble, Marker, Message and Message Scroller.

If FreshRSS adds a matching surface later, it can be mapped here. Adding new behavior belongs in a separate FreshRSS extension rather than this theme.
