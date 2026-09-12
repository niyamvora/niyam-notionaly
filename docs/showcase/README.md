# Showcase

A real before-and-after: a personal photograph put through
`niyam-notionaly-illustrations`.

| File | What it is |
|---|---|
| `portrait-reference.jpg` | The source photograph. Resized web copy, cropped, metadata stripped |
| `portrait-notionaly-monochrome.png` | The on-spec result — one ink, no colour |
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

| File | Ink coverage | Chromatic pixels | Spec |
|---|---|---|---|
| `portrait-notionaly-monochrome.png` | 18.9% | **0.0%** | Passes the one-ink rule; slightly denser than the 6–16% band |
| `portrait-notionaly-color.png` | 25.7% | **9.1%** | Fails — the spec permits no colour in artwork, ever |

The colour version is kept deliberately, as a counter-example. A portrait containing a full
table of food is naturally denser than the single-figure scenes the coverage band was
measured from, which is why the monochrome result sits a little above it and still reads
correctly.

The full-resolution original is **not in this repository** and is not tracked by Git.
