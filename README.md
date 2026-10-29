![Static Badge](https://img.shields.io/badge/course_status-under_development-%23fcc200?style=for-the-badge)

# Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access

This repo holds the course materials for *Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access*, a micro-credentialing course (about 20 hours) from CUAHSI (the Consortium of Universities for the Advancement of Hydrologic Science, Inc.). Researchers and graduate students with some Python experience learn to build reproducible workflows that find, retrieve and combine federal open water data: NASA SWOT, the NOAA National Water Model (NWM) and USGS Water Data for the Nation (WDFN). The course is designed to be modular with the goal to support additions or adjustments to the datasets included.

**Want to read the course?** Start at the draft site, <https://cuahsi.github.io/federal-water-data-curriculum/>. The rest of this README is for people who build and maintain the course.

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

`teaching-materials/` holds what's needed to *run* the course. It isn't part of the website. It has two
folders:

- **`materials/`: what learners and instructors use.**
  - `slides/`: one PowerPoint deck per session, with speaker notes
  - `notebooks/`: one notebook per lesson with code, plus one conda environment file for all of them, for HydroShare
  - `readings/`: readings to cover details the sessions don't cover (Word, exported to PDF)
  - `quizzes/`: one quiz per module, as `text2qti` text plus a QTI zip for Canvas, with answer keys for
    instructors
  - `instructor-guide/`: prep material for a new or substitute instructor

  Everything but the instructor guide is built locally and shared through Canvas or HydroShare. It's
  git-ignored and never committed.
- **`how-to-build/`: how the materials are made.** The guide (`guide.md`), the per-session topic lists, the
  prompts, design rules and review checklist, the deck template and the tools. Nothing in it goes to learners.

Everything in `materials/` is generated from the lesson pages. To change content, edit the lesson, then
update the materials.

### How to rebuild

The builders are [Claude Code](https://claude.com/claude-code) skills in `.claude/skills/`, run in this order:
decks (`/build-slides N`), the session's notebooks (`/build-notebooks N`, written around the deck), readings
(`/build-slides reading M`), quizzes (`/build-quizzes`) and the instructor guide (`/build-instructor-guide`).
[`teaching-materials/how-to-build/guide.md`](teaching-materials/how-to-build/guide.md) explains the setup each
needs, how to run the same prompts in Claude on the web or desktop, the session map and the file names.
[`AGENT_SETUP.md`](AGENT_SETUP.md) explains how to set up Claude Code for this repo.

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

The course is licensed under the [GNU General Public License v3.0](LICENSE) (SPDX: `GPL-3.0-only`), the same license as the
[CUAHSI notebooks](https://github.com/CUAHSI/notebooks) it adapts code from. Each lesson credits its sources,
and the References page lists them all. Contributors, the agency sources the course relies on most, funding and the use of AI tools are
described on the Acknowledgements page. Both are on the [course site](https://cuahsi.github.io/federal-water-data-curriculum/)
(sources: [`references.md`](references.md), [`acknowledgements.md`](acknowledgements.md)).

To cite the course, use [`CITATION.cff`](CITATION.cff) (on GitHub, **Cite this repository** in the sidebar
formats it as APA or BibTeX).
