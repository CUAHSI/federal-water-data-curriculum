# Roadmap — Federal Open Water Data for Researchers

**Goal:** rough cut of Modules 3–4 **today (Wed 10/7)** across three parallel sessions; review, PRs and polish
with Lindsay **Thu 10/8**; Lindsay out Fri; Sat–Mon buffer before the 10/13 sweep and partner review.

**Order:** Module 4 → Module 3 (rough cuts drafted today, in parallel). Module 2: suggestions only. **Module 1 off-limits.**

**Branching:** fork-and-pull setup — `upstream` = CUAHSI repo, `origin` = Lindsay's fork. One feature branch per PR,
cut from `upstream/dev`, pushed to **`upstream`** with a PR into `upstream`'s `dev`. The agent commits locally on feature
branches without asking; **pushing and opening PRs require Lindsay's approval**. PRs target `dev`; only
Lindsay merges. GitHub Pages builds from `dev`, labelled as a draft.

---

## Schedule — rough cut today, polish later

Start now; no need to wait for night. **Rough cut** = every section drafted, every code block runs, sources
credited, links resolve. Prose polish, figures beyond the essentials, and `[TODO]`/`[PARTNER REVIEW]` items
come later.

Three Claude Code sessions run **in parallel**, each in its own git worktree, so they never touch the same
files or branches:

| Lane | Branches (PR #) | Work | Depends on |
|---|---|---|---|
| **A — NWM** | `content/03-nwm-access-routes` (#4) | P1.3 access-route measurements → P4.1 NWM page; owns `environments/nwm.yml` | — |
| **B — Synthesis** | `content/04-synthesis` (#1) | P1.1 USGS + P1.2 SWOT spikes → P3.1 page 04/02; owns `environments/synthesis.yml`. Write the NWM section last, using Lane A's numbers (read `spike/nwm/REPORT.md`); if not ready, leave a clearly marked stub | Lane A for the NWM section only |
| **C — Pages** | `content/03-swot-raster` (#5), `content/03-nwis-overview` (#6), `content/04-comparative-overview` (#2), `content/04-overview-additional` (#3) | P4.2, P4.3, P3.2, P3.3, P4.4 issue text; owns `environments/swot.yml`, `nwis.yml` | Lane B's SWOT spike for the Raster example (or run its own small one) |

| When | What |
|---|---|
| Wed ~14:30 | Setup (≈20 min), then start lanes A, B, C |
| Wed afternoon | Each lane posts its rough cut when done; Lindsay skims and answers questions as they come up. Typical: page drafting is fast; the slow parts are environment solves and data downloads (NWM files are large) |
| Thu (with Lindsay) | Approve pushes → draft PRs; review and revise; merge to `dev`; preview site live. Then polish pass |
| Fri (Lindsay out) | One unattended session: full `content-reviewer` pass + execute every example on `dev`; fixes on local branches, report for Saturday |
| Sat–Mon | Buffer before the 10/13 sweep |

Lanes share one `spike/` folder outside the repo (e.g. `~/fwdc-spike/{nwm,usgs,swot}`); each lane writes only to
its own subfolder. Only the lane that owns an environment creates or updates it.

## Phase 1 — Data spike (first) → `spike/` scratch folder outside the repo, plus a report

- [x] **P1.1 USGS 12200500, Dec 1–31 2025** (`dataretrieval.waterdata`): continuous discharge + gage height,
      daily values, field measurements. Identify the peak (date/time, discharge, stage). *Done (Lane B): `spike/usgs/REPORT.md`; PR [#53](https://github.com/CUAHSI/federal-water-data-curriculum/pull/53).*
- [x] **P1.2 SWOT over the lower Skagit** *(done, Lane B: `spike/swot/REPORT.md`; PR [#53](https://github.com/CUAHSI/federal-water-data-curriculum/pull/53))* — both products will be taught in Modules 3 and 4:
  - `SWOT_L2_HR_RiverSP` via hydrocron: reach/node WSE (and width) time series for the SWORD reach(es) at the gage.
  - `SWOT_L2_HR_Raster_100m` via `earthaccess` + `xarray`: water area / water fraction for each pass.
  - Confirm which passes truly cover the gage reach (CMR search on 10/7 suggested UTM 10U tiles on Dec 1, Dec 4,
    **Dec 12 ~09:00 UTC**, Dec 14 — that search also returned false matches near the antimeridian, so verify).
  - Show a pre-event vs. near-peak water-extent comparison; note what RiverSP does and does not capture out of bank.
- [x] **P1.3 NWM forecasts — measure each access route** (report in `~/fwdc-spike/nwm/REPORT.md`; findings in [PR #54](https://github.com/CUAHSI/federal-water-data-curriculum/pull/54), draft) for the gage reach (COMID via NLDI). Record for each:
      works for Dec 2025? key needed? files touched, **bytes transferred, wall time, peak memory**, lines of code.
  1. NOAA NWM API (api.water.noaa.gov/nwm/v1, no key): single reach, latest run + ~3-day archive. Expected to
     miss Dec 2025 — measure on *today's* forecast instead.
  2. `hydrotools` (`nwm_client_new`, GCP backend, no key): 2–3 short-range reference times before the peak + one
     medium-range member. Downloads whole CONUS files per timestep.
  3. Kerchunk / virtual Zarr references, no key: (a) NOAA's published references in `s3://noaa-nodd-kerchunk-pds`
     (NWM short-range only; check whether they reach Dec 2025 — they point at the rolling-window source bucket);
     (b) build references yourself for the same GCP files from route 2 and open them with `xarray`. Measure the
     same things. Expectation from Element84's study: faster and far less memory, but **similar bytes**, because
     NWM files are chunked by time with all ~2.7M reaches in each chunk.
  4. Scale test: repeat routes 2–3 for ~1,000 reaches (e.g. everything upstream of the gage via NLDI navigation).
     The per-file cost should barely change — that's the teaching point.
  5. CIROH NWM / BigQuery API: **not used and not recommended in the course** (team decision; see the TODO
     at the top of 03/02). Don't run it.
- [ ] **P1.4 Spike report** (`spike/REPORT.md` + figures): results table for P1.3, plots for P1.1–P1.2, problems hit.

## Phase 2 — Environments
- [x] P2.1 `environments/synthesis.yml`, `swot.yml`, `nwm.yml`, `nwis.yml` (conda-forge, minimal pins). Create each
      in a fresh env and run the relevant spike scripts in it. Branch: `env/course-environments`. *(Ticked for Lane B per Lindsay, 2026-10-08; env files were created on each lane's content branch.)*

## Phase 3 — Module 4 drafts — every code block executed
- [x] **P3.1 04/02 "Synthesizing Federal data products"** (branch `content/04-synthesis`, PR [#53](https://github.com/CUAHSI/federal-water-data-curriculum/pull/53), draft rough cut):
      flood context (image with credit + alt text) · area of interest (USGS gage ↔ NWM COMID ↔ SWORD reach) ·
      USGS observations incl. out-of-bank measurement limits · NWM forecasts: how forecasts changed approaching
      the peak, using the no-key route, with a one-paragraph pointer to Module 3's access-route guidance ·
      SWOT: RiverSP WSE through the event + Raster water extent pre-event vs. near peak · conclusions.
- [x] **P3.2 04/01 "Comparative overview"** (branch `content/04-comparative-overview`, [PR #49](https://github.com/CUAHSI/federal-water-data-curriculum/pull/49), draft): NWM spatial/temporal
      bullets, accuracy section, comparison table (shared terminology), "Data provider recommendations" drafted
      from agency sources, each cited and marked `[PARTNER REVIEW: NASA|NOAA|USGS]`.
- [x] **P3.3 04/00 overview + 04/03 additional data** (branch `content/04-overview-additional`, [PR #50](https://github.com/CUAHSI/federal-water-data-curriculum/pull/50), draft): objectives and
      concepts; short tours of SWOT SoS discharge, AORC precipitation, NGEN hydrofabric.

## Phase 4 — Module 3 alignment drafts
Cut from `upstream/dev`, which already includes the colleagues' Module 3 updates (PRs #40–#43). Build on their
text; don't rewrite sections that are already filled in.
- [x] **P4.1 03/02 NWM** (branch `content/03-nwm-access-routes`, [PR #54](https://github.com/CUAHSI/federal-water-data-curriculum/pull/54), draft). Resolve the TODO at the top of the page
      (kerchunk / a better option than hydrotools; **BigQuery is not suggested**). Fold the P1.3 findings into the
      page's existing *Temporal scaling*, *Spatial scaling* and *Parallelization* sections, and add a short
      **"Which access route for which use case?"** table near the top, for example:

      | Use case | Recommended route | Key? | Caveat |
      |---|---|---|---|
      | Today's / last few days' forecast for a few reaches | NOAA NWM API | No | ~3-day archive; experimental service |
      | Past forecasts, a few reaches, a few issue times | `hydrotools` (GCP archive) | No | Downloads whole CONUS files; cost grows with time span, not reach count |
      | Many reaches or a region | Kerchunk/virtual-Zarr references + `xarray`/`dask`, ideally run in-cloud | No | Lazy reads and low memory; still reads full time-slices, so bytes stay high |
      | Long historical record (simulation, not forecasts) | NWM retrospective (cloud Zarr) | No | Different product — already described on the page |

      Final rows and numbers come from the spike — don't publish these expectations as findings. Learners see the
      recommendations, not our exploration. Also fix the broken install lines (`nwm-envpython3 -m`); setup → `environments/nwm.yml`.
- [x] **P4.2 03/01 SWOT** (branch `content/03-swot-raster`, [PR #47](https://github.com/CUAHSI/federal-water-data-curriculum/pull/47), draft): add Raster water-area discovery + download alongside
      RiverSP/hydrocron, with "which product for which question"; fix `river_datasets_all`; replace the expired signed
      CloudFront PDF link; setup → `environments/swot.yml`.
- [x] **P4.3 03/03 NWIS + 03/00 overview** (branch `content/03-nwis-overview`, [PR #48](https://github.com/CUAHSI/federal-water-data-curriculum/pull/48), draft): continuous values + field
      measurements as used in 04/02; fix `get_reference_tablea`; modernized `waterdata` first; setup →
      `environments/nwis.yml`; 03/00 objectives + concepts (APIs, keys/rate limits, scaling, agency libraries).
- [x] **P4.4 Module 2 suggestions** ([issue #52](https://github.com/CUAHSI/federal-water-data-curriculum/issues/52)) — write the proposed issue text (no `02-*` edits), including a short pointer from
      02_meet_noaa_nwm to the new access-route guidance. Open the issue only with Lindsay's approval.

## Phase 5 — Wrap-up (each lane)
- [x] P5.1 Run `content-reviewer` on every branch; fix all "Must fix". *(Ticked for Lane B per Lindsay, 2026-10-08.)*
- [x] P5.2 **Lane report** (`spike/<lane>/REPORT.md`, also printed in the session): per branch — what changed,
      what ran (with versions), reviewer summary, `[TODO]`/`[PARTNER REVIEW]` markers, decisions taken on Lindsay's
      behalf, and the push/PR requests ready to approve. *(Ticked for Lane B per Lindsay, 2026-10-08.)*

## Later — first cut complete (Fri–Mon)
- [ ] L1 `LICENSE` (GPL-3.0 text from gnu.org) + "Sources and credits" page listing every notebook and agency resource.
- [ ] L2 Full `content-reviewer` pass and execute every example on `dev`.
- [ ] L3 Status summary for the 10/13 sweep.

## Phase 6 — Consistency and enrichment pass (Thu 10/8, lanes done by 21:00)

**Goal:** by Friday morning, Modules 2–4 read as one course. Every lesson follows `STYLE_GUIDE.md`: shared
framework and lesson structure, NASA → NOAA → USGS order (04/02 excepted), WDFN naming, Module 3 lessons
that stand alone on shared example rivers, rendered figures and maps, consistent callouts, reproducibility woven
in, glossary links, References entries, and learning objectives from issue #36. Module 1 stays read-only.
"Check your understanding" waits until after the internal review.

**How work flows:** agents commit, push their own `<type>/<topic>` branches to `upstream` and open **draft PRs into
`dev`** without asking. Lindsay reviews and merges. Lane branches don't edit `ROADMAP.md`; each PR lists the task
IDs it completed, and Lindsay ticks the boxes.

| When | What |
|---|---|
| Thu ~16:30 | Lindsay merges the kit update (`STYLE_GUIDE.md`, `CLAUDE.md`, settings/guard, agents, skills) |
| Thu ~16:45–17:45 | **P6.0 setup**, one session → draft PR → Lindsay merges |
| Thu ~17:45–21:00 | **Lanes A–D** in parallel → draft PRs; Lindsay merges as each lands |
| Thu ~21:00 | **P6.5 integration** kicked off; runs overnight → draft PR ready for Lindsay Fri morning |
| Fri–Mon | EDS and ODS review on `dev` (separate instructions) |

### P6.0 — Setup (one session, before the lanes) · branch `chore/p6-setup` · time box ~1 hour
- [ ] P6.0.1 Rename environments per STYLE_GUIDE §5 (`m03-swot`, `m03-nwm`, `m03-wdfn`, `m04-synthesis`), with
      matching `name:` fields; recreate each and run a smoke-test import. Update env names in setup sections (find/replace only).
- [ ] P6.0.2 WDFN renames: `02-…/03_meet_usgs_nwis.md` → `03_meet_usgs_wdfn.md` and `03-…/03_access_usgs_nwis.md` →
      `03_access_usgs_wdfn.md`; titles "Meet USGS WDFN" and "Retrieve USGS WDFN data"; update `myst.yml` toc and internal links.
- [ ] P6.0.3 Convert every existing `[TODO …]`, `[POLISH …]`, `[PARTNER REVIEW: X …]` and other bracket placeholder in
      Modules 2–4 to STYLE_GUIDE §7 callouts. Mechanical only; keep the wording; report before/after counts.
- [ ] P6.0.4 Scaffold `glossary.md` (MyST `glossary`), seeded from the Module 2 terminology tables, the STYLE_GUIDE §1 shared
      concepts and obvious jargon; add it to the toc after Module 4. Confirm `{term}` links render.
- [ ] P6.0.5 References system: a course-wide `references.md` at the end of the toc, built from one reference file per page
      (so lanes don't conflict), with proper citations (author/org, year, title, URL, DOI for datasets and software), plus a
      check script that lists external links with no entry. Wire it into `content-reviewer`. Document the mechanism in STYLE_GUIDE §8.
- [ ] P6.0.6 Create `images/m02/`, `images/m03/`, `images/m04/` and add one working `figure` example to STYLE_GUIDE §4.
- [ ] P6.0.7 Course and module objectives from issue #36 (latest comment), placed verbatim:
      - Course landing page (`index.md`): all six objectives.
      - Module 2 `00_introduction.md`: *Characterize the river data products from NASA SWOT, NOAA NWM, and USGS WDFN, including
        relevant variables, derivation, spatial and temporal resolution, and known limitations.*
      - Module 3 `00_introduction.md`: *Adapt provided Python scripts to retrieve data from NASA SWOT, NOAA NWM, and USGS WDFN
        using their recommended APIs and libraries.* and *Select the most appropriate programmatic approach for downloading data
        at large temporal and spatial scales for different hydrologic applications.*
      - Module 4 `00_introduction.md`: *Compare and describe the capabilities and limitations of NASA SWOT, NOAA NWM, and USGS
        WDFN data for a single flood event at the appropriate scales and resolutions.*
      - Module 1 (read-only): the open science/FAIR/reproducibility and data management/publishing objectives go in the PR
        description as a suggested edit for the Module 1 authors.
- [ ] P6.0.8 **Choose the shared example rivers** for Module 3 (STYLE_GUIDE §2 and §10): one main river/basin and one
      "Now you try it" river, each with (a) SWOT RiverSP reaches and Raster coverage with good-quality passes in 2025–2026,
      (b) NWM reaches (COMIDs found via NLDI), and (c) an active WDFN monitoring location with continuous discharge. Not the
      Skagit. Check coverage with real queries; report the candidates considered and why. Fill in the STYLE_GUIDE §10 table.
      Time box 30 minutes; if nothing clean turns up, pick the best and add a `TODO (dev team)` callout.

### Lane A — Module 3 SWOT · branch `content/p6-m03-swot` · owns `03-…/01_access_nasa_swot.md`, `images/m03/swot-*`, its reference file
- [ ] P6.A1 Rebuild the main thread on the §10 main river. Keep the Mississippi headwaters as a short "a river with no SWOT
      reaches" side example; retire the Aitkin walkthrough.
- [ ] P6.A2 Stand-alone lesson: no NOAA/NWM, USGS/WDFN data or Module 4 mentions. Describe locations without other agencies' products.
- [ ] P6.A3 Module 3 lesson structure (STYLE_GUIDE §2), incl. "Choosing an access route" (`earthaccess` vs `hydrocron`)
      and "Understanding what you downloaded" (shared concepts).
- [ ] P6.A4 "Now you try it" on the §10 second river: a short task with the steps to change and expected result, plus a collapsed answer.
- [ ] P6.A5 Rendered figures for every plotting block, a location map, and a "what the data looks like" visual.
- [ ] P6.A6 Reproducibility woven in (STYLE_GUIDE §6), glossary links, references.
- [ ] P6.A7 `content-reviewer` + `learner-reviewer`; fix must-fixes and blockers; push; draft PR; lane report.

### Lane B — Module 3 NWM and WDFN · branch `content/p6-m03-nwm-wdfn` · owns `03-…/00_introduction.md`, `02_access_noaa_nwm.md`, `03_access_usgs_wdfn.md`, `images/m03/nwm-*`, `images/m03/wdfn-*`, their reference files
- [ ] P6.B1 NWM: rebuild the examples on the §10 main river (replaces the Skagit; resolves the existing callout). No Module 4,
      SWOT or USGS-data mentions. NLDI/NHDPlus stay as COMID-finding tools; a gage ID may be used only to locate a reach,
      and the text says so.
- [ ] P6.B2 WDFN: "WDFN" throughout; examples on the §10 main river; remove "same site the SWOT lesson uses" and any SWOT/NWM
      mentions; legacy `nwis` only as a short contrast.
- [ ] P6.B3 Both pages to the Module 3 lesson structure, incl. "Choosing an access route" (align the NWM table's format) and
      "Understanding what you downloaded".
- [ ] P6.B4 "Now you try it" on the §10 second river, per page.
- [ ] P6.B5 Rendered figures; a location map and data visual per page.
- [ ] P6.B6 03/00 overview: NASA → NOAA → USGS order, the shared-concepts framework, the shared rivers, links to each lesson.
- [ ] P6.B7 Reproducibility, glossary links, references.
- [ ] P6.B8 `content-reviewer` + `learner-reviewer`; fix; push; draft PR; lane report.

### Lane C — Module 4 · branch `content/p6-m04` · owns `04-…/*`, `images/m04/*`, their reference files
- [ ] P6.C1 NASA → NOAA → USGS order in 04/00, 04/01 (every section and table) and 04/03. **04/02 keeps its storyline order.**
- [ ] P6.C2 04/03: add SWOTViz (https://swotviz.cuahsi.io/) as an exploration option, with a `TODO (dev team)` callout:
      "SWOTViz is in development; confirm it's ready to point learners to".
- [ ] P6.C3 Every link to CUAHSI/notebooks `Science Examples` or the `develop` branch gets the STYLE_GUIDE §7 link-confirmation
      callout (attribution lines stay).
- [ ] P6.C4 Rendered figures for every plotting block in 04/02 and 04/03; a study-area map early in 04/02.
- [ ] P6.C5 Shared-concepts framing in 04/01's comparison table; reproducibility, glossary links, references (04/00–04/03).
- [ ] P6.C6 `content-reviewer` + `learner-reviewer`; fix; push; draft PR; lane report.

### Lane D — Module 2 and glossary · branch `content/p6-m02` · owns `02-…/*`, `glossary.md`, `images/m02/*`, their reference files
- [ ] P6.D1 Module 2 pages to the lesson structure; terminology tables with the full shared-concept set (add Time,
      Version/provenance, Data unit) in NASA → NOAA → USGS order; WDFN naming.
- [ ] P6.D2 02/00 overview: the objective from P6.0.7, the shared-concepts framework, links to each "Meet" page.
- [ ] P6.D3 A light visual per Module 2 page (coverage map or example data plot).
- [ ] P6.D4 Reproducibility hooks (data versions, provenance, citation) and glossary links; references.
- [ ] P6.D5 Grow `glossary.md` with the terms Module 2 introduces.
- [ ] P6.D6 `content-reviewer` + `learner-reviewer`; fix; push; draft PR; lane report.

### P6.5 — Integration (overnight, after lane PRs merge) · branch `chore/p6-integration`
- [ ] P6.5.1 Add glossary terms requested in lane reports; fix `{term}` build warnings.
- [ ] P6.5.2 References check passes course-wide; the References page reads cleanly.
- [ ] P6.5.3 Course-wide checks: no "NWIS" in titles/headings; NASA → NOAA → USGS (except 04/02); no cross-agency or
      Module 4 mentions in Module 3; Module 3 uses the §10 rivers; no old bracket flags; env names match files; objectives in place.
- [ ] P6.5.4 `learner-reviewer` on Modules 2–4 in order; fix blockers; leave friction items as `TODO (dev team)` callouts.
- [ ] P6.5.5 Draft PR plus a report for Lindsay: callout counts by owner (dev team / NASA / NOAA / USGS), what changed,
      open questions, and anything EDS/ODS should know before reviewing.

### Parked
- [ ] "Check your understanding" in Modules 2–4 (after the internal review).
- [ ] Slides built from the repo plus a course narration guide (after partner review). Keep lesson sections self-contained
      with one key figure each so slides can be generated later.

---

## Source material and credit
**Repo license: GPL-3.0** (matches CUAHSI/notebooks). Cite and credit every notebook and agency resource used.

CUAHSI/notebooks, `develop`, `Data Access Examples/`:
NB-USGS `USGS - Plotting Streamflow using NWIS DataRetrieval/collect-usgs-streamflow.ipynb` ·
NB-NWM `BigQuery/access-nwm-forecasts-using-bigquery-myst.ipynb` (narrative model: forecasts around the July 2023
Vermont flood) · NB-SWOT-LP `SWOT - River Longitudinal Profiles for Water Resources/LongProfileVerticalDatum.ipynb` ·
NB-SWOT-SOS `SWOT - Compare Observed and SoS Discharge/…` · NB-SOS-XR `SWOT - Visualizing SOS Discharge with Xarray/…` ·
NB-HF `NGEN - Hydrofabric Exploration/…` · NB-AORC `AORC - Data Collection and Manipulation Primer/…-myst.ipynb`.

Agency resources (issue #9): NASA SWOT resources, Earthdata Cloud Cookbook, SWOT webinar, Earthdata trainings,
`earthaccess` docs · CIROH NWM intro/data access/BigQuery API/NWM API docs, RIVR, HydroLearn NWM101 + OP_040,
NOAA NWM API (api.water.noaa.gov/nwm/v1/docs), NOAA NODD kerchunk registry, Element84 kerchunk study ·
USGS Water Data OGC APIs, API key signup, `dataRetrieval` API-limit notes, 2026 changes slides,
`dataretrieval-python` docs · HydroLearn floodplain course · PO.DAAC Hydrocron Skagit tutorial.

## Decisions log
| Date | Decision | By |
|---|---|---|
| 2026-10-07 | Markdown + code blocks; agent executes every example. Runnable notebooks maybe later. | Lindsay |
| 2026-10-07 | One conda env per agency lesson + one for Module 4, in `environments/`. | Lindsay |
| 2026-10-07 | Module 4 uses NWM **forecasts**; observed record from USGS. | Lindsay |
| 2026-10-07 | Provider recommendations drafted from agency sources, marked for partner review. | Lindsay |
| 2026-10-07 | PRs target `dev`; Pages builds from `dev`, marked draft. | Lindsay |
| 2026-10-07 | Repo license GPL-3.0; cite all notebooks and agency materials. | Lindsay |
| 2026-10-07 | SWOT: teach both RiverSP (WSE) and Raster (water area) in Modules 3 and 4. | Lindsay |
| 2026-10-07 | NWM: recommend routes that scale, by use case; package findings into Module 3, not the exploration itself. | Lindsay |
| 2026-10-07 | Use the existing `dev` branch (fast-forwarded to `main`) as the integration branch. | Claude, per Lindsay's "develop or similar" |
| 2026-10-07 | Don't recommend the CIROH NWM/BigQuery API; evaluate kerchunk vs. hydrotools (from the TODO in 03/02). | Team (PR #43) |
| 2026-10-07 | Fork-and-pull: agent branches and PRs go directly to `upstream` (CUAHSI); `origin` (fork) unused. | Lindsay |
| 2026-10-07 | Rough cut today in parallel lanes; polish later. Review Thu; Lindsay out Fri. | Lindsay |
| 2026-10-07 | **Proposed — confirm:** agent commits locally on feature branches without asking (keeps one branch per PR moving without waiting on you); pushes/PRs still need approval. | Claude |
| 2026-10-08 | Reserve the Skagit River / December 2025 flood for the Module 4 case study. Module 3 lessons will switch to other examples (the NWM page currently uses Skagit; flagged with a TODO, to change later). | Lindsay |
| 2026-10-08 | List the CIROH NWM BigQuery API in the 03/02 access-route table as an option for researchers on CIROH projects (access by request, linked to CIROH), not as a general recommendation. Narrows the 2026-10-07 BigQuery decision. | Lindsay |
| 2026-10-08 | `STYLE_GUIDE.md` is the source of truth for structure, voice and terms (shared framework across SWOT/NWM/WDFN). | Lindsay |
| 2026-10-08 | USGS product is called WDFN (NWIS only as history or the legacy module). | Lindsay |
| 2026-10-08 | Agency order NASA → NOAA → USGS course-wide; 04/02 keeps its storyline order. | Lindsay |
| 2026-10-08 | Environments named `m<module>-<product>` (`m03-swot`, `m03-nwm`, `m03-wdfn`, `m04-synthesis`). | Lindsay |
| 2026-10-08 | Module 3 lessons stand alone (no cross-agency or Module 4 mentions) and share one main river plus one "Now you try it" river; Mississippi headwaters kept as a "no SWOT data" side example. | Lindsay |
| 2026-10-08 | Open items use two callout types: `TODO (dev team)` and `Partner review (AGENCY)`. | Lindsay |
| 2026-10-08 | Reproducibility/open science woven through the text, not separate exercises. | Lindsay |
| 2026-10-08 | Course-wide References and Glossary pages; rendered figures/maps shown; location and data visuals added. | Lindsay |
| 2026-10-08 | Learning objectives from issue #36 (latest comment) mapped to modules; Module 1's suggested only. | Lindsay |
| 2026-10-08 | Links to CUAHSI/notebooks `Science Examples` or the `develop` branch flagged for a dev-team decision. | Lindsay |
| 2026-10-08 | Module 2 unlocked; Module 1 stays read-only. | Lindsay |
| 2026-10-08 | Agents push their own `<type>/<topic>` branches and open draft PRs into `dev` without asking; Lindsay reviews and merges. | Lindsay |
| 2026-10-08 | "Check your understanding", slides and narration guide parked. | Lindsay |
