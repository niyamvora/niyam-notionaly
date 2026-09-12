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
px = [p for p in im.getdata() if p[3] > 200]
print("opaque coverage:", round(len(px)/(im.size[0]*im.size[1])*100, 1), "%")
for c, n in Counter(p[:3] for p in px).most_common(6):
    print("#%02X%02X%02X" % c, round(n/len(px)*100, 1), "%")
PY
```

Expect coverage in the 6-20% band and every listed colour to be a near-neighbour of
`#231F20` or `#FFFFFF`. Anything chromatic in that list is a fail.

Coverage alone is not enough — check **edge-per-ink** too, which catches a drawing that is
technically sparse but visually busy:

```bash
python3 - <<'PY'
from PIL import Image, ImageFilter
bw = Image.open("out.png").convert("L").resize((512, 512)).point(lambda p: 0 if p < 128 else 255)
ink  = sum(1 for p in bw.getdata() if p < 128)
edge = sum(1 for p in bw.filter(ImageFilter.FIND_EDGES).getdata() if p > 40)
print("edge/ink:", round(edge / ink, 2), "- under 0.30 is calm, 0.40+ reads busy")
PY
```

If it comes back high, consolidate the ink into larger solid masses and delete small detail.
Do not simply draw less.

## Iteration order

Fix in this order — earlier fixes often resolve later problems:

1. Colour crept in → regenerate, restate the one-ink rule first
2. Too dense → strip detail before touching anything else
3. Monoline → restate the tapered brush instruction
4. No black mass → fill hair and legwear solid
5. Stiff pose → shift weight, twist torso, add motion
6. Still generic → change the action, not the style
