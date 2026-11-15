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

Findings, each with its severity and `path:line`, and recommendations.

On a re-score, which items were scored afresh and which were inherited.

When the work stops, leave what was done and why it stopped.

## Default

- Score these items: decision grounds, verification fit, scope, security.
- Decision grounds: score whether each decision is grounded in the mechanisms it actually changes, with its constraints and rejected alternatives, and is implementable on the current structure.
- Verification fit: score whether each verification checks the property of its item by a method that can fail when the property does not hold.
- Scope: score whether the scope is neither too broad nor missing a requirement, adds no new mechanism where an extension suffices, and gives a separation reason for a directly related problem it leaves out.
- Score the decision layer. Do not score which files change or which tests run; those are the build's.
- Score each item on a scale of 10: 9–10 excellent, 7–8 good, 5–6 insufficient, 3–4 poor, 1–2 failing.
- Read only; change nothing.
