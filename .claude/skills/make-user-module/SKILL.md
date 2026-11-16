---
name: make-user-module
description: >-
  Make an AutoFlow user module from what the user wants the module to do:
  draft its module definition in the form of docs/module-interface.md, show it
  to the user, check it against the Writing rules, confirm the user module
  location, and write the module's folder there. Use when the user asks to make,
  write or create a user module.
---

# Make a user module

This skill makes one user module: a folder `<location>/<name>/` holding one `SKILL.md`, the module definition, in a user module location. It is a Claude Code project skill of this repository, run from a session opened in a clone of it. It is not a module: it is not among the top-level folders of this repository that hold a `SKILL.md`, so it is not in the list of modules.

Paths below are relative to the repository root, the folder holding `docs/module-interface.md`.

## Rules

- Write nothing in a user module location until the draft meets every rule `check.py` checks, the user has seen the draft and agreed to it, and the user has confirmed the location.
- While a rule is not met, write nothing and tell the user which rule, as `check.py` names it.
- When `name` is the name of a default module, tell the user that the user module will be used in that default module's place, and write only on the user's confirmation.
- Do not replace a folder of the same name already in the location without the user's confirmation. Create `<location>/<name>` so that the creation fails when the folder already exists, and on that failure write nothing.
- In the location, write `<location>/<name>/SKILL.md` and nothing else.
- Change nothing in this repository.

## Steps

1. **Read the interface.** Read `docs/module-interface.md` in full, and follow its Module definition, Writing guidance and Writing rules as written there; do not work from a summary of them. Read two or three default modules' `SKILL.md` (for example `review/SKILL.md` and `analysis/SKILL.md`) for the form a definition is written in, and write the draft in that form.

2. **Learn what the module is to do.** Take what the user wants the module to do from the request. Ask the user for what each item of the interface's Module definition needs and the request does not settle.

3. **Draft the module definition.** Choose `name` with the user. Write the draft as `<draft folder>/<name>/SKILL.md`, where `<draft folder>` is a new temporary folder outside this repository and outside any user module location (for example one made with `mktemp -d`). Write the front matter in the plain form the default modules use, which `check.py` reads, with `name`, `description` and `goal` as text: write `name` on one line; quote a value of these three (`"…"` or `'…'`) that is a null or boolean word (`null`, `true`, `false`, `yes`, `no`, `on`, `off`, in any case) or starts with a digit, `+`, `-`, `.`, `~` or `:`; and start a block scalar's text on the line right after its indicator (`>`, `>-`, `|`, `|-`).

4. **Check the draft.** Run:

   ```
   python3 .claude/skills/make-user-module/check.py <draft folder>/<name>/SKILL.md
   ```

   Exit status 0 means every rule it checks is met; 1 means a rule is not met, and each `rule not met:` line names the rule; 2 is a usage error. A `default module:` line says `name` is the name of a default module.

5. **Show the draft.** Show the user the whole draft and the check's result. Name each rule not met. Revise the draft with the user and check it again (step 4) until it meets every rule and the user agrees to it. If the user changes `name`, move the draft to a folder of the new name.

6. **Default module name.** When the check printed a `default module:` line, tell the user that the user module named `<name>` will be used in place of the default module `<name>` in the list of modules. Continue only on the user's confirmation; otherwise go back to step 5 for another `name`, or stop.

7. **Confirm the location.** Propose `~/.autoflow/modules`, the `modules` folder of the AutoFlow home, as the user module location. The user may name another. Use the location the user confirms, with `~` expanded to the home folder.

8. **Existing folder.** When `<location>/<name>` already exists, show the user what it holds and ask whether to replace it. Replacing removes that folder and everything in it, in step 9 right before the folder is created again. Without the user's confirmation, write nothing; go back to step 5 for another `name`, or stop.

9. **Write.** Create `<location>` if it does not exist. When the user confirmed replacing `<location>/<name>` in step 8, remove it now, right before the next command. Create `<location>/<name>` with a command that fails when it already exists, such as `mkdir "<location>/<name>"` (without `-p`). When that fails, the folder appeared after step 8: write nothing and go back to step 8. Otherwise write `<location>/<name>/SKILL.md` with the draft's content, and nothing else in the location. Run `check.py` on the written `SKILL.md`; it must exit 0.

10. **Finish.** Remove the draft folder. Tell the user the path written, and, when the name is a default module's, that the user module is used in that module's place.

When the user stops at any step, remove the draft folder and leave the location as it was.
