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
- Stop when the work for a test can go on only by a change to the target's tests in the tree, fixtures, `conftest`, test settings or workflow files beyond what the tests it is made for need or outside them, naming it.
- Before each test run, whether an instruction asks for it or not, judge whether it fits in its method and environment and within what the machine shares with other work. When it does not, by that judgment or as a failure shows, state the misfit and its grounds, find a form that fits and can show what the run is meant to show, and run it in its place. Stop on a misfit only when no such form can run for want of a tool, permission or environment that cannot be obtained, naming what is needed.

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

- each one-off run: its script and log, its result, the conditions it ran under, and what its fit was judged from;
- each test run that did not fit: the misfit and its grounds, and the form run in its place with how it differs and how it shows what the run was meant to show, or, when the work stopped, the tool, permission or environment that could not be obtained;
- each change made for a test to the target's tests in the tree, fixtures, `conftest`, test settings or workflow files: the files it touches and the grounds that the rest of the suite and the CI workflow run as before.

When the work stops, leave what was done and why it stopped.

## Default

- Classify each test by when the defect it checks surfaces: one run on the change's checkout settles it, or it surfaces only after deployment. Read this from the target's code, documents, build, packaging and deployment files and CI configuration, and record what was read.
- Place a test in the target only when its defect surfaces only after deployment, its failure breaks the deployment or the operation as a whole, and a job in the target's CI configuration runs it. That a later change could break the behavior is no ground for placing a test.
- Do not add to or change what the target's CI runs in order to place a test.
- A change made for a test to the target's tests in the tree, fixtures, `conftest`, test settings or workflow files holds only what the tests it is made for need and stays inside them, so the rest of the suite and the CI workflow run as before. A placed test written into the tree is not itself an addition to or a change of what the target's CI runs.
- Make a placed test follow the target's test conventions and be reached by its test discovery.
- Keep every other test in the work folder and run it by its path.
- Write each run's log in the work folder.
- Run each test on a checkout whose status shows no change and no untracked file outside what the target ignores, and record that status and the commit it was at.
- Choose for each test run a method and an environment that fit what the test is meant to show.
- Run a one-off run, one that repeats a test, adds load, stresses or times it, only within what the machine shares with other work: the other sessions, other runs and the operator's tools. Judge its fit from what can be read on the machine, and record what the judgment was read from.
- Keep each one-off run's script in the work folder with its log and result.
- Commit a test only when it is placed, and before its run: put no implementation in its commit, write the commit message as `<type>(#<issue>): <description>`, and run the target's lint over the staged files before the commit.
- Do not push.
