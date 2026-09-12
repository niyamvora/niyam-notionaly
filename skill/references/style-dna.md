# Style DNA

Measured, not remembered. The numbers here are observations from published work across
several hand-drawn illustration libraries — see **Sources** at the bottom of this file.

This spec describes one specific point in that family: **strict monochrome**. Where the
sources disagree, the choice made here is stated and justified rather than assumed.

## One sentence

One warm near-black ink, hand-drawn with a tapered brush, on nothing. Solid black masses
against opaque white shapes. Enormous emptiness. Friendly, ordinary, calm.

## The palette is one color

```
Ink       #231F20    warm near-black — the ONLY colour in the artwork
Tint      #231F20 at 15-25% opacity — every "grey" is this, never a separate grey
Fill      #FFFFFF    opaque white, used to make shapes sit on top of each other
Ground    #FFFFFF    solid white, filling the canvas
```

There is no second colour. No blue, no beige, no accent. Measured across 13 assets: 100%
of opaque pixels were `#231F20` or `#FFFFFF`. Every mid-tone was the same ink at reduced
alpha. If you catch yourself adding a muted terracotta, you have left the style.

**Do not** use `#000000`. Pure black is colder and reads as clip-art. `#231F20` is the look.

## Density — the number most people get wrong

- Ink covers **6-16% of the canvas.** The drawing is overwhelmingly empty.
- Subject bounding box is **44-74% of the canvas** (typically ~60%), centred, with a
  12-20% margin on every side.
- Inside the subject, most area is still white. Garments are white with a black outline,
  not filled shapes.

If the canvas looks more than about a fifth covered in ink, it is too heavy. Delete detail.

**Coverage alone does not measure sparseness.** Two drawings at identical ink coverage can
read completely differently depending on whether the ink sits in a few solid masses or is
scattered as fine detail. The measure that catches it is **edge-per-ink** — how much outline
there is per unit of ink:

```
edge/ink  < 0.30   a few big solid shapes. Calm. What this style wants.
          ~ 0.40   the same ink broken into fine detail. Reads busy.
          > 0.60   almost all outline, almost no fill. Thin and floaty.
```

The companion measure is **solid-mass share** — the proportion of ink that is shape interior
rather than outline:

```
solid mass  > 70%   properly anchored
            ~ 60%   drifting toward detail
            < 40%   outline-only. Weak, regardless of how sparse it is.
```

Measured on four versions of the same portrait, the outline-only one had the *lowest* ink
coverage of all — 7.1%, comfortably inside the target band — and was still the weakest,
because only 30% of its ink was solid shape. **Coverage is not the measure.** A drawing can
be sparse and still fail. What it needs is ink consolidated into one or two solid masses.

Measured on two versions of the same portrait: 0.26 versus 0.41 at ~16% coverage each. The
fix for a busy drawing is never "use less ink" — it is *consolidate* the ink into larger
masses and delete the small stuff.

## Canvas

- **1:1 square**, 1040x1040 reference (any square size is fine; 1024 or 1200 are good).
- **Solid white background.** The measured source libraries ship transparent PNGs, but this
  project outputs white by default: transparent assets show as a checkerboard in most file
  viewers and vanish against dark backgrounds. If you specifically need to composite over a
  colour, ask for transparent and the rule flips — nothing else about the style changes.
- **Icons are the exception and stay transparent.** They overlay other surfaces, so a white
  ground would show as a box behind them.
- No frame, no border, no background scene, no ground plane, no horizon.

## Line quality

- Hand-drawn, **tapered** — strokes swell in the middle and thin at the ends, like a brush
  pen. This is the single biggest tell. Uniform monoline reads as a generic icon set.
- Slight wobble. Confident, not shaky. Drawn quickly by someone who can draw.
- Rounded ends. No sharp chisel terminals.
- Contours are open — lines break and leave gaps rather than sealing every shape.
- No hatching, no stippling, no texture, no shadow, no gradient, no outline-glow.

## Value structure

The contrast comes from three tones and nothing else:

1. **Solid black masses** — hair, trousers, skirts, shoes, one or two props.
2. **Opaque white** — shirts, tops, paper, main surfaces.
3. **Ink at ~20%** — skin (optionally), bags, secondary surfaces, inner planes.

A good composition has one or two large black masses anchoring it. Hair and legwear
usually carry that weight. Without a black mass the drawing goes weak and floaty.

## Accent marks

Small floating marks scattered near the figure — tiny filled dots, short dashes, and 2-3
tick lines near the head for energy or motion. Six to twelve of them, asymmetric, never a
neat pattern. They are the only decoration in the style.

## Text and symbols

"No text" needs one qualification, observed in the references:

- **No words, labels, captions or sentences.** Never.
- **A single symbol glyph on an object is fine** — a `$` on a money bag, an arrow on a sign.
  It reads as part of the drawn object, not as a caption.
- **Diagram nodes use `...` placeholder dots**, never real text. This is how the style draws
  a flowchart without lettering, and it is the correct move any time structure needs to be
  shown. Real labels live outside the artwork, set in actual type.

## Subject matter

Ordinary human moments, mostly work and daily life: reading, carrying, walking, typing,
talking, packing, waiting, thinking. Calm and friendly. Not absurd, not metaphorical, not
heroic. One or two figures, occasionally three.

## Sources and cross-source findings

The style family was sampled across several libraries. Two were measured directly:

| Library | Ink | Accent | Ink coverage | Linework |
|---|---|---|---|---|
| [Notioly](https://www.notioly.com/) — 13 PNGs measured | `#231F20` | none | 6-16% | tapered |
| [Open Doodles](https://www.opendoodles.com/) — 8 SVGs inspected | `#000000` | one (`#FF788F`) | 16-24% | tapered |

What they agree on, and what this spec therefore treats as load-bearing:

- **One ink dominates.** Never a full palette.
- **At most one accent**, and both libraries work fine with none.
- **The canvas is mostly empty** — 76-94% white across both.
- **Linework is filled paths, never strokes.** Every Open Doodles SVG carries
  `stroke="none"`; every line is a closed filled shape. This is verified in source, not
  inferred — see `icons-and-vector.md`.

Where they differ, and what this spec picks:

- **Ink colour.** Notioly's `#231F20` is warmer and reads less harsh than Open Doodles'
  `#000000`. This spec uses `#231F20`.
- **Accent.** Open Doodles allows one; Notioly uses none. This spec uses **none**, because
  a single ink is what makes a large set look like one hand.
- **Density.** Open Doodles runs heavier. This spec targets the sparser Notioly end.

## Never

- A second colour of any kind
- Pure `#000000`
- Gradients, drop shadows, textures, paper grain, noise
- Backgrounds, scenery, ground lines, framing boxes
- Uniform monoline stroke on an illustration (fine for icons only)
- Flat vector geometry, corporate memphis, blobby limbs, oversized heads
- Cute mascots, chibi proportions, kawaii faces
- 3D, isometric, skeuomorphic
- Words, labels, captions or sentences inside the artwork
