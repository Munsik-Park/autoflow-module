---
name: test-first
description: >-
  Choose when the required behavior must be pinned by tests before it is
  implemented. Writes a test for each item the verification design checks by
  test and shows it failing on the code without the implementation. Each test
  stays in the work folder with its run record; only a test that guards a
  defect surfacing only after deployment and breaking the deployment or the
  operation as a whole, and that a job of the target's CI runs, is committed on
  the branch. Usually used after design and before build. Does not implement
  the change.
metadata:
  goal: Each item to be checked by test has a test, seen failing on the code without the implementation, shown by its log.
---

## Input

Required:

- The branch.
- The acceptance criteria applied.
- The verification design.

Helpful:

- The feature design.
- The issue.

## Exit

- End when each item has its test and its failing run.
- Stop when a test of a required behavior already passes on the current code, naming the item.
- Stop when a run leaves a change or an untracked file outside what the target ignores, naming what it left.
- Stop when the work for a test can go on only by a change to what the target's CI runs beyond what the tests it is made for need, naming it.
- When a test run does not fit in its method or environment, whether an instruction asks for it or a failure shows it, state the misfit and its grounds, and run a form that fits in its place when one shows what the run is meant to show; otherwise stop.

## Output

For each test:

- its path;
- the item it checks;
- when the defect it checks surfaces, with the grounds read;
- whether it is placed in the target;
- its run on the current code: the command, the log, the summary line, the exit status, the commit the code was at, the checkout's status, and the SHA-256 of each test file it ran;
- for a placed test, the defect it guards, the CI job expected to run it and the configuration file that was read from, and its commit;
- for a test whose defect surfaces only after deployment and whose failure breaks the deployment or the operation as a whole, but that no job in the target's CI configuration runs, the defect it would guard and that no job runs it.

For the runs:

- what was set to direct the files each test run writes;
- each one-off run: its script and log, the CPU count, the load averages before and after it and at each failure, the other work read as process names and counts without their arguments, the processes it ran in parallel, its number of runs, its projected and actual length, the target's per-test timeout, and its result, with the failure rate its runs rule out when none failed;
- each test run that did not fit: the misfit and its grounds, and the form run in its place with how it differs, or that the work stopped;
- each change to what the target's CI runs: the files it touches and what the target's test discovery collected before and after it.

When the work stops, leave what was done and why it stopped.

## Default

- Classify each test by when the defect it checks surfaces: one run on the change's checkout settles it, or it surfaces only after deployment. Read this from the target's code, documents, build, packaging and deployment files and CI configuration, and record what was read.
- Place a test in the target only when its defect surfaces only after deployment, its failure breaks the deployment or the operation as a whole, and a job in the target's CI configuration runs it. That a later change could break the behavior is no ground for placing a test.
- Keep a change to what the target's CI runs (its tests in the tree, fixtures, `conftest`, test settings and workflow files) made for a test to what the tests it is made for need, and inside them: change only the files that hold those tests, define a fixture or helper where only those tests reach it and apply it to each of them explicitly, and change no shared fixture or helper file, test setting or workflow file. List what the target's test discovery collects before and after the change, and record that it is the same outside those tests. A change to what the target's CI runs that the scope itself names is the scope's work, not a change made for a test.
- Make a placed test follow the target's test conventions and be reached by its test discovery.
- Keep every other test in the work folder and run it by its path.
- Write each run's log in the work folder.
- Run each test on a checkout whose status shows no change and no untracked file outside what the target ignores, and record that status and the commit it was at.
- Direct the files a test run writes (caches, reports, temporary and home folders) to the work folder or to what the target ignores, through the tools' options or environment, and record what was set. Remove no file.
- Choose for each test run a method whose single run settles what the run is meant to show. Use a one-off run, one that repeats a test, adds load, stresses or times it, only when no such method exists, and state the failure rate its runs without a failure rule out (about 3/n at 95% confidence for n runs).
- Run a one-off run only within what the machine shares with other work: the other sessions, other runs and the operator's tools. Before it, read the CPU count, the 1- and 5-minute load averages and the processes of other work by name and count, without their arguments, and judge whether it fits the machine; only then run it once, within that fit, to measure its length, and project its total length. It fits the machine when the processes it runs in parallel, each worker of a test runner counted, number at most what the instructions set or, where they set none, half the CPU count, and, added to the higher load average or, where it is greater, the number of other work's processes then using a CPU, read from their state or CPU use and not their arguments, stay within the CPU count; a load already at or above the CPU count leaves no room. It fits in time when the projected length of all the module run's one-off runs stays within the time the instructions set or, where they set none, 15 minutes. The instructions set that time and that number, not the fit against the current load: it is read when the run starts, and a run an instruction asks for that fails it does not fit.
- Stop the one-off runs when together they pass that time, stop every process a one-off run started, and confirm that none is left before the module run ends.
- A single run of the target's tests, or of the files of them an instruction names, with the target's settings, is not a one-off run: keep those settings, its parallelism included, and run no one-off run beside it. Running the same tests again within the module run is a repeat.
- Read the load averages when a one-off run fails. Record a failure of a one-off run that coincides, by that reading, with a load above the CPU count, the target's per-test timeout firing included, as a condition of the environment: what the run is meant to show is then not shown, neither as a pass nor as a confirmed failure, and the run does not fit. A failure of a one-off run at a load within the CPU count, a timeout included, and a failure of any other run, is a result about the test.
- Keep each one-off run's script in the work folder with its log and result.
- Commit a test only when it is placed, and before its run: put no implementation in its commit, write the commit message as `<type>(#<issue>): <description>`, and run the target's lint over the staged files before the commit.
- Do not push.
