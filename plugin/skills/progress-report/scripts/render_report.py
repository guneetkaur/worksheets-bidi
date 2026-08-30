#!/usr/bin/env python3
"""
render_report.py — turn analysis.json + narrative.json into the report HTML.

The house style lives here, not in the model's head, so every report in the
series looks like the same document. Claude supplies the prose in narrative.json;
every number comes from analysis.json.

Usage:
    python3 render_report.py --analysis /tmp/analysis.json \
                             --narrative /tmp/narrative.json \
                             --out reports/index.html
"""

import argparse
import html
import json
import re
from datetime import date as _date

STATUS_CLASS = {
    "mastered": "good", "on-track": "good", "closed": "good",
    "in-progress": "watch", "improving": "watch", "watch": "watch",
    "blocked": "gap", "new": "gap", "open": "gap",
    "not-started": "neutral", "untaught": "neutral", "carried": "neutral",
}

TAXONOMY_LABELS = {
    "blank": ("Not attempted", "Left empty — fatigue, unfamiliarity, or ran out of sheet"),
    "wrong-rule": ("Wrong rule", "A systematic misconception applied more than once"),
    "wrong-fact": ("Wrong stored fact", "One memorised answer is wrong"),
    "operation-confusion": ("Wrong operation", "Answer is right for a different operation"),
    "transcription": ("Transcription", "Knew it, wrote it wrong — reversal, smear, misaligned row"),
    "near-miss": ("Near miss", "Off by a step, no pattern"),
    "wrong-choice": ("Wrong option", "Multiple-choice miss, no arithmetic to inspect"),
    "untaught": ("Untaught", "Content never covered"),
}


def e(s):
    return html.escape(str(s if s is not None else ""))


def fmt_delta(now, before):
    """Returns (big value, caption) for the change tile."""
    if before is None or now is None:
        return "—", "first report in the series"
    d = round(now - before, 1)
    if abs(d) < 0.05:
        return "level", f"same as the {before}% before it"
    return f"{d:+.1f}", f"points against {before}% last period"


def sparkline(daily, period_start):
    """Whole-history accuracy line; days inside this period drawn emphasised."""
    if len(daily) < 2:
        return ""
    W, H, L, R, T, B = 980, 200, 44, 16, 14, 34
    iw, ih = W - L - R, H - T - B
    lo = min(40, min(d["accuracy"] for d in daily) - 5)
    span = 100 - lo

    def X(i):
        return round(L + iw * i / (len(daily) - 1), 1)

    def Y(v):
        return round(T + ih * (100 - v) / span, 1)

    pts = [(X(i), Y(d["accuracy"])) for i, d in enumerate(daily)]
    line = " ".join(f"{x},{y}" for x, y in pts)
    area = f"{pts[0][0]},{T+ih} " + line + f" {pts[-1][0]},{T+ih}"

    grid, labels = [], []
    for g in (40, 60, 80, 100):
        if g < lo:
            continue
        grid.append(f'<line class="grid-line" x1="{L}" y1="{Y(g)}" x2="{W-R}" y2="{Y(g)}"></line>')
        labels.append(f'<text class="axis-txt" x="{L-8}" y="{Y(g)+4}" text-anchor="end">{g}{"%" if g==100 else ""}</text>')

    band = ""
    if period_start:
        idx = [i for i, d in enumerate(daily) if d["date"] > period_start]
        if idx:
            x0 = X(max(idx[0] - 1, 0))
            band = f'<rect class="period-band" x="{x0}" y="{T}" width="{W-R-x0}" height="{ih}"></rect>'

    dots, ticks = [], []
    step = max(1, len(daily) // 9)
    for i, (d, (x, y)) in enumerate(zip(daily, pts)):
        cls = "series-dot" if (not period_start or d["date"] > period_start) else "series-dot faded"
        dots.append(
            f'<circle class="{cls}" cx="{x}" cy="{y}" r="4">'
            f'<title>{e(d["date"])} — {d["accuracy"]}% ({d["correct"]}/{d["questions"]}'
            f'{", " + str(d["blank"]) + " blank" if d["blank"] else ""})</title></circle>')
        if i % step == 0 or i == len(daily) - 1:
            anchor = "end" if i == len(daily) - 1 else "middle"
            xx = x + 10 if i == len(daily) - 1 else x
            ticks.append(f'<text class="axis-txt" x="{xx}" y="{H-12}" text-anchor="{anchor}">{e(d["date"][5:])}</text>')

    return f"""<figure class="chart">
  <figcaption>Accuracy per practice day, whole history. The shaded span is this reporting period. Hover any point for the sheet count and blanks.</figcaption>
  <svg viewBox="0 0 {W} {H}" role="img" aria-label="Accuracy per practice day across the whole history.">
    {band}
    {''.join(grid)}
    {''.join(labels)}
    <polygon class="series-area" points="{area}"></polygon>
    <polyline class="series-line" points="{line}"></polyline>
    {''.join(dots)}
    {''.join(ticks)}
  </svg>
</figure>"""


def chip(label, status):
    cls = STATUS_CLASS.get((status or "").lower(), "neutral")
    return f'<span class="chip {cls}"><span class="dot"></span>{e(label)}</span>'


def tile(k, v, s):
    return f'<div class="tile"><div class="k">{e(k)}</div><div class="v">{e(v)}</div><div class="s">{e(s)}</div></div>'


def bars(tracks):
    rows = []
    for name, t in tracks.items():
        if not t.get("accuracy"):
            continue
        rows.append(
            f'<div class="bar-row"><span>{e(name)}</span>'
            f'<span class="bar-track"><span class="bar-fill" style="width:{t["accuracy"]}%"></span></span>'
            f'<span class="bar-val">{t["correct"]}/{t["questions"]} · {round(t["accuracy"])}%</span></div>')
    return '<div class="bars">' + "".join(rows) + "</div>"


def after_cell(v):
    """The 'give after' column: bare sheet ids get the id chip, prose passes through."""
    if not v:
        return "&mdash;"
    return f'<span class="sid">{e(v)}</span>' if re.fullmatch(r"[a-z0-9][a-z0-9-]*", v) else v


def error_table(errors, limit=None):
    shown = errors[:limit] if limit else errors
    body = "".join(
        f'<tr><td class="num">{e(x["question"])[:70]}</td>'
        f'<td class="num wrong">{e(x["given"]) or "blank"}</td>'
        f'<td class="num right">{e(x["correct"])}</td>'
        f'<td>{e(x["note"] or TAXONOMY_LABELS.get(x["class"], (x["class"], ""))[0])}</td>'
        f'<td class="mono muted-cell">{e(x["date"][5:])}</td></tr>' for x in shown)
    more = ""
    if limit and len(errors) > limit:
        more = f'<p class="tablenote">{len(errors) - limit} further misses of this kind not listed.</p>'
    return ('<div class="scroll"><table><thead><tr><th>Question</th><th class="num">Wrote</th>'
            '<th class="num">Correct</th><th>What happened</th><th>Date</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div>{more}')


def build(a, n):
    p, cum = a["period"]["totals"], a["cumulative"]["totals"]
    prior = a.get("prior_totals") or {}
    title = n.get("title") or "Ambar Progress Report"
    period_label = n.get("period_label") or f'through {a["generated_for_data_through"]}'

    # ---- tiles
    dv, dc = fmt_delta(p["accuracy"], prior.get("accuracy"))
    tiles = [
        tile("This period", f'{p["accuracy"]}%', f'{p["correct"]} of {p["questions"]} · {p["sheets"]} sheets over {p["days"]} days'),
        tile("Change", dv, dc),
        tile("All time", f'{cum["accuracy"]}%', f'{cum["correct"]:,} of {cum["questions"]:,} · {cum["days"]} practice days'),
        tile("Open gaps", str(len([g for g in n.get("gaps", []) if g.get("status", "").lower() not in ("closed",)])),
             n.get("gaps_caption", "carried until evidence closes them")),
    ]

    # ---- gate board
    gate_rows = "".join(
        f'<tr><td><strong>{e(g["track"])}</strong></td><td>{e(g.get("stage",""))}</td>'
        f'<td>{chip(g.get("status_label", g.get("status","")), g.get("status",""))}</td>'
        f'<td class="mono">{e(g.get("evidence",""))}</td><td>{e(g.get("next_gate",""))}</td></tr>'
        for g in n.get("gates", []))
    gate_board = (
        '<div class="scroll"><table><thead><tr><th>Track</th><th>Where she is</th><th>Status</th>'
        '<th>Last evidence</th><th>Next gate</th></tr></thead>'
        f'<tbody>{gate_rows}</tbody></table></div>') if gate_rows else ""

    # ---- gap cards
    err_by_id = {}
    for g in n.get("gaps", []):
        notes = set(g.get("error_notes", []))
        classes = set(g.get("error_classes", []))
        qre = re.compile(g["question_match"]) if g.get("question_match") else None
        wre = re.compile(g["worksheet_match"]) if g.get("worksheet_match") else None
        if not (notes or classes or qre or wre):
            err_by_id[g["id"]] = []
            continue
        sel = []
        for x in a["errors"]:
            if notes and x["note"] not in notes:
                continue
            if classes and x["class"] not in classes:
                continue
            if qre and not qre.search(x["question"]):
                continue
            if wre and not wre.search(x["worksheet"]):
                continue
            sel.append(x)
        err_by_id[g["id"]] = sel

    gap_cards = ""
    for g in n.get("gaps", []):
        st = g.get("status", "open").lower()
        rows = err_by_id.get(g["id"]) or []
        tbl = error_table(rows, limit=g.get("evidence_limit", 12)) if rows else ""
        opened = f'<span class="meta">opened {e(g.get("opened",""))}</span>' if g.get("opened") else ""
        gap_cards += f"""<div class="card stripe {STATUS_CLASS.get(st,'gap')}">
  <div class="card-head">
    <div><div class="kicker">{e(g.get("track",""))} {opened}</div><h3>{e(g["title"])}</h3></div>
    {chip(g.get("status_label", st), st)}
  </div>
  <p>{g["what"]}</p>
  {tbl}
  <p class="fix"><strong>Fix:</strong> {g["fix"]}</p>
</div>"""

    # ---- taxonomy
    tax_rows = "".join(
        f'<tr><td><strong>{e(TAXONOMY_LABELS.get(k,(k,""))[0])}</strong></td>'
        f'<td>{e(TAXONOMY_LABELS.get(k,("",""))[1])}</td><td class="num">{v}</td></tr>'
        for k, v in a["taxonomy"].items())
    tax = ('<div class="scroll"><table><thead><tr><th>Class</th><th>Meaning</th><th class="num">Count</th>'
           f'</tr></thead><tbody>{tax_rows}</tbody></table></div>') if tax_rows else ""

    # ---- retries
    retry_cards = ""
    for r in a.get("retries", []):
        seq = " → ".join(f'<span class="mono">{e(x["score"])}</span> <span class="meta">{e(x["date"][5:])}</span>'
                         for x in r["attempts"])
        retry_cards += f'<li><strong>{e(r["worksheet"])}</strong><p>{seq}</p></li>'
    retries = f'<ul class="retries">{retry_cards}</ul>' if retry_cards else ""

    # ---- unfinished
    unf_rows = "".join(
        f'<tr><td>{e(u["worksheet"])}</td><td class="num">{u["correct"]}/{u["n"]}</td>'
        f'<td class="num">{u["blank"]}</td><td class="mono">{e(u["date"][5:])}</td></tr>'
        for u in a.get("unfinished_sheets", []))
    unfinished = ('<div class="scroll"><table><thead><tr><th>Sheet</th><th class="num">Score</th>'
                  f'<th class="num">Blank</th><th>Date</th></tr></thead><tbody>{unf_rows}</tbody></table></div>'
                  ) if unf_rows else '<p>No sheet was left unfinished this period.</p>'

    # ---- actions
    act = "".join(
        f'<li><div><strong>{e(x["title"])}</strong><p>{x["why"]}</p></div></li>'
        for x in n.get("actions", []))
    carried = ""
    if n.get("carried_actions"):
        carried = '<div class="card"><div class="kicker">From last report</div><ul class="plain">' + "".join(
            f'<li>{chip(c.get("status_label", c.get("status","open")), c.get("status","open"))} {c["title"]}</li>'
            for c in n["carried_actions"]) + "</ul></div>"

    sections = []
    if n.get("headline"):
        sections.append(f'<section class="headline"><p class="lede">{n["headline"]}</p></section>')

    sections.append(f"""<section>
  <div class="sec-head"><h2>Since the last report</h2><span class="note">{e(period_label)}</span></div>
  {n.get("since_last", "")}
  {sparkline(a["daily"], a.get("period_start_exclusive"))}
</section>""")

    if gate_board:
        sections.append(f"""<section>
  <div class="sec-head"><h2>Where each track stands</h2><span class="note">Gate board</span></div>
  {gate_board}
</section>""")

    if gap_cards:
        sections.append(f"""<section>
  <div class="sec-head"><h2>Open gaps</h2><span class="note">Carried until the evidence closes them</span></div>
  {gap_cards}
</section>""")

    sections.append(f"""<section>
  <div class="sec-head"><h2>Every miss, classified</h2><span class="note">{p["wrong"] + p["blank"]} misses this period</span></div>
  <p>Blanks and wrong answers need opposite responses — a blank sheet gets re-given early in a session, a wrong sheet gets taught. They are counted separately throughout.</p>
  {tax}
</section>""")

    if a.get("repeated_facts"):
        rf = "".join(
            f'<tr><td class="num">{e(r["question"])}</td><td class="num wrong">{e(r["given"])}</td>'
            f'<td class="num">{r["times"]}&times;</td><td class="mono">{e(", ".join(d[5:] for d in r["dates"]))}</td></tr>'
            for r in a["repeated_facts"])
        sections.append(f"""<section>
  <div class="sec-head"><h2>Same answer, more than once</h2><span class="note">Stored wrong, not guessed</span></div>
  <p>A miss repeated identically is a memorised-wrong fact rather than a slip. These are the cheapest things on the list to fix.</p>
  <div class="scroll"><table><thead><tr><th>Question</th><th class="num">Answer given</th>
  <th class="num">Times</th><th>Dates</th></tr></thead><tbody>{rf}</tbody></table></div>
</section>""")

    sections.append(f"""<section>
  <div class="sec-head"><h2>Re-attempts and unfinished sheets</h2><span class="note">The learning signal</span></div>
  {('<h3 class="sub">Sheets she came back to</h3>' + retries) if retries else ''}
  <h3 class="sub">Left unfinished</h3>
  {unfinished}
</section>""")

    sections.append(f"""<section>
  <div class="sec-head"><h2>By track</h2><span class="note">This period</span></div>
  <div class="card">{bars(a["period"]["tracks"])}
  <p class="tablenote">{e(n.get("tracks_note", "Small denominators move these bars a long way — read them next to the sheet counts, not on their own."))}</p></div>
</section>""")

    sections.append(f"""<section>
  <div class="sec-head"><h2>What to do next</h2><span class="note">In order</span></div>
  <ol class="actions">{act}</ol>
  {carried}
</section>""")

    # ---- the assignment plan: re-do / assign / build ----------------------
    cat = a.get("catalogue")
    if n.get("redo"):
        rows = "".join(
            f'<tr><td><span class="sid">{e(r.get("id",""))}</span><br>'
            f'<span class="muted-cell">{r.get("sheet","")}</span></td>'
            f'<td class="num">{r.get("standing","")}<br><span class="muted-cell">{r.get("when","")}</span></td>'
            f'<td>{r.get("why","")}</td><td>{after_cell(r.get("after",""))}</td></tr>'
            for r in n["redo"])
        sections.append(f"""<section>
  <div class="sec-head"><h2>Do again</h2><span class="note">{len(n["redo"])} sheets, all already built</span></div>
  <p>{n.get("redo_note", "Each of these has an unresolved score against it. Nothing here is busywork — every one settles a specific open question.")}</p>
  <div class="scroll"><table><thead><tr><th>Sheet</th><th>Where it stands</th><th>Why re-give it</th><th>Give after</th></tr></thead>
  <tbody>{rows}</tbody></table></div>
</section>""")

    if cat:
        cov = "".join(
            f'<div class="bar-row"><span>{e(t)}</span>'
            f'<span class="bar-track"><span class="bar-fill" style="width:{c["pct"]}%"></span></span>'
            f'<span class="bar-val">{c["done"]} / {c["built"]} done</span></div>'
            for t, c in sorted(cat["coverage"].items(), key=lambda kv: -kv[1]["pct"]))
        assign = ""
        if n.get("assign_next"):
            arows = "".join(
                f'<tr><td><strong>{e(r["track"])}</strong></td><td>{r["sheets"]}</td><td>{r["why"]}</td></tr>'
                for r in n["assign_next"])
            assign = f"""<div class="card stripe watch" style="margin-top:16px">
  <h3>The ones worth assigning next, per track</h3>
  <div class="scroll"><table><thead><tr><th>Track</th><th>Assign next</th><th>Why this one</th></tr></thead>
  <tbody>{arows}</tbody></table></div>
</div>"""
        sections.append(f"""<section>
  <div class="sec-head"><h2>Already written, never opened</h2><span class="note">{cat["untouched_count"]} sheets</span></div>
  <p class="lede">She has attempted {cat["attempted"]} of the {cat["built"]} sheets in the app. Every track has a queue.</p>
  <div class="card"><div class="bars">{cov}</div>
  <p class="tablenote">{n.get("coverage_note", f'There are also {cat["notes_total"]} deep-dive notes in the app, none of them recorded as read.')}</p></div>
  {assign}
</section>""")

    if n.get("build"):
        cards = ""
        for i, b in enumerate(n["build"], 1):
            kicker = b.get("kicker") or f'{i} &middot; {b.get("kind", "drill")}'
            cards += f"""<div class="card stripe {STATUS_CLASS.get(b.get("priority","open"), "neutral")}">
  <div class="kicker">{kicker}</div>
  <h3>{e(b["title"])}</h3>
  <p>{b["what"]}</p>
  <p class="fix"><strong>Settles:</strong> {b["settles"]}</p>
</div>"""
        sections.append(f"""<section>
  <div class="sec-head"><h2>Build these</h2><span class="note">Nothing in the app covers them</span></div>
  <p>{n.get("build_note", "Each exists to settle a question the current sheets cannot answer.")}</p>
  {cards}
</section>""")

    if n.get("schedule"):
        weeks = "".join(
            f'<div class="week"><h3>{e(w["title"])}</h3><ol>'
            + "".join(f"<li>{item}</li>" for item in w["items"]) + "</ol></div>"
            for w in n["schedule"])
        tail = f'<div class="card stripe good" style="margin-top:20px"><h3>{e(n["schedule_note_title"])}</h3><p style="margin-bottom:0">{n["schedule_note"]}</p></div>' if n.get("schedule_note") else ""
        sections.append(f"""<section>
  <div class="sec-head"><h2>{e(n.get("schedule_heading", "A suggested order"))}</h2><span class="note">{e(n.get("schedule_note_label", "Next few weeks"))}</span></div>
  <div class="weeks">{weeks}</div>
  {tail}
</section>""")

    body = "\n".join(sections)
    gen = n.get("generated_on") or _date.today().isoformat()

    return f"""<title>{e(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,500;0,600;1,500&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
<header class="mast">
  <div class="mast-in">
    <p class="eyebrow">{e(n.get("eyebrow", "Worksheet results"))} &middot; {e(period_label)} &middot; Class III</p>
    <h1>{e(title)}</h1>
    <p class="dek">{n.get("dek", "")}</p>
    <div class="tiles">{''.join(tiles)}</div>
  </div>
</header>
<div class="wrap">
{body}
<p class="footnote">
  Generated {e(gen)} from <code>results/results.csv</code> in this repository — {cum["questions"]} answers across {cum["sheets"]} sheets, data through {e(a["generated_for_data_through"])}.<br><br>
  Method: repeated &ldquo;Finish &amp; Check&rdquo; presses inside one sitting collapse into a single attempt; where a sheet was attempted more than once on the same day the best attempt is counted, and the other attempts are reported separately when they were abandoned. Blanks count as incorrect but are tracked apart from wrong answers throughout. <code>total_time_s</code> in this file is unreliable, so no speed claims are made.<br><br>
  Earlier reports are kept alongside this one in <code>reports/</code>.
</p>
</div>"""


CSS = """
:root{--ground:#F4F3F8;--surface:#FFFFFF;--surface-2:#FAF9FC;--band:#EFEDF6;
--ink:#191727;--ink-2:#403C56;--muted:#6B6685;--line:#E1DEEB;
--accent:#3B3A8F;--accent-2:#6462C4;--accent-soft:#EBEAF7;
--good:#1C7048;--good-soft:#E4F2EA;--watch:#8C5B06;--watch-soft:#FAEFDA;
--gap:#A83226;--gap-soft:#FAE8E5;
--shadow:0 1px 2px rgba(25,23,39,.05),0 8px 24px -14px rgba(25,23,39,.22)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
--ground:#121120;--surface:#1B1929;--surface-2:#222032;--band:#232135;
--ink:#EFEDF7;--ink-2:#C7C2DA;--muted:#948FAE;--line:#302D45;
--accent:#A6A3F2;--accent-2:#8482DE;--accent-soft:#252347;
--good:#5FCB92;--good-soft:#16301F;--watch:#E3A947;--watch-soft:#33280F;
--gap:#F0836F;--gap-soft:#361C1A;
--shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -16px rgba(0,0,0,.7)}}
:root[data-theme="dark"]{
--ground:#121120;--surface:#1B1929;--surface-2:#222032;--band:#232135;
--ink:#EFEDF7;--ink-2:#C7C2DA;--muted:#948FAE;--line:#302D45;
--accent:#A6A3F2;--accent-2:#8482DE;--accent-soft:#252347;
--good:#5FCB92;--good-soft:#16301F;--watch:#E3A947;--watch-soft:#33280F;
--gap:#F0836F;--gap-soft:#361C1A;
--shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -16px rgba(0,0,0,.7)}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
font-family:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px 88px}
h1,h2,h3{font-family:Spectral,"Iowan Old Style",Georgia,serif;font-weight:600;text-wrap:balance;margin:0}
a{color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:3px}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
.mast{border-bottom:1px solid var(--line);
background:repeating-linear-gradient(to right,var(--line) 0 1px,transparent 1px 28px),
repeating-linear-gradient(to bottom,var(--line) 0 1px,transparent 1px 28px),var(--surface)}
.mast-in{max-width:1080px;margin:0 auto;padding:44px 24px 34px;background:linear-gradient(to bottom,transparent,var(--surface) 88%)}
.eyebrow{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
h1{font-size:clamp(32px,5vw,48px);line-height:1.06;letter-spacing:-.015em}
.dek{margin:14px 0 0;max-width:62ch;color:var(--ink-2);font-size:17px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:26px 0 0}
.tile{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 18px;box-shadow:var(--shadow)}
.tile .k{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.tile .v{font-family:Spectral,Georgia,serif;font-size:31px;line-height:1.15;margin-top:7px;font-variant-numeric:tabular-nums}
.tile .s{font-size:13.5px;color:var(--muted);margin-top:3px}
section{margin-top:56px}
section.headline{margin-top:44px}
.sec-head{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:22px}
.sec-head h2{font-size:26px;letter-spacing:-.01em}
.sec-head .note,.meta{font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
h3.sub{font-size:17px;margin:22px 0 10px}
p{margin:0 0 14px;max-width:68ch}
.lede{font-size:18px;color:var(--ink-2)}
.tablenote{font-size:14px;color:var(--muted);margin-top:14px}
.chip{display:inline-flex;align-items:center;gap:6px;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;padding:3px 9px;border-radius:999px;border:1px solid transparent;white-space:nowrap}
.chip.good{background:var(--good-soft);color:var(--good);border-color:var(--good)}
.chip.watch{background:var(--watch-soft);color:var(--watch);border-color:var(--watch)}
.chip.gap{background:var(--gap-soft);color:var(--gap);border-color:var(--gap)}
.chip.neutral{background:var(--accent-soft);color:var(--accent);border-color:var(--accent)}
.chip .dot{width:6px;height:6px;border-radius:50%;background:currentColor}
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:22px 24px;box-shadow:var(--shadow)}
.card+.card{margin-top:16px}
.card h3{font-size:20px;margin-bottom:4px}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap;margin-bottom:12px}
.stripe{border-left:3px solid var(--line)}
.stripe.gap{border-left-color:var(--gap)}
.stripe.watch{border-left-color:var(--watch)}
.stripe.good{border-left-color:var(--good)}
.stripe.neutral{border-left-color:var(--accent)}
.kicker{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.fix{margin:14px 0 0;padding-top:12px;border-top:1px solid var(--line);max-width:none}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:14.5px;min-width:440px}
th,td{text-align:left;padding:8px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:500;border-bottom:1px solid var(--ink-2)}
td.num,th.num,.mono{font-family:"IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:none}
.wrong{color:var(--gap);font-weight:500}
.right{color:var(--good);font-weight:500}
.muted-cell{color:var(--muted)}
.bars{display:grid;gap:10px}
.bar-row{display:grid;grid-template-columns:minmax(140px,1.1fr) 1fr auto;gap:14px;align-items:center;font-size:14.5px}
.bar-track{height:9px;border-radius:3px;background:var(--band);position:relative;overflow:hidden}
.bar-fill{position:absolute;inset:0 auto 0 0;border-radius:3px;background:var(--accent-2)}
.bar-val{font-family:"IBM Plex Mono",monospace;font-size:13px;font-variant-numeric:tabular-nums;color:var(--ink-2);min-width:88px;text-align:right}
.chart{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px 20px 8px;box-shadow:var(--shadow);margin:22px 0 0}
.chart figcaption{font-size:13.5px;color:var(--muted);margin:2px 0 12px;max-width:68ch}
.chart svg{display:block;width:100%;height:auto}
.grid-line{stroke:var(--line);stroke-width:1}
.period-band{fill:var(--accent-2);opacity:.06}
.axis-txt{font-family:"IBM Plex Mono",monospace;font-size:10.5px;fill:var(--muted)}
.series-line{fill:none;stroke:var(--accent-2);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.series-area{fill:var(--accent-2);opacity:.10}
.series-dot{fill:var(--surface);stroke:var(--accent-2);stroke-width:2}
.series-dot.faded{opacity:.45}
.series-dot:hover{fill:var(--accent-2)}
ol.actions{counter-reset:a;list-style:none;padding:0;margin:0;display:grid;gap:12px}
ol.actions li{counter-increment:a;display:grid;grid-template-columns:34px 1fr;gap:14px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 18px;box-shadow:var(--shadow)}
ol.actions li::before{content:counter(a);font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--accent);border:1px solid var(--accent);border-radius:6px;height:28px;display:grid;place-items:center}
ol.actions strong{display:block;font-size:16px;margin-bottom:2px}
ol.actions p{margin:0;font-size:14.5px;color:var(--ink-2)}
ul.retries{list-style:none;padding:0;margin:0;display:grid;gap:10px}
ul.retries li{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 18px;box-shadow:var(--shadow)}
ul.retries p{margin:4px 0 0}
ul.plain{margin:0;padding-left:20px}
ul.plain li{margin-bottom:8px;max-width:66ch}
.sid{font-family:"IBM Plex Mono",monospace;font-size:12.5px;background:var(--band);padding:2px 7px;border-radius:4px;white-space:nowrap;color:var(--ink-2)}
.weeks{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.week{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px 20px;box-shadow:var(--shadow)}
.week h3{font-size:17px;margin-bottom:10px}
.week ol{margin:0;padding-left:20px;font-size:14.5px}
.week li{margin-bottom:7px}
.footnote{margin-top:56px;padding-top:20px;border-top:1px solid var(--line);font-size:13.5px;color:var(--muted);max-width:none}
.footnote code{font-family:"IBM Plex Mono",monospace;font-size:12.5px;background:var(--band);padding:1px 5px;border-radius:4px;overflow-wrap:anywhere}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--narrative", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with open(args.analysis, encoding="utf-8") as fh:
        a = json.load(fh)
    with open(args.narrative, encoding="utf-8") as fh:
        n = json.load(fh)

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(build(a, n))
    print(args.out)


if __name__ == "__main__":
    main()
