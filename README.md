# autoflow-module

AutoFlow modules written to the [module interface](docs/module-interface.md).

Each module is a folder holding one `SKILL.md`, which defines the module: what it is for, what it needs, the state it works toward, when it stops, what it leaves, and its defaults.

| Module | Goal |
| --- | --- |
| [audit](audit/SKILL.md) | Each test of a required behavior has a test-first judgment, and each security item has a score and its ground. |
| [build](build/SKILL.md) | The design is implemented within its scope on the branch, the tests it was given pass, and each item of the verification design is checked as it says or the reason it is not is recorded. |
| [ci](ci/SKILL.md) | Each pull request has a CI verdict and its ground. |
| [delivery](delivery/SKILL.md) | Each branch of the change is pushed and has a pull request whose body lets the operator decide on it. |
| [quality](quality/SKILL.md) | Each quality item has a score and its ground. |
| [review](review/SKILL.md) | The pull request is reviewed, and its verdict and findings are set out in one report. |
| [test-first](test-first/SKILL.md) | Each item to be checked by test has a test, seen failing on the code without the implementation, shown by its log. |

## Running a module

For now, a module is run by giving a session the path of the module's `SKILL.md` and the inputs its `input` section names. Criteria other than the module's defaults are given in the same instructions.

## Version

The version of the modules in this repository is in [`VERSION`](VERSION) at the repository root. It is separate from the version of the module interface, which is a date given in that document's [Version](docs/module-interface.md#version) section.
