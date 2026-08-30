# Difficulty Levels — Guide

Three calibration levels. A single request for a *"3-sheet set"* or *"set of three"* produces all three as separate files.

| Level | Label | Mix | Use case |
|---|---|---|---|
| **1** | *Textbook* | Mostly direct recall; mirrors school's own practice sheets | First pass after chapter is taught |
| **2** | *Mixed* | ~70% recall + ~20% understanding/application + ~10% HOTS | Standard practice (default if unstated) |
| **3** | *Stretch* | Fewer recall; more application, reasoning, HOTS | Confidence-builder before tests |

## How each level changes each question type

### Fill in the blanks
- **L1**: Direct restatement from the notebook. One simple blank per sentence.
  *e.g. "Big, tall and strong plants are called **\_\_\_\_**."*
- **L2**: Same but with 2 blanks per sentence or a slight twist.
  *e.g. "Plants with \_\_\_\_ stems that need the \_\_\_\_ of a wall are called climbers."*
- **L3**: Apply the concept rather than restate.
  *e.g. "A plant's \_\_\_\_ absorbs water from the soil — because \_\_\_\_."*

### MCQs
- **L1**: Distractors are obviously wrong.
  *e.g. "Which of these is a tree? (a) Rose (b) Mint (c) Neem (d) Watermelon"*
- **L2**: Distractors are plausible; requires understanding.
  *e.g. "Which of these is a tree? (a) Cotton (b) Neem (c) Rose plant (d) Tulsi"*
- **L3**: Reasoning / HOTS.
  *e.g. "Which plant would be best for a kitchen garden on a small balcony? (a) Mango (b) Mint (c) Banyan (d) Coconut"*

### Match the following
- **L1**: Direct 1:1 term → definition pairs straight from notebook.
- **L2**: Mix terms and facts, requires understanding connections.
- **L3**: Real-world application pairs (e.g., "plant → where you'd find it", "plant part → what happens if it's damaged").

### True / False
- **L1**: Clear-cut factual T/F.
- **L2**: Subtle wording that requires careful reading.
- **L3**: Statements requiring inference from concepts.

### Short answer
- **L1**: Repeat a definition from the notebook.
- **L2**: Explain a concept in one's own words.
- **L3**: "Why?" / "What would happen if?" / "How is X different from Y?"

### One-word / name the part
- **L1**: Directly testable from notebook.
- **L2**: Requires connecting two facts (e.g., "Which plant has weak stems AND grows along the ground?").
- **L3**: Real-world example (e.g., "Name a tree that is called the tree of life.").

## Recommended question mix per level

| Question type | L1 count | L2 count | L3 count |
|---|---|---|---|
| Fill in the blanks | 8 | 6 | 4 |
| MCQs (4-option) | 8 | 8 | 6 |
| Match the following | 1 section (6 pairs) | 1 section (6 pairs) | 1 section (5 pairs) |
| True / False | — | 4 | 4 |
| One-word / Name the part | — | 4 | 4 |
| Short answer | — | — | 4 |
| Odd one out | — | 2 | 4 |
| HOTS / reasoning | — | 1 | 3 |

Target total marks: ~25–30 per sheet.

## Workflow for a 3-sheet set

When user says *"create a 3-sheet difficulty set on <chapter>"* or *"3 practice sheets on <chapter>"*:

1. Read chapter source (notebook photos + source notes + known textbook facts).
2. Brainstorm the question pool first (4× the questions you'll actually use).
3. Triage each pooled question into L1/L2/L3 based on cognitive demand.
4. Assemble three separate children arrays with the mix above.
5. Write 3 `.docx` files, each using `titleBlock(..., "Worksheet N (L1 Textbook)")` etc.
6. File names:
   - `Worksheet N (L1 Textbook) - <Title>.docx`
   - `Worksheet N (L2 Mixed) - <Title>.docx`
   - `Worksheet N (L3 Stretch) - <Title>.docx`

Return all three `computer://` links in the final message.
