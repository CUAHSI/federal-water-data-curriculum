# Teaching materials

Everything needed to *run* *Federal Open Water Data for Researchers*: session slides, pre- and post-session
readings, the learner bundle for HydroShare, the module quizzes and the instructor guide. These files are
generated from the lesson pages (`0*/`), which stay the single source of truth. To fix content, edit the
lesson, then rebuild. This folder isn't part of the website build (`myst.yml` excludes it).

The rules (names, the session map, learner-facing outputs, live coding, quizzes) are in
[STYLE_GUIDE §11](../STYLE_GUIDE.md#11-teaching-materials). This README records the names the Phase 8 lanes
build to, so they agree before they start.

## How outputs are built

Most outputs are written by a Claude Code agent following a **skill**: a set of instructions in
`.claude/skills/<name>/SKILL.md` (`build-slides`, `build-notebooks`, `build-quizzes`, `build-instructor-guide`).
"Rebuild" means asking an agent to run that skill again. A person can do the same work by hand by following
the skill's steps. Only some steps are plain scripts you run yourself:

- `tools/prepare_learner_copy.py` and `tools/check_stale.py` (standard library only, any Python 3.9 or later; no
  conda environment needed);
- `tools/build_notebooks.py` (lane F; needs `nbformat` and `pyyaml`);
- rendering: `quarto render` locally, or Actions → Render slides → Run workflow;
- quizzes: `text2qti <file>.txt` makes the QTI zip.

Small hand fixes to an output (a typo on a slide) are fine, but make the same fix in the lesson page too, or
the next rebuild undoes it.

## Before you rebuild

Some builders need tools that aren't in the lesson environments. Install them once per machine:

| Skill | Needs | Used for |
|---|---|---|
| `build-slides` | [Quarto](https://quarto.org/docs/get-started/) (includes Typst, so no LaTeX needed) | rendering decks and reading PDFs locally; the Render slides action installs its own |
| `build-notebooks` | `papermill` and `ipykernel` in **each** lesson environment; `nbformat` and `pyyaml` in the Python that runs `tools/build_notebooks.py` | running every notebook top to bottom to test it |
| `build-quizzes` | [`text2qti`](https://pypi.org/project/text2qti/) | turning each quiz `.txt` into a QTI zip for Canvas |
| `build-instructor-guide` | nothing extra | |

**papermill and ipykernel** go into your installed copy of each lesson environment, not into the
`environments/*.yml` files:

```bash
conda install -n m03-swot -c conda-forge papermill ipykernel
conda install -n m03-nwm -c conda-forge papermill ipykernel
conda install -n m03-wdfn -c conda-forge papermill ipykernel
conda install -n m04-synthesis -c conda-forge papermill ipykernel
conda run -n m03-swot papermill --version   # check; repeat for each environment
```

The `.yml` files are the recipes learners build their environments from, and they're copied into the learner
bundle. `conda install -n <env>` changes only the environment installed on your machine, so learners still get
exactly what the `.yml` lists. papermill is a testing tool and the notebooks don't import it, so a notebook
that runs in your environment also runs in theirs. `ipykernel` is already in every `.yml`; installing it only
matters if your environment was built before it was added. Run notebooks inside the lesson's environment
(`conda run -n m03-swot papermill <notebook> <output>`), so each one is tested with the learners' packages.

**text2qti, nbformat and pyyaml** go into your everyday Python (e.g. conda `base`): `pip install text2qti
nbformat pyyaml`.

**Credentials.** Testing the notebooks logs in to NASA Earthdata and calls the USGS Water Data API, so the
terminal that runs the builder needs `EARTHDATA_USERNAME`, `EARTHDATA_PASSWORD` and `API_USGS_PAT` set as
environment variables (`earthaccess.login()` and `dataretrieval` read them from there). Save them once as
user environment variables (AGENT_SETUP.md, "Windows: credentials"), then open a new terminal; a terminal only reads
environment variables when it starts. Never write the values into a file in this repo.

## Layout

Lanes and task IDs are from ROADMAP.md Phase 8. Lane G (Acknowledgements, `CITATION.cff`, the root README)
works outside this folder.

| Folder | What's in it | Built by | Goes to learners? | Lane |
|---|---|---|---|---|
| `slides/` | One Quarto reveal.js deck (`.qmd`, with speaker notes) per session; `slides/rendered/` holds the HTML, PPTX and PDF renders of the decks **and the reading PDFs**, from the "Render slides" workflow | `build-slides` skill | Yes, via Canvas | E |
| `readings/` | Pre- and post-session readings (`.qmd`; rendered to PDF) | `build-slides` skill | Yes, via Canvas | E |
| `learner-bundle/` | Student and solutions notebooks, environment files and a README, for HydroShare | `build-notebooks` skill, `tools/build_notebooks.py` | Yes, via HydroShare | F |
| `learner-bundle/scaffolds/` | Hand-edited "Now you try it" starters that `build_notebooks.py` reads; **source, not generated** | people (lane F drafts them) | Not as files; they become the student notebooks' starter cells | F |
| `quizzes/` | One `text2qti` quiz per module (`.txt`) and its QTI zip for Canvas | `build-quizzes` skill | Yes, via Canvas | H |
| `quizzes/*_key.md` | Answer key and objective coverage per quiz | `build-quizzes` skill | **No**, instructors only | H |
| `instructor-guide/` | Prep material for a new or substitute instructor | `build-instructor-guide` skill | **No**, instructors only | P8.5 |
| `tools/` | `check_stale.py`, `prepare_learner_copy.py` (P8.0); `build_notebooks.py` (lane F) | | No | |
| `manifest.json` | One entry per generated output: its sources and the commit it was built from | `check_stale.py --update` | No | every lane |

Decks are built from learner copies, so their speaker notes follow the learner-facing rules too (no internal
links, no open callouts), and any deck format is safe to share.

## Tools

**`tools/prepare_learner_copy.py`.** Every learner-facing builder starts from this copy of a page. It removes
every `TODO (dev team)` and `Partner review (…)` callout, turns internal course links (other pages, `{term}`,
`{ref}` and `{doc}` roles, the Glossary and References pages, the repo) into plain text, keeps external links
and images, and reports the counts. Put the counts in your PR. If the report ends with
`WARNING: ... flag mention(s) left`, a page names a flag outside a callout (in prose or code): check it by hand
before anything built from it goes to learners.

Run from the repo root. Write learner copies to a scratch directory outside this repo (`<scratch-dir>` below):

```bash
python teaching-materials/tools/prepare_learner_copy.py 03-federal-water-data-access-retrieval/01_access_nasa_swot.md -o <scratch-dir>/01_access_nasa_swot.md
python teaching-materials/tools/prepare_learner_copy.py 03-federal-water-data-access-retrieval/*.md --out-dir <scratch-dir>/learner
```

From Python:

```python
import sys
sys.path.insert(0, "teaching-materials/tools")
from prepare_learner_copy import prepare

page = "03-federal-water-data-access-retrieval/01_access_nasa_swot.md"
text, counts = prepare(open(page, encoding="utf-8").read())
```

**`tools/check_stale.py`.** Lists outputs whose sources changed since they were built (exit code 1 if any).
A `STALE` line names the output; its manifest entry's `builder` says which skill rebuilds it.

To rebuild an output, on your feature branch:

1. Commit the lesson change. Staleness is measured against commits, so uncommitted edits don't count.
2. Run the builder (the skill, or the script).
3. Record the rebuild:
   ```bash
   python teaching-materials/tools/check_stale.py --update teaching-materials/quizzes/module-01_quiz_data-best-practices.txt \
       --kind quiz --builder build-quizzes --source 01-data-best-practices
   ```
4. Commit the output and `manifest.json` together.
5. Run `python teaching-materials/tools/check_stale.py`: the output should no longer be listed.

`--kind` is one of `slides`, `reading`, `notebook`, `environment`, `bundle-readme`, `quiz`,
`instructor-guide` (answer keys use `quiz`). `--kind`, `--builder` and `--source` are needed only for a new entry; `--source` (repeat
it for each path) replaces the recorded sources. Paths are repo-relative. A directory in `sources` (e.g.
`01-data-best-practices` or `images/m03`) covers every file under it.

Renders in `slides/rendered/` have no manifest entries: they follow their `.qmd`, so re-render a deck
whenever its `.qmd` is rebuilt. Recorded commits must stay reachable, so merge PRs with merge commits, not
squash merges; otherwise `check_stale.py` reports the entry's commit as "not in this clone" and it needs
recording again.

Each manifest entry looks like this:

```json
{
  "output": "teaching-materials/slides/session-03_module-03_lesson-01_retrieve-nasa-swot-data.qmd",
  "kind": "slides",
  "sources": ["03-federal-water-data-access-retrieval/00_introduction.md", "03-federal-water-data-access-retrieval/01_access_nasa_swot.md", "images/m03"],
  "source_commit": "<full SHA>",
  "built_at": "2026-10-26T15:02:11Z",
  "builder": "build-slides"
}
```

## Session map

All sessions are in 2026, at 2:00 pm ET. The Dec 1 peer review and Dec 3 demos have no decks. The same map is in
STYLE_GUIDE §11; change both together.

| Session | Date | Length | Covers | Lesson pages |
|---|---|---|---|---|
| 1 | Tue Nov 3 | 90 min | Course welcome, logistics, setup; Module 1 overview + lessons 1–3 | `01-data-best-practices/00`–`03` |
| 2 | Thu Nov 5 | 120 min | Module 2 overview + lessons 1–3 | `02-federal-water-data-landscape/00`–`03` |
| 3 | Tue Nov 10 | 90 min | Module 3 overview + lesson 1 | `03-federal-water-data-access-retrieval/00`, `01` |
| 4 | Thu Nov 12 | 90 min | Module 3 lesson 2 | `03-federal-water-data-access-retrieval/02` |
| 5 | Tue Nov 17 | 90 min | Module 3 lesson 3 | `03-federal-water-data-access-retrieval/03` |
| 6 | Thu Nov 19 | 120 min | Module 4 overview + lessons 1–3 | `04-federal-water-data-synthesis/00`–`03` |

## File names

The naming rule is in STYLE_GUIDE §11: whole words, numbers kept, lowercase with hyphens inside a part and
underscores between parts. **Module slugs** are the module folder names without their number
(`data-best-practices`, `federal-water-data-landscape`, `federal-water-data-access-retrieval`,
`federal-water-data-synthesis`). **Lesson slugs** come from the lesson page's title (its `#` heading),
lowercased, with spaces turned into hyphens and punctuation dropped: *Retrieve NASA SWOT data* →
`retrieve-nasa-swot-data`. A file for a whole module uses `module-NN_<module slug>`; a file for one lesson uses
`module-NN_lesson-NN_<lesson slug>`. One exception: Module 4 lesson 2's title is too long, so its slug is
shortened to `synthesizing-federal-data-products`. So `module-03_lesson-01_retrieve-nasa-swot-data` has three parts:
`module-03` | `lesson-01` | `retrieve-nasa-swot-data`.

### Slides and readings (lane E)

| Session | Deck (`slides/`) |
|---|---|
| 1 | `session-01_module-01_data-best-practices.qmd` |
| 2 | `session-02_module-02_federal-water-data-landscape.qmd` |
| 3 | `session-03_module-03_lesson-01_retrieve-nasa-swot-data.qmd` |
| 4 | `session-04_module-03_lesson-02_retrieve-noaa-nwm-data.qmd` |
| 5 | `session-05_module-03_lesson-03_retrieve-usgs-wdfn-data.qmd` |
| 6 | `session-06_module-04_federal-water-data-synthesis.qmd` |

A reading has its deck's name plus `_pre-reading.qmd` or `_post-reading.qmd`, in `readings/`, e.g.
`readings/session-03_module-03_lesson-01_retrieve-nasa-swot-data_pre-reading.qmd`. Skip a reading when nothing
needs to go in it. Renders keep the same base name (`.html`, `.pptx`, `.pdf`); deck renders and reading PDFs
both land in `slides/rendered/`.

### Learner bundle (lane F)

Notebooks only for lessons with code. Each lesson gets a student notebook, a `_solutions` notebook and an
`_environment.yml` copied from `environments/` (the conda environment *name* inside stays short, e.g. `m03-swot`).

```
learner-bundle/
├── README.md
├── module-03_federal-water-data-access-retrieval/
│   ├── module-03_lesson-01_retrieve-nasa-swot-data.ipynb
│   ├── module-03_lesson-01_retrieve-nasa-swot-data_solutions.ipynb
│   ├── module-03_lesson-01_retrieve-nasa-swot-data_environment.yml        (from environments/m03-swot.yml)
│   ├── module-03_lesson-02_retrieve-noaa-nwm-data[.ipynb | _solutions.ipynb | _environment.yml]   (m03-nwm)
│   └── module-03_lesson-03_retrieve-usgs-wdfn-data[.ipynb | _solutions.ipynb | _environment.yml]  (m03-wdfn)
├── module-04_federal-water-data-synthesis/
│   ├── module-04_lesson-02_synthesizing-federal-data-products[...]  (m04-synthesis)
│   └── module-04_lesson-03_additional-federal-water-data[...]                                     (m04-synthesis)
└── scaffolds/                        hand-edited source, read by build_notebooks.py
    └── <lesson file stem>.yml        e.g. module-03_lesson-01_retrieve-nasa-swot-data.yml
```

Module 4 lesson 1 (*Comparative overview of Federal data products*) has no code, so it has no notebook.
Module 4 lesson 3 has three short code blocks; lane F decides whether they make a useful notebook and says so
in its PR. Modules 1 and 2 have no notebooks (Module 2's short examples are shown on slides).

### Quizzes (lane H)

| Module | Quiz source | QTI zip | Answer key |
|---|---|---|---|
| 1 | `module-01_quiz_data-best-practices.txt` | `.zip` of the same name | `module-01_quiz_data-best-practices_key.md` |
| 2 | `module-02_quiz_federal-water-data-landscape.txt` | ″ | `…_key.md` |
| 3 | `module-03_quiz_federal-water-data-access-retrieval.txt` | ″ | `…_key.md` |
| 4 | `module-04_quiz_federal-water-data-synthesis.txt` | ″ | `…_key.md` |

### Instructor guide (P8.5)

`instructor-guide/00_start-here.md`, `01_prepare-to-teach.md`, `02_how-the-course-is-built.md`, and one
`session-NN_<deck slug>.md` per session using the deck names above without `.qmd`, e.g.
`session-03_module-03_lesson-01_retrieve-nasa-swot-data.md`.

## Learner-facing outputs

Slides, readings, notebooks, the bundle README and quizzes go to pilot learners, who can't open the website or
this repo. They keep external links but have no links into the course and no `TODO (dev team)` or
`Partner review` callouts: build them from `prepare_learner_copy.py` output. The instructor guide is
instructor-facing, so internal links and open callouts are fine there.
