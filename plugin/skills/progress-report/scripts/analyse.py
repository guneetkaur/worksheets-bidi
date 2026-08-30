#!/usr/bin/env python3
"""
analyse.py — deterministic analysis of Ambar's worksheet results.

Reads the repo CSV (and, if present, reports/_state.json from the previous run)
and writes a single JSON blob that the report is built from. Every number in the
report must come from this file — never from reading the CSV by eye.

Usage:
    python3 analyse.py --csv results/results.csv \
                       [--state reports/_state.json] \
                       [--since YYYY-MM-DD] \
                       [--catalogue index.html] \
                       --out /tmp/analysis.json

Period rules:
  * --since given            -> period = rows with date > since
  * --state given, no --since-> period = rows with date > state.covered_through
  * neither                  -> period = the whole file (first report)

Attempt de-duplication: the webapp writes one row per question per press of
"Finish & Check", so one sitting can appear several times. Rows are grouped by
(date, worksheet, submitted_at) into attempts; where a sheet was attempted more
than once on the same day the BEST attempt is the one counted. Every other
attempt is still reported under `abandoned_attempts` when it has blanks, because
an abandoned sheet is a finding in its own right.
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict, OrderedDict

# --------------------------------------------------------------------------
# track classification — order matters, first match wins
# --------------------------------------------------------------------------
TRACK_RULES = [
    ("Mental Subtraction",   r"subtract|borrow"),
    ("Mental Multiplication", r"\btables?\b|multiplication"),
    ("Mental Addition",      r"number bonds|doubles|carry|ltr|anchoring|bridging|addition|worksheet \d+"),
    ("Reasoning (SOF)",      r"^drill \d"),
    ("English (IEO)",        r"vocabulary|verbs|tenses|articles|prepositions|adjectives|degrees|comprehension|written expression|noun|pronoun|adverb"),
    ("Science (NSO)",        r"\bnso\b|human body|matter & materials|water & air|earth & universe|\bfood\b"),
    ("GK (IGKO)",            r"surroundings|igko|\bgko\b|current affairs|life skills|sports"),
    ("Maths (IMO topics)",   r"geometry|data handling|fraction|division|measurement|time & money"),
]


def classify_track(worksheet: str) -> str:
    w = worksheet.lower()
    for name, pattern in TRACK_RULES:
        if re.search(pattern, w):
            return name
    return "Unclassified"


# --------------------------------------------------------------------------
# error taxonomy — see error_taxonomy.md for the full definitions
# --------------------------------------------------------------------------
def parse_binary_op(question):
    """Return (a, op, b) for a plain arithmetic item, else None."""
    m = re.match(r"^\s*(\d+)\s*([+−\-×x*])\s*(\d+)\s*=", str(question))
    if not m:
        return None
    op = {"+": "+", "−": "-", "-": "-", "×": "x", "x": "x", "*": "x"}[m.group(2)]
    return int(m.group(1)), op, int(m.group(3))


def classify_error(row):
    """Classify one wrong answer. Returns (class, note)."""
    given = (row["given_answer"] or "").strip()
    correct = (row["correct_answer"] or "").strip()
    if given == "":
        return "blank", "not attempted"

    parsed = parse_binary_op(row["question"])
    if parsed and given.lstrip("-").isdigit() and correct.lstrip("-").isdigit():
        a, op, b = parsed
        g, c = int(given), int(correct)

        # operation confusion: the answer is right for a DIFFERENT operation
        alt = {"+": [a - b, a * b], "-": [a + b, a * b], "x": [a + b, a - b]}[op]
        if g in alt:
            return "operation-confusion", f"answer for a different operation on {a},{b}"

        # transcription: correct answer with digits reversed, or a digit smeared in
        if str(g) == str(c)[::-1] and len(str(c)) > 1:
            return "transcription", f"{c} written backwards"
        if len(str(g)) > len(str(c)) and str(c) in str(g):
            return "transcription", f"digit smear around {c}"

        # smaller-from-larger (the classic borrow bug), column by column
        if op == "-" and len(str(a)) == len(str(b)) == len(str(g)):
            sfl = "".join(str(abs(int(x) - int(y))) for x, y in zip(str(a), str(b)))
            if sfl.lstrip("0") == str(g).lstrip("0"):
                return "wrong-rule", "smaller-from-larger, borrow ignored"

        # mixed-operation-per-column (adds the tens, subtracts the units)
        if op == "-" and len(str(a)) == len(str(b)) == 2 == len(str(g)):
            mixed = str(int(str(a)[0]) + int(str(b)[0])) + str(int(str(a)[1]) - int(str(b)[1]))
            if mixed == str(g):
                return "wrong-rule", "adds the tens, subtracts the units"

        if abs(g - c) <= max(2, c * 0.05):
            return "near-miss", f"off by {g - c:+d}"
        return "wrong-fact", f"gave {g}, correct {c}"

    return "wrong-choice", ""


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# --------------------------------------------------------------------------
# the app's own sheet catalogue, read straight out of index.html
# --------------------------------------------------------------------------
TRACK_CONSTS = {"T": "SOF NSO — Science", "TGK": "SOF IGKO — GK"}

CAT_PATTERNS = [
    r'\{\s*"?id"?\s*:\s*"([^"]+)"\s*,\s*"?track"?\s*:\s*("(?:[^"]+)"|T|TGK)\s*,\s*"?title"?\s*:\s*"([^"]+)"',
    r'id\s*:\s*"([a-z0-9-]+)"\s*,\s*track\s*:\s*("(?:[^"]+)"|T|TGK)\s*,\s*title\s*:\s*"([^"]+)"',
]


def read_catalogue(path):
    """Every sheet the app defines: {id: (track, title, is_note)}."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    cat = {}
    for pattern in CAT_PATTERNS:
        for m in re.finditer(pattern, src):
            sid, track, title = m.group(1), m.group(2), m.group(3)
            track = TRACK_CONSTS.get(track, track.strip('"'))
            cat.setdefault(sid, (track, title, sid.startswith("note-") or title.startswith("Notes:")))
    return cat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--state", default=None)
    ap.add_argument("--since", default=None)
    ap.add_argument("--catalogue", default=None,
                    help="path to the app's index.html, to report what exists but has never been opened")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rows = read_rows(args.csv)
    for r in rows:
        r["ok"] = (r.get("is_correct") or "").strip().lower() == "yes"
        r["blank"] = not (r.get("given_answer") or "").strip()
        r["submitted_at"] = r.get("submitted_at") or ""
        r["track"] = classify_track(r["worksheet"])

    state = {}
    if args.state and os.path.exists(args.state):
        with open(args.state, encoding="utf-8") as fh:
            state = json.load(fh)

    since = args.since or state.get("covered_through")

    # ---------------- attempts -> best-per-sheet-per-day ----------------
    attempts = defaultdict(list)
    for r in rows:
        attempts[(r["date"], r["worksheet"], r["submitted_at"])].append(r)

    sheets = defaultdict(list)   # (date, worksheet) -> list of attempts
    abandoned = []
    for (date, ws, _sub), items in attempts.items():
        rec = {
            "date": date, "worksheet": ws, "track": items[0]["track"],
            "n": len(items),
            "correct": sum(1 for i in items if i["ok"]),
            "blank": sum(1 for i in items if i["blank"]),
            "rows": items,
        }
        rec["wrong"] = rec["n"] - rec["correct"] - rec["blank"]
        sheets[(date, ws)].append(rec)

    best = []
    for key, recs in sheets.items():
        recs.sort(key=lambda r: (-r["correct"], r["blank"]))
        best.append(recs[0])
        for other in recs[1:]:
            if other["blank"] >= max(3, other["n"] * 0.3):
                abandoned.append({k: other[k] for k in ("date", "worksheet", "n", "correct", "blank")})
    best.sort(key=lambda r: (r["date"], r["worksheet"]))

    period = [s for s in best if not since or s["date"] > since]
    prior = [s for s in best if since and s["date"] <= since]

    def totals(group):
        n = sum(s["n"] for s in group)
        c = sum(s["correct"] for s in group)
        b = sum(s["blank"] for s in group)
        return {
            "sheets": len(group), "questions": n, "correct": c, "blank": b,
            "wrong": n - c - b,
            "accuracy": round(c / n * 100, 1) if n else None,
            "days": len({s["date"] for s in group}),
        }

    # ---------------- per-day series (whole history) ----------------
    by_day = defaultdict(lambda: {"n": 0, "c": 0, "b": 0, "sheets": 0})
    for s in best:
        d = by_day[s["date"]]
        d["n"] += s["n"]; d["c"] += s["correct"]; d["b"] += s["blank"]; d["sheets"] += 1
    daily = [
        {"date": k, "questions": v["n"], "correct": v["c"], "blank": v["b"],
         "sheets": v["sheets"], "accuracy": round(v["c"] / v["n"] * 100, 1)}
        for k, v in sorted(by_day.items())
    ]

    # ---------------- per-track ----------------
    def track_rollup(group):
        out = defaultdict(lambda: {"sheets": 0, "questions": 0, "correct": 0, "blank": 0})
        for s in group:
            t = out[s["track"]]
            t["sheets"] += 1; t["questions"] += s["n"]
            t["correct"] += s["correct"]; t["blank"] += s["blank"]
        for t in out.values():
            t["accuracy"] = round(t["correct"] / t["questions"] * 100, 1) if t["questions"] else None
        return OrderedDict(sorted(out.items(), key=lambda kv: -(kv[1]["accuracy"] or 0)))

    # ---------------- errors in the period ----------------
    errors = []
    for s in period:
        for r in s["rows"]:
            if r["ok"]:
                continue
            cls, note = classify_error(r)
            errors.append({
                "date": s["date"], "worksheet": s["worksheet"], "track": s["track"],
                "question_id": r.get("question_id", ""),
                "question": r["question"],
                "given": (r["given_answer"] or "").strip(),
                "correct": (r["correct_answer"] or "").strip(),
                "class": cls, "note": note,
            })

    tax = defaultdict(int)
    for e in errors:
        tax[e["class"]] += 1

    # repeated identical misses = a wrong stored fact, worth surfacing on its own
    repeats = defaultdict(list)
    for e in errors:
        if e["class"] in ("wrong-fact", "near-miss", "wrong-rule", "operation-confusion"):
            repeats[(e["question"].strip(), e["given"])].append(e["date"])
    repeated_facts = [
        {"question": q, "given": g, "times": len(ds), "dates": sorted(set(ds))}
        for (q, g), ds in repeats.items() if len(ds) > 1
    ]
    repeated_facts.sort(key=lambda r: -r["times"])

    # sheets where most misses are blanks -> unfinished, not wrong
    unfinished = [
        {"date": s["date"], "worksheet": s["worksheet"], "n": s["n"],
         "correct": s["correct"], "blank": s["blank"]}
        for s in period if s["blank"] and s["blank"] >= s["wrong"]
    ]

    # re-attempts of the same sheet across days -> the learning signal
    seen = defaultdict(list)
    for s in best:
        seen[s["worksheet"]].append(s)
    retries = []
    for ws, recs in seen.items():
        if len(recs) < 2:
            continue
        recs.sort(key=lambda r: r["date"])
        if any(r["date"] > (since or "") for r in recs[1:]):
            retries.append({
                "worksheet": ws,
                "attempts": [{"date": r["date"], "score": f'{r["correct"]}/{r["n"]}',
                              "accuracy": round(r["correct"] / r["n"] * 100)} for r in recs],
            })

    # ---------------- the app catalogue: what exists vs what she has opened ----
    catalogue = None
    if args.catalogue and os.path.exists(args.catalogue):
        cat = read_catalogue(args.catalogue)
        ever = {s["worksheet"] for s in best}
        best_by_title = {}
        for s in best:
            cur = best_by_title.get(s["worksheet"])
            if not cur or s["date"] > cur["date"]:
                best_by_title[s["worksheet"]] = s

        coverage, untouched, notes = defaultdict(lambda: {"built": 0, "done": 0}), [], defaultdict(int)
        for sid, (track, title, is_note) in cat.items():
            if is_note:
                notes[track] += 1
                if title not in ever:
                    untouched.append({"id": sid, "track": track, "title": title, "kind": "note"})
                continue
            coverage[track]["built"] += 1
            if title in ever:
                coverage[track]["done"] += 1
            else:
                untouched.append({"id": sid, "track": track, "title": title, "kind": "sheet"})
        for t in coverage:
            c = coverage[t]
            c["untouched"] = c["built"] - c["done"]
            c["notes"] = notes.get(t, 0)
            c["pct"] = round(c["done"] / c["built"] * 100, 1) if c["built"] else 0.0

        # re-do candidates: last sitting was below par or left unfinished,
        # and no later sitting of the same sheet has cleared it
        redo = []
        title_to_id = {ti: sid for sid, (tr, ti, isn) in cat.items() if not isn}
        for title, s in best_by_title.items():
            pct = s["correct"] / s["n"] * 100
            if pct >= 95 and not s["blank"]:
                continue
            redo.append({
                "id": title_to_id.get(title), "worksheet": title, "track": s["track"],
                "score": f'{s["correct"]}/{s["n"]}', "accuracy": round(pct),
                "blank": s["blank"], "wrong": s["wrong"], "date": s["date"],
                "reason": "unfinished" if s["blank"] >= s["wrong"] and s["blank"] else "below par",
            })
        redo.sort(key=lambda r: (r["accuracy"], r["date"]))

        catalogue = {
            "built": sum(c["built"] for c in coverage.values()),
            "attempted": sum(c["done"] for c in coverage.values()),
            "untouched_count": sum(c["untouched"] for c in coverage.values()),
            "notes_total": sum(notes.values()),
            "coverage": OrderedDict(sorted(coverage.items(), key=lambda kv: -kv[1]["untouched"])),
            "untouched": sorted(untouched, key=lambda u: (u["track"], u["id"])),
            "redo_candidates": redo,
        }

    out = {
        "generated_for_data_through": max((s["date"] for s in best), default=None),
        "period_start_exclusive": since,
        "period": {
            "totals": totals(period),
            "tracks": track_rollup(period),
            "sheets": [{k: s[k] for k in ("date", "worksheet", "track", "n", "correct", "blank", "wrong")}
                       for s in period],
        },
        "cumulative": {
            "totals": totals(best),
            "tracks": track_rollup(best),
        },
        "prior_totals": totals(prior) if prior else None,
        "daily": daily,
        "errors": errors,
        "taxonomy": OrderedDict(sorted(tax.items(), key=lambda kv: -kv[1])),
        "repeated_facts": repeated_facts,
        "unfinished_sheets": unfinished,
        "abandoned_attempts": abandoned,
        "retries": retries,
        "catalogue": catalogue,
        "previous_state": state or None,
    }

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)

    t = out["period"]["totals"]
    print(f"period: {t['sheets']} sheets, {t['questions']} questions, "
          f"{t['accuracy']}% — {len(errors)} misses in {len(tax)} classes", file=sys.stderr)
    print(args.out)


if __name__ == "__main__":
    main()
