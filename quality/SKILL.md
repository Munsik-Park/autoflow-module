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
- Stop when a test run leaves a change or an untracked file outside what the target ignores, naming what it left.
- When a test run does not fit in its method or environment, whether an instruction asks for it or a failure shows it, state the misfit and its grounds, and run a form that fits in its place when one shows what the run is meant to show; otherwise stop.

## Output

For each item:

- the score;
- its ground.

Findings with their severity, `path:line`, weight and the grounds of the weight, and recommendations. A carried finding names its source, and a weight given here names the weight it carried.

For the test runs it made:

- what was set to direct the files each test run writes;
- each one-off run: its script and log, the CPU count, the load averages before and after it and at each failure, the other work read as process names and counts without their arguments, the processes it ran in parallel, its number of runs, its projected and actual length, the target's per-test timeout, and its result, with the failure rate its runs rule out when none failed;
- each test run that did not fit: the misfit and its grounds, and the form run in its place with how it differs, or that the work stopped.

On a re-score, which items were scored afresh and which were inherited.

When the work stops, leave what was done and why it stopped.

## Default

- Score these items: completeness, quality, test coverage, test quality, security (from the audit), fit, impact scope, minimal implementation, commit conventions, documentation updates.
- Take the test-first judgment of each test from the audit evaluation when it is among the inputs and judged the commits after the head the first build run on the branch began at, up to the head the last build run ended at. Otherwise judge it here: a record is a run only when the log at its path carries the recorded summary line, and test-first is confirmed for a test when its failing run is on a commit whose history has none of the commits after the head the first build run on the branch began at, up to the head the last build run ended at, its passing run is on a commit whose history has all of them, both records show a checkout whose status shows no change and no untracked file outside what the target ignores, and both give the SHA-256 its files have.
- Score test coverage and test quality of a test not placed in the target from its run records and its test-first judgment. A recorded line its log does not carry counts against the item that cites it.
- Under test quality, count against it a test placed in the target whose defect one run on the change's checkout settles, whose failure does not break the deployment or the operation as a whole, or that no job in the target's CI configuration runs; a placed test without the defect it guards and its CI job stated; and a change to what the target's CI runs (its tests in the tree, fixtures, `conftest`, test settings and workflow files) made for a test beyond what the tests it was made for need or outside them, or without the test discovery's lists before and after it.
- Judge minimal implementation against the smallest sufficient change that resolves the confirmed problem within the scope. Fail the item when a hunk traces to none of it.
- Score on a scale of 10: 9–10 excellent, 7–8 good, 5–6 insufficient, 3–4 poor, 1–2 failing.
- Give each finding one weight by two questions. First: can its problem occur where the target actually runs? A problem that needs no condition of that environment can; one that needs such a condition can unless a stated environment rules it out. Second: does the level the target requires for the property the finding concerns oblige addressing it? Without a level stated for that property, a problem that needs no such condition takes as its level the criterion it was measured by, which obliges addressing it. The weight is one of:
  - `cannot occur`: a stated environment rules the problem out;
  - `need not be addressed`: it can occur, and the level does not oblige addressing it;
  - `must be addressed`: it can occur, and the level obliges addressing it;
  - `not established`: it needs a condition of the environment, can occur, and no level for that property is stated; treated as must be addressed.
- Stated means stated by, first to last: the instructions of the call, the applied criteria, and the target's own documents and files before the change's commits. Anything else read counts only where it cites one of these. Where two differ, the earlier stands, and the grounds name both.
- Record the weight's grounds: the instructions' passage, a document's section and quoted sentence, a file and line at a commit, or the criterion; for `not established`, or where no environment was stated, what was looked for and where.
- A weight carried from the audit evaluation or the findings deferred or separated stands when it carries its grounds, is not `not established`, and no source earlier in that order than its grounds states otherwise; otherwise the finding is given a weight here.
- The weight changes neither severity nor any score.
- Direct the files a test run writes (caches, reports, temporary and home folders) to the work folder, through the tools' options or environment, and record what was set. Remove no file.
- Choose for each test run a method whose single run settles what the run is meant to show. Use a one-off run, one that repeats a test, adds load, stresses or times it, only when no such method exists, and state the failure rate its runs without a failure rule out (about 3/n at 95% confidence for n runs).
- Run a one-off run only within what the machine shares with other work: the other sessions, other runs and the operator's tools. Before it, read the CPU count, the 1- and 5-minute load averages and the processes of other work by name and count, without their arguments, and judge whether it fits the machine; only then run it once, within that fit, to measure its length, and project its total length. It fits the machine when the processes it runs in parallel, each worker of a test runner counted, number at most what the instructions set or, where they set none, half the CPU count, and, added to the higher load average or, where it is greater, the number of other work's processes then using a CPU, read from their state or CPU use and not their arguments, stay within the CPU count; a load already at or above the CPU count leaves no room. It fits in time when the projected length of all the module run's one-off runs stays within the time the instructions set or, where they set none, 15 minutes. The instructions set that time and that number, not the fit against the current load: it is read when the run starts, and a run an instruction asks for that fails it does not fit.
- Stop the one-off runs when together they pass that time, stop every process a one-off run started, and confirm that none is left before the module run ends.
- A single run of the target's tests, or of the files of them an instruction names, with the target's settings, is not a one-off run: keep those settings, its parallelism included, and run no one-off run beside it. Running the same tests again within the module run is a repeat.
- Read the load averages when a one-off run fails. Record a failure of a one-off run that coincides, by that reading, with a load above the CPU count, the target's per-test timeout firing included, as a condition of the environment: what the run is meant to show is then not shown, neither as a pass nor as a confirmed failure, and the run does not fit. A failure of a one-off run at a load within the CPU count, a timeout included, and a failure of any other run, is a result about the test.
- Keep each one-off run's script in the work folder with its log and result.
- Read only; change nothing.
