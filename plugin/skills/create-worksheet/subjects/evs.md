# EVS — Subject Guide

Environmental Studies for Class III CBSE. Covers plants, animals, food, water, air, family, home, neighbourhood, festivals, transport, body parts and hygiene across the year.

## Known chapters (syllabus)

Update this list as new chapters come up. Each chapter has (or will have) a folder at `worksheets/EVS/Chapter - <Name>/`.

| Chapter | Status | Folder |
|---|---|---|
| Plants Around Us | ✅ Covered (Q1 2026-27) | `EVS/Chapter - Plants Around Us/` |

## Content sources for each chapter

When the user asks for a new EVS worksheet, first check:

1. `worksheets/EVS/Chapter - <Name>/Source Notes - <Name>.docx` — our chapter notes (Q&A + key concepts + key words + topic map)
2. `worksheets/EVS/Chapter - <Name>/source-images/` — WhatsApp photos of the notebook + textbook pages the user has shared
3. `sources/reference-samples/` — any external reference samples

If source material exists, base the worksheet strictly on those concepts. Do not pull outside content.

## Recommended question mix (default)

When subject+chapter are given but type breakdown isn't, use this as the default for EVS:

- **Section A**: 10 fill-in-the-blanks (each 1 mark) — factual recall
- **Section B**: 20 MCQs (each 1 mark) — understanding
- Total: **30 marks**, fits on one page with our tight layout.

Alternative "practice sheet" style (closer to school format):
- Fill-ups (5-6), Match (5-6), MCQs (5), Short answer or One-word (5), optional Draw/Label.

## EVS-specific question types that work well

- **Odd one out** (e.g., "Which one is not a tree: Rose, Mint, Banyan, Pumpkin")
- **Classify list** — plant/animal categorisation
- **Label diagram** — parts of a plant, parts of a flower, parts of a tree
- **Identify from illustration** — trees vs shrubs vs herbs vs climbers vs creepers
- **Draw & label** — seed germination stages, water cycle, food chain

## Reusable illustration assets (Plants)

The following PNG + SVG illustrations exist at `EVS/Chapter - Plants Around Us/assets/` and are reusable in any worksheet:

| Asset | Use in |
|---|---|
| `tree.png` | Identify the type of plant (tree image) |
| `shrub.png` | Identify the type of plant (shrub image) |
| `herb.png` | Identify the type of plant (herb image) |
| `climber.png` | Identify the type of plant (climber image) |
| `creeper.png` | Identify the type of plant (creeper image) |
| `labeled_plant.png` | Label the parts of a plant (diagram with 5 empty label boxes pointing to flower/leaves/fruit/stem/root) |

Recommended dimensions when embedding (width × height in points):
- Tree: 110 × 145
- Shrub: 170 × 145
- Herb: 140 × 140
- Climber: 120 × 160
- Creeper: 210 × 125
- Labeled plant (full diagram): 430 × 356

## Plants Around Us — topic map (for worksheet composition)

The chapter breaks into these sub-topics. A full-chapter worksheet should touch most of them:

1. Different kinds of plants — trees, shrubs, herbs, climbers, creepers
2. Parts of a plant — root, stem, leaf, flower, fruit (plus tree: trunk, bark, branches)
3. Sun and plants — why sunlight matters
4. Seeds and germination — what a seed needs, seedling
5. Photosynthesis — leaves as "kitchen of the plant", chlorophyll
6. Flowers → fruits → seeds
7. Taking care of plants — water, sunlight, nutrients, love
8. Kitchen garden — what, why, benefits
9. Saving paper — environmental value

Key-word list is available in `Source Notes - Plants Around Us.docx`.

### Known textbook facts students should know
- Rafflesia = world's largest flower
- Coconut tree = "tree of life"
- Sunflower turns its head to follow the sun
- Stomata = tiny pores on leaves
- Chlorophyll = green pigment in leaves

## Folder conventions

```
EVS/
└── Chapter - <Chapter Name>/
    ├── Source Notes - <Chapter Name>.docx     # Chapter content reference
    ├── source-images/                          # Original notebook/textbook photos
    ├── Worksheet 1 - <Short Title>.docx
    ├── Worksheet 2 - <Short Title>.docx
    └── ...
```

Pick the next worksheet number by `ls` on the folder.
