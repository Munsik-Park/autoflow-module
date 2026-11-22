---
name: quality
description: >-
  Choose after build when an independent score is needed of whether the change
  is complete, correct, verified and within its scope, against the acceptance
  criteria and the design. Runs in a session other than the one that made the
  change. Does not change anything.
metadata:
  goal: Each quality item has a score and its ground.
---

## Input

Required:

- The change (its commit range).
- The acceptance criteria applied.
- The build report.

Helpful:

- The feature design.
- The verification design.
- The analysis report (its scope judgments).
- The audit evaluation.
- The findings deferred or separated.
- The previous evaluation (on a re-score).

## Exit

- End when every item is scored.

## Output

For each item:

- the score;
- its ground.

Findings with their severity, `path:line`, weight and the grounds of the weight, and recommendations. A carried finding names its source, and a weight given here names the weight it carried.

On a re-score, which items were scored afresh and which were inherited.

When the work stops, leave what was done and why it stopped.

## Default

- Score these items: completeness, quality, test coverage, test quality, security (from the audit), fit, impact scope, minimal implementation, commit conventions, documentation updates.
- Judge minimal implementation against the smallest sufficient change that resolves the confirmed problem within the scope. Fail the item when a hunk traces to none of it.
- Score on a scale of 10: 9–10 excellent, 7–8 good, 5–6 insufficient, 3–4 poor, 1–2 failing.
- Give each finding one weight by two questions. First: can its problem occur where the target actually runs? A problem that needs no condition of that environment can; one that needs such a condition can unless a stated environment rules it out. Second: does the level the target requires for the property the finding concerns oblige addressing it? Without a level stated for that property, a problem that needs no such condition takes as its level the criterion it was measured by, which obliges addressing it. The weight is one of:
  - `cannot occur`: a stated environment rules the problem out;
  - `need not be addressed`: it can occur, and the level does not oblige addressing it;
  - `must be addressed`: it can occur, and the level obliges addressing it;
  - `not established`: it needs a condition of the environment, can occur, and no level for that property is stated; treated as must be addressed.
- Stated means stated by, first to last: the instructions of the call, the applied criteria, and the target's own documents and files before the change's commits. Anything else read counts only where it cites one of these. Where two differ, the earlier stands, and the grounds name both.
- Record the weight's grounds: the instructions' passage, a document's section and quoted sentence, a file and line at a commit, or the criterion; for `not established`, or where no environment was stated, what was looked for and where.
- A weight carried from the audit evaluation or the findings deferred or separated stands when it carries its grounds, is not `not established`, and no source earlier in that order than its grounds states otherwise; otherwise the finding is given a weight here.
- The weight changes neither severity nor any score.
- Read only; change nothing.
