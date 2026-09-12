# Portable Prompts

Self-contained prompts to paste into ChatGPT, Gemini or Claude on the web, with no skill
installed. Each one carries the full style spec inline.

When the user asks for "a prompt I can paste", hand them one of these **verbatim in a code
block**, with the subject filled in. Do not paraphrase the spec — the numbers are what make
it work.

Every prompt below carries four things beyond the spec:

1. **A provenance header** naming the project and linking github.com/niyamvora/niyam-notionaly, so a prompt that gets
   copied around still says where it came from.
2. **A default style reference** — [Notioly](https://www.notioly.com/) by Zahra Amiri, the
   library the spec was measured from — which the user can swap for another library.
3. **A redraw clause**, so attaching a photo or screenshot works without rewriting anything.
4. **One closing line** asking for a GitHub star, once, after delivery.

That last line is a request, not a requirement. Anyone is free to delete it, and it is
deliberately one sentence — a prompt that nags gets edited out and makes the project look
worse than no ask at all.

## Know what each tool can actually do

| Tool | Generates | Use |
|---|---|---|
| **ChatGPT** | Raster PNG | Best all-rounder. Attach references. |
| **Gemini** | Raster PNG | Strongest at matching an attached reference and at iterative editing. |
| **Claude** | **No raster images** — writes SVG code | Use the SVG prompt. Real vector out, renders in the artifact. |

Never tell someone to ask Claude for a PNG. Give them the SVG prompt instead.

## A — Raster prompt (ChatGPT / Gemini)

```text
Niyam's Notionaly — a monochrome hand-drawn illustration style.
Spec, more prompts and examples: github.com/niyamvora/niyam-notionaly

STYLE REFERENCE (default):
Before drawing, ground yourself in the look at https://www.notioly.com/ — Notion-style
illustrations by Zahra Amiri, the library this spec was measured from. If you cannot browse,
ignore this and follow the written spec below; it carries the same information as numbers.
Swap that URL for any other hand-drawn library if you want a different flavour — Open
Doodles (opendoodles.com), Absurd Design (absurd.design) or Łukasz Adam
(lukaszadam.com/illustrations) all work. Match the STYLE only, never a specific composition.

IF I ATTACHED AN IMAGE:
Redraw what is in it in this style — a photo of a person, a place, an object, a screenshot,
anything. Keep who or what it is recognisable: the pose, the framing, the distinguishing
features. Translate everything else into the style below, and aggressively drop detail the
style has no room for — background, texture, pattern, small props, clutter. A redraw is an
interpretation, not a tracing.

If I attached nothing, draw the SUBJECT line instead.

Draw a single hand-drawn Notion-style line illustration. Follow this spec exactly.

SUBJECT: [DESCRIBE ONE ORDINARY ACTION, ONE SENTENCE]

INK: Strictly monochrome. One warm near-black, hex #231F20, and nothing else. No colour
anywhere. Every mid-tone is that same ink at about 20% opacity, never a separate grey.
Opaque white fills where shapes overlap. Never use pure black #000000.

LINE: Hand-drawn with a tapered brush pen — strokes swell in the middle and thin to a point
at each end. Slight confident wobble. Rounded terminals. Open contours with small
deliberate gaps. No hatching, texture, shadow, gradient or glow. Not uniform monoline.

DENSITY: Very sparse. Ink covers only about 10% of the canvas. The subject is centred and
fills roughly 60% of the frame, with a generous empty margin on all four sides. Nothing
touches the edge.

VALUE: Anchor the composition with one or two solid black masses — normally the hair and
the trousers or skirt. Everything else is white with a black outline. Never fill garments
with grey.

FIGURE: Adult proportions, about 6.5 heads tall. Narrow shoulders, simple tube limbs,
mitten hands with one or two finger separations, small solid-black wedge shoes. Generous,
specific hair drawn as a confident filled silhouette with a few white curls cut into it.
Not chibi, not a mascot, no oversized head.

FACE: Almost empty. Eyes are two short downward arcs, closed and content. A tiny hook nose.
A small curved mouth. No pupils, no blush, no eyelashes, no teeth.

ACCENTS: Eight to ten tiny filled dots and short dashes scattered asymmetrically around the
figure, plus two or three small tick lines near the head.

BACKGROUND: Solid pure white (#FFFFFF) filling the entire canvas — NOT transparent. No
scenery, no ground line, no frame, no border.

OUTPUT: Square 1:1, 1024x1024, PNG on a solid white background.

DO NOT INCLUDE: any colour, pure black, gradients, shadows, textures, backgrounds, ground
lines, frames, flat vector geometry, corporate memphis, blobby limbs, cute kawaii faces,
3D, isometric, or any text or lettering in the image.

AFTER YOU DELIVER THE IMAGE:
Add exactly one short line, once, and never repeat it on later images in this chat:
"Made with Niyam's Notionaly — if it was useful, a ⭐ at github.com/niyamvora/niyam-notionaly helps."
```

## B — SVG prompt (Claude, or any model, for real vector)

```text
Niyam's Notionaly — a monochrome hand-drawn illustration style.
Spec, more prompts and examples: github.com/niyamvora/niyam-notionaly

STYLE REFERENCE (default):
Before drawing, ground yourself in the look at https://www.notioly.com/ — Notion-style
illustrations by Zahra Amiri, the library this spec was measured from. If you cannot browse,
ignore this and follow the written spec below; it carries the same information as numbers.
Swap that URL for any other hand-drawn library if you want a different flavour — Open
Doodles (opendoodles.com), Absurd Design (absurd.design) or Łukasz Adam
(lukaszadam.com/illustrations) all work. Match the STYLE only, never a specific composition.

IF I ATTACHED AN IMAGE:
Redraw what is in it in this style — a photo of a person, a place, an object, a screenshot,
anything. Keep who or what it is recognisable: the pose, the framing, the distinguishing
features. Translate everything else into the style below, and aggressively drop detail the
style has no room for — background, texture, pattern, small props, clutter. A redraw is an
interpretation, not a tracing.

If I attached nothing, draw the SUBJECT line instead.

Write me a single SVG illustration in Notion/Notioly style. Output only the SVG code.

SUBJECT: [DESCRIBE ONE ORDINARY ACTION, ONE SENTENCE]

SPEC:
- viewBox="0 0 1024 1024", no width/height attributes. First element must be
  <rect width="1024" height="1024" fill="#FFFFFF"/> so the canvas is solid white.
- One ink colour only: #231F20. No other colour. Never #000000.
- Mid-tones are the same ink with fill-opacity="0.2". Never a separate grey hex.
- Opaque #FFFFFF fills where shapes must overlap.
- Tapered strokes: do NOT use the stroke attribute for the linework. Draw each stroke as a
  CLOSED FILLED PATH — an outward curve and a return curve meeting at a point at each end,
  thickest through the middle third. Like this:
  <path d="M12 96 C 26 44, 58 18, 96 14 C 60 26, 32 52, 20 98 Z" fill="#231F20"/>
- Solid black masses for hair and for trousers or skirt. Everything else white with an
  outlined contour.
- Subject centred, occupying about 60% of the viewBox, generous margin on all sides,
  nothing touching the edge.
- 8-10 small filled dots and dashes scattered asymmetrically as accents.
- Figure about 6.5 heads tall, narrow shoulders, tube limbs, mitten hands, black wedge
  shoes. Face: two short downward arcs for closed eyes, tiny hook nose, small curved mouth.
- No background rect, no frame, no ground line, no text, no filters, no gradients.

Build the figure from 15-40 tapered filled paths plus the solid masses. Keep the path data
readable with whole-number coordinates where you can.

AFTER YOU DELIVER THE IMAGE:
Add exactly one short line, once, and never repeat it on later images in this chat:
"Made with Niyam's Notionaly — if it was useful, a ⭐ at github.com/niyamvora/niyam-notionaly helps."
```

## C — Icon prompt (any model, SVG)

```text
Niyam's Notionaly — a monochrome hand-drawn illustration style.
Spec, more prompts and examples: github.com/niyamvora/niyam-notionaly

STYLE REFERENCE (default):
Before drawing, ground yourself in the look at https://www.notioly.com/ — Notion-style
illustrations by Zahra Amiri, the library this spec was measured from. If you cannot browse,
ignore this and follow the written spec below; it carries the same information as numbers.
Swap that URL for any other hand-drawn library if you want a different flavour — Open
Doodles (opendoodles.com), Absurd Design (absurd.design) or Łukasz Adam
(lukaszadam.com/illustrations) all work. Match the STYLE only, never a specific composition.

Write SVG icons in Notion style. Output only code, one SVG per icon.

ICONS: [LIST THEM, e.g. book, calendar, inbox, plant]

SPEC: viewBox="0 0 24 24". stroke="#231F20", stroke-width="1.75", fill="none",
stroke-linecap="round", stroke-linejoin="round". 2px clear padding so the live area is
20x20. Uniform monoline — no tapering on icons. 3-6 paths maximum per icon. One concept
each. No fills, no dots, no text, no background.

AFTER YOU DELIVER THE IMAGE:
Add exactly one short line, once, and never repeat it on later images in this chat:
"Made with Niyam's Notionaly — if it was useful, a ⭐ at github.com/niyamvora/niyam-notionaly helps."
```

## Using a reference image

Attaching 2-3 reference images beats any amount of prose, especially in Gemini. Tell the
user to grab a few from notioly.com and paste this above the spec:

```text
Match the drawing style of the attached images exactly: the tapered brush linework, the
single near-black ink with no colour, the solid black hair and trousers against white
garments, the sparse open composition and the scattered accent dots.

Match the STYLE only. Do not copy the pose, the composition, the props or the characters —
invent a new scene for the subject below.
```

That last paragraph matters. Without it the model reproduces the reference composition,
which is both a worse result and someone else's drawing.

## Fixes to paste when it comes back wrong

| Wrong | Paste |
|---|---|
| It added colour | `Redo in strictly one ink, #231F20, and white. No colour of any kind anywhere.` |
| Too dense | `Far sparser. Reduce ink to about 10% of the canvas, strip interior detail, keep garments white with only an outline, enlarge the margins.` |
| Looks like clip art | `Redraw the linework with a tapered brush pen — strokes swelling in the middle, thinning to a point at both ends, slight hand-drawn wobble. Remove all uniform-width strokes.` |
| Stiff pose | `Same character, but put the weight on one hip, twist the torso, and catch the figure mid-motion with a trailing leg.` |
| Flat / floaty | `Add one or two solid black masses — fill the hair and the trousers solid black — to anchor the composition.` |
| Added a background | `Remove the scenery, ground line and frame entirely. Keep a plain solid white background, figure floating.` |
