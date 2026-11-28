# AutoFlow Module Interface

Version: 2026-11-09 (Draft)

This document sets the form in which an AutoFlow module describes its work.

## Contents

1. Overview
2. Terms
3. Flow
4. Work locations
5. Module definition
6. Writing guidance
7. Writing rules
8. Example
9. Module locations
10. Version
11. Appendix: stages and reference compositions
12. Open questions

## Overview

A module takes on one piece of the work AutoFlow handles. When every module describes its work in the same form, a work session works from that description, and the coordination session reads the descriptions to choose modules. This makes it possible to build and use together several modules that do the same work in ways suited to different situations, modules that are inserted in the middle of a flow, and modules that carry a particular method.

## Terms

- Module: a unit that takes on one piece of work. It is defined in the form of this document.
- Module definition: one module described in the form of this document.
- Coordination session: the session that takes an issue, chooses modules, prepares their inputs and calls them, and receives the results to decide what comes next.
- Work session: a session that carries out one module.
- Workspace: the place, one per repository, that holds the information the coordination session refers to.
- Stage: a division of the work AutoFlow handles.
- Workflow: the modules chosen for one issue, and how they are connected.

## Flow

The coordination session reads `description` to choose the module that fits the issue and the situation, prepares what `input` names from the results gathered so far, and calls the module by `name`. The work session works toward `goal`, and when it reaches `exit` it leaves `output` and ends. For the behavior and judgment criteria it needs during the work, it first finds what sets them and follows it, and uses `default` where it finds nothing. The coordination session looks at `output`, judges whether the goal was reached, and decides what comes next.

## Work locations

- The coordination session gives each module run a work folder with the call. Every file in it is the module run's: everything `output` names, and the work session's own working files.
- Inputs are given as values or paths. The work session reads them where they are.
- A module that changes the target repository leaves the change as commits in the checkout it works in.

## Module definition

Each item is described in terms of the work, fully enough to do the work.

### Required items

- **name**

  The name by which the module is called.

- **description**

  The module's role. It states the work the module does and the way it works that set it apart from other modules doing the same work, what it takes, and, where its result serves other work, how that result can be used. From these the coordination session works out how the modules relate; which module runs next is its decision, so a description places the module in no order of modules.

- **goal**

  The state that must hold when the module has finished its work. Work done in different ways has the same goal when it is the same work.

- **input**

  What the module needs to reach its goal. It separates what is required from what helps.

### Optional items

- **exit**

  The condition on which the work stops. It states what, once met, stops the work.

- **output**

  What the module leaves when it finishes its work, including what it leaves when it stops without reaching its goal.

- **default**

  The behavior and judgment criteria applied where nothing else sets them.

## Writing guidance

Write so that the definition's readers act on it correctly, the coordination session in choosing the module and the work session in doing the work, and so that the definition can be changed on its own.

- Write about the work in general. When it records what happened in one situation, the work session reads that as an instruction for every case.
- Make the module definition complete on its own. When it and other documents point to each other, a change to one tangles the others.
- Give an instruction its reason when `goal` and `description` do not show it. Write the reason itself with the instruction, not a pointer to where it is recorded. A work session that knows why an instruction is given can follow its intent in a case the instruction does not name.
- When an instruction turns out to be misread, or open to a misreading, rewrite the instruction and its reason so that the intended reading follows from them. Do not add a sentence that rules the misreading out; such a sentence answers that one case alone.
- Keep it light. The items are the seven above; anything else belongs in the workspace. Within an item, keep a sentence only when it changes what its reader does, the coordination session choosing a module or the work session doing the work; each sentence adds to what is read. Remove a sentence only when it is plain that removing it changes nothing: one that seems to repeat another may still change how an instruction is read.

## Writing rules

A module definition follows the `SKILL.md` format of the Agent Skills specification.

- A module is one folder holding one `SKILL.md` file. The folder's name is the same as `name`.
- The front matter holds `name` and `description`, and `goal` is written under `metadata` as the `goal` key.
- The body has `input`, `exit`, `output` and `default` each as a section with a heading. An optional item that is not written has no section.
- `name` uses only lowercase letters, digits and hyphens, and is at most 64 characters. It does not start or end with a hyphen and has no consecutive hyphens.
- `description` is at most 1024 characters.
- A user module with the `name` of a default module is used in its place.

## Example

The review module filled in with this form:

- name: review
- description: Checks a pull request of a single repository with several reviewers and gathers the results into one verdict. Takes the pull request. The verdict and findings are grounds for the decision on the pull request
- input: required is the pull request to review. What helps is the result of an earlier review, and the issue and the criteria applied to it
- goal: The pull request review is done, and its verdict and findings are set out
- exit: The goal is reached when every reviewer's check is gathered in the report. It stops when a reviewer cannot be run.
- output: The review report (verdict, findings with their severity, the commit reviewed). When it stops, what was done and why it stopped
- default: none

## Module locations

Module definitions are kept in two places.

- Default modules: modules distributed with the AutoFlow plugin.
- User modules: modules a user makes and uses in every workspace.

The coordination session scans both places to build the list of modules. When a user module has the `name` of a default module, the list holds the user module in its place. In building the list it reads only the `name`, `goal` and `description` of each module definition, and reads the whole definition only of the module it chooses.

## Version

The version of this document is shown as a date (YYYY-MM-DD). The date is moved only by a change after which existing module definitions no longer fit as they are; other changes are kept in the repository's history.

## Appendix: stages and reference compositions

### Stages

The work AutoFlow handles is divided into stages. A module does the work of one stage, and a workflow is made by choosing the stages an issue needs.

| Stage | What it adds | Current modules |
| --- | --- | --- |
| Criteria review | Whether the problem the issue raises holds and what causes it, whether the issue's acceptance criteria hold against the code and policies, where they apply, and which cases to look at in depth | criterion-screen, criterion-trace, criterion-in-depth, criterion-reconcile |
| Criterion decision | A decision on each point the criteria review raised about an acceptance criterion's content (the criterion kept, revised, split, excluded or added), with the text it decides and its grounds | criterion-decision |
| Analysis | How to resolve the problem as the criteria review or the issue's criteria set it: the current structure, the gap to close, whether a change is needed and whether code is the means, the approaches, decision points, and the criteria to apply to the work | analysis, criteria-apply |
| Design | Structural decisions and their constraints, alternatives set aside, and how each criterion will be verified | design |
| Implementation | Changes on a branch and their verification record, and the range of commits changed | test-first, build |
| Evaluation | An independent score of another stage's result, with its grounds and recommendations | hypothesis (analysis), plan (design), audit (tests-first and security of the implementation), quality (completeness) |
| Delivery | A pull request for the operator to look at and judge, the results and evidence for each criterion, and what could not be verified | delivery |
| CI | The CI verdict on the pull request head, and its grounds | ci |
| Review | A report gathering the reviewers' checks into one | review |

An evaluation stage takes another stage's result and adds grounds for judging it.

A criterion decision stage takes the points a criteria review raises by disposing of a criterion with a change to its content or by leaving an item undecided, and the stages that work by the criteria take its decisions.

### Reference compositions

Combinations that are often used. Use them as starting points, adding or removing stages to fit the issue.

| Composition | Stages | When used |
| --- | --- | --- |
| Full | Criteria review, analysis, design, implementation, delivery, CI, review; evaluation of analysis, design and implementation | When an issue is solved with AutoFlow from the start to a pull request |
| Analysis and review | Criteria review, analysis, implementation and pull request outside AutoFlow, review | When settling the problem, finding how to resolve it and the review are done with AutoFlow and the implementation outside it |
| Review only | Work and pull request outside AutoFlow, review | When reviewing a change made outside AutoFlow, or an existing pull request |

## Open questions

None.
