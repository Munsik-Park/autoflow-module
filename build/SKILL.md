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
- each test that meets the conditions for placement but that no job in the target's CI configuration runs, with the defect it would guard and that no job runs it.

When the work stops, leave what was done and what blocks, with how to reproduce it.

## Default

- Do not change a test you were given.
- Do not fit the code to test inputs: no hard-coding and no special cases.
- Record an improvement beyond the scope as a scope judgment instead of making it.
- Keep the comments the change adds free of issue or pull request numbers, review rounds, criterion ids, change history and restatements of the code.
- Classify each test you write by when the defect it checks surfaces: one run on the change's checkout settles it, or it surfaces only after deployment. Read this from the target's code, documents, build, packaging and deployment files and CI configuration, and record what was read.
- Place a test you write in the target only when its defect surfaces only after deployment, its failure breaks the deployment or the operation as a whole, and a job in the target's CI configuration runs it. That a later change could break the behavior is no ground for placing a test.
- Do not add to or change what the target's CI runs in order to place a test.
- Make a placed test follow the target's test conventions and be reached by its test discovery.
- Keep every other test you write in the work folder.
- Write each run's log in the work folder.
- Run the target's tests locally once, the way the target runs them, and each test in the work folder once by its path.
- Make each run on the head the run ends at, on a checkout whose status shows no change and no untracked file outside what the target ignores, and record that status and the commit.
- Commit a test you write only when it is placed, and before its run.
- Write commit messages as `<type>(#<issue>): <description>`.
- Run the target's lint over the staged files before each commit.
- Do not push.
