![Static Badge](https://img.shields.io/badge/course_status-under_development-%23fcc200?style=for-the-badge)

# Federal Open Water Data for Researchers

This repo holds the course materials for *Federal Open Water Data for Researchers*, a micro-credentialing
course from CUAHSI (the Consortium of Universities for the Advancement of Hydrologic Science, Inc.) (about 20 hours). Researchers and graduate students with some Python learn to
find, retrieve and combine federal open water data: NASA SWOT, the NOAA National Water Model (NWM) and
USGS Water Data for the Nation (WDFN). The course will later move into
[CUAHSI's Water Content Portal](https://water-content-portal.cuahsi.io/).

**Want to read the course?** Start at the draft site,
<https://cuahsi.github.io/federal-water-data-curriculum/>. The rest of this README is for people who build and
maintain the course.

The repo has two parts: **the website** (the lessons, which are the source of truth) and **the teaching
materials** generated from it.

## The website

The lessons are [MyST](https://mystmd.org/) Markdown pages, organized by module:

| Folder | Module |
|---|---|
| `01-data-best-practices/` | 1 · Data best practices in water research |
| `02-federal-water-data-landscape/` | 2 · Federal water data landscape |
| `03-federal-water-data-access-retrieval/` | 3 · Federal water data access and retrieval (one stand-alone lesson per agency) |
| `04-federal-water-data-synthesis/` | 4 · Federal water data synthesis |

Also part of the site: `index.md` (the home page), `glossary.md`, `references.md`, `acknowledgements.md` and
`images/` (figures and maps, one folder per module). `myst.yml` sets the table of contents.

Each Module 3 lesson has its own conda environment in `environments/`, and the Module 4 lessons share one
(`m04-synthesis.yml`). The "Tools and environment setup" section of each Module 3 lesson shows how to create
the environment (`conda env create -f environments/<file>.yml`) and which free accounts the lesson needs (a
NASA Earthdata Login for SWOT; an optional but recommended USGS API key for WDFN).

Every push to `dev` builds the site and publishes a draft preview to GitHub Pages:
<https://cuahsi.github.io/federal-water-data-curriculum/>.

### Build the site locally

You need Node.js (20 or later) and npm. Install MyST once:

```bash
npm install -g mystmd
```

Then, from the repo root, build and serve the site at <http://localhost:3000>:

```bash
myst start
```

`myst build --html` does a one-off build, the same one the PR checks run.

## Teaching materials

`teaching-materials/` holds what's needed to *run* the course. It isn't part of the website:

- `slides/`: one Quarto reveal.js deck per session, with speaker notes (`slides/rendered/` holds the HTML,
  PPTX and PDF renders, plus the reading PDFs)
- `readings/`: pre- and post-session readings for the content the session time can't cover
- `learner-bundle/`: student and solutions notebooks, environment files and a README, for HydroShare
- `quizzes/`: one quiz per module, as `text2qti` text plus a QTI zip for Canvas
- `instructor-guide/`: prep material for a new or substitute instructor

These files are generated from the lesson pages. To change content, edit the lesson, then rebuild.
[`teaching-materials/README.md`](teaching-materials/README.md) explains the session map, the file names, the
setup each builder needs, and the tools.

### How to rebuild

- **Regenerate content** with the [Claude Code](https://claude.com/claude-code) skills in `.claude/skills/`: `build-slides`, `build-notebooks`,
  `build-quizzes` and `build-instructor-guide`. Ask an agent to run the skill, or follow its `SKILL.md` steps
  by hand. [`AGENT_SETUP.md`](AGENT_SETUP.md) explains how to set up Claude Code for this repo.
- **Render the slides and readings** with the "Render slides" action (**Actions → Render slides → Run
  workflow**). It can open a draft PR with the rendered files. To render locally, run `quarto render` on a
  deck or reading (needs [Quarto](https://quarto.org/docs/get-started/)).
- **Rebuild a quiz's QTI zip** with `text2qti <file>.txt` (`pip install text2qti`).
- **Find stale outputs** (outputs whose lesson pages changed since they were built):

  ```bash
  python teaching-materials/tools/check_stale.py
  ```

## Contributing

We use a fork-and-pull workflow, and `dev` is the integration branch:

1. Fork the repo, then create a branch from `dev` named `<type>/<topic>`, where type is `content`, `chore`,
   `env`, `fix` or `docs` (for example, `content/04-synthesis`).
2. Read [`STYLE_GUIDE.md`](STYLE_GUIDE.md) before editing a page. Run every code example you add in its
   lesson's environment, and check that `myst build --html` succeeds.
3. Open a pull request into `dev`. The PR checks build the site and check the links on the pages you changed.

Course planning lives in [`ROADMAP.md`](ROADMAP.md). Contributors working with Claude Code should also read
[`CLAUDE.md`](CLAUDE.md) and [`AGENT_SETUP.md`](AGENT_SETUP.md).

## License and how to cite

The course is licensed under GPL-3.0, matching the
[CUAHSI notebooks](https://github.com/CUAHSI/notebooks) it adapts code from. Each lesson credits its sources,
and the References page lists them all. Contributors, funding and the use of AI tools are described on the
Acknowledgements page. Both are on the [course site](https://cuahsi.github.io/federal-water-data-curriculum/)
(sources: [`references.md`](references.md), [`acknowledgements.md`](acknowledgements.md)).

To cite the course, use [`CITATION.cff`](CITATION.cff) (on GitHub, **Cite this repository** in the sidebar
formats it as APA or BibTeX).
