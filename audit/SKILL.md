---
name: audit
description: >-
  Choose after build when an independent judgment is needed that each test of a
  required behavior failed on the code without the implementation and passes
  with it, together with a security score of the change. Runs in a session
  other than the one that made the change. Reads the change's commits, the
  build report, the test records and git. Does not change anything.
metadata:
  goal: Each test of a required behavior has a test-first judgment, and each security item has a score and its ground.
---

## Input

Required:

- The change (its commit range).
- The build report.
- The failing runs of the tests.

Helpful:

- The verification design.
- The previous evaluation (on a re-score).

## Exit

- End when test-first is judged and every item is scored.
- When test-first is not confirmed, score nothing and state what is missing.

## Output

For each test:

- the evidence read;
- the judgment.

For each item:

- the score;
- its ground.

Findings, each with its severity and `path:line`, and recommendations.

On a re-score, which items were scored afresh and which were inherited.

When the work stops, leave what was done and why it stopped.

## Default

- Score these items: authentication and authorization, input validation, data exposure, infrastructure isolation, dependencies.
- Score each item on a scale of 10: 9–10 excellent, 7–8 good, 5–6 insufficient, 3–4 poor, 1–2 failing.
- Only read; change nothing.
