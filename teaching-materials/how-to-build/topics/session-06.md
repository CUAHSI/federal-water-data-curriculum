# Session 6 · Module 4: Synthesizing federal water data

- **When:** Thu Nov 19, 2026, 2:00–4:00 pm ET (120 min, with a 5-minute break)
- **Deck:** `teaching-materials/materials/slides/261119_lplatt_open-water-data_module-04_federal-water-data-synthesis.pptx`
- **Reading:** none for this cohort
- **Notebook:** `module-04_federal-water-data-synthesis.ipynb` plus `module_04_helpers.py`, side by side in the HydroShare resource (built locally, never committed)
- **Pages (source material only; this cohort can't see the website, so nothing learners see points to it):** `04/00` =
  `04-federal-water-data-synthesis/00_introduction.md`, `04/01` = `01_comparative_overview.md`, `04/02` =
  `02_synthesize_river_data.md`

**Where:** `deck`, `notebook`, `reading`, `how-to`, `cut` (see session-01.md). **Min** adds up to the session
length.

Reworked on 2026-11-18 (grill-me with Lindsay). The session no longer walks through a three-product flood case study.
Published studies combine these products in pairs, not all three at once, so the session teaches the **skills for
combining** them, each with a small example on the Skagit River near Mount Vernon, WA (USGS-12200500), December 2025:
linking locations, lining up time, units and variables, and vertical references. Retrieval is hidden in `module_04_helpers.py`
(Module 3's routes as functions); each helper returns `(data, info)` with values in native units. Uncertainty and
provenance are not separate skills (Modules 1–3 cover them); the SWORD-version point sits in linking. Scaling is not
covered. 04/03 is cut.

| # | Topic | Source | Where | Min | What the slides should show or do |
|---|---|---|---|---|---|
| 1 | Session title | – | deck | 1 | Module 4, Synthesizing federal water data, Nov 19; Lindsay Platt and Kimberlee Wong |
| 2 | Program schedule | – | deck | 1 | Highlight on Nov 19; past modules and sessions greyed out |
| 3 | Session objectives | new (not 04/00) | deck | 1 | Four skill-based objectives: link a gage to its NWM and SWOT reach by ID and by distance in a shared CRS; line up observations, forecasts and passes in time; convert units and decide which variables compare; explain why products on different vertical references are compared as changes, and how a conversion is done |
| 4 | What doesn't line up | 04/01 § Side-by-side comparison | deck | 3 | Table: location ID, variable, unit, time, vertical reference, version across SWOT, NWM, WDFN. Each row maps to a skill |
| 5 | Setup: `module_04_helpers.py` | new | deck + notebook | 2 | Import of the five helpers and `get_usgs` (lightly trimmed) with line-by-line comments: each helper returns `(data, info)` with values in native units. Underscores in the file name, since Python can't import hyphens |
| 6 | Ready to code | – | deck + how-to | 2 | Notebook and `module_04_helpers.py` in one folder (pynhd adds a harmless `cache/` folder), `open-water-data` kernel, Earthdata Login (Raster), optional USGS key, the place |
| 7 | Skill 1: link locations | 04/02 § Defining the area of interest | deck | 3 | Three IDs for one place (gage, COMID 24270288, SWORD reach 78310800031); three methods: by ID, by geometry, by grid; link through the gage: the one product that pairs with both others (SWOT and NWM share no variable yet; may change as SWOT Level 4 discharge matures). Given SWORD reach IDs (PO.DAAC Hydrocron Skagit tutorial) |
| 8 | By ID: gage to COMID | 04/02 § Defining the area of interest | deck + notebook | 2 | `NLDI().getfeature_byid("nwissite", site)` → 24270288 |
| 9 | Each product's location and CRS | new | deck | 3 | Table: USGS point, NLDI line, Hydrocron GeoJSON LineString, Raster grid in UTM 10N (EPSG:32610) |
| 10 | By geometry: distances in meters | new (tested 2026-11-18) | deck + notebook | 3 | `to_crs(32610)` + `.distance`: 7 m to …031, 1,148 m to …021 |
| 11 | A reach ID belongs to a SWORD version | PO.DAAC SWOT Version D release note; USGS ScienceBase SWOT–gage pairs | deck | 3 | Table of the three gages' reach IDs in v16 and v17b; NASA's release note: SWOT moved from SWORD v16 to v17b and "V17b has new reach definitions", so the same stretch can carry a different ID (this gage: 78310800021 in v16, 78310800031 in v17b); record the SWOT product and SWORD versions with every reach ID; Hydrocron returns `sword_version` "17b" |
| 12 | SWORD and NHDPlus are different lines | new (deck-only strip schematic) | deck | 2 | Strip in the style of the time schematic: km along SWORD v17b reach 78310800031 (11.0 km, `line.project` in UTM 10N); rows for SWOT (the one reach), NWM (the 9 overlapping COMIDs, 24270288 in bold) and USGS (gage at km 9.8); two short lines: one-to-many, no crosswalk or shared variable yet. Figure deck-only (not in `images/`) |
| 13 | By grid: cut the Raster around the gage | 04/02 § Water extent… | deck + notebook | 2 | pyproj point → EPSG:32610 (`always_xy=True`: x = longitude, y = latitude), `.sel` box. One 12 Dec granule (72 MB, ~30 s). Basin-polygon clipping (NLDI basin + rioxarray) only as a prepared answer in the notes |
| 14 | Live coding 1: link the locations | – | deck + notebook | 11 | Sections: setup, by ID, one CRS, distances, map, Raster clip |
| 15 | Break (no slide) | – | – | 5 | No slide (Lindsay removed the break slide); call it at the end of live coding 1 |
| 16 | Skill 2: line up time | 04/02 § Looking ahead…, § A view from above… | deck | 4 | Two short lines plus a deck-only schematic in UTC: USGS 15-minute ticks, three NWM issue times with hourly valid times, a SWOT pass matched to the nearest gage value; zoom panel: the RiverSP file name's time range (08:57:19–09:05:08 on 12 Dec) vs. the reach's own `time_str` (…021 at 09:00:49): match the reach's time |
| 17 | Skill 3: units and variables | 04/01 table | deck | 4 | Table: discharge with discharge (× 35.3147), water level with water level; NWM has no water level, SWOT no discharge |
| 18 | Skill 4: vertical references | 04/02 § RiverSP; 04/00 § Common units and references | deck | 3 | Text plus a deck-only vertical-datum schematic (not to scale) at Mount Vernon: NAVD88 zero; gage datum 1.16 m above it; EGM2008 zero about 1.2 m above NAVD88 (gage datum ~0.04 m below it); water surface; gage height from the gage datum, SWOT wse from the geoid; the ≈1.2 m offset in an accent color, with VDatum (1.23 m at Concrete) as the source in the notes; convert or compare changes; two lines: to convert, NOAA VDatum (the tool NASA points to); ready-made, the USGS ScienceBase SWOT–gage pairs on EGM2008 (a subset of gages). The former approaches slide is folded in here (sources in the notes) |
| 19 | Live coding 2: time, units and vertical references | – | deck + notebook | 40 | Notebook sections in order: NWM forecasts at the COMID; Label NWM times as UTC; Convert m³/s to ft³/s; Forecasts on the gage record; The gage value at each SWOT pass; Each product's vertical reference; VDatum at Concrete; Gage datum to EGM2008 with VDatum; Change since 1 December: gage and SWOT; SWOT changes on the gage's changes. VDatum works at Concrete and errors west of about −122.15° (Mount Vernon), so a saved value (computed with PROJ/pyproj) is used there |
| 20 | Now you try it: the Willamette | Module 3 example river | deck + notebook | 1 | One slide; the exercise is in the notebook only: skills 1–3 at Salem (USGS-14191000), Feb–Mar 2026, answers collapsed |
| 21 | Today's recap | – | deck | 3 | One line per skill |
| 22 | Additional content from this pilot | 02/02 forcings; dataretrieval README; USGS Water Data Blog 2026-10-28 | deck | 6 | NWM forcings (HRRR/RAP short range, GFS medium range + NBM in v3.0, AORC retrospective); `parallel_chunks(n)` with n ≤ 10; USGS STAC Parquet `/continuous` and `/daily` for bulk pulls, the regular API for recent values. Links: `parallel_chunks(n)` → dataretrieval-python README section; "New STAC collections" → the USGS Water Data Blog post; a bullet linking diagrams of each NWM configuration and its forcings, by Irene Garousi-Nejad (CUAHSI), on HydroShare |
| 23 | Final assessment: combine open federal water data | assessment design (Canvas page) | deck | 3 | One line (pick a question, get the data, combine, submit code and README in Canvas, explain in a 10-minute demo); table of questions × products × skills (no options/place column; places are on Canvas): 1 NWM lead time (1A French Broad, Asheville NC, Sep 2024; 1B Winooski, Essex Junction VT, Jul 2024), 2A do SWOT water-level changes follow the gage-height changes? (SWOT reaches + USGS gage height; Missouri, Omaha NE, May–Jul 2024), 2B do SWOT water levels match the gage on the same vertical reference? (+ NOAA VDatum; Mississippi, Thebes IL, Jun–Sep 2024), 3 water at high flow, SWOT Raster (3A Pearl, Bogalusa LA, Feb 2025; 3B Sacramento, Verona CA, Feb 2024), 4A crest down the Delaware, Montague → Trenton NJ, Dec 2023, 4B SWOT full record at Baton Rouge LA; a Skills column (1 past NWM forecasts, issue vs. valid time, units; 2A matching passes, changes; 2B datum conversion; 3 Raster, CRS, clipping; 4A many gages and reaches at once; 4B long record in several requests); footer: choose by products, repeats fine, options 3 and 4A take longer, 4–5 hours at most; answering the question is a bonus, we assess gathering, combining and explaining. No download routes named |
| 24 | What you hand in and show | assessment design (Canvas page) | deck | 2 | Left: submit in Canvas: code (notebook with outputs, or script + figure PNG; module_04_helpers.py if used), environment (file or note), README from the template with a Publishing plan (per dataset: a copy of the values or download instructions + citation, and whether the product can change between downloads; derived data to provide; Module 1); no credentials in code. Right: demo in rubric order, 10 min max, step 5 = reproducibility and publishing; no slides, walk through the notebook or script and README. Bottom: Dec 1 peer review; Dec 3 demos, Canvas submission by end of day; pass = average ≥ 3 (Proficient); details on Canvas. Notes: criteria 1–4 scored in the demo, criterion 5 (reproducibility and provenance) scored after Dec 3 from the Canvas submission; IDs on Canvas, peer groups by option, demos mixed, certificate = 100% on 4 quizzes + passing assessment by end of Dec 3, released Dec 4 |
| 25 | What's due and what's next | – | deck | 3 | Module 4 quiz opens at the end of the session, closes Dec 3; 100% on all 4 for the certificate; Dec 1 peer review, Dec 3 demos |
| 26 | Further reading and questions | – | deck | 7 | External sources only (incl. NOAA Ocean Service "What is the geoid?"), then questions |
| – | 04/01 lesson (coverage, timing, accuracy, recommendations) | 04/01 | cut | – | Covered by Modules 2–3; only the comparison rows are used (topic 4) |
| – | 04/03 lesson (SWOTViz, SoS, AORC, USDA/USACE) | 04/03 | cut | – |  |

## Website follow-ups (for the later website update; not done yet)

- **04/00:** replace the learning objectives with the session's four skill-based objectives; update the module overview
  (no longer a three-product case study; 04/03 not taught).
- **04/02:** restructure from the flood story into skills (setup helpers, linking, time, units and variables, vertical
  references); add the CRS table, the distance check (closes the "SWORD spatial lookup" and gage-reach distance TODOs),
  the SWORD Version C/D renumbering, the VDatum example and conversion approaches; drop the Module 4 environment file
  in favor of `open-water-data`; keep `md` instead of `_`.
- **04/01 and 04/03:** decide their role on the website (taught content now covers only the comparison rows).
- Session 5 follow-up already listed elsewhere: 03/03 "request only what's new" wording.
