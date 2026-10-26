# Module 2 quiz: answer key (instructors only)

Quiz: `module-02_quiz_federal-water-data-landscape.txt` (QTI: `.zip` of the same name). 11 questions, one point
each, 2 "select all that apply". No code. About 11–13 minutes.

Answers are shuffled in Canvas (`shuffle answers: true`), so the letters below are the order in the `.txt` source,
not what learners see.

## Objective coverage

Module 2 has one objective (from `02-federal-water-data-landscape/00_introduction.md`): *Characterize the river data
products from NASA SWOT, NOAA NWM, and USGS WDFN, including relevant variables, derivation, spatial and temporal
resolution, and known limitations.* All 11 questions map to it. The table breaks it into the parts the objective
names, so you can see that each part is tested at least twice.

| Part of the objective | Taught in | Questions |
|---|---|---|
| Variables and units | Module overview (One framework; units and reference points); each "Meet" page, Terminology | 1, 5, 6 |
| Derivation | Each "Meet" page, Dataset derivation | 1, 2, 3 |
| Spatial coverage and resolution | Module overview ("Reach" means different things); Meet NASA SWOT, Spatial coverage | 7, 8 |
| Temporal coverage and resolution | Each "Meet" page, Temporal coverage; Meet NOAA NWM, Which configuration do I want? | 9, 10 |
| Known limitations, quality flags and provenance | Module overview (flags; version/provenance); each "Meet" page, Data content and Usage and support | 3, 4, 11 |

By product: SWOT 1, 4, 6, 7, 8, 9, 11; NWM 3, 4, 5, 7, 10, 11; USGS 2, 4, 5, 6, 9, 11.

## Answers

| Q | Part | Type | Correct answer | Lesson section |
|---|---|---|---|---|
| 1 | Variables, derivation | single | a) WSE, width and slope from radar; no measured discharge | Meet NASA SWOT, Dataset derivation |
| 2 | Derivation | single | b) Discharge is computed from gage height with a rating curve; few high-flow measurements | Meet USGS WDFN, Dataset derivation; Data content (Accuracy) |
| 3 | Derivation, limitations | single | b) Each model version can produce different estimates | Meet NOAA NWM, Dataset derivation; Usage and support (Change over time) |
| 4 | Quality flags | select all | SWOT `reach_q` = 1 is suspect, not wrong; USGS provisional may be revised; NWM has no per-value flag | Module overview (Data quality flags); Meet NASA SWOT, Terminology and What the data look like; Meet USGS WDFN, Terminology |
| 5 | Units | single | c) They nearly agree: 1,000 m³/s ≈ 35,300 ft³/s | Module overview (Units and reference points differ) |
| 6 | Units, vertical reference | single | c) Different vertical references, so raw values don't compare | Module overview (Units and reference points differ) |
| 7 | Spatial | single | d) Separate networks of different lengths; no one-to-one match | Module overview ("Reach" means different things) |
| 8 | Spatial resolution | single | a) A 30 m wide headwater stream | Meet NASA SWOT, Spatial coverage (Is my river wide enough?) |
| 9 | Temporal resolution | single | a) NASA SWOT RiverSP | Meet NASA SWOT, Temporal coverage; Meet NOAA NWM and Meet USGS WDFN, Temporal coverage |
| 10 | Temporal coverage | single | a) The retrospective simulation | Meet NOAA NWM, Temporal coverage (Which configuration do I want?) |
| 11 | Provenance | select all | SWOT short name and access date; NWM version, configuration and reference time; USGS service, retrieval date and approval status | Module overview (Version / provenance); each "Meet" page, Usage and support (Change over time) |

## Notes for spot-checking

- Q5 and Q6 use invented round numbers (not course data) to test unit and datum reasoning; the module overview
  uses the same 120 m vs. 20 ft illustration in Q6.
- Q9 assumes a recent storm, so the NWM analysis and USGS continuous values both exist hourly or better.
