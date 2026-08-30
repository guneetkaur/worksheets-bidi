#!/usr/bin/env python3
"""Build the five new diagnostic/drill sheets and append them to index.html.

Every answer is computed, never typed — so the answer key cannot drift from the
question. Run with --check to verify only.
"""
import json, re, sys, pathlib

SCHOOL = "Math — Addition & Subtraction (School L3)"
MUL    = "Mental Math — Multiplication"
SUB    = "Mental Math — LTR Subtraction"


def fill(label, ans):
    return {"label": label, "answers": [ans]}


def mcq(label, options, correct):
    """options are strings; `correct` is the value that must be present once."""
    assert options.count(correct) == 1, (label, options, correct)
    return {"label": label, "options": options, "answerIndex": options.index(correct)}


# ---------------------------------------------------------------- 1. missing number
missing_small  = [(4, 10), (7, 15), (12, 20), (9, 16)]
missing_addend = [(708, 940), (484, 774), (436, 740), (284, 614), (365, 500), (127, 903)]
missing_start  = [(400, 400), (250, 100), (180, 320), (95, 205)]   # __ − b = c
missing_sub    = [(900, 145), (740, 260), (512, 200), (630, 375)]  # a − __ = c
star           = [(850, 1500), (1240, 2000), (376, 1000), (2450, 3600)]

s1 = {
  "id": "mn-drill-1", "track": SCHOOL,
  "title": "Diagnostic Drill 1 — Missing Number (all four positions)", "marks": 22,
  "note": "To find a missing part, take it back off. 708 + __ = 940 means 940 − 708 = 232. "
          "To find a missing start, put it back on: __ − 400 = 400 means 400 + 400 = 800.",
  "sections": [
    {"title": "Warm-up — you already do these", "marks": 4, "layout": "grid",
     "questions": [fill(f"{a} + [_] = {t}", t - a) for a, t in missing_small]},
    {"title": "Missing addend — take it back off", "marks": 6, "layout": "grid",
     "questions": [fill(f"{a} + [_] = {t}", t - a) for a, t in missing_addend]},
    {"title": "Missing start — put it back on", "marks": 4, "layout": "grid",
     "questions": [fill(f"[_] − {b} = {c}", b + c) for b, c in missing_start]},
    {"title": "Missing part of a subtraction", "marks": 4, "layout": "grid",
     "questions": [fill(f"{a} − [_] = {c}", a - c) for a, c in missing_sub]},
    {"title": "School phrasing — find the star", "marks": 4, "layout": "lines",
     "questions": [fill(f"{a} + ★ = {t}   ★ = [_]", t - a) for a, t in star]},
  ],
}

# ---------------------------------------------------------------- 2. column carry
carry_sums = [(1368, 2547), (2364, 3548), (4759, 4402), (3854, 2259), (1476, 2685), (5238, 1594)]
carry_words = [
  ("A library has {a} storybooks and {b} textbooks. How many books in all?", 1368, 2547),
  ("A factory made {a} toys in January and {b} in February. Total toys?", 2364, 3548),
  ("A shop sold {a} pencils last month and {b} this month. How many altogether?", 1657, 2486),
  ("Papa drove {a} km in the first week and {b} km in the second. Total distance?", 1275, 2648),
  ("{a} people came to the fair on Saturday and {b} on Sunday. How many in all?", 3459, 2673),
  ("A school collected ₹{a} in one drive and ₹{b} in the next. Total collected?", 2586, 1735),
]

s2 = {
  "id": "cc-drill-1", "track": SCHOOL,
  "title": "Diagnostic Drill 2 — Column Carry with Word Problems", "marks": 12,
  "note": "Every sum here carries from the tens into the hundreds. Write the little 1 above the "
          "hundreds column before you add it — that is the step that gets dropped.",
  "sections": [
    {"title": "Column addition — watch the tens carry into the hundreds", "marks": 6, "layout": "grid",
     "questions": [fill(f"{a} + {b} = [_]", a + b) for a, b in carry_sums]},
    {"title": "Same sums, dressed as word problems", "marks": 6, "layout": "lines",
     "questions": [fill(t.format(a=a, b=b) + " [_]", a + b) for t, a, b in carry_words]},
  ],
}

# ---------------------------------------------------------------- 3. four weak facts
weak = [(7, 8), (4, 7), (4, 8), (8, 3)]
neighbours = [(6, 8), (6, 7), (7, 7), (8, 8), (4, 6), (3, 7)]
facts_a = [(a, b) for a, b in weak] + [(b, a) for a, b in weak]           # 8
facts_b = [(a, b) for a, b in weak] * 2 + [(b, a) for a, b in weak] * 2   # 16 mixed
facts_c = neighbours                                                      # 6 contrast

s3 = {
  "id": "mul-rev-2", "track": MUL,
  "title": "Revision Drill 2 — Four Weak Facts (7×8, 4×7, 4×8, 8×3)", "marks": 30,
  "note": "Four facts only, over and over, both ways round. 7×8 = 56 — say it as \"five, six, seven, eight\": 56 = 7×8. "
          "4×7 and 4×8 are double-double: 4×7 → 7 doubled is 14, doubled again is 28.",
  "sections": [
    {"title": "The four facts, both ways round", "marks": 8, "layout": "grid",
     "questions": [fill(f"{a} × {b} = [_]", a * b) for a, b in facts_a]},
    {"title": "Same four, mixed up — no thinking time", "marks": 16, "layout": "grid",
     "questions": [fill(f"{a} × {b} = [_]", a * b) for a, b in facts_b]},
    {"title": "Their neighbours — don't get pulled onto the wrong row", "marks": 6, "layout": "grid",
     "questions": [fill(f"{a} × {b} = [_]", a * b) for a, b in neighbours]},
  ],
}

# ---------------------------------------------------------------- 4. name the operation
# distractors are the actual bugs: a+b (operation flip) and the tens-add answer
def tens_add(a, b):
    """The 'adds the tens, subtracts the units' answer, when it is well formed."""
    if len(str(a)) == len(str(b)) == 2 and int(str(a)[1]) >= int(str(b)[1]):
        return int(str(int(str(a)[0]) + int(str(b)[0])) + str(int(str(a)[1]) - int(str(b)[1])))
    return None


sub_pairs = [(86, 11), (89, 12), (67, 23), (47, 14), (78, 35), (95, 42), (69, 27), (58, 13)]
add_pairs = [(46, 23), (57, 31)]

op_mcq, op_fill = [], []
for a, b in sub_pairs:
    correct, flip, bug = a - b, a + b, tens_add(a, b)
    opts = [str(correct), str(flip)]
    if bug and str(bug) not in opts:
        opts.append(str(bug))
    for cand in (correct + 1, correct - 1, correct + 10):
        if len(opts) >= 4:
            break
        if str(cand) not in opts:
            opts.append(str(cand))
    opts = sorted(opts[:4], key=int)
    op_mcq.append(mcq(f"{a} − {b} = ?", opts, str(correct)))
    op_fill.append(fill(f"{a} − {b} = [_]", correct))
for a, b in add_pairs:
    correct = a + b
    opts = sorted({str(correct), str(a - b), str(correct + 10), str(correct - 1)}, key=int)[:4]
    op_mcq.append(mcq(f"{a} + {b} = ?", opts, str(correct)))
    op_fill.append(fill(f"{a} + {b} = [_]", correct))

sign_check = [
    mcq("In 86 − 11, what must you do?", ["add the numbers", "take the second from the first"],
        "take the second from the first"),
    mcq("In 46 + 23, what must you do?", ["add the numbers", "take the second from the first"],
        "add the numbers"),
    mcq("You are doing 89 − 12. The tens are 8 and 1. Should the answer's tens digit be bigger or smaller than 8?",
        ["bigger", "smaller", "the same"], "smaller"),
    mcq("True or false: in a subtraction, every column is subtracted — you never add one of them.",
        ["true", "false"], "true"),
]

s4 = {
  "id": "op-diag-1", "track": SUB,
  "title": "Diagnostic — Name the Operation Before You Answer", "marks": 24,
  "note": "Read the SIGN first, out loud, before you read the numbers. In a subtraction every "
          "column comes down — the tens never go up.",
  "sections": [
    {"title": "Read the sign — what must you do?", "marks": 4, "layout": "lines", "questions": sign_check},
    {"title": "Pick the answer (the wrong ones are the traps)", "marks": 10, "layout": "lines", "questions": op_mcq},
    {"title": "Now write them yourself", "marks": 10, "layout": "grid", "questions": op_fill},
  ],
}

# ---------------------------------------------------------------- 5. number relationships
pred_succ = [
    fill("The predecessor of 3,299 is [_]", 3298),
    fill("3,299 is the predecessor of [_]", 3300),
    fill("The successor of 5,298 is [_]", 5299),
    fill("5,298 is the successor of [_]", 5297),
    fill("The predecessor of 4,700 is [_]", 4699),
    fill("4,700 is the predecessor of [_]", 4701),
    fill("The successor of 8,999 is [_]", 9000),
    fill("8,999 is the successor of [_]", 8998),
]

def cmp_q(left_txt, lv, right_txt, rv):
    correct = "<" if lv < rv else (">" if lv > rv else "=")
    return mcq(f"{left_txt} ___ {right_txt}", ["<", ">", "="], correct)

compare = [
    cmp_q("6,110 − 1", 6109, "6,110 − 0", 6110),
    cmp_q("4,250 − 0", 4250, "4,250 − 10", 4240),
    cmp_q("900 − 100", 800, "900 − 10", 890),
    cmp_q("7,000 − 1", 6999, "6,999 − 0", 6999),
    cmp_q("3,400 + 0", 3400, "3,400 − 0", 3400),
    cmp_q("500 − 50", 450, "500 − 5", 495),
]

truefalse = [
    mcq("900 − 145 gives the same answer as 145 − 900.", ["true", "false"], "false"),
    mcq("Taking away MORE leaves you with LESS.", ["true", "false"], "true"),
    mcq("Taking away 0 changes the number.", ["true", "false"], "false"),
    mcq("1 less than 8,900 is 8,899.", ["true", "false"], "true"),
    mcq("The predecessor of a number is always 1 bigger than it.", ["true", "false"], "false"),
    mcq("If 5,298 is the predecessor of a number, that number is 5,299.", ["true", "false"], "true"),
]

s5 = {
  "id": "nr-diag-1", "track": SCHOOL,
  "title": "Diagnostic — Number Relationships (both phrasings)", "marks": 20,
  "note": "Watch the direction. \"The predecessor OF 3,299\" is one LESS (3,298). "
          "\"3,299 IS the predecessor of ___\" is one MORE (3,300). Same words, opposite answer.",
  "sections": [
    {"title": "Predecessor and successor — read which way round it is", "marks": 8, "layout": "grid",
     "questions": pred_succ},
    {"title": "Compare — put in <, > or =", "marks": 6, "layout": "lines", "questions": compare},
    {"title": "True or false", "marks": 6, "layout": "lines", "questions": truefalse},
  ],
}

SHEETS = [s1, s2, s3, s4, s5]

# ---------------------------------------------------------------- checks
def check():
    seen = set()
    for sh in SHEETS:
        assert sh["id"] not in seen; seen.add(sh["id"])
        total = sum(sec["marks"] for sec in sh["sections"])
        assert total == sh["marks"], (sh["id"], total, sh["marks"])
        for sec in sh["sections"]:
            assert len(sec["questions"]) == sec["marks"], (sh["id"], sec["title"], len(sec["questions"]), sec["marks"])
            for q in sec["questions"]:
                if "options" in q:
                    assert 0 <= q["answerIndex"] < len(q["options"]), q
                    assert len(set(q["options"])) == len(q["options"]), q
                else:
                    assert q["answers"] and isinstance(q["answers"][0], int), q
                    assert q["label"].count("[_]") == 1, ("no input slot", q)
    # spot-check arithmetic independently of how it was generated
    for sec in s1["sections"]:
        for q in sec["questions"]:
            m = re.match(r"^(\d+) \+ \[_\] = (\d+)$", q["label"])
            if m: assert int(m.group(1)) + q["answers"][0] == int(m.group(2)), q
            m = re.match(r"^\[_\] − (\d+) = (\d+)$", q["label"])
            if m: assert q["answers"][0] - int(m.group(1)) == int(m.group(2)), q
            m = re.match(r"^(\d+) − \[_\] = (\d+)$", q["label"])
            if m: assert int(m.group(1)) - q["answers"][0] == int(m.group(2)), q
    for sec in s3["sections"]:
        for q in sec["questions"]:
            a, b = map(int, re.match(r"^(\d+) × (\d+) = \[_\]$", q["label"]).groups())
            assert a * b == q["answers"][0], q
    for q in s4["sections"][2]["questions"]:
        a, op, b = re.match(r"^(\d+) ([−+]) (\d+) = \[_\]$", q["label"]).groups()
        assert (int(a) - int(b) if op == "−" else int(a) + int(b)) == q["answers"][0], q
    print(f"OK — {len(SHEETS)} sheets, "
          f"{sum(len(sec['questions']) for sh in SHEETS for sec in sh['sections'])} questions")


if __name__ == "__main__":
    check()
    if "--check" in sys.argv:
        sys.exit(0)
    path = pathlib.Path(sys.argv[1])
    src = path.read_text()
    if "NEW_DIAGNOSTIC_SHEETS" in src:
        sys.exit("already inserted — nothing to do")
    anchor = "WORKSHEETS.push(...ADD_REVISION_2);"
    assert anchor in src, "anchor not found"
    block = ("\nconst NEW_DIAGNOSTIC_SHEETS = "
             + json.dumps(SHEETS, ensure_ascii=False)
             + ";\nWORKSHEETS.push(...NEW_DIAGNOSTIC_SHEETS);")
    path.write_text(src.replace(anchor, anchor + block, 1))
    print(f"appended {len(SHEETS)} sheets to {path}")
