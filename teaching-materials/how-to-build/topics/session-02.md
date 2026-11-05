# Session 2 · Module 2: The federal water data landscape

- **When:** Thu Nov 5, 2026, 2:00–4:00 pm ET (120 min, no break)
- **Deck:** `teaching-materials/materials/slides/261105_lplatt_open-water-data_module-02_federal-water-data-landscape.pptx`
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
| 6 | How each page is organized | 02/00 § How each page is organized | deck | 1 | The four things to watch for |
| 7 | The course's example rivers | 02/00 § The course's example rivers | deck | 3 | `images/m02/00_introduction-course-rivers-map.png`; which river each module uses |
| 8 | Meet NASA SWOT: who makes it and why | 02/01 § Meet NASA SWOT (intro) | deck | 2 | Section divider, then one slide on the mission |
| 9 | SWOT terminology | 02/01 § Terminology | deck | 4 | One shared-framework table for both river products, with (RiverSP) or (Raster) next to what's unique, and an italic line under it saying SWORD is the river network RiverSP uses. The table defines reach, node, pass and granule, so they don't get their own slide. WSE units say "above the geoid". Raster details come from the Module 3 SWOT lesson |
| 10 | How SWOT values are made | 02/01 § Dataset derivation | deck | 4 | Orbits and versions; product names carry the version (RiverSP and Raster short names and DOIs, with what L2 means in the notes); a statement slide on the Level 4 discharge estimates |
| 11 | Where SWOT sees | 02/01 § Spatial coverage | deck | 3 | River widths: 100 m to plan on, about 50 m not guaranteed, about 30 m is the SWORD network and not what SWOT observes. The notes walk through all three and use the Ohio (about 700 m) and the Mississippi headwaters (no SWORD reaches) as examples |
| 12 | When SWOT sees | 02/01 § Temporal coverage | deck | 1 | Revisit pattern, record start and release time, on the orbits slide |
| 13 | What SWOT data look like, and the quality flags | 02/01 § Data content | deck | 12 | One question for each product: Raster, "where was the water?" (`images/m03/swot-raster-water-frac.png`), and RiverSP, "how high was the river?" (`images/m03/swot-location-map.png`, then `images/m02/01_meet_nasa_swot-ohio-reach-wse.png` as a spotlight build). Visuals for the flags: pixel → node → reach, and the flag counts for this reach (*deck only*); the notes give the 0–3 scale. Accuracy and limitations |
| 14 | Using SWOT data: citation and access routes | 02/01 § Usage and support | deck | 4 | How to cite, with a formatted example; the access routes; what PO.DAAC is |
| 15 | Activity 1: can SWOT answer this? | 02/01 § Spatial coverage; 02/01 § Temporal coverage; 02/01 § Dataset derivation | deck | 4 | Activity slide with three short scenarios that each hide a different limit: a 300 m river with no gage that may have overflowed its banks; a 70 m river in SWORD wanted weekly for a year; a 150 m river with a one-day flash flood whose hydrograph you want to recreate. Learners answer Yes, Maybe or No and name the limit. Then the answers, one per slide (Yes if a pass caught it; Maybe; No) |
| 16 | Meet NOAA NWM: who makes it and why | 02/02 § Meet NOAA NWM (intro) | deck | 2 | Section divider, then one slide |
| 17 | NWM terminology | 02/02 § Terminology | deck | 4 | NWM in the shared framework; reference time and valid time with `images/m03/nwm-ohio-louisville-forecasts.png` |
| 18 | Where the NWM runs: NHDPlus reaches | 02/02 § Spatial coverage | deck | 3 | One slide with `images/m03/nwm-ohio-louisville-map.png`: extent, NHDPlus, COMID and `feature_id`, one value per reach, and no coordinates in the output |
| 19 | How NWM values are made | 02/02 § Dataset derivation | deck | 4 | Two slides: values are model output, and what a configuration is; then no quality flag, so version and configuration matter. The notes say observations only come in at the start. Leave out the Texas comparison: it isn't one of the course rivers |
| 20 | Retrospective vs. forecasts; the configurations | 02/02 § Temporal coverage | deck | 9 | The configuration table, with no build: the notes say it is for reference and that archived forecasts aren't the retrospective. Then `images/m02/02_meet_noaa_nwm-ohio-configurations.png` at full size under a thin title bar: first with the hydrograph covered, to explain the strips along the top, then the whole figure, then the Retrospective highlighted |
| 21 | Reading the configurations figure | 02/02 § Data content | deck | 5 | The same figure, with one configuration highlighted per slide: Analysis & Assimilation, Short-Range, Medium-Range, Long-Range. No comparison with the gage: that's Module 4 |
| 22 | Using NWM data: citation and access routes | 02/02 § Usage and support | deck | 4 | No DOI for operational forecasts; NOAA's format with worked examples for a retrospective and a forecast. Access: the NOAA NWM API for current forecasts, Google Cloud back to September 2018 for past forecasts, and separate public datasets for the retrospective |
| 23 | Activity 2: pick the configuration | 02/02 § Temporal coverage | deck | 4 | Activity slide with four short scenarios; then the answers, one per slide. Question 4 is the next 8 hours using the most recent forecast (Short-Range): the answer says Medium- and Long-Range also cover those hours but update less often |
| 24 | Meet USGS WDFN: who makes it and why | 02/03 § Meet USGS WDFN (intro) | deck | 2 | Section divider; NWIS → WDFN in one slide |
| 25 | WDFN terminology | 02/03 § Terminology | deck | 5 | WDFN in the shared framework; monitoring location, parameter code, statistic: daily values are often the mean, but can be another statistic such as the maximum; `images/m03/wdfn-ohio-louisville-map.png`, with the notes explaining that it shows one county, so nothing appears across the river |
| 26 | How discharge is made | 02/03 § Dataset derivation | deck | 4 | Gage height → rating curve → discharge; rating curve from the field measurements at Louisville (*deck only*) |
| 27 | Where WDFN measures | 02/03 § Spatial coverage | deck | 2 |  |
| 28 | How far back records go | 02/03 § Temporal coverage | deck | 2 |  |
| 29 | What WDFN data look like: approval status | 02/03 § Data content | deck | 4 | `images/m02/03_meet_usgs_wdfn-ohio-daily-approval.png`; provisional vs. approved; qualifiers |
| 30 | Using WDFN data: citation and access routes | 02/03 § Usage and support | deck | 2 | How to cite, with a formatted example; API keys and limits |
| 31 | Activity 3: read a WDFN record | 02/03 § Dataset derivation; 02/03 § Data content | deck | 10 | No hydrograph: a table of real WDFN values at Louisville (*deck only*): continuous gage height and discharge at the April 2025 crest, the daily mean, the field measurement, and one `ESTIMATED` daily value. Questions: which values were measured directly and which calculated; why the continuous and daily values differ; which is most likely to change. Then the answers, one per slide. About WDFN only: comparing the products is Module 4 |
| 32 | Where this leads | 02/00 § Where this leads | deck | 1 | Module 3 retrieves each product |
| 33 | Recap and what's due | – | deck | 2 | A table of what each product is useful for: length of record, resolution in time, resolution in space, direct or derived. Not a list of quality flags. Then the Module 2 quiz and the technical setup |
| 34 | Further reading and questions | 02/01–03 § Further reading | deck | 5 | The lessons' external links, one slide per product in two columns, then open the floor for questions here (there is no separate questions slide) |
| 35 | Full citation text for each product | 02/01–03 § Usage and support | reading | – | The exact citation strings and DOIs, so learners can copy them |
| 36 | How the session's figures were made | – | cut | – | The figure scripts stay on the lesson pages. No code on Module 2 slides or in its reading |
