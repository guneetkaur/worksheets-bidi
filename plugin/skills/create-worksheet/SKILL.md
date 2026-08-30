---
name: create-worksheet
description: Generate CBSE Class III worksheets (practice sheets, revision sheets, or weekly tests) for Ambar. Use whenever the user asks to create, draft, make, build, or design a worksheet, practice sheet, revision sheet, test paper, or assessment for any subject (EVS, Hindi, English, Math, Science, GK, Computer, etc.). Triggers on "worksheet on X", "practice questions for Y", "make a test on Z", "fill-in-the-blanks for...", "MCQs for...", "3-sheet difficulty set", "revision sheet", "weekly test". Skill knows the student (Ambar, Class III, CBSE), locked visual style, and a full catalogue of question types that flex by chapter + difficulty level. Also supports syllabus-progress tracking and a mistake-journal workflow to target weak topics.
---

# create-worksheet — Ambar's Worksheet Generator

This skill produces **printable .docx worksheets** for Ambar, Class III CBSE. It wraps the visual style, layout rules, and Node-based renderer that were tuned across six Plants-Around-Us worksheets so every new worksheet looks consistent.

## Fixed context (do not ask)

These are locked for this project. Do not ask the user about them:

- **Student name:** Ambar
- **Class:** III (3rd)
- **Board:** CBSE
- **Header style:** Green theme (title color `#1F5B2E`, accent `#2E7D32`, table header shade `#C8E6C9` / `#E8F1E8`). Do NOT use the DPS school-style header — our green style on every sheet.
- **Page:** A4 (210mm × 297mm, 11906 × 16838 DXA), 0.5" margins (720 DXA)
- **Minimum fonts (never go below):** Body ≥ 22 half-pt (11pt). Section headers ≥ 24 (12pt). MCQ options ≥ 20 (10pt). Title ≥ 32 (16pt). Instruction text ≥ 20 (10pt).
- **Info bar:** Name / Roll No / Section / Date — four cells under the title
- **Answer key default:** **Do not include** an answer key unless the user explicitly asks for one.
- **Output format:** **PDF only.** Generate the worksheet as a `.docx` internally, immediately convert it to PDF with LibreOffice (`soffice`), then **delete or hide the intermediate .docx** and only share the `.pdf` with the user.
- **File naming:** `<Variant> N - <Short Title>.pdf` where `<Variant>` = `Worksheet` | `Revision` | `Weekly Test`. Saved to `worksheets/<Subject>/Chapter - <Chapter Name>/`.

## Three supported variants

Every request falls into one of three variants. Infer the variant from the prompt; ask only if ambiguous.

| Variant | Title prefix | When to pick | Notes |
|---|---|---|---|
| **Practice Sheet** *(default)* | `Practice Sheet N` | Weekly practice, adding to school work | Standard mix of question types |
| **Revision Sheet** | `Revision Sheet N` | Before a test; covers multiple chapters | Pull from the syllabus log; mix chapters |
| **Weekly Test / Assessment** | `Weekly Test N` | Explicit "test" / "assessment" request | Slightly longer; add "Time: 30 min" under the title |

All three use our green house style — never the DPS school header.

## Difficulty levels

Three calibration levels. If the user asks for a "set of three" or "3-sheet set", generate **all three as separate files** in one pass.

| Level | Label | Mix | Use case |
|---|---|---|---|
| **1** | *"Textbook"* | Mostly direct recall; mirrors the school's sample sheet | First pass after the chapter is taught |
| **2** | *"Mixed"* | ~70% recall + ~20% understanding/application + ~10% HOTS | Standard practice; the default if unstated |
| **3** | *"Stretch"* | Fewer pure recall; more application, reasoning, HOTS | Confidence-builder before tests |

When generating a 3-sheet set, label files `Worksheet N (L1 Textbook) - ...`, `Worksheet N (L2 Mixed) - ...`, `Worksheet N (L3 Stretch) - ...` so they're easy to tell apart.

See `templates/difficulty_levels.md` for examples per question type.

## Content sourcing

Content for the worksheet comes from (in priority order):

1. **Photos the user has shared** — check the chapter folder's `source-images/` directory. These are deliberately NOT in the repo (see `.gitignore`), so on a fresh clone the folder will be empty — ask the user to attach the photos to the chat rather than assuming the chapter has no source. WhatsApp zip uploads of notebook + textbook pages are the primary source.
2. **Source Notes docx** — the per-chapter `Source Notes - <Chapter>.docx` if it exists.
3. **Well-known textbook-grade facts** that a Class III CBSE child should know even if not in the notebook (e.g., Rafflesia = world's largest flower, Coconut = tree of life, Sunflower follows the sun). These are OK to include.
4. **Never invent** facts outside points 1-3.

If no source material exists for a chapter yet, pause and ask the user to share photos or a quick topic list before generating.

## Syllabus progress tracking

Maintain a per-subject log at `worksheets/<Subject>/_progress.md`.

Format (append-only):

```
# <Subject> — Syllabus Progress

## Quarter 1 (Apr–Jun 2026)

- [x] Plants Around Us  — started 2026-04-15, worksheets: WS1–WS6, last practiced 2026-04-24
- [ ] <next chapter>  — not yet covered
```

Every time a new chapter is worked on, add or update its entry. Every time a worksheet is generated, append the date to `worksheets: ...`. This lets revision sheets intelligently mix chapters from the quarter.

## Mistake journal (weak-topics tracker)

Maintain a per-subject `worksheets/<Subject>/_mistakes.md` logging topics Ambar got wrong.

Format:

```
# <Subject> — Mistake Journal

## 2026-04-24  —  Plants Around Us  (Worksheet 3)
- Confused climber vs creeper (Q2, Q15)
- Forgot: chlorophyll is the green pigment (Q9)

## 2026-04-20  —  ...
```

When the user says *"target his weak areas"* or *"focus on recent mistakes"*, read `_mistakes.md`, pick the 3–5 most recent recurring weak topics, and bias the new worksheet toward those.

Update this file when the user says things like "he got these wrong: …" or "he's confusing X and Y".

## When the skill runs — the "smart" interaction

Smart mode: **build directly when the user's prompt has enough info, only ask about the missing bits.**

A worksheet request needs these four things:

1. **Subject** (EVS, Hindi, English, Math, Science, GK, etc.)
2. **Chapter / topic** (e.g., "Plants Around Us", "Sanyukt Vyanjan", "Adjectives")
3. **Question types + counts** (e.g., "10 fill-ups and 15 MCQs")
4. **Total marks** (can be computed from type+count, only ask if the user wants custom weighting)

**Decision procedure:**

- If the prompt supplies all four → **build directly, no questions.**
- If only the subject and chapter are given (no type breakdown) → ask a single consolidated question (AskUserQuestion) offering a recommended mix based on the chapter from the subject guide (e.g., EVS default: 10 fill-ups + 20 MCQs; Hindi default: 1 comprehension + matra + vilom + T/F).
- If the subject is given but no chapter → ask for chapter from the subject guide's known list (if any), plus a suggested question mix.
- If nothing clear is given → one AskUserQuestion covering subject + chapter + type mix.

**Never** ask about name, class, style, colours, fonts, margins, or answer keys. Those are fixed.

## The six-step build flow

When actually building a worksheet, follow this flow every time:

1. **Read the subject guide** for the chosen subject (see `subjects/<subject>.md`). It lists known chapters, question types that fit, and content sources the project holds (notebook Q&A, school sample sheets, etc.).

2. **Read the question catalog** (`question_catalog.md`) for renderer signatures and usage examples.

3. **Determine the output path.** Create `worksheets/<Subject>/Chapter - <Chapter>/` if it doesn't exist. Pick the next sequential worksheet number by listing the folder.

4. **Generate the build script.** Write `build_<short>.js` to the outputs directory. Import from the shared module:

   ```javascript
   const B = require('/path/to/.skills/create-worksheet/templates/worksheet_builder.js');
   const { Packer } = require('docx');

   const children = [];
   children.push(...B.titleBlock("EVS", "Practice Sheet 7", "Plants Around Us", 30));
   children.push(B.infoRow());
   children.push(B.sectionHeader(1, "Fill in the blanks", 10));
   fillUps.forEach((item, i) => children.push(B.fillItem(i + 1, item.parts)));
   // ... more sections ...

   Packer.toBuffer(B.buildDoc(children)).then(buf =>
     require('fs').writeFileSync(outputPath, buf));
   ```

5. **Run the build** (`node build_<short>.js`), then validate the docx (`python3 <docx_skill>/scripts/office/validate.py`).

6. **Preview and check layout.** Convert the docx to PDF with `soffice --headless --convert-to pdf` and read pages as JPEG. If content spills awkwardly, tighten spacing (see Print-density rules below). Re-run until the layout is clean.

7. **Convert to PDF and clean up.** This is the final delivery step:
   ```bash
   python3 <docx_skill>/scripts/office/soffice.py --headless --convert-to pdf "<file>.docx" --outdir "<chapter folder>/"
   rm "<chapter folder>/<file>.docx"   # only the PDF should remain
   ```
   Share **only the PDF** with the user via `computer://` link.

   If the user explicitly asks for an editable version ("send me the docx", "I want to tweak it"), keep the docx — otherwise the PDF is the single source of truth.

## Print-density rules

These patterns were tuned empirically for single-page or two-page worksheets:

- MCQ options render as 2×2 grid in a borderless nested table (saves ~60% vertical vs one-option-per-line).
- Match the following uses a bordered 2-column table with shaded header row (`#E8F1E8`).
- Fill-in-blanks lines are `"  _______________  "` — spaces on both sides are deliberate padding.
- Use `pageBreakBefore: true` on the answer-key paragraph (if requested) instead of a standalone `PageBreak` paragraph — the latter creates phantom blank pages.
- For draw-and-label boxes, use `spacing: { after: 3200 }` inside cells on a spare page, `after: 900` when sharing a page.
- Answer lines in "Name the part" / "Short answer" use `border: { bottom: SINGLE, size: 8, color: "555555" }` for a clean solid underline instead of underscores.

### Print-hardening rules (do not violate)

1. **Minimum font sizes** — never smaller than: body 11pt (size 22), MCQ options 10pt (size 20), section headers 12pt (size 24), title 16pt (size 32), instructions 10pt (size 20). If content doesn't fit at these sizes, let it spill to a second page — don't shrink fonts.
2. **No orphaned questions** — never leave a single question dangling at the very bottom of a page with its options on the next page. Use `pageBreakBefore: true` on a question's paragraph (or preceding section header) to move it cleanly to the next page.
3. **Clean page breaks** — never cut a match table or a 2×2 MCQ grid mid-way across pages.
4. **Generous writing space** — for fill-ups, the blank should be wide enough for a Class III student's handwriting (~15 underscores minimum).
5. **B&W mode** — if the user says *"print-friendly"*, *"black and white"*, *"ink-saver"*, or *"greyscale"*, pass `bwMode: true` to `B.buildDoc()` so greens become dark greys (#333333 / #555555 / #EEEEEE shading). Student's actual writing remains black. See `worksheet_builder.js` for the flag.

## The "no answer key" default

Do not include an answer key unless the user explicitly asks ("add answer key", "with answers", "for checking", etc.). This is the default because school practice sheets don't have one. If asked, add a `pageBreakBefore: true` answer-key section at the end in compact 2- or 3-column format.

## Sharing the file

After generating and converting to PDF, post a short summary and a single `computer://` link to the PDF inside `worksheets/`. Do NOT write long explanations of the content — the file speaks for itself. Example:

> **Worksheet 7 — Plants Around Us** (Class III, 30 marks, 2 pages).
> Covers 5 plant types, germination, photosynthesis, kitchen garden.
>
> [View worksheet](computer:///Users/guneetkaur/Documents/Claude/Projects/Ambar%20Worksheet/EVS/Chapter%20-%20Plants%20Around%20Us/Worksheet%207%20-%20Plants%20Around%20Us.pdf)

Always link to the **.pdf** — not the .docx — unless the user explicitly asked for an editable copy.

## What to read when invoked

Always read these files in this order before building:

1. This SKILL.md (you're here)
2. `question_catalog.md` — full list of question types + renderer signatures
3. `subjects/<the-chosen-subject>.md` — chapter list and subject-specific patterns
4. `templates/worksheet_builder.js` — the reusable renderer (signatures, defaults)
5. `templates/difficulty_levels.md` — how L1/L2/L3 differ per question type (for 3-sheet sets)
6. `worksheets/<Subject>/_progress.md` — what's been covered (for revision sheets)
7. `worksheets/<Subject>/_mistakes.md` — weak topics (if user said "target weak areas")
8. `templates/progress_tracker.md` — schema for updating _progress.md
9. `templates/mistake_journal.md` — schema for updating _mistakes.md
10. Optionally `examples/*.js` — working sample build scripts

## Extending to new subjects

The project currently has subject guides for: **EVS, Hindi, English, Math, GK, Computer**. (English/Math/GK/Computer are stubs — flesh them out as syllabus comes in.)

When a subject's chapters begin:

1. Update `subjects/<subject>.md` with:
   - Chapters being taught (add to the table)
   - Subject-specific question types (e.g., Math word problems, English grammar drills)
   - Content sources available in the project folder
2. If new question types are needed, add a renderer to `templates/worksheet_builder.js` and document it in `question_catalog.md`.
3. Start a `worksheets/<Subject>/_progress.md` and `_mistakes.md` log for that subject.

## Do NOT

- Do NOT use emojis in the worksheet output
- Do NOT include an answer key unless explicitly asked
- Do NOT ask about name/class/style/colours/fonts/margins
- Do NOT hard-code answers inside blanks
- Do NOT use `\n` in TextRun content — create separate Paragraph elements
- Do NOT forget to preview the PDF — spillovers are easy to miss
