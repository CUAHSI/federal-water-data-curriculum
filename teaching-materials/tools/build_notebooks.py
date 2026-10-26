"""Build the learner bundle's notebooks from the lesson pages (STYLE_GUIDE §11, build-notebooks skill).

For each Module 3 and 4 lesson with code, this writes to ``teaching-materials/learner-bundle/``:

- ``<lesson>.ipynb``            student notebook: "Now you try it" starters come from ``scaffolds/<lesson>.yml``
- ``<lesson>_solutions.ipynb``  solutions notebook: the lesson's example answer
- ``<lesson>_environment.yml``  a copy of the lesson's ``environments/*.yml`` (the env ``name:`` is kept)

Each notebook starts from the learner copy of the page (``prepare_learner_copy.prepare``: no internal callouts,
no internal course links) and has, in order: a title cell (title, learning goal, environment, introduction), an
attribution and licence cell, a credentials cell, then the lesson in order. Headings keep the lesson's text, every
``python`` code block becomes a code cell, and prose is condensed by these rules:

- each run of prose between two code cells keeps at most ``SENTENCE_BUDGET`` sentences of paragraph text (a
  sentence ending in ":" that leads into a table, list or code block is always kept);
- lists, tables, block quotes and notes are kept whole: they hold the "what comes back" details;
- printed outputs, shell and YAML blocks (environment creation) and lesson figures are dropped (the code cell that
  draws a figure stays); externally hosted figures are kept as images;
- "Now you try it" and "Further reading" are kept whole;
- paragraphs about creating the environment (``DROP_PARAGRAPHS``) and code blocks the credentials cell replaces
  (``Lesson.drop_code``) are left out.

Outputs are cleared and notebook metadata is kept to the kernelspec, so rebuilds give small diffs.

Usage (from the repo root; needs nbformat and pyyaml):
    python teaching-materials/tools/build_notebooks.py               # build every lesson
    python teaching-materials/tools/build_notebooks.py --lesson module-03_lesson-01_retrieve-nasa-swot-data
    python teaching-materials/tools/build_notebooks.py --check       # report what would change, write nothing

Scaffold files (``learner-bundle/scaffolds/<lesson>.yml``) are hand-edited source, not generated::

    try_it:            # one entry per example-answer code block, in order
      - |
        site_name = ...   # TODO: ...

A lesson with a "Now you try it" section must have a scaffold; the build stops if one is missing or has the
wrong number of entries. A lesson without one gets a student notebook that matches its solutions notebook.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import nbformat
import yaml

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from prepare_learner_copy import prepare  # noqa: E402

REPO_ROOT = TOOLS.parents[1]
BUNDLE = REPO_ROOT / "teaching-materials" / "learner-bundle"
SCAFFOLDS = BUNDLE / "scaffolds"

SENTENCE_BUDGET = 4
KEEP_WHOLE_SECTIONS = ("Now you try it", "Further reading")
# Paragraphs about creating the conda environment: the bundle ships the environment file and the README covers setup.
DROP_PARAGRAPHS = (
    "Create an empty YAML file",
    "Create the YAML file",
    "Create and activate the environment",
    "Copy and paste the code snippet",
    "If you work in Jupyter, choose the",
    "You will create a {term}",
    "You will create a conda environment",
    "Log in to earthaccess",
    "Check that the key is available",
)
CREDENTIALS = ("earthdata", "usgs")
SETUP_SECTION = "Tools and environment setup"
SETUP_NOTE = ("This notebook runs in the `{env}` conda environment, made from `{stem}_environment.yml` in this folder "
              "(the bundle README says how). Credentials are set up in the Credentials section above.")


@dataclass
class Lesson:
    stem: str                 # file stem in the bundle, from STYLE_GUIDE §11
    page: str                 # lesson page, repo-relative
    env: str                  # environments/<env>.yml
    session: int
    credentials: tuple        # subset of CREDENTIALS
    goal: str                 # from the module's learning objectives
    drop_code: tuple = ()     # substrings: python blocks containing one are left out
    drop_paragraphs: tuple = field(default_factory=tuple)

    @property
    def module_folder(self) -> str:
        module = self.stem.split("_")[0]
        return {"module-03": "module-03_federal-water-data-access-retrieval",
                "module-04": "module-04_federal-water-data-synthesis"}[module]


M3_GOAL = ("Retrieve {product} data for a location of interest, describe what comes back using the course's shared "
           "concepts, and choose an access pattern that scales with your question.")

LESSONS = [
    Lesson(
        stem="module-03_lesson-01_retrieve-nasa-swot-data",
        page="03-federal-water-data-access-retrieval/01_access_nasa_swot.md",
        env="m03-swot", session=3, credentials=("earthdata",),
        goal=M3_GOAL.format(product="NASA SWOT"),
        drop_code=("auth = earthaccess.login()",),
    ),
    Lesson(
        stem="module-03_lesson-02_retrieve-noaa-nwm-data",
        page="03-federal-water-data-access-retrieval/02_access_noaa_nwm.md",
        env="m03-nwm", session=4, credentials=(),
        goal=M3_GOAL.format(product="NOAA NWM"),
        drop_paragraphs=("The environment file pins the Python version",),
    ),
    Lesson(
        stem="module-03_lesson-03_retrieve-usgs-wdfn-data",
        page="03-federal-water-data-access-retrieval/03_access_usgs_wdfn.md",
        env="m03-wdfn", session=5, credentials=("usgs",),
        goal=M3_GOAL.format(product="USGS WDFN"),
        drop_code=('print("API_USGS_PAT is set:"',),
        drop_paragraphs=("The environment file lets most packages float",),
    ),
    Lesson(
        stem="module-04_lesson-02_synthesizing-federal-data-products",
        page="04-federal-water-data-synthesis/02_synthesize_river_data.md",
        env="m04-synthesis", session=6, credentials=("usgs", "earthdata"),
        goal=("Retrieve and line up USGS observations, NWM forecasts and SWOT measurements for one flood, accounting "
              "for differences in location identifiers, units, vertical reference, time zone and sampling, and explain "
              "what each product can and cannot show."),
        drop_paragraphs=("A pinned conda environment is what lets", "You will need the same credentials as in Module 3",
                         "The sections below walk through the data you would collect"),
    ),
    Lesson(
        stem="module-04_lesson-03_additional-federal-water-data",
        page="04-federal-water-data-synthesis/03_additional_data.md",
        env="m04-synthesis", session=6, credentials=("earthdata",),
        goal=("Take a first step with related Federal water data products (SWOT discharge from the SWORD of Science "
              "and NOAA AORC precipitation) using the same discover-before-download habits as Module 3."),
    ),
]

# --------------------------------------------------------------------------------------------- parsing the page

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
CODE_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([\w+-]*)")
DIRECTIVE = re.compile(r"^\s*(:{3,})\s*\{([\w-]+)\}\s*(.*?)\s*$")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
OPTION = re.compile(r"^\s*:[\w-]+:")


@dataclass
class Item:
    kind: str                 # heading, para, list, table, quote, code, fence, figure, dropdown, note
    text: str = ""
    level: int = 0
    lang: str = ""
    title: str = ""
    children: list = field(default_factory=list)


def _starts_block(line: str) -> bool:
    return bool(HEADING.match(line) or CODE_FENCE.match(line) or DIRECTIVE.match(line)
                or line.lstrip().startswith(("|", ">")) or LIST_ITEM.match(line))


def parse(lines: list[str]) -> list[Item]:
    items, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if m := HEADING.match(line):
            items.append(Item("heading", m.group(2), level=len(m.group(1))))
            i += 1
        elif m := CODE_FENCE.match(line):
            fence, j = m.group(2), i + 1
            while j < len(lines) and not lines[j].strip().startswith(fence):
                j += 1
            indent = len(m.group(1))
            body = [ln[indent:] if ln[:indent].isspace() else ln for ln in lines[i + 1:j]]
            items.append(Item("code" if m.group(3) == "python" else "fence", "\n".join(body), lang=m.group(3)))
            i = j + 1
        elif m := DIRECTIVE.match(line):
            colons, name, arg, j = m.group(1), m.group(2), m.group(3), i + 1
            while j < len(lines) and lines[j].strip() != colons:
                j += 1
            body = [ln for ln in lines[i + 1:j] if not OPTION.match(ln)]
            kind = {"figure": "figure", "dropdown": "dropdown"}.get(name, "note")
            items.append(Item(kind, "\n".join(lines[i + 1:j]).strip(), title=arg, children=parse(body)))
            i = j + 1
        elif line.lstrip().startswith("|"):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            items.append(Item("table", "\n".join(lines[i:j])))
            i = j
        elif line.lstrip().startswith(">"):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                j += 1
            items.append(Item("quote", "\n".join(lines[i:j])))
            i = j
        elif LIST_ITEM.match(line):
            j = i + 1
            while j < len(lines):
                if lines[j].strip():
                    if not (lines[j].startswith((" ", "\t")) or LIST_ITEM.match(lines[j])):
                        break
                else:
                    nxt = next((ln for ln in lines[j:] if ln.strip()), "")
                    if not (nxt.startswith((" ", "\t")) or LIST_ITEM.match(nxt)):
                        break
                j += 1
            items.append(Item("list", "\n".join(lines[i:j]).rstrip()))
            i = j
        else:
            j = i + 1
            while j < len(lines) and lines[j].strip() and not _starts_block(lines[j]):
                j += 1
            items.append(Item("para", " ".join(ln.strip() for ln in lines[i:j])))
            i = j
    return items


# --------------------------------------------------------------------------------------------- condensing prose

ABBREVIATIONS = ("e.g.", "i.e.", "U.S.", "vs.", "approx.", "Mt.", "No.", "Fig.", "al.", "etc.")
INLINE = re.compile(r"`[^`]*`|\[[^\]]*\]\([^)]*\)")
SENTENCE_END = re.compile(r"[.!?:][)*_\"']*\s+(?=[A-Z0-9*_(\[`\"])")


def sentences(text: str) -> list[str]:
    """Split a paragraph into sentences, leaving inline code and links intact."""
    protected = []

    def hide(m):
        protected.append(m.group(0))
        return f"\x00{len(protected) - 1}\x00"

    masked = INLINE.sub(hide, text)
    out, start = [], 0
    for m in SENTENCE_END.finditer(masked):
        head = masked[start:m.end()].rstrip()
        if head.endswith(":") or any(head.endswith(a) for a in ABBREVIATIONS):
            continue  # a colon only ends a sentence at the end of a paragraph; abbreviations never do
        out.append(head)
        start = m.end()
    out.append(masked[start:].strip())
    if len(out) > 1 and re.fullmatch(r"\*\*[^*]+\*\*", out[0]):
        out[:2] = [f"{out[0]} {out[1]}"]  # a bold run-in label ("**The point-and-click way.**") isn't a sentence
    restore = re.compile("\x00(\\d+)\x00")
    return [restore.sub(lambda m: protected[int(m.group(1))], s) for s in out if s]


class Builder:
    """Turns parsed items into (kind, source) cells; kind is 'markdown', 'code' or 'solution'."""

    def __init__(self, lesson: Lesson):
        self.lesson = lesson
        self.cells: list[tuple[str, str]] = []
        self.prose: list[str] = []
        self.budget = SENTENCE_BUDGET
        self.section = ""
        self.after_code = False
        self.drop_paragraphs = DROP_PARAGRAPHS + lesson.drop_paragraphs

    @property
    def keep_whole(self) -> bool:
        return self.section in KEEP_WHOLE_SECTIONS

    def flush(self):
        if self.prose:
            self.cells.append(("markdown", "\n\n".join(self.prose)))
            self.prose = []
        self.budget = SENTENCE_BUDGET

    def para(self, text: str):
        if any(text.startswith(p) or text.lstrip("*").startswith(p) for p in self.drop_paragraphs):
            return
        if self.keep_whole:
            self.prose.append(text)
            return
        parts = sentences(text)
        kept = parts[: max(self.budget, 0)]
        if len(parts) > len(kept) and parts[-1].endswith(":"):
            # The lead-in to the next table, list or code block; a very short one ("The main ones:") needs the
            # sentence before it too.
            lead = parts[-2:] if len(parts[-1].split()) < 8 and len(parts) - len(kept) > 1 else parts[-1:]
            kept += lead
        if not kept:
            return
        self.budget -= len(kept)
        self.prose.append(" ".join(kept))

    def add(self, items: list[Item], solution: bool = False):
        for item in items:
            was_after_code, self.after_code = self.after_code, False
            if item.kind == "heading":
                self.flush()
                self.section = item.text
                if item.level > 1:
                    self.prose.append(f"{'#' * item.level} {item.text}")
                if item.text == SETUP_SECTION:
                    self.prose.append(SETUP_NOTE.format(env=self.lesson.env, stem=self.lesson.stem))
            elif item.kind == "para":
                self.para(item.text)
            elif item.kind in ("list", "table", "quote"):
                if item.kind == "list" and any(p in item.text.split("\n")[0] for p in self.drop_paragraphs):
                    continue
                self.prose.append(item.text)
            elif item.kind == "note":
                body = " ".join(c.text for c in item.children if c.kind == "para")
                self.prose.append(f"> **{item.title}.** {body}" if item.title else f"> {body}")
            elif item.kind == "figure":
                if item.title.startswith("http"):  # externally hosted context figure: no code draws it
                    alt = next((ln.split(":alt:", 1)[1].strip() for ln in item.text.splitlines() if ":alt:" in ln), "")
                    caption = " ".join(c.text for c in item.children if c.kind == "para")
                    self.prose.append(f"![{alt or 'Figure'}]({item.title})\n\n*{caption}*")
            elif item.kind == "dropdown":
                if not any(c.kind == "code" for c in item.children):
                    continue  # e.g. the YAML file contents: the bundle ships the environment file
                is_answer = item.title.lower().startswith("example answer")
                if not is_answer:
                    self.prose.append(f"**{item.title}**")
                self.add(item.children, solution=is_answer)
            elif item.kind == "code":
                if any(s in item.text for s in self.lesson.drop_code):
                    self.after_code = True
                    continue
                self.flush()
                self.cells.append(("solution" if solution else "code", item.text.strip("\n")))
                self.after_code = True
            elif item.kind == "fence":
                if was_after_code or item.lang in ("bash", "sh", "shell", "yaml", "yml", ""):
                    continue  # printed output, or environment setup
                self.prose.append(f"```{item.lang}\n{item.text}\n```")
        return self


# --------------------------------------------------------------------------------------------- the fixed cells

def title_cell(lesson: Lesson, title: str, intro: str, solutions: bool, has_try_it: bool) -> str:
    env_file = f"{lesson.stem}_environment.yml"
    kind = ("This lesson has no \"Now you try it\" task, so the student and solutions copies of this notebook are "
            "the same." if not has_try_it else
            "**Solutions notebook.** This copy includes the example answer to every \"Now you try it\" task."
            if solutions else
            "**Student notebook.** \"Now you try it\" cells are starters: fill in the `...` blanks, guided by the "
            "`# TODO:` comments. The solutions notebook in the same folder has an example answer.")
    return (f"# {title}\n\n"
            f"*Federal Open Water Data for Researchers* (CUAHSI), session {lesson.session}.\n\n"
            f"**Learning goal:** {lesson.goal}\n\n"
            f"**Environment:** run this notebook in the `{lesson.env}` conda environment, created from "
            f"`{env_file}` in this folder (see the bundle README). Run the cells in order: later cells reuse "
            f"variables from earlier ones.\n\n"
            f"{kind}\n\n{intro}")


def attribution_cell(adapted: list[str]) -> str:
    lines = ["## Attribution and licence", "",
             "This notebook is part of *Federal Open Water Data for Researchers*, a CUAHSI course, and is released "
             "under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) (GPL-3.0). You "
             "may use, change and share it under the same licence."]
    if adapted:
        lines += ["", "It adapts code and ideas from these sources:", ""]
        lines += [f"- {a}" for a in adapted]
    lines += ["", "Other sources used in the lesson are listed under \"Further reading\" at the end of this notebook."]
    return "\n".join(lines)


EARTHDATA_MD = (
    "**NASA Earthdata Login.** Downloading SWOT files needs a free account from "
    "[urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov). `earthaccess.login()` looks for your username and "
    "password in the `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` environment variables, then in a `~/.netrc` "
    "file, and otherwise asks you for them. In a hosted Jupyter environment, the simplest route is to let it ask: "
    "run the cell and type your details into the boxes it shows. To avoid typing them every session, run "
    "`earthaccess.login(persist=True)` once, which saves them to `~/.netrc` in your home folder. Never type your "
    "password into a code cell: it would be saved in the notebook. See the "
    "[`earthaccess` authentication how-to](https://earthaccess.readthedocs.io/en/latest/user/howto/authenticate/).")
EARTHDATA_CODE = (
    "import earthaccess\n\n"
    "# Uses EARTHDATA_USERNAME/EARTHDATA_PASSWORD or ~/.netrc if set; otherwise asks you to type them\n"
    "auth = earthaccess.login()\n"
    "print(\"Logged in to NASA Earthdata:\", auth.authenticated)")
USGS_MD = (
    "**USGS Water Data API key (optional).** The USGS Water Data APIs work without a key, but a key raises your "
    "rate limit. Request one at the [USGS Water Data API signup page](https://api.waterdata.usgs.gov/signup/). "
    "`dataretrieval` reads it from the `API_USGS_PAT` environment variable and sends it for you. If your hosted "
    "environment doesn't set that variable, uncomment the two lines below and paste your key when asked: it is kept "
    "only for this session and isn't saved in the notebook. Don't print the key or write it into a cell.")
USGS_CODE = (
    "import os\n\n"
    "# Optional: set the key for this session only (it isn't saved in the notebook)\n"
    "# from getpass import getpass\n"
    "# os.environ[\"API_USGS_PAT\"] = getpass(\"USGS API key: \")\n"
    "print(\"API_USGS_PAT is set:\", bool(os.getenv(\"API_USGS_PAT\")))")
NO_CREDENTIALS_MD = ("No account or key is needed for anything in this notebook: the NLDI, the NOAA NWM API and the "
                     "NWM archives on Google Cloud and AWS are all public.")


def credentials_cells(lesson: Lesson) -> list[tuple[str, str]]:
    if not lesson.credentials:
        return [("markdown", "## Credentials\n\n" + NO_CREDENTIALS_MD)]
    md = ["## Credentials", "",
          "Credentials come only from your account or environment, never from the notebook itself."]
    code = []
    for cred in lesson.credentials:
        md += ["", EARTHDATA_MD if cred == "earthdata" else USGS_MD]
        code.append(EARTHDATA_CODE if cred == "earthdata" else USGS_CODE)
    return [("markdown", "\n".join(md))] + [("code", c) for c in code]


# --------------------------------------------------------------------------------------------- notebooks

def load_scaffold(lesson: Lesson) -> list[str] | None:
    path = SCAFFOLDS / f"{lesson.stem}.yml"
    if not path.exists():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [s.rstrip("\n") for s in data.get("try_it", [])]


def make_notebook(cells: list[tuple[str, str]]) -> nbformat.NotebookNode:
    nb = nbformat.v4.new_notebook()
    nb.metadata = {"kernelspec": {"name": "python3", "display_name": "Python 3 (ipykernel)", "language": "python"}}
    for kind, source in cells:
        cell = nbformat.v4.new_markdown_cell(source) if kind == "markdown" else nbformat.v4.new_code_cell(source)
        cell.pop("id", None)
        nb.cells.append(cell)
    nb.nbformat_minor = 4  # 4.4 has no cell ids, so rebuilds don't churn them
    return nb


def build(lesson: Lesson) -> tuple[dict[str, str], dict]:
    """Return {bundle-relative path: file text} for one lesson, and the learner-copy counts."""
    raw = (REPO_ROOT / lesson.page).read_text(encoding="utf-8")
    text, counts = prepare(raw)
    items = parse(text.splitlines())

    title = next(i.text for i in items if i.kind == "heading" and i.level == 1)
    first_section = next(n for n, i in enumerate(items) if i.kind == "heading" and i.level == 2)
    intro_paras = [i.text for i in items[:first_section] if i.kind == "para"]
    intro = " ".join(sentences(" ".join(intro_paras[:2]))[:SENTENCE_BUDGET])

    body = Builder(lesson).add(items[first_section:])
    body.flush()

    further = next((i for i in items if i.kind == "heading" and i.text == "Further reading"), None)
    adapted = []
    if further:
        after = items[items.index(further) + 1:]
        for it in after:
            if it.kind == "list":
                entries = re.split(r"\n(?=[-*] )", it.text)
                adapted += [re.sub(r"^[-*]\s+", "", e).split("\n\n")[0].replace("\n", " ").strip()
                            for e in entries if "dapted from" in e]
    adapted = [re.sub(r"\s+", " ", a) for a in adapted]

    solution_cells = [src for kind, src in body.cells if kind == "solution"]
    scaffold = load_scaffold(lesson)
    if solution_cells:
        if scaffold is None:
            raise SystemExit(f"{lesson.stem}: no scaffold; write scaffolds/{lesson.stem}.yml (see this script's docstring)")
        if len(scaffold) != len(solution_cells):
            raise SystemExit(f"{lesson.stem}: scaffold has {len(scaffold)} try_it entries; the lesson has "
                             f"{len(solution_cells)} example-answer code blocks")

    outputs = {}
    for solutions in (False, True):
        cells = [("markdown", title_cell(lesson, title, intro, solutions, bool(solution_cells))),
                 ("markdown", attribution_cell(adapted))] + credentials_cells(lesson)
        starters = iter(scaffold or [])
        for kind, src in body.cells:
            if kind == "solution":
                cells.append(("code", src if solutions else next(starters)))
            else:
                cells.append((kind, src))
        name = f"{lesson.module_folder}/{lesson.stem}{'_solutions' if solutions else ''}.ipynb"
        outputs[name] = nbformat.writes(make_notebook(cells)) + "\n"

    env_text = (REPO_ROOT / "environments" / f"{lesson.env}.yml").read_text(encoding="utf-8")
    env_text = env_text.replace(f"environments/{lesson.env}.yml", f"{lesson.stem}_environment.yml")
    outputs[f"{lesson.module_folder}/{lesson.stem}_environment.yml"] = env_text
    counts["has_try_it"] = bool(solution_cells)
    return outputs, counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--lesson", action="append", help="build only this lesson stem (repeatable)")
    parser.add_argument("--check", action="store_true", help="report files that would change; write nothing")
    args = parser.parse_args(argv)

    lessons = [l for l in LESSONS if not args.lesson or l.stem in args.lesson]
    if args.lesson and len(lessons) != len(args.lesson):
        parser.error(f"unknown lesson; choose from {[l.stem for l in LESSONS]}")
    changed = 0
    for lesson in lessons:
        outputs, counts = build(lesson)
        print(f"{lesson.stem}: removed {counts['todo_callouts_removed']} TODO and "
              f"{counts['partner_review_callouts_removed']} Partner review callouts; converted "
              f"{counts['internal_links_converted']} internal links"
              + ("" if counts["has_try_it"] else "; no \"Now you try it\" (student = solutions)")
              + (f"; WARNING: {counts['flag_mentions_left']} flag mention(s) left" if counts.get("flag_mentions_left") else ""))
        for rel, content in outputs.items():
            path = BUNDLE / rel
            old = path.read_text(encoding="utf-8") if path.exists() else None
            if old == content:
                continue
            changed += 1
            print(f"  {'would write' if args.check else 'wrote'} {path.relative_to(REPO_ROOT).as_posix()}")
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    sys.exit(main())
