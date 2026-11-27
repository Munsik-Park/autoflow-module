---
name: criteria-apply
description: >-
  Choose after analysis to fix the acceptance criteria the work goes by. Later
  modules take its output instead of the report's table. Applies decisions;
  judges nothing.
metadata:
  goal: The applied criteria are the report's criteria with every settled decision applied, in order.
---

## Input

Required:

- The analysis report.

Helpful:

- The criterion decisions, each naming the criterion, its disposition (excluded, revised, split or added) and the text it decides.

## Exit

- End when every decision is applied.

## Output

The criteria as applied, in order, each with:

- its id;
- its text.

The decisions applied, in order.

When the work stops, leave what was done and why it stopped.

## Default

- Where a decision supersedes an earlier one, apply it in place of the earlier one.
- Change no criterion beyond what a decision states.
- Change nothing in the target.
