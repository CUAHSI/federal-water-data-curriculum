# CLAUDE.md — federal-water-data-curriculum

Course content for **"Federal Open Water Data for Researchers"**, a ~20-hour CUAHSI micro-credentialing
course. It is a **MyST Markdown book** (`myst.yml`, `book-theme`) that will later move into CUAHSI's
Water Content Portal. Your job: draft lesson content by following `ROADMAP.md`, adapting the data-access
patterns in CUAHSI's notebooks and the agency resources listed there.

**Schedule:** rough cut of Modules 3–4 today (Wed 10/7) in three parallel sessions ("lanes" in `ROADMAP.md`);
review and polish with Lindsay Thu 10/8; Lindsay out Fri; first cut due Mon 10/12.

**Rough-cut standard (today):** every section drafted, every code block runs, sources credited, links resolve,
build passes. Don't polish prose, add optional figures or chase edge cases — mark them `[POLISH: ...]` and move on.

**Lanes:** if your prompt names a lane, work only on that lane's branches, spike subfolder and environment files.
Never edit files another lane owns.

**Working without Lindsay watching:** she may be away from the session. Don't stall on questions — take the most
reasonable reading, note the assumption in your lane report, and keep going. Commit locally on feature
branches as you go; leave pushes and PRs as requests for Lindsay to approve.

## Scope — what you may edit

| Path | Rule |
|---|---|
| `04-federal-water-data-synthesis/` | **Work here first.** Full edits. |
| `03-federal-water-data-access-retrieval/` | Draft after Module 4 (ROADMAP Phase 4). Colleagues recently filled in parts of these pages: build on their text, keep edits focused, list changed sections in the PR. |
| `02-federal-water-data-landscape/` | **Do not edit.** Draft suggested changes as issue text (ROADMAP P4.4). |
| `01-data-best-practices/` | **Do not edit or propose changes.** Staff are working on it. |
| `environments/` | Conda env files: one per agency lesson (`swot.yml`, `nwm.yml`, `nwis.yml`) + `synthesis.yml` for Module 4. |
| `myst.yml` | Update the `toc` when adding/renaming pages. |
| `.claude/`, `.github/workflows/` | Don't change unless Lindsay asks. |

Edits to Modules 1 and 2 are blocked by `.claude/settings.json`; don't try to work around that.

## Content conventions

- Pages are `.md` with fenced ```` ```python ```` / ```` ```bash ```` blocks. Don't convert to `.ipynb` or
  add `{code-cell}` blocks (runnable notebooks may come later, on request).
- Module 3 agency pages keep the skeleton: intro + recommended tools → **Tools and environment setup** →
  **Programmatic data discovery** (GUI equivalent, then code) → **Programmatic data downloads** → further reading.
- Shared vocabulary across agencies (from Module 2): *Location Identifier, Variable, Variable unit,
  Data Quality Flag(s)*. Use these terms.
- Preferred tools: NASA SWOT → `earthaccess`, PO.DAAC `hydrocron`; NOAA NWM → `pynhd` (NLDI/COMIDs),
  `hydrotools` (NOAA-OWP); NOAA NWM API (no key) for current forecasts; kerchunk/virtual-Zarr references for
  many-reach work. **Do not recommend the CIROH NWM/BigQuery API** (team decision) — see ROADMAP P1.3; USGS → `dataretrieval` modernized `waterdata`
  module first (legacy `nwis` only for contrast — the source notebook uses legacy, port it).
- Module 4 case study: **Skagit River flood, December 2025** (atmospheric river). USGS gage 12200500
  (Skagit River near Mount Vernon, WA). NWM content uses **forecasts**; the observed record comes from USGS.
- Audience: researchers and grad students with some Python, new to these APIs. Explain *why* before
  *how*; small examples; describe what comes back (columns, units, quality flags).
- Content that agencies must confirm gets `[PARTNER REVIEW: NASA|NOAA|USGS] <what to check>`.
  Anything you couldn't verify gets `[TODO: verify ...]`. Never invent facts, figures or quotes.
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
- Keep a running list for the "Sources and credits" page (ROADMAP L1).
Use the `port-notebook` skill. Clone source repos into a scratch directory outside this repo; never commit them.

## Running and checking your work

- **Run every code example you add or change**, in the matching `environments/*.yml` env
  (`conda run -n <env> python <script>`), using scratch scripts outside the course folders.
  In PRs, say which blocks ran (with package versions) and which couldn't, and why.
- Build: `myst build --html` — a page that breaks the build is not done.
- Links: `python3 .claude/scripts/check_links.py --changed`.
- **Before asking to push, run the `content-reviewer` subagent** and fix every "Must fix" item.
  Include its summary line in your push/PR request.

## Git workflow — hard rules

Enforced by `.claude/settings.json` and `.claude/hooks/git_guard.py`; follow them anyway.

1. **Remotes (fork-and-pull):** `upstream` = CUAHSI/federal-water-data-curriculum (canonical; branches and PRs go here),
   `origin` = Lindsay's fork (don't use it). Integration branch is **`upstream/dev`**. Branch from it:
   `git fetch upstream && git switch -c <type>/<module>-<topic> upstream/dev` (e.g. `content/04-synthesis`).
   Push with `git push -u upstream <branch>`; open PRs with `gh pr create --repo CUAHSI/federal-water-data-curriculum --base dev --head <branch>`.
   Always pass `--repo CUAHSI/federal-water-data-curriculum` to `gh pr`/`gh issue` commands. If `gh` isn't
   available, follow the browser fallback in the `open-pr` skill (and write issue text to a file for Lindsay).
2. **Never commit to, or push to, `main` or `dev`.**
3. **Commit freely on feature branches** (small, descriptive commits). **Ask before every push**: name the
   branch and summarize what it contains; wait for an explicit yes.
4. **Open PRs as drafts against `dev` in CUAHSI/federal-water-data-curriculum** (`gh pr create --repo CUAHSI/federal-water-data-curriculum --draft --base dev`), only after approval.
   Use the `open-pr` skill.
5. **Never merge a PR**, approve one, enable auto-merge, force-push, or delete branches.
6. One roadmap task (or a clear slice of one) per branch/PR.

## Working from the roadmap

- Start each session: read `ROADMAP.md`, run the `roadmap-status` skill, state the next task in a few lines.
- Work through your lane's tasks in order and finish with the lane report (ROADMAP P5.2).
- When a task is done, tick its box in `ROADMAP.md` on the same branch with the PR link; record any
  decision Lindsay makes in the Decisions log.
- If something is ambiguous or a data source doesn't work, say so early — the deadline is tight.
