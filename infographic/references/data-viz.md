# Data Visualisation

## The governing rule

**Illustrations are hand-drawn. Charts are not.**

Charts use clean, exact geometry — straight lines, true proportions, accurate axes. The
wobbly brush line belongs to the artwork only. A hand-drawn bar chart misrepresents its own
data, and "it is a style choice" is not a defence when a bar is 4% too long.

The contrast is deliberate and it reads well: loose figures, precise data.

## Chart selection

| Data | Use | Not |
|---|---|---|
| One headline figure | **A big number.** 88px, with a label | A single-slice donut |
| Parts of a whole | Stacked bar, or a bar per part | A pie chart |
| Ranking / comparing categories | Horizontal bars, sorted by value | A radar chart |
| Change over time | Line, or a column per period | A 3D anything |
| Two things compared | Two columns side by side | An infographic cliché |
| Process or flow | Node diagram (see below) | A chart |

Most infographic "charts" should be big numbers. Reach for a real chart only when the shape
of the data carries the point.

## Specs

**Big number.** 88px/700, tabular numerals, `--ink`. A 14px uppercase label above it, one
line of 18px body below. In colourful mode this is the one thing that may take `--accent`.

**Horizontal bars.** Bar height 32px, gap 16px. Fill `--ink` (or `--accent`). Track
`--tint-8`, full width, so lengths compare. Label left in 14px, value right, tabular.
Sort by value unless the order is inherently meaningful. No gridlines.

**Columns.** Width 48px, gap 24px. One baseline rule, 1px `--tint`. No y-axis line, no
gridlines — put the value directly above each column.

**Line.** 2px `--ink`, round caps, no area fill, no smoothing. A 5px filled dot at each data
point. One baseline rule only.

**Node diagram.** This is the style's own device — see `diagrams/01-two-people-node-diagram.png`
in the notion skill. Rounded rectangles, 1.75px `--ink` outline, `--tint-8` fill, connected
by 1.75px orthogonal lines with rounded corners. **Real labels go in real HTML type inside
the nodes** — the `...` placeholder is for generated artwork, not for a composed page where
you can set actual text.

## Always

- Label every axis and every series.
- Start bar and column axes at **zero**. Always.
- Put the number on or beside the mark; make the reader do no arithmetic.
- Cite the source in the 12px footer line.
- Round consistently, and say the unit once.

## Never

- 3D, drop shadows, bevels, glows
- Gradient fills
- Pie or donut with more than two slices
- Dual y-axes
- Truncated axes
- A chart where a sentence would do
