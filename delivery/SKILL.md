---
name: delivery
description: >-
  Choose when the change is committed on its branch, its local tests pass, and
  it must reach the operator as a pull request. Pushes the branches and opens a
  pull request in each repository the change touches, sub-repositories
  included, with the parent's pointer commit where one is needed. The body
  states each acceptance criterion with its outcome and evidence, how the
  change was shown working, what could not be verified and why, and what is
  left undone, so the operator can decide on it. Usually used after the build
  and its evaluations, before ci and review. Does not change the change's code,
  re-run its tests or merge.
metadata:
  goal: Each branch of the change is pushed and has a pull request whose body lets the operator decide on it.
---

## Input

Required:

- The issue.
- The change (its branches and commits).
- The acceptance criteria applied to it.
- The build report (its local test results).

Helpful:

- How each criterion was verified.
- The quality evaluation.
- The feature design.
- What the work lacked (tools, permissions).
- The findings deferred or separated.
- The base branch.

## Exit

- End when every branch of the change is pushed and has its pull request.
- Stop before pushing when the change's local tests are not shown passing.

## Output

For each branch:

- the repository;
- the branch;
- the head commit;
- its pull request.

When the work stops, leave what was pushed or opened, and why it stopped.

## Default

- Open each pull request as a draft on the repository's default branch.
- Title each pull request `[<type> · #<issue>] <description>`.
- Make the pull request in the issue's repository close the issue (`Closes #<n>`); make the others reference it.
- State in the body, at the commit it stands on:
  - each applied criterion with met or not, and its evidence;
  - each item verified other than by a test, with the method and why;
  - what could not be verified and why;
  - what is left undone.
- Write the evidence in the body or in files of the repository: the work folder is local.
- Change nothing else: do not change code, merge, mark a pull request ready or add a label.
