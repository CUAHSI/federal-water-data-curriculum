# Session 2 · Module 2: The federal water data landscape

- **When:** Thu Nov 5, 2026, 2:00–4:00 pm ET (120 min, no break)
- **Deck:** `teaching-materials/materials/slides/session-02_module-02_federal-water-data-landscape.pptx`
- **Reading:** `teaching-materials/materials/readings/module-02_reading_federal-water-data-landscape.docx`
- **Pages:** `02/00` = `02-federal-water-data-landscape/00_introduction.md`, `02/01` = `01_meet_nasa_swot.md`,
  `02/02` = `02_meet_noaa_nwm.md`, `02/03` = `03_meet_usgs_wdfn.md`

**Where:** `deck`, `notebook`, `reading`, `how-to`, `cut` (see session-01.md). **Min** adds up to the session
length.

No code on these slides: Module 2 is an overview, and code starts in Module 3. New figures marked *deck only* stay out of `images/` and the lesson pages until the course lead agrees.

| # | Topic | Source | Where | Min | What the slides should show or do |
|---|---|---|---|---|---|
| 1 | Session title | – | deck | 1 |  |
| 2 | Program schedule | – | deck | 1 | Session 2 outlined |
| 3 | Lesson objectives | 02/00 § Learning objectives | deck | 1 | Learning objectives for today: the module's main objectives (the list before "These break down into"), copied word for word from the overview page |
| 4 | Module 2 overview | 02/00 § Module overview | deck | 1 | Know what a product *is* before you code against it |
| 5 | One framework for three products | 02/00 § One framework for three products | deck | 4 | The shared-concepts table (STYLE_GUIDE §1); build: one row at a time |
| 6 | How each page is organized | 02/00 § How each page is organized | deck | 2 | The four things to watch for |
| 7 | The course's example rivers | 02/00 § The course's example rivers | deck | 3 | `images/m02/00_introduction-course-rivers-map.png`; which river each module uses |
| 8 | Meet NASA SWOT: who makes it and why | 02/01 § Meet NASA SWOT (intro) | deck | 2 | Section divider, then one slide on the mission |
| 9 | SWOT terminology | 02/01 § Terminology | deck | 5 | SWOT in the shared framework; reach, node, pass, granule, product names; `images/m03/swot-location-map.png` for reaches |
| 10 | How SWOT values are made | 02/01 § Dataset derivation | deck | 3 | Measures the water surface, not discharge; orbits and versions |
| 11 | Where SWOT sees | 02/01 § Spatial coverage | deck | 3 | Coverage limits: which rivers are in SWORD |
| 12 | When SWOT sees | 02/01 § Temporal coverage | deck | 2 | Revisit pattern; record start |
| 13 | What SWOT data look like, and the quality flags | 02/01 § Data content | deck | 7 | Both products: RiverSP (`images/m02/01_meet_nasa_swot-ohio-reach-wse.png`, spotlight build) and Raster (`images/m03/swot-raster-water-frac.png`); visuals for the flags: pixel → node → reach, and the flag counts for this reach (*deck only*); accuracy and limitations |
| 14 | Using SWOT data: citation and access routes | 02/01 § Usage and support | deck | 4 | How to cite; the access routes |
| 15 | Activity 1: choose a SWOT flag threshold | 02/01 § Data content | deck | 4 | Activity slide with the flag counts for the Ohio reach; then the answers. Bounded: how many values each threshold keeps, and what else to check |
| 16 | Meet NOAA NWM: who makes it and why | 02/02 § Meet NOAA NWM (intro) | deck | 2 | Section divider, then one slide |
| 17 | NWM terminology | 02/02 § Terminology | deck | 6 | NWM in the shared framework; configuration, reference time, NHDPlus and COMIDs; `images/m03/nwm-ohio-louisville-map.png` for reaches, `images/m03/nwm-ohio-louisville-forecasts.png` for reference vs. valid time |
| 18 | How NWM values are made | 02/02 § Dataset derivation | deck | 3 | Model versions matter. Leave out the Texas comparison: it isn't one of the course rivers |
| 19 | Where the NWM runs | 02/02 § Spatial coverage | deck | 2 |  |
| 20 | Retrospective vs. forecasts; which configuration | 02/02 § Temporal coverage | deck | 7 | The configuration table first, with no build: the notes say it is for reference, summarize it briefly and move on. Then explain the configurations with `images/m02/02_meet_noaa_nwm-ohio-configurations.png`, then "Which configuration do I want?" |
| 21 | What NWM forecasts look like | 02/02 § Data content | deck | 5 | `images/m02/02_meet_noaa_nwm-ohio-medium-range.png`; no per-value quality flag |
| 22 | Using NWM data: citation and access routes | 02/02 § Usage and support | deck | 4 |  |
| 23 | Activity 2: pick the NWM configuration | 02/02 § Temporal coverage | deck | 4 | Activity slide with four short scenarios; then the answers, one per slide |
| 24 | Meet USGS WDFN: who makes it and why | 02/03 § Meet USGS WDFN (intro) | deck | 3 | Section divider; NWIS → WDFN in one slide |
| 25 | WDFN terminology | 02/03 § Terminology | deck | 5 | WDFN in the shared framework; monitoring location, parameter code, statistic: daily values are often the mean, but can be another statistic such as the maximum; `images/m03/wdfn-ohio-louisville-map.png` |
| 26 | How discharge is made | 02/03 § Dataset derivation | deck | 4 | Gage height → rating curve → discharge; rating curve from the field measurements at Louisville (*deck only*) |
| 27 | Where WDFN measures | 02/03 § Spatial coverage | deck | 2 |  |
| 28 | How far back records go | 02/03 § Temporal coverage | deck | 2 |  |
| 29 | What WDFN data look like: approval status | 02/03 § Data content | deck | 6 | `images/m02/03_meet_usgs_wdfn-ohio-daily-approval.png`; provisional vs. approved |
| 30 | Using WDFN data: citation and access routes | 02/03 § Usage and support | deck | 4 |  |
| 31 | Activity 3: the peak of a historic flood in WDFN data | 02/03 § Data content | deck | 10 | Activity slide with `images/m03/wdfn-ohio-louisville-discharge.png`: April 2025 at Louisville, what discharge data can and can't tell you, and what other data to use. Then the answers. About WDFN only: comparing the products is Module 4 |
| 32 | Where this leads | 02/00 § Where this leads | deck | 1 | Module 3 retrieves each product |
| 33 | Recap and what's due | – | deck | 2 | Three bullets; Module 2 quiz (see Canvas); the Module 2 reading |
| 34 | Further reading and questions | 02/01–03 § Further reading | deck | 5 | The lessons' external links, then open the floor for questions here (there is no separate questions slide) |
| 35 | Full citation text for each product | 02/01–03 § Usage and support | reading | – | The exact citation strings and DOIs, so learners can copy them |
| 36 | How the session's figures were made | – | cut | – | The figure scripts stay on the lesson pages. No code on Module 2 slides or in its reading |
