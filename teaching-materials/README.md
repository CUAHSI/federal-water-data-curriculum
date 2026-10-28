# Teaching materials

Everything needed to *run* *Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access*: session slides, module readings, the learner bundle for HydroShare, the module quizzes and the instructor guide. These files are
generated from the lesson pages (`0*/`), which stay the single source of truth. To fix content, edit the
lesson, then rebuild. This folder isn't part of the website build (`myst.yml` excludes it).

## Two folders: what you use, and how it's made

```
teaching-materials/
├── materials/       WHAT YOU USE: the finished materials for learners and instructors
│   ├── slides/              session decks (PowerPoint; local only, never committed)
│   ├── readings/            module readings (Word and PDF; local only, never committed)
│   ├── learner-bundle/      notebooks and environments for HydroShare
│   ├── quizzes/             Canvas quizzes and answer keys (local only, never committed)
│   └── instructor-guide/    prep for a new or substitute instructor
└── how-to-build/    HOW IT'S MADE: instructions, prompts, templates and tools
    ├── guide.md             start here to build or update slides and readings
    ├── topics/              what goes on each session's deck, notebook or reading
    ├── *-prompt.md          the prompts Claude follows
    ├── design-rules.md, review-checklist.md
    ├── scaffolds/           hand-edited "Now you try it" starters for the notebooks
    ├── tools/               scripts (check_stale, check_topics, prepare_learner_copy, build_notebooks)
    ├── manifest.json        what each committed output was built from
    ├── templates/           the deck template (committed); reading template, example decks (local only)
    └── to-update/           existing decks or readings to update (local only)
```

If you want to **teach**, look in `materials/`. If you want to **change or rebuild** something, start in
`how-to-build/`. Nothing in `how-to-build/` goes to learners.

The rules (names, the session map, learner-facing outputs, live coding, quizzes) are in
[STYLE_GUIDE §11](../STYLE_GUIDE.md#11-teaching-materials). This README records the names the Phase 8 lanes
build to, so they agree before they start.

## How outputs are built

Most outputs are written by a Claude Code agent following a **skill**: a set of instructions in
`.claude/skills/<name>/SKILL.md` (`build-slides`, `build-notebooks`, `build-quizzes`, `build-instructor-guide`).
"Rebuild" means asking an agent to run that skill again. A person can do the same work by hand by following
the skill's steps. Only some steps are plain scripts you run yourself:

- `how-to-build/tools/prepare_learner_copy.py` and `how-to-build/tools/check_stale.py` (standard library only, any Python 3.9 or later; no
  conda environment needed);
- `how-to-build/tools/build_notebooks.py` (lane F; needs `nbformat` and `pyyaml`);
- `how-to-build/tools/check_topics.py`, which checks the session topic lists in `how-to-build/topics/`;
- quizzes: `text2qti <file>.txt` makes the QTI zip.

Small hand fixes to an output (a typo on a slide) are fine, but make the same fix in the lesson page too, or
the next rebuild undoes it.

## Before you rebuild

Some builders need tools that the lesson environments don't include. Set them up once per machine. Run the
commands below in Git Bash (see [AGENT_SETUP.md](../AGENT_SETUP.md)).

| Skill | Needs | Used for |
|---|---|---|
| `build-slides` | Your template and example decks in `how-to-build/templates/` (see `how-to-build/guide.md`); `python-pptx` in any scratch Python; `python-docx` too, for readings; PowerPoint and Word (or LibreOffice) to export slides and readings to PDF for checking | writing and checking decks and readings |
| `build-notebooks` | `papermill` in **each** lesson environment; `nbformat` and `pyyaml` in the Python that runs `how-to-build/tools/build_notebooks.py` (lane F writes it) | running every notebook top to bottom to test it. The skill also allows `jupyter nbconvert --execute`; this course uses papermill |
| `build-quizzes` | [`text2qti`](https://pypi.org/project/text2qti/) | turning each quiz `.txt` into a QTI zip for Canvas |
| `build-instructor-guide` | nothing extra | |

### Lesson environments and papermill

The `environments/*.yml` files are the recipes learners build their environments from, and they're copied
into the learner bundle. Your installed environments are your own copies built from those recipes. Add
testing tools to your copies only, never to the `.yml` files.

1. **Make sure your environments match the recipes.** Create any that are missing, and update any built from
   an older `.yml`:
   ```bash
   conda env create -f environments/m03-swot.yml          # if m03-swot doesn't exist yet
   conda env update -n m03-swot -f environments/m03-swot.yml --prune   # if it exists but may be out of date
   ```
   Do the same for `m03-nwm`, `m03-wdfn` and `m04-synthesis`. (`conda env list` shows which you have.) `--prune` removes packages the `.yml` doesn't list, papermill
   included, so repeat step 2 whenever you repeat step 1.
2. **Add papermill and ipykernel without changing anything else.** `--freeze-installed` stops conda from
   upgrading or downgrading the packages already installed, so your environment keeps the learners'
   versions. (conda still refreshes `ca-certificates` and `certifi`; that's expected and harmless.) `ipykernel` is already in every `.yml`; listing it again does nothing if it's there.
   ```bash
   for e in m03-swot m03-nwm m03-wdfn m04-synthesis; do
     conda install -y -n "$e" -c conda-forge --freeze-installed papermill ipykernel
   done
   for e in m03-swot m03-nwm m03-wdfn m04-synthesis; do conda run -n "$e" papermill --version; done
   ```
   If conda says it can't install without changing other packages, stop and ask: don't remove the flag.
3. **Run each notebook inside its lesson's environment, with that environment's kernel**, so it's tested
   with the learners' packages:
   ```bash
   conda run -n m03-swot papermill -k python3 <notebook>.ipynb <scratch-dir>/<notebook>_out.ipynb
   ```

The notebooks don't import papermill, so a notebook that runs in your environment also runs in the
learners' environment, as long as your environment matches the `.yml` (step 1).

### text2qti, nbformat and pyyaml

Install these into any Python on your PATH (conda `base` is fine): `pip install text2qti nbformat pyyaml`.
Check with `text2qti --version` in the shell you'll build in.

### Credentials

Testing notebooks logs in to real services. The process running the builder needs these environment
variables set:

| Notebooks | Needs |
|---|---|
| Module 3 lesson 1 (SWOT), Module 4 lessons 2 and 3 | `EARTHDATA_USERNAME`, `EARTHDATA_PASSWORD` (read by `earthaccess.login()`) |
| Module 3 lesson 3 (WDFN), Module 4 lesson 2 | `API_USGS_PAT` (read by `dataretrieval`) |
| Module 3 lesson 2 (NWM) | nothing |

Save them once as Windows user environment variables, following
[AGENT_SETUP.md, "Windows: credentials"](../AGENT_SETUP.md#windows-credentials), which also shows how to
check them without printing the values. A program only sees environment variables that existed when it
started. After saving or changing them, close your terminals (and VS Code, if you use it), open a new
terminal, and start Claude Code from there. Never write the values into a file in this repo.

## Layout

Lanes and task IDs are from ROADMAP.md Phase 8. Lane G (Acknowledgements, `CITATION.cff`, the root README)
works outside this folder.

**`materials/`: what you use**

| Folder | What's in it | Built by | Goes to learners? | Lane |
|---|---|---|---|---|
| `materials/slides/` | One PowerPoint deck (`.pptx`, with speaker notes) per session, built from its topic list. **Git-ignored: decks are built locally and never committed**, and aren't in `manifest.json` | `build-slides` skill, from `how-to-build/` | Yes, via Canvas | E |
| `materials/readings/` | At most one reading per module for Modules 2–4 (a Word document, exported to PDF). **Git-ignored: readings are built locally and never committed**, and aren't in `manifest.json` | `build-slides` skill, from `how-to-build/` | Yes, via Canvas | E |
| `materials/learner-bundle/` | Student and solutions notebooks, environment files and a README, for HydroShare | `build-notebooks` skill, `how-to-build/tools/build_notebooks.py` | Yes, via HydroShare | F |
| `materials/quizzes/` | One `text2qti` quiz per module (`.txt`) and its QTI zip for Canvas. **Git-ignored: quizzes are built locally and never committed**, and aren't in `manifest.json`. Kept with their keys in a private course folder and loaded into Canvas | `build-quizzes` skill | Yes, via Canvas | H |
| `materials/quizzes/*_key.md` | Answer key and objective coverage per quiz, with the commit it was built from. **Git-ignored**, like the quizzes | `build-quizzes` skill | **No**, instructors only | H |
| `materials/instructor-guide/` | Prep material for a new or substitute instructor | `build-instructor-guide` skill | **No**, instructors only | P8.5 |

**`how-to-build/`: how it's made** (nothing here goes to learners)

| Folder or file | What's in it | Who edits it | Lane |
|---|---|---|---|
| `how-to-build/guide.md`, `*-prompt.md`, `design-rules.md`, `review-checklist.md` | How to build and update decks and readings, the prompts Claude follows, the look, and the review checklist | people | E |
| `how-to-build/topics/` | One topic list per session: what goes on the deck, in a notebook, in a reading or nowhere | people | E |
| `how-to-build/scaffolds/` | Hand-edited "Now you try it" starters (`<lesson file stem>.yml`) that `build_notebooks.py` turns into the student notebooks' starter cells | people (lane F drafts them) | F |
| `how-to-build/templates/template.pptx` | The course deck template: one example slide per slide type, copied by every deck build. **Committed** | people | E |
| `how-to-build/templates/` (everything else), `how-to-build/to-update/` | The reading template, example decks, and existing decks or readings to update. **Local only:** git-ignored, never committed | people | E |
| `how-to-build/tools/` | `check_stale.py`, `prepare_learner_copy.py` (P8.0); `check_topics.py` (lane E); `build_notebooks.py` (lane F) | people | all |
| `how-to-build/manifest.json` | One entry per committed output: its sources and the commit it was built from | `check_stale.py --update` | every lane |

Decks are built from learner copies, so their speaker notes follow the learner-facing rules too (no internal
links, no open callouts), and any deck format is safe to share.

## Tools

**`how-to-build/tools/prepare_learner_copy.py`.** Every learner-facing builder starts from this copy of a page. It removes
every `TODO (dev team)` and `Partner review (…)` callout, turns internal course links (other pages, `{term}`,
`{ref}` and `{doc}` roles, the Glossary and References pages, the repo) into plain text, keeps external links
and images, and reports the counts. Put the counts in your PR. If the report ends with
`WARNING: ... flag mention(s) left`, a page names a flag outside a callout (in prose or code): check it by hand
before anything built from it goes to learners.

Run from the repo root. Write learner copies to a scratch directory outside this repo (`<scratch-dir>` below):

```bash
python teaching-materials/how-to-build/tools/prepare_learner_copy.py 03-federal-water-data-access-retrieval/01_access_nasa_swot.md -o <scratch-dir>/01_access_nasa_swot.md
python teaching-materials/how-to-build/tools/prepare_learner_copy.py 03-federal-water-data-access-retrieval/*.md --out-dir <scratch-dir>/learner
```

From Python:

```python
import sys
sys.path.insert(0, "teaching-materials/how-to-build/tools")
from prepare_learner_copy import prepare

page = "03-federal-water-data-access-retrieval/01_access_nasa_swot.md"
text, counts = prepare(open(page, encoding="utf-8").read())
```

**`how-to-build/tools/check_stale.py`.** Lists outputs whose sources changed since they were built (exit code 1 if any).
A `STALE` line names the output; its manifest entry's `builder` says which skill rebuilds it.

To rebuild an output, on your feature branch (slides, readings and quizzes are local only: skip steps 3–5 and
record the build commit in the file itself, for a quiz in its answer key):

1. Commit the lesson change. Staleness is measured against commits, so uncommitted edits don't count.
2. Run the builder (the skill, or the script).
3. Record the rebuild:
   ```bash
   python teaching-materials/how-to-build/tools/check_stale.py --update teaching-materials/materials/learner-bundle/README.md \
       --kind bundle-readme --builder build-notebooks --source 03-federal-water-data-access-retrieval
   ```
4. Commit the output and `manifest.json` together.
5. Run `python teaching-materials/how-to-build/tools/check_stale.py`: the output should no longer be listed.

`--kind` is one of `notebook`, `environment`, `bundle-readme` or `instructor-guide` (`slides`, `reading` and
`quiz` are still accepted, but those outputs are local only and never recorded). `--kind`, `--builder` and `--source` are needed only for a new entry; `--source` (repeat
it for each path) replaces the recorded sources. Paths are repo-relative. A directory in `sources` (e.g.
`01-data-best-practices` or `images/m03`) covers every file under it.

Recorded commits must stay reachable, so merge PRs with merge commits, not
squash merges; otherwise `check_stale.py` reports the entry's commit as "not in this clone" and it needs
recording again.

Each manifest entry looks like this:

```json
{
  "output": "teaching-materials/materials/learner-bundle/README.md",
  "kind": "bundle-readme",
  "sources": ["03-federal-water-data-access-retrieval"],
  "source_commit": "<full SHA>",
  "built_at": "2026-10-26T15:02:11Z",
  "builder": "build-notebooks"
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

| Session | Deck (`materials/slides/`) |
|---|---|
| 1 | `session-01_module-01_data-best-practices.pptx` |
| 2 | `session-02_module-02_federal-water-data-landscape.pptx` |
| 3 | `session-03_module-03_lesson-01_retrieve-nasa-swot-data.pptx` |
| 4 | `session-04_module-03_lesson-02_retrieve-noaa-nwm-data.pptx` |
| 5 | `session-05_module-03_lesson-03_retrieve-usgs-wdfn-data.pptx` |
| 6 | `session-06_module-04_federal-water-data-synthesis.pptx` |

Readings are per module, for Modules 2–4 only, named `module-NN_reading_<module slug>.docx`:

| Module | Reading (`materials/readings/`) | From the `reading` rows of |
|---|---|---|
| 2 | `module-02_reading_federal-water-data-landscape.docx` | session 2 |
| 3 | `module-03_reading_federal-water-data-access-retrieval.docx` | sessions 3–5 |
| 4 | `module-04_reading_federal-water-data-synthesis.docx` | session 6 |

Skip a reading when its topic lists have no `reading` rows. Its PDF keeps the same base name, next to it in
`materials/readings/`. Both are local only (see `how-to-build/guide.md`).

### Learner bundle (lane F)

Notebooks only for lessons with code. Each lesson gets a student notebook, a `_solutions` notebook and an
`_environment.yml` copied from `environments/` (the conda environment *name* inside stays short, e.g. `m03-swot`).

```
materials/learner-bundle/
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
```

The hand-edited "Now you try it" starters are build instructions, not outputs, so they live in
`how-to-build/scaffolds/<lesson file stem>.yml` (e.g. `module-03_lesson-01_retrieve-nasa-swot-data.yml`).

Module 4 lesson 1 (*Comparative overview of Federal data products*) has no code, so it has no notebook.
Module 4 lesson 3 has three short code blocks; lane F decides whether they make a useful notebook and says so
in its PR. Modules 1 and 2 have no notebooks (Module 2's short examples are shown on slides).

### Quizzes (lane H)

Local only (git-ignored) and never committed: see the `build-quizzes` skill for handover and Canvas setup.

| Module | Quiz source | QTI zip | Answer key |
|---|---|---|---|
| 1 | `module-01_quiz_data-best-practices.txt` | `.zip` of the same name | `module-01_quiz_data-best-practices_key.md` |
| 2 | `module-02_quiz_federal-water-data-landscape.txt` | ″ | `…_key.md` |
| 3 | `module-03_quiz_federal-water-data-access-retrieval.txt` | ″ | `…_key.md` |
| 4 | `module-04_quiz_federal-water-data-synthesis.txt` | ″ | `…_key.md` |

### Instructor guide (P8.5)

`materials/instructor-guide/00_start-here.md`, `01_prepare-to-teach.md`, `02_how-the-course-is-built.md`, and one
`session-NN_<deck slug>.md` per session using the deck names above without `.pptx`, e.g.
`session-03_module-03_lesson-01_retrieve-nasa-swot-data.md`.

## Learner-facing outputs

Slides, readings, notebooks, the bundle README and quizzes go to pilot learners, who can't open the website or
this repo. They keep external links but have no links into the course and no `TODO (dev team)` or
`Partner review` callouts: build them from `prepare_learner_copy.py` output. The instructor guide is
instructor-facing, so internal links and open callouts are fine there.
