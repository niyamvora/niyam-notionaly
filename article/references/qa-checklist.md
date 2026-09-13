# QA Checklist — set level

Run the **parent** skill's `references/qa-checklist.md` on every image first, including the
runnable ink and edge/ink measurements. That catches colour creep, density and linework.

This file catches what only shows up when you look at the set together and at the article.

## Must pass

- [ ] **No text anywhere in any image.** No caption, no label, no node name, no title in a
      corner, no stray lettering. This is the most common failure and it is fatal.
- [ ] **Same person throughout.** Hair silhouette, skin value, top, bottom and accessory
      identical in every image. Lay the set out side by side and check.
- [ ] **No repeated prop or action** between any two images in the set.
- [ ] **No structure used more than twice** across the set.
- [ ] **Every image has a placement** — a specific paragraph it sits after, not "somewhere in
      section 2".
- [ ] **Every image passes the removal test.** Delete the person mentally; if the idea still
      reads, the person was decoration.
- [ ] **Every caption is six to fourteen words** (or characters, in Chinese) and names the
      picture rather than explaining it.
- [ ] **Count is right** — 1-3 for a short post, 4-8 for an article, 9 at the absolute most.
- [ ] **Consistent canvas.** All 16:9 unless the user asked otherwise.

## Failure signals

- Two images in one article both showing a person carrying a stack
- An image that could be swapped with another in the set without the article changing
- Images spaced evenly, one per section, regardless of what the sections do
- A caption longer than the paragraph above it
- Arrows with words on them, or boxes with names in them
- A picture that needs its caption to be comprehensible
- The character's hair changing between image 2 and image 5
- An image illustrating a heading rather than an idea
- Colour used to mark a flow or a warning — the style has one ink and no exceptions

## Measuring a 16:9 asset

The parent's ink band — 6-16% — was measured on **1:1** assets. A body illustration puts the
same figure on a canvas 78% wider, so a perfectly good one measures near 6% and looks like a
borderline fail. Measure inside the subject's bounding box instead, where the band holds:

```bash
python3 - <<'PY'
from PIL import Image, ImageFilter
im = Image.open("01-name.png").convert("RGB")
W, H = im.size
g = im.convert("L").point(lambda p: 255 if p < 250 else 0).getbbox()
sub = list(im.crop(g).convert("L").getdata())
print("ink in subject bbox:", round(sum(1 for p in sub if p < 250)/len(sub)*100, 1), "% (6-16)")
print("margins: L%d%% R%d%% T%d%% B%d%% (12-20)" % (
    g[0]/W*100, (W-g[2])/W*100, g[1]/H*100, (H-g[3])/H*100))
bw = im.convert("L").resize((900, 900)).point(lambda p: 0 if p < 128 else 255)
ink  = sum(1 for p in bw.getdata() if p < 128)
edge = sum(1 for p in bw.filter(ImageFilter.FIND_EDGES).getdata() if p > 40)
print("edge/ink:", round(edge/ink, 2), "(<0.30)  solid mass:", round(max(ink-edge,0)/ink*100), "% (>70)")
PY
```

Resize to a **square** for the edge/ink pass — the metric is a ratio, so the distortion
cancels, and a 16:9 resize biases it.

**edge/ink and solid mass are the two that catch a weak drawing**, and they are scale- and
aspect-invariant, so they apply unchanged. A 16:9 illustration that is all thin outline reads
floaty at any coverage: consolidate into larger solid masses rather than drawing less. A prop
is allowed to carry one of them — a solid band on a case, a filled bag — when the figure's
hair and legwear are not enough to anchor a wide frame.

## Iteration order

Fix in this order; earlier fixes often resolve later ones.

1. **Text in the image** → the removal edit prompt, or regenerate with the avoid line restated
   first. Never ship an image with lettering in it.
2. **Character drifted** → regenerate the odd ones out with the five locked attributes pasted
   verbatim.
3. **Figure is decoration** → rewrite the composition line so the action is the idea.
4. **Repeats another image** → change the prop and the action, keep the character.
5. **Reads as a diagram** → strip boxes and arrows, go back to one person and one prop.
6. **Still flat** → the problem is usually the shot list, not the drawing. Go back to
   `shot-list.md` and check the idea line survives without "and".

## The delivery test

Read the article with the images in place, in order, at the width they will actually be
viewed. A good set makes the argument skimmable — someone scrolling the pictures alone should
come away with the shape of the piece.

If the images could belong to any article on the topic, they are stock art with better
linework. Go back to step one.
