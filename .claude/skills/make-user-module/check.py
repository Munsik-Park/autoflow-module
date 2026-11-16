#!/usr/bin/env python3
"""Check a draft module definition against the mechanically checkable Writing rules.

Usage: check.py <path to the draft SKILL.md>

The draft is a `SKILL.md` in a folder named for the module. The script checks
the Writing rules of docs/module-interface.md that can be checked mechanically:

- the module is one folder holding one `SKILL.md` file, and the folder's name
  is the same as `name`;
- the front matter holds `name` and `description`, and `goal` under
  `metadata`, in the layout below;
- the body has an `Input` section with content, and `Exit`, `Output` and
  `Default` only as sections with content when present, each headed
  `## Input`, `## Exit`, `## Output`, `## Default` as the default modules head
  them;
- `name` uses only lowercase letters, digits and hyphens, does not start or
  end with a hyphen, has no consecutive hyphens, and is at most 64 characters;
- `description` is at most 1024 characters.

The front matter is accepted only in the layout the default modules use. Any
other front matter does not meet the front matter rule, and the line says what
to change and the layout to use.

- The file's first line is `---`, and the front matter ends at the next line
  that is `---`. Between them are these lines and no others, in this order:

      name: <value>
      description: <value>
      metadata:
        goal: <value>

  Every key but `goal` is at the start of its line; `goal` is indented two
  spaces. There is no other key, no repeated key, no blank line and no comment
  line, and no line ends with a space.
- `key: <value>` has one space after the colon and the value on the rest of
  the line, plain, double-quoted or single-quoted. `name` is always written
  on one line so.
- `description` may instead be a block scalar, `description: >`, `>-`, `|`
  or `|-`, and `goal` one written `goal: >-` or `goal: |-`: the line is
  followed by the text on lines each indented exactly two spaces more than the
  key and not blank, up to the next key or the closing `---`. With `|` the
  lines are joined with a line break, with `>` with a space; with `-` the text
  has no final line break, without it one.
- Characters. In the front matter, including its two `---` lines, the only
  whitespace is space and the line end (LF; a CRLF line end is read as LF). A
  tab, any other character that Python reports as whitespace, a control
  character (Unicode category Cc) other than LF, a format (Cf), line separator
  (Zl) or paragraph separator (Zp) character, a space separator (Zs) other than
  space, and U+FFFE and U+FFFF do not meet the front matter rule wherever they
  are; the line names each one's code point and line.
- A plain value starts with a letter (a character whose Unicode category
  starts with L), is not a YAML 1.1 null or boolean word (`null`, `y`, `n`,
  `yes`, `no`, `true`, `false`, `on`, `off`, in any case), holds no `: ` and
  no ` #`, and does not end with `:`. Any other one-line value must be quoted.
  Every plain null, boolean, number, date, timestamp, merge key (`<<`) and
  value key (`=`) of YAML 1.1 and of the YAML 1.2 core schema, and every plain
  symbol (`:x`) of Ruby's YAML reader, either starts with a character that is
  not a letter or is one of these words.
- A double-quoted value is on one line and has only the escapes `\\\\`, `\\"`,
  `\\n` and `\\t`, which YAML 1.1 and YAML 1.2 both read. A single-quoted value
  is on one line, and `''` in it stands for `'`. Nothing follows the closing
  quote. A value is not empty.

Sections are the level-2 headings (`## `) outside fenced code blocks; a level-1
heading also ends a section. A deeper heading (`###` and below) belongs to the
section it is in, whatever its title. A section has content only when it has a
line that is not blank, not a heading and not a fence marker line; a line inside
a fenced code block counts only when the fence is closed. An empty fenced block,
sub-headings alone, or an unclosed fence is no content.

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
import unicodedata
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

LAYOUT = (
    "write the front matter as the lines 'name: <value>', 'description: <value>', "
    "'metadata:' and '  goal: <value>' (indented two spaces), in this order and "
    "with no other line; 'description' may instead be written 'description: >-' "
    "('>', '>-', '|' or '|-') and 'goal' '  goal: >-' ('>-' or '|-'), followed by "
    "the text on lines indented two spaces more than the key"
)
LAYOUT_KEYS = [("name", 0), ("description", 0), ("metadata", 0), ("goal", 2)]
KEY_LINE_RE = re.compile(r"(?P<indent> *)(?P<key>[^ :#][^:]*):(?: |$)")
BLOCK_INDICATORS = {">", ">-", "|", "|-"}
# `goal` ends the front matter. Its final line break under `>` or `|` is read by
# js-yaml and npm `yaml` and not by go-yaml when the front matter text handed to
# the reader does not end with a line break.
GOAL_BLOCK_INDICATORS = {">-", "|-"}
NAME_RE = re.compile(r"[a-z0-9-]+")

# The YAML 1.1 null and boolean words, matched in any case: Ruby's YAML reader
# reads plain `NuLL` as null.
NULL_WORD_RE = re.compile(r"(?i:null)")
BOOL_WORD_RE = re.compile(r"(?i:y|n|yes|no|true|false|on|off)")


class FrontMatterError(Exception):
    pass


def spaces(n):
    return f"{n} space" if n == 1 else f"{n} spaces"


def layout_error(msg):
    return FrontMatterError(
        f"the front matter is not in the layout the default modules use: {msg}; {LAYOUT}"
    )


class Plain(str):
    """The text of a plain scalar, with the number of the line it is on."""

    def __new__(cls, text, lineno):
        obj = super().__new__(cls, text)
        obj.lineno = lineno
        return obj


class Block(str):
    """The text of a block scalar, with its key's line number and indicator."""

    def __new__(cls, text, lineno, style):
        obj = super().__new__(cls, text)
        obj.lineno = lineno
        obj.style = style
        return obj


def bad_character(ch):
    """Return True for a character the front matter must not hold.

    These are every character other than space and LF that Python reports as
    whitespace (tab among them), every control character (Cc) other than LF,
    every format (Cf), line separator (Zl) and paragraph separator (Zp)
    character, every space separator (Zs) other than space, and U+FFFE and
    U+FFFF, which are outside the characters YAML reads.
    """
    if ch in " \n":
        return False
    if ch.isspace() or ch in "\ufffe\uffff":
        return True
    return unicodedata.category(ch) in ("Cc", "Cf", "Zl", "Zp", "Zs")


def character_problems(lines):
    """Return one message per line [(lineno, text)] holding a bad character."""
    msgs = []
    for lineno, line in lines:
        seen = []
        for ch in line:
            if bad_character(ch) and ch not in seen:
                seen.append(ch)
        if seen:
            names = ", ".join(
                f"U+{ord(ch):04X}" + (f" ({unicodedata.name(ch)})" if unicodedata.name(ch, "") else "")
                for ch in seen
            )
            msgs.append(
                f"line {lineno}: character {names}; the front matter holds no whitespace other "
                "than space and the line end, and no tab, control, format or separator "
                "character; remove it, or write a space in its place"
            )
    return msgs


# The escapes YAML 1.1 and YAML 1.2 both read; `\/` is YAML 1.2 only.
DQ_ESCAPES = {"\\": "\\", '"': '"', "n": "\n", "t": "\t"}


def single_quoted_value(value, lineno):
    """Return the value of a single-line single-quoted scalar, or raise."""
    out = []
    i = 1
    while i < len(value):
        ch = value[i]
        if ch == "'":
            if value[i + 1:i + 2] == "'":
                out.append("'")
                i += 2
                continue
            if i != len(value) - 1:
                raise FrontMatterError(f"line {lineno}: text after the closing quote")
            return "".join(out)
        out.append(ch)
        i += 1
    raise FrontMatterError(f"line {lineno}: single-quoted value not closed on its line")


def double_quoted_value(value, lineno):
    """Return the value of a single-line double-quoted scalar, or raise."""
    out = []
    i = 1
    while i < len(value):
        ch = value[i]
        if ch == "\\":
            esc = value[i + 1:i + 2]
            if esc not in DQ_ESCAPES:
                raise FrontMatterError(
                    f"line {lineno}: escape '\\{esc}' in a double-quoted value; "
                    "the escapes accepted are '\\\\', '\\\"', '\\n' and '\\t'; "
                    "write any other character as itself"
                )
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


def one_line_value(value, lineno):
    """Return a one-line value: str when quoted, Plain when plain; or raise."""
    if value[0] == '"':
        return double_quoted_value(value, lineno)
    if value[0] == "'":
        return single_quoted_value(value, lineno)
    if re.search(r": | #|:$", value):
        raise FrontMatterError(
            f"line {lineno}: plain value {show(value)} holds ': ' or ' #' or ends with ':'; "
            "quote it (\"...\" or '...')"
        )
    return Plain(value, lineno)


def read_block(lines, i, key, indent, style, key_lineno):
    """Read the text lines of a block scalar from lines[i]; return (Block, next index)."""
    want = indent + 2
    content = []
    while i < len(lines):
        lineno, line = lines[i]
        if line.strip(" ") == "":
            raise layout_error(f"line {lineno}: blank line in the text of '{key}'")
        cur = len(line) - len(line.lstrip(" "))
        if cur <= indent:
            break
        if cur != want:
            raise layout_error(
                f"line {lineno}: a line of the text of '{key}' is indented {spaces(cur)}, not {want}"
            )
        if line.endswith(" "):
            raise layout_error(f"line {lineno}: the line ends with a space")
        content.append(line[want:])
        i += 1
    if not content:
        raise layout_error(
            f"line {key_lineno}: '{key}: {style}' is not followed by lines of text indented {want} spaces"
        )
    value = ("\n" if style.startswith("|") else " ").join(content)
    if not style.endswith("-"):
        value += "\n"
    return Block(value, key_lineno, style), i


def unexpected_line(lineno, line, key, indent, seen):
    """Return the layout error for a line that is not the `key` line expected there.

    `key` is None after `goal`, where the front matter ends.
    """
    keys = [k for k, _ in LAYOUT_KEYS]
    m = KEY_LINE_RE.match(line)
    if line.strip(" ") == "":
        msg = f"line {lineno}: blank line"
    elif line.lstrip(" ").startswith("#"):
        msg = f"line {lineno}: comment line"
    elif m is None:
        msg = f"line {lineno}: not a 'key: value' line"
    elif m.group("key") in seen:
        msg = f"line {lineno}: key '{m.group('key')}' repeated"
    elif m.group("key") == key:
        at = len(m.group("indent"))
        msg = f"line {lineno}: '{key}' is indented {spaces(at)}, not {indent}"
    elif m.group("key") in keys:
        msg = f"line {lineno}: key '{m.group('key')}' out of order"
    else:
        msg = f"line {lineno}: key '{m.group('key')}' is not in the layout"
    if key is None:
        msg += "; the front matter ends after 'goal'"
    elif m is None or m.group("key") != key:
        msg += f"; the line '{' ' * indent}{key}:' comes here"
    return layout_error(msg)


def read_front_matter(lines):
    """Read front matter lines [(lineno, text)] in the layout; return {key: value}, or raise.

    The values are those of `name`, `description` and `goal`.
    """
    values = {}
    seen = []
    i = 0
    for key, indent in LAYOUT_KEYS:
        if i == len(lines):
            raise layout_error(f"the front matter ends before '{key}'")
        lineno, line = lines[i]
        prefix = " " * indent + key + ":"
        if line != prefix and not line.startswith(prefix + " "):
            raise unexpected_line(lineno, line, key, indent, seen)
        if line.endswith(" "):
            raise layout_error(f"line {lineno}: the line ends with a space")
        seen.append(key)
        i += 1
        rest = line[len(prefix):]
        if key == "metadata":
            if rest:
                raise layout_error(f"line {lineno}: text after 'metadata:'")
            continue
        if rest == "":
            values[key] = Plain("", lineno)
            continue
        value = rest[1:]
        if value.startswith(" "):
            raise layout_error(f"line {lineno}: more than one space after '{key}:'")
        if key == "goal" and value in BLOCK_INDICATORS - GOAL_BLOCK_INDICATORS:
            raise layout_error(
                f"line {lineno}: 'goal: {value}'; YAML readers differ on the final line break "
                f"of the last value of the front matter; write 'goal: {value}-'"
            )
        if value in BLOCK_INDICATORS:
            values[key], i = read_block(lines, i, key, indent, value, lineno)
        else:
            values[key] = one_line_value(value, lineno)
    if i < len(lines):
        lineno, line = lines[i]
        raise unexpected_line(lineno, line, None, 0, seen)
    return values


def split_front_matter(text):
    """Return (front matter lines, body lines with numbers), or raise."""
    lines = text.split("\n")
    if lines[0] != "---":
        raise FrontMatterError("the file does not start with a '---' front matter line")
    for idx in range(1, len(lines)):
        if lines[idx] == "---":
            fm = [(n + 1, lines[n]) for n in range(1, idx)]
            body = [(n + 1, lines[n]) for n in range(idx + 1, len(lines))]
            return fm, body
    raise FrontMatterError("the front matter has no closing '---' line")


def front_matter_extent(text):
    """Return the lines [(lineno, text)] whose characters are checked.

    These are the front matter with its two '---' lines. When the first line is
    not '---', it is checked alone if it is '---' once its bad characters are
    removed. When there is no closing '---' line, the lines run to the first
    later line starting with '---', or to the end of the file.
    """
    lines = text.split("\n")
    numbered = [(n + 1, line) for n, line in enumerate(lines)]
    if lines[0] != "---":
        first = "".join(ch for ch in lines[0] if not bad_character(ch))
        return numbered[:1] if first == "---" else []
    for idx in range(1, len(lines)):
        if lines[idx] == "---":
            return numbered[:idx + 1]
    for idx in range(1, len(lines)):
        if lines[idx].startswith("---"):
            return numbered[:idx + 1]
    return numbered


HEADING_RE = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")


def check_body(body, problems):
    """Check the body's item sections.

    Sections are the level-2 headings outside fenced code blocks; a level-1
    heading also ends a section. A deeper heading belongs to the section it is
    in and is not content. A line inside a fence counts as content only when
    the fence is closed.
    """
    found = {}
    current = None
    fence = None
    fence_text = False
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
        fm = FENCE_RE.match(line)
        if fm:
            fence = fm.group(1)
            fence_text = False
            continue
        hm = HEADING_RE.match(line)
        if hm:
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


def show(text):
    """Quote a value for a message, with newlines and tabs written as escapes."""
    return "'" + text.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t") + "'"


def text_problem(key, value, problems, one_line=False):
    """Record under the front matter rule a value of `key` not written as text.

    Return True when a problem was recorded. `one_line` is set for `name`,
    which is written on one line, plain or quoted.
    """
    quote = "quote it (\"...\" or '...')"
    if one_line and isinstance(value, Block):
        msg = (
            f"line {value.lineno}: '{key}' is a block scalar ('{value.style}'); "
            f"write '{key}' on one line, plain or quoted"
        )
    elif isinstance(value, Plain) and value == "":
        msg = (
            f"line {value.lineno}: '{key}' has no value, which a YAML reader reads as null; "
            "write the value as text"
        )
    elif isinstance(value, Plain) and (NULL_WORD_RE.fullmatch(value) or BOOL_WORD_RE.fullmatch(value)):
        kind = "null" if NULL_WORD_RE.fullmatch(value) else "a boolean"
        msg = (
            f"line {value.lineno}: '{key}' is written plain as '{value}', which a YAML reader "
            f"reads as {kind}; {quote}"
        )
    elif isinstance(value, Plain) and not unicodedata.category(value[0]).startswith("L"):
        msg = (
            f"line {value.lineno}: '{key}' is written plain as '{value}', which starts with "
            f"'{value[0]}', not a letter; a plain value is taken as text only when it starts "
            f"with a letter; {quote}"
        )
    elif value == "":
        msg = f"'{key}' is empty"
    else:
        return False
    problems[RULE_FRONT_MATTER].append(msg)
    return True


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
        bad_chars = character_problems(front_matter_extent(text))
        problems[RULE_FRONT_MATTER].extend(bad_chars)
        if fm_lines is not None and not bad_chars:
            try:
                data = read_front_matter(fm_lines)
            except FrontMatterError as exc:
                problems[RULE_FRONT_MATTER].append(str(exc))
        check_body(body, problems)

    name = None
    if data is not None:
        name_ok = not text_problem("name", data["name"], problems, one_line=True)
        text_problem("description", data["description"], problems)
        text_problem("metadata.goal", data["goal"], problems)

        if name_ok:
            name = str(data["name"])
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

        if len(data["description"]) > 1024:
            problems[RULE_DESCRIPTION].append(f"'description' is {len(data['description'])} characters")

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
