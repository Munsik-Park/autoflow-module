---
name: criterion-reconcile
description: >-
  Settles the criteria review into one record: takes criterion-screen's review
  record, criterion-trace's findings and criterion-in-depth's verdicts, and
  settles each difference between them in the code. Runs in a session of its
  own. Its record is the result of the criteria review: whether the problem
  the issue raises holds and what causes it, how far the cause reaches, and
  each criterion's disposition. The record is the problem analysis takes; its
  dispositions that change a criterion's content, and the items it leaves
  undecided, are the points criterion-decision decides.
metadata:
  goal: >-
    The review record agrees with the trace and the in-depth verdicts, each
    difference settled in the code, and every item has its disposition.
---

## Input

Required:

- The review record criterion-screen wrote.
- The trace.

Helpful:

- The in-depth verdicts.

## Exit

- End when every difference is settled or recorded as undecided.

## Output

The review record brought up to date, as a new file:

- the screen's record with the trace findings added as settled;
- per trace finding and per in-depth case, whether it was applied, rejected or left unresolved, with grounds;
- every item with its disposition, and the text of each disposition that changes a criterion: revised with its text, split with the id and text of each criterion it makes, added with its text;
- each item it could not decide with confidence.

When the work stops, leave what was done and why it stopped.

## Default

- Record a criterion that does not hold in a case it applies to as a finding for that case, with the rule or condition that prevents it; never record it as holding conditionally.
- Leave the screen's record as it is.
- Change nothing in the target.
