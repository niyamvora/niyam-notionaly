# QA Checklist

Check every asset before delivering. Most failures are the same four.

## Must pass

- [ ] **One ink only.** `#231F20`, plus white. Zero chromatic colour anywhere.
- [ ] **Not pure black.** No `#000000`.
- [ ] **Greys are opacity**, not a separate hex.
- [ ] **Sparse.** Ink covers roughly 10% of the canvas, no more than about 20%.
- [ ] **Margins.** Subject is centred at ~60% of frame. Nothing touches any edge.
- [ ] **Tapered linework**, not uniform monoline. (Icons excepted.)
- [ ] **One or two solid black masses** anchoring the value, normally hair and legwear.
- [ ] **Garments white**, outlined — not filled grey.
- [ ] **Background solid white.** No scenery, ground line, frame or border.
- [ ] **Face nearly empty.** Arc eyes, tiny nose, small mouth. No pupils or blush.
- [ ] **Accent marks present** — 8-12 dots and dashes, asymmetric.
- [ ] **No text** anywhere in the artwork.
- [ ] **Not a copy** of any reference composition.

## Failure signals

- Any colour at all, including "just a little muted accent"
- Uniform-width strokes making it look like a generic icon pack
- A desk, floor, wall or window added to ground the scene
- Two figures standing apart symmetrically like a lineup
- Oversized head, blobby limbs, corporate-memphis proportions
- Five articulated fingers
- Drop shadow, gradient, paper texture or noise
- The canvas looks busy or more than a fifth covered in ink
- A caption, label or watermark in the image

## Verifying the ink claim

Do not eyeball this — measure it:

```bash
python3 - <<'PY'
from PIL import Image
from collections import Counter
im = Image.open("out.png").convert("RGBA")
# Flatten onto white first, then count INK — not opaque pixels. This project ships a solid
# white ground by default, so an alpha test reports 100% coverage on every asset it draws.
im = Image.alpha_composite(Image.new("RGBA", im.size, (255,)*4), im).convert("RGB")
px = [p for p in im.getdata() if sum(p) / 3 < 250]
print("ink coverage:", round(len(px)/(im.size[0]*im.size[1])*100, 1), "%")
for c, n in Counter(px).most_common(6):
    chroma = max(c) - min(c)
    print("#%02X%02X%02X" % c, round(n/len(px)*100, 1), "%",
          "<- CHROMATIC, FAIL" if chroma > 6 else "")
PY
```

Expect coverage in the 6-20% band and every listed colour to be a near-neighbour of
`#231F20` or `#FFFFFF`. Judge colour by the chroma column rather than by the hex — a resized
or JPEG-compressed asset spreads into dozens of near-neighbours that are all still one ink.

**The band assumes a 1:1 canvas.** The same figure on a 16:9 body illustration sits on a
canvas 78% wider and lands near 6%. There, measure ink inside the subject's bounding box,
where the 6-16% band still holds — `niyam-notionaly-article` → `references/qa-checklist.md`
carries that snippet.

**If `PIL` will not import**, the system Python is externally managed (PEP 668). Do not pass
`--break-system-packages`; build a throwaway venv instead:
`python3 -m venv /tmp/qa && /tmp/qa/bin/pip -q install pillow && /tmp/qa/bin/python - <<'PY'`

Coverage alone is not enough — check **edge-per-ink** too, which catches a drawing that is
technically sparse but visually busy:

```bash
python3 - <<'PY'
from PIL import Image, ImageFilter
im = Image.open("out.png").convert("RGBA")
# flatten onto white FIRST: convert("L") turns transparent pixels black,
# which reports an almost-empty drawing as ~90% ink.
im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im)
bw = im.convert("L").resize((512, 512)).point(lambda p: 0 if p < 128 else 255)
ink  = sum(1 for p in bw.getdata() if p < 128)
edge = sum(1 for p in bw.filter(ImageFilter.FIND_EDGES).getdata() if p > 40)
print("edge/ink:   ", round(edge / ink, 2), "- under 0.30 calm, 0.40+ busy, 0.60+ floaty")
print("solid mass: ", round(max(ink - edge, 0) / ink * 100), "% - over 70% is properly anchored")
PY
```

If edge/ink comes back high or solid mass comes back low, consolidate the ink into larger
solid masses and delete small detail. **Do not simply draw less** — an outline-only drawing
can sit well inside the coverage band and still be the weakest thing you produce.

## Iteration order

Fix in this order — earlier fixes often resolve later problems:

1. Colour crept in → regenerate, restate the one-ink rule first
2. Too dense → strip detail before touching anything else
3. Monoline → restate the tapered brush instruction
4. No black mass → fill hair and legwear solid
5. Stiff pose → shift weight, twist torso, add motion
6. Still generic → change the action, not the style
