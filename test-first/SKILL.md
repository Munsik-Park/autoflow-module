---
name: test-first
description: >-
  Choose when the required behavior must be pinned by tests before it is
  implemented. Each test stays in the work folder with its run record; only a
  test the target must keep is committed on the branch. Usually used after
  design and before build. Does not implement the change.
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
- Stop when the work for a test can go on only by a change beyond what that test needs or outside it, naming it.
- Stop before any test run whose method and scale have not been judged against what the run must verify, which the judgment does not change: neither too little to show it nor more than showing it needs. When they do not fit, by that judgment or as a failure shows, state this with its grounds, choose a method and scale that fit, and run them. Stop on a misfit only when no method and scale that fit can run for want of a tool, permission or environment that cannot be obtained, naming what is needed.

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

- each test run it made: the command, the log and its result, and for a run made beyond the target's own tests (any run other than one run of a test, with nothing added to it or to what it runs under, the way the target runs its tests or by its path), also its script and the conditions it ran under;
- each test run that did not fit: the misfit and its grounds, and the method and scale run in its place with how they differ and how they show what the run must verify, or, when the work stopped, the tool, permission or environment that could not be obtained;
- each change made for a test: what it changes and the grounds that the target's other tests and its CI run as before.

When the work stops, leave what was done and why it stopped.

## Default

- Classify each test by when the defect it checks surfaces: one run on the change's checkout settles it, or it surfaces only after deployment. Read this from the target's code, documents, build, packaging and deployment files and CI configuration, and record what was read.
- Place a test in the target only when its defect surfaces only after deployment, its failure breaks the deployment or the operation as a whole, and a job in the target's CI configuration runs it. A placed test is maintained like the code and runs in every later review and verification, while a later change is checked by its own run.
- To place a test, add only the test; change nothing else the target's CI runs.
- Anything changed for a test, such as a fixture or a setting, applies to that test alone and holds only what it needs, so the other tests and CI run as before.
- Make a placed test follow the target's test conventions and be reached by its test discovery.
- Keep every other test in the work folder and run it by its path.
- Write each run's log in the work folder.
- Run each test on a checkout whose status shows no change and no untracked file outside what the target ignores, and record that status and the commit it was at.
- Keep the script of each run made beyond the target's own tests in the work folder with its log and result.
- Commit a test only when it is placed, and before its run: put no implementation in its commit, write the commit message as `<type>(#<issue>): <description>`, and run the target's lint over the staged files before the commit.
- Do not push.
