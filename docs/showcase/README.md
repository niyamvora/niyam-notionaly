# Showcase

A real before-and-after: a personal photograph put through
`niyam-notionaly-illustrations`.

| File | What it is |
|---|---|
| `portrait-reference.jpg` | The source photograph. Resized web copy, cropped, metadata stripped |
| `portrait-notionaly-chatgpt.png` | ChatGPT, from the redraw-a-photo prompt (worked subject 9). Downloaded transparent; white ground added afterwards, which is why that prompt now asks for white directly |
| `portrait-notionaly-codex.png` | Codex, same prompt. Flattened to white here |
| `portrait-notionaly-outline.png` | Outline only — no solid masses. Sparsest of all and still the weakest |
| `portrait-notionaly-monochrome.png` | An earlier take — same ink, more fine detail |
| `portrait-notionaly-color.png` | The same portrait with the one-ink rule deliberately broken |

## Licence — this folder is excluded

**The images in this folder are NOT covered by the repository's MIT licence and are not
reusable assets.**

`portrait-reference.jpg` is a personal reference photo shared by the repository author. The
two derived portraits depict a real, identifiable person. All rights reserved; they are here
to demonstrate the skill's output and for no other purpose.

Do not reuse, redistribute, retrain on, or repurpose them. Everything else in this
repository is MIT and free to use.

## Measured against the spec

| File | Ink | Chromatic | Edge/ink | Verdict |
|---|---|---|---|---|
| `portrait-notionaly-chatgpt.png` | 16.5% | **0.0%** | **0.26** | On-spec. Ink well consolidated into solid masses |
| `portrait-notionaly-codex.png` | 10.6% | **0.0%** | 0.34 | On-spec. Closest to the ~10% coverage the prompt asks for |
| `portrait-notionaly-outline.png` | 7.1% | **0.0%** | 0.70 | Sparsest of all and still weakest — only 30% solid mass |
| `portrait-notionaly-monochrome.png` | 16.0% | **0.0%** | 0.41 | Same ink, scattered as fine detail. Reads busier |
| `portrait-notionaly-color.png` | 16.7% | **9.1%** | 0.39 | Fails — the spec permits no colour in artwork, ever |

Edge-per-ink is the useful number here. The first two are within half a percent on coverage,
yet clearly different to look at: the same quantity of ink in a few big shapes versus spread
across small detail.

The colour version is kept deliberately, as a counter-example. A portrait containing a full
table of food is naturally denser than the single-figure scenes the coverage band was
measured from, which is why the monochrome result sits a little above it and still reads
correctly.

The full-resolution original is **not in this repository** and is not tracked by Git.
