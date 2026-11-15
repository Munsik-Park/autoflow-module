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

## Version

The version of the modules in this repository is in [`VERSION`](VERSION) at the repository root. It is separate from the version of the module interface, which is a date given in that document's [Version](docs/module-interface.md#version) section.
