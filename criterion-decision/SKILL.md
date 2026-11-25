---
name: criterion-decision
description: >-
  Choose when the work shows that the content of an acceptance criterion may
  have to change and that change is not yet decided: an output records a
  criterion shown wrong, a criteria review disposes of a criterion by changing
  its content or leaves an item undecided, or a finding would change what a
  criterion requires. Decides each point put to it (the criterion kept,
  revised, split, excluded or added) from the material itself, weighing the
  reading it is given without taking its conclusion. Runs in a new session of
  its own, never the session whose work raised the point. Its decisions are
  the criterion decisions criteria-apply and the later modules take. Does not
  decide how a criterion is verified or how the change is made.
metadata:
  goal: Each point put to it has a decision (the criterion kept, revised, split, excluded or added), with the text it decides and its grounds.
---

## Input

Required:

- The issue.
- The points to decide, each with the criterion, what was found against it and how that was checked, the change proposed if any, and the reading that raised it with where that reading stops.

Helpful:

- The output that records each point.
- The criterion decisions already made, with their grounds.
- The acceptance criteria applied.
- The target's documents.

## Exit

- Ends when every point has a decision.
- Stops when a decision needs a tool, permission or environment that cannot be obtained, naming what is needed.

## Output

The decision record:

- the situation;
- per point, the criterion's id, the decision, the text decided on one line (for revised and added; for split, each criterion it makes with its id and text), the options weighed, the grounds, and one command with its result that checks the fact the decision rests on;
- for a decision that replaces an earlier one, that decision and the fact or reproduced error that allows it;
- each further point the decisions raise, for the coordination session to put to it;
- what it could not confirm and what it needed.

When stopped: what was done and why it stopped.

## Default

- Decide from the material: open what a decision relies on and run what a claim needs to be checked; the reading given is where to start, and its conclusion is not grounds.
- Decide the points given, and those only.
- A criterion is wrong when a fact it presumes does not hold, or when its scope does not fit the problem: too narrow when the same cause reaches past what it names, too wide when it binds in a separate problem.
- Do not keep a criterion's letter by adding a rule it does not state.
- Keep what a criterion requires as behavior a user, a caller or an operator observes.
- Change a decision already made only on a fact that was not available when it was made and that a commit, a command's result or a file at a commit shows, or on an error in its grounds reproduced by a command; a different reading of the same material changes nothing.
- Where two decisions already made on a criterion put to it disagree, decide between them and name both.
- Ground each decision: a commit and `path:line` for a fact of the code, a command and its result, or a document, its section and a quoted sentence for a policy.
- Do not decide how a criterion is verified.
- Change nothing in the target.
