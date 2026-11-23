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
- The tests and their failing runs.
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
  - for each test, its runs: the command, the summary line, the exit status, the commit the code was at, the checkout's status, and the SHA-256 of its files;
  - each run made beyond the target's own tests (any run other than one run of a test, with nothing added to it or to what it runs under, the way the target runs its tests or by its path) that is evidence for a criterion or a test: its result and the conditions it ran under;
  - each test placed in the target, with the defect it guards and the CI job expected to run it;
  - each test whose defect surfaces only after deployment and whose failure breaks the deployment or the operation as a whole, but that no job in the target's CI configuration runs, with the defect it would guard and that no job runs it;
  - each item verified other than by a test, with the method and why;
  - what could not be verified and why;
  - the alternatives the design set aside and why, when the design records them;
  - what is left undone.
- Write the evidence in the body or in files of the repository: the work folder is local. Write the result and conditions of such a run in the body, and its scripts and logs in no file of the repository.
- Write the pointer commit's message as `<type>(#<issue>): <description>`.
- Run the target's lint over the staged files before the pointer commit.
- Change nothing else: do not change code, merge, mark a pull request ready or add a label.
