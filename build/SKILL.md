---
name: build
description: >-
  Choose when the design is settled and the change must be implemented on the
  branch. Implements the design within its scope, makes the tests it is given
  pass without changing them, checks each item of the verification design as
  it says, and records the results. Leaves commits on the branch. Re-run on the
  same branch with findings to answer them. Usually used after test-first,
  before the evaluations and delivery. Does not push or open a pull request.
metadata:
  goal: The design is implemented within its scope on the branch, the tests it was given pass, and each item of the verification design is checked as it says or the reason it is not is recorded.
---

## Input

Required:

- The branch.
- The acceptance criteria applied.
- The feature design, with its scope.
- The verification design.

Helpful:

- The tests written for the change, with their run records.
- The issue.
- On a re-run, the previous report and the findings to answer.
- The findings deferred or separated.

## Exit

- End when the scope is implemented and each item is checked.
- Stop when the work can go on only by changing a test you were given, when the criteria cannot all hold together, or when a criterion is shown wrong. Record what blocks.
- Stop when a run leaves a change or an untracked file outside what the target ignores, naming what it left.
- Stop when the work can go on only by a change to what the target's CI runs beyond what the tests it is made for need, naming it.
- When a test run does not fit in its method or environment, whether an instruction asks for it or a failure shows it, state the misfit and its grounds, and run a form that fits in its place when one shows what the run is meant to show; otherwise stop.

## Output

The commit range:

- the branch;
- its head when the run began;
- its head when the run ended.

The report:

- each criterion and each verification item, with how it was checked (command, log, summary line) and its result, or why it was not checked;
- each test you wrote: its path, the item it checks, and when the defect it checks surfaces, with the grounds read;
- the passing run of each test you were given and of each test you wrote: the command, the log, the summary line, the exit status, the commit the code was at, the checkout's status, and the SHA-256 of each test file it ran;
- the documents you changed;
- the lint result for each commit;
- each scope judgment;
- each test placed in the target's tree, with the defect it guards, the CI job expected to run it and the configuration file that was read from;
- each test whose defect surfaces only after deployment and whose failure breaks the deployment or the operation as a whole, but that no job in the target's CI configuration runs, with the defect it would guard and that no job runs it;
- what was set to direct the files each test run writes;
- each one-off run: its script and log, the CPU count, the load averages before and after it and at each failure, the other work read as process names and counts without their arguments, the processes it ran in parallel, its number of runs, its projected and actual length, the target's per-test timeout, and its result, with the failure rate its runs rule out when none failed;
- each test run that did not fit: the misfit and its grounds, and the form run in its place with how it differs, or that the work stopped;
- each change to what the target's CI runs: the files it touches and what the target's test discovery collected before and after it.

When the work stops, leave what was done and what blocks, with how to reproduce it.

## Default

- Do not change a test you were given.
- Do not fit the code to test inputs: no hard-coding and no special cases.
- Record an improvement beyond the scope as a scope judgment instead of making it.
- Keep the comments the change adds free of issue or pull request numbers, review rounds, criterion ids, change history and restatements of the code.
- Classify each test you write by when the defect it checks surfaces: one run on the change's checkout settles it, or it surfaces only after deployment. Read this from the target's code, documents, build, packaging and deployment files and CI configuration, and record what was read.
- Place a test you write in the target only when its defect surfaces only after deployment, its failure breaks the deployment or the operation as a whole, and a job in the target's CI configuration runs it. That a later change could break the behavior is no ground for placing a test.
- Keep a change to what the target's CI runs (its tests in the tree, fixtures, `conftest`, test settings and workflow files) to what the tests it is made for need, and inside them: change only the files that hold those tests, define a fixture or helper where only those tests reach it and apply it to each of them explicitly, and change no shared fixture or helper file, test setting or workflow file. List what the target's test discovery collects before and after the change, and record that it is the same outside those tests.
- Make a placed test follow the target's test conventions and be reached by its test discovery.
- Keep every other test you write in the work folder.
- Write each run's log in the work folder.
- Run the target's tests locally once, the way the target runs them, and each test you were given or wrote that is not placed once by its path.
- Make each run on the head the run ends at, on a checkout whose status shows no change and no untracked file outside what the target ignores, and record that status and the commit.
- Direct the files a test run writes (caches, reports, temporary and home folders) to the work folder or to what the target ignores, through the tools' options or environment, and record what was set. Remove no file.
- Choose for each test run a method whose single run settles what the run is meant to show. Use a one-off run, one that repeats a test, adds load, stresses or times it, only when no such method exists, and state the failure rate its runs without a failure rule out (about 3/n at 95% confidence for n runs).
- Run a one-off run only within what the machine shares with other work: the other sessions, other runs and the operator's tools. Before it, read the CPU count, the 1- and 5-minute load averages and the processes of other work by name and count, without their arguments, run it once to measure its length, and project its total length. It fits the machine when the processes it runs in parallel, each worker of a test runner counted, number at most what the instructions set or, where they set none, half the CPU count, and, added to the higher load average, stay within the CPU count; a load already at or above the CPU count leaves no room. It fits in time when the projected length of all the module run's one-off runs stays within the time the instructions set or, where they set none, 15 minutes. The instructions set that time and that number, not the fit against the current load: it is read when the run starts, and a run an instruction asks for that fails it does not fit.
- Stop a one-off run that passes that time, stop every process a one-off run started, and confirm that none is left before the module run ends.
- A single run of the target's tests, or of the files of them an instruction names, with the target's settings, is not a one-off run: keep those settings, its parallelism included, and run no one-off run beside it. Running the same tests again is a repeat.
- Read the load averages when a one-off run fails. Record a failure of a one-off run that coincides, by that reading, with a load above the CPU count, or with the target's per-test timeout firing where what the test shows is not itself a hang or a time, as a condition of the environment: what the run is meant to show is then not shown, neither as a pass nor as a confirmed failure, and the run does not fit. A failure of any other run is a result about the test.
- Keep each one-off run's script in the work folder with its log and result.
- Commit a test you write only when it is placed, and before its run.
- Write commit messages as `<type>(#<issue>): <description>`.
- Run the target's lint over the staged files before each commit.
- Do not push.
