---
name: design
description: >-
  Choose after analysis and its evaluation when the change must be designed
  before it is built. Writes a feature design (the architecture decisions, the
  constraints they hold under, the alternatives rejected with grounds, and the
  scope beyond the criteria) and a verification design (for each criterion and
  scope item, how it is verified and what failure that catches, or why it is
  not verified). Re-run with an evaluation, findings or a build that could not
  proceed. Usually before plan and test-first. Does not implement.
metadata:
  goal: "A design the build can implement and verify: the decisions with their constraints and rejected alternatives, and a verification design that says how each criterion and scope item is verified and what failure each verification catches."
---

## Input

Required:

- The acceptance criteria applied.
- The analysis report.

Helpful:

- The hypothesis evaluation.
- The criterion decisions.
- The target's documents.
- On a re-run, the previous designs and, to answer, the plan evaluation, the findings or the build's blocking record.

## Exit

- End when every decision is made and every item has its verification or its reason.
- Stop when a criterion is shown wrong or a point cannot be decided with confidence. Record it.

## Output

The feature design:

- each decision, its constraints, and the alternatives rejected with their grounds;
- the scope: each problem included or separated, with its grounds, and a separation reason for each directly related problem left out;
- each point that could not be decided with confidence.

The verification design:

- for each applied criterion (by its id) and each included scope item, how it is verified and what failure that catches, or why it is not verified;
- for each item verified other than by an executable test, the method and why;
- the feature-design changes that would make an item verifiable.

When the work stops, leave what was done and why it stopped.

## Default

- Keep the feature design at the decision layer: leave file lists, per-test dispositions and oracle conditions to the build.
- Propose a verification only for a behavior a consumer requires whose absence would cost something concrete; otherwise state why its absence costs nothing.
- Make each verification catch a failure that no other verification and no existing mechanism (a test, a lint rule, a schema, a type check, a build check) already catches.
- For an item hard to verify, look for a tool that verifies it directly before settling on a person's observation or a mock.
- Add no interface or indirection to production code only to fit a test.
- Change nothing in the target.
