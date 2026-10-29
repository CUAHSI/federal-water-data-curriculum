"""Make a learner-facing copy of a course page (STYLE_GUIDE §11).

Pilot learners can't open the website or the repo, so every learner-facing builder (slides, readings,
notebooks, quizzes) starts from this copy. It:

- removes every ``TODO (dev team)`` and ``Partner review (NASA|NOAA|USGS)`` admonition;
- turns internal course links into plain text: relative Markdown links to other pages (including the
  Glossary and References pages), in-page ``#anchor`` links, links to the course repo or website, and the
  ``{term}``, ``{ref}``, ``{doc}``, ``{numref}`` and ``{download}`` roles;
- keeps external ``http(s)``/``mailto`` links and images;
- drops MyST target labels such as ``(m01-project-organization)=``, which would show up as text;
- reports the counts, so open items aren't forgotten.

Code blocks and inline code are left alone.

Usage:
    python teaching-materials/how-to-build/tools/prepare_learner_copy.py PAGE.md            # copy to stdout
    python teaching-materials/how-to-build/tools/prepare_learner_copy.py PAGE.md -o OUT.md
    python teaching-materials/how-to-build/tools/prepare_learner_copy.py PAGE.md... --out-dir DIR

With ``--out-dir``, each copy keeps its path relative to the repo root (``DIR/03-.../01_access_nasa_swot.md``),
so pages with the same file name don't collide. Counts go to stderr; ``--json`` prints them as JSON instead.

From Python::

    from prepare_learner_copy import prepare
    text, counts = prepare(open(page, encoding="utf-8").read())

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

# Opening line of an internal callout: a ::: or ``` fence, the admonition directive and one of the two
# flag titles from STYLE_GUIDE §7.
CALLOUT_OPEN = re.compile(
    r"^(?P<indent>[ \t]*)(?P<fence>:{3,}|`{3,})\{admonition\}[ \t]+"
    r"(?P<kind>TODO \(dev team\)|Partner review \((?:NASA|NOAA|USGS)\))"
)
CODE_FENCE = re.compile(r"^[ \t]*(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
LABEL_LINE = re.compile(r"^\([A-Za-z0-9_.:-]+\)=[ \t]*$")
ROLE = re.compile(r"\{(?P<role>term|ref|doc|numref|download)\}`(?P<body>[^`]+)`")
BARE_ROLE = re.compile(r"\{(?:term|ref|doc|numref|download)\}(?=\w)")
INLINE_CODE = re.compile(r"(`+)(?:(?!\1).)+?\1")
# Links to the course itself are internal even though they use http(s).
COURSE_URL = re.compile(
    r"^https?://(?:www\.)?(?:github\.com/cuahsi/federal-water-data-curriculum|cuahsi\.github\.io/federal-water-data-curriculum)",
    re.IGNORECASE,
)
EXTERNAL_URL = re.compile(r"^(?:https?:|mailto:)", re.IGNORECASE)


def _role_text(match: re.Match) -> str:
    """``{term}`reproducible <Reproducibility>``` -> ``reproducible``; ``{term}`FAIR``` -> ``FAIR``."""
    body = match.group("body").strip()
    explicit = re.match(r"^(?P<text>.*?)\s*<[^<>]+>$", body, re.S)
    text = explicit.group("text") if explicit and explicit.group("text") else body
    if match.group("role") in ("ref", "numref", "doc") and not explicit:
        # A bare {ref}`label` renders as the target's title, which we don't have; make the label readable.
        text = text.replace("-", " ").replace("_", " ")
    return text


def _match_bracket(s: str, start: int, open_ch: str, close_ch: str) -> int:
    """Index of the bracket closing the one at ``start``, or -1."""
    depth = 0
    i = start
    while i < len(s):
        ch = s[i]
        if ch == "\\":
            i += 2
            continue
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _convert_links(s: str, counts: dict) -> str:
    """Replace internal ``[text](target)`` links with their text; keep external links and images."""
    out = []
    i = 0
    while i < len(s):
        if s[i] == "[" and (i == 0 or s[i - 1] not in "!\\"):
            close = _match_bracket(s, i, "[", "]")
            if close != -1 and close + 1 < len(s) and s[close + 1] == "(":
                end = _match_bracket(s, close + 1, "(", ")")
                if end != -1:
                    text = _convert_links(s[i + 1 : close], counts)  # e.g. an image inside the link
                    target = s[close + 2 : end].strip().split()[0] if s[close + 2 : end].strip() else ""
                    if EXTERNAL_URL.match(target) and not COURSE_URL.match(target):
                        counts["external_links_kept"] += 1
                        out.append(f"[{text}]({s[close + 2 : end]})")
                    else:
                        counts["internal_links_converted"] += 1
                        out.append(text)
                    i = end + 1
                    continue
        if s[i] == "!" and i + 1 < len(s) and s[i + 1] == "[":
            # Image: keep it whole (alt text may itself contain brackets).
            close = _match_bracket(s, i + 1, "[", "]")
            if close != -1 and close + 1 < len(s) and s[close + 1] == "(":
                end = _match_bracket(s, close + 1, "(", ")")
                if end != -1:
                    out.append(s[i : end + 1])
                    i = end + 1
                    continue
        out.append(s[i])
        i += 1
    return "".join(out)


def _convert_prose(line: str, counts: dict) -> str:
    """Convert links in a prose line without touching inline code (link text may contain code)."""
    spans: list[str] = []

    def hide(code: re.Match) -> str:
        spans.append(code.group(0))
        return f"\x00{len(spans) - 1}\x00"

    hidden = _convert_links(INLINE_CODE.sub(hide, line), counts)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], hidden)


def prepare(text: str) -> tuple[str, dict]:
    """Return the learner copy of a page's Markdown and the counts of what changed."""
    counts = {
        "todo_callouts_removed": 0,
        "partner_review_callouts_removed": 0,
        "internal_links_converted": 0,
        "external_links_kept": 0,
        "labels_removed": 0,
    }
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    code_fence: str | None = None  # the fence of the plain code block we're in, if any
    directive_fences: list[str] = []  # open ```{directive} fences
    i = 0
    while i < len(lines):
        line = lines[i]
        bare = line.rstrip("\r\n")

        if code_fence is not None:
            out.append(line)
            if bare.strip().startswith(code_fence[0]) and set(bare.strip()) == {code_fence[0]} \
                    and len(bare.strip()) >= len(code_fence):
                code_fence = None
            i += 1
            continue

        callout = CALLOUT_OPEN.match(bare)
        if callout:
            fence = callout.group("fence")
            key = "todo_callouts_removed" if callout.group("kind").startswith("TODO") else "partner_review_callouts_removed"
            counts[key] += 1
            i += 1
            while i < len(lines):
                closing = lines[i].strip()
                i += 1
                if closing and set(closing) == {fence[0]} and len(closing) >= len(fence):
                    break
            # Don't leave a double blank line where the callout was.
            if out and not out[-1].strip() and i < len(lines) and not lines[i].strip():
                i += 1
            continue

        fence_match = CODE_FENCE.match(bare)
        if fence_match:
            fence, info = fence_match.group("fence"), fence_match.group("info").strip()
            if info.startswith("{"):
                directive_fences.append(fence)  # a ```{note} directive: its body is prose
            elif not info and directive_fences and fence == directive_fences[-1]:
                directive_fences.pop()  # closes that directive
            else:
                code_fence = fence
            out.append(line)
            i += 1
            continue

        if LABEL_LINE.match(bare):
            counts["labels_removed"] += 1
            i += 1
            if out and not out[-1].strip() and i < len(lines) and not lines[i].strip():
                i += 1
            continue

        eol = line[len(bare):]
        roles_done, n_roles = ROLE.subn(_role_text, bare)
        # A role missing its backticks ("{term}USGS") renders as raw text on the site too; drop the role.
        roles_done, n_bare = BARE_ROLE.subn("", roles_done)
        counts["internal_links_converted"] += n_roles
        counts["malformed_roles_fixed"] = counts.get("malformed_roles_fixed", 0) + n_bare
        out.append(_convert_prose(roles_done, counts) + eol)
        i += 1

    result = "".join(out)
    leftover = len(re.findall(r"TODO \(dev team\)|Partner review \((?:NASA|NOAA|USGS)\)", result))
    if leftover:
        counts["flag_mentions_left"] = leftover  # e.g. prose or code that names a flag; check by hand
    return result, counts


def _summary(name: str, counts: dict) -> str:
    msg = (
        f"{name}: removed {counts['todo_callouts_removed']} TODO (dev team) and "
        f"{counts['partner_review_callouts_removed']} Partner review callouts; converted "
        f"{counts['internal_links_converted']} internal links to text; kept "
        f"{counts['external_links_kept']} external links; removed {counts['labels_removed']} labels"
    )
    if counts.get("malformed_roles_fixed"):
        msg += f"; fixed {counts['malformed_roles_fixed']} role(s) missing backticks (fix the page too)"
    if counts.get("flag_mentions_left"):
        msg += f"; WARNING: {counts['flag_mentions_left']} flag mention(s) left, check by hand"
    return msg


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("pages", nargs="+", type=Path, help="course page(s) to copy")
    dest = parser.add_mutually_exclusive_group()
    dest.add_argument("-o", "--output", type=Path, help="write the copy here (one page only)")
    dest.add_argument("--out-dir", type=Path, help="write copies here, keeping repo-relative paths")
    parser.add_argument("--json", action="store_true", help="print the counts as JSON on stderr")
    args = parser.parse_args(argv)

    if len(args.pages) > 1 and not args.out_dir:
        parser.error("use --out-dir with more than one page")

    all_counts = {}
    for page in args.pages:
        text, counts = prepare(page.read_text(encoding="utf-8"))
        try:
            rel = page.resolve().relative_to(REPO_ROOT)
        except ValueError:
            rel = Path(page.name)
        all_counts[rel.as_posix()] = counts
        if args.out_dir:
            target = args.out_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8", newline="\n")
        elif args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8", newline="\n")
        else:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stdout.write(text)
        if not args.json:
            print(_summary(rel.as_posix(), counts), file=sys.stderr)

    if args.json:
        print(json.dumps(all_counts, indent=2), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
