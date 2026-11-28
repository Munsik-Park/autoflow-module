---
name: plan
description: >-
  Choose when an independent score of the design's intent is needed: whether
  each decision is grounded, whether each criterion's verification fits it,
  and whether the scope is right. Takes the feature design, the verification
  design and the applied criteria, in a session other than the design's. Its
  scores and findings are grounds for judging whether the design can be built
  from, and what a re-run of design answers. Does not change anything.
metadata:
  goal: Each item has a score and its ground.
---

## Input

Required:

- The feature design.
- The verification design.
- The applied criteria.

Helpful:

- The criterion decisions.
- The previous evaluation (on a re-score).

## Exit

- End when every item is scored.

## Output

For each item:

- the score;
- its ground.

Findings, each with its severity, `path:line`, weight and the grounds of the weight, and recommendations.

On a re-score, which items were scored afresh and which were inherited.

When the work stops, leave what was done and why it stopped.

## Default

- Score these items: decision grounds, verification fit, scope, security.
- Decision grounds: score whether each decision is grounded in the mechanisms it actually changes, with its constraints and rejected alternatives, and is implementable on the current structure.
- Verification fit: score whether each verification checks the property of its item by a method that can fail when the property does not hold.
- Scope: score whether the scope is neither too broad nor missing a requirement, adds no new mechanism where an extension suffices, and gives a separation reason for a directly related problem it leaves out.
- Score the decision layer. Do not score which files change or which tests run; those are the build's.
- Score each item on a scale of 10: 9–10 excellent, 7–8 good, 5–6 insufficient, 3–4 poor, 1–2 failing.
- Give each finding one weight. A weight says how far a problem must be addressed where the target is actually used. Judge it from what is stated, as the target's maintainers would: a finding can hold and still describe a use the target does not have, while a use it has, by anyone who can reach it, brings the problem about however rarely. What the target requires is what is stated for the property, or else what the change sets out to do and what its use relies on; a criterion nothing states is not a requirement. The change is required to address only its share: what it introduces and, for a problem it makes reachable or worse, keeping itself from bringing it about without fixing the cause, which is left to a separate change. Addressing harm that cannot be undone, such as data lost or exposed, is required within that share however rarely it comes about. The weight is one of:
  - `cannot occur`: the target's process cannot bring the problem about;
  - `need not be addressed`: it can, but the actual use does not, or nothing the target requires asks for it;
  - `must be addressed`: the actual use brings it about and what the target requires asks for it;
  - `not established`: what is stated does not settle the weight.
- Stated means stated by, first to last: the instructions of the call, the criterion decisions, the applied criteria, and the target's own documents and files before the proposed change. Anything else read counts only where it cites one of these. Where two differ, the earlier stands, and the grounds name both.
- Record the weight's grounds: the instructions' passage, a document's section and quoted sentence, or a file and line at a commit; for `not established`, what was looked for and where.
- The weight changes neither severity nor any score.
- Read only; change nothing.
