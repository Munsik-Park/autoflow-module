---
name: plan
description: >-
  Choose after design when an independent score of the design's intent is
  needed: whether each decision is grounded, whether each criterion's
  verification fits it, and whether the scope is right. Runs in a session
  other than the design's. Does not change anything.
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
- Give each finding one weight by two questions. First: can its problem occur in the process the target runs in? Second: does the target's actual use bring the problem about, and does what the target requires oblige addressing it? The actual use is who or what uses the target, how much, on what inputs and at what point of its development, including anyone untrusted who can reach it; an input that comes from outside the target can carry whatever its form allows, and a condition that use meets, however rarely, brings the problem about, while one it does not meet does not. Answer both from what is stated, as the target's maintainers would: a finding can hold and still describe a use the target does not have. What the target requires is what is stated for the property the finding concerns or, where nothing is, what the change sets out to do, what the target's actual use relies on and the rigor the rest of the target keeps; a problem the change neither introduces nor makes reachable or worse is not one the change is required to address, and of a problem it makes reachable or worse, the change addresses what keeps the change from bringing it about and leaves the cause where it is, in code the change does not change, since fixing that cause reaches beyond the change. A criterion the finding was measured by that nothing states says what was checked, not how far the target must meet it. Where the target's actual use can bring about a problem that the change introduces or makes reachable or worse and one occurrence of which would do harm that cannot be undone, such as data lost, secrets or personal data exposed, or access control broken, what the target requires obliges addressing what keeps the change from bringing it about, since that harm does not shrink with how rarely it occurs. The weight is one of:
  - `cannot occur`: the process the target runs in cannot bring the problem about;
  - `need not be addressed`: it can occur, but the target's actual use does not bring it about or what the target requires does not oblige addressing it;
  - `must be addressed`: it can occur, the target's actual use brings it about, and what the target requires obliges addressing it;
  - `not established`: what is stated does not show enough to answer either question.
- Stated means stated by, first to last: the instructions of the call, the criterion decisions, the applied criteria, and the target's own documents and files before the proposed change. Anything else read counts only where it cites one of these. Where two differ, the earlier stands, and the grounds name both.
- Record the weight's grounds: the instructions' passage, a document's section and quoted sentence, or a file and line at a commit; for `not established`, what was looked for and where.
- The weight changes neither severity nor any score.
- Read only; change nothing.
