# AutoFlow Module Interface

Version: 2026-11-09 (Draft)

This document sets the form in which an AutoFlow module describes its work.

## Contents

1. Overview
2. Terms
3. Flow
4. Module definition
5. Writing guidance
6. Writing rules
7. Example
8. Module locations
9. Version
10. Appendix: stages and reference compositions
11. Open questions

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

The coordination session reads `description` to choose the module that fits the issue and the situation, prepares what `input` names from the results gathered so far, and calls the module by `name`. The work session works toward `goal`, and when it reaches `exit` it leaves `output` and ends. For the behavior and judgment criteria it needs during the work, it follows those the coordination session gave, and `default` when it was given none. The coordination session looks at `output`, judges whether the goal was reached, and decides what comes next.

## Module definition

Each item is described in terms of the work, fully enough to do the work.

### Required items

- **name**

  The name by which the module is called.

- **description**

  The situations in which this module is chosen. It states the situations it applies to and the way it works that set it apart from other modules doing the same work.

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

  The behavior and judgment criteria applied when none are given. When the coordination session gives other criteria in calling the module, the module follows those.

## Writing guidance

Write so that a work session can work correctly from the module definition alone, and so that the definition stays easy to change later.

- Write about the work in general. When it records what happened in one situation, the work session reads that as an instruction for every case.
- Make the module definition complete on its own. When it and other documents point to each other, a change to one tangles the others.
- Keep it light. The items are the seven above; anything else belongs in the workspace.

## Writing rules

A module definition follows the `SKILL.md` format of the Agent Skills specification.

- A module is one folder holding one `SKILL.md` file. The folder's name is the same as `name`.
- The front matter holds `name` and `description`, and `goal` is written under `metadata` as the `goal` key.
- The body has `input`, `exit`, `output` and `default` each as a section with a heading. An optional item that is not written has no section.
- `name` uses only lowercase letters, digits and hyphens, and is at most 64 characters. It does not start or end with a hyphen and has no consecutive hyphens.
- `description` is at most 1024 characters.
- A default module and a user module do not share a name.

## Example

The review module filled in with this form:

- name: review
- description: When a pull request of a single repository is checked by several reviewers and the results are gathered into one verdict
- input: required is the pull request to review. What helps is the result of an earlier review, and the issue and the criteria applied to it
- goal: The pull request review is done, and its verdict and findings are set out
- exit: The goal is reached when every reviewer's check is gathered in the report. It stops when a reviewer cannot be run.
- output: The review report (verdict, findings with their severity, the commit reviewed). When it stops, what was done and why it stopped
- default: none

## Module locations

Module definitions are kept in two places.

- Default modules: modules distributed with the AutoFlow plugin.
- User modules: modules a user makes and uses in every workspace.

The coordination session scans both places to build the list of modules. In building the list it reads only the `name`, `goal` and `description` of each module definition, and reads the whole definition only of the module it chooses.

## Version

The version of this document is shown as a date (YYYY-MM-DD). The date is moved only by a change after which existing module definitions no longer fit as they are; other changes are kept in the repository's history.

## Appendix: stages and reference compositions

### Stages

The work AutoFlow handles is divided into stages. A module does the work of one stage, and a workflow is made by choosing the stages an issue needs.

| Stage | What it adds | Current modules |
| --- | --- | --- |
| Criteria review | Whether the issue's acceptance criteria hold against the code and policies, where they apply, and which cases to look at in depth | criterion-screen, criterion-trace, criterion-in-depth, criterion-reconcile |
| Analysis | The current structure, its gap from the request, whether a change is needed and whether code is the means, decision points, and the criteria to apply to the work | analysis, criteria-apply |
| Design | Structural decisions and their constraints, alternatives set aside, and how each criterion will be verified | design |
| Implementation | Changes on a branch and their verification record, and the range of commits changed | build |
| Evaluation | An independent score of an earlier stage's result, with its grounds and recommendations | hypothesis (analysis), plan (design), audit (tests-first and security of the implementation), quality (completeness) |
| Delivery | A pull request for the operator to look at and judge, the results and evidence for each criterion, and what could not be verified | delivery |
| CI | The CI verdict on the pull request head, and its grounds | ci |
| Review | A report gathering the reviewers' checks into one | review |

An evaluation stage follows another stage and adds grounds for judging its result.

### Reference compositions

Combinations that are often used. Use them as starting points, adding or removing stages to fit the issue.

| Composition | Stages | When used |
| --- | --- | --- |
| Full | Criteria review, analysis, design, implementation, delivery, CI, review; evaluation after analysis, design and implementation | When an issue is solved with AutoFlow from the start to a pull request |
| Analysis and review | Analysis (criteria review first when the criteria are unclear), implementation and pull request outside AutoFlow, review | When finding the cause and the review are done with AutoFlow and the implementation outside it |
| Review only | Work and pull request outside AutoFlow, review | When reviewing a change made outside AutoFlow, or an existing pull request |

## Open questions

None.
