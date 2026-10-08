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
- **Glossary page:** one course-wide Glossary page. Define each term once there. On each page, link the first
  use of a term to its glossary entry (the MyST `{term}` role).

## 9. Check your understanding (later)

Not part of this round. We'll add "Check your understanding" sections after the internal review.

## 10. Course example rivers

*Filled in during roadmap task P6.0.8.*

| Role | River / basin | SWOT reach IDs | NWM COMIDs | WDFN monitoring location | Date window |
|---|---|---|---|---|---|
| Main example (Module 3) | | | | | |
| Now you try it (Module 3) | | | | | |
| Module 4 case study | Skagit River, WA (Dec 2025 flood) | — | — | USGS-12200500 | Dec 2025 |
