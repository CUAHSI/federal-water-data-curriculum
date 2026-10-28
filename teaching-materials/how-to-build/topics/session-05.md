# Session 5 · Module 3, lesson 3: Retrieve USGS WDFN data

- **When:** Tue Nov 17, 2026, 2:00–3:30 pm ET (90 min)
- **Deck:** `teaching-materials/materials/slides/session-05_module-03_lesson-03_retrieve-usgs-wdfn-data.pptx`
- **Reading:** `teaching-materials/materials/readings/module-03_reading_federal-water-data-access-retrieval.docx` (shared by
  sessions 3–5)
- **Notebook:** `module-03_lesson-03_retrieve-usgs-wdfn-data.ipynb` (learner bundle)
- **Pages:** `03/03` = `03-federal-water-data-access-retrieval/03_access_usgs_wdfn.md`

**Where:** `deck`, `notebook`, `reading`, `how-to`, `cut` (see session-01.md). **Min** adds up to the session
length.

| # | Topic | Source | Where | Min | What the slides should show or do |
|---|---|---|---|---|---|
| 1 | Session title | – | deck | 1 |  |
| 2 | Program schedule | – | deck | 1 | Session 5 outlined |
| 3 | Lesson objectives | 03/00 § Learning objectives | deck | 1 | Learning objectives for today, exactly these two (Module 3's main objectives with the other two products removed): "Adapt provided Python scripts to retrieve data from USGS WDFN using their recommended APIs and libraries." and "Select the most appropriate programmatic approach for downloading data at large temporal and spatial scales for different hydrologic applications." |
| 4 | What you'll retrieve; legacy vs. modernized services | 03/03 § Retrieve USGS WDFN data (intro) | deck | 4 | `images/m03/wdfn-ohio-louisville-map.png`; why `waterdata`, not `nwis` |
| 5 | Choosing an access route | 03/03 § Choosing an access route | deck | 4 |  |
| 6 | Setup: API key and environment | 03/03 § USGS Water Data API key, § Create the conda environment | deck + how-to | 2 | Why a key; setup in the "How to" guide |
| 7 | Codes: parameters and statistics | 03/03 § Codes: parameters and statistics | deck + notebook | 4 | 00060, 00065, 00003 |
| 8 | Finding monitoring locations | 03/03 § Finding monitoring locations | deck + notebook | 8 | Short code; what comes back |
| 9 | Live coding 1: codes and locations | 03/03 § Codes…, § Finding monitoring locations | deck + notebook | 12 | Live-coding slide |
| 10 | Continuous data | 03/03 § Continuous data | deck + notebook | 4 | Three-year limit per call |
| 11 | Daily data | 03/03 § Daily data | deck + notebook | 3 |  |
| 12 | Field measurements | 03/03 § Field  measurements | deck + notebook | 3 |  |
| 13 | Plot the data | 03/03 § Plot the data | deck + notebook | 3 | `images/m03/wdfn-ohio-louisville-discharge.png` |
| 14 | Live coding 2: downloads | 03/03 § Programmatic data downloads | deck + notebook | 12 | Live-coding slide |
| 15 | Understanding what you downloaded | 03/03 § Understanding what you downloaded | deck | 7 | Approval status and qualifiers; columns and units |
| 16 | The legacy `nwis` module, for contrast | 03/03 § Retrieve USGS WDFN data (intro) | deck | 2 | Before → after: the same request both ways |
| 17 | Temporal and spatial scaling; parallelization | 03/03 § Temporal scaling, § Spatial scaling, § Parallelization | deck | 6 |  |
| 18 | Now you try it: the Willamette | 03/03 § Now you try it | deck + notebook | 4 | Task slide; answers in the solutions notebook |
| 19 | Module 3 wrap-up: three routes compared | 03/00 | deck | 2 | One slide comparing how each product is retrieved |
| 20 | Recap and what's due | – | deck | 2 | Module 3 quiz (see Canvas); the Module 3 reading |
| 21 | Further reading and questions | 03/03 § Further reading | deck | 5 | The lessons' external links, then open the floor for questions here (there is no separate questions slide) |
| 22 | The legacy `nwis` comparison in full | 03/03 § Retrieve USGS WDFN data (intro) | notebook | – | Optional "Going further" section |
| 23 | Counting qualifiers on long records | 03/03 § Understanding what you downloaded | notebook | – | Optional "Going further" section |
| 24 | The metadata object, reference tables, paging | 03/03 § Spatial scaling, § Parallelization | reading | – |  |
