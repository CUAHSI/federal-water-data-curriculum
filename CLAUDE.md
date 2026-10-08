# CLAUDE.md — federal-water-data-curriculum

Course content for **"Federal Open Water Data for Researchers"**, a ~20-hour CUAHSI micro-credentialing
course. It is a **MyST Markdown book** (`myst.yml`, `book-theme`) that will later move into CUAHSI's
Water Content Portal. Your job: draft lesson content by following `ROADMAP.md`, adapting the data-access
patterns in CUAHSI's notebooks and the agency resources listed there.

**Schedule:** Phase 6 (consistency and enrichment pass, see `ROADMAP.md`) runs Thu evening 10/8 into
Fri 10/9 while Lindsay is out. Junior reviewers work in the course Fri–Mon. Content sweep 10/13, then partner review.

**Read `STYLE_GUIDE.md` before editing any page.** It is the source of truth for structure, voice, terms,
agency order, environments, figures, flags, citations, the glossary and the course example rivers (§10).

**Lanes:** if your prompt names a lane, work only on that lane's branches, spike subfolder and environment files.
Never edit files another lane owns.

**Working without Lindsay watching:** she may be away from the session. Don't stall on questions — take the most
reasonable reading, note the assumption in your lane report, and keep going. Commit and push your feature
branches as you go and open draft PRs; Lindsay reviews and merges them.

## Scope — what you may edit

| Path | Rule |
|---|---|
| `02-` to `04-` module folders | Full edits per `STYLE_GUIDE.md` and your lane. Colleagues also edit these pages: build on their text and list changed sections in the PR. |
| `glossary.md`, `references.md`, `images/` | Course-wide Glossary, References page, and rendered figures/maps (`images/<module>/`). |
| `01-data-best-practices/` | **Do not edit or propose changes.** Staff are working on it. |
| `environments/` | One file per lesson: `m03-swot.yml`, `m03-nwm.yml`, `m03-wdfn.yml`, `m04-synthesis.yml` (STYLE_GUIDE §5). |
| `myst.yml` | Update the `toc` when adding/renaming pages. |
| `.claude/`, `.github/workflows/` | Don't change unless Lindsay asks. |

Edits to Module 1 are blocked by `.claude/settings.json`; don't try to work around that.

## Content conventions

`STYLE_GUIDE.md` covers structure, voice, terms (WDFN, not NWIS), NASA → NOAA → USGS order, Module 3 lessons
that stand alone, figures, flags and citations. In addition:
- Pages are `.md` with fenced code blocks. Don't convert to `.ipynb` or add `{code-cell}` blocks.
- Preferred tools: NASA SWOT → `earthaccess`, PO.DAAC `hydrocron`; NOAA NWM → `pynhd` (NLDI/COMIDs),
  `hydrotools` (NOAA-OWP); NOAA NWM API (no key) for current forecasts; kerchunk/virtual-Zarr references for
  many-reach work. **Do not recommend the CIROH NWM/BigQuery API** (team decision) — see ROADMAP P1.3; USGS → `dataretrieval` modernized `waterdata`
  module first (legacy `nwis` only for contrast — the source notebook uses legacy, port it).
- Module 4 case study (Module 4 only; never mention it in Module 3): **Skagit River flood, December 2025** (atmospheric river). USGS gage 12200500
  (Skagit River near Mount Vernon, WA). NWM content uses **forecasts**; the observed record comes from USGS.
- Audience: researchers and grad students with some Python, new to these APIs. Explain *why* before
  *how*; small examples; describe what comes back (columns, units, quality flags).
- Open items use the two callout forms in STYLE_GUIDE §7 (`TODO (dev team)` / `Partner review (AGENCY)`).
  Never invent facts, figures or quotes.
- Credentials only from environment variables (`API_USGS_PAT`, `EARTHDATA_USERNAME`/`EARTHDATA_PASSWORD`;
  `earthaccess.login()` picks these up automatically,
  no other keys). Never write real values into any file or print them.

## Source material and attribution

Sources are listed in `ROADMAP.md`. The course repo is **GPL-3.0**, matching CUAHSI/notebooks
(`develop` branch, `Data Access Examples/`), so notebook code may be adapted directly. **Cite and credit
everything you use** — notebooks and agency materials alike:
- Notebook: in the page's "Further reading" — `Adapted from [<title>](<url>) by <authors>, CUAHSI notebooks (GPL-3.0).`
- Agency documentation, tutorials, figures and recommendations: link the source next to the claim it supports,
  and list it in "Further reading". Images: caption with credit and source link, plus alt text.
- Every source must also appear on the course References page (STYLE_GUIDE §8).
Use the `port-notebook` skill. Clone source repos into a scratch directory outside this repo; never commit them.

## Running and checking your work

- **Run every code example you add or change**, in the lesson's environment (`environments/m0*-*.yml`)
  (`conda run -n <env> python <script>`), using scratch scripts outside the course folders.
  In PRs, say which blocks ran (with package versions) and which couldn't, and why.
- Build: `myst build --html` — a page that breaks the build is not done.
- Links: `python3 .claude/scripts/check_links.py --changed`.
- **Before opening a PR, run the `content-reviewer` and `learner-reviewer` subagents** and fix every "Must fix"
  and "Blocker" item. Put both summary lines in the PR description.

## Git workflow — hard rules

Enforced by `.claude/settings.json` and `.claude/hooks/git_guard.py`; follow them anyway.

1. **Remotes (fork-and-pull):** `upstream` = CUAHSI/federal-water-data-curriculum (canonical; branches and PRs go here),
   `origin` = Lindsay's fork (don't use it). Integration branch is **`upstream/dev`**. Branch from it:
   `git fetch upstream && git switch -c <type>/<module>-<topic> upstream/dev` (e.g. `content/04-synthesis`).
   Push with `git push -u upstream <branch>`; open PRs with `gh pr create --repo CUAHSI/federal-water-data-curriculum --base dev --head <branch>`.
   Always pass `--repo CUAHSI/federal-water-data-curriculum` to `gh pr`/`gh issue` commands. If `gh` isn't
   available, follow the browser fallback in the `open-pr` skill (and write issue text to a file for Lindsay).
2. **Never commit to, or push to, `main` or `dev`.**
3. **Commit and push your own feature branches without asking** (small, descriptive commits). Branch names
   must be `<type>/<topic>` with type `content`, `chore`, `env`, `fix` or `docs`; always push with the remote
   and branch named: `git push -u upstream <branch>`. The guard blocks anything else.
4. **Open draft PRs against `dev` yourself** when a task is done and reviewed
   (`gh pr create --repo CUAHSI/federal-water-data-curriculum --draft --base dev ...`), using the `open-pr` skill.
   Never mark a PR ready or change its base. Lindsay reviews and merges every PR.
5. **Never merge a PR**, approve one, enable auto-merge, force-push, or delete branches.
6. One roadmap task (or a clear slice of one) per branch/PR.

## Working from the roadmap

- Start each session: read `ROADMAP.md`, run the `roadmap-status` skill, state the next task in a few lines.
- Work through your lane's tasks in order and finish with a lane report (what changed per page, what ran,
  open callouts, decisions you made for Lindsay).
- **Don't edit `ROADMAP.md` on lane branches** (parallel lanes would conflict). List the task IDs you completed
  in the PR description; Lindsay ticks the boxes.
- If something is ambiguous or a data source doesn't work, say so early — the deadline is tight.
