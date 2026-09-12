---
name: niyam-notionly-infographic
description: Build infographics, data posters, stat slides and social data cards by composing real HTML with real type, using monochrome Notion-style illustrations as the artwork. Use when the user asks for an infographic, a data poster, a stats graphic, a visual summary of an article or report, a chart-led slide, or a shareable data card. Handles poster, 16:9 slide and square social canvases, and exports to PNG or PDF with headless Chrome.
---

# Infographics

Compose infographics as **HTML with real text**, illustrated with monochrome Notion-style
artwork from `niyam-notionly-illustrations`.

## The rule that decides the whole approach

**Never generate an infographic as a raster image.** An infographic is mostly text and
numbers, and image models garble both — you get plausible labels reading "Reveune" and bars
that contradict the values printed on them. This is not fixable by prompting.

So it splits in two:

| Layer | Built with |
|---|---|
| Layout, headlines, labels, numbers, charts | HTML + CSS — real, selectable, exact |
| Spot illustrations, framing figures | `niyam-notionly-illustrations` → transparent mono PNG/SVG |

## Read as needed

- `references/layout-system.md` — the three canvases, grid, type scale, spacing, density.
- `references/color-policy.md` — **mono by default.** Read before choosing any colour.
- `references/data-viz.md` — chart selection and specs.
- `references/composition-recipes.md` — hero, stat row, bars, process, comparison, closer.
- `references/html-template.md` — how to use the skeleton.
- `references/qa-checklist.md` — check against the rendered PNG, not the source.
- `assets/template.html` — **the working skeleton. Copy it; do not rewrite the CSS.**

## Colour — do not ask, assume mono

Default to monochrome `#231F20`. Switch to the colourful variant **only** on an explicit
signal from the user: "colourful", "add colour", "brand colours", "make it pop", a named
colour, or a supplied palette. Then it is one accent on data marks only — body type stays
ink, and the illustrations stay monochrome regardless. Details in `color-policy.md`.

## Workflow

### 1. Content first

Write the headline, the numbers and the labels as plain text before choosing any layout.
If the user gave an article, pull out the three to six claims that carry real figures.

If a claim has no number behind it, it is a sentence, not a stat. Do not invent figures, and
do not dress an opinion as data.

### 2. Pick the canvas

`poster` (1200 wide, scrolls) | `slide` (1920x1080) | `social` (1080 square). Ask only if
the user gave no clue. Default `poster`.

### 3. Choose recipes and illustration slots

From `composition-recipes.md`. Decide how many illustrations and where — **four to six on a `poster`**, one on a `slide`
or `social`.

Spread them through the page rather than stacking one hero at the top: one in the hero, one
inside **each** stat tile, one in a split section beside the paragraph it explains. An
infographic whose art could be deleted without changing the page is a text document with
decoration.

### 4. Generate the illustrations

Hand off to **`niyam-notionly-illustrations`** (this skill's parent), one asset per call, transparent background. Save
to the workspace:

```text
examples/infographics/<name>/illustrations/
```

### 5. Compose

Copy `assets/template.html` into the workspace as `examples/infographics/<name>/index.html`
and fill it in. Set `data-preset`. Keep asset paths relative.

Compute bar widths from the real values — never eyeball a percentage.

### 6. Export

Headless Chrome. Use the installed browser directly; do not open an interactive Chrome tab.

On macOS under Codex, launching an app from `/Applications` may be blocked by the workspace
sandbox and fail without producing a screenshot. If the first render produces no output
file, do not repeat the same command. Re-run the exact render once with the shell tool's
escalated sandbox permission, explaining that the installed Chrome binary needs to render a
local workspace HTML file. This is a local render and does not require network access.

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# PNG — set the window to the canvas width; height grows for poster
"$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=2 \
  --window-size=1200,3000 \
  --screenshot=out.png \
  "file://$PWD/index.html"

test -s out.png || { echo "Chrome did not create out.png" >&2; exit 1; }

# PDF
"$CHROME" --headless=new --disable-gpu --no-sandbox --no-pdf-header-footer \
  --print-to-pdf=out.pdf "$PWD/index.html"
```

`--force-device-scale-factor=2` is what keeps the type crisp; without it the PNG looks soft.
Use an absolute path or a `file://` URL — Chrome will not resolve a bare relative one.

For `slide`, use `--window-size=1920,1080`. For `social`, `1080,1080`. Both are fixed
heights and need nothing further.

**`poster` height must be trimmed.** Its height is whatever the content comes to, and the
CLI cannot ask the page. Render deliberately too tall, then crop the blank tail — otherwise
the PNG ends in a slab of empty white:

```bash
"$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1200,6000 \
  --screenshot=raw.png "file://$PWD/index.html"

test -s raw.png || { echo "Chrome did not create raw.png" >&2; exit 1; }
```

```python
# trim.py — crop the blank tail
from PIL import Image
im = Image.open("raw.png").convert("RGB")
w, h = im.size
px = im.load()
pad = 96 * 2                      # bottom margin x device scale factor
bottom = h
while bottom > 1 and all(px[x, bottom-1] == (255,255,255) for x in range(0, w, 7)):
    bottom -= 1
im.crop((0, 0, w, min(h, bottom + pad))).save("out.png")
```

Sampling every 7th pixel is enough to detect a blank row and keeps the scan fast. Ignore the
`CVDisplayLinkCreateWithCGDisplay` errors Chrome prints on macOS — they are harmless.

If Pillow is unavailable but `ffmpeg` is installed, decode the PNG to raw RGB, find the last
non-white row with standard Python, then crop with `ffmpeg`:

```bash
tmp_rgb=$(mktemp /tmp/infographic.XXXXXX)
ffmpeg -hide_banner -loglevel error -y -i raw.png -f rawvideo -pix_fmt rgb24 "$tmp_rgb"
IFS=, read img_w img_h < <(ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height -of csv=p=0 raw.png)

crop_h=$(python3 - "$tmp_rgb" "$img_w" "$img_h" <<'PY'
import sys

path = sys.argv[1]
width, height = map(int, sys.argv[2:])
row_bytes = width * 3
last = -1
with open(path, "rb") as image:
    for y in range(height):
        row = image.read(row_bytes)
        if any(channel < 250 for channel in row):
            last = y
print(min(height, last + 1 + 192))  # preserve the 96px bottom margin at 2x
PY
)

ffmpeg -hide_banner -loglevel error -y -i raw.png \
  -vf "crop=${img_w}:${crop_h}:0:0" out.png
rm -f "$tmp_rgb"
test -s out.png || { echo "Trim did not create out.png" >&2; exit 1; }
```

### 7. Check

Run `references/qa-checklist.md` **against the rendered PNG**, not the HTML. Clipping,
soft type and broken images are invisible in source.

### 8. Deliver

Report what was built, the canvas, the path to the HTML and the exported file. Mention that
the HTML is the editable source.

## Defaults

| Unstated | Default |
|---|---|
| Canvas | `poster` |
| Colour | Monochrome |
| Sections | Hero + illustrated stat row + split + source |
| Illustrations | **Four to six on `poster`** (hero + one per stat tile + split), one on `slide`/`social` |
| Export | PNG at 2x |

## Do not

- Generate the infographic as a single image
- Invent numbers, or present an opinion as a statistic
- Add colour unless asked
- Truncate an axis or start bars above zero
- Put an illustration behind text, or fade it into a background
- Ship a `poster` with only one illustration and plain text below it
- Draw charts with hand-drawn wobble — data marks are exact
- Add a web font unless asked
