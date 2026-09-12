# Assets

## `reference/` — calibration only

Real Notioly assets, kept so the model can *see* line quality, ink weight and spacing
rather than only read about them. See `../NOTICE.md` for terms.

**Look at these to judge style. Never copy a composition, pose or prop from them.**

| Folder | Holds | Currently |
|---|---|---|
| `reference/illustrations/` | Full scenes with figures | 5 |
| `reference/diagrams/` | Figures plus node/flow structures | 1 |
| `reference/icons/` | Single-object monoline icons | empty |
| `reference/characters/` | Isolated figures, neutral poses | empty |

### What each reference demonstrates

| File | Why it is here |
|---|---|
| `illustrations/01-pair-walking.png` | Two figures overlapping; opposite value schemes; mid-stride |
| `illustrations/02-pushing-pram.png` | Figure plus large prop; 20%-ink tints on bag and wheels |
| `illustrations/03-teaching-child-to-ride-bike.png` | Adult and child overlapping; heavy black legwear anchor |
| `illustrations/04-walking-with-two-bags.png` | Mid-stride with trailing leg; motion dashes; white props |
| `illustrations/05-money-flying-away.png` | 20% ink on skin and prop; a single symbol glyph on an object |
| `diagrams/01-two-people-node-diagram.png` | **The closest thing to an infographic in the set.** Nodes use `...` placeholder dots instead of real text; figures sit at opposite corners framing the structure |

### Filling the empty folders

The highest-value thing to add is a real Notioly **`.svg`**, which shows how the paths are
actually constructed — something the PNGs cannot. Free packs exist; drop one into the
matching folder and the vector guidance can be tightened against fact.

Add references only in **this** style. Mixing in other sites' "Notion-style" work dilutes
the spec and makes output less consistent. A genuinely different look belongs in its own
sibling skill folder, not in here.

## Output does not live here

Generated assets go into the **workspace**, never into the skill folder — the skill is
copied to `~/.codex/skills/` on every install and should stay small.

```text
examples/
├── characters/     figures and scenes
├── icons/          single-object monoline, 24px grid
├── spots/          objects and props
├── explorations/   cross-tool prompt tests, grouped by generator
└── infographics/   composed pages (see niyam-notionaly-infographic)
```
