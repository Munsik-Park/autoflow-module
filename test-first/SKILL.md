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

## Output

For each test:

- its path;
- the item it checks;
- when the defect it checks surfaces, with the grounds read;
- whether it is placed in the target;
- its run on the current code: the command, the log, the summary line, the exit status, the commit the code was at, the checkout's status, and the SHA-256 of each test file it ran;
- for a placed test, the defect it guards, the CI job expected to run it and the configuration file that was read from, and its commit;
- for a test that meets the conditions for placement but that no job in the target's CI configuration runs, the defect it would guard and that no job runs it.

When the work stops, leave what was done and why it stopped.

## Default

- Classify each test by when the defect it checks surfaces: one run on the change's checkout settles it, or it surfaces only after deployment. Read this from the target's code, documents, build, packaging and deployment files and CI configuration, and record what was read.
- Place a test in the target only when its defect surfaces only after deployment, its failure breaks the deployment or the operation as a whole, and a job in the target's CI configuration runs it. That a later change could break the behavior is no ground for placing a test.
- Do not add to or change what the target's CI runs in order to place a test.
- Make a placed test follow the target's test conventions and be reached by its test discovery.
- Keep every other test in the work folder and run it by its path.
- Write each run's log in the work folder.
- Run each test on a checkout whose status shows no change and no untracked file outside what the target ignores, and record that status and the commit it was at.
- Commit a test only when it is placed, and before its run: put no implementation in its commit, write the commit message as `<type>(#<issue>): <description>`, and run the target's lint over the staged files before the commit.
- Do not push.
