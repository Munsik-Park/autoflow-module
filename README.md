# autoflow-module

AutoFlow modules written to the [module interface](docs/module-interface.md).

Each module is a folder holding one `SKILL.md`, which defines the module: what it is for, what it needs, the state it works toward, when it stops, what it leaves, and its defaults.

| Module | Goal |
| --- | --- |
| [review](review/SKILL.md) | The pull request is reviewed, and its verdict and findings are set out in one report. |

## Running a module

For now, a module is run by giving a session the path of the module's `SKILL.md` and the inputs its `input` section names. Criteria other than the module's defaults are given in the same instructions.
