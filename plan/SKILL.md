---
name: plan
description: >-
  Choose after design when an independent score of the design's intent is
  needed: whether each decision is grounded, whether each criterion's
  verification fits it, and whether the scope is right. Runs in a session
  other than the design's. Does not change anything.
metadata:
  goal: Each item has a score and its ground.
---

## Input

Required:

- The feature design.
- The verification design.
- The applied criteria.

Helpful:

- The criterion decisions.
- The previous evaluation (on a re-score).

## Exit

- End when every item is scored.

## Output

For each item:

- the score;
- its ground.

Findings, each with its severity, `path:line`, weight and the grounds of the weight, and recommendations.

On a re-score, which items were scored afresh and which were inherited.

When the work stops, leave what was done and why it stopped.

## Default

- Score these items: decision grounds, verification fit, scope, security.
- Decision grounds: score whether each decision is grounded in the mechanisms it actually changes, with its constraints and rejected alternatives, and is implementable on the current structure.
- Verification fit: score whether each verification checks the property of its item by a method that can fail when the property does not hold.
- Scope: score whether the scope is neither too broad nor missing a requirement, adds no new mechanism where an extension suffices, and gives a separation reason for a directly related problem it leaves out.
- Score the decision layer. Do not score which files change or which tests run; those are the build's.
- Score each item on a scale of 10: 9–10 excellent, 7–8 good, 5–6 insufficient, 3–4 poor, 1–2 failing.
- Give each finding one weight by two questions. First: can its problem occur where the target actually runs? A problem that needs no condition of that environment can; one that needs such a condition can unless a stated environment rules it out. Second: does the level the target requires for the property the finding concerns oblige addressing it? Without a level stated for that property, a problem that needs no such condition takes as its level the criterion it was measured by, which obliges addressing it. The weight is one of:
  - `cannot occur`: a stated environment rules the problem out;
  - `need not be addressed`: it can occur, and the level does not oblige addressing it;
  - `must be addressed`: it can occur, and the level obliges addressing it;
  - `not established`: it needs a condition of the environment, can occur, and no level for that property is stated; treated as must be addressed.
- Stated means stated by, first to last: the instructions of the call, the criterion decisions, the applied criteria, and the target's own documents and files before the proposed change. Anything else read counts only where it cites one of these. Where two differ, the earlier stands, and the grounds name both.
- Record the weight's grounds: the instructions' passage, a document's section and quoted sentence, a file and line at a commit, or the criterion; for `not established`, or where no environment was stated, what was looked for and where.
- The weight changes neither severity nor any score.
- Read only; change nothing.
