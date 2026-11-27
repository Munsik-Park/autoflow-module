---
name: analysis
description: >-
  Choose when the request, and the cause of a defect it reports, must be
  understood before deciding on a change. Restates the issue's acceptance
  criteria. Usually after the criteria review, or first when there is none, and
  before criteria-apply, hypothesis and design. Re-run with an evaluation or
  findings to answer. Does not design or change code.
metadata:
  goal: >-
    The request is understood well enough to be evaluated: the structure as it
    stands, the gap, whether a change is owed and whether code is the lever,
    and the decision points, each conclusion with its grounds.
---

## Input

Required:

- The issue.

Helpful:

- The criteria review record.
- The criterion decisions.
- The target's documents.
- On a re-run, the previous report and the evaluation or findings to answer.

## Exit

- End when every conclusion has its grounds or is recorded as not established, with what was left unchecked.

## Output

The report:

- how the analysis was done;
- the affected area as it stands;
- the cases the request names, their problem type and the resolution approaches;
- an acceptance criteria table: for each criterion, its id, the criterion restated faithfully and its place in the issue;
- each material the issue or a criterion references, with what it shows or why it could not be opened;
- per approach, the gap and whether code is the lever;
- the conclusion: no change needed, the lever is not code, or the code changes;
- for a defect, the cause and its evidence, or what is known and what was left unchecked;
- each scope judgment (other sites of the cause, what fixing it exposes) with its grounds;
- the documents the change is expected to update;
- each decision point with its decision and grounds;
- each criterion shown wrong: its id, the fact that shows it wrong, how that was checked, the change proposed if any, and where the reading stops;
- each point it could not decide with confidence.

When the work stops, leave what was done and why it stopped.

## Default

- State the structure as fact, apart from the issue's hypothesis.
- Conclude that code must change only on evidence that none of data, configuration, the environment or an earlier fix closes the gap, since a coding agent tends to write new code where none is needed.
- Do not present a cause that is not established as established.
- Do not mark down a resolution for reusing existing code, since a coding agent tends to write anew what existing code already provides.
- Open every material the issue or a criterion references yourself, since what the issue or someone else says of a material can differ from what the material shows.
- On a re-run, keep the acceptance criteria table unchanged: a change to a criterion stands only as a decision.
- Change nothing in the target.
