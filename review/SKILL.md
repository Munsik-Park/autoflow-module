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
- the highest severity among the findings weighed `must be addressed` or `not established`, since only those may still require a change to the pull request.

Beside the report, each reviewer's review as the reviewer wrote it.

When the review stops, the output is what was done and why it stopped.

## Default

- Severity levels, highest first: Critical, High, Medium, Low, Low Confidence. Low Confidence is a suspected issue that could not be confirmed.
- Whether each finding holds is judged before it enters the report. A finding does not hold when its claim does not: it does not reproduce, the source it cites says otherwise, or it misreads a rule. It holds in part when its claim does not hold but the problem behind it is real, and the report then names that problem.
- A finding judged not to hold, or to hold in part, is recorded with the grounds that show it: a command and its output, a file and line at a commit, or a document's section and quoted sentence. Without such grounds the finding holds.
- Give each finding that holds or holds in part one weight by two questions, since a weight says how far a real problem must be addressed in the target's actual use; for one that holds in part, the weight is that of the problem the report names. First: can its problem occur in the process the target runs in? Second: does the target's actual use bring the problem about, and does what the target requires oblige addressing it? The actual use is who or what uses the target, how much, on what inputs and at what point of its development, including anyone untrusted who can reach it; an input that comes from outside the target can carry whatever its form allows, and a condition that use meets, however rarely, brings the problem about, while one it does not meet does not. Answer both from what is stated, as the target's maintainers would: a finding can hold and still describe a use the target does not have. What the target requires is what is stated for the property the finding concerns or, where nothing is, what the change sets out to do, what the target's actual use relies on and the rigor the rest of the target keeps; a problem the change neither introduces nor makes reachable or worse is not one the change is required to address, and of a problem it makes reachable or worse, the change addresses what keeps the change from bringing it about and leaves the cause where it is, in code the change does not change, since fixing that cause reaches beyond the change. A criterion the finding was measured by that nothing states says what was checked, not how far the target must meet it. Where the target's actual use can bring about a problem that the change introduces or makes reachable or worse and one occurrence of which would do harm that cannot be undone, such as data lost, secrets or personal data exposed, or access control broken, what the target requires obliges addressing what keeps the change from bringing it about, since that harm does not shrink with how rarely it occurs. The weight is one of:
  - `cannot occur`: the process the target runs in cannot bring the problem about;
  - `need not be addressed`: it can occur, but the target's actual use does not bring it about or what the target requires does not oblige addressing it;
  - `must be addressed`: it can occur, the target's actual use brings it about, and what the target requires obliges addressing it;
  - `not established`: what is stated does not show enough to answer either question.
- Stated means stated by, first to last: the instructions of the call, the criteria applied, the issue, and the target's own documents and files at the pull request's base commit. Anything else read counts only where it cites one of these. Where two differ, the earlier stands, and the grounds name both.
- Record the weight's grounds: the instructions' passage, a document's section and quoted sentence, or a file and line at a commit; for `not established`, what was looked for and where.
- The weight changes neither a finding's severity nor whether it holds.
