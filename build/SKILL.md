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

- The tests written for the change.
- The issue.
- On a re-run, the previous report and the findings to answer.
- The findings deferred or separated.

## Exit

- End when the scope is implemented and each item is checked.
- Stop when the work can go on only by changing a test you were given, when the criteria cannot all hold together, or when a criterion is shown wrong. Record what blocks.

## Output

The commit range:

- the branch;
- its head when the run began;
- its head when the run ended.

The report:

- each criterion and each verification item, with how it was checked (command, log, summary line) and its result, or why it was not checked;
- the passing run of each test you were given;
- the documents you changed;
- the lint result for each commit;
- each scope judgment;
- each test kept in the target's tree, with the CI job expected to run it.

When the work stops, leave what was done and what blocks, with how to reproduce it.

## Default

- Do not change a test you were given.
- Do not fit the code to test inputs: no hard-coding and no special cases.
- Record an improvement beyond the scope as a scope judgment instead of making it.
- Keep the comments the change adds free of issue or pull request numbers, review rounds, criterion ids, change history and restatements of the code.
- Run the tests locally once, the way the target runs them.
- Write commit messages as `<type>(#<issue>): <description>`.
- Run the target's lint over the staged files before each commit.
- Do not push.
