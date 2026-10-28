# Module 3 quiz: answer key (instructors only)

Quiz: `module-03_quiz_federal-water-data-access-retrieval.txt` (QTI: `.zip` of the same name). 12 questions, one
point each, 2 "select all that apply", 2 with code (Q3, Q11). About 13–15 minutes.

Answers are shuffled in Canvas (`shuffle answers: true`), so the letters below are the order in the `.txt` source,
not what learners see. Questions use the Module 3 example rivers only (Ohio River at Louisville); none mention the
Module 4 case study.

## Canvas setup after import

`text2qti` 0.8.0 always writes one allowed attempt into the QTI file, and that can't be changed from the `.txt`.
After importing the zip, set **Allowed attempts** to Unlimited and **Score to keep** to Highest (the zip already
sets highest), so the quiz matches its description. Check that code blocks, ³ superscripts and ≤ display, and that
both feedback lines show after an attempt.

## Objective coverage

Module objectives (from `03-federal-water-data-access-retrieval/00_introduction.md`), using the five sub-objectives:

| Objective | Taught in | Questions |
|---|---|---|
| O1. Explain web APIs and why agency libraries are a better starting point | Module overview (Important concepts: API, Agency libraries, Files vs. services) | 1, 2 |
| O2. Set up credentials safely with environment variables | Module overview (Authentication and API keys); each lesson, Tools and environment setup | 3, 4 |
| O3. Use discovery tools and check results before downloading | Module overview (Discovery vs. download); each lesson, Programmatic data discovery | 5, 6 |
| O4. Retrieve SWOT, NWM and WDFN data and describe what comes back | Each lesson, Programmatic data downloads; Understanding what you downloaded | 7, 8, 9 |
| O5. Choose an access pattern that scales; avoid overloading agency services | Each lesson, Choosing an access route; Best practices FAQs | 10, 11, 12 (also 2) |

By lesson: SWOT 3, 4, 5, 7, 12; NWM 2, 9, 10, 12; WDFN 4, 6, 8, 11, 12; overview 1, 2.

## Answers

| Q | Objective | Type | Correct answer | Lesson section |
|---|---|---|---|---|
| 1 | O1 | single | c) Libraries absorb API changes and handle login, paging and formats | Module overview, Agency libraries |
| 2 | O1, O5 | single | b) Files: number of files touched. Services: number of requests sent | Module overview, Files vs. services |
| 3 | O2 | single, code | b) The `os.environ[...] = "..."` line | Retrieve NASA SWOT data, Log in to earthaccess; Retrieve USGS WDFN data, Create the conda environment (key check) |
| 4 | O2 | select all | SWOT granule downloads need Earthdata Login; `hydrocron` needs no login; USGS key optional but raises rate limit | SWOT lesson, Choosing an access route and Tools; NWM lesson, Tools (no key); WDFN lesson, USGS Water Data API key |
| 5 | O3 | single | b) Screen out false matches by footprint polygon or UTM zone before downloading | Retrieve NASA SWOT data, Find Raster granules over the Ohio at Louisville |
| 6 | O3 | single | d) Some locations have more than one series; the 1995 location's gage no longer reports | Retrieve USGS WDFN data, Finding monitoring locations (which of those have daily mean discharge?) |
| 7 | O4 | single | b) Keep `reach_q` ≤ 1, check the degraded ones, and record your rule | Retrieve NASA SWOT data, RiverSP time series with `hydrocron`; Understanding what you downloaded |
| 8 | O4 | single | b) The daily mean averages the day's 15-minute values | Retrieve USGS WDFN data, Daily data |
| 9 | O4 | single | c) Two forecasts, issued at different times, of the same hour | Retrieve NOAA NWM data, Programmatic data downloads (Reference time); Understanding what you downloaded |
| 10 | O5 | single | c) Kerchunk references built once per run, ideally in the cloud | Retrieve NOAA NWM data, Why NWM downloads cost what they cost; Temporal scaling |
| 11 | O5 | single, code | c) Thousands of requests; one call with no site ID (optionally `bbox`) | Retrieve USGS WDFN data, Spatial scaling; Parallelization |
| 12 | O5 | select all | Let `earthaccess.download()` parallelize; split NWM work over files, not reaches; save data and skip re-downloads | SWOT, NWM and WDFN lessons, Parallelization |

## Notes for spot-checking

- Q3's password is a made-up placeholder, not a real credential.
- Q6's "29 rows for 27 locations" comes from the lesson's Jefferson County example; the 1995 end date (for a location
  with only one series) is invented to make the scenario concrete.
- Q10's "around 200 GB" for a month of `hydrotools` downloads is the lesson's own estimate (Temporal scaling).
