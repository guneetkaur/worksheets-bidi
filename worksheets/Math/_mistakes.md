# Math — Mistake Journal

## 2026-08-25  —  Full re-analysis from the git repo CSV (4,063 rows, 7 Jul – 24 Aug)

Pulled `results/results.csv` from `guneetkaur/worksheets-bidi` (last commit 24 Aug 17:48 IST; the local clone at `/Volumes/samsung_backup/workspace/new/worksheets-bidi` is byte-identical). The copy inside the Ambar Worksheet folder is stale — 490 rows, ends 24 Jul. **Do not use the folder copy.** Five new sessions since the 10 Aug entry: 11, 12, 21, 23, 24 Aug.

Method: repeated "Finish & Check" presses inside one sitting collapse to one attempt; best attempt per sheet per day. Overall 1,065/1,205 = 88.4% across 62 sheets on 17 days.

Full report (dashboard): https://claude.ai/code/artifact/f34d9f78-21da-4b30-890c-4416e3749846

### THE BIG ONE — subtraction with borrow: one wrong rule, applied 12 times out of 12

23 Aug, Worksheet 4 (L1) 2-digit − 2-digit WITH borrow: **0/12**. Every answer is explained by the same bug — she takes the SMALLER digit from the LARGER one in each column and ignores the borrow entirely ("smaller-from-larger").

| Sum | Wrote | Correct | What she did |
|---|---|---|---|
| 34 − 17 | 23 | 17 | 3−1=2 · 7−4=3 |
| 43 − 18 | 35 | 25 | 4−1=3 · 8−3=5 |
| 50 − 29 | 39 | 21 | 5−2=3 · 9−0=9 |
| 42 − 18 | 36 | 24 | 4−1=3 · 8−2=6 |
| 54 − 18 | 44 | 36 | 5−1=4 · 8−4=4 |
| 52 − 15 | 43 | 37 | 5−1=4 · 5−2=3 |
| 41 − 17 | 36 | 24 | 4−1=3 · 7−1=6 |
| 41 − 14 | 33 | 27 | 4−1=3 · 4−1=3 |
| 30 − 22 | 12 | 8  | 3−2=1 · 2−0=2 |
| 54 − 17 | 43 | 37 | 5−1=4 · 7−4=3 |
| 51 − 24 | 33 | 27 | 5−2=3 · 4−1=3 |
| 31 − 19 | 28 | 12 | 3−1=2 · 9−1=8 |

Zero random slips — a single teachable misconception, not twelve errors.

**24 Aug re-attempt of the same sheet: 10/12.** Fixed in a day. The two survivors are the hardest family: `30 − 22` → wrote 20, `51 − 24` → wrote 40. Both are now partial-method (she borrows, then loses the units), specifically **borrow across a zero / large units gap**. Drill exactly that before opening the next subtraction stage.

### Two more systematic rules, previously unlogged

**1. Adds the tens, subtracts the units** (23 Aug, WS3 no-borrow, 10/14)
- `86 − 11` → 95 (8+1=9 in the tens, 6−1=5 in the units)
- `89 − 12` → 97 (8+1=9, 9−2=7)
Same family as the July `2 × 6 = 8` bug: she reads the numbers before she reads the sign.

**2. Missing addends go BLANK — third independent sighting** (23 Aug, L3 WS1 addition to 4 digits)
All four skipped, while she attempted the sections either side:
`708 + __ = 940`, `484 + __ = 774`, `436 + __ = 740`, `284 + __ = 614`.
Previously seen as missing-minuend errors on the marked school sheet (21 Jul) and missing-factor misses in July's tables work. Small ones (`4 + __ = 10`) she gets right; three-digit ones she won't start. **Most under-treated gap in the file.**

### Addition — 4-digit column work is where the carry now drops
23 Aug, L3 Worksheet 1: 13/22. Two word-problem answers **exactly 90 short**:
- 1368 + 2547 → 3825 (correct 3915)
- 2364 + 3548 → 5822 (correct 5912)
- 4759 + 4402 → 8961 (correct 9161, −200)
- 3854 + 2259 → 51113 (digit smear)
Her mental-maths carry is perfect through Stage 9. The **column + word-problem format** is what breaks it — practise in that format specifically.

Stage 7 (WS12, 3d+2d) still sits at 7/14 from 9 Aug, all blanks. Untouched since. Re-give it first thing in a session.

### Multiplication — the July problem is closed
| Date | Sheet | Score |
|---|---|---|
| 5 Aug | Revision Drill 1 (tables 3 & 4 weak facts) | 30/30 |
| 11 Aug | WS2 — tables 3 and 4 | 21/26 |
| 21 Aug | WS3 — tables 6 and 7 | 23/26 |
| 23 Aug | WS4 — tables 8 and 9 | 25/26 |

69/78 (89%) since 11 Aug. Every miss is one of four facts:
- `7 × 8` → **55**, three times in one sheet (memorised-wrong, off by one). Teach "5, 6, 7, 8" → 56 = 7×8.
- `4 × 7` → **42** and `4 × 8` → **48**, twice each on 11 Aug — both are the ×6 answers; she was reading the wrong row.
- `8 × 3` → **224** (typo).

**The 42+/44 gate on Diagnostic Sheet 1 has still not been re-run since 22 Jul (38/44)** — while she has since cleared tables 6, 7, 8 and 9 at 88–96%. Either re-run once to close the record or retire the gate as overtaken.

### Reasoning / English / GK
- Drill 5 Coding–Decoding: **3/20 with 15 blank** on 11 Aug (first thing in 8 weeks she walked away from), then **18/20** on 12 Aug. Unfamiliar question *types* stop her on first contact; one night's gap fixes it. Not a reason to slow the drill schedule.
- English 216/234 (92%). New soft spots on 21–24 Aug: comparatives/superlatives (`difficulter`, `more good`, `pretty` for "the ___ dress" — irregulars not in yet); a/an by **sound** not spelling ("___ one-eyed pirate" → *a*; "a umbrella" not flagged); `between` vs `beside`; `in` vs `on` for containers. Articles & Prepositions L3 dropped to 8/15 with the last three blank — the only English sheet she has abandoned.
- GK 63/63 (100%) across all four Me & My Surroundings sheets incl. the mini olympiad paper.
- Geometry & Data Handling L1 (first ever): 11/15. All four misses definitional — rectangle = 3 sides, cube = 4 faces, pentagon = 6 sides, five-bar tally = 4. **Untaught, not weak.** One deep-dive sitting clears it.

### CORRECTION to the 10 Aug "fatigue, not knowledge" conclusion
That held for the data then; it does not hold for August.
- Across all 17 practice days there is **no relationship** between sheets-per-day and accuracy (r ≈ −0.0), nor between volume and blanks (r = 0.04).
- On 23 Aug — her lowest day (71%) — the 0/12 borrow sheet was submitted **14 minutes into the session**; the 25/26 tables sheet came 2.5 hours later. She was not tired; the sheet was new.

The correct split: **blanks = fatigue or unfamiliarity; wrong answers = knowledge.** Opposite responses — a blank sheet gets re-given early in a session, a wrong sheet gets taught.

### Next actions (ranked)
1. Borrow across zero — 2–3 short sheets, then re-run WS4 for a clean 12/12.
2. Missing-addend sheet, taught as "take it back off" — sit with her on it.
3. Re-give WS12 (3d+2d) at the start of a session.
4. Drill four facts, not four tables: 7×8, 4×7, 4×8, check 8×3. Then close or retire the Diagnostic 1 gate.
5. 4-digit addition in **column form with word-problem wrappers**.
6. English: comparatives as three rules (-er/-est, more/most, irregulars) + a/an by sound.
7. Geometry deep-dive (shape names, sides, faces, tally marks) before the next IMO sheet.



## 2026-08-10 (later)  —  CORRECTION + full re-analysis: earlier fetch was truncated, she HAS been practicing

The "nothing since 22 July" note below was wrong — it came from a web-fetch that silently truncated at line 391 of the CSV. The real repo file has 3,694 rows through 10 Aug. Re-pulled the whole file via shell `curl` and parsed it properly this time (grouped by worksheet+date+submitted_at so repeated "Finish & Check" presses within one sitting collapse into one session, keeping the best score — same logic as the app's dedup fix). Five more sessions exist: **26 Jul, 5 Aug, 6 Aug, 9 Aug, 10 Aug.**

### Addition — racing ahead, Stage 9 keystone already cleared
| Date | Sheet | Best score | Note |
|---|---|---|---|
| 26 Jul | Stage 3 (WS8, 2d+1d) | 24/24 | |
| 26 Jul | Stage 4 (WS9, 2d+2d no carry) | 18/18 | |
| 26 Jul | Stage 5 keystone L1 (WS10) | 16/16 | |
| 5 Aug | Stage 5 L2 Mixed (WS10) | 16/16 | |
| 6 Aug | **Stage 5 MASTERY TEST** | **18/20 (90%)** | **Gate passed.** The 2 misses were `89+52` answered 141 and `79+35` answered 114 — those are each other's correct answers, swapped. Not a calculation error, a row-alignment slip (wrote the right number on the wrong line). |
| 6 Aug | Stage 5 L3 Stretch (WS10) | 10/12 | 2 word problems left blank, not wrong — session was 68 min, this came near the end |
| 9 Aug | Stage 7 (WS12, 3d+2d) | 7/14 (stalled) | **Every miss is a blank, not a wrong answer** — she worked steadily up from 1→7 correct over 24 min then stopped mid-sheet (whole "Speed strip" section untouched). A same-day retry 45 min later opened fresh and only got to 1/14 before abandoning — she was done for the day, not confused. **Needs a clean re-attempt, ideally first thing in a session.** |
| 9 Aug | Stage 8 (WS13, 3d+3d no carry) | 12/14 | same shape — 2 blanks in the closing speed strip |
| 9 Aug | **Stage 9 keystone (WS14 L1, 3d+3d WITH carry)** | **14/14 — perfect on the first sitting** | biggest keystone of the addition track, no hesitation |
| 10 Aug | Stage 9 keystone re-run (WS14 L1) | 12/12 | confirms 9 Aug wasn't a fluke |
| 10 Aug | Stage 9 L2 Mixed (WS14) | 12/12 | perfect |

Stage 6 (round-and-adjust, WS11) was skipped over — she jumped straight from Stage 5 to Stage 7. Worth circling back since the +9/+19/+29 trick is used later, but it's not blocking anything.

**Pattern:** every genuine error since 26 Jul has been an unfinished section near the end of a long session (68–109 min), not a wrong calculation. The one 17-minute session (10 Aug) was clean start to finish, both sheets perfect. **Shorter, earlier sessions are outperforming long ones — fatigue, not knowledge, is now the limiting factor on Addition.**

### Subtraction — off to a clean start
- 26 Jul Diagnostic Baseline: 25/25
- 6 Aug WS1 (facts within 20): 14/14
- 6 Aug WS2 (subtract 9/8/11, ten-trick): 12/12
No subtraction errors logged yet at all.

### Multiplication — the tables 3/4 bug looks fixed, needs confirmation
- 5 Aug Revision Drill 1 (targeted at the tables 3/4 false-rule and add-instead-of-multiply errors from the 22 Jul entry below): **30/30, zero errors.**
- Diagnostic Sheet 1 (the 42+/44 gate test) has NOT been re-run since 22 Jul (38/44). Given the drill is perfect, this is very likely to pass now — re-run it to confirm and formally clear Stage 2.

### English (running in parallel, for context)
Verbs & Tenses L1/L2/L3 and Reading Comprehension L1/L2, plus a Mini Olympiad paper — all 26 Jul–6 Aug, all 15–18 out of 15–18, i.e. at or near perfect throughout. No action needed there.

### Next actions
1. Re-run Multiplication Diagnostic 1 to formally confirm the 42+/44 gate.
2. Give Stage 7 (WS12, 3d+2d) a clean re-attempt early in a session — she has the skill, just hasn't finished a sitting.
3. Advance Addition to Stage 10 (multi-addend / real-world) — Stage 9 keystone is solidly done.
4. Optional: loop back to Stage 6 (round-and-adjust) since it was skipped.

## 2026-08-10  —  CONFIRMED: repo CSV verified complete, no maths logged since 22 July

*(Superseded by the entry above — this was based on a truncated fetch. Left here for the error-pattern detail below, which is still accurate for the 7–22 Jul data.)*

Repo file = the consolidated file uploaded earlier (491 lines, 20 attempts, 7–24 Jul). Verified: the ONLY record after 22 Jul is Drill 4 — Ranking & Ordering (24 Jul, reasoning, 20/20). **No maths worksheet has been logged for 19 days.** Either she has been on school/paper work only, or app results are not syncing. Check this first — the whole feedback loop depends on it.

Complete multiplication error list (every non-blank wrong answer in the file):

| Date | Question | Gave | Correct | Pattern |
|---|---|---|---|---|
| 7 Jul | 3 × 9 | 29 | 27 | false rule (a−1)(b) |
| 7 Jul | 3 × 8 | 28 | 24 | false rule — twice |
| 7 Jul | 4 × 9 | 39 | 36 | false rule |
| 7 Jul | 9 × 4 | 39 | 36 | false rule (commuted) |
| 7 Jul | 7 × 2 | 16 | 14 | near-miss |
| 7 Jul | 4 × 4 | 61 | 16 | DIGIT REVERSAL |
| 7 Jul | 9 × 5 | 54 | 45 | DIGIT REVERSAL |
| 8 Jul | 2 × 8 | 18 | 16 | near-miss |
| 8 Jul | 10 × 6 | 30 | 60 | used ×5 |
| 8 Jul | 2 × __ = 18 | 8 | 9 | missing factor, table 2 |
| 8 Jul | __ × 2 = 16 | 7 | 8 | missing factor, table 2 |
| 20 Jul | 2 × 6 | 8 | 12 | **ADDED (2+6)** |
| 22 Jul | 2 × 6 | 8 | 12 | **ADDED — same error, 2 days apart** |
| 22 Jul | 4 × 6 | 10 | 24 | **ADDED (4+6)** |
| 22 Jul | 4 × 7 | 25 | 28 | near-miss |
| 22 Jul | 6 × 3 | 16 | 18 | near-miss |
| 22 Jul | 4 × 4 | 18 | 16 | near-miss |
| 22 Jul | 8 × 4 | 36 | 32 | gave 4×9 |

**Adding instead of multiplying is now confirmed 3× across 2 dates** (2×6 twice, 4×6 once) — the single most important bug.

Note the failure mode CHANGED between sittings: 7 Jul errors were systematic (false rule, reversals); 22 Jul errors were operation-confusion and near-misses. Different bugs on different days points to attention/fatigue, not fixed ignorance.

**Progress check:** Diagnostic 1 went 36/44 (7 Jul) → 38/44 (22 Jul). Gate is 42+/44. Two weeks, +2 marks — multiplication has essentially stalled. Addition, by contrast, is done.

## 2026-08-10  —  Deep analysis of repo results.csv (worksheets-bidi), Jul 7–22 data

Read raw per-question rows (not just scores). Two ERROR PATTERNS emerge that scores alone hide:

### PATTERN A — Digit reversal (she KNOWS the fact, writes it backwards)
- `4 × 4` → wrote **61**  (correct 16)
- `9 × 5` → wrote **54**  (correct 45)
Both are the correct answer with digits swapped. This is NOT a knowledge gap — it's a recording/transcription error. Likely rushing. Fix = "say it, then write it" + check the tens digit.

### PATTERN B — A systematic wrong rule on tables 3/4/9
- `3 × 9` → **29** (correct 27)
- `3 × 8` → **28** (correct 24)
- `4 × 9` → **39** (correct 36)
In each case she answers (first factor − 1) followed by the second factor. She is pattern-matching a false rule rather than skip-counting. This is the single most fixable multiplication error — it explains most of the tables 3/4 misses logged on 22 Jul.

### PATTERN C — Multiplying vs adding confusion (PERSISTENT)
- `2 × 6` → **8** on 20 Jul AND again on 22 Jul. 2 + 6 = 8 — she is ADDING.
- Related: `2 × 8` → 18, `10 × 6` → 30 (that's 5 × 6), `7 × 2` → 16.
Same fact wrong on two separate dates = not a slip. When the first factor is small (2), she sometimes switches operation. Worth checking she reads the × sign, not just the numbers.

### Confirmed strengths (from raw rows)
- Diagnostic 3 (15 carry sums + 10 three-digit): **25/25, zero errors** — the carry gap is genuinely closed.
- WS5 Mastery 20/20, WS6 Consolidation 20/20, WS7 Tens Anchoring 24/24 on BOTH 17 and 20 Jul (repeated, not a fluke).
- Missing-addend work (`4 + __ = 10`, `12 + __ = 20`) — all correct.
- Missing-FACTOR work (`2 × __ = 14`, `__ × 10 = 80`) — 6/8, errors only on 2 × __ = 18 and __ × 2 = 16, both table-2 (see Pattern C).

### Data-quality note
`total_time_s` is unreliable in these records (values include −784.5 and 595636.5). Do not draw speed conclusions from this CSV — use the live admin timer instead.

### Actions
1. Drill Pattern B directly: show her 3×8 by skip-counting aloud (3,6,9…24) and contrast with her "28". Name the false rule so she can catch it.
2. Pattern A: two-second check — read the answer back aloud before moving on.
3. Pattern C: mixed +/× sheet where she must first say WHICH operation, before answering.
4. Re-run Diagnostic 1; gate stays 42+/44.

## 2026-08-10  —  SCHOOL Maths Practice Sheet (dated 21/7/26, photos received 3 Aug)

Marked school sheet, DPS East of Kailash, Class III-B. Analysed from photos.

### What she got RIGHT (strong areas)
- **Q2 Fill in the blanks — 10/10.** Every one correct, including the harder ones: 1000 more than 8,779 = 9,779; missing addend (850 + ★ = 1500 → 650); "10 tens more than 2,350" → 2,450; comparing quantities (1,500 vs 1,000 → 500 more); order property (4,576 + 234 + 67 = 234 + 67 + 4,576). This is real conceptual strength.
- **Q6 column addition with carries** — 6,718 + 568 + 24 = 7,310 correct, carries written properly. Matches the mental-math track evidence that carrying is now solid.
- Terminology mostly right: sum/total, difference, subtrahends (T/F i correct).

### ERRORS — three distinct root causes

**1. Predecessor / successor direction (CONCEPTUAL — most important)**
- Q1(i) "3,299 is the predecessor of ___" → she chose 3,298. Correct: 3,300.
  She answered "what is the predecessor OF 3,299" instead of "3,299 is the predecessor of WHAT". The direction of the relationship is reversed in her head.
- Note: Q3(b) she got right (5,298 is the predecessor of 5,299) — so she can do it when the sentence is phrased the usual way. It's specifically the INVERTED phrasing that breaks.

**2. Missing minuend / "___ − 400 = 400" (CONCEPTUAL)**
- Q1(iv) she answered 80; correct is 800. She subtracted rather than added to find the missing start number. Same family as Q3(a): "35 less than 500" → she wrote 466 (correct 465) — arithmetic slip, but in the same missing-number/less-than territory.

**3. Comparing when subtracting 0 vs 1 (CONCEPTUAL)**
- Q5(ii) 6,110 − 1 ___ 6,110 − 0 → she wrote >. Correct: <. Taking away MORE leaves LESS — the "subtract 0 leaves it unchanged" idea isn't connected to ordering yet.
- Q4(ii) 900 − 145 = 145 − 900: she first wrote T, corrected to F. Order matters in subtraction — shaky, self-corrected.
- Q4(v) 1 less than 8,900 = 8,899: written answer messy/corrected; teacher marked it.

### PROCESS issue (costing marks independent of maths)
- Teacher's note on Q3: **"Write complete statement."** She wrote only the corrected number, not the full sentence. Marks lost on presentation, not on maths.

### NOT ATTEMPTED
- Q7 (column subtraction 1,697 from 7,830) — blank, teacher marked "?"
- Q8, Q9 (Word Stories) — blank, teacher wrote **"Absent"**. So the whole word-problem + column-subtraction section is untested. Nothing can be concluded about her word-problem ability from this sheet — she must complete these.

### Implication → next actions
1. Targeted drill on **predecessor/successor in BOTH phrasings** ("X is the predecessor of ___" as well as "the predecessor of X is ___").
2. Drill **missing minuend/subtrahend** ( ___ − 400 = 400,  ___ − 250 = 100 ) — teach as "add them back".
3. Explicitly teach **subtracting 0 vs subtracting more → ordering**, and that subtraction is NOT reversible.
4. Practise **writing the complete statement** in correct-the-sentence questions — pure marks recovery.
5. She still owes the **column subtraction + 2 word stories** from this sheet. Monthly Test 1 (already built) covers exactly these.

## 2026-07-24  —  Consolidated from webapp results (Jul 7–24, 20 attempts)

### Multiplication — tables 3 and 4 are THE weak spot (recurring across 3 attempts)
- Missed repeatedly: 3×8 (twice, gave 28), 3×9 (gave 29), 4×6 (gave 10), 4×7 (gave 25), 4×9/9×4 (gave 39, twice), 8×4 (gave 36), 6×3 (gave 16), 4×4 (gave 18)
- Pattern in errors: answers like 28 for 3×8, 39 for 4×9 suggest near-miss recall (off by one step in skip-count), not guessing
- 2×6 answered "8" twice (Jul 20, 22) — adding instead of multiplying when rushing
- Tables 2, 5, 10: solid (WS1 32/37; misses were speed slips, and word problem 2×8=18 → careless)
- Diagnostic 1 trajectory: 36/44 (Jul 7) → 15/44 (Jul 20, mostly blank — abandoned attempt, ignore) → 38/44 (Jul 22). Wrongs on Jul 22 ALL in tables 3/4/related.

### Addition — carry gap is FIXED
- Diagnostic 3 re-test (Jul 15): 25/25 including all carry sums — the Jun 23 carry weakness is resolved
- Diagnostic 2: 19/20 (one slip: 63+24=85)
- Stage 1 gates all passed: WS2 bonds-20 20/20, WS3 doubles 20/20, WS4 near-doubles 19/20 (7+8=13 slip), WS5 mastery 20/20, WS6 consolidation 20/20, WS7 tens anchoring 24/24 twice
- Note: total_time values in these CSVs are unreliable (reload quirks, one negative) — don't judge speed from them; watch it live instead

### Implication
- Multiplication: do NOT advance to tables 6–9 yet. One targeted weak-fact drill on tables 3/4 (added to app as Revision Drill 1), re-run Diagnostic 1 after — gate = 42+/44
- Addition: Stages 1–2 complete and gated. Open Stage 3 (2-digit + 1-digit) → fast-track toward Stage 5 keystone since Diag 3 was perfect

## 2026-06-23  —  Mental Math LTR Addition  (Diagnostic Sheets 1–3)
- Solid on Sheet 1 (single-digit) and Sheet 2 (two-digit, no carry)
- Slips on Sheet 3 (carry / three-digit baseline) — carrying is the gap
- Speed is a challenge across the board — accuracy is OK but he is slow / not yet fluent
- Implication: start Stage 2 (Tens anchoring & bridging) to build carry-readiness; add timed fluency drills, not just accuracy practice
