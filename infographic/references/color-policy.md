# Colour Policy

**Default to monochrome. Add colour only when the user asks for it.**

Do not ask "would you like colour?" — assume mono and proceed. Switch to the colourful
variant only on an explicit signal: "colourful", "add colour", "brand colours", "make it
pop", a named colour, or a supplied brand palette.

## Mono mode — the default

```css
--ink:    #231F20;              /* text, rules, chart marks, illustrations */
--tint:   rgba(35, 31, 32, 0.20);  /* fills, tracks, table stripes, panels */
--tint-8: rgba(35, 31, 32, 0.08);  /* very light panel grounds */
--paper:  #FFFFFF;
```

That is the whole palette. Charts encode with **solid vs. tint vs. outline**, never hue.
This matches the illustrations exactly, which is the point.

Two-series bar chart in mono: series A solid `--ink`, series B `--tint`. Three series is the
practical ceiling — beyond that, split into separate charts rather than inventing greys.

## Colourful mode — only on request

Keep `--ink` for all body text, rules and labels. Add **one** accent, used only for data
marks and one highlighted value:

```css
--accent: #D9730D;   /* pick one from Notion's palette below */
```

Notion's own palette, which is what to draw from:

```
#D9730D orange    #CB912F yellow    #448361 green     #337EA9 blue
#9065B0 purple    #C14C8A pink      #D44C47 red       #9F6B53 brown
```

Rules that still apply in colourful mode:

- Body text, headings, labels and axis lines stay `--ink`. Never colour type for decoration.
- One accent, not a rainbow. A second colour needs a real reason — genuinely distinct data
  series, not variety.
- Backgrounds stay `--paper`. No coloured panels, no gradients.

Only if the user asks for a **multi-series** chart that truly needs it, take further colours
from the palette above in that order, and keep saturation consistent.

## Illustrations stay monochrome

Even in colourful mode, the artwork stays `#231F20`. That is the style's identity, and
mono figures against one accent looks deliberate where coloured figures look muddy.

If the user explicitly wants tinted artwork, recolour rather than regenerate — the assets
are single-ink, so it is a one-line change:

```css
/* PNG: tint a transparent mono asset */
.illus { filter: brightness(0) saturate(100%)
         invert(47%) sepia(89%) saturate(1200%) hue-rotate(2deg); }
```
```xml
<!-- SVG: just swap the fill -->
<svg fill="#D9730D"> … </svg>
```

Prefer the SVG route; it is exact and the filter route is a guess.
