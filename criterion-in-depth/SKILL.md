---
name: criterion-in-depth
description: >-
  Choose for a criterion whose cases the screen handed on for an in-depth look.
  Runs once per criterion, in a session given only that criterion's target file,
  so its verdict does not lean on the screen's.
metadata:
  goal: >-
    Each target case of the criterion has a verdict resting on the code that
    decides the behavior and the condition applied there.
---

## Input

Required:

- The criterion's target file.

## Exit

- End when every target case has a verdict.

## Output

For each target case:

- the verdict;
- the deciding code and condition, as `path:line` at the commit read;
- the grounds.

When the work stops, leave what was done and why it stopped.

## Default

- Rest a verdict on the deciding code, never on the point where the behavior shows alone.
- Where the behavior occurs only under a condition, check whether a situation that does not meet it arises, and from which input, state or flow; where one does, the behavior does not hold there.
- Change nothing in the target.
