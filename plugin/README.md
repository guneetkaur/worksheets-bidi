# ambar-worksheet

> Source of truth: `plugin/` in the `worksheets-bidi` repo, which is also the
> working directory. Every path in these skills is relative to the repo root.

A Cowork / Claude Code plugin that generates printable CBSE Class III worksheets for Ambar.

## What it does

Two skills:

- **create-worksheet** — print-ready worksheets with consistent green-theme styling across every subject.
- **progress-report** — the recurring results review, built from the `worksheets-bidi` repo and pushed back to it.

## Triggers

Say any of these in Cowork:

- *"Make me an EVS worksheet on Plants with 10 fill-ups and 15 MCQs"*
- *"Create a 3-sheet difficulty set on Animals Around Us"*
- *"Hindi practice sheet on matra"*
- *"Revision sheet covering everything we've done in EVS"*
- *"Weekly test on Plants, 30 minutes"*
- *"Target his weak areas from last week"*
- *"Black-and-white worksheet on Germination"*

For the report:

- *"Run the progress report"*
- *"How is Ambar doing?"*
- *"What's changed since the last report?"*
- *"Fortnightly review"* / *"monthly review"*
- *"Analyse her results and push the report"*

## What's inside

- **create-worksheet skill** with:
  - Reusable `worksheet_builder.js` module (13 question-type renderers)
  - Subject guides: EVS, Hindi, English, Math, GK, Computer
  - Difficulty-level guide (L1 Textbook / L2 Mixed / L3 Stretch)
  - Progress-tracker schema (`_progress.md`)
  - Mistake-journal schema (`_mistakes.md`)
  - Working example scripts (EVS + Hindi)

- **progress-report skill** with:
  - `analyse.py` — question-level analysis of `results/results.csv`, with automatic
    error classification (borrow bugs, operation confusion, transcription slips,
    repeated wrong facts, unfinished sheets, re-attempt sequences)
  - `render_report.py` — the locked house style; the report looks the same every issue
  - `report_format.md` — the fourteen fixed parts of a report
  - `error_taxonomy.md` — the error classes and when one becomes a tracked gap
  - `templates/state_schema.md` — `reports/_state.json`, the memory between runs
  - Reads the app's own sheet catalogue out of `index.html`, so the report ends with
    what to re-give, what is already built and untouched, and what actually needs writing

## Locked context

The skill is hard-wired for **Ambar, Class III, CBSE**:

- Green theme on every worksheet (our house style — never the DPS school header)
- A4 page size, 0.5" margins
- Minimum fonts: body 11pt, MCQ options 10pt, headers 12pt
- Default variant: Practice Sheet (also supports Revision Sheet, Weekly Test)
- Answer key: never included by default (included only if explicitly requested)

## Three supported variants

| Variant | When |
|---|---|
| Practice Sheet *(default)* | Weekly practice |
| Revision Sheet | Multi-chapter, pre-test |
| Weekly Test | Formal assessment with time limit |

## Three difficulty levels

| Level | Label | Mix |
|---|---|---|
| **1** | Textbook | Direct recall, mirrors school |
| **2** | Mixed *(default)* | 70% recall + 20% understanding + 10% HOTS |
| **3** | Stretch | Application/reasoning/HOTS |

Say *"3-sheet set"* or *"set of three"* to get all three levels in one pass.

## Supported question types

Fill in the blanks · MCQs (2×2 grid) · Match the following · True/False · Odd one out · One-word answers · Short answers · Name the part · Label diagram (with images) · Identify-from-illustration · Draw & label · Sort into groups · Classify list

## Supported subjects

Full guides: **EVS**, **Hindi** (with Devanagari support).
Stub guides ready to flesh out: **English**, **Math**, **GK**, **Computer**.

## How the report works

Each run reads `reports/_state.json` from the repo to find where the last report
stopped, analyses only what is new, carries open gaps forward, and writes:

```
reports/index.html      always the latest
reports/YYYY-MM-DD.html archived snapshot
reports/_state.json     gates, open gaps, outstanding actions
```

A gap closes only on evidence — a re-attempt at or above the track's normal level.
Never because time passed.

The report also reads `index.html` and compares every sheet the app defines against
every sheet she has opened. That check is what keeps the recommendations honest:
roughly three quarters of the app has never been attempted, so "build a new sheet"
has to survive a search of the catalogue first.

Run it fortnightly or monthly; the period is always "since the last report", so the
cadence can drift without leaving holes.

## Extending

To add a new subject:

1. Create `skills/create-worksheet/subjects/<name>.md` with the chapter list and subject-specific question types.
2. If new question-type renderers are needed, add them to `templates/worksheet_builder.js` and document in `question_catalog.md`.

## Requirements

- Node.js with the `docx` npm package installed (Cowork's shell sandbox has this available).
- LibreOffice for optional PDF preview.
- ImageMagick (`convert`) for generating illustration assets from SVG.

## Install

Install from the `.plugin` file in Cowork: *Settings → Plugins → Install from file*.
