# Session 4 · Module 3, lesson 2: Retrieve NOAA NWM data

- **When:** Thu Nov 12, 2026, 2:00–3:30 pm ET (90 min), then office hours after 3:30 pm ET
- **Deck:** `teaching-materials/materials/slides/session-04_module-03_lesson-02_retrieve-noaa-nwm-data.pptx`
- **Reading:** `teaching-materials/materials/readings/module-03_reading_federal-water-data-access-retrieval.docx` (shared by
  sessions 3–5)
- **Notebook:** `module-03_lesson-02_retrieve-noaa-nwm-data.ipynb` (`materials/notebooks/`)
- **Pages:** `03/00` = `03-federal-water-data-access-retrieval/00_introduction.md`, `03/02` = `02_access_noaa_nwm.md`;
  the opening figure is from `02/02` = `02-federal-water-data-landscape/02_meet_noaa_nwm.md`

**Where:** `deck`, `notebook`, `reading`, `how-to`, `cut` (see session-01.md). **Min** adds up to the session
length. Live-coding rows name the notebook sections (they match the lesson headings).

The deck follows Session 3's shape, so learners meet the same steps in the same order: discovery, a live-coding
stretch, how the routes differ and scale, a second live-coding stretch, what came back, then "Now you try it".
Session 3 introduced the module, APIs and agency libraries, so the opening is short: it starts from Module 2's
timeline of the NWM configurations instead. Code stays on slides only where it conveys a concept; the exact code is
explained and practised in the notebook during live coding. Interactive time (live coding and "Now you try it",
54 minutes) is longer than slide time (36 minutes). Office hours follow the session, after 3:30 pm ET.

| # | Topic | Source | Where | Min | What the slides should show or do |
|---|---|---|---|---|---|
| 1 | Session title | – | deck | 1 |  |
| 2 | Program schedule | – | deck | 1 | Session 4 outlined |
| 3 | Lesson objectives | 03/00 § Learning objectives | deck | 1 | Learning objectives for today, exactly these two (Module 3's main objectives with the other two products removed, and "code" in place of the page's "scripts"): "Adapt provided Python code to retrieve data from NOAA NWM using their recommended APIs and libraries." and "Select the most appropriate programmatic approach for downloading data at large temporal and spatial scales for different hydrologic applications." |
| 4 | Where we left off: the NWM configurations | 02/02 § Data content; 03/02 § Retrieve NOAA NWM data (intro) | deck | 3 | Module 2's "All the configurations on one timeline" build (`images/m02/02_meet_noaa_nwm-ohio-configurations.png`), copied from the Session 2 deck: the strips alone, the full figure, then Short-Range, Medium-Range and Long-Range highlighted in turn. Skip the Retrospective and Analysis & Assimilation steps: the notes say today is about forecasts, and the retrospective is a different product |
| 5 | From the configurations to the data | 03/02 § Retrieve NOAA NWM data (intro) | deck | 1 | One slide: the same two steps as Session 3 (discovery finds the COMID, download gets the forecast values); one NetCDF file per forecast hour covering every reach; today's forecasts from the API, past ones from the archive |
| 6 | The example rivers | 03/00 § The example rivers; 03/02 § Finding COMIDs with the NLDI, § Now you try it | deck | 2 | Session 3's map slide, with each river's COMID in place of its SWORD reach ID (`10164004`, `23791093`) |
| 7 | Discovery: find the COMID | 03/02 § Programmatic data discovery, § Finding COMIDs with the NLDI | deck | 4 | The point-and-click equivalent (NWPS map: screenshot of a clicked reach and its ID), then concept code: `feature_byloc` for the Louisville point, the same lookup as one NLDI URL, then what a COMID is and upstream navigation with `images/m03/nwm-ohio-louisville-map.png` |
| 8 | Ready to code | 03/02 § Tools and environment setup | deck + how-to | 1 | The notebook, the `open-water-data` kernel, no account or key today; the `hydrotools` cell is optional (memory) |
| 9 | Live coding 1: find the reach | 03/02 § Programmatic data discovery, § Finding COMIDs with the NLDI | deck + notebook | 14 | Live-coding slide lists only the sections: define your query, a point, a monitoring site, every reach upstream, the map. The notes carry what to point out, including that the gage ID only names the location |
| 10 | Reading NWM times | 03/02 § Programmatic data downloads | deck | 1 | Configuration, reference time (UTC, `00Z`, `t00z` in file names) and valid time, with each route's column names. Module 2 defined the two times; this is the vocabulary the code uses |
| 11 | Files or services | 03/02 § Choosing an access route, § Programmatic data downloads | deck | 2 | One table: the NOAA NWM API, `hydrotools` and kerchunk references, by what each gives you, what it covers, what it returns and what it scales with |
| 12 | Why NWM downloads cost what they cost | 03/02 § Why NWM downloads cost what they cost | deck | 4 | A statement slide (cost grows with forecast runs, not reaches; one chunk per hour holds all 2,776,734 reaches), then one summary table (data transferred and time per route, 1 and 498 reaches) |
| 13 | A route that scales | 03/02 § Choosing an access route, § Temporal scaling, § Spatial scaling | deck | 4 | Session 3's schematic, redrawn for the NWM: how many reaches across, which forecast runs (the last few days, a few past runs, many past runs) up, fuzzy regions for the API, `hydrotools` and kerchunk, one highlighted per slide with its purpose and limit. The bands run the full width because reaches don't drive the cost. The kerchunk slide's notes point to the retrospective for a long simulated record |
| 14 | Parallelization | 03/02 § Parallelization, § Spatial scaling | deck | 2 | Do and avoid: parallelize over files, not reaches; one call with every COMID; let `hydrotools` handle its downloads; a small thread pool for building references; run next to the data |
| 15 | Live coding 2: get NWM forecasts | 03/02 § Programmatic data downloads, § Understanding what you downloaded | deck + notebook | 26 | Live-coding slide lists only the sections, including "Understanding what you downloaded". Start the optional `hydrotools` cell and talk while it runs. What came back is read here, on the real results, not on slides |
| 16 | No quality flag: record what you used | 03/02 § Understanding what you downloaded | deck | 4 | Why there is no per-value flag, what to record and cite instead (version, configuration, reference times, archive, access date), then `images/m03/nwm-ohio-louisville-forecasts.png`: runs disagree, so look at several |
| 17 | Now you try it: the Willamette | 03/02 § Now you try it | deck + notebook | 14 | Learners follow along in the notebook's "Now you try it" section (no time limit on the slide). The lesson's three steps; the example answer is collapsed in the notebook |
| 18 | Recap and what's next | – | deck | 1 | What each route is for; Session 5 |
| 19 | Further reading and questions | 03/02 § Further reading | deck | 4 | The lesson's external links (this cohort can't see the lesson pages), then open the floor for questions here (there is no separate questions slide) |
| 20 | Office hours | – | deck | 0 | The last slide, after 3:30 pm ET: stay on with questions about the notebook, setup or your own river |
| 21 | The exact code for each step | 03/02 § Finding COMIDs with the NLDI, § NOAA NWM API: today's forecasts for a few reaches, § `hydrotools`: past forecasts from the cloud archive, § Kerchunk references: lazy, cloud-native reads with `xarray` | notebook | – | Explained during live coding, not on slides |
| 22 | NOAA's published kerchunk references | 03/02 § Kerchunk references: lazy, cloud-native reads with `xarray` | notebook | – | Optional "Going further" section |
| 23 | The full cost and timing tables | 03/02 § Why NWM downloads cost what they cost | reading | – | Peak memory, the reference build, and the medium-range member |
| 24 | `hydrotools` troubleshooting and settings | 03/02 § `hydrotools`: past forecasts from the cloud archive, § Parallelization | reading | – | Half-downloaded files, timeouts on slow connections, units, categorical columns, `limit`, `timeout` and `group_size` |
| 25 | The NWM retrospective | 03/02 § Temporal scaling | reading | – |  |
| 26 | Other services: NWPS API and the CIROH BigQuery API | 03/02 § Retrieve NOAA NWM data (intro), § Choosing an access route | cut | – | Named in the lesson but not used in it |
