# Icons and Vector Output

## Which route produces real vector

There are two honest routes to SVG, and they suit different asset types.

| Asset | Route | Why |
|---|---|---|
| `icon` | **Hand-author SVG directly** | Monoline at icon scale is simple geometry. Cleanest result, tiny files. |
| `spot` | **Hand-author SVG directly** | Same — a few paths. |
| `character` | Hand-author, or generate + trace | Doable by hand with the tapered technique below. |
| `illustration` | **Generate PNG, then trace** | Tapered organic linework is impractical to hand-author at scene complexity. |

Do not claim a PNG is a vector. If the user asks for SVG on a complex illustration, run the
trace step and say that is what you did.

## Icons — hand-authored spec

Icons are the one place where **uniform monoline is correct**. They are UI furniture, not
illustration.

- `viewBox="0 0 24 24"`, 24x24 design grid
- Stroke `#231F20`, `stroke-width="1.75"`, `fill="none"`
- `stroke-linecap="round"`, `stroke-linejoin="round"`
- 2px clear padding — live area is 20x20
- Geometry on whole or half pixels where possible
- One concept per icon, 3-6 paths maximum
- No tapering, no accent dots, no fills

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"
     fill="none" stroke="#231F20" stroke-width="1.75"
     stroke-linecap="round" stroke-linejoin="round">
  <path d="M4 5.5A1.5 1.5 0 0 1 5.5 4H11v16H5.5A1.5 1.5 0 0 1 4 18.5Z"/>
  <path d="M20 5.5A1.5 1.5 0 0 0 18.5 4H13v16h5.5a1.5 1.5 0 0 0 1.5-1.5Z"/>
  <path d="M11 4v16"/>
</svg>
```

Scale the stroke with the grid: a 48px icon uses `stroke-width="2"` on `viewBox="0 0 48 48"`
proportionally, not a scaled-up 24 grid.

## Tapered strokes in hand-authored SVG

Illustrations need strokes that swell and thin. SVG `stroke` cannot taper — there is no
variable-width stroke in SVG — so any tapered line **must** be a closed filled path.

This is not a guess. Every [Open Doodles](https://www.opendoodles.com/) SVG inspected
carries `stroke="none"`: the entire figure is built from filled shapes, typically only
2-29 paths for a whole character. Draw each stroke as an outward curve and a return curve
meeting at two sharp points.

```svg
<!-- one tapered stroke: thick in the middle, pointed at both ends -->
<path d="M12 96 C 26 44, 58 18, 96 14 C 60 26, 32 52, 20 98 Z" fill="#231F20"/>
```

Rules for this: `fill="#231F20"`, no `stroke` attribute, maximum thickness around the middle
third, both ends meeting at a point. Build a figure from 15-40 such paths plus a few solid
masses for hair and legwear.

**Use `assets/taper.py` rather than computing these by hand.** Hand-computed beziers come
out uniform and dead, which is the most common way a hand-authored asset fails the style:

```python
from taper import stroke, arc, circle, blob, svg
paths = circle(200, 200, 118, w=10, wobble=2.0)      # hand-drawn circle, two arcs + gaps
paths.append(stroke([(200, 200), (200, 118)], w=10, w0=8, w1=3))   # a tapered hand
open("clock.svg", "w").write(svg(400, [f'<path d="{d}"/>' for d in paths]))
```

`stroke()` emits a closed filled path that is fattest through the middle and comes to a
point at each end. `circle()` draws a contour as two tapered arcs with deliberate gaps —
open contours are part of the style. Run `python3 taper.py` for its self-check.

Objects and icons hand-author well this way. **Figures do not** — a convincing person needs
15-40 individually shaped strokes and is better generated then traced.

It is slow but it is genuinely editable vector. Use it for icons, spots and objects.
For a full scene, trace instead.

## Tracing a generated PNG to SVG

One-time setup:

```bash
brew install potrace
```

Then:

```bash
# 1. flatten transparency onto white and threshold to 1-bit
python3 - <<'PY'
from PIL import Image
im = Image.open("in.png").convert("RGBA")
bg = Image.new("RGBA", im.size, (255,255,255,255))
flat = Image.alpha_composite(bg, im).convert("L")
flat.point(lambda p: 255 if p > 128 else 0).convert("1").save("in.pbm")
PY

# 2. trace — turdsize drops speckles, alphamax keeps corners soft
potrace in.pbm -s -o out.svg --turdsize 3 --alphamax 1.2 --opttolerance 0.3
```

Then post-process `out.svg`:
- Replace potrace's `fill="#000000"` with `fill="#231F20"`
- Delete the white background rectangle potrace emits as the first path
- Set `viewBox` to a square and remove fixed `width`/`height` so it scales

The 20% tints will trace as solid shapes. Either drop them before tracing, or after tracing
set those specific paths to `fill="#231F20" fill-opacity="0.2"`.

## Export formats

| Ask | Give them |
|---|---|
| "SVG" / "vector" / "editable" | `.svg` — hand-authored or traced |
| "PNG" | `.png`, solid white background, 1024 or 2048 square |
| "for Notion" | `.png` at 1024 — Notion does not render uploaded SVG inline |
| "for Figma" | `.svg` |
| "for a website" | `.svg`, plus a `.png` fallback |
| "icon set" | one `.svg` per icon, consistent 24 grid, plus a contact-sheet preview |

Notion caveat worth stating: Notion will not render an uploaded `.svg` as an image block.
Ship PNG for Notion use and keep the SVG as the source.
