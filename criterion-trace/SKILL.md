---
name: criterion-trace
description: >-
  Choose when it must be known how far each cause the criteria review
  confirmed reaches beyond the points the issue reports, and whether each
  behavior a criterion requires conflicts with the rules the code already has.
  Takes the issue and criterion-screen's review record only, in a session
  other than the screen's, and assumes no fix. Its findings add to what the
  criteria review settles about the problem the issue raises: how far its
  cause reaches, and whether what the criteria require can hold.
  criterion-reconcile settles them into the review record.
metadata:
  goal: >-
    For each confirmed cause, how far it reaches beyond the reported points,
    and for each required behavior, whether a rule or behavior in force keeps
    it from holding, each with grounds.
---

## Input

Required:

- The issue.
- The review record criterion-screen wrote.

## Exit

- End when each confirmed cause and each required behavior is judged.

## Output

Each finding, with:

- its question (cause reach or rule conflict);
- whether the screen's record already had it;
- its grounds.

When the work stops, leave what was done and why it stopped.

## Default

- Assume no fix: leave out an effect that would follow only from a particular approach.
- Ground each finding: for a fact of the code, a commit and `path:line`; for a policy, a document, its section and a quoted sentence.
- Change nothing in the target.
