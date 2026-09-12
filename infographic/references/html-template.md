# HTML Template

`assets/template.html` is a working skeleton. **Copy it and fill it in — do not rewrite the
CSS from scratch.** It already carries the tokens, the three canvas presets, the type scale
and every component below.

## Switching canvas

One attribute on `<body>`:

```html
<body data-preset="poster">   <!-- default, 1200px, scrolls -->
<body data-preset="slide">    <!-- 1920x1080, fixed height -->
<body data-preset="social">   <!-- 1080 square -->
```

For a Notion embed, keep `poster` and set `--canvas-w:900px`.

## Components

| Class | What it is |
|---|---|
| `.section` | A block with the standard 96px separation |
| `.hero` | Headline + illustration, two columns |
| `.display` `.section-title` `.body` `.label` `.source` | The type scale |
| `.grid.cols-2` `.grid.cols-3` | Column layouts |
| `.stat` + `.stat-num` | Big-number tile |
| `.bars` + `.bar-row` `.bar-track` `.bar-fill` | Horizontal bars. Width is set inline as a percentage |
| `.nodes` + `.node` `.connector` | The node diagram |
| `.illus` `.illus--spot` `.illus--corner` | Illustration slots |
| `.num` | Tabular numerals on any number in a column |
| `.rule` | Hairline separator — use sparingly |

## Colour

Mono is the default and needs no change. For colourful mode, uncomment `--accent` in
`:root` and use `.bar-fill--accent` on data marks only. Body type stays `--ink`. See
`color-policy.md`.

## Rules

- Bar widths are real percentages of the real values. Never eyeball them.
- Every number that sits in a column gets `font-variant-numeric:tabular-nums` (the `.num`
  class, already applied inside `.stat-num` and `.bar-value`).
- Illustrations are `<img>` with `alt=""` when decorative, or real alt text when they carry
  meaning. Never a CSS background — they must sit on the page unfaded. Their white ground
  matches the page, so no seam shows.
- Do not add a web font unless asked. The system stack matches Notion closely and needs no
  network fetch, which also keeps headless export deterministic.
