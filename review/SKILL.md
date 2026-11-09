---
name: review
description: >-
  Review one pull request with one or more reviewers and gather their reviews
  into one verdict. Use when a pull request is to be reviewed and the result is
  wanted as a single report: each reviewer is run on the pull request, and
  every finding is weighed before it enters the report.
metadata:
  goal: The pull request is reviewed, and its verdict and findings are set out in one report.
---

## Input

Required:

- The pull request to review: its repository and number.

Helpful:

- The report of an earlier review of the same pull request.
- The issue the pull request answers, and the criteria applied to it.

## Exit

- The review ends when every reviewer's review is in the report.
- It stops when a reviewer cannot be run or the pull request cannot be read.

## Output

A report that names:

- the pull request and the head commit that was reviewed;
- each finding once, with the reviewers that raised it, its severity, and whether it holds, and the grounds when it does not hold or holds in part;
- the highest severity among the findings that hold.

Beside the report, each reviewer's review as the reviewer wrote it.

When the review stops, the output is what was done and why it stopped.

## Default

- Severity levels, highest first: Critical, High, Medium, Low, Low Confidence. Low Confidence is a suspected issue that could not be confirmed.
- Each finding is weighed before it enters the report. A finding does not hold when its claim does not: it does not reproduce, the source it cites says otherwise, or it misreads a rule. It holds in part when its claim does not hold but the problem behind it is real, and the report then names that problem.
- A finding judged not to hold, or to hold in part, is recorded with the grounds that show it: a command and its output, a file and line at a commit, or a document's section and quoted sentence. Without such grounds the finding holds.
