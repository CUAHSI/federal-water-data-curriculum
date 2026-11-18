# Session 6 · Module 4: Synthesizing federal water data

- **When:** Thu Nov 19, 2026, 2:00–4:00 pm ET (120 min, with a 5-minute break)
- **Deck:** `teaching-materials/materials/slides/261119_lplatt_open-water-data_module-04_federal-water-data-synthesis.pptx`
- **Reading:** none for this cohort
- **Notebook:** `module-04_federal-water-data-synthesis.ipynb` plus `helpers.py`, side by side in the HydroShare resource (built locally, never committed)
- **Pages (source material only; this cohort can't see the website, so nothing learners see points to it):** `04/00` =
  `04-federal-water-data-synthesis/00_introduction.md`, `04/01` = `01_comparative_overview.md`, `04/02` =
  `02_synthesize_river_data.md`

**Where:** `deck`, `notebook`, `reading`, `how-to`, `cut` (see session-01.md). **Min** adds up to the session
length.

Reworked on 2026-11-18 (grill-me with Lindsay). The session no longer walks through a three-product flood case study.
Published studies combine these products in pairs, not all three at once, so the session teaches the **skills for
combining** them, each with a small example on the Skagit River near Mount Vernon, WA (USGS-12200500), December 2025:
linking locations, lining up time, units and variables, and vertical references. Retrieval is hidden in `helpers.py`
(Module 3's routes as functions); each helper returns `(data, info)` with values in native units. Uncertainty and
provenance are not separate skills (Modules 1–3 cover them); the SWORD-version point sits in linking. Scaling is not
covered. 04/03 is cut.

| # | Topic | Source | Where | Min | What the slides should show or do |
|---|---|---|---|---|---|
| 1 | Session title | – | deck | 1 | Module 4, Synthesizing federal water data, Nov 19; Lindsay Platt and Kimberlee Wong |
| 2 | Program schedule | – | deck | 1 | Highlight on Nov 19 |
| 3 | Session objectives | new (not 04/00) | deck | 1 | Four skill-based objectives: link a gage to its NWM and SWOT reach by ID and by distance in a shared CRS; line up observations, forecasts and passes in time; convert units and decide which variables compare; explain why products on different vertical references are compared as changes, and how a conversion is done |
| 4 | What doesn't line up | 04/01 § Side-by-side comparison | deck | 3 | Table: location ID, variable, unit, time, vertical reference, version across SWOT, NWM, WDFN. Each row maps to a skill |
| 5 | Setup: `helpers.py` | new | deck + notebook | 2 | Import of the five helpers, one call and its `info` record. Notes: `md.query_time` is the request duration, not when it was made |
| 6 | Ready to code | – | deck + how-to | 2 | Notebook and `helpers.py` in one folder (pynhd adds a harmless `cache/` folder), `open-water-data` kernel, Earthdata Login (Raster), optional USGS key, the place |
| 7 | Skill 1: link locations | 04/02 § Defining the area of interest | deck | 3 | Three IDs for one place (gage, COMID 24270288, SWORD reach 78310800031); three methods: by ID, by geometry, by grid; link through the gage. Given SWORD reach IDs (PO.DAAC Hydrocron Skagit tutorial) |
| 8 | By ID: gage to COMID | 04/02 § Defining the area of interest | deck + notebook | 2 | `NLDI().getfeature_byid("nwissite", site)` → 24270288 |
| 9 | Each product's location and CRS | new | deck | 3 | Table: USGS point, NLDI line, Hydrocron GeoJSON LineString, Raster grid in UTM 10N (EPSG:32610) |
| 10 | By geometry: distances in meters | new (tested 2026-11-18) | deck + notebook | 3 | `to_crs(32610)` + `.distance`: 7 m to …031, 1,148 m to …021 |
| 11 | A reach ID belongs to a SWORD version | USGS ScienceBase SWOT–gage pairs | deck | 3 | Mount Vernon = 78310800021 in Version C (SWORD v16), 78310800031 in Version D (v17b); Sedro-Woolley and Concrete shift too. Hydrocron returns `sword_version` 17b |
| 12 | SWORD and NHDPlus are different lines | new | deck | 2 | One-to-many (≈10 km SWORD reaches vs. shorter flowlines), no published crosswalk, no shared variable: link through the gage. Explained only, no code |
| 13 | By grid: cut the Raster around the gage | 04/02 § Water extent… | deck + notebook | 2 | pyproj point → EPSG:32610, `.sel` box. One 12 Dec granule (72 MB, ~30 s). Basin-polygon clipping (NLDI basin + rioxarray) only as a prepared answer in the notes |
| 14 | Live coding 1: link the locations | – | deck + notebook | 11 | Sections: setup, by ID, one CRS, distances, map, Raster clip |
| 15 | Break | – | deck | 5 |  |
| 16 | Skill 2: line up time | 04/02 § Looking ahead…, § A view from above… | deck | 4 | UTC everywhere (NWM times unlabeled); reference vs. valid time, plot forecasts at valid time; nearest 15-minute gage value to each overpass |
| 17 | Skill 3: units and variables | 04/01 table | deck | 4 | Table: discharge with discharge (× 35.3147), water level with water level; NWM has no water level, SWOT no discharge |
| 18 | Live coding 2: time and units | – | deck + notebook | 21 | NWM short range 11 Dec 00Z/12Z/18Z at COMID 24270288 (~45 s), UTC labels, m³/s → ft³/s, forecasts on the gage record, gage value at each pass |
| 19 | Skill 4: vertical references | 04/02 § RiverSP; 04/00 § Common units and references | deck | 3 | Gage datum 3.8 ft NAVD88; SWOT on EGM2008; convert or compare changes |
| 20 | Converting: the approaches | new | deck | 4 | NOAA VDatum and the McQuillan GDAL workflow (what NASA points to); USGS ScienceBase pairs (subset of gages, 1 km buffer + manual review, VDatum with epoch and tide corrections); our pyproj test: stated accuracy 1.25–2.25 m, method choice moved the answer ~0.35 m, so "a meter or more of uncertainty" |
| 21 | VDatum in code | CUAHSI LongProfileVerticalDatum notebook | deck + notebook | 3 | Three steps (datum elevation + datum; NAVD88 → EGM2008 at the gage; gage height in m + converted datum); `region=contiguous`, GEOID18, short timeout, saved fallback |
| 22 | Live coding 3: vertical references | – | deck + notebook | 12 | VDatum or saved value, changes since 1 Dec, SWOT vs. gage changes |
| 23 | Now you try it: the Willamette | Module 3 example river | deck + notebook | 1 | One slide; the exercise is in the notebook only: skills 1–3 at Salem (USGS-14191000), Feb–Mar 2026, answers collapsed |
| 24 | Today's recap | – | deck | 3 | One line per skill |
| 25 | Additional content from this pilot | 02/02 forcings; dataretrieval README; USGS Water Data Blog 2026-10-28 | deck | 6 | NWM forcings (HRRR/RAP short range, GFS medium range + NBM in v3.0, AORC retrospective); `parallel_chunks(n)` with n ≤ 10; USGS STAC Parquet `/continuous` and `/daily` for bulk pulls, the regular API for recent values |
| 26 | Final assessment | – | deck | 5 | Placeholder until Lindsay designs it (Nov 18 evening) |
| 27 | What's due and what's next | – | deck | 3 | Module 4 quiz opens at the end of the session, closes Dec 3; 100% on all 4 for the certificate; Dec 1 peer review, Dec 3 demos |
| 28 | Further reading and questions | – | deck | 7 | External sources only, then questions |
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
