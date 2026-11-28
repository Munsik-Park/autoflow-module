---
name: criterion-decision
description: >-
  Choose when a criteria review disposes of a criterion by changing its
  content or leaves an item undecided. Decides each point from the material
  itself, weighing the reading it is given without taking its conclusion. Runs
  in a new session of its own. Its decisions are the criterion decisions
  criteria-apply applies and the modules that work by the criteria take. Does
  not decide how a criterion is verified or how the change is made.
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
- Change a decision already made only on new grounds: a fact unavailable when it was made, shown by a commit, a command's result or a file at a commit, or an error in its grounds that a command reproduces.
- Where two decisions already made on a criterion put to it disagree, decide between them and name both.
- Ground each decision: a commit and `path:line` for a fact of the code, a command and its result, or a document, its section and a quoted sentence for a policy.
- Do not decide how a criterion is verified.
- Change nothing in the target.
