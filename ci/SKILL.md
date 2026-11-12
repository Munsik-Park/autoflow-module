---
name: ci
description: >-
  Choose when a pull request is open and the CI result on its head commit is
  needed as one verdict. Reads the checks published on GitHub and judges green,
  failing or timed out. When the target's CI does not run for the pull request
  at all (no workflow, or excluded by a trigger, path or condition), records
  not-run with its ground, kept apart from a failure or a delay. Given the test
  files the change added, confirms the CI job that actually ran each one.
  Records the verdict in the pull request body; does not re-run CI or change
  code. Usually used after delivery and before review.
metadata:
  goal: Each pull request has a CI verdict and its ground.
---

## Input

Required:

- The pull requests.

Helpful:

- The test files the change added.
- The checks the build left to CI.

## Exit

- End when every pull request has a verdict.
- When a pull request cannot be read, record it as not judged and go on with the others.

## Output

For each pull request:

- the verdict: green, not-run, failing, timed out or conflicting;
- its ground, including the commit judged.

For each added test file, the CI job that ran it.

When the work stops, leave what was done and why it stopped.

## Default

- Do not judge a pull request with no checks as green.
- Wait at most 15 minutes.
- Record the verdict and its ground in the CI section of the pull request body.
- Change nothing else: do not re-run CI, push or merge.
