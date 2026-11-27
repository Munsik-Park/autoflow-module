---
name: review
description: >-
  Review one pull request with one or more reviewers and gather their reviews
  into one verdict. Use when a pull request is to be reviewed and the result is
  wanted as a single report: each reviewer is run on the pull request, and
  every finding is checked for whether it holds before it enters the report.
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
- the highest severity among the findings that hold.

Beside the report, each reviewer's review as the reviewer wrote it.

When the review stops, the output is what was done and why it stopped.

## Default

- Severity levels, highest first: Critical, High, Medium, Low, Low Confidence. Low Confidence is a suspected issue that could not be confirmed.
- Whether each finding holds is judged before it enters the report. A finding does not hold when its claim does not: it does not reproduce, the source it cites says otherwise, or it misreads a rule. It holds in part when its claim does not hold but the problem behind it is real, and the report then names that problem.
- A finding judged not to hold, or to hold in part, is recorded with the grounds that show it: a command and its output, a file and line at a commit, or a document's section and quoted sentence. Without such grounds the finding holds.
- Give each finding that holds or holds in part one weight by two questions, since a weight says how far a real problem must be addressed where the target actually runs; for one that holds in part, the weight is that of the problem the report names. First: can its problem occur where the target actually runs? A problem that needs no condition of that environment can; one that needs such a condition can unless a stated environment rules it out. Second: does the level the target requires for the property the finding concerns oblige addressing it? Without a level stated for that property, a problem that needs no such condition takes as its level the criterion it was measured by, which obliges addressing it. The weight is one of:
  - `cannot occur`: a stated environment rules the problem out;
  - `need not be addressed`: it can occur, and the level does not oblige addressing it;
  - `must be addressed`: it can occur, and the level obliges addressing it;
  - `not established`: it needs a condition of the environment, can occur, and no level for that property is stated; treated as must be addressed.
- Stated means stated by, first to last: the instructions of the call, the criteria applied, the issue, and the target's own documents and files at the pull request's base commit. Anything else read counts only where it cites one of these. Where two differ, the earlier stands, and the grounds name both.
- Record the weight's grounds: the instructions' passage, a document's section and quoted sentence, a file and line at a commit, or the criterion; for `not established`, or where no environment was stated, what was looked for and where.
- The weight changes neither severity, nor whether a finding holds, nor the highest severity the report names.
