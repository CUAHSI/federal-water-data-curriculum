# Roadmap — Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access

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

### P6.0 — Setup (one session, before the lanes) · branch `chore/p6-setup` · time box ~1 hour · *(done, PR [#59](https://github.com/CUAHSI/federal-water-data-curriculum/pull/59))*
- [x] P6.0.1 Rename environments per STYLE_GUIDE §5 (`m03-swot`, `m03-nwm`, `m03-wdfn`, `m04-synthesis`), with
      matching `name:` fields; recreate each and run a smoke-test import. Update env names in setup sections (find/replace only).
- [x] P6.0.2 WDFN renames: `02-…/03_meet_usgs_nwis.md` → `03_meet_usgs_wdfn.md` and `03-…/03_access_usgs_nwis.md` →
      `03_access_usgs_wdfn.md`; titles "Meet USGS WDFN" and "Retrieve USGS WDFN data"; update `myst.yml` toc and internal links.
- [x] P6.0.3 Convert every existing `[TODO …]`, `[POLISH …]`, `[PARTNER REVIEW: X …]` and other bracket placeholder in
      Modules 2–4 to STYLE_GUIDE §7 callouts. Mechanical only; keep the wording; report before/after counts.
- [x] P6.0.4 Scaffold `glossary.md` (MyST `glossary`), seeded from the Module 2 terminology tables, the STYLE_GUIDE §1 shared
      concepts and obvious jargon; add it to the toc after Module 4. Confirm `{term}` links render.
- [x] P6.0.5 References system: a course-wide `references.md` at the end of the toc, built from one reference file per page
      (so lanes don't conflict), with proper citations (author/org, year, title, URL, DOI for datasets and software), plus a
      check script that lists external links with no entry. Wire it into `content-reviewer`. Document the mechanism in STYLE_GUIDE §8.
- [x] P6.0.6 Create `images/m02/`, `images/m03/`, `images/m04/` and add one working `figure` example to STYLE_GUIDE §4.
- [x] P6.0.7 Course and module objectives from issue #36 (latest comment), placed verbatim:
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
- [x] P6.0.8 **Choose the shared example rivers** for Module 3 (STYLE_GUIDE §2 and §10): one main river/basin and one
      "Now you try it" river, each with (a) SWOT RiverSP reaches and Raster coverage with good-quality passes in 2025–2026,
      (b) NWM reaches (COMIDs found via NLDI), and (c) an active WDFN monitoring location with continuous discharge. Not the
      Skagit. Check coverage with real queries; report the candidates considered and why. Fill in the STYLE_GUIDE §10 table.
      Time box 30 minutes; if nothing clean turns up, pick the best and add a `TODO (dev team)` callout.

### Lane A — Module 3 SWOT · branch `content/p6-m03-swot` · owns `03-…/01_access_nasa_swot.md`, `images/m03/swot-*`, its reference file · *(done, PR [#64](https://github.com/CUAHSI/federal-water-data-curriculum/pull/64))*
- [x] P6.A1 Rebuild the main thread on the §10 main river. Keep the Mississippi headwaters as a short "a river with no SWOT
      reaches" side example; retire the Aitkin walkthrough.
- [x] P6.A2 Stand-alone lesson: no NOAA/NWM, USGS/WDFN data or Module 4 mentions. Describe locations without other agencies' products.
- [x] P6.A3 Module 3 lesson structure (STYLE_GUIDE §2), incl. "Choosing an access route" (`earthaccess` vs `hydrocron`)
      and "Understanding what you downloaded" (shared concepts).
- [x] P6.A4 "Now you try it" on the §10 second river: a short task with the steps to change and expected result, plus a collapsed answer.
- [x] P6.A5 Rendered figures for every plotting block, a location map, and a "what the data looks like" visual.
- [x] P6.A6 Reproducibility woven in (STYLE_GUIDE §6), glossary links, references.
- [x] P6.A7 `content-reviewer` + `learner-reviewer`; fix must-fixes and blockers; push; draft PR; lane report.

### Lane B — Module 3 NWM and WDFN · branch `content/p6-m03-nwm-wdfn` · owns `03-…/00_introduction.md`, `02_access_noaa_nwm.md`, `03_access_usgs_wdfn.md`, `images/m03/nwm-*`, `images/m03/wdfn-*`, their reference files · *(done, PR [#63](https://github.com/CUAHSI/federal-water-data-curriculum/pull/63))*
- [x] P6.B1 NWM: rebuild the examples on the §10 main river (replaces the Skagit; resolves the existing callout). No Module 4,
      SWOT or USGS-data mentions. NLDI/NHDPlus stay as COMID-finding tools; a gage ID may be used only to locate a reach,
      and the text says so.
- [x] P6.B2 WDFN: "WDFN" throughout; examples on the §10 main river; remove "same site the SWOT lesson uses" and any SWOT/NWM
      mentions; legacy `nwis` only as a short contrast.
- [x] P6.B3 Both pages to the Module 3 lesson structure, incl. "Choosing an access route" (align the NWM table's format) and
      "Understanding what you downloaded".
- [x] P6.B4 "Now you try it" on the §10 second river, per page.
- [x] P6.B5 Rendered figures; a location map and data visual per page.
- [x] P6.B6 03/00 overview: NASA → NOAA → USGS order, the shared-concepts framework, the shared rivers, links to each lesson.
- [x] P6.B7 Reproducibility, glossary links, references.
- [x] P6.B8 `content-reviewer` + `learner-reviewer`; fix; push; draft PR; lane report.

### Lane C — Module 4 · branch `content/p6-m04` · owns `04-…/*`, `images/m04/*`, their reference files · *(done, PR [#62](https://github.com/CUAHSI/federal-water-data-curriculum/pull/62))*
- [x] P6.C1 NASA → NOAA → USGS order in 04/00, 04/01 (every section and table) and 04/03. **04/02 keeps its storyline order.**
- [x] P6.C2 04/03: add SWOTViz (https://swotviz.cuahsi.io/) as an exploration option, with a `TODO (dev team)` callout:
      "SWOTViz is in development; confirm it's ready to point learners to".
- [x] P6.C3 Every link to CUAHSI/notebooks `Science Examples` or the `develop` branch gets the STYLE_GUIDE §7 link-confirmation
      callout (attribution lines stay).
- [x] P6.C4 Rendered figures for every plotting block in 04/02 and 04/03; a study-area map early in 04/02.
- [x] P6.C5 Shared-concepts framing in 04/01's comparison table; reproducibility, glossary links, references (04/00–04/03).
- [x] P6.C6 `content-reviewer` + `learner-reviewer`; fix; push; draft PR; lane report.

### Lane D — Module 2 and glossary · branch `content/p6-m02` · owns `02-…/*`, `glossary.md`, `images/m02/*`, their reference files · *(done, PR [#61](https://github.com/CUAHSI/federal-water-data-curriculum/pull/61))*
- [x] P6.D1 Module 2 pages to the lesson structure; terminology tables with the full shared-concept set (add Time,
      Version/provenance, Data unit) in NASA → NOAA → USGS order; WDFN naming.
- [x] P6.D2 02/00 overview: the objective from P6.0.7, the shared-concepts framework, links to each "Meet" page.
- [x] P6.D3 A light visual per Module 2 page (coverage map or example data plot).
- [x] P6.D4 Reproducibility hooks (data versions, provenance, citation) and glossary links; references.
- [x] P6.D5 Grow `glossary.md` with the terms Module 2 introduces.
- [x] P6.D6 `content-reviewer` + `learner-reviewer`; fix; push; draft PR; lane report.

### P6.5 — Integration (overnight, after lane PRs merge) · branch `chore/p6-integration` · *(done, PR [#65](https://github.com/CUAHSI/federal-water-data-curriculum/pull/65))*
- [x] P6.5.1 Add glossary terms requested in lane reports; fix `{term}` build warnings.
- [x] P6.5.2 References check passes course-wide; the References page reads cleanly.
- [x] P6.5.3 Course-wide checks: no "NWIS" in titles/headings; NASA → NOAA → USGS (except 04/02); no cross-agency or
      Module 4 mentions in Module 3; Module 3 uses the §10 rivers; no old bracket flags; env names match files; objectives in place.
- [x] P6.5.4 `learner-reviewer` on Modules 2–4 in order; fix blockers; leave friction items as `TODO (dev team)` callouts.
- [x] P6.5.5 Draft PR plus a report for Lindsay: callout counts by owner (dev team / NASA / NOAA / USGS), what changed,
      open questions, and anything EDS/ODS should know before reviewing.

## Phase 7 — Move SWOT discharge from main product to "in development" (Tue 10/13)

**Goal:** SWOT is taught as water surface elevation, width, slope and water extent. SWOT discharge (SoS,
`SWOT_L4_HR_DAWG_SOS_DISCHARGE`, and the `dschg_*` fields in RiverSP) is no longer presented as a core SWOT
variable. It stays in Module 4 only as an in-development "additional" dataset (04/03), and Module 2 mentions it
once, briefly, as in development, pointing to 04/03.

One session, one branch: `content/p7-rm-swot-discharge`. Draft PR into `dev`. *(done, PR [#70](https://github.com/CUAHSI/federal-water-data-curriculum/pull/70))*

- [x] P7.1 Inventory first: list every mention of SWOT discharge in Modules 2–4, `glossary.md`, `STYLE_GUIDE.md`
      and `references/` (`rg -n -i "discharge|dschg|SoS|DAWG" ...`), and classify each as *remove*, *reword to
      in-development*, or *keep* (non-SWOT discharge, e.g. USGS/NWM, stays as is). Put the table in the PR description.
- [x] P7.2 Module 2, Meet NASA SWOT (`02-…/01_meet_nasa_swot.md`):
      - Terminology table: Variable = water surface elevation, width, slope (and water area for Raster);
        Variable unit = m (WSE, width), m/km (slope). Drop discharge and m³/s.
      - "Key point" box and Dataset derivation: SWOT measures WSE, width and slope. Replace the discharge
        derivation paragraph with 1–2 sentences: discharge estimates are in development (SoS), not yet a
        recommended research product, see Module 4 → Additional data.
      - Data content: remove discharge from "Primary variables"; one "In development" bullet pointing to 04/03.
      - Update any Module 2 figure, caption or callout that features SWOT discharge.
- [x] P7.3 Module 2 overview (`02-…/00_introduction.md`): SWOT column of the shared-concepts table and the units
      note no longer imply SWOT discharge. The NWM/USGS streamflow/discharge comparison stays.
- [x] P7.4 Module 4:
      - `01_comparative_overview.md`: SWOT Variable/unit rows show WSE, width, slope (+ water area); no
        "derived discharge". Check the accuracy and recommendations text for SWOT discharge claims.
      - `00_introduction.md`: reword the objective/bullet that names SoS discharge so it's clearly an
        in-development "additional" dataset, alongside AORC and the hydrofabric.
      - `02_synthesize_river_data.md`: confirm the case study doesn't use or imply SWOT discharge.
      - `03_additional_data.md`: keep SoS, with an "In development" label up front (status, version and date
        range, not recommended for research use yet). Keep its `Partner review (NASA)` callout.
- [x] P7.5 Consistency: `glossary.md` (RiverSP entry; any SoS term marked in development) and `STYLE_GUIDE.md` §1
      (SWOT units: m, m/km). In Module 3 (`03-…/01_access_nasa_swot.md`), check only that the existing
      "no discharge here yet" note doesn't contradict the new framing; adjust wording minimally if it does.
- [x] P7.6 References: drop entries no longer cited; keep SoS/PO.DAAC entries used in 04/03. Build passes;
      references check passes.
- [x] P7.7 `content-reviewer` + `learner-reviewer` on the changed pages; fix must-fixes and blockers; push;
      draft PR listing every changed sentence/table cell (before → after) for Lindsay's review.

## Phase 8 — Teaching materials (built from the course content, rebuildable)

**Goal:** everything needed to *run* the course is generated from the lesson pages and can be regenerated
when they change:
- **Session slide decks** with instructor notes, plus pre- and post-session reading PDFs for content that
  doesn't fit the session time.
- **A learner bundle for HydroShare:** notebooks (student and solutions), environment files and a README for
  the Module 3 and 4 lessons with code.
- **Module quizzes:** one per module, multiple choice, QTI for Canvas.
- **An instructor guide.**
- **An Acknowledgements page.**

The website (`0*/` pages) stays the single source of truth. Generated material lives in `teaching-materials/`,
which is not part of the website build.

**Pilot constraint:** pilot learners can't see the website or this repo. They learn from the sessions, so they
get the slides and reading PDFs (via Canvas) and the learner bundle (via HydroShare). Learner-facing outputs
must stand on their own:
- **External links are fine** (agency docs, datasets, tools).
- **No links into the course itself:** no links to other course pages, the glossary, the References page or
  the repo. Convert them to plain text, or point to the deck or reading that covers the topic.
- **No `TODO (dev team)` or `Partner review` callouts.**

**How work flows:** as in Phase 6. Agents push their own `<type>/<topic>` branches to `upstream` and open draft
PRs into `dev`. Lane branches don't edit `ROADMAP.md`; each PR lists its task IDs.

| Order | What |
|---|---|
| 1 | Lindsay adds the settings and workflow changes by hand (see "Lindsay, by hand") |
| 2 | **P8.0 setup**, one session → draft PR → merge |
| 3 | **Lanes E, F, G, H** in parallel → draft PRs → merge as each lands |
| 4 | **P8.5 instructor guide** (needs E, F and H merged) |

### Lindsay, by hand (before P8.0; agents can't edit these paths)
- [X] Add to `allow` in `.claude/settings.json`: `"Bash(quarto render:*)"`, `"Bash(quarto check:*)"`,
      `"Bash(quarto --version:*)"`, `"Bash(papermill:*)"`, `"Bash(text2qti:*)"`. (The three `quarto` entries
      can now be removed.)
- [X] Add `.github/workflows/render-slides.yml` (from this kit). It renders the decks and readings on request,
      never per PR. Later replaced by `render-readings.yml`, then removed: decks and readings are built
      locally (#93).
- [X] Add the four `.claude/skills/build-*` folders (from this kit).
- [X] Repo **Settings → Actions → General**: tick **Allow GitHub Actions to create and approve pull requests**. This setting lets the Render slides workflow open draft PRs; it can’t approve or merge its own PRs, because GitHub never lets a PR's author approve it and the workflow only creates a draft. The remaining risk is that a future workflow could approve or merge someone else's PR, but any workflow change has to come through a reviewed PR (agents can't automatically edit .github/workflows/), so approving and merging stay with people. Since #93 removed the render workflows, nothing uses this setting any more; you can untick it.
- [X] Install Quarto locally (https://quarto.org/docs/get-started/). Its bundled Typst makes the reading
      PDFs, so no LaTeX is needed. No longer needed: readings are Word documents (#93).

### P8.0 — Setup · branch `chore/p8-setup` · about 45 min
- [ ] P8.0.1 Create `teaching-materials/` with `materials/` (`slides/`, `readings/`, `learner-bundle/`,
      `quizzes/`, `instructor-guide/`), `how-to-build/` (`tools/`, `manifest.json`) and a `README.md`. Exclude `teaching-materials/` from the MyST site build
      in `myst.yml`.
- [ ] P8.0.2 Add **STYLE_GUIDE §11 Teaching materials** (text below) and add `teaching-materials/` to the
      CLAUDE.md repo map.
- [ ] P8.0.3 `teaching-materials/how-to-build/manifest.json` plus `teaching-materials/how-to-build/tools/check_stale.py`:
    - The manifest has one entry per output: `output`, `kind`, `sources` (lesson paths, images and environment
      files it was built from), `source_commit`, `built_at` and `builder` (skill name).
    - `check_stale.py` uses only the standard library. For each entry it runs
      `git diff --quiet <source_commit> HEAD -- <sources>` and prints the stale outputs, with an exit code of 1
      if any are stale. It also takes `--update <output>` to rewrite an entry after a rebuild.
- [ ] P8.0.4 `teaching-materials/how-to-build/tools/prepare_learner_copy.py`: copies a page for learner-facing use. It:
    - removes every `TODO (dev team)` and `Partner review (…)` admonition
    - turns internal course links (relative links to other pages, `{term}`, `{ref}`, `{doc}` roles, links to
      the References or Glossary pages) into plain text, keeping external `http(s)` links
    - reports the counts of both

    Every learner-facing builder uses it.
- [ ] P8.0.5 Write down the **session map** and the **file names** (§11) in `teaching-materials/README.md`, so
      the lanes agree on names before they start.

### Lane E — Slides and readings · branch `content/p8-slides` · owns `teaching-materials/how-to-build/` (guide, prompts, design rules, checklist, topics, `check_topics.py`)
Decks (PowerPoint) and readings (Word) are built locally from the topic lists and never committed; see
`teaching-materials/how-to-build/guide.md`. Use the `build-slides` skill.
- [X] P8.E1 Prompt kit: topic lists for sessions 1–6, design rules seeded from Lindsay's decks, deck, update and
      reading prompts, review checklist, `check_topics.py`, local deck and reading templates (#93).
- [X] P8.E2 Pilot: Session 1 deck (`/build-slides 1`), reviewed and notes reformatted.
- [ ] P8.E3 Decks for sessions 2–6 (`/build-slides N`), one at a time, each reviewed with the checklist.
- [ ] P8.E4 Module readings for Modules 2–4 (`/build-slides reading M`), only where the topic lists have
      `reading` rows.
- [ ] P8.E5 Share the decks and reading PDFs through Canvas.

### Lane F — Learner bundle · branch `content/p8-learner-bundle` · owns `teaching-materials/materials/learner-bundle/*`, `teaching-materials/how-to-build/tools/build_notebooks.py`
Use the `build-notebooks` skill.
- [ ] P8.F1 `build_notebooks.py` plus scaffold files (in `teaching-materials/how-to-build/scaffolds/`); a student notebook and a solutions notebook for each
      Module 3 and 4 lesson that has code; environment files.
- [ ] P8.F2 Run every solutions notebook top to bottom in its environment. Run every student notebook up to
      the first "Now you try it" cell.
- [ ] P8.F3 Bundle `README.md`, written for HydroShare (what's here, how to open it, credentials, licence,
      how to cite).
- [ ] P8.F4 Manifest entries; review; draft PR.

### Lane G — Credits and orientation · branch `docs/p8-credits-readme` · owns `acknowledgements.md`, `CITATION.cff`, root `README.md`, the authors fields
- [ ] P8.G1 Remove the per-page authors. They probably come from `authors:` in `myst.yml` (project
      frontmatter) and/or page frontmatter; remove them everywhere.
- [ ] P8.G2 Add `acknowledgements.md` (text below) to the toc, after References.
- [ ] P8.G3 Add `CITATION.cff` with the course as learning material: Platt as contact, the
      Writing – Original Draft authors in the order below, the repo URL, GPL-3.0 and the version `pilot-2026-11`.
- [ ] P8.G4 Update the root `README.md` to orient a newcomer:
    - what this repo is
    - **the website** (`0*/` pages, glossary, references; built from `dev` to GitHub Pages)
    - **teaching materials** (`teaching-materials/`; not on the website): `materials/` holds what learners and
      instructors use (slides, readings, the learner bundle, quizzes, the instructor guide); `how-to-build/`
      holds the instructions, prompts and tools that make them
    - **how to rebuild:**
        - build or update decks and readings with `/build-slides` (see `teaching-materials/how-to-build/guide.md`);
          they're built locally and shared through Canvas, never committed
        - regenerate notebooks and quizzes with the `build-notebooks` and `build-quizzes` skills
        - rebuild a quiz's QTI file with `text2qti <file>.txt`
        - find stale outputs with `python teaching-materials/how-to-build/tools/check_stale.py`
    - how to contribute (fork → branch → PR into `dev`)
    - licence and how to cite
- [ ] P8.G5 Review; draft PR.

### Lane H — Module quizzes · branch `content/p8-quizzes` · owns `teaching-materials/materials/quizzes/*`
Use the `build-quizzes` skill. Follows issue #32 (formative, retakes allowed, the correct answer always shown
with an explanation, QTI for Canvas).
- [ ] P8.H1 One quiz per module (Modules 1–4): about 10–15 minutes, multiple choice (mostly single answer,
      with 2–3 "select all that apply"), mapped to that module's
      learning objectives, with feedback on every question.
- [ ] P8.H2 Convert each with `text2qti`; check that the QTI zips build.
- [ ] P8.H3 An objective-coverage table and an answer-key summary per quiz in the PR (for spot-checking); manifest
      entries; draft PR.

### P8.5 — Instructor guide (after E, F and H merge) · branch `content/p8-instructor-guide`
Use the `build-instructor-guide` skill. Draft PR.

### Parked
- [ ] Publishing the learner bundle (plus the slides and reading PDFs, which are built locally) to a HydroShare collection.
      Lindsay will do this with the HydroShare staff after F merges.
- [ ] Canvas: replace the "Lesson pages" module items with the session's slides and reading PDFs.
- [ ] Canvas: set the minimum quiz score for module checkpoints (issue #32) as a module requirement.

---

### STYLE_GUIDE §11 text (P8.0.2)

Added; the current text is in `STYLE_GUIDE.md` §11 (updated in #93 for PowerPoint decks, Word readings and the
`materials/` + `how-to-build/` layout).

### `acknowledgements.md` text (P8.G2)

```markdown
---
title: Acknowledgements
---

*Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access* was developed by CUAHSI with contributions from colleagues at NOAA,
USGS and NASA. Contributions are described with the [CRediT contributor roles](https://credit.niso.org/).

## Contributors

| Name | Affiliation | Contributions |
|---|---|---|
| Lindsay Platt | CUAHSI | Conceptualization; Writing – Original Draft; Project Administration |
| Kimberlee Wong | CUAHSI | Writing – Original Draft |
| Kaysa Vaarre-Lamoureux | CUAHSI | Writing – Original Draft |
| Abner Bogan | CUAHSI | Writing – Original Draft |
| Julia Masterman | CUAHSI | Conceptualization |
| Irene Garousi-Nejad | CUAHSI | Conceptualization; Resources; Writing – Review & Editing |
| Tony Castronova | CUAHSI | Conceptualization; Resources |
| Danielle Tijerina-Kreuzer | CUAHSI | Conceptualization; Resources |
| Jason Regina | NOAA | Resources; Writing – Review & Editing |
| Elise Hinman | USGS | Writing – Review & Editing |
| Cee Nell | USGS | Resources; Writing – Review & Editing |
| Michael Mahoney | USGS | Resources; Writing – Review & Editing |
| *[NASA contributor(s)]* | NASA | *[contributions]* |

:::{admonition} TODO (dev team): NASA attribution
:class: attention
Add the NASA contributor(s) and their contributions.
:::

Contributions from federal agency staff are acknowledged with thanks. Acknowledgment does not imply
endorsement of this course by NASA, NOAA or USGS.

This course adapts code and examples from the [CUAHSI notebooks](https://github.com/CUAHSI/notebooks)
repository (GPL-3.0); individual lessons credit the notebooks they draw on.

## Funding

This material is based upon work supported by the U.S. National Science Foundation under
[Award No. 2535162](https://www.nsf.gov/awardsearch/show-award?AWD_ID=2535162). Any opinions, findings, and
conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily
reflect the views of the National Science Foundation.

## Use of AI tools

Generative AI tools (Anthropic's Claude) were used to help draft lesson text, code examples, figures and
the teaching materials (slides, readings, notebooks, quizzes and instructor guide) from outlines, existing
CUAHSI notebooks and contributors' materials. Contributors reviewed, edited and tested all content, ran every
code example, and are responsible for the course as published.
```

## Parked

None at the moment.

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
| 2026-10-13 | SWOT discharge (SoS / `dschg_*`) is not a core SWOT teaching variable; it appears only as an in-development "additional" dataset in 04/03 and is mentioned as such in Module 2. | Lindsay |
