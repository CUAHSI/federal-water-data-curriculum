# Session 3 · Module 3, lesson 1: Retrieve NASA SWOT data

- **When:** Tue Nov 10, 2026, 2:00–3:30 pm ET (90 min)
- **Deck:** `teaching-materials/slides/session-03_module-03_lesson-01_retrieve-nasa-swot-data.pptx`
- **Reading:** `teaching-materials/readings/module-03_reading_federal-water-data-access-retrieval.qmd` (shared by
  sessions 3–5)
- **Notebook:** `module-03_lesson-01_retrieve-nasa-swot-data.ipynb` (learner bundle)
- **Pages:** `03/00` = `03-federal-water-data-access-retrieval/00_introduction.md`, `03/01` = `01_access_nasa_swot.md`

**Where:** `deck`, `notebook`, `reading`, `how-to`, `cut` (see session-01.md). **Min** adds up to the session
length. Live-coding rows name the notebook sections (they match the lesson headings).

| # | Topic | Source | Where | Min | What the slides should show or do |
|---|---|---|---|---|---|
| 1 | Session title | – | deck | 1 | |
| 2 | Program schedule | – | deck | 1 | Session 3 outlined |
| 3 | Lingering questions from Session 2 | – | deck | 2 | |
| 4 | Goals for today | 03/00 § Learning objectives | deck | 1 | |
| 5 | Module 3 overview and objectives | 03/00 § Module overview, § Learning objectives | deck | 2 | |
| 6 | The three lessons, each standing alone | 03/00 § The lessons | deck | 1 | |
| 7 | The example rivers | 03/00 § The example rivers | deck | 2 | Ohio at Louisville in the lessons; Willamette at Salem for "Now you try it" |
| 8 | One framework, retrieval view | 03/00 § One framework for three products | deck | 3 | The shared-concepts table again, now with the retrieval column |
| 9 | Important concepts and terminology | 03/00 § Important concepts and terminology | deck | 4 | API, granule, cloud-native formats, lazy loading; one term per slide or a build |
| 10 | What you'll retrieve | 03/01 § Retrieve NASA SWOT data (intro) | deck | 2 | `images/m03/swot-location-map.png` |
| 11 | Choosing an access route | 03/01 § Choosing an access route | deck | 4 | The routes and when to use each (build: highlight the route the lesson uses) |
| 12 | Setup: Earthdata Login and the lesson's environment | 03/01 § Make an Earthdata Login account, § Create the lesson's environment | deck + how-to | 2 | One slide: what's needed and that the "How to" guide walks through it |
| 13 | The point-and-click equivalent | 03/01 § The point-and-click equivalent | deck | 1 | Earthdata Search screenshot |
| 14 | Find datasets | 03/01 § Find datasets | deck + notebook | 2 | Short code (≤ 12 lines) and what comes back |
| 15 | A river with no SWOT reaches | 03/01 § A river with no SWOT reaches: the Mississippi headwaters | deck + notebook | 2 | Why an empty result is an answer |
| 16 | Find Raster granules over the Ohio | 03/01 § Find Raster granules over the Ohio at Louisville | deck + notebook | 3 | |
| 17 | Find RiverSP granules over the Ohio | 03/01 § Find RiverSP granules over the Ohio at Louisville | deck + notebook | 2 | |
| 18 | Live coding 1: discovery | 03/01 § Programmatic data discovery | deck + notebook | 12 | Live-coding slide: notebook sections "Find datasets" to "Find RiverSP granules over the Ohio at Louisville" |
| 19 | RiverSP reaches with `earthaccess` | 03/01 § RiverSP reaches with `earthaccess` | deck + notebook | 3 | |
| 20 | Raster water area with `earthaccess` | 03/01 § Raster water area with `earthaccess` | deck + notebook | 4 | `images/m03/swot-raster-water-frac.png` |
| 21 | RiverSP time series with `hydrocron` | 03/01 § RiverSP time series with `hydrocron` | deck + notebook | 4 | `images/m03/swot-hydrocron-wse-flood.png` |
| 22 | Live coding 2: downloads | 03/01 § Programmatic data downloads | deck + notebook | 12 | Live-coding slide: the three download sections |
| 23 | Understanding what you downloaded | 03/01 § Understanding what you downloaded | deck | 5 | Columns, units and quality flags; the degraded 13 April scene as a spotlight build |
| 24 | Best practices: temporal scaling | 03/01 § Temporal scaling | deck | 2 | `images/m03/swot-hydrocron-wse-full-record.png`: the full record in one request |
| 25 | Best practices: spatial scaling and parallelization | 03/01 § Spatial scaling, § Parallelization | deck | 2 | |
| 26 | Now you try it: the Willamette | 03/01 § Now you try it | deck + notebook | 4 | Task slide naming the notebook cell; answers are in the solutions notebook |
| 27 | Recap and what's next | – | deck | 2 | Three bullets; Session 4 |
| 28 | Final questions | – | deck | 5 | |
| 29 | Bitwise decoding of the quality flags | 03/01 § Understanding what you downloaded | reading | – | The detail behind the 13 April scene |
| 30 | Release-note caveats behind the flags | 03/01 § Understanding what you downloaded | reading | – | |
| 31 | Further reading | 03/01 § Further reading | reading | – | |
