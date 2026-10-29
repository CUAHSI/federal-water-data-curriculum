---
name: build-notebooks
description: Build or rebuild the learner bundle (student and solutions notebooks, environment files and README) for the Module 3 and 4 lessons with code, for HydroShare. Use when asked to make or update notebooks or the learner bundle, or when check_stale.py lists bundle files.
---

# Build the learner bundle

You produce `teaching-materials/materials/learner-bundle/`, the hands-on material pilot learners get on HydroShare.
They can't see the website or the repo, so everything here stands on its own. Read STYLE_GUIDE.md first,
especially §11.

Install papermill and ipykernel into the lesson's conda environment, not into environments/*.yml; see teaching-materials/README.md.

## Layout and names (STYLE_GUIDE §11)

```
teaching-materials/materials/learner-bundle/
├── README.md
├── module-03_federal-water-data-access-retrieval/
│   ├── module-03_lesson-01_retrieve-nasa-swot-data.ipynb
│   ├── module-03_lesson-01_retrieve-nasa-swot-data_solutions.ipynb
│   ├── module-03_lesson-01_retrieve-nasa-swot-data_environment.yml
│   └── … lessons 02 and 03
└── module-04_federal-water-data-synthesis/   same pattern; notebooks only for lessons with code
```

Slugs come from each lesson's title.

## The builder is a script, so rebuilds are repeatable

Write and maintain `teaching-materials/how-to-build/tools/build_notebooks.py` (needs `nbformat`). Don't
hand-write notebooks. For each lesson with code, it:
1. Reads the learner copy of the page (`prepare_learner_copy.py`: no internal callouts, no internal course
   links, external links kept).
2. Makes the notebook:
    - **Cell 1:** the title, the lesson's learning goal, the environment to use and a one-paragraph
      introduction.
    - **Cell 2:** attribution and licence (GPL-3.0; credit the CUAHSI notebooks the lesson adapts).
    - **Cell 3:** a credentials cell for that product: Earthdata Login via `earthaccess.login()`, or the
      `API_USGS_PAT` environment variable. Explain what to set in the hosted environment, and never hard-code
      a secret.
    - **Then the lesson in order:** headings become Markdown headings with the **same text** (slides refer to
      them), prose is condensed to the explanation needed to run and read the code (2–4 sentences per
      block), and every code block becomes a code cell.
    - **Figures:** where the lesson shows a figure, the cell that makes it stays.
    - **"Going further":** rows in the session's topic list (`teaching-materials/how-to-build/topics/`)
      whose "Where" is `notebook` only go in an optional "Going further" section at the end, after "Now you
      try it", with the lesson's own headings and code.
3. **"Now you try it":** the task text becomes a Markdown cell. The solution:
    - **Solutions notebook:** the full solution.
    - **Student notebook:** a starter: the solution as partially completed code, with `...` blanks and
      `# TODO:` hints. Starters are edited by hand directly in the student notebook, and rebuilds keep
      them. A lesson's first build copies the full solution in with a `STARTER TO WRITE` line; turn it into a
      starter: keep the lines learners shouldn't have to retype (imports, plotting boilerplate), blank the
      values and calls that practise the lesson's skill, and delete that line. If a solution changed, check
      that its starter still fits.
4. Copies the lesson's environment from `environments/` to `<lesson>_environment.yml`. Keep the env `name:`.
5. Writes outputs cleared and metadata minimal (kernelspec only), so diffs stay small.

## Test
- Run each **solutions** notebook top to bottom in its environment (`papermill` or
  `jupyter nbconvert --execute`), with the credentials set.
- Run each **student** notebook up to its first "Now you try it" cell.
- Record the runtimes, and any cell that depends on the date (e.g. NWM forecasts are kept about 3 days; SWOT
  passes vary). Put these in the README's "Before you run" section and in the PR.

## README (learner-facing, written for a HydroShare resource)
- What the course and bundle are, and the folder map. Say that the slides and readings come from the sessions
  (via Canvas).
- How to open it in the hosted environment and which environment goes with each notebook.
- Credentials: what to create (Earthdata Login, USGS API token) and how to set them.
- How to use student vs. solutions notebooks.
- The table: file → module/lesson → session → environment → time to run → data or account needed.
- Licence (GPL-3.0), how to cite (from `CITATION.cff`), acknowledgements.
- External links only; nothing to the course website or the repo.

## Record and report
Update `manifest.json` for every output (`check_stale.py --update`). The PR reports:
- the files built
- test results and runtimes
- the callout and internal-link counts per page
- starters created or changed
