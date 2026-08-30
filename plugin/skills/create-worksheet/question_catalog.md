# Question Catalogue

Every question type supported by `worksheet_builder.js`. Use this as the reference when composing a new worksheet. All renderers return `Paragraph` or `Table` objects you push into the `children` array.

---

## 1. Fill in the blanks — `B.fillItem(idx, parts)`

Each item is a list of text fragments with blanks inserted between them.

```javascript
B.fillItem(1, ["Big, tall and strong plants are called ", "."])
// renders: 1. Big, tall and strong plants are called  _______________ .

B.fillItem(2, ["A seed needs ", ", ", " and ", " to germinate."])
// renders: 2. A seed needs _______ , _______ and _______ to germinate.
```

Use for: vocabulary recall, single-word factual answers, notebook-style answers turned into cloze.

---

## 2. Multiple Choice — `B.mcqBlock(idx, question, options)`

Returns `[questionPara, optionsTable]` — push both.

```javascript
const [q, t] = B.mcqBlock(1, "Which of these is a tree?",
                          ["Rose", "Mint", "Neem", "Watermelon"]);
children.push(q, t);
```

Renders as a 2×2 option grid, 4 options (a, b, c, d).

Use for: testing understanding, distinguishing similar concepts.

---

## 3. Match the following — `B.matchTable(left, right, colA?, colB?)`

```javascript
B.matchTable(
  [ { n: 1, text: "Trunk" }, { n: 2, text: "Chlorophyll" } ],
  [ { letter: "a", text: "Green pigment in leaves" },
    { letter: "b", text: "Thick main stem of a tree" } ]
);
```

Produces a 2-column bordered table with shaded header row. Use different letter order for the right column so students must think.

Custom column names (optional): `B.matchTable(left, right, "Plant", "Type")`.

---

## 4. True / False — `B.tfItem(idx, statement)`

```javascript
B.tfItem(1, "A rose plant is a herb.");
// renders: 1. A rose plant is a herb.   ( )
```

Use for: concept verification, myth-busting.

---

## 5. Odd one out — `B.oddOneOut(idx, options)`

```javascript
B.oddOneOut(1, ["Rose", "Mint", "Spinach", "Coriander"]);
// renders: 1. Rose  •  Mint  •  Spinach  •  Coriander
```

Use for: classification reasoning (students circle the odd one).

---

## 6. One-word answer — `B.oneWordItem(idx, question)`

Inline Q+answer line on the same row (compact).

```javascript
B.oneWordItem(1, "Which tree is known as the tree of life?");
// renders: 1. Which tree is known as the tree of life?  Ans. _______________
```

Use for: rapid-fire factual recall.

---

## 7. Short answer — `B.shortQuestion(idx, question)` + `B.answerLine()`

Question on one line, followed by 1–3 blank answer lines.

```javascript
children.push(B.shortQuestion(1, "Why should we not waste paper?"));
children.push(B.answerLine());
// for a two-line answer, push answerLine() twice
```

Use for: "answer in one sentence" style questions, definitions.

---

## 8. Name the part — use `B.fillItem` with a clue phrasing

There is no separate renderer; phrase the clue as the prompt and place the blank at the end.

```javascript
B.fillItem(1, ["I stay below the ground and drink water from the soil. I am the ", "."])
// 1. I stay below the ground and drink water from the soil. I am the _______________ .
```

Use for: playful identification questions ("I am…" format).

---

## 9. Label a diagram — image + on-image label boxes

No code rendering — the diagram itself (PNG) has empty label boxes drawn in. Create the image separately (e.g., an SVG converted to PNG with `ImageMagick convert`), place it in a folder, and embed with:

```javascript
new ImageRun({
  type: "png",
  data: fs.readFileSync("/path/to/labeled_plant.png"),
  transformation: { width: 430, height: 380 },
  altText: { title: "plant", description: "plant to label", name: "plant" }
})
```

For Plants: `labeled_plant.png` (with 5 blank ovals for flower/leaves/fruit/stem/root) is in `EVS/Chapter - Plants Around Us/source-images/` or can be regenerated from `outputs/plants_svg/*.svg`.

---

## 10. Identify from illustration — `B.imageRow(items)`

Row of plant/object illustrations with answer line beneath each.

```javascript
B.imageRow([
  { imgPath: "/path/tree.png", imgW: 110, imgH: 145 },
  { imgPath: "/path/shrub.png", imgW: 170, imgH: 145 },
  { imgPath: "/path/herb.png", imgW: 140, imgH: 140 },
  { imgPath: "/path/climber.png", imgW: 120, imgH: 160 },
  { imgPath: "/path/creeper.png", imgW: 210, imgH: 125 }
]);
```

Use for: "identify the type of X" questions (plant types, shapes, grammatical categories, etc.).

---

## 11. Draw and label — `B.drawBoxRow(labels, heightDxa?)`

Empty bordered boxes for students to draw inside.

```javascript
B.drawBoxRow(["Stage 1: Seed", "Stage 2: Seedling", "Stage 3: Young plant"], 3200);
// 3 big boxes, each ~2 inches tall. Use 900 if sharing a page with other content.
```

Use for: drawing stages, labelled diagrams, charts.

---

## 12. Sort into groups — `B.sortChart(groups, writingLines?)`

Table with headers per group and guide lines inside each column.

```javascript
B.sortChart(["Tree", "Shrub", "Herb", "Climber", "Creeper"], 6);
```

Use for: categorisation exercises. Often paired with a word bank in the instruction.

---

## 13. Classify list — `B.classifyList(items, cols?)`

Two-column list of terms with blank lines next to each for students to fill the category.

```javascript
B.classifyList([
  { name: "Neem" }, { name: "Rose" }, { name: "Mint" },
  { name: "Money plant" }, { name: "Watermelon" }, { name: "Mango" }
], 2);
```

Use for: "write the type next to each" style questions.

---

## Quick-reference table

| Need | Renderer |
|---|---|
| Fill in the blanks | `fillItem` |
| 4-option MCQ | `mcqBlock` |
| Match the following | `matchTable` |
| True/False | `tfItem` |
| Odd one out | `oddOneOut` |
| One-word answer (inline) | `oneWordItem` |
| Short answer (1-3 lines) | `shortQuestion` + `answerLine` |
| Clue-based naming | `fillItem` (with clue phrasing) |
| Image identification row | `imageRow` |
| Draw & label stages | `drawBoxRow` |
| Sort into categories | `sortChart` |
| Classify a list | `classifyList` |

---

## Composing a worksheet

A typical Class III practice sheet mixes 4–6 question types. Recommended counts:

- **EVS practice sheet**: 1 fill-up section (6–10), 1 MCQ section (5–10), 1 match (5–6 pairs), 1 short-answer or one-word (5), optional 1 draw/label.
- **Hindi practice sheet**: 1 गद्यांश (comprehension passage + MCQs + vilom), 1 matra-fill section (4–8), 1 vyanjan classify or sort, 1 T/F, 1 short answer. See `subjects/hindi.md`.

Keep total marks between **20–40** so the worksheet fits 1–2 pages.
