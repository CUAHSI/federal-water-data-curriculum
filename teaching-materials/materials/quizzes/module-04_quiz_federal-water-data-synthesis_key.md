# Module 4 quiz: answer key (instructors only)

Quiz: `module-04_quiz_federal-water-data-synthesis.txt` (QTI: `.zip` of the same name). 12 questions, one point
each, 2 "select all that apply", 1 with code (Q8). About 13–15 minutes.

Answers are shuffled in Canvas (`shuffle answers: true`), so the letters below are the order in the `.txt` source,
not what learners see.

## Canvas setup after import

`text2qti` 0.8.0 always writes one allowed attempt into the QTI file, and that can't be changed from the `.txt`.
After importing the zip, set **Allowed attempts** to Unlimited and **Score to keep** to Highest (the zip already
sets highest), so the quiz matches its description. Check that code blocks, ³ superscripts and ≤ display, and that
both feedback lines show after an attempt.

## Objective coverage

Module objectives (from `04-federal-water-data-synthesis/00_introduction.md`), using the four sub-objectives:

| Objective | Taught in | Questions |
|---|---|---|
| O1. Compare SWOT, NWM and WDFN by coverage, timing, accuracy and quality information | Comparative overview (Spatial coverage; Temporal availability; Accuracy; Which product for which question?); case study, SWOT section | 1, 2, 9 |
| O2. Link the same river location across agencies (SWORD reach, NWM feature_id/COMID, USGS gage) | Case study, Defining the area of interest | 4, 5, 6 |
| O3. Retrieve and line up observations, forecasts and satellite data (units, vertical reference, time zone, sampling) | Case study, USGS, NWM and SWOT sections | 7, 8 |
| O4. Explain what each product can and cannot show during a flood | Comparative overview (Accuracy); case study (Field measurements; forecasts table; SWOT results; Conclusions) | 3, 10, 11, 12 |

## Answers

| Q | Objective | Type | Correct answer | Lesson section |
|---|---|---|---|---|
| 1 | O1 | single | a) NASA SWOT Raster | Comparative overview, Which product for which question? |
| 2 | O1 | select all | Field measurements near the peak with `measurement_rated`; whether the peak is above the highest measured flow | Comparative overview, Accuracy (USGS); case study, Field measurements and the limits of out-of-bank flow |
| 3 | O4 | select all | USGS peak above any measured flow; NWM gave hours of warning; SWOT near-peak pass missed the gage's reach | Case study, Conclusions (and the USGS, NWM and SWOT sections) |
| 4 | O2 | single | b) SWORD reach: a ~10 km reach. NWM `feature_id`: one NHDPlus segment. USGS ID: a single gage | Case study, Defining the area of interest (identifier table) |
| 5 | O2 | single | a) Ask the NLDI for the reach the gage is indexed to, then cross-check | Case study, Defining the area of interest |
| 6 | O2 | single | b) The center is one point on a ~10 km reach; compare centerlines with the gage | Case study, Defining the area of interest (SWORD reach paragraph and study-area map) |
| 7 | O3 | single | b) Compare changes from a common baseline pass | Case study, River water surface elevation through the event (RiverSP) |
| 8 | O3 | single, code | c) `daily`, because its dates are the gage's local days, not UTC | Case study, Starting on the ground (daily values plotted at UTC midnight) |
| 9 | O1 | single | c) Kept `reach_q` ≤ 2, then checked the degraded passes against the gage | Case study, River water surface elevation through the event (RiverSP) |
| 10 | O4 | single | c) Its 18-hour window ends at 18:00 UTC on 11 December, before the crest | Case study, Looking ahead: forecasts from NOAA NWM |
| 11 | O4 | single | c) The observed peak comes from the rating, not a measurement; NWM estimates a reach | Case study, forecasts table and the paragraph after it |
| 12 | O4 | single | c) The stage–discharge relationship at the site has changed over time | Case study, Starting on the ground (record stage without a record flow) |

## Notes for spot-checking

- Numbers in Q3, Q9–Q12 are from the case study page as accessed 2026-10-08 (all USGS values `Approved` at access).
- Q11 uses the 12Z forecast (160,000 ft³/s) so its "20%" matches the lesson's own wording.
- Q12 rests on the lesson's reading that a record stage without a record flow means the rating has shifted. USGS
  partner review of that passage is closed (the callout is gone from `dev`); Q2, Q3 and Q11 follow the reviewed wording (the peak is computed
  from stage through the rating, so it is less certain than a measurement).
- Module 4 lesson 3 (Additional Federal water data) is not tested: it is a short tour with no learning objective of
  its own.
