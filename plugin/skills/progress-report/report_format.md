# The report format

Every report in the series has the same fourteen parts in the same order. Consistency
is the point — Mandeep should be able to open report 6 and find the borrow gap in
the same place he found it in report 3, and see whether it moved.

`render_report.py` builds parts 1–2, 5, 7–10 and 13 mechanically from `analysis.json`.
Claude writes parts 3, 4, 6, 11, 12 and 14 and supplies them in `narrative.json`. **Never hand-write a number that the analysis file already
computed** — if a figure isn't in `analysis.json`, either extend the script or
leave the claim out.

---

## 1. Masthead

Title, period label, and the one-paragraph dek. The title stays `Ambar Progress
Report N` across the series so the archive sorts and reads sensibly. The dek says
what this period was about in two sentences — not a summary of the sections below.

## 2. Scoreboard — four tiles

Fixed, in this order:

| Tile | Content |
|---|---|
| **This period** | accuracy %, with correct/total, sheet count, days practised |
| **Change** | delta in points against the previous period (or "first report") |
| **All time** | cumulative accuracy and total practice days |
| **Open gaps** | count of gaps still open after this period |

## 3. Headline *(Claude writes)*

One paragraph, no heading, set large. The single most important thing that happened
this period. If nothing important happened, say that plainly — a quiet period is a
finding, not a failure to report.

## 4. Since the last report *(Claude writes)*

Two to four short paragraphs of prose, followed by the accuracy chart (whole
history, this period shaded). Cover what moved, what stalled, and what is new.
Write it as if to someone who read the last report and wants the diff — not as a
recap of everything.

## 5. Gate board

A table with a row per track: **Track · Where she is · Status · Last evidence ·
Next gate.** Status is one of `mastered`, `in-progress`, `blocked`, `not-started`.
Every track appears every time, including the dormant ones — a track that has gone
quiet for three reports is information.

"Last evidence" is always a real score and date (`25/26 · 23 Aug`), never an
adjective.

## 6. Open gaps *(Claude writes the prose; evidence tables are generated)*

One card per gap, each with:

- **Title** — name the misconception, not the topic. "Smaller-from-larger, borrow
  ignored" beats "Subtraction difficulty".
- **Status** — `new`, `improving`, `open`, or `closed`, plus the date it opened.
- **What** — what rule she is actually running, in one short paragraph.
- **Evidence table** — pulled from `analysis.json`, question / wrote / correct /
  what happened / date.
- **Fix** — what to do about it, concretely enough to act on today.

Gaps **carry forward** between reports via `reports/_state.json` until closed. A
gap is only closed by evidence: a re-attempt at or above the track's usual level.
Closing a gap on a hunch is the one thing this report must never do.

## 7. Every miss, classified

The taxonomy table — counts by error class for the period. See `error_taxonomy.md`
for what each class means and how the script decides.

The standing note above this table: blanks and wrong answers need opposite
responses. It stays in every report because it is the thing most easily forgotten.

## 8. Same answer, more than once

Any miss repeated identically — a memorised-wrong fact rather than a slip. Cheapest
items on the whole list to fix, so they get their own section. Omitted when empty.

## 9. Re-attempts and unfinished sheets

Two short blocks. Re-attempts show the score sequence across dates — this is where
learning is most visible (`0/12 → 10/12`). Unfinished sheets are listed separately
because they need re-giving, not teaching.

## 10. By track

Horizontal bars for the period, with the standing caution that small denominators
move bars a long way.

## 11. What to do next *(Claude writes)*

At most seven, ranked, each one line of "why". Below them, the carried actions from
the previous report with a status chip each — `done`, `open`, or `dropped`. An
action that has been open across three reports gets called out in the headline.

## 12. Do again *(Claude writes, from `analysis.catalogue.redo_candidates`)*

The script lists every sheet whose latest sitting was below 95% or left unfinished.
Claude curates: keep only the ones that settle an open question, drop the rest, and
give each a "give after" prerequisite where one exists. Never list a sheet as a
re-do without saying what re-giving it would settle.

## 13. Already written, never opened

Coverage bars per track, straight from `analysis.catalogue` — how many sheets the
app defines against how many she has ever opened. Below them, a Claude-written
row per track naming the specific sheet ids to assign next and why that one.

The app holds far more than she has attempted. Always check what already exists
before proposing anything new — reading `index.html` is part of the run, not an
optional extra.

## 14. Build these *(Claude writes)*

Only sheets that genuinely do not exist. Each card carries what it contains and a
**Settles:** line naming the question it answers. A sheet that would merely be nice
to have does not belong here.

Optionally followed by a week-by-week order (`schedule` in the narrative), which is
the place to sequence re-dos, existing sheets and new builds together.

---

## Length discipline

A report is worth reading only if it is read. Target: the whole thing scans in
three minutes. Prose parts (3, 4, gap "what" and "fix", action "why", and the re-do / assign / build
reasons) together should come to roughly 900–1,200 words. Everything else is tables and chips.

If a period produced almost nothing, the report gets shorter — it does not get
padded to look substantial.
