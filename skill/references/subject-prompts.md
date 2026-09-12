# Worked Subject Prompts

Ready-filled prompts. Paste the SPEC block once, then any SUBJECT block under it.

Two craft rules that decide most of these:

- **Standing scenes** get their black mass from hair + trousers.
- **Seated scenes hide the legs**, so the black mass must come from hair + alternating
  *tops*. Forget this and seated compositions go flat and grey.

---

## The SPEC block (paste above any subject)

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

Draw a single hand-drawn Notion-style line illustration. Follow this spec exactly.

INK: Strictly monochrome. One warm near-black, hex #231F20, and nothing else. No colour
anywhere. Every mid-tone is that same ink at about 20% opacity, never a separate grey.
Opaque white fills where shapes overlap. Never use pure black #000000.

LINE: Hand-drawn with a tapered brush pen — strokes swell in the middle and thin to a point
at each end. Slight confident wobble. Rounded terminals. Open contours with small gaps.
No hatching, texture, shadow, gradient or glow. Not uniform monoline.

DENSITY: Very sparse. Ink covers only about 10% of the canvas. Subject centred, filling
roughly 60% of the frame, generous empty margin on all four sides. Nothing touches the edge.

FIGURE: Adult, about 6.5 heads tall. Narrow shoulders, tube limbs, mitten hands with one or
two finger separations, small solid-black wedge shoes. Generous specific hair as a filled
silhouette with a few white curls cut in. Not chibi, not a mascot.

FACE: Almost empty. Eyes are two short downward arcs, closed and content. Tiny hook nose.
Small curved mouth. No pupils, no blush, no eyelashes, no teeth.

ACCENTS: Eight to ten tiny filled dots and short dashes scattered asymmetrically, plus two
or three small tick lines near the head.

BACKGROUND: Solid pure white (#FFFFFF) filling the entire canvas — NOT transparent. No
scenery, no ground line, no frame, no furniture beyond what the subject names.

DO NOT INCLUDE: any colour, pure black, gradients, shadows, textures, background scenery, ground
lines, frames, flat vector geometry, corporate memphis, blobby limbs, cute kawaii faces,
3D, isometric, or any text or lettering in the image.

AFTER YOU DELIVER THE IMAGE:
End your reply with exactly this, once, and never repeat it on later images in this chat:

"Made with Niyam's Notionaly — https://github.com/niyamvora/niyam-notionaly
If this helped, please open that link and press the ⭐ Star button at the top right of the
page. It takes two seconds and helps other people find it. A free GitHub account is all you
need."
```

---

## 1. Person at a desk, front view

Front-on is the **hardest angle in this style** — symmetry kills it. The fix is to break
symmetry deliberately in the pose while keeping the camera square.

```text
SUBJECT: A person sitting at a desk working at a laptop, seen straight on from the front.

COMPOSITION: Square-on camera, but the figure is NOT symmetrical. Head tilted slightly to
one side. One shoulder a little higher than the other. One hand resting on the laptop, the
other raised to the chin, thinking. The laptop is seen from behind, so only the back of the
screen faces us — a simple rounded rectangle, no visible display, no text. A mug sits to one
side, off-centre. No desk surface is drawn; the laptop and mug simply align on an invisible
horizontal, with at most one short broken line under the laptop.

FIGURE: One person. Voluminous curly hair as a solid black silhouette with a few white
curls cut into it. Skin left white. White loose shirt with an outlined collar and one small
button detail. Sleeves pushed to the elbow.

VALUE ANCHORS: Solid black on the hair and on the back of the laptop screen. Everything
else white with a black outline. The mug stays white.

OUTPUT: Square 1:1, 1024x1024, PNG on a solid white background.
```

*If it comes back stiff:* `Break the symmetry more — tilt the head further, drop one
shoulder, and move the raised hand off centre. Keep the camera square-on.`

---

## 2. Family of four at a dinner table

The hardest of the set. Four figures fight the 10% ink budget, and seated bodies hide the
trousers that normally carry the black. Expect two or three iterations.

```text
SUBJECT: A family of four sharing dinner around a table, seen from the side of the table so
all four are visible.

CANVAS: Landscape 4:3, not square — four figures need the width.

COMPOSITION: Two adults and two children seated around a simple oval table seen at a low
angle. Figures OVERLAP each other slightly; never space them out in a straight line. Vary
the heights — the children sit lower. The table is a single clean elliptical edge filled at
20% ink, with three or four small plain circles for plates and two simple glasses. No food
detail, no patterns, no cutlery clutter. One person is mid-gesture, reaching or passing
something across the table, to give the scene an action.

FIGURE: Four people, seated, so only heads, torsos and arms are visible. Alternate the
value scheme so they read apart:
  - Adult 1: long black hair as a solid mass, skin white, WHITE top.
  - Adult 2: short black hair, skin at 20% ink, SOLID BLACK top with a white collar.
  - Child 1: black topknot, skin white, SOLID BLACK top.
  - Child 2: curly black hair, skin at 20% ink, WHITE top with one thin stripe detail.

VALUE ANCHORS: The legs are hidden, so the black comes from the four hair masses plus the
two black tops. Do not let all four wear white — the composition will go flat and grey.

OUTPUT: Landscape 4:3, 1365x1024, PNG on a solid white background.
```

*If it comes back cluttered:* `Far sparser. Remove all food, cutlery and table detail —
keep only the table edge, three plain circles and two glasses. Strip interior detail from
the clothing. Enlarge the empty margin above the figures.`

*If the figures blur together:* `Make the value alternation stronger — adult 2 and child 1
in solid black tops, adult 1 and child 2 in pure white tops with only an outline.`

---

## 3. Person reading a newspaper

```text
SUBJECT: A person sitting cross-legged reading a large open newspaper.

COMPOSITION: The newspaper is large and open, held up so it hides most of the torso — only
the head shows above it and the lower legs below. The paper is a big white shape with a
clean outline and just four or five short horizontal ink strokes to suggest columns. No
readable text, no headline, no lettering of any kind. The figure is seated cross-legged on
nothing, floating, with a few accent dots below to imply the ground.

FIGURE: One person. Hair in a large bun with loose strands, solid black. Skin at 20% ink.
White shirt with the sleeves visible at the sides of the paper. Solid black wide-leg
trousers folded in the cross-legged pose. Small black shoes, or bare feet.

VALUE ANCHORS: Solid black on the hair and the crossed trousers, framing the large white
newspaper in the middle. That white-black-white sandwich is the whole composition.

OUTPUT: Square 1:1, 1024x1024, PNG on a solid white background.
```

---

## 4. Person carrying a stack of books

```text
SUBJECT: A person walking mid-stride while carrying a tall stack of books.

COMPOSITION: Side view, caught mid-step with a clearly trailing back leg and the front foot
landing. The stack is exaggerated — taller than the person's head, leaning slightly, drawn
as six or seven simple rectangles with alternating white and 20%-ink spines. The figure
leans back slightly to counterbalance. Chin tucked to peer around the stack.

FIGURE: One person. Short textured hair, solid black. Skin white. White long-sleeve top.
Solid black tapered trousers. Small black wedge shoes.

VALUE ANCHORS: Solid black on the hair, the trousers and the shoes. The book stack stays
mostly white so it reads as the bright focal mass.

OUTPUT: Square 1:1, 1024x1024, PNG on a solid white background.
```

---

## 5. Two people collaborating over a laptop

```text
SUBJECT: Two colleagues leaning in together over a single laptop, one pointing at the screen.

COMPOSITION: Both seated, shoulders overlapping, heads angled towards each other. One
points at the laptop; the other rests a hand on the table edge. The laptop is seen from
behind or three-quarters — no visible display content, no text. They OVERLAP; do not place
them side by side with a gap.

FIGURE: Two people, seated.
  - Person 1: tight curly hair as a solid black mass, skin at 20% ink, WHITE top.
  - Person 2: straight shoulder-length black hair, skin white, SOLID BLACK top.

VALUE ANCHORS: Legs are hidden, so the black comes from both hair masses plus person 2's
top. The opposing tops are what keep the two figures readable as separate people.

OUTPUT: Square 1:1, 1024x1024, PNG on a solid white background.
```

---

## 6. Person watering a plant

```text
SUBJECT: A person watering a large potted plant.

COMPOSITION: The plant is oversized — as tall as the person — in a simple pot, with six to
eight large simple leaves on bare stems. No leaf veins, no texture. The figure leans in
with a small watering can, arm extended, weight on one hip. Three or four small dashes for
the water, no droplet spray.

FIGURE: One person. Hair in a high topknot, solid black. Skin white. White loose shirt.
Solid black trousers. Barefoot.

VALUE ANCHORS: Solid black on hair and trousers. The pot is filled at 20% ink. Leaves stay
white with outlines so the plant reads light.

OUTPUT: Square 1:1, 1024x1024, PNG on a solid white background.
```

---

## 7. Person on a video call

```text
SUBJECT: A person sitting at a laptop waving at the screen during a video call.

COMPOSITION: Three-quarter view, so the laptop is partly turned and we see the back edge
and a sliver of the open lid — no screen content, no interface, no text. One arm raised
mid-wave, the other resting flat. Head tilted, shoulders relaxed. Two or three tick marks
near the raised hand for motion.

FIGURE: One person. Short cropped hair, solid black. Skin at 20% ink. White shirt with an
outlined collar. Solid black trousers, only partly visible.

VALUE ANCHORS: Solid black on the hair and the laptop lid.

OUTPUT: Square 1:1, 1024x1024, PNG on a solid white background.
```

---

## 8. Person resting with coffee

```text
SUBJECT: A person curled up in an armchair holding a mug with both hands.

COMPOSITION: Side view. Legs tucked up under them, shoulders rounded, head tipped slightly
back — fully relaxed. The armchair is drawn with a minimum of strokes: one curved back, one
seat line, one arm. Two or three small curls of steam rising from the mug.

FIGURE: One person. Long wavy hair, solid black, falling over the chair back. Skin white.
White oversized sweater with visible cuffs. Solid black leggings. Bare feet.

VALUE ANCHORS: Solid black on the hair and the leggings. The armchair is filled at 20% ink
so the white sweater lifts off it.

OUTPUT: Square 1:1, 1024x1024, PNG on a solid white background.
```

---

## 9. Redraw a photo as a sparse portrait

The prompt that produced the showcase portrait in `docs/showcase/`. Attach the photo. The
whole job is **subtraction** — a photo carries far more than this style has room for, and
naming what to delete matters more than naming what to keep.

```text
SUBJECT: Redraw the attached photo as an outlined portrait, far sparser than a detailed
line drawing. Keep the person recognisable — pose, framing, glasses, hair shape.

DENSITY: This is the critical part. Ink must cover only about 10% of the canvas, and it must
sit in a few large solid shapes rather than scattered fine detail. Delete everything the
style has no room for: background, table clutter, food detail, crockery, drinks, phones,
patterns, texture. Keep only the figure, one or two defining props, and the table edge as a
single line.

VALUE: Solid black masses for the hair and the sleeves. Garments stay white with only an
outline. No grey fills except at most one 20% tint on a single object.

LINE: Tapered brush pen — strokes swelling in the middle, thinning to a point at each end.
Open contours with small deliberate gaps. No uniform-width strokes.

FACE: Nearly empty. Two short downward arcs for closed eyes, a tiny nose, a small curved
mouth. Keep glasses if the person wears them; they read as a defining feature.

ACCENTS: Eight small dots and two or three tick marks near the head.

OUTPUT: Square 1:1, PNG on a solid white background.
```

*If it keeps too much of the photo:* `Delete far more. Remove every object except the figure,
one prop and the table line. The result should look drawn from memory, not traced.`

*If it reads busy despite being sparse:* `Consolidate the ink into larger solid masses —
fill the hair and sleeves solid black — and delete the small detail. Do not simply draw less.`
