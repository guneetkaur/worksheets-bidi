# Syllabus Progress Tracker

Each subject maintains an append-only log at `worksheets/<Subject>/_progress.md`. The skill creates it automatically on first run and updates it whenever a new worksheet is generated.

## Schema

```markdown
# <Subject> — Syllabus Progress

Last updated: YYYY-MM-DD

## Quarter 1 (Apr–Jun 2026-27)

- [x] **Plants Around Us**
  - Started: 2026-04-15
  - Worksheets: WS1, WS2, WS3, WS4, WS5, WS6
  - Last practiced: 2026-04-24
  - Weak spots: see _mistakes.md (2026-04-24)

- [ ] **Animals Around Us**
  - Not yet covered

## Quarter 2 (Jul–Sep 2026-27)

- [ ] ...
```

## Maintenance rules

- **First time a chapter is touched**: add it as a row with status `[x]` and `Started: <today>`.
- **Every worksheet generated**: append the worksheet number to `Worksheets:` and update `Last practiced:` to today.
- **New quarter**: add a `## Quarter N (date range)` section before adding chapters.
- **Never delete**: history is kept forever so we can revisit.

## When reading for revision sheets

When the user asks for a *"revision sheet"* or *"exam prep"*:

1. Read `_progress.md` for the subject.
2. Pick all chapters marked `[x]` (covered).
3. For a month/quarter revision, limit to the relevant date range.
4. Build a single cumulative worksheet pulling the most important concept from each chapter. Allocate 3–5 marks per chapter so they all get covered.
5. Label the file `Revision Sheet N - Q1 covers ....docx` and save under `worksheets/<Subject>/Revision/`.

## Date format

Use ISO dates (`YYYY-MM-DD`) everywhere. Run `date +%Y-%m-%d` in bash to get today.
