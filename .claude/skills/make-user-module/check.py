#!/usr/bin/env python3
"""Check a draft module definition against the mechanically checkable Writing rules.

Usage: check.py <path to the draft SKILL.md>

The draft is a `SKILL.md` in a folder named for the module. The script checks
the Writing rules of docs/module-interface.md that can be checked mechanically:

- the module is one folder holding one `SKILL.md` file, and the folder's name
  is the same as `name`;
- the front matter holds `name` and `description`, and `goal` under
  `metadata`;
- the body has an `Input` section with content, and `Exit`, `Output` and
  `Default` only as sections with content when present, each headed
  `## Input`, `## Exit`, `## Output`, `## Default` as the default modules head
  them;
- `name` uses only lowercase letters, digits and hyphens, does not start or
  end with a hyphen, has no consecutive hyphens, and is at most 64 characters;
- `description` is at most 1024 characters.

The front matter is read as the plain YAML the default modules use: `key: value`
lines whose value is a plain scalar or a double-quoted scalar on one line,
folded (`>`, `>-`) and literal (`|`, `|-`) block scalars, and one level of
nested keys under a key with no value. A front matter written in any other form
(single-quoted values, flow collections, comments, anchors, tags, sequences,
deeper nesting, and the like) does not meet the front matter rule.

Output: one line per rule not met, starting with `rule not met:`, naming the
rule as the interface words it, followed by what does not meet it. When `name`
is the name of a default module, one line starting with `default module:`
names that module; that line is not a rule not met. Default modules are the
top-level folders of the repository holding a `SKILL.md` whose name does not
start with `.`; the repository root is found from this script's own location
(`<root>/.claude/skills/make-user-module/check.py`). The line is not printed
when the checked file is that default module's own `SKILL.md`.

Exit status: 0 when every rule is met, 1 when a rule is not met, 2 on a usage
error (wrong arguments, or a path that is not a readable file).

Python 3 standard library only.
"""

import os
import re
import sys
from pathlib import Path

RULE_FORMAT = (
    "A module definition follows the `SKILL.md` format of the Agent Skills "
    "specification."
)
RULE_FOLDER = (
    "A module is one folder holding one `SKILL.md` file. The folder's name is "
    "the same as `name`."
)
RULE_FRONT_MATTER = (
    "The front matter holds `name` and `description`, and `goal` is written "
    "under `metadata` as the `goal` key."
)
RULE_BODY = (
    "The body has `input`, `exit`, `output` and `default` each as a section "
    "with a heading. An optional item that is not written has no section."
)
RULE_NAME = (
    "`name` uses only lowercase letters, digits and hyphens, and is at most 64 "
    "characters. It does not start or end with a hyphen and has no consecutive "
    "hyphens."
)
RULE_DESCRIPTION = "`description` is at most 1024 characters."

RULE_ORDER = [
    RULE_FORMAT,
    RULE_FOLDER,
    RULE_FRONT_MATTER,
    RULE_BODY,
    RULE_NAME,
    RULE_DESCRIPTION,
]

SECTIONS = ["Input", "Exit", "Output", "Default"]
REQUIRED_SECTIONS = {"Input"}
SECTION_WORDS = {
    "input": "Input",
    "inputs": "Input",
    "exit": "Exit",
    "exits": "Exit",
    "output": "Output",
    "outputs": "Output",
    "default": "Default",
    "defaults": "Default",
}

KEY_RE = re.compile(r"^(?P<indent> *)(?P<key>[A-Za-z0-9_][A-Za-z0-9_-]*):(?: (?P<value>.*))?$")
BLOCK_INDICATORS = {">", ">-", "|", "|-"}
PLAIN_FIRST_BAD = set("\"'[]{}&*!|>%@`#,?")
NAME_RE = re.compile(r"^[a-z0-9-]+$")


class FrontMatterError(Exception):
    pass


DQ_ESCAPES = {"\\": "\\", '"': '"', "n": "\n", "t": "\t", "/": "/"}


def double_quoted_value(value, lineno):
    """Return the value of a single-line double-quoted scalar, or raise."""
    out = []
    i = 1
    while i < len(value):
        ch = value[i]
        if ch == "\\":
            esc = value[i + 1:i + 2]
            if esc not in DQ_ESCAPES:
                raise FrontMatterError(f"line {lineno}: escape '\\{esc}' in a double-quoted value")
            out.append(DQ_ESCAPES[esc])
            i += 2
            continue
        if ch == '"':
            if i != len(value) - 1:
                raise FrontMatterError(f"line {lineno}: text after the closing quote")
            return "".join(out)
        out.append(ch)
        i += 1
    raise FrontMatterError(f"line {lineno}: double-quoted value not closed on its line")


def plain_value(text, lineno):
    """Return the value of a plain or double-quoted scalar, or raise."""
    value = text.strip()
    if not value:
        return ""
    if value[0] == '"':
        return double_quoted_value(value, lineno)
    if value[0] in PLAIN_FIRST_BAD:
        raise FrontMatterError(f"line {lineno}: value starts with '{value[0]}'")
    if value.startswith("- ") or value == "-":
        raise FrontMatterError(f"line {lineno}: value is a sequence entry")
    if ": " in value or value.endswith(":"):
        raise FrontMatterError(f"line {lineno}: value holds ': '")
    if " #" in value:
        raise FrontMatterError(f"line {lineno}: value holds ' #'")
    return value


def read_block(lines, start, parent_indent, style):
    """Read a block scalar's content lines; return (value, next index)."""
    content = []
    indent = None
    i = start
    while i < len(lines):
        lineno, line = lines[i]
        if line.strip() == "":
            content.append("")
            i += 1
            continue
        cur = len(line) - len(line.lstrip(" "))
        if line[cur:cur + 1] == "\t":
            raise FrontMatterError(f"line {lineno}: tab in indentation")
        if cur <= parent_indent:
            break
        if indent is None:
            indent = cur
        elif cur < indent:
            raise FrontMatterError(f"line {lineno}: block line less indented than the block")
        content.append(line[indent:])
        i += 1
    # Trailing blank lines belong to no value under the chomping used here.
    while content and content[-1] == "":
        content.pop()
    if not content:
        raise FrontMatterError(f"line {lines[start - 1][0]}: empty block scalar")
    if style.startswith("|"):
        value = "\n".join(content)
    else:
        value = content[0]
        for prev, cur in zip(content, content[1:]):
            if cur == "":
                value += "\n"
            elif prev == "":
                value += cur
            elif cur.startswith(" ") or prev.startswith(" "):
                value += "\n" + cur
            else:
                value += " " + cur
    if not style.endswith("-"):
        value += "\n"
    return value, i


def parse_front_matter(lines):
    """Parse front matter lines [(lineno, text)] into a dict of str or dict."""
    data = {}
    i = 0
    while i < len(lines):
        lineno, line = lines[i]
        if line.strip() == "":
            i += 1
            continue
        m = KEY_RE.match(line)
        if not m or m.group("indent"):
            raise FrontMatterError(f"line {lineno}: not a plain 'key: value' line")
        key = m.group("key")
        if key in data:
            raise FrontMatterError(f"line {lineno}: key '{key}' repeated")
        raw = m.group("value")
        i += 1
        if raw is not None and raw.strip() in BLOCK_INDICATORS:
            data[key], i = read_block(lines, i, 0, raw.strip())
        elif raw is not None and raw.strip() != "":
            data[key] = plain_value(raw, lineno)
        else:
            nested = {}
            nest_indent = None
            while i < len(lines):
                nlineno, nline = lines[i]
                if nline.strip() == "":
                    i += 1
                    continue
                cur = len(nline) - len(nline.lstrip(" "))
                if cur == 0:
                    break
                nm = KEY_RE.match(nline)
                if not nm:
                    raise FrontMatterError(f"line {nlineno}: not a plain 'key: value' line")
                if nest_indent is None:
                    nest_indent = cur
                elif cur != nest_indent:
                    raise FrontMatterError(f"line {nlineno}: nested key not at the indentation of the others")
                nkey = nm.group("key")
                if nkey in nested:
                    raise FrontMatterError(f"line {nlineno}: key '{key}.{nkey}' repeated")
                nraw = nm.group("value")
                i += 1
                if nraw is not None and nraw.strip() in BLOCK_INDICATORS:
                    nested[nkey], i = read_block(lines, i, nest_indent, nraw.strip())
                elif nraw is not None and nraw.strip() != "":
                    nested[nkey] = plain_value(nraw, nlineno)
                else:
                    raise FrontMatterError(f"line {nlineno}: key '{key}.{nkey}' has no value (only one level of nesting)")
            if nest_indent is None:
                data[key] = ""
            else:
                data[key] = nested
    return data


def split_front_matter(text):
    """Return (front matter lines, body lines with numbers), or raise."""
    lines = text.split("\n")
    if not lines or lines[0].rstrip() != "---":
        raise FrontMatterError("the file does not start with a '---' front matter line")
    for idx in range(1, len(lines)):
        if lines[idx].rstrip() == "---":
            fm = [(n + 1, lines[n]) for n in range(1, idx)]
            body = [(n + 1, lines[n]) for n in range(idx + 1, len(lines))]
            return fm, body
    raise FrontMatterError("the front matter has no closing '---' line")


HEADING_RE = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def check_body(body, problems):
    """Check the body's item sections."""
    found = {}
    current = None
    fence = None
    for lineno, line in body:
        fm = FENCE_RE.match(line)
        if fence is not None:
            if fm and fm.group(1)[0] == fence[0] and len(fm.group(1)) >= len(fence):
                fence = None
            if current is not None:
                found[current][1] = True
            continue
        if fm:
            fence = fm.group(1)
            if current is not None:
                found[current][1] = True
            continue
        hm = HEADING_RE.match(line)
        if hm:
            level = len(hm.group(1))
            title = (hm.group(2) or "").strip()
            word = SECTION_WORDS.get(title.lower())
            if level <= 2:
                current = None
            if word is not None:
                if level == 2 and title == word and line.rstrip() == f"## {word}":
                    if word in found:
                        problems[RULE_BODY].append(f"line {lineno}: second '## {word}' section")
                    else:
                        found[word] = [lineno, False]
                        current = word
                else:
                    problems[RULE_BODY].append(
                        f"line {lineno}: '{line.strip()}' is not headed '## {word}'"
                    )
            elif current is not None and level > 2:
                found[current][1] = True
            continue
        if current is not None and line.strip():
            found[current][1] = True
    for word in SECTIONS:
        if word in found:
            if not found[word][1]:
                problems[RULE_BODY].append(f"line {found[word][0]}: '## {word}' section has no content")
        elif word in REQUIRED_SECTIONS:
            problems[RULE_BODY].append(f"no '## {word}' section")


def default_modules():
    root = Path(__file__).resolve().parent.parent.parent.parent
    modules = {}
    try:
        entries = sorted(os.listdir(root))
    except OSError:
        return modules
    for entry in entries:
        if entry.startswith("."):
            continue
        skill = root / entry / "SKILL.md"
        if skill.is_file():
            modules[entry] = skill.resolve()
    return modules


def main(argv):
    if len(argv) == 2 and argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    if len(argv) != 2:
        print("usage: check.py <path to the draft SKILL.md>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"usage error: '{path}' is not a file", file=sys.stderr)
        return 2
    try:
        raw = path.read_bytes()
    except OSError as exc:
        print(f"usage error: cannot read '{path}': {exc}", file=sys.stderr)
        return 2

    problems = {rule: [] for rule in RULE_ORDER}

    folder = path.resolve().parent
    if path.name != "SKILL.md":
        problems[RULE_FOLDER].append(f"the file is named '{path.name}', not 'SKILL.md'")
    try:
        same = [e for e in os.listdir(folder) if e.lower() == "skill.md"]
    except OSError:
        same = []
    if len(same) > 1:
        problems[RULE_FOLDER].append(
            "the folder holds more than one SKILL.md file: " + ", ".join(sorted(same))
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        problems[RULE_FORMAT].append("the file is not UTF-8 text")
        text = None

    data = None
    if text is not None:
        text = text.replace("\r\n", "\n")
        try:
            fm_lines, body = split_front_matter(text)
        except FrontMatterError as exc:
            problems[RULE_FRONT_MATTER].append(str(exc))
            fm_lines, body = None, [(n + 1, l) for n, l in enumerate(text.split("\n"))]
        if fm_lines is not None:
            try:
                data = parse_front_matter(fm_lines)
            except FrontMatterError as exc:
                problems[RULE_FRONT_MATTER].append(
                    "the front matter is not in the plain form the default modules use: " + str(exc)
                )
        check_body(body, problems)

    name = None
    if data is not None:
        for key in ("name", "description"):
            value = data.get(key)
            if value is None or value == "":
                problems[RULE_FRONT_MATTER].append(f"no '{key}'")
            elif not isinstance(value, str):
                problems[RULE_FRONT_MATTER].append(f"'{key}' is not a single value")
        meta = data.get("metadata")
        if not isinstance(meta, dict):
            problems[RULE_FRONT_MATTER].append("no 'metadata' holding 'goal'")
        elif not isinstance(meta.get("goal"), str) or meta.get("goal") == "":
            problems[RULE_FRONT_MATTER].append("no 'goal' under 'metadata'")

        if isinstance(data.get("name"), str) and data["name"]:
            name = data["name"]
            if not NAME_RE.match(name):
                problems[RULE_NAME].append(f"'{name}' has a character other than a lowercase letter, digit or hyphen")
            if name.startswith("-") or name.endswith("-"):
                problems[RULE_NAME].append(f"'{name}' starts or ends with a hyphen")
            if "--" in name:
                problems[RULE_NAME].append(f"'{name}' has consecutive hyphens")
            if len(name) > 64:
                problems[RULE_NAME].append(f"'name' is {len(name)} characters")
            if folder.name != name:
                problems[RULE_FOLDER].append(f"the folder is named '{folder.name}', and 'name' is '{name}'")

        desc = data.get("description")
        if isinstance(desc, str) and len(desc) > 1024:
            problems[RULE_DESCRIPTION].append(f"'description' is {len(desc)} characters")

    failed = False
    for rule in RULE_ORDER:
        if problems[rule]:
            failed = True
            print(f"rule not met: {rule} -- " + "; ".join(problems[rule]))

    if name is not None:
        modules = default_modules()
        own = modules.get(name)
        if own is not None and own != path.resolve():
            print(
                f"default module: '{name}' is the name of the default module '{name}' "
                f"({own}); a user module with this name is used in its place"
            )

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
