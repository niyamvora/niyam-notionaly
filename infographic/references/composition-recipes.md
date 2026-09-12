# Composition Recipes

Assemble a page from these. Most infographics are **hero + stat row + one more section +
source**. Resist adding a fifth.

## Hero — every infographic has exactly one

Kicker label, one headline of at most two lines, one sentence of context, and one
illustration at 40-50% of the block width. The illustration sits beside the text, never
behind it.

Use `.hero`.

## Illustrated stat row — the workhorse

Three big numbers across. Each tile is **illustration / label / number / one line of
meaning**, in that order. Two tiles look sparse, four crowd; three is right on `poster` and
`slide`, two on `social`.

The illustration inside each tile is the default, not a flourish. A stat row without art is
a table, and the whole point of this format is that the art sits *with* the number it
belongs to.

Use `.grid.cols-3` with `.stat` and `.stat-illus`.

## Ranked bars

A sorted list of categories with a bar and a value each. Sort by value unless the order
carries meaning on its own. Cap at seven rows — beyond that it stops being an infographic
and becomes a table, which is fine, but make it a table.

Use `.bars`.

## Process or flow

Three to five nodes with connectors. This is the style's own device — see
`diagrams/01-two-people-node-diagram.png` in the notion skill, where two figures sit at
opposite corners framing the structure. Copy that placement: figures at the edges, structure
in the middle.

Real labels go in real type inside the nodes. The `...` placeholder belongs to generated
artwork, not to a composed page.

Use `.nodes`.

## Split — illustration beside the text it explains

A two-column row: a paragraph on one side, one illustration filling the other. Use it for
the idea that needs a picture rather than a number. Alternate which side the art sits on
between consecutive splits, or the page develops a visible seam down the middle.

Use `.split` with `.split--art-left` / `.split--art-right`.

## Band — a row of small spots

Three to five small illustrations across, each with a one-line caption. Good for a set of
parallel items — steps, categories, things to avoid — where each deserves an image but none
deserves a paragraph.

Use `.band`.

## Comparison

Two columns, one idea each. Borrow the illustration rule: give the two sides **opposing
value schemes** — one panel on `--tint-8`, the other on `--paper` — so they separate without
needing a colour.

Use `.grid.cols-2`.

## Closer

One small illustration, one line of conclusion, and the 12px source line. Optional, but it
stops a `poster` ending abruptly.

## Assembling

| Preset | Pattern | Illustrations |
|---|---|---|
| `poster` | Hero → illustrated stat row → split → process or band → closer | 4-6 |
| `slide` | Hero *or* one section. One idea. If it scrolls, it is not a slide | 1 |
| `social` | Hero only — one illustration, one number, one line | 1 |

A `poster` that uses only the hero slot and then runs as plain text has failed the format.
Spread the art through the page: one in the hero, one per stat tile, one in a split.

## The order to build in

1. Write the **content** first — headline, the numbers, the labels. Plain text.
2. Choose the recipes that fit what you wrote. Never pick a layout then hunt for content.
3. Decide the illustration slots — how many, where.
4. Generate the illustrations.
5. Compose the HTML.
6. Export.

Doing step 4 before step 1 is how you end up with art that does not match the argument.
