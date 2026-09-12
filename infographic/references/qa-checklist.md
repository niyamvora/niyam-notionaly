# QA Checklist

Render the PNG and **look at it** before delivering. Most of these are invisible in source.

## Content

- [ ] One headline, two lines maximum.
- [ ] Every number has a unit and a label.
- [ ] Bar widths are the real percentages of the real values — check the arithmetic.
- [ ] Bar and column axes start at zero.
- [ ] Source line present.
- [ ] No claim in the artwork that the data does not support.

## Layout

- [ ] Six sections maximum on `poster`; one idea on `slide`; hero only on `social`.
- [ ] At least 40% of the canvas is empty.
- [ ] Nothing is clipped at the canvas edge — check the rendered PNG, not the HTML.
- [ ] `slide` fits in 1080px with no scrollbar.
- [ ] Spacing uses only the 8 / 16 / 24 / 40 / 64 / 96 scale.
- [ ] Numbers in columns are tabular and actually align.

## Style

- [ ] Mono unless the user asked for colour.
- [ ] In colourful mode: one accent, on data marks only. Body type still `--ink`.
- [ ] Illustrations are monochrome `#231F20`, on white, not faded, not behind text.
- [ ] Charts are clean geometry. No hand-drawn wobble on a data mark.
- [ ] No gradients, shadows, bevels, 3D or pie charts.
- [ ] Illustrations sit at edges and corners, not competing with the data.

## Export

- [ ] PNG renders at the intended pixel size.
- [ ] Text is crisp — if it is soft, the device scale factor is wrong.
- [ ] All images resolved; no broken-image icons in the render.
- [ ] Asset paths are relative to the HTML file.

## Common failures

| Looks like | Cause |
|---|---|
| Cramped, nothing breathes | Too many sections. Cut one |
| Art and data feel unrelated | Illustrations chosen before the content was written |
| Bars look wrong | Axis not starting at zero, or widths eyeballed |
| Muddy, low contrast | Tint used where solid ink belonged |
| Generic corporate deck | No illustrations, or they are centred instead of framing |
| Blurry text in the PNG | Missing `--force-device-scale-factor` |
