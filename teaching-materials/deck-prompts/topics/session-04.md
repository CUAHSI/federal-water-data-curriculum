# Session 4 · Module 3, lesson 2: Retrieve NOAA NWM data

- **When:** Thu Nov 12, 2026, 2:00–3:30 pm ET (90 min)
- **Deck:** `teaching-materials/slides/session-04_module-03_lesson-02_retrieve-noaa-nwm-data.pptx`
- **Reading:** `teaching-materials/readings/module-03_reading_federal-water-data-access-retrieval.qmd` (shared by
  sessions 3–5)
- **Notebook:** `module-03_lesson-02_retrieve-noaa-nwm-data.ipynb` (learner bundle)
- **Pages:** `03/02` = `03-federal-water-data-access-retrieval/02_access_noaa_nwm.md`

**Where:** `deck`, `notebook`, `reading`, `how-to`, `cut` (see session-01.md). **Min** adds up to the session
length.

| # | Topic | Source | Where | Min | What the slides should show or do |
|---|---|---|---|---|---|
| 1 | Session title | – | deck | 1 | |
| 2 | Program schedule | – | deck | 1 | Session 4 outlined |
| 3 | Goals for today | – | deck | 1 | |
| 4 | What you'll retrieve | 03/02 § Retrieve NOAA NWM data (intro) | deck | 3 | `images/m03/nwm-ohio-louisville-map.png` |
| 5 | Choosing an access route | 03/02 § Choosing an access route | deck | 4 | API for today's forecasts; `hydrotools` or kerchunk for the archive |
| 6 | Tools and environment | 03/02 § Tools and environment setup | deck + how-to | 2 | What each tool is for; setup in the "How to" guide |
| 7 | Finding COMIDs with the NLDI | 03/02 § Programmatic data discovery, § Finding COMIDs with the NLDI | deck + notebook | 7 | Short code; what a COMID is; upstream navigation |
| 8 | NOAA NWM API: today's forecasts | 03/02 § NOAA NWM API: today's forecasts for a few reaches | deck + notebook | 5 | Short code and the response shape |
| 9 | Live coding 1: NLDI and the API | 03/02 § Finding COMIDs with the NLDI, § NOAA NWM API… | deck + notebook | 12 | Live-coding slide |
| 10 | `hydrotools`: past forecasts | 03/02 § `hydrotools`: past forecasts from the cloud archive | deck + notebook | 6 | Whole files are downloaded; what comes back |
| 11 | Kerchunk references | 03/02 § Kerchunk references: lazy, cloud-native reads with `xarray` | deck + notebook | 9 | Build: references → lazy dataset → one reach; ≤ 12 lines per slide |
| 12 | Live coding 2: the archive | 03/02 § `hydrotools`…, § Kerchunk references… | deck + notebook | 12 | Live-coding slide |
| 13 | Understanding what you downloaded | 03/02 § Understanding what you downloaded | deck | 7 | `images/m03/nwm-ohio-louisville-forecasts.png`; units, times, no quality flag |
| 14 | Why NWM downloads cost what they cost | 03/02 § Why NWM downloads cost what they cost | deck | 4 | One summary table (data transferred and time per route) |
| 15 | Temporal and spatial scaling | 03/02 § Temporal scaling, § Spatial scaling | deck | 4 | |
| 16 | Parallelization | 03/02 § Parallelization | deck | 1 | |
| 17 | Now you try it: the Willamette | 03/02 § Now you try it | deck + notebook | 4 | Task slide; answers in the solutions notebook |
| 18 | Recap and what's next | – | deck | 2 | |
| 19 | Final questions | – | deck | 5 | |
| 20 | NOAA's published kerchunk references | 03/02 § Kerchunk references… | notebook | – | Optional "Going further" section |
| 21 | The full cost and timing tables | 03/02 § Why NWM downloads cost what they cost | reading | – | |
| 22 | `hydrotools` troubleshooting and settings | 03/02 § `hydrotools`… | reading | – | Event loop, half-downloaded files, units, parallel downloads |
| 23 | The NWM retrospective | 03/02 § Temporal scaling | reading | – | |
| 24 | Further reading | 03/02 § Further reading | reading | – | |
