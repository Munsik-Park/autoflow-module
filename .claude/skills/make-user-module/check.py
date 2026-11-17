#!/usr/bin/env python3
"""Check a draft module definition against the mechanically checkable Writing rules.

Usage: check.py <path to the draft SKILL.md>

The draft is a `SKILL.md` in a folder named for the module.

The front matter is read as the coordinator's module list reads it, and the
Writing rules are checked on the values so read. The module list is
`tools/modules.py` of Munsik-Park/autoflow-coordinator, branch
`module-interface`, at commit 24f8759, and check.py follows it: `scalar`,
`block`, `mapping` and `front_matter` below are that file's functions, and
`values` takes `name`, `metadata.goal` (only when `metadata` is a mapping) and
`description` as its `entry` does. A front matter that file cannot read, where
it lists an error entry, does not meet the front matter rule, and the line gives
that error. How other YAML readers read the front matter is not checked.

Nesting bound: a front matter whose keys nest 32 levels or deeper (the
top-level keys are level 1) does not meet the front matter rule, and is not
read. That file's `mapping` calls itself once per level and stops with
RecursionError when the levels come near Python's recursion limit (1000 by
default), at a depth that depends on the calls around it; the module list
cannot reliably read nesting that deep, so check.py fails well below it. The
levels are counted as `mapping` would descend, up to the line on which it would
stop.

On the values so read, the script checks the Writing rules of
docs/module-interface.md that can be checked mechanically:

- the module is one folder holding one `SKILL.md` file, and the folder's name
  is the same as `name`;
- the front matter holds `name` and `description`, and `goal` under
  `metadata`, each as text that is not empty;
- the body has an `Input` section with content, and `Exit`, `Output` and
  `Default` only as sections with content when present, each headed
  `## Input`, `## Exit`, `## Output`, `## Default` as the default modules head
  them;
- `name`, the whole value, uses only lowercase letters, digits and hyphens,
  does not start or end with a hyphen, has no consecutive hyphens, and is at
  most 64 characters;
- `description` is at most 1024 characters.

Anything else the front matter holds is not checked.

The body is the lines after the line that closes the front matter, as
`front_matter` finds it, or the whole file when there is no front matter.
Blocks are found as CommonMark 0.31.2 finds them: fenced code blocks, indented
code blocks, and HTML blocks of all seven kinds, each from its start condition
to its end condition as the specification states them; one not closed runs to
the end of the body. An indented code block and an HTML block of kind 7 do not
interrupt a paragraph. Block quotes and list items are not read as containers:
every line is read as a line of the document itself.

A line inside one of those blocks is never a heading. Sections are the level-2
headings (`## `) outside them; a level-1 heading also ends a section. A deeper
heading (`###` and below) belongs to the section it is in, whatever its title.
A section has content only when it has a line that is not blank, not a heading,
not a fence marker line and not in an HTML block; a line inside a fenced code
block counts only when the fence is closed, and a line of an indented code block
counts. An empty fenced block, sub-headings alone, an unclosed fence, or HTML
blocks alone (a comment, for example) is no content.

Output: one line per rule not met, starting with `rule not met:`, naming the
rule as the interface words it, followed by what does not meet it. When the
folder's name is the folder name of a default module (with the folder rule met,
it is also `name`), one line starting with `default module:` names that module;
that line is not a rule not met. Default modules are the top-level folders of
the repository holding a `SKILL.md` whose name does not start with `.`, as the
module list scans its default location; the repository root is found from this
script's own location (`<root>/.claude/skills/make-user-module/check.py`). The
line is not printed when the checked file is that default module's own
`SKILL.md`.

Exit status: 0 when every rule is met, 1 when a rule is not met, 2 on a usage
error (wrong arguments, or a path that is not a readable file).

Python 3 standard library only.
"""

import os
import re
import sys
from pathlib import Path

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

NAME_RE = re.compile(r"[a-z0-9-]+")

MAX_DEPTH = 32


def scalar(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
        return v[1:-1]
    return v


def block(lines, i, indent, style):
    """Lines of a block scalar indented deeper than indent, from i. Returns (text, next i)."""
    body = []
    while i < len(lines) and (not lines[i].strip() or len(lines[i]) - len(lines[i].lstrip()) > indent):
        body.append(lines[i].strip())
        i += 1
    while body and not body[-1]:
        body.pop()
    if style[0] == '|':
        text = '\n'.join(body)
    else:
        paras, cur = [], []
        for line in body:
            if line:
                cur.append(line)
            else:
                paras.append(' '.join(cur))
                cur = []
        paras.append(' '.join(cur))
        text = '\n'.join(paras)
    return text, i


def mapping(lines, i, indent):
    """Keys at exactly this indent, from i. Returns (dict, next i)."""
    out = {}
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith('#'):
            i += 1
            continue
        ind = len(line) - len(line.lstrip())
        if ind < indent:
            break
        if ind > indent or ':' not in line:
            raise ValueError(f'line {i + 1}: {line.strip()!r} is not a key')
        key, _, rest = line.strip().partition(':')
        rest = rest.strip()
        i += 1
        if rest in ('>', '>-', '|', '|-'):
            out[key], i = block(lines, i, ind, rest)
        elif rest:
            out[key] = scalar(rest)
        else:
            nxt = next((l for l in lines[i:] if l.strip()), '')
            child = len(nxt) - len(nxt.lstrip())
            if nxt and child > ind:
                out[key], i = mapping(lines, i, child)
            else:
                out[key] = ''
    return out, i


def front_matter(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    if not lines or lines[0].strip() != '---':
        raise ValueError('no front matter')
    try:
        end = next(n for n in range(1, len(lines)) if lines[n].strip() == '---')
    except StopIteration:
        raise ValueError('front matter not closed')
    return mapping(lines[1:end], 0, 0)[0]


def values(fm):
    meta = fm.get('metadata')
    return fm.get('name'), meta.get('goal') if isinstance(meta, dict) else None, fm.get('description')


def depth(text):
    """Levels `mapping` would descend in the front matter of text, the top-level keys being
    level 1, up to the line on which it would stop; 0 when front_matter would find none."""
    lines = text.split('\n')
    if lines[0].strip() != '---':
        return 0
    end = next((n for n in range(1, len(lines)) if lines[n].strip() == '---'), None)
    if end is None:
        return 0
    lines = lines[1:end]
    indents = [0]
    deepest = 1
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith('#'):
            i += 1
            continue
        ind = len(line) - len(line.lstrip())
        while len(indents) > 1 and ind < indents[-1]:
            indents.pop()
        if ind > indents[-1] or ':' not in line:
            break
        rest = line.strip().partition(':')[2].strip()
        i += 1
        if rest in ('>', '>-', '|', '|-'):
            while i < len(lines) and (not lines[i].strip() or len(lines[i]) - len(lines[i].lstrip()) > ind):
                i += 1
        elif not rest:
            nxt = next((l for l in lines[i:] if l.strip()), '')
            child = len(nxt) - len(nxt.lstrip())
            if nxt and child > ind:
                indents.append(child)
                deepest = max(deepest, len(indents))
    return deepest


def body_lines(text):
    """Return the body lines [(lineno, text)]: after the line closing the front matter, as
    `front_matter` finds it, or every line when there is no front matter."""
    lines = text.split("\n")
    numbered = [(n + 1, line) for n, line in enumerate(lines)]
    if lines[0].strip() == "---":
        for n in range(1, len(lines)):
            if lines[n].strip() == "---":
                return numbered[n + 1:]
    return numbered


HEADING_RE = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")
THEMATIC_BREAK_RE = re.compile(r"^ {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$")
SETEXT_UNDERLINE_RE = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")

TAG_NAME = r"[A-Za-z][A-Za-z0-9-]*"
ATTRIBUTE = (
    r"[ \t]+[A-Za-z_:][A-Za-z0-9_.:-]*"
    r"(?:[ \t]*=[ \t]*(?:[^ \t\"'=<>`]+|'[^']*'|\"[^\"]*\"))?"
)
HTML_BLOCK_6_NAMES = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|"
    "colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|"
    "form|frame|frameset|h1|h2|h3|h4|h5|h6|head|header|hr|html|iframe|legend|li|"
    "link|main|menu|menuitem|nav|noframes|ol|optgroup|option|p|param|search|"
    "section|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul"
)
HTML_BLOCK_START = [
    (1, re.compile(r" {0,3}<(?:pre|script|style|textarea)(?:[ \t>]|$)", re.I)),
    (2, re.compile(r" {0,3}<!--")),
    (3, re.compile(r" {0,3}<\?")),
    (4, re.compile(r" {0,3}<![A-Za-z]")),
    (5, re.compile(r" {0,3}<!\[CDATA\[")),
    (6, re.compile(rf" {{0,3}}</?(?:{HTML_BLOCK_6_NAMES})(?:[ \t>]|/>|$)", re.I)),
    (7, re.compile(
        rf" {{0,3}}(?:<(?!(?:pre|script|style|textarea)(?![A-Za-z0-9-])){TAG_NAME}(?:{ATTRIBUTE})*[ \t]*/?>"
        rf"|</{TAG_NAME}[ \t]*>)[ \t]*$",
        re.I,
    )),
]
HTML_BLOCK_END = {
    1: re.compile(r"</(?:pre|script|style|textarea)>", re.I),
    2: re.compile(r"-->"),
    3: re.compile(r"\?>"),
    4: re.compile(r">"),
    5: re.compile(r"\]\]>"),
}


def indentation(line):
    col = 0
    for ch in line:
        if ch == " ":
            col += 1
        elif ch == "\t":
            col += 4 - col % 4
        else:
            break
    return col


def html_block_start(line, paragraph):
    for kind, start in HTML_BLOCK_START:
        if start.match(line) and not (kind == 7 and paragraph):
            return kind
    return None


def check_body(body, problems):
    """Check the body's item sections, on the blocks the module docstring names."""
    found = {}
    current = None
    fence = None
    fence_text = False
    html = None
    indented_code = False
    paragraph = False

    def mark(line):
        if current is not None and line.strip():
            found[current][1] = True

    for lineno, line in body:
        if fence is not None:
            fm = FENCE_CLOSE_RE.match(line)
            if fm and fm.group(1)[0] == fence[0] and len(fm.group(1)) >= len(fence):
                if current is not None and fence_text:
                    found[current][1] = True
                fence = None
            elif line.strip():
                fence_text = True
            continue
        blank = not line.strip(" \t")
        if html is not None:
            if html >= 6:
                if blank:
                    html = None
                    paragraph = False
            elif HTML_BLOCK_END[html].search(line):
                html = None
            continue
        if indented_code:
            if blank or indentation(line) >= 4:
                mark(line)
                continue
            indented_code = False
        if blank:
            paragraph = False
            continue
        if not paragraph and indentation(line) >= 4:
            indented_code = True
            mark(line)
            continue
        fm = FENCE_RE.match(line)
        if fm:
            fence = fm.group(1)
            fence_text = False
            paragraph = False
            continue
        kind = html_block_start(line, paragraph)
        if kind is not None:
            paragraph = False
            if kind >= 6 or not HTML_BLOCK_END[kind].search(line):
                html = kind
            continue
        hm = HEADING_RE.match(line)
        if hm:
            paragraph = False
            level = len(hm.group(1))
            if level > 2:
                continue
            current = None
            title = (hm.group(2) or "").strip()
            word = SECTION_WORDS.get(title.lower())
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
            continue
        paragraph = not (THEMATIC_BREAK_RE.match(line) or (paragraph and SETEXT_UNDERLINE_RE.match(line)))
        mark(line)
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


def show(text):
    """Quote a value for a message, with a character that does not print written as an escape."""
    text = text.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")
    return "'" + "".join(ch if ch.isprintable() else f"\\u{ord(ch):04x}" for ch in text) + "'"


def keys_read(mapping_read):
    return ", ".join(show(k) for k in mapping_read) or "none"


def is_text(key, value, problems, fm):
    """Record under the front matter rule a value of `key` that is not text, or is empty.

    Return True when the value is text that is not empty.
    """
    meta = fm.get("metadata")
    if value is None and key != "metadata.goal":
        msg = f"there is no '{key}' (keys read: {keys_read(fm)})"
    elif value is None and not isinstance(meta, dict):
        msg = "there is no 'metadata.goal': " + (
            "there is no 'metadata'" if meta is None else "'metadata' is a value, not keys"
        )
    elif value is None:
        msg = f"there is no 'goal' under 'metadata' (keys read there: {keys_read(meta)})"
    elif isinstance(value, dict):
        msg = f"'{key}' holds nested keys ({keys_read(value)}), not text"
    elif value == "":
        msg = f"'{key}' is empty"
    else:
        return True
    problems[RULE_FRONT_MATTER].append(msg)
    return False


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

    fm = None
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as exc:
        print(f"usage error: cannot read '{path}': {exc}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        problems[RULE_FRONT_MATTER].append(f"the coordinator's module list cannot read the file: {exc}")
        text = None
    if text is not None:
        levels = depth(text)
        if levels >= MAX_DEPTH:
            problems[RULE_FRONT_MATTER].append(
                f"the front matter nests {levels} levels deep, {MAX_DEPTH} or more: "
                "the coordinator's module list cannot reliably read nesting that deep"
            )
        else:
            try:
                fm = front_matter(path)
            except ValueError as exc:
                where = " (line 1 is the line after the opening '---')" if str(exc).startswith("line ") else ""
                problems[RULE_FRONT_MATTER].append(
                    f"the coordinator's module list cannot read the front matter: {exc}{where}"
                )
        check_body(body_lines(text), problems)

    if fm is not None:
        name, goal, description = values(fm)
        name_ok = is_text("name", name, problems, fm)
        is_text("description", description, problems, fm)
        is_text("metadata.goal", goal, problems, fm)

        if name_ok:
            shown = show(name)
            if not NAME_RE.fullmatch(name):
                problems[RULE_NAME].append(f"{shown} has a character other than a lowercase letter, digit or hyphen")
            if name.startswith("-") or name.endswith("-"):
                problems[RULE_NAME].append(f"{shown} starts or ends with a hyphen")
            if "--" in name:
                problems[RULE_NAME].append(f"{shown} has consecutive hyphens")
            if len(name) > 64:
                problems[RULE_NAME].append(f"'name' is {len(name)} characters")
            if folder.name != name:
                problems[RULE_FOLDER].append(f"the folder is named {show(folder.name)}, and 'name' is {shown}")

        if isinstance(description, str) and len(description) > 1024:
            problems[RULE_DESCRIPTION].append(f"'description' is {len(description)} characters")

    failed = False
    for rule in RULE_ORDER:
        if problems[rule]:
            failed = True
            print(f"rule not met: {rule} -- " + "; ".join(problems[rule]))

    own = default_modules().get(folder.name)
    if own is not None and own != path.resolve():
        print(
            f"default module: '{folder.name}' is the name of the default module '{folder.name}' "
            f"({own}); a user module with this name is used in its place"
        )

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
