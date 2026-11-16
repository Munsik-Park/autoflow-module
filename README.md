# autoflow-module

AutoFlow modules written to the [module interface](docs/module-interface.md).

Each module is a folder holding one `SKILL.md`, which defines the module: what it is for, what it needs, the state it works toward, when it stops, what it leaves, and its defaults.

| Module | Goal |
| --- | --- |
| [analysis](analysis/SKILL.md) | The request is understood well enough to be evaluated: the structure as it stands, the gap, whether a change is owed and whether code is the lever, and the decision points, each conclusion with its grounds. |
| [audit](audit/SKILL.md) | Each test of a required behavior has a test-first judgment, and each security item has a score and its ground. |
| [build](build/SKILL.md) | The design is implemented within its scope on the branch, the tests it was given pass, and each item of the verification design is checked as it says or the reason it is not is recorded. |
| [ci](ci/SKILL.md) | Each pull request has a CI verdict and its ground. |
| [criteria-apply](criteria-apply/SKILL.md) | The applied criteria are the report's criteria with every settled decision applied, in order. |
| [criterion-in-depth](criterion-in-depth/SKILL.md) | Each target case of the criterion has a verdict resting on the code that decides the behavior and the condition applied there. |
| [criterion-reconcile](criterion-reconcile/SKILL.md) | The review record agrees with the trace and the in-depth verdicts, each difference settled in the code, and every item has its disposition. |
| [criterion-screen](criterion-screen/SKILL.md) | Each acceptance criterion is reviewed against the code and policy, each case it applies to has a verdict with its grounds, every item found has a disposition, and each case that needs an in-depth look is handed on. |
| [criterion-trace](criterion-trace/SKILL.md) | For each confirmed cause, how far it reaches beyond the reported points, and for each required behavior, whether a rule or behavior in force keeps it from holding, each with grounds. |
| [delivery](delivery/SKILL.md) | Each branch of the change is pushed and has a pull request whose body lets the operator decide on it. |
| [design](design/SKILL.md) | A design the build can implement and verify: the decisions with their constraints and rejected alternatives, and a verification design that says how each criterion and scope item is verified and what failure each verification catches. |
| [hypothesis](hypothesis/SKILL.md) | Each item has a score and its ground. |
| [plan](plan/SKILL.md) | Each item has a score and its ground. |
| [quality](quality/SKILL.md) | Each quality item has a score and its ground. |
| [review](review/SKILL.md) | The pull request is reviewed, and its verdict and findings are set out in one report. |
| [test-first](test-first/SKILL.md) | Each item to be checked by test has a test, seen failing on the code without the implementation, shown by its log. |

## Running a module

For now, a module is run by giving a session the path of the module's `SKILL.md` and the inputs its `input` section names. Criteria other than the module's defaults are given in the same instructions.

## Making a user module

A user module is a module a user makes and uses in every workspace ([Module locations](docs/module-interface.md#module-locations)). The Claude Code project skill [`make-user-module`](.claude/skills/make-user-module/SKILL.md) makes one.

- Where to run it: in a Claude Code session opened in a clone of this repository, as `/make-user-module`, followed by what the module is to do.
- What it asks: what the module definition needs and the request does not settle; agreement to the drafted module definition, which it shows; the user module location, proposing `~/.autoflow/modules`, the `modules` folder of the AutoFlow home, or another the user names; confirmation when `name` is the name of a default module, since the user module is then used in that module's place; and confirmation before it replaces a folder of the same name already in the location.
- What it checks: before writing, it checks the draft with [`check.py`](.claude/skills/make-user-module/check.py) against the Writing rules that can be checked mechanically, and writes nothing while a rule is not met, saying which rule. `check.py` can also be run alone: `python3 .claude/skills/make-user-module/check.py <folder>/<name>/SKILL.md`.
- Where it writes: `<location>/<name>/SKILL.md`, and nothing else in the location.

The skill is not a module. It is not a top-level folder of this repository holding a `SKILL.md`, so it is not in the list of modules.

## Version

The version of the modules in this repository is in [`VERSION`](VERSION) at the repository root. It is separate from the version of the module interface, which is a date given in that document's [Version](docs/module-interface.md#version) section.
