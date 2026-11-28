---
name: criterion-screen
description: >-
  Checks the issue's acceptance criteria against the code and policy, as the
  part of the criteria review that the rest of it works from; the criteria
  review's result settles whether the problem the issue raises holds and what
  causes it, and whether the criteria could lead the work wrong or short of
  done. Takes the issue. Reviews each criterion: fit with the code and policy,
  cause, actual against expected behavior, contradiction, terms and scope,
  size and separation, testability, unverified estimates. Screens every case
  each criterion applies to: where the behavior shows, the code that decides
  it, and whether it holds. Its review record, and the target file it writes
  for each criterion with cases that need an in-depth look, are what the other
  criteria review modules take: criterion-trace and criterion-reconcile the
  record, criterion-in-depth the target file. The result of the criteria
  review is criterion-reconcile's record. Does not decide how the change will
  be made.
metadata:
  goal: >-
    Each acceptance criterion is reviewed against the code and policy, each
    case it applies to has a verdict with its grounds, every item found has a
    disposition, and each case that needs an in-depth look is handed on.
---

## Input

Required:

- The issue.

Helpful:

- The target's policy documents the criteria touch (decision records, rule documents).

## Exit

- End when every criterion is reviewed and screened.

## Output

The review record:

- what was read (each repository and the commit read, the documents, the materials) and why;
- what was left out and why;
- per criterion, each review item with its finding or that it holds, with its grounds;
- per case:
  - where the behavior shows;
  - the code that decides it (`path:line`);
  - the verdict;
  - how far its grounds reach;
  - whether it is an in-depth target;
- every item found, with its disposition and its grounds: a criterion kept, revised (with its text), split (with the id and text of each criterion it makes), excluded or added (with its text); a problem included or separated;
- each item it could not decide with confidence;
- what it could not confirm, and what it needed.

Per criterion with in-depth cases, a target file holding only:

- the issue body;
- the criterion;
- the cases;
- their code locations;
- the commit read.

When the work stops, leave what was done and why it stopped.

## Default

- Ground each finding: a commit and `path:line` for a fact of the code; a document, its section and a quoted sentence for a policy.
- Never make how the change will be made an item.
- Keep what a criterion requires as behavior a user, a caller or an operator observes.
- Put no verdict or grounds in a target file.
- Change nothing in the target.
