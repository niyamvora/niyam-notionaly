---
name: niyam-notionaly-article
description: Illustrate a whole article, blog post, newsletter, Notion page or methodology doc with a coherent set of monochrome Notion-style illustrations — pick which passages deserve art, produce a shot list, then generate each image. Use when the user asks to illustrate an article or post, add body illustrations to a doc, suggest where a piece needs images, produce a shot list, draw a concept/flow/before-after/process as a picture, or illustrate a set rather than one asset. Works for English and Chinese articles. 也用于中文文章配图：为中文文章、帖子、博客、Notion 文档、方法论、流程或观点生成正文配图、文章插图、配图建议和 shot list；输出是 Notionaly 单色手绘风格，不是红橙蓝手写批注风格。
---

# Article Illustration

Turn a piece of writing into a **set** of illustrations that belong together: choose the
passages worth illustrating, describe each shot, then draw them in the Notionaly style.

The parent skill `niyam-notionaly-illustrations` owns the style. This skill owns **what to
draw and where it goes**. Never restate the style spec here — read it from the parent.

## The rule that shapes everything

**A body illustration is not decoration for a paragraph. It is one idea from the article,
drawn as a person doing something.**

If the picture could be swapped for any other picture in the set without the article
reading differently, it was decoration. Cut it.

## Read as needed

- `references/shot-list.md` — digesting the piece, choosing anchors, the shot-list format,
  and how captions and labels work (including Chinese).
- `references/structures.md` — the eight structures, how to turn an abstract claim into a
  physical action, and the no-repeats rule.
- `references/prompt-template.md` — the 16:9 body-illustration prompt and edit prompts.
- `references/qa-checklist.md` — **set-level** checks. Per-asset checks live in the parent.

From the parent skill, which installs alongside this one as
`niyam-notionaly-illustrations` (in this repo, `skill/`):

- `niyam-notionaly-illustrations` → `references/style-dna.md` — the measured spec.
  Non-negotiable.
- `niyam-notionaly-illustrations` → `references/characters.md` — how to lock a figure so it
  stays the same person across a set.
- `niyam-notionaly-illustrations` → `references/qa-checklist.md` — run this on **every**
  image, including the runnable ink measurement.

## Where the words go

The Notionaly style carries **no text inside the artwork**. That is not a limitation to work
around — it is the thing that makes a set look like one hand.

So every label the article needs lives **outside** the image, in real type:

| Wanted | Put it |
|---|---|
| A caption under the image | In the markdown / HTML, as real text |
| A name on a step or node | Real text beside the image, or `...` placeholder dots inside it |
| Emphasis, a warning, a result | In the prose. The drawing carries it by posture and composition |

A structure that cannot be read without words written on it is too complicated. Simplify the
structure until the picture works wordlessly and the caption merely names it.

**Chinese articles work exactly the same way.** Captions and labels are written in Chinese,
set in real type outside the image. Do not put handwritten Chinese into the artwork — image
models garble CJK glyphs, and the style has no room for lettering regardless. Write the
image prompt itself in English even for a Chinese article; the spec was measured in English
and models follow it more reliably. See `references/shot-list.md`.

## Workflow

### 1. Digest the piece

Read the article, link, Notion page, markdown file or pasted text in full. Pull out:

- The central claim.
- The passages where the reader's understanding actually turns.
- What is better left as prose. Most of it.

Do not illustrate evenly. Illustrate the **cognitive anchors** — a core judgement, a split, a
loop, a before and after, a path, a common trap, a change of state.

### 2. Shot list first

If the user asked what to illustrate, or where a piece needs images, stop here and deliver
the shot list. Format in `references/shot-list.md`. One row per image:

placement · idea · structure · what the figure does · props · caption

**Four to eight images** for a normal article. One to three for a short post. Nine is a lot;
past that you are making a picture book, not illustrating an argument.

### 3. Generate

If the user asked to generate, illustrate, draw or make them — do it, do not stop to confirm
the shot list.

Hand each shot to the parent skill's raster pipeline using
`references/prompt-template.md`. **One image per call.** Never tile several onto one canvas.

Lock the figure before the first call and restate those five attributes verbatim in every
prompt — hair silhouette, skin value, top, bottom, one accessory. Models do not remember a
character between calls, and a set where the person changes hair halfway reads as stock art.

### 4. Check

Run the parent's `references/qa-checklist.md` on each image — including the ink measurement,
not an eyeball. Then run this skill's `references/qa-checklist.md` across the set.

### 5. Deliver

Save into the **workspace**, never into a skill folder:

```text
examples/articles/<article-slug>/
├── 01-<topic>.png
├── 02-<topic>.png
└── shot-list.md
```

Number in reading order. Never overwrite an existing asset unless asked.

Report: how many, where each one goes in the article, the path, which are strongest and
which are optional. Show the work — do not lecture about the style.

## Defaults

| Unstated | Default |
|---|---|
| Canvas | 16:9 landscape, 1600x900 |
| Count | 4-8 for an article, 1-3 for a short post |
| Format | PNG |
| Figures | One, the same person throughout |
| Caption language | The article's language |
| Prompt language | English, always |

16:9 is this skill's default because body illustrations sit in a text column. Aspect is not
one of the parent's four non-negotiables — one ink, sparse, tapered strokes and solid black
masses are, and they hold at every canvas size.

## Do not

- Write text, labels or handwriting inside the artwork
- Add colour to mark a flow, a warning or a result — the style has one ink
- Reuse a metaphor, prop or composition from an earlier image in the set
- Let the figure stand beside the idea instead of performing it
- Illustrate every section because it is there
- Build a flow chart, a slide or a formal diagram — for those, use
  **`niyam-notionaly-infographic`**, which composes real HTML with real type
- Change the character's hair, clothing or accessory between images in one set
