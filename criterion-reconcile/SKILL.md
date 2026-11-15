---
name: criterion-reconcile
description: >-
  Choose after criterion-trace and criterion-in-depth to settle the criteria
  review. Where a trace finding or an in-depth verdict differs from the
  screen's record, confirms in the code which holds and brings the record to
  match. Its record is the result of the review, each item with its
  disposition. Runs in a session of its own.
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
- every item with its disposition;
- each item it could not decide with confidence.

When the work stops, leave what was done and why it stopped.

## Default

- Record a criterion that does not hold in a case it applies to as a finding for that case, with the rule or condition that prevents it; never record it as holding conditionally.
- Leave the screen's record as it is.
- Change nothing in the target.
