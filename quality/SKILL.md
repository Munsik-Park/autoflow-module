---
name: quality
description: >-
  Choose after build when an independent score is needed of whether the change
  is complete, correct, verified and within its scope, against the acceptance
  criteria and the design. Runs in a session other than the one that made the
  change. Does not change anything.
metadata:
  goal: Each quality item has a score and its ground.
---

## Input

Required:

- The change (its commit range).
- The acceptance criteria applied.
- The build report, and on a re-run of build the earlier build reports.

Helpful:

- The feature design.
- The verification design.
- The tests and their failing runs.
- The analysis report (its scope judgments).
- The audit evaluation.
- The findings deferred or separated.
- The previous evaluation (on a re-score).

## Exit

- End when every item is scored.
- Stop before any test run whose method and scale have not been judged against what the run must verify, which the judgment does not change: neither too little to show it nor more than showing it needs. When they do not fit, by that judgment or as a failure shows, state this with its grounds, choose a method and scale that fit, and run them. Stop on a misfit only when no method and scale that fit can run for want of a tool, permission or environment that cannot be obtained, naming what is needed.

## Output

For each item:

- the score;
- its ground.

Findings with their severity, `path:line`, weight and the grounds of the weight, and recommendations. A carried finding names its source, and a weight given here names the weight it carried.

For the runs:

- each test run it made: the command, the log and its result, and for a run made beyond the target's own tests (any run other than one run of a test, with nothing added to it or to what it runs under, the way the target runs its tests or by its path), also its script and the conditions it ran under;
- each test run that did not fit: the misfit and its grounds, and the method and scale run in its place with how they differ and how they show what the run must verify, or, when the work stopped, the tool, permission or environment that could not be obtained.

On a re-score, which items were scored afresh and which were inherited.

When the work stops, leave what was done and why it stopped.

## Default

- Score these items: completeness, quality, test coverage, test quality, security (from the audit), fit, impact scope, minimal implementation, commit conventions, documentation updates.
- Take the test-first judgment of each test from the audit evaluation when it is among the inputs and judged the commits after the head the first build run on the branch began at, up to the head the last build run ended at. Otherwise judge it here: a record is a run only when the log at its path carries the recorded summary line, and test-first is confirmed for a test when its failing run is on a commit whose history has none of the commits after the head the first build run on the branch began at, up to the head the last build run ended at, its passing run is on a commit whose history has all of them, both records show a checkout whose status shows no change and no untracked file outside what the target ignores, and both give the SHA-256 its files have.
- Score test coverage and test quality of a test not placed in the target from its run records and its test-first judgment. A line in a run record that the run's log does not carry counts against the item that cites it.
- Under test quality, count against it a test placed in the target whose defect one run on the change's checkout settles, whose failure does not break the deployment or the operation as a whole, or that no job in the target's CI configuration runs; a placed test without the defect it guards and its CI job stated; anything other than the test changed in what the target's CI runs to place it; and anything changed for a test, apart from the designed change, that does more than the test needs or applies beyond it.
- Judge minimal implementation against the smallest sufficient change that resolves the confirmed problem within the scope. Fail the item when a hunk traces to none of it.
- Score on a scale of 10: 9–10 excellent, 7–8 good, 5–6 insufficient, 3–4 poor, 1–2 failing.
- Give each finding one weight. A weight says how far a problem must be addressed where the target is actually used. Judge it from what is stated, as the target's maintainers would: a finding can hold and still describe a use the target does not have, while a use it has, by anyone who can reach it, brings the problem about however rarely. What the target requires is what is stated for the property, or else what the change sets out to do and what its use relies on; a criterion nothing states is not a requirement. The change is required to address only its share: what it introduces and, for a problem it makes reachable or worse, keeping itself from bringing it about without fixing the cause, which is left to a separate change. Addressing harm that cannot be undone, such as data lost or exposed, is required within that share however rarely it comes about. The weight is one of:
  - `cannot occur`: the target's process cannot bring the problem about;
  - `need not be addressed`: it can, but the actual use does not, or nothing the target requires asks for it;
  - `must be addressed`: the actual use brings it about and what the target requires asks for it;
  - `not established`: what is stated does not settle the weight.
- Stated means stated by, first to last: the instructions of the call, the applied criteria, and the target's own documents and files before the change's commits. Anything else read counts only where it cites one of these. Where two differ, the earlier stands, and the grounds name both.
- Record the weight's grounds: the instructions' passage, a document's section and quoted sentence, or a file and line at a commit; for `not established`, what was looked for and where.
- A weight carried from the audit evaluation or the findings deferred or separated stands when it carries its grounds, is not `not established`, and no source earlier in that order than its grounds states otherwise; otherwise the finding is given a weight here.
- The weight changes neither severity nor any score.
- Keep the script of each run made beyond the target's own tests in the work folder with its log and result.
- Read only; change nothing.
