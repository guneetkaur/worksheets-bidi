---
name: progress-report
description: Build and publish Ambar's worksheet progress report from the results repo. Use whenever the user asks for a progress report, fortnightly or monthly review, "how is Ambar doing", "analyse her results", "what's changed since last time", "update the report", "run the report", or "push the report". Reads results/results.csv from the worksheets-bidi repo, analyses every answer at the question level, carries open gaps forward from the previous run, writes reports/index.html plus a dated archive copy, and pushes to the repo.
---

# progress-report — Ambar's recurring results review

Produces one report in a continuing series. The value is not the snapshot, it is the
**diff**: what moved since last time, which gaps closed, which have now been open
for three reports running.

## Fixed context (do not ask)

- **Student:** Ambar, Class III, CBSE.
- **Everything lives in one repo:** `guneetkaur/worksheets-bidi`, which is the working
  directory. All paths below are relative to it — `results/results.csv`, `index.html`,
  `reports/`, `worksheets/`, `sources/`, `plugin/`.
- If anyone points at a `results.csv` outside this repo, say it is stale and use the
  repo's. An out-of-date copy once produced a wrong "nothing since 22 July" analysis.
- **Output:** `reports/index.html` (always the latest) plus `reports/YYYY-MM-DD.html`
  (archive) and `reports/_state.json`, committed and pushed.
- **Cadence:** whatever the user runs it at. The period is always "since the last
  report", read from `_state.json` — never a fixed window.
- **House style:** locked in `scripts/render_report.py`. Do not restyle it; a series
  that looks different every issue is harder to read, not fresher.

## Read before building

1. This file.
2. `report_format.md` — the fourteen fixed parts and who writes each.
3. `error_taxonomy.md` — the error classes and the rule for promoting one to a gap.
4. `templates/state_schema.md` — how gaps and actions carry between runs.

## The run

### 1. Get the repo

Try in this order and stop at the first that works:

- **In place via `device_bash`** — `git pull` in the working directory and work there.
  This is the cleanest path: the push happens with the user's own credentials.
- **Cloud clone** — `git clone https://github.com/guneetkaur/worksheets-bidi.git` into
  the container. Fine for reading and building; needs a token to push (step 7).
- **Staged file** — if neither works, ask the user to attach the current
  `results.csv`. Build the report, deliver it as a file, and say plainly that it was
  not pushed.

Record the last commit date. If it is older than the previous report's
`covered_through`, there is nothing new: say so in one line and stop rather than
generating an empty report.

### 2. Analyse

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/progress-report/scripts/analyse.py \
  --csv <repo>/results/results.csv \
  --state <repo>/reports/_state.json \
  --catalogue <repo>/index.html \
  --out /tmp/analysis.json
```

`--catalogue` reads the app's own sheet list out of `index.html`. **Always pass
it.** Without it the report can recommend building something the app already
contains — which has happened: a geometry facts sheet and a comparatives drill were
both proposed before `note-imo-geometry` and `note-ieo-adjectives` turned up in the
catalogue, already covering exactly the misses.

Omit `--state` on the very first run. Pass `--since YYYY-MM-DD` to override the
period when the user asks for a specific window.

Then **read `/tmp/analysis.json` properly** — `errors`, `repeated_facts`, `retries`
and `unfinished_sheets` especially. The script classifies arithmetic automatically
and parks every multiple-choice miss in `wrong-choice`; those need a human read.
Look at which distractor she picked — it usually names the misconception.

### 3. Read the catalogue before recommending anything

`analysis.catalogue` gives coverage per track, every sheet never opened, and
`redo_candidates` — sheets whose latest sitting was below 95% or left unfinished.

Three rules:

- **Never propose building a sheet without checking `untouched` first.** If the app
  already holds one that covers it, the recommendation is "assign `<id>`", not "build".
- **Curate `redo_candidates`.** The script lists everything below par; keep only
  those that settle an open question and drop the rest. A re-do without a stated
  purpose is busywork.
- **Read the sheet, not just its title.** Sheet titles mislead: `sub-w4-l1` is titled
  "with Borrow" but its only section is "Round-and-adjust — no borrowing needed!"
  and it teaches a mental strategy, not column subtraction. Grep `index.html` for the
  sheet id and read its section titles and `note` before drawing a conclusion about
  why she missed on it.

### 4. Reconcile gaps against the previous state

For each gap in `_state.json`:

- Did this period produce evidence on it? Append to `history`.
- Did the evidence meet the closing rule in `templates/state_schema.md`? Only then
  set `status: closed`. **Never close a gap because it wasn't practised.**
- Otherwise carry it forward as `open` or `improving`.

Then look for new gaps using the promotion rules in `error_taxonomy.md`. Two
instances make a pattern; one is a slip.

### 5. Write `narrative.json`

This is the only place Claude's prose enters. Structure:

```json
{
  "title": "Ambar Progress Report 3",
  "period_label": "10 Aug – 24 Aug 2026",
  "eyebrow": "Fortnightly review",
  "generated_on": "2026-08-25",
  "dek": "One paragraph on what this period was about.",
  "headline": "The single most important thing that happened. Set large, no heading.",
  "since_last": "<p>Two to four paragraphs of HTML prose.</p>",
  "gates": [
    { "track": "Mental Subtraction", "stage": "Stage 2 — borrow (keystone)",
      "status": "in-progress", "status_label": "in progress",
      "evidence": "10/12 · 24 Aug", "next_gate": "Clean 12/12 on WS4" }
  ],
  "gaps": [
    { "id": "borrow-smaller-from-larger", "track": "Mental Subtraction",
      "title": "Smaller-from-larger, borrow ignored", "opened": "23 Aug",
      "status": "improving", "status_label": "improving",
      "what": "<p>What rule she is actually running.</p>",
      "fix": "What to do about it, concretely.",
      "error_notes": ["smaller-from-larger, borrow ignored"],
      "evidence_limit": 12 }
  ],
  "_evidence_filters": "any of error_notes / error_classes / question_match / worksheet_match — combined with AND",
  "actions": [ { "title": "…", "why": "One line." } ],
  "redo": [
    { "id": "sub-w4-l1", "sheet": "2-digit − 2-digit with borrow",
      "standing": "0/12 → 10/12", "when": "23–24 Aug",
      "why": "Two survivors left, both borrow-across-zero.",
      "after": "add-w11" }
  ],
  "assign_next": [
    { "track": "Mental addition", "sheets": "<span class=\"sid\">add-w11</span>",
      "why": "The skipped prerequisite." }
  ],
  "build": [
    { "kind": "drill", "priority": "open", "title": "Missing number — all four positions",
      "what": "<p>What the sheet contains.</p>",
      "settles": "The question it answers." }
  ],
  "schedule": [ { "title": "Week 1 — close the borrow gap", "items": ["…", "…"] } ],
  "schedule_note_title": "One scheduling note", "schedule_note": "…",
  "carried_actions": [ { "title": "…", "status": "done", "status_label": "done" } ],
  "tracks_note": "Optional override for the caution under the bars."
}
```

Four optional keys select which rows from `analysis.json` fill a gap's evidence
table, combined with AND: `error_notes` (exact match on the note the script wrote),
`error_classes` (taxonomy class), `question_match` and `worksheet_match` (regular
expressions). Use `question_match` for a gap the script can't name — for example
`"\\+ __ ="` to pull just the missing-addend blanks out of the 22 blanks in the
period. Leave all four out for a gap with no tabulated evidence.

Prose fields accept HTML. Keep the whole narrative to 600–900 words; a quiet period
gets a shorter report, not a padded one.

Do not write a number into the narrative that isn't in `analysis.json`.

### 6. Render and check

Render to a temp path first. The renderer emits a **fragment** — its own `<title>`
and `<style>`, no `<html>`/`<head>`/`<body>` — because that is exactly what the
Artifact tool wants. The repo copies get wrapped into standalone documents.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/progress-report/scripts/render_report.py \
  --analysis /tmp/analysis.json --narrative /tmp/narrative.json --out /tmp/report.html

python3 - <<'PY'
import pathlib, shutil, datetime
src = pathlib.Path("/tmp/report.html").read_text()
head, rest = src.split("</style>", 1)
doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       + head + "</style></head><body>" + rest + "</body></html>")
out = pathlib.Path("<repo>/reports"); out.mkdir(exist_ok=True)
(out / "index.html").write_text(doc)
(out / f"{datetime.date.today()}.html").write_text(doc)
PY
```

Publish `/tmp/report.html` (the fragment) as the Artifact; commit the wrapped
`reports/*.html` to the repo.

Render it and look at it before pushing — screenshot with Playwright (Chromium is at
`/opt/pw-browsers/chromium`) in light and dark, and at 390px wide. Check for
horizontal overflow and label collisions.

### 7. Write state, commit, push

Write `<repo>/reports/_state.json` per `templates/state_schema.md` — increment
`report_number`, set `covered_through` to `analysis.generated_for_data_through`.

```bash
git -C <repo> add reports/
git -C <repo> commit -m "reports: progress report N (through YYYY-MM-DD)"
git -C <repo> push
```

If pushing from the cloud clone, the remote needs a token. Look for `GITHUB_TOKEN`
or `AMBAR_REPO_TOKEN` in the environment first. If neither is set, **ask for one
once** rather than failing silently, and use it as
`https://<token>@github.com/guneetkaur/worksheets-bidi.git` — never write the token
into a file that gets committed.

If the push cannot happen, say so in one sentence, deliver the HTML as a file, and
tell the user exactly which command to run.

### 8. Update the journals

`worksheets/<Subject>/_progress.md` and `_mistakes.md` are in the repo, so they are
edited in place and committed with the report — no mirroring step.

Append a dated entry to `worksheets/<Subject>/_mistakes.md` for every subject
with new findings, and update `worksheets/<Subject>/_progress.md` where a stage
or gate moved. Follow the existing shape of those files — newest entry at the top of
`_mistakes.md`. Link the report URL in the entry.

### 9. Deliver

Publish `reports/index.html` as an Artifact **at the same URL every run** so the link
never changes — pass the previous run's URL as `url` (it is stored in `_state.json`
as `artifact_url`; find it with `action: "list"` if missing). Then post a short
summary: the headline finding, the one or two gaps that moved, and the link. Do not
restate the report in chat — it is right there.

## Standing judgements

Carry these into every run unless new evidence overturns them:

- **Blanks are fatigue or unfamiliarity; wrong answers are knowledge.** They get
  opposite responses. Never merge them into one "misses" number.
- **A repeated identical answer is a stored fact, not a slip.** Highest fix-to-effort
  ratio in the file.
- **Definitional misses on first contact with a topic mean untaught, not weak.** Say
  so rather than listing them as errors.
- **Do not conclude fatigue from a low score without checking the timestamps.**
  Submission times are in the CSV; use them.
- **Small denominators lie.** A track at 52% on 38 questions is not a worse track
  than one at 88% on 400.
- **Assign before you build.** Roughly three quarters of the app has never been
  opened. Anything proposed as new work has to survive a check against the catalogue
  first.

## Do NOT

- Do NOT close a gap without evidence.
- Do NOT restyle the report between issues.
- Do NOT read the stale `results.csv` in the project folder.
- Do NOT draw speed or timing conclusions from `total_time_s` — the column contains
  negative and six-figure values and is unusable.
- Do NOT pad a quiet period. A three-paragraph report for a quiet fortnight is the
  correct output.
