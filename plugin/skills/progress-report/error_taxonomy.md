# Error taxonomy

Every wrong answer is put in exactly one class. The classes exist because they call
for *different responses* — that is the only reason to distinguish them.

`analyse.py` assigns the class automatically where the item is plain arithmetic
(`a op b = __`). Review its output before writing the report: the script is good at
the arithmetic classes and blind to everything in a multiple-choice question, which
it parks in `wrong-choice` for a human read.

| Class | What it means | What it calls for |
|---|---|---|
| `blank` | Not attempted | Re-give the sheet early in a session. **Never teach from a blank** — you don't know what she'd have written. |
| `wrong-rule` | A systematic misconception, applied more than once | Teach the rule. One intervention fixes every instance at once. The highest-value class in the file. |
| `wrong-fact` | One memorised answer is wrong, method is fine | Drill that fact. Not the table, the fact. |
| `operation-confusion` | The answer is correct for a *different* operation | She's reading the numbers before the sign. Mixed-operation sheets where she names the operation before answering. |
| `transcription` | She knew it and wrote it wrong — digit reversal, smear, right answer on the wrong line | Say it, then write it. Not a maths problem. |
| `near-miss` | Off by a step, no pattern across instances | Fluency, not understanding. More reps, timed. |
| `wrong-choice` | Multiple-choice miss with no arithmetic to inspect | Read the distractor she picked — it usually names the misconception. Classify by hand into one of the classes above where the pattern is clear. |
| `untaught` | Content she has never been given | Not an error. Flag as coverage, not weakness, and say so plainly in the report. |

## Rules the script applies

- **Operation confusion** — the given answer equals `a+b`, `a−b` or `a×b` for an
  operation other than the one asked.
- **Smaller-from-larger** — for `a − b` of equal digit length, the given answer
  matches the column-by-column absolute differences. This is the classic borrow bug.
- **Adds the tens, subtracts the units** — for two-digit `a − b`, the tens digit of
  the answer is `a₁+b₁` while the units digit is `a₂−b₂`.
- **Transcription** — the given answer is the correct answer reversed, or contains
  the correct answer with an extra digit smeared in.
- **Near miss** — within 2, or within 5% of the correct answer, with no other
  pattern matched.

## The rule that overrides all of them

**Two instances make a pattern; one is a slip.** A class only becomes a *gap* in
the report when it repeats — either the same wrong rule across several questions in
one sheet, or the same wrong answer across two sittings. A single odd answer gets
counted in the taxonomy table and nowhere else.

## Promoting a class to a gap

A gap card is warranted when any of these hold:

1. A `wrong-rule` class fires on **three or more** questions in one sheet.
2. The same `wrong-fact` appears on **two or more separate dates**.
3. A whole section is `blank` on **two consecutive** attempts at that sheet.
4. A track's accuracy drops below 70% on a sheet the previous stage predicted she
   was ready for.

Anything else stays in the tables.
