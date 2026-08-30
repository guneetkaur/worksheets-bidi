# worksheets-bidi

Ambar's practice app, her results, and the recurring progress report.

| Path | What it is |
|---|---|
| `index.html` | The worksheet app — 205 sheets across nine tracks. Pick a sheet; "Finish & Check" marks it and syncs one row per question to `results/`. |
| `results/results.csv` | Every answer she has ever submitted. The single source of truth. |
| `reports/index.html` | The latest progress report. `reports/YYYY-MM-DD.html` are the archived issues. |
| `reports/_state.json` | Memory between reports: gates, open gaps, outstanding actions, `covered_through`. |
| `worksheets/` | Syllabus progress logs (`_progress.md`), mistake journals (`_mistakes.md`), prep plans, and the `.docx` source notes per subject. |
| `tools/build_sheets.py` | Generates new sheets and appends them to `index.html`. Answers are computed, never typed. `--check` verifies without writing. |

## Running the report

Installed as the `progress-report` skill in the `ambar-worksheet` plugin — say
"run the progress report" in Cowork. For the raw numbers only:

```bash
python3 <plugin>/skills/progress-report/scripts/analyse.py \
  --csv results/results.csv --state reports/_state.json \
  --catalogue index.html --out /tmp/analysis.json
```

The period is always "since the last report", read from `_state.json`.

## Not in here, on purpose

Generated worksheet PDFs and notebook source photos — see `.gitignore`. They are
outputs, rebuildable from the plugin, and binaries don't diff.
