---
name: audit
description: >-
  Choose after build when an independent judgment is needed that each test of a
  required behavior failed on the code without the implementation and passes
  with it, together with a security score of the change. Runs in a session
  other than the one that made the change. Reads the change's commits, the
  build report, the test records and git. Does not change anything.
metadata:
  goal: Each test of a required behavior has a test-first judgment, and each security item has a score and its ground.
---

## Input

Required:

- The change (its commit range).
- The build report, and on a re-run of build the earlier build reports.
- The tests and their failing runs.

Helpful:

- The verification design.
- The previous evaluation (on a re-score).

## Exit

- End when test-first is judged and every item is scored.
- When test-first is not confirmed, score nothing and state what is missing.

## Output

For each test:

- the evidence read: its run records, their logs and the SHA-256 of its files;
- the judgment.

For each item:

- the score;
- its ground.

Findings, each with its severity, `path:line`, weight and the grounds of the weight, and recommendations.

On a re-score, which items were scored afresh and which were inherited.

When the work stops, leave what was done and why it stopped.

## Default

- Score these items: authentication and authorization, input validation, data exposure, infrastructure isolation, dependencies.
- Score each item on a scale of 10: 9–10 excellent, 7–8 good, 5–6 insufficient, 3–4 poor, 1–2 failing.
- Give each finding one weight by two questions. First: can its problem occur where the target actually runs? A problem that needs no condition of that environment can; one that needs such a condition can unless a stated environment rules it out. Second: does the level the target requires for the property the finding concerns oblige addressing it? Without a level stated for that property, a problem that needs no such condition takes as its level the criterion it was measured by, which obliges addressing it. The weight is one of:
  - `cannot occur`: a stated environment rules the problem out;
  - `need not be addressed`: it can occur, and the level does not oblige addressing it;
  - `must be addressed`: it can occur, and the level obliges addressing it;
  - `not established`: it needs a condition of the environment, can occur, and no level for that property is stated; treated as must be addressed.
- Stated means stated by, first to last: the instructions of the call, and the target's own documents and files before the change's commits. Anything else read counts only where it cites one of these. Where two differ, the earlier stands, and the grounds name both.
- Record the weight's grounds: the instructions' passage, a document's section and quoted sentence, a file and line at a commit, or the criterion; for `not established`, or where no environment was stated, what was looked for and where.
- The weight changes neither severity nor any score.
- Judge each test from its run records. A record is a run only when the log at its path carries the recorded summary line; state any other record as not run.
- Confirm test-first for a test when its failing run is on a commit whose history has none of the commits after the head the first build run on the branch began at, up to the head the last build run ended at, its passing run is on a commit whose history has all of them, both records show a checkout whose status shows no change and no untracked file outside what the target ignores, and both give the SHA-256 its files have.
- Only read; change nothing.
