# Math — Subject Guide (stub)

CBSE Class III Math. Numbers, operations, shapes, measurement, money, time.

## Known chapters (syllabus) — to be filled as covered

| Chapter / Topic | Status | Folder |
|---|---|---|
| (none yet) | — | — |

## Math-specific question types

- **Straight computation** — number sentences to solve (2+3=?, 47 - 29 =?)
- **Word problems** — Class III level: "Ambar has 24 apples, gives 9 away, how many left?"
- **Missing number** — `3 + __ = 10`, `12 × __ = 24`
- **Ordering / comparing** — arrange smallest→largest, insert `<`, `>`, `=`
- **Number names** — write in words / figures
- **Place value** — tens, hundreds, thousands
- **Match** — shape ↔ name, time ↔ clock face, money ↔ value
- **Fill the number pattern** — 2, 4, 6, __, __
- **Geometry** — identify shapes, count sides/corners
- **Measurement** — cm/m, grams/kg, litres, time (hours/minutes)
- **Draw** — a clock showing 3:30, a square of 5 cm, etc.

## Math-specific rendering notes

- Numbers and math expressions **render well in Calibri**. No special font needed.
- Use **monospace for aligned sums** if doing vertical addition/subtraction:

```
   4 7
 - 2 9
 -----
```

For this, override the run font inline: `new TextRun({ text: "...", font: "Consolas", size: 24 })`.

- **Number lines** — can draw with ASCII-art or as simple SVG.
- **Clocks / shapes** — embed as images (create SVG → PNG like we did for plants).

## Default question mix (practice sheet)

| Q | Type | Marks |
|---|---|---|
| Q1 | Addition / subtraction sums | 5 |
| Q2 | Missing numbers (fill) | 5 |
| Q3 | Word problems | 6 (2 marks × 3) |
| Q4 | Place value | 4 |
| Q5 | Shapes — identify & count sides | 3 |
| Q6 | Compare using >, <, = | 3 |

Total: ~26 marks.

## Content sourcing

- Primary: notebook/textbook photos
- Textbook: typically *Math-Magic 3* (NCERT) or similar

## Folder conventions

```
Math/
└── Chapter - <Chapter Name>/
    ├── Source Notes - <Chapter Name>.docx
    ├── source-images/
    └── Worksheet 1 - <Short Title>.docx
```

## TODO

- Fill in chapter list once syllabus is known
- Build number-line / clock SVG templates if needed
- Decide on vertical-sum rendering approach (inline monospace vs image)
