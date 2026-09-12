# Calibration references are not included in this repo

The files that belong in these folders are **other people's artwork**. They are kept
locally for style calibration and are deliberately excluded from version control — see
`.gitignore` and `../../NOTICE.md`.

A fresh clone therefore has empty reference folders. The skill still works; it just cannot
*show* the model line quality, only describe it. The written spec in
`references/style-dna.md` was measured from these files and carries the numbers, so nothing
is lost from the specification itself.

## To populate them

Download a handful of Notion-style illustrations from [Notioly](https://www.notioly.com/)
(free packs exist) and drop them in by type:

```text
reference/
├── illustrations/   full scenes with figures
├── diagrams/        figures plus node or flow structures
├── icons/           single-object monoline icons
└── characters/      isolated figures, neutral poses
```

Five or six is plenty. A real `.svg` is worth more than any PNG, because it shows how the
paths are actually constructed.

**Calibration only.** Look at them to judge stroke feel, ink weight and spacing. Never copy
a composition, pose or prop into generated work. Style is not copyrightable; specific
compositions are.
