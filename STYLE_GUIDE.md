# Course style guide

How we write *Federal Open Water Data for Researchers*. It applies to everyone who edits the course:
the curriculum team, reviewers and Claude Code. When this guide and an older page disagree, the guide wins;
fix the page.

## 1. One framework, three data products

Learners should be able to move between NASA SWOT, NOAA NWM and USGS WDFN data because every product is
introduced the same way. Use agency vocabulary (granule, COMID, monitoring location), but always map it back
to the shared framework the first time it appears on a page.

### Shared concepts

| Shared concept | Question it answers | SWOT | NWM | WDFN |
|---|---|---|---|---|
| Location identifier | *Where* is this value? | `reach_id`, `node_id` (SWORD) | COMID / `feature_id` (NHDPlus) | monitoring location ID (`USGS-12200500`) |
| Variable | *What* was measured or modeled? | water surface elevation, width, … | streamflow | discharge, gage height, … |
| Variable unit | In what units? | m, m/km, m³/s | m³/s | ft³/s, ft |
| Time | *When*, and how often? | overpass time | forecast reference time + valid time | timestamp (continuous / daily) |
| Data quality flag(s) | How much should I trust it? | `reach_q`, `wse_qual`, … | none per value (model output) | approval status (provisional / approved), qualifiers |
| Version / provenance | Which release, from where? | product version (e.g. `D`), collection DOI | model version (e.g. v3.0), run configuration | service, retrieval date |
| Data unit | What is one "file" or record? | granule | one output file per timestep | one time series per location + parameter |

Module 2 terminology tables and the course Glossary use exactly these shared-concept names.

### Agency order and names

- **Order is always NASA → NOAA → USGS**: in lists, tables, sections, figure legends and the table of contents.
  *One exception:* the Module 4 case-study page (04/02) keeps its storyline order.
- **USGS: say WDFN.** NWIS (the National Water Information System) still exists, but NWISWeb has been replaced
  by **Water Data for the Nation (WDFN)**, which publishes NWIS data. Use "WDFN" as the umbrella term
  ("data from WDFN", "the WDFN APIs"). Say "NWIS" only when explaining that history or the legacy `nwis`
  module, and never in titles.
- First mention on each page uses the full name: *NASA Surface Water and Ocean Topography (SWOT)*,
  *NOAA National Water Model (NWM)*, *USGS Water Data for the Nation (WDFN)*.

## 2. Lesson structure

Every lesson in a module has the same sections, in the same order. If a section doesn't apply, keep the
heading and add one sentence saying why.

**Module 2: "Meet <product>"**
Terminology (shared-concept table) → Dataset derivation → Spatial coverage → Temporal coverage →
Data content → Usage and support → Further reading

**Module 3: "Retrieve <product> data"**
1. Introduction: what you'll retrieve, linking to the matching Module 2 page.
    - When there may be multiple tools, this also includes a section and table to help choose 
    an access route: a use-case table (which tool for which job, and its scaling limits)
2. Tools and environment setup
4. Programmatic data discovery: the GUI equivalent first, then code
5. Programmatic data downloads
6. Understanding what you downloaded: walk through the shared concepts for the actual output
7. Best practices FAQs: temporal scaling, spatial scaling, parallelization
8. Now you try it: the same steps on the course's second river (see below)
9. Further reading

**Module 3 lessons stand alone.** A Module 3 lesson never mentions the other agencies' products, the Module 4
case study or the Skagit River. Each lesson has its own main example, chosen so the product actually has
data there, plus its own environment. It may link back to Module 1 (concepts) and to its own Module 2 page.
Comparisons and combinations belong only in Module 4. This keeps the course modular: an agency lesson can be
added or removed without rewriting the others.

**Shared example rivers (Module 3).** All three Module 3 lessons use the same main river/basin, plus a second one
for "Now you try it". Both are chosen so that all three products have good data there, and neither is the Module 4
case study. Each lesson still describes the river without mentioning the other agencies' products. The chosen
rivers, sites, reaches and dates are listed in §10. The Mississippi headwaters stay in the SWOT lesson as a short
side example of a river with no SWOT reaches.

## 3. Voice

- Second person ("you"), present tense, friendly and precise. Explain *why* before *how*.
- Audience: graduate students and researchers with intermediate Python and limited hydrologic-data experience.
  Define hydrology and data terms at first use (and link them to the Glossary).
- Keep paragraphs short. Put one idea in each code block.

## 4. Code, figures and maps

- Every code block gets a lead-in sentence (what and why) and is followed by a description of what came back
  (type, key columns, units, quality flags).
- **If code makes a figure or map, show the rendered output** right after the block. Save it under
  `images/<module>/<page>-<short-name>.png` and embed it with a MyST `figure` directive that has a caption and
  `alt` text.
- Add location maps and "what the data looks like" visuals generously, whenever they help a learner orient.
  Maps are static images (pages aren't executed); a short code block shows how each was made.
- Every example is run before it's committed, in the lesson's environment.
- Code is commented to explain exactly what is happening in the chunk and follows reproducible techniques.

**Figure example.** Images live in `images/m02/`, `images/m03/` or `images/m04/`. From a page in a module folder,
the path starts with `../`. Every figure has `alt` text (what the image shows, for a screen reader), a caption
(what to notice) and, for data figures, the data source and access date. Credit images you did not make, with a link.

````markdown
:::{figure} ../images/m03/example-ohio-louisville-discharge.png
:alt: Line chart of daily mean discharge at the Ohio River at Louisville, KY, from 15 March to 15 May 2025. Flow rises from about 100,000 to a crest of 712,000 cubic feet per second on 9 April 2025, then falls back below 200,000 by late April.
:width: 100%

Daily mean discharge at USGS 03294500, Ohio River at Louisville, KY, during the April 2025 flood. Data: USGS Water Data
for the Nation daily values (parameter `00060`, statistic `00003`), accessed 2026-10-08; values from 9 April 2025 onward
(including the crest) were provisional at access.
:::
````

## 5. Environments

One conda environment per lesson that has code, named `m<module>-<product>`:

| File | Environment name | Lesson |
|---|---|---|
| `environments/m03-swot.yml` | `m03-swot` | Retrieve NASA SWOT data |
| `environments/m03-nwm.yml` | `m03-nwm` | Retrieve NOAA NWM data |
| `environments/m03-wdfn.yml` | `m03-wdfn` | Retrieve USGS WDFN data |
| `environments/m04-synthesis.yml` | `m04-synthesis` | Module 4 synthesis |

The file name and the `name:` inside the file always match.

## 6. Reproducibility and open science, throughout

There are no separate exercises for this. Instead, Module 1's ideas show up naturally whenever we introduce
code or data. Link back to the relevant Module 1 section the first time each idea appears on a page:

- **Environments:** why the lesson pins an environment, and how to record package versions.
- **Data versions:** name the product version, model version or approval status you used, and why it matters
  for re-running later.
- **Recording your query:** keep identifiers, bounding boxes, dates and parameter codes in variables or a
  config cell, not scattered through the code.
- **Raw vs. derived data:** keep downloads unchanged, write derived results separately, and say where.
- **Citation:** how to cite the dataset (DOI where one exists) and the date you accessed it.
- **Provisional data:** note when results could change (e.g. provisional USGS data).

## 7. Flags: TODOs and reviews

Every open item is a visible callout box that says **who** it's for. Use only these two forms:

````markdown
:::{admonition} TODO (dev team): <short topic>
:class: attention
What needs doing or deciding, and anything the reader should know.
:::

:::{admonition} Partner review (NASA): <short topic>
:class: important
The specific claim or recommendation the agency should confirm or correct.
:::
````

- The agency in a partner review is one of `NASA`, `NOAA`, `USGS`.
- Don't use inline `[TODO …]`, `[POLISH …]`, `[PARTNER REVIEW …]` or bracketed placeholders any more.
- To list them: `rg "TODO \(dev team\)|Partner review \(" 0*/`
- **CUAHSI notebook links:** every link to the CUAHSI/notebooks `Science Examples` folder, and every link to the
  notebooks repo's `develop` branch, gets a `TODO (dev team): confirm this link` callout. Attribution lines for
  adapted code stay in place regardless, because GPL-3.0 requires credit.

## 8. Citations, references and glossary

- Link sources inline, next to the claim they support.
- **References page:** one course-wide References page at the end lists every external source cited anywhere,
  as a proper citation: author or organization, year, title, URL, and a DOI for datasets and software. It's
  kept in sync with the links in the pages, and the check fails if a link has no reference entry.
- **How it works.** Each page has its own reference file, `references/<page-key>.md`, so lanes never edit the same
  file. The key is `m` + the module number + the page's file name, e.g. `03-…/01_access_nasa_swot.md` →
  `references/m03-01_access_nasa_swot.md` (top-level pages: `references/index.md`, `references/glossary.md`).
  `references.md` (last in the toc) includes every file under a heading for its page. A new page needs a new
  reference file and an `{include}` line in `references.md`.
- **Entry format.** One list item per source, alphabetical by author: author or organization, year (`n.d.` if none),
  *title*, publisher or repository if different, URL, and a DOI for datasets and software. Add the access date for
  pages that change. The URL must match the link used on the page (the check ignores `#fragments` and trailing slashes).

  ```markdown
  - NOAA Office of Water Prediction. (n.d.). *About the National Water Model*. https://water.noaa.gov/about/nwm (accessed 2026-10-08).
  - Hodson, T. O., & Hariharan, J. A. (2023). *dataretrieval (python): a Python package for discovering and retrieving water data available from Federal hydrologic web services* (software). U.S. Geological Survey. https://doi.org/10.5066/P94I5TX3
  ```
- **Check.** `python3 references/check_references.py --changed` (use `python` where `python3` isn't on the path) (or pass page paths; no arguments checks every page).
  It lists each external link outside code blocks that has no entry in that page's reference file and exits 1 if any
  are missing. Entries no longer linked from the page are listed as "unused" (warning only).
- **Glossary page:** one course-wide Glossary page. Define each term once there. On each page, link the first
  use of a term to its glossary entry (the MyST `{term}` role).

## 9. Check your understanding (later)

Not part of this round. We'll add "Check your understanding" sections after the internal review.

## 10. Course example rivers

Chosen in roadmap task P6.0.8 (2026-10-08) from real queries. SWOT counts are Version D RiverSP reach observations
from `hydrocron`, 2025-01-01 to 2026-10-01; Raster scenes are 100 m Raster Version D scenes whose footprint contains the gage.

| Role | River / basin | SWOT reach IDs | NWM COMIDs | WDFN monitoring location | Date window |
|---|---|---|---|---|---|
| Main example (Module 3) | Ohio River at Louisville, KY (Ohio basin) | `74267300251` (gage reach, ~170 m away); neighbors `74267300241`, `74267300261` | `10164004` | USGS-03294500 | 2025-03-15 to 2025-05-15 (April 2025 flood; daily-mean crest 712,000 ft³/s on 2025-04-09) |
| Now you try it (Module 3) | Willamette River at Salem, OR (Willamette basin) | `78220000131` (gage reach, ~30 m away); neighbor `78220000141` | `23791093` | USGS-14191000 | 2026-02-01 to 2026-03-31 (winter high flows; February daily-mean max 62,200 ft³/s) |
| Module 4 case study | Skagit River, WA (Dec 2025 flood) | — | — | USGS-12200500 | Dec 2025 |

**What we checked**

| | Ohio at Louisville (main) | Willamette at Salem (try it) |
|---|---|---|
| SWOT reach prior width (`p_width`) | 720 m | 150 m |
| SWOT passes over the gage | 4 (160, 175, 466, 481) | 3 (039, 274, 345) |
| Reach observations, `reach_q` ≤ 1 / all valid | 114 / 118 (every month has 3–6 good ones; 5 in April 2025) | 62 / 91 (2–4 good ones per month) |
| Raster scenes over the gage, 2025–2026 | 113 | 83 |
| NWM | NLDI indexes the gage to COMID `10164004` (Ohio River); the NOAA NWM API returns short-range forecasts; archived short-range files exist for 2025-04-09 (Google Cloud and AWS) | NLDI indexes the gage to COMID `23791093` (reach code `17090007000072`); the NOAA NWM API returns short-range forecasts (the API's `name` field is blank for this reach) |
| WDFN | Continuous discharge 2009–present, daily values 1928–present; active | Continuous discharge 1986–present, daily values 1909–present; active |

Notes for lesson authors:
- No reach had `reach_q` = 0 in this period; good observations are `reach_q` = 1 ("suspect" in the summary flag). Explain this rather than filtering on `reach_q == 0`.
- The Willamette also peaked on 2025-12-20 (97,700 ft³/s), during the same December 2025 storms as the Module 4 Skagit flood. The February–March 2026 window avoids overlapping the case study.
- The NOAA NWM API `streamflow` endpoint reported units of ft³/s for these reaches on 2026-10-08.
- Candidates considered and why they were not chosen: Connecticut at Thompsonville (NLDI indexes the gage to a tributary COMID, "Rawlins Brook"); Susquehanna at Marietta (the gage reach had no `reach_q` ≤ 1 observations); Missouri at Hermann and Mississippi at St. Louis (only 12/61 and 20/60 good observations); Sacramento at Freeport (good SWOT data, but tidal and with no daily values after 2015); Columbia at The Dalles (dam-controlled, 33/59 good); Mississippi at St. Paul (50/90 good, 190 m wide; acceptable backup).
