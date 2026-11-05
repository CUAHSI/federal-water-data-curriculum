# Session 3 · Module 3, lesson 1: Retrieve NASA SWOT data

- **When:** Tue Nov 10, 2026, 2:00–3:30 pm ET (90 min)
- **Deck:** `teaching-materials/materials/slides/session-03_module-03_lesson-01_retrieve-nasa-swot-data.pptx`
- **Reading:** `teaching-materials/materials/readings/module-03_reading_federal-water-data-access-retrieval.docx` (shared by
  sessions 3–5)
- **Notebook:** `module-03_lesson-01_retrieve-nasa-swot-data.ipynb` (`materials/notebooks/`)
- **Pages:** `03/00` = `03-federal-water-data-access-retrieval/00_introduction.md`, `03/01` = `01_access_nasa_swot.md`

**Where:** `deck`, `notebook`, `reading`, `how-to`, `cut` (see session-01.md). **Min** adds up to the session
length. Live-coding rows name the notebook sections (they match the lesson headings).

The deck groups the lesson into concepts rather than following it section by section. Code stays on slides only
where it conveys a concept; the exact code is explained and practised in the notebook during live coding. Learners
use one conda environment for the whole course, `open-water-data`, set up from the HydroShare resource.

| # | Topic | Source | Where | Min | What the slides should show or do |
|---|---|---|---|---|---|
| 1 | Session title | – | deck | 1 |  |
| 2 | Program schedule | – | deck | 1 | Session 3 outlined |
| 3 | Lesson objectives | 03/00 § Learning objectives | deck | 1 | Learning objectives for today, exactly these two (Module 3's main objectives with the other two products removed): "Adapt provided Python scripts to retrieve data from NASA SWOT using their recommended APIs and libraries." and "Select the most appropriate programmatic approach for downloading data at large temporal and spatial scales for different hydrologic applications." |
| 4 | Why how you get the data matters | 03/00 § Module overview, § The lessons | deck | 3 | The module's purpose, the lessons standing alone, then a statement slide: how you get it matters too |
| 5 | APIs and agency libraries | 03/00 § Important concepts and terminology | deck | 3 | Concept code: a `hydrocron` request is a URL plus parameters. Then why agency libraries are the better starting point |
| 6 | The example rivers | 03/00 § The example rivers | deck | 2 | Ohio at Louisville in the lessons; Willamette at Salem for "Now you try it" |
| 7 | What you'll retrieve | 03/01 § Retrieve NASA SWOT data (intro) | deck | 1 | `images/m03/swot-location-map.png`; defines granule, cycle and pass |
| 8 | Pick the product first | 03/01 § Choosing an access route | deck | 2 | RiverSP or Raster, by the question each answers |
| 9 | Discovery before download | 03/00 § Important concepts and terminology; 03/01 § The point-and-click equivalent | deck | 3 | Discovery vs. download; Earthdata Search screenshot |
| 10 | A search as code | 03/01 § Find Raster granules over the Ohio at Louisville | deck + notebook | 2 | Concept code: the same search in code, and the search becomes part of your methods |
| 11 | A match isn't an observation | 03/01 § Find Raster granules over the Ohio at Louisville, § A river with no SWOT reaches: the Mississippi headwaters | deck + notebook | 5 | Results only, no code: 44 granules, most in the wrong UTM zones, screened to 9; reading a granule name; 42 Mississippi granules with 0 reaches in the box |
| 12 | Ready to code | 03/01 § Make an Earthdata Login account | deck + how-to | 2 | Accounts, the HydroShare resource and its README, `open-water-data`, the check-your-setup notebook |
| 13 | Live coding 1: discovery | 03/01 § Programmatic data discovery | deck + notebook | 16 | Live-coding slide: notebook setup cells, then sections "Find datasets" to "Find RiverSP granules over the Ohio at Louisville" |
| 14 | Files or services | 03/00 § Important concepts and terminology; 03/01 § Programmatic data downloads | deck | 3 | `earthaccess` whole files vs. `hydrocron` just the observations you ask for; how cost grows |
| 15 | A route that scales | 03/01 § Choosing an access route, § Temporal scaling, § Spatial scaling | deck | 4 | The routes, moving an outline: one place over a long record, everything in an area, very large jobs next to the data. `images/m03/swot-hydrocron-wse-full-record.png`: the full record in one request |
| 16 | Parallel code and rate limits | 03/01 § Parallelization; 03/00 § Important concepts and terminology | deck | 2 | Do and avoid |
| 17 | Live coding 2: downloads | 03/01 § Programmatic data downloads | deck + notebook | 16 | Live-coding slide: the three download sections |
| 18 | Read what came back | 03/01 § Understanding what you downloaded, § RiverSP time series with `hydrocron`, § Raster water area with `earthaccess` | deck | 9 | What one unit is and where its flag lives (not the shared-concepts table again); `images/m03/swot-hydrocron-wse-flood.png`; quality flags; `images/m03/swot-raster-water-frac.png` with the degraded 13 April scene as a spotlight build |
| 19 | Now you try it: the Willamette | 03/01 § Now you try it | deck + notebook | 7 | Task slide naming the notebook cell; the example answer is collapsed under the task in the notebook |
| 20 | Recap and what's next | – | deck | 2 | Three bullets; Session 4 |
| 21 | Further reading and questions | 03/01 § Further reading | deck | 5 | The lessons' external links, then open the floor for questions here (there is no separate questions slide) |
| 22 | The exact code for each step | 03/01 § Find datasets, § Find RiverSP granules over the Ohio at Louisville, § RiverSP reaches with `earthaccess`, § Raster water area with `earthaccess`, § RiverSP time series with `hydrocron` | notebook | – | Explained during live coding, not on slides |
| 23 | Bitwise decoding of the quality flags | 03/01 § Understanding what you downloaded | reading | – | The detail behind the 13 April scene |
| 24 | Release-note caveats behind the flags | 03/01 § Understanding what you downloaded | reading | – |  |
