---
name: test-first
description: >-
  Choose when the required behavior must be pinned by tests before it is
  implemented. Writes a test for each item the verification design checks by
  test and shows it failing on the code without the implementation. Tests the
  target should keep are committed on the branch; tests for this work only stay
  in the work folder. Usually used after design and before build. Does not
  implement the change.
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

## Output

For each test:

- its path;
- the item it checks;
- whether the target keeps it;
- its run on the current code: the command, the log, the summary line and the exit status;
- its commit.

When the work stops, leave what was done and why it stopped.

## Default

- Make each test the target keeps follow the target's test conventions and be reached by its test discovery.
- Keep any other test in the work folder and run it by its path.
- Put no implementation in a test commit.
- Write commit messages as `<type>(#<issue>): <description>`.
- Run the target's lint over the staged files before each commit.
- Do not push.
