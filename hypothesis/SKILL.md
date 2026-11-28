---
name: hypothesis
description: >-
  Choose after analysis when an independent score is needed of whether the
  analysis report's conclusion is supported by its grounds, whether the report
  kept to the problem it was given and whether the analysis reached its goal.
  Runs in a session other than the analysis's.
  Re-derives the grounds from the source rather than the report's account.
  Does not change anything.
metadata:
  goal: Each item has a score and its ground.
---

## Input

Required:

- The analysis report.
- The issue.

Helpful:

- The criteria review record.
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

- Score these items: conclusion grounds (whether the evidence, re-derived from the source, supports the structure as stated, the gap, whether a change is owed and the lever), the problem as given (whether the problem the report states is the one analysis was given, re-derived from the criteria review record and the criterion decisions, or from the issue's criteria when there is no record), goal coverage (whether the report answers everything the analysis owes, for the whole request).
- Score a well-grounded conclusion that no change is needed, or that the lever is not code, as high as a well-grounded code change.
- Do not mark down reuse of existing code.
- Score on a scale of 10: 9–10 excellent, 7–8 good, 5–6 insufficient, 3–4 poor, 1–2 failing.
- Read only; change nothing.
