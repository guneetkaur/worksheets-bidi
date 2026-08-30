# Mistake Journal — Weak Topics Tracker

Per-subject log at `worksheets/<Subject>/_mistakes.md` that captures topics Ambar got wrong or shaky on. Used by the skill to target weak areas in the next worksheet.

## Schema

```markdown
# <Subject> — Mistake Journal

## 2026-04-24  —  Plants Around Us  (Worksheet 3)

- Confused **climber vs creeper** (Q2, Q15)  — needs more practice distinguishing weak-stem plants
- Forgot: **chlorophyll** is the green pigment (Q9)
- Said Rafflesia is a tree, not a flower (Q21) — fact not yet internalized

## 2026-04-20  —  Plants Around Us  (Worksheet 1)

- Couldn't recall **photosynthesis** spelling (Q14)
- ...
```

## Maintenance rules

- **Additive**: new entries are appended to the top (most recent first).
- **Per-worksheet**: each review session gets its own dated block.
- **Be specific**: capture the concept, not just "got 5 wrong". Concepts are what the next worksheet will target.

## When the user says …

> *"He got these wrong: climber vs creeper, chlorophyll."*
> *"Log this: he's confusing tree vs shrub."*
> *"Add to his weak list: Rafflesia."*

Append to `_mistakes.md` under today's date with the chapter and the current worksheet number.

## When generating a new worksheet

If the user prompt includes any of:
- *"target his weak areas"*
- *"focus on recent mistakes"*
- *"revision of what he got wrong"*
- *"help him with [topic]"* where the topic appears in `_mistakes.md`

…then:

1. Read `_mistakes.md` for the subject.
2. Collect weak concepts from the last 3 entries.
3. Bias at least **50% of the new worksheet** toward those concepts (more repetition, different phrasings, direct drilling).
4. Tag the file: `Worksheet N (Targeted) - <what>.docx`.
5. Mention in the chat summary which weak topics were targeted.

## Optional: mark improvement

When a concept has been practiced successfully (user confirms "he got it this time"), you can annotate the entry:

```markdown
- ~~Confused climber vs creeper~~  ✅ resolved 2026-04-28
```

Keep the strikethrough so we know it was a weak spot historically.
