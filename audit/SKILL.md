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
- Stop before any test run whose method and scale have not been judged against what the run must verify, which the judgment does not change: neither too little to show it nor more than showing it needs. When they do not fit, by that judgment or as a failure shows, state this with its grounds, choose a method and scale that fit, and run them. Stop on a misfit only when no method and scale that fit can run for want of a tool, permission or environment that cannot be obtained, naming what is needed.

## Output

For each test:

- the evidence read: its run records, their logs and the SHA-256 of its files;
- the judgment.

For each item:

- the score;
- its ground.

Findings, each with its severity, `path:line`, weight and the grounds of the weight, and recommendations.

For the runs:

- each test run it made: the command, the log and its result, and for a run made beyond the target's own tests (any run other than one run of a test, with nothing added to it or to what it runs under, the way the target runs its tests or by its path), also its script and the conditions it ran under;
- each test run that did not fit: the misfit and its grounds, and the method and scale run in its place with how they differ and how they show what the run must verify, or, when the work stopped, the tool, permission or environment that could not be obtained.

On a re-score, which items were scored afresh and which were inherited.

When the work stops, leave what was done and why it stopped.

## Default

- Score these items: authentication and authorization, input validation, data exposure, infrastructure isolation, dependencies.
- Score each item on a scale of 10: 9–10 excellent, 7–8 good, 5–6 insufficient, 3–4 poor, 1–2 failing.
- Give each finding one weight by two questions. First: can its problem occur in the process the target runs in? Second: does the target's actual use bring the problem about, and does what the target requires oblige addressing it? The actual use is who or what uses the target, how much, on what inputs and at what point of its development, including anyone untrusted who can reach it; an input that comes from outside the target can carry whatever its form allows, and a condition that use meets, however rarely, brings the problem about, while one it does not meet does not. Answer both from what is stated, as the target's maintainers would: a finding can hold and still describe a use the target does not have. What the target requires is what is stated for the property the finding concerns or, where nothing is, what the change sets out to do, what the target's actual use relies on and the rigor the rest of the target keeps; a problem the change neither introduces nor makes reachable or worse is not one the change is required to address, and of a problem it makes reachable or worse, the change addresses what keeps the change from bringing it about and leaves the cause where it is, in code the change does not change, since fixing that cause reaches beyond the change. A criterion the finding was measured by that nothing states says what was checked, not how far the target must meet it. Where the target's actual use can bring about a problem that the change introduces or makes reachable or worse and one occurrence of which would do harm that cannot be undone, such as data lost, secrets or personal data exposed, or access control broken, what the target requires obliges addressing what keeps the change from bringing it about, since that harm does not shrink with how rarely it occurs. The weight is one of:
  - `cannot occur`: the process the target runs in cannot bring the problem about;
  - `need not be addressed`: it can occur, but the target's actual use does not bring it about or what the target requires does not oblige addressing it;
  - `must be addressed`: it can occur, the target's actual use brings it about, and what the target requires obliges addressing it;
  - `not established`: what is stated does not show enough to answer either question.
- Stated means stated by, first to last: the instructions of the call, and the target's own documents and files before the change's commits. Anything else read counts only where it cites one of these. Where two differ, the earlier stands, and the grounds name both.
- Record the weight's grounds: the instructions' passage, a document's section and quoted sentence, or a file and line at a commit; for `not established`, what was looked for and where.
- The weight changes neither severity nor any score.
- Judge each test from its run records. A record is a run only when the log at its path carries the recorded summary line; state any other record as not run.
- Confirm test-first for a test when its failing run is on a commit whose history has none of the commits after the head the first build run on the branch began at, up to the head the last build run ended at, its passing run is on a commit whose history has all of them, both records show a checkout whose status shows no change and no untracked file outside what the target ignores, and both give the SHA-256 its files have.
- Keep the script of each run made beyond the target's own tests in the work folder with its log and result.
- Only read; change nothing.
