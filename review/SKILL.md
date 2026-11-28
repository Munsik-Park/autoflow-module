---
name: review
description: >-
  Review one pull request with one or more reviewers and gather their reviews
  into one verdict. Use when a pull request is to be reviewed and the result
  is wanted as a single report: each reviewer is run on the pull request, and
  every finding is checked for whether it holds before it enters the report.
  The report's verdict and findings, each weighed for whether it must be
  addressed, are grounds for the decision on the pull request and what a
  further change to it answers.
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
- each finding once, with its severity and whether it holds, and the grounds when it does not hold or holds in part; for a finding that holds or holds in part, its weight and the grounds of the weight;
- the highest severity among the findings weighed `must be addressed` or `not established`, since only those may still require a change to the pull request.

Beside the report, each reviewer's review as the reviewer wrote it.

When the review stops, the output is what was done and why it stopped.

## Default

- Severity levels, highest first: Critical, High, Medium, Low, Low Confidence. Low Confidence is a suspected issue that could not be confirmed.
- Whether each finding holds is judged before it enters the report. A finding does not hold when its claim does not: it does not reproduce, the source it cites says otherwise, or it misreads a rule. It holds in part when its claim does not hold but the problem behind it is real, and the report then names that problem.
- A finding judged not to hold, or to hold in part, is recorded with the grounds that show it: a command and its output, a file and line at a commit, or a document's section and quoted sentence. Without such grounds the finding holds.
- Give each finding that holds or holds in part one weight; for one that holds in part, the weight is that of the problem the report names. A weight says how far a problem must be addressed where the target is actually used. Judge it from what is stated, as the target's maintainers would: a finding can hold and still describe a use the target does not have, while a use it has, by anyone who can reach it, brings the problem about however rarely. What the target requires is what is stated for the property, or else what the change sets out to do and what its use relies on; a criterion nothing states is not a requirement. The change is required to address only its share: what it introduces and, for a problem it makes reachable or worse, keeping itself from bringing it about without fixing the cause, which is left to a separate change. Addressing harm that cannot be undone, such as data lost or exposed, is required within that share however rarely it comes about. The weight is one of:
  - `cannot occur`: the target's process cannot bring the problem about;
  - `need not be addressed`: it can, but the actual use does not, or nothing the target requires asks for it;
  - `must be addressed`: the actual use brings it about and what the target requires asks for it;
  - `not established`: what is stated does not settle the weight.
- Stated means stated by, first to last: the instructions of the call, the criteria applied, the issue, and the target's own documents and files at the pull request's base commit. Anything else read counts only where it cites one of these. Where two differ, the earlier stands, and the grounds name both.
- Record the weight's grounds: the instructions' passage, a document's section and quoted sentence, or a file and line at a commit; for `not established`, what was looked for and where.
- The weight changes neither a finding's severity nor whether it holds.
