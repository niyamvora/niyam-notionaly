# Shot List

The shot list is the deliverable before any image exists. It is also the thing worth getting
right — a good shot list drawn adequately beats a bad shot list drawn beautifully.

## Choosing what to illustrate

Read the whole piece first. Then find the **cognitive anchors** — the places where the
reader's understanding turns. These earn a picture:

- The central claim, stated once
- A split: one thing becoming two, or a choice between paths
- A loop: output feeding back into input
- A before and after
- A sequence with a real handoff in it
- A common trap, and what it costs
- A change of state in the person doing the work
- One thing serving several purposes

These do **not**:

- A section heading, because it is a section heading
- A list of features
- A definition
- Anything the prose already states plainly in one sentence
- Anything needing a caption longer than the paragraph it sits under

**Do not space images evenly through the article.** Two illustrations in a dense argument and
none in the throat-clearing is correct. Even spacing is a sign you illustrated the layout
rather than the ideas.

## Count

| Piece | Images |
|---|---|
| Short post, under ~600 words | 1-3 |
| Normal article | 4-8 |
| Long piece, 3000+ words | up to 9 |

Nine is a ceiling, not a target. Enough is enough.

## Format

One row per image. Keep it terse — this is a plan, not a treatment.

```markdown
## Shot list — <article title>

### 01 · <short name>
- **Placement:** after the paragraph beginning "..."
- **Idea:** the one thing this image says, in one sentence without "and"
- **Structure:** one of the eight in `structures.md`
- **Figure:** what the person is physically doing
- **Props:** one or two, named
- **Caption:** the real text that will sit under the image
```

If the user only asked for a plan, deliver exactly this and stop.

## The idea line is the test

Write it in one sentence with no "and". If you need "and", it is two images — or, more often,
it is one image trying to explain a whole section and should be narrowed.

Bad: "the content pipeline and how review fits into it"
Good: "review is the step everything queues behind"

## Captions and labels

The artwork has no text in it. Ever. So the shot list carries the words, and they end up in
the article as real type.

- **Caption** — one line under the image, naming what it shows. Six to fourteen words. It
  names the picture; it does not explain it. If the caption is doing the explaining, the
  picture failed.
- **Node labels** — if a structure has parts that need naming, set them as real text beside
  or under the image, or draw `...` placeholder dots inside it the way the parent spec
  describes. Never letter them into the drawing.
- **No titles.** Do not put a title in the top-left corner of the image, or anywhere in it.
  The article already has headings.

## Chinese and other non-English articles

Captions and labels take the article's language. Everything else is unchanged.

- **Captions in Chinese**: write them in Chinese, set in real type outside the image.
  短、准、不解释 — six to fourteen characters is usually right.
- **The image prompt stays in English.** The style spec was measured and written in English
  and image models follow it far more reliably that way. A Chinese article gets an English
  prompt and a Chinese caption; nothing about the drawing changes.
- **Never put handwritten Chinese in the artwork.** Image models garble CJK glyphs badly —
  wrong strokes, invented characters — and the style has no room for lettering regardless.
  这一点没有例外：文字一律放在图外，用真实排版。
- The subject matter may need localising even when the structure does not. A commute, a desk,
  a meal, a shop front — draw what the article's reader actually does.

## Worked example

From an article arguing that teams lose time to handoffs, not to the work itself:

```markdown
### 03 · the queue at the handoff
- **Placement:** after "...the work was never the slow part."
- **Idea:** work piles up waiting to be passed on, not while being done
- **Structure:** flow
- **Figure:** holding out a stack of folders to someone who has not turned round yet
- **Props:** the stack, a second figure half-turned away
- **Caption:** 等待交接的时间，比做事的时间长
```

Note what is absent: no arrow labelled "handoff", no red highlight, no words in the picture.
The stack held out to a back that has not turned is the whole argument.
