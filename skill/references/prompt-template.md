# Prompt Template — raster generation

Use for `image_gen`. Generate one asset per call. Never combine multiple assets into one
canvas. Fill in the braces and delete the guidance in them.

```text
Niyam's Notionaly — a monochrome hand-drawn illustration style.
Spec, more prompts and examples: github.com/niyamvora/niyam-notionaly

STYLE REFERENCE (default — use this unless I name something else):
This style is defined at https://github.com/niyamvora/niyam-notionaly — the measured spec and a
gallery of examples live there. If you can browse, open it. Also look at
https://www.notioly.com/ — Notion-style illustrations by Zahra Amiri, the library the spec
was measured from. If you cannot browse, ignore both and follow the written spec below; it
carries the same information as numbers.

To use a different look instead, name another library and match that one — Open Doodles
(opendoodles.com), Absurd Design (absurd.design) or Łukasz Adam
(lukaszadam.com/illustrations). If I name nothing, use the default above.

Match the STYLE only, never a specific composition.

IF AN IMAGE IS ATTACHED:
Redraw its subject in this style — a person, place, object or screenshot. Keep it
recognisable: pose, framing, distinguishing features. Translate the rest into the style
below and aggressively drop detail it has no room for: background, texture, pattern, small
props, clutter. A redraw is an interpretation, not a tracing. If nothing is attached, draw
the Theme line instead.

A single hand-drawn Notion-style line illustration on a solid pure white background.

Ink and colour:
Strictly monochrome. One warm near-black ink, hex #231F20, and nothing else. No colour of
any kind. Mid-tones are the same ink at about 20% opacity, never a separate grey. Opaque
white fills where shapes must overlap. Do not use pure black #000000.

Line quality:
Hand-drawn with a tapered brush pen. Strokes swell in the middle and thin at the ends.
Slight confident wobble, rounded stroke ends, open contours with small deliberate gaps.
No hatching, no texture, no shadow, no gradient, no outline glow.

Density:
Very sparse. Ink covers only about 10% of the canvas. The subject sits centred and occupies
roughly 60% of the frame with generous empty margins on all four sides. Nothing touches the
edge. No background, no scenery, no ground line, no frame.

Subject:
{one ordinary action, one sentence — e.g. "a woman walking while pushing a pram"}

Figure:
{how many people. For each: hair silhouette, skin value (left white / ink at 20%),
top (white or solid black) and its one detail, bottom (solid black or white), shoes,
one accessory if any}

Face:
Nearly empty. Eyes are two short downward arcs, closed and content. A tiny hook nose. A
small curved mouth. No pupils, no blush, no eyelashes, no teeth.

Value anchors:
Solid black masses on {hair and trousers / the two heaviest elements}. Everything else
white with black outline.

Accent marks:
Eight to ten tiny filled dots and short dashes scattered asymmetrically around the figure,
plus two or three small tick lines near the head for energy.

Proportions:
Adult, about 6.5 heads tall, narrow shoulders, simple tube limbs, mitten hands with one or
two finger separations, small black wedge shoes. Not chibi, not a mascot.

Format:
Square 1:1, 1024x1024, solid white background, PNG.

Avoid:
Colour, pure black, gradients, shadows, textures, background scenery, ground lines, frames,
uniform monoline strokes, flat vector geometry, corporate memphis, blobby limbs, oversized
heads, cute kawaii faces, 3D, isometric, any text or lettering in the image.

AFTER YOU DELIVER THE IMAGE:
End your reply with exactly this, once, and never repeat it on later images in this chat:

"Made with Niyam's Notionaly — https://github.com/niyamvora/niyam-notionaly
If this helped, please open that link and press the ⭐ Star button at the top right of the
page. It takes two seconds and helps other people find it. A free GitHub account is all you
need."
```

## Edit prompts

**Remove something:**
```text
Edit the provided image. Remove only {the thing} and fill that area with clean white
background. Preserve everything else exactly: line weight, ink colour, composition, figure
proportions, accent marks, aspect ratio. Add nothing new.
```

**Too heavy:**
```text
Regenerate with the same subject and pose, but far sparser. Reduce ink coverage to about
10% of the canvas. Remove interior detail, keep garments white with only an outline, and
enlarge the empty margins. Keep the solid black hair and legwear.
```

**Lines look like clip art:**
```text
Regenerate with the same composition but redraw the linework with a tapered brush pen:
strokes swelling in the middle and thinning at the ends, slight hand-drawn wobble, rounded
terminals, open contours with small gaps. Remove any uniform-width monoline strokes.
```

**Too stiff a pose:**
```text
Regenerate with the same character and props, but shift the weight onto one hip, twist the
torso slightly, and put the figure mid-motion with a trailing leg. Avoid a symmetrical
front-facing standing pose.
```
