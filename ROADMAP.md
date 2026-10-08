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
