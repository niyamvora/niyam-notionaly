# Notice

## What this project is

An original specification for drawing in a monochrome, hand-drawn illustration style,
written by **measuring published work across several libraries** rather than by copying any
of them: ink sampled from pixels, tints confirmed as alpha variants, canvas and coverage
measured, and SVG sources inspected to see how the linework is actually constructed.

The numbers in [`references/style-dna.md`](references/style-dna.md) are observations about a
visual style. Visual style is not copyrightable; specific compositions are. This project
describes the former and tells you repeatedly not to reproduce the latter.

## Sources studied

No single library is the source of this spec. These were sampled, measured or consulted
while writing it, and all are worth your time in their own right:

| Library | By | Notes |
|---|---|---|
| [Notioly](https://www.notioly.com/) | Zahra Amiri | Notion-style; 13 assets measured. Free with attribution |
| [Open Doodles](https://www.opendoodles.com/) | Pablo Stanley | CC0 public domain; 8 SVG sources inspected |
| [Absurd Design](https://absurd.design/) | Diana Valeanu | Hand-drawn black-and-white, surreal |
| [Overflow Design](https://www.overflow.design/) | — | Hand-drawn illustrations and icons |
| [DrawKit](https://www.drawkit.com/) | James Daly | Includes monochrome hand-drawn packs |
| [Łukasz Adam](https://lukaszadam.com/illustrations) | Łukasz Adam | Free monochrome line illustrations |

Where these libraries disagree — ink colour, whether to allow one accent, how dense to draw
— `style-dna.md` records the difference and states which convention this project follows and
why. Each library's own assets remain under its own licence.

## Calibration references

`skill/assets/reference/` is for a small number of real illustrations, used to let the model
*see* line quality rather than only read about it.

**Those files are not included in this repository.** They are other people's artwork and are
excluded via `.gitignore`. See [`assets/reference/FETCH.md`](assets/reference/FETCH.md) for
how to add your own, under whatever terms the source sets.

Calibration only. Never trace, copy or reproduce a reference composition in generated work.

## Not affiliated

Not affiliated with, endorsed by, or connected to Notion Labs, Inc., Notioly, or any library
listed above. "Notion" is a trademark of Notion Labs, Inc., used here only descriptively, to
name the visual family this project targets.
