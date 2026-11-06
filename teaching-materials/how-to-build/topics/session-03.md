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
use one conda environment for the whole course, `open-water-data`, set up from the HydroShare resource. Interactive
time (live coding and "Now you try it", 54 minutes) is longer than slide time (36 minutes).

| # | Topic | Source | Where | Min | What the slides should show or do |
|---|---|---|---|---|---|
| 1 | Session title | – | deck | 1 |  |
| 2 | Program schedule | – | deck | 1 | Session 3 outlined |
| 3 | Lesson objectives | 03/00 § Learning objectives | deck | 1 | Learning objectives for today, exactly these two (Module 3's main objectives with the other two products removed): "Adapt provided Python scripts to retrieve data from NASA SWOT using their recommended APIs and libraries." and "Select the most appropriate programmatic approach for downloading data at large temporal and spatial scales for different hydrologic applications." |
| 4 | Why how you get the data matters | 03/00 § Module overview, § The lessons | deck | 3 | The module's purpose, the lessons standing alone, then a statement slide: how you get it matters too |
| 5 | APIs and agency libraries | 03/00 § Important concepts and terminology; 03/01 § RiverSP time series with `hydrocron` | deck | 3 | Concept code: a `hydrocron` request is a URL plus parameters, then the same request as one URL and what it returns. Then why agency libraries are the better starting point |
| 6 | The example rivers | 03/00 § The example rivers | deck | 1 | Ohio at Louisville in the lessons; Willamette at Salem for "Now you try it" |
| 7 | What you'll retrieve | 03/01 § Retrieve NASA SWOT data (intro), § RiverSP reaches with `earthaccess` | deck | 1 | `images/m03/swot-location-map.png`; defines granule; a one-line note in the speaker notes that reach IDs have a structure |
| 8 | Pick the product first | 03/01 § Choosing an access route | deck | 1 | RiverSP or Raster, by the question each answers |
| 9 | Discovery before download | 03/00 § Important concepts and terminology; 03/01 § The point-and-click equivalent | deck | 2 | Discovery vs. download; Earthdata Search screenshot, with links to Earthdata Search and SWOTViz |
| 10 | A search as code | 03/01 § Find Raster granules over the Ohio at Louisville | deck + notebook | 1 | Concept code: the same search in code, and the search becomes part of your methods |
| 11 | Ready to code | 03/01 § Make an Earthdata Login account | deck + how-to | 1 | Accounts, the HydroShare resource and its README, `open-water-data`, the check-your-setup notebook |
| 12 | Keep your password out of your code | 03/01 § Tools and environment setup | deck + notebook | 2 | The three places `earthaccess.login()` looks, and the how-to link |
| 13 | Set up your project folder | Module 1 § Project organization; 03/01 § Programmatic data downloads | deck + notebook | 1 | Module 1's numbered folders for this project; raw data apart from derived |
| 14 | Live coding 1: discovery | 03/01 § Programmatic data discovery | deck + notebook | 22 | Live-coding slide lists only the sections. The notes carry what to point out, including why 44 granules screen to 9, reading a granule name, and the Mississippi headwaters with no reaches in the box |
| 15 | Files or services | 03/00 § Important concepts and terminology; 03/01 § Programmatic data downloads | deck | 2 | `earthaccess` whole files vs. `hydrocron` just the observations you ask for; which products each serves, and that `hydrocron` has no Raster; what each scales with |
| 16 | A route that scales | 03/01 § Choosing an access route, § Temporal scaling, § Spatial scaling | deck | 4 | A schematic with locations and time on its axes and fuzzy regions for each route, one highlighted per slide, with each route's purpose and limit. `images/m03/swot-hydrocron-wse-full-record.png` after the `hydrocron` slide |
| 17 | Parallel code and rate limits | 03/01 § Parallelization; 03/00 § Important concepts and terminology | deck | 2 | Do and avoid; the `hydrocron` API key and PO.DAAC's Dask tutorial |
| 18 | Live coding 2: downloads | 03/01 § Programmatic data downloads, § Understanding what you downloaded | deck + notebook | 20 | Live-coding slide lists only the sections, including "Understanding what you downloaded". What came back is read here, on the real results, not on slides |
| 19 | Read the quality flags | 03/01 § Understanding what you downloaded, § RiverSP time series with `hydrocron`, § Raster water area with `earthaccess` | deck | 6 | Why flags are rarely 0; checking degraded values against their neighbors, with uncertainty showing; maps of the Raster flags, then what a strict filter does to the 13 April scene |
| 20 | Now you try it: the Willamette | 03/01 § Now you try it | deck + notebook | 12 | Steps for getting the series and checking it against its flags, a time series and a gridded plot; the example answer is collapsed in the notebook |
| 21 | Recap and what's next | – | deck | 1 | Three bullets; Session 4 |
| 22 | Further reading and questions | 03/01 § Further reading | deck | 2 | The lessons' external links, then open the floor for questions here (there is no separate questions slide) |
| 23 | The exact code for each step | 03/01 § Find datasets, § Find RiverSP granules over the Ohio at Louisville, § RiverSP reaches with `earthaccess`, § Raster water area with `earthaccess`, § RiverSP time series with `hydrocron` | notebook | – | Explained during live coding, not on slides |
| 24 | Bitwise decoding of the quality flags | 03/01 § Understanding what you downloaded | reading | – | The detail behind the 13 April scene |
| 25 | Release-note caveats behind the flags | 03/01 § Understanding what you downloaded | reading | – |  |
