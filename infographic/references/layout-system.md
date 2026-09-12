# Layout System

## Three canvases

| Preset | Size | Grid | Margin | Use |
|---|---|---|---|---|
| `poster` | 1200 x auto (portrait, scrolls) | 12 col, 24px gutter | 80px | Content-heavy, many sections |
| `slide` | 1920 x 1080 (16:9) | 12 col, 32px gutter | 96px | Decks. **One idea per slide** |
| `social` | 1080 x 1080 or 1080 x 1350 | 6 col, 24px gutter | 72px | Instagram, LinkedIn, X |

A Notion-embed variant is just `poster` with `--canvas-w: 900px`. Change the one variable;
do not build a separate preset.

`slide` is the strict one. If the content needs scrolling, it is not a slide — either cut it
or switch to `poster`.

## Type

One grotesque throughout. No second family, no handwritten display face — the hand-drawn
character comes from the illustrations, and a script headline next to them reads as clutter.

```css
--font: ui-sans-serif, -apple-system, "Inter", "Helvetica Neue", Arial, sans-serif;
```

Scale at `poster` (1200px). Multiply by 1.4 for `slide`, by 0.9 for `social`:

| Role | Size / weight | Notes |
|---|---|---|
| Display | 64px / 700 / -0.02em | The one headline. Two lines maximum |
| Stat number | 88px / 700 / -0.03em | Tabular numerals. The hero of most infographics |
| Section | 32px / 700 / -0.01em | |
| Body | 18px / 400 / 1.55 | Max ~70 characters per line |
| Label | 14px / 500 / uppercase / 0.06em | Axis labels, tile captions, kickers |
| Source | 12px / 400 / 60% ink | Footer, citations |

```css
font-variant-numeric: tabular-nums;   /* on every number that sits in a column */
```

## Spacing

One 8px scale: `8 / 16 / 24 / 40 / 64 / 96`. Nothing between.

- Between sections: 96px (`poster`), 64px (`social`)
- Section heading to its content: 24px
- Inside a tile: 24px padding
- Label to the number it belongs to: 8px

Separate sections with whitespace. Use a hairline rule (`1px solid var(--tint)`) only when
two adjacent sections would otherwise read as one.

## Density

The illustrations are ~90% empty. The page must not fight that.

- **Six sections maximum** on a `poster`. Three is usually better.
- **One idea per section.** If a heading needs "and", split it.
- At least 40% of the canvas is empty.
- **Four to six illustrations on a `poster`**, one on a `slide` or `social`.

An infographic that fills every pixel will look nothing like the artwork sitting in it.

## Placing illustrations

Follow reference `diagrams/01-two-people-node-diagram.png` in the notion skill: figures sit
at the **corners or edges**, framing the structure. They do not sit in the middle competing
with data.

- **Hero:** one illustration beside the headline, ~40% of the hero block width
- **Inside every stat tile:** a 150px spot above the label. This is the default, not an
  option — a stat row with no art is a table
- **Split section:** one illustration filling half the row, paired with the text it explains
- **Band:** a row of three to five small spots with captions
- **Framing pair:** two figures at opposite corners of a diagram, as in the reference

Never put an illustration behind text. No opacity-faded background artwork — mono assets
turn to mud behind type.

### The density test

An infographic where the art could be deleted without the page changing meaningfully is a
text document with decoration. Each illustration should sit **with** the words it belongs
to — above its own number, beside its own paragraph — not collected in one hero slot while
the rest of the page runs as plain prose.
