---
name: niyam-notionly-illustrations
description: Generate Notion-style (Notioly-style) illustrations, characters, icons and spot marks — strictly monochrome hand-drawn line art in one warm near-black ink on a transparent background. Use when the user asks for Notion-style or Notioly-style illustrations, line-art characters, minimal monoline icons, template or landing-page artwork, empty-state graphics, avatars, or an SVG/PNG illustration asset in that clean hand-drawn productivity-app look. Also use when the user wants a copy-paste prompt to generate such art in ChatGPT, Gemini or Claude.
---

# Notion-Style Illustrations

Make illustration assets in the Notioly / Notion look: one warm near-black ink, hand-drawn
tapered linework, solid black hair and legwear against white garments, an almost empty
canvas, transparent background.

The style is narrow on purpose. Its whole value is that every asset looks like it came from
the same hand. Do not improvise on the spec.

## Read as needed

Do not load everything at once.

- `references/style-dna.md` — the measured spec. **Always read this first.**
- `references/characters.md` — proportions, faces, hair, clothing, reuse.
- `references/composition-patterns.md` — asset types and composition patterns.
- `references/prompt-template.md` — raster generation template and edit prompts.
- `references/icons-and-vector.md` — icon spec, tapered SVG technique, PNG→SVG tracing.
- `references/subject-prompts.md` — worked, ready-filled prompts for common subjects.
- `references/portable-prompts.md` — self-contained prompts for ChatGPT/Gemini/Claude web.
- `references/qa-checklist.md` — checks before delivery, including a measurable ink test.
- `assets/README.md` — what each reference demonstrates and where output belongs.
- `assets/taper.py` — tapered-path generator for hand-authored SVG. Use it rather than
  computing beziers by hand; run `python3 taper.py` for its self-check.
- `assets/reference/` — real Notioly assets for line-quality calibration only, split into
  `illustrations/`, `diagrams/`, `icons/`, `characters/`. Look at them to judge stroke feel
  and spacing. **Never copy a composition, pose or prop from them.**

## The four non-negotiables

Everything else is detail. These four are what make or break it:

1. **One ink.** `#231F20` and white. No colour, ever. Greys are that ink at ~20% opacity.
2. **Sparse.** Ink covers about 10% of the canvas. Subject ~60% of frame, centred, big margins.
3. **Tapered strokes.** Brush-pen linework that swells and thins. Not uniform monoline.
4. **Solid black masses.** Hair and trousers carry the weight. Garments stay white.

## Workflow

### 1. Settle four things before drawing

- **Asset type** — `illustration`, `character`, `icon`, or `spot`.
- **Format** — SVG or PNG. If unstated, infer: icons and spots default to SVG,
  illustrations to PNG, anything described as editable/scalable/Figma-bound to SVG.
- **Subject** — one ordinary action, expressible in one sentence without "and".
- **Where it will be used** — Notion page, website, Figma, deck. This decides the format
  (Notion will not render uploaded SVG; ship PNG there).

Ask only if genuinely ambiguous. Otherwise pick the sensible default and say what you picked.

### 2. If the user wants a prompt, not an image

When they ask for something to paste into ChatGPT, Gemini or Claude, go straight to
`references/portable-prompts.md` and hand back the right prompt **verbatim in a code block**
with the subject filled in. Do not paraphrase the spec — the specific numbers are what make
it work. Pick the right one for the tool: Claude cannot generate raster images, so give it
the SVG prompt.

### 3. Generating

**Raster** — use `image_gen` with the template in `references/prompt-template.md`. One asset
per call. Never combine several into one canvas. Request a transparent background.

**Vector** — follow `references/icons-and-vector.md`:
- Icons and spots: hand-author the SVG. Monoline is correct at icon scale.
- Characters: hand-author using the tapered filled-path technique.
- Full illustrations: generate a PNG, then trace it with potrace. Say that is what you did —
  never present a PNG as a vector.

For a set, lock the character description and restate it verbatim in every prompt. Models do
not remember a character between calls.

### 4. Check

Run `references/qa-checklist.md`. For raster output, actually run the ink-measurement
snippet rather than eyeballing it — colour creep and over-density are the two most common
failures and both are measurable.

Iterate in the order that file gives. Colour first, density second.

### 5. Deliver

Save into the **workspace**, never into the skill folder, split by asset type:

```text
examples/
├── characters/     figures and scenes
├── icons/          single-object monoline, 24px grid
├── spots/          objects and props
└── explorations/   cross-tool prompt tests, grouped by generator
```

Name sequentially and descriptively: `characters/01-reading-in-chair.png`,
`icons/calendar.svg`. Create only the folders you actually use.

Never mix another style's output into this tree. This skill draws one style and only one;
a different look belongs in a different skill with its own spec and its own output folder. Never overwrite an existing
asset unless asked.

Report: what was made, the format, the path, and which ones are strongest. Keep it short —
show the work, do not lecture about the style.

## Composing a page

For an infographic, data poster, slide or social card, use the companion skill
**`niyam-notionly-infographic`** (nested at `infographic/`). It composes real HTML with real
type and calls this skill for its artwork. Do not build one by generating a single image —
text and numbers garble.

## Defaults

| Unstated | Default |
|---|---|
| Asset type | `illustration` |
| Format | PNG for illustrations, SVG for icons/spots/characters |
| Canvas | 1:1 square, 1024x1024 |
| Background | Transparent |
| Figures | One |
| Count | One asset, unless a set was asked for |

## Do not

- Add colour "just as an accent"
- Use `#000000`
- Add a background, ground line or frame
- Put text or labels inside the artwork
- Copy a composition, pose or prop from anything in `assets/reference/`
- Present a raster PNG as SVG
- Draw mascots, chibi proportions or corporate-memphis figures
