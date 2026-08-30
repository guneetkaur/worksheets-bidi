# `reports/_state.json`

The memory between runs. Without it every report re-analyses the whole history and
loses the "what changed" framing that makes the series worth keeping.

Written at the end of every run, committed alongside the report.

```json
{
  "report_number": 3,
  "generated_on": "2026-09-08",
  "covered_through": "2026-09-07",
  "period_accuracy": 84.2,
  "cumulative_accuracy": 87.9,
  "gates": [
    {
      "track": "Mental Subtraction",
      "stage": "Stage 2 — borrow (keystone)",
      "status": "in-progress",
      "evidence": "10/12 · 24 Aug",
      "next_gate": "Clean 12/12 on WS4"
    }
  ],
  "gaps": [
    {
      "id": "borrow-smaller-from-larger",
      "track": "Mental Subtraction",
      "title": "Smaller-from-larger, borrow ignored",
      "opened": "2026-08-23",
      "status": "improving",
      "history": [
        { "date": "2026-08-23", "evidence": "0/12" },
        { "date": "2026-08-24", "evidence": "10/12" }
      ],
      "closed_on": null
    }
  ],
  "actions": [
    {
      "id": "borrow-across-zero",
      "title": "Two or three borrow-across-zero sheets, then re-run WS4",
      "opened": "2026-08-25",
      "status": "open"
    }
  ]
}
```

## Field rules

- **`covered_through`** — the last date present in the CSV at the time of the run,
  not the run date. The next run analyses rows strictly after this.
- **`gaps[].id`** — a stable kebab-case slug naming the *misconception*. Never
  renumber or rename it; the whole point is that it is the same id across reports.
- **`gaps[].status`** — `new` on first appearance, `open` if unchanged, `improving`
  if the evidence moved the right way, `closed` once the closing rule is met. Once
  closed, keep the entry with `closed_on` set for two further reports, then drop it.
- **`gaps[].history`** — one entry per report that saw evidence, so a gap card can
  show its own trajectory without re-reading old reports.
- **`actions[].status`** — `open`, `done`, or `dropped`. Carry every open action
  into the next report's carried-actions block. An action open across three reports
  is escalated into the headline.

## Closing rule

A gap closes only on evidence: a re-attempt of the sheet (or a sheet covering the
same skill) at or above the track's normal level, on a date after the gap opened.
Never close a gap because time has passed or because it wasn't practised.
