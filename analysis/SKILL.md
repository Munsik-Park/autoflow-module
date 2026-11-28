---
name: analysis
description: >-
  Choose when the problem is set, by the criteria review or by the issue's
  criteria, and how to resolve it must be found before deciding on a change.
  Takes the problem as given, from the criteria review record where there is
  one and otherwise from the issue's criteria, with the criterion decisions
  where there are any, and finds whether a change is owed, whether code is the
  lever, the approaches and the decision points. Restates the issue's
  acceptance criteria. Its report is what hypothesis scores, what
  criteria-apply takes the criteria table from and what design works from;
  each criterion it shows wrong is stated with what shows it wrong, for a
  decision on that criterion. Re-run with an evaluation or findings to answer.
  Does not design or change code.
metadata:
  goal: >-
    How to resolve the problem as given is found well enough to be evaluated:
    the structure as it stands, the gap to close, whether a change is owed and
    whether code is the lever, the approaches and the decision points, each
    conclusion with its grounds.
---

## Input

Required:

- The issue.

Helpful:

- The criteria review record: the problem as the criteria review established it.
- The criterion decisions: the criteria as decided.
- The target's documents.
- On a re-run, the previous report and the evaluation or findings to answer.

## Exit

- End when every conclusion has its grounds or is recorded as not established, with what was left unchecked.

## Output

The report:

- how the analysis was done;
- the problem as given, and where it was taken from: the criteria review record and the criterion decisions, or the issue's criteria;
- the affected area as it stands;
- the cases the problem covers, their problem type and the resolution approaches;
- an acceptance criteria table: for each criterion, its id, the criterion restated faithfully and its place in the issue;
- each material the issue or a criterion references, with what it shows or why it could not be opened;
- per approach, the gap and whether code is the lever;
- the conclusion: no change needed, the lever is not code, or the code changes;
- each scope judgment (the sites the change must cover for the problem as given, what fixing it exposes) with its grounds;
- the documents the change is expected to update;
- each decision point with its decision and grounds;
- each criterion shown wrong: its id, the fact that shows it wrong, how that was checked, the change proposed if any, and where the reading stops;
- each part of the problem as given that what was read does not establish or contradicts: what was given, what was read, how that was checked, and where the reading stops;
- each point it could not decide with confidence.

When the work stops, leave what was done and why it stopped.

## Default

- Take the problem as given: what the criteria review record finds (each cause, its reach and the case verdicts), with the criteria as the criterion decisions leave them, or, without a record, what the issue's criteria state; a disposition in the record that changes a criterion stands only once a decision makes it. The criteria review establishes the problem with checks of its own, and a problem found again here can differ from it unchecked. Where what is read does not establish the problem or contradicts it, record that rather than establish the problem yourself.
- State the structure as fact, apart from the issue's hypothesis.
- Conclude that code must change only on evidence that none of data, configuration, the environment or an earlier fix closes the gap, since a coding agent tends to write new code where none is needed.
- Do not mark down a resolution for reusing existing code, since a coding agent tends to write anew what existing code already provides.
- Open every material the issue or a criterion references yourself, since what the issue or someone else says of a material can differ from what the material shows.
- On a re-run, keep the acceptance criteria table unchanged: a change to a criterion stands only as a decision.
- Change nothing in the target.
