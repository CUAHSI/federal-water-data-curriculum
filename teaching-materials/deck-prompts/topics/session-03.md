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
| 1 | Session title | – | deck | 1 |  |
| 2 | Program schedule | – | deck | 1 | Session 3 outlined |
| 3 | Lesson objectives | 03/00 § Learning objectives | deck | 1 | Learning objectives for today, exactly these two (Module 3's main objectives with the other two products removed): "Adapt provided Python scripts to retrieve data from NASA SWOT using their recommended APIs and libraries." and "Select the most appropriate programmatic approach for downloading data at large temporal and spatial scales for different hydrologic applications." |
| 4 | Module 3 overview | 03/00 § Module overview | deck | 2 |  |
| 5 | The three lessons, each standing alone | 03/00 § The lessons | deck | 1 |  |
| 6 | The example rivers | 03/00 § The example rivers | deck | 2 | Ohio at Louisville in the lessons; Willamette at Salem for "Now you try it" |
| 7 | One framework, retrieval view | 03/00 § One framework for three products | deck | 3 | The shared-concepts table again, now with the retrieval column |
| 8 | Important concepts and terminology | 03/00 § Important concepts and terminology | deck | 5 | API, granule, cloud-native formats, lazy loading; one term per slide or a build |
| 9 | What you'll retrieve | 03/01 § Retrieve NASA SWOT data (intro) | deck | 2 | `images/m03/swot-location-map.png` |
| 10 | Choosing an access route | 03/01 § Choosing an access route | deck | 4 | The routes and when to use each (build: highlight the route the lesson uses) |
| 11 | Setup: Earthdata Login and the lesson's environment | 03/01 § Make an Earthdata Login account, § Create the lesson's environment | deck + how-to | 2 | One slide: what's needed and that the "How to" guide walks through it |
| 12 | The point-and-click equivalent | 03/01 § The point-and-click equivalent | deck | 1 | Earthdata Search screenshot |
| 13 | Find datasets | 03/01 § Find datasets | deck + notebook | 2 | Short code (≤ 12 lines) and what comes back |
| 14 | A river with no SWOT reaches | 03/01 § A river with no SWOT reaches: the Mississippi headwaters | deck + notebook | 2 | Why an empty result is an answer |
| 15 | Find Raster granules over the Ohio | 03/01 § Find Raster granules over the Ohio at Louisville | deck + notebook | 3 |  |
| 16 | Find RiverSP granules over the Ohio | 03/01 § Find RiverSP granules over the Ohio at Louisville | deck + notebook | 2 |  |
| 17 | Live coding 1: discovery | 03/01 § Programmatic data discovery | deck + notebook | 12 | Live-coding slide: notebook sections "Find datasets" to "Find RiverSP granules over the Ohio at Louisville" |
| 18 | RiverSP reaches with `earthaccess` | 03/01 § RiverSP reaches with `earthaccess` | deck + notebook | 3 |  |
| 19 | Raster water area with `earthaccess` | 03/01 § Raster water area with `earthaccess` | deck + notebook | 4 | `images/m03/swot-raster-water-frac.png` |
| 20 | RiverSP time series with `hydrocron` | 03/01 § RiverSP time series with `hydrocron` | deck + notebook | 4 | `images/m03/swot-hydrocron-wse-flood.png` |
| 21 | Live coding 2: downloads | 03/01 § Programmatic data downloads | deck + notebook | 12 | Live-coding slide: the three download sections |
| 22 | Understanding what you downloaded | 03/01 § Understanding what you downloaded | deck | 6 | Columns, units and quality flags; the degraded 13 April scene as a spotlight build |
| 23 | Best practices: temporal scaling | 03/01 § Temporal scaling | deck | 2 | `images/m03/swot-hydrocron-wse-full-record.png`: the full record in one request |
| 24 | Best practices: spatial scaling and parallelization | 03/01 § Spatial scaling, § Parallelization | deck | 2 |  |
| 25 | Now you try it: the Willamette | 03/01 § Now you try it | deck + notebook | 4 | Task slide naming the notebook cell; answers are in the solutions notebook |
| 26 | Recap and what's next | – | deck | 2 | Three bullets; Session 4 |
| 27 | Further reading and questions | 03/01 § Further reading | deck | 5 | The lessons' external links, then open the floor for questions here (there is no separate questions slide) |
| 28 | Bitwise decoding of the quality flags | 03/01 § Understanding what you downloaded | reading | – | The detail behind the 13 April scene |
| 29 | Release-note caveats behind the flags | 03/01 § Understanding what you downloaded | reading | – |  |
