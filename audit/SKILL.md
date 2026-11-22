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
- Stop when a test run leaves a change or an untracked file outside what the target ignores, naming what it left.
- When a test run does not fit in its method or environment, whether an instruction asks for it or a failure shows it, state the misfit and its grounds, and run a form that fits in its place when one shows what the run is meant to show; otherwise stop.

## Output

For each test:

- the evidence read: its run records, their logs and the SHA-256 of its files;
- the judgment.

For each item:

- the score;
- its ground.

Findings, each with its severity, `path:line`, weight and the grounds of the weight, and recommendations.

For the test runs it made:

- what was set to direct the files each test run writes;
- each one-off run: its script and log, the CPU count, the load averages before and after it and at each failure, the other work read as process names and counts without their arguments, the processes it ran in parallel, its number of runs, its projected and actual length, the target's per-test timeout, and its result, with the failure rate its runs rule out when none failed;
- each test run that did not fit: the misfit and its grounds, and the form run in its place with how it differs, or that the work stopped.

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
- Direct the files a test run writes (caches, reports, temporary and home folders) to the work folder, through the tools' options or environment, and record what was set. Remove no file.
- Choose for each test run a method whose single run settles what the run is meant to show. Use a one-off run, one that repeats a test, adds load, stresses or times it, only when no such method exists, and state the failure rate its runs without a failure rule out (about 3/n at 95% confidence for n runs).
- Run a one-off run only within what the machine shares with other work: the other sessions, other runs and the operator's tools. Before it, read the CPU count, the 1- and 5-minute load averages and the processes of other work by name and count, without their arguments, and judge whether it fits the machine; only then run it once, within that fit, to measure its length, and project its total length. It fits the machine when the processes it runs in parallel, each worker of a test runner counted, number at most what the instructions set or, where they set none, half the CPU count, and, added to the higher load average, stay within the CPU count; a load already at or above the CPU count leaves no room. It fits in time when the projected length of all the module run's one-off runs stays within the time the instructions set or, where they set none, 15 minutes. The instructions set that time and that number, not the fit against the current load: it is read when the run starts, and a run an instruction asks for that fails it does not fit.
- Stop the one-off runs when together they pass that time, stop every process a one-off run started, and confirm that none is left before the module run ends.
- A single run of the target's tests, or of the files of them an instruction names, with the target's settings, is not a one-off run: keep those settings, its parallelism included, and run no one-off run beside it. Running the same tests again is a repeat.
- Read the load averages when a one-off run fails. Record a failure of a one-off run that coincides, by that reading, with a load above the CPU count, or with the target's per-test timeout firing where what the test shows is not itself a hang or a time, as a condition of the environment: what the run is meant to show is then not shown, neither as a pass nor as a confirmed failure, and the run does not fit. A failure of any other run is a result about the test.
- Keep each one-off run's script in the work folder with its log and result.
- Only read; change nothing.
