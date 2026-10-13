# Module overview

In Module 2 you met three Federal water data products: NASA Surface Water and Ocean Topography (SWOT) satellite observations, NOAA National Water Model (NWM) streamflow simulations and forecasts, and the stream gage observations published by USGS Water Data for the Nation (WDFN). This module is about getting those data into your own code: finding what exists (_discovery_) and retrieving it (_download_ or _access_), using the tools each agency recommends.

Getting the data is only half of the goal. How you get it matters too. A workflow that downloads a whole national file to read one value, or that sends thousands of requests where a few would do, wastes your time and loads shared agency systems. It also tends to break when those systems change, which creates support work for the agencies. The access patterns researchers use are often out of step with what data providers recommend. Each lesson therefore ends with best practices for scaling across **time** (one place, a long record) and **space** (many places, a short window), and for parallel code. We hope you will pass these practices on to others in the water community.

## Learning objectives

By the end of this module, learners should be able to:
- Adapt provided Python scripts to retrieve data from NASA SWOT, NOAA NWM, and USGS WDFN using their recommended APIs and libraries.
- Select the most appropriate programmatic approach for downloading data at large temporal and spatial scales for different hydrologic applications.

These break down into:
- Explain what a web API is, and why agency-maintained Python libraries (`earthaccess`, `hydrotools`, `dataretrieval`) are usually a better starting point than calling the API directly.
- Set up credentials (NASA Earthdata login, USGS API key) safely, using environment variables rather than writing secrets into code.
- Use each agency's discovery tools to find which datasets, river reaches, files or monitoring locations cover a place and time, and check that the results are what you expect before downloading.
- Retrieve SWOT, NWM and WDFN data for a location of interest, and describe what comes back using the shared concepts below.
- Choose an access pattern that scales with your question (one location over a long record, versus many locations over a short window), and avoid patterns that overload agency services.

## The lessons

The lessons stand alone: each one covers one product, with its own examples and its own software environment, so you can take them in any order or only the one you need.

1. [Retrieve NASA SWOT data](01_access_nasa_swot.md): river reach time series with PO.DAAC's `hydrocron` service (nodes work the same way), and whole data files (granules) with `earthaccess`. Environment: `environments/m03-swot.yml`.
2. [Retrieve NOAA NWM data](02_access_noaa_nwm.md): finding reach IDs (COMIDs) with the NLDI, and streamflow forecasts through the NOAA NWM API, `hydrotools` and kerchunk references. Environment: `environments/m03-nwm.yml`.
3. [Retrieve USGS WDFN data](03_access_usgs_wdfn.md): monitoring locations, continuous values, daily values and field measurements with `dataretrieval`'s `waterdata` module. Environment: `environments/m03-wdfn.yml`.

Each lesson follows the same structure, so once you know one, you can find your way around the others:

1. **Introduction:** what you'll retrieve, with a link to the matching Module 2 page and, where there's more than one tool, a table to help you choose an access route.
2. **Tools and environment setup:** accounts or keys you need, and the lesson's conda environment file (in `environments/` in the course repository).
3. **Programmatic data discovery:** the point-and-click (GUI) way to explore, then the code that does the same thing reproducibly.
4. **Programmatic data downloads:** retrieving values, and what comes back.
5. **Understanding what you downloaded:** the shared concepts below, for the actual output.
6. **Best practices FAQs:** temporal scaling, spatial scaling and parallelization.
7. **Now you try it:** the same steps on a second river, with the answer you should get.
8. **Further reading.**

## The example rivers

All three lessons use the same two rivers, chosen because every product has good data there.

| Role | River | Example period |
|---|---|---|
| Main example in each lesson | **Ohio River at Louisville, Kentucky** | Spring 2025, including a large flood in early April |
| "Now you try it" | **Willamette River at Salem, Oregon** | February–March 2026, winter high flows |

The Ohio at Louisville is a large, wide river (about 700 m across), which suits satellite measurements, model reaches and stream gages alike. The Willamette at Salem is much narrower (about 150 m), so it's a good test of how each product handles a smaller river.

## One framework for three products

Each agency has its own vocabulary: a SWOT *granule*, an NWM *COMID*, a USGS *monitoring location*. Underneath, every product answers the same questions. The course describes all three with the same seven shared concepts, and each lesson's "Understanding what you downloaded" section walks through them for its own output:

| Shared concept | Question it answers | SWOT | NWM | WDFN |
|---|---|---|---|---|
| {term}`Location identifier` | *Where* is this value? | `reach_id`, `node_id` (from {term}`SWORD`) | {term}`COMID` / `feature_id` (from {term}`NHDPlus`) | {term}`monitoring location ID <Monitoring location ID>` (e.g. `USGS-03294500`) |
| {term}`Variable` | *What* was measured or modeled? | water surface elevation, width, … | streamflow | discharge, gage height, … |
| {term}`Variable unit` | In what units? | m, m/km, m³/s | m³/s | ft³/s, ft |
| {term}`Time` | *When*, and how often? | overpass time | forecast reference time + valid time | timestamp (continuous / daily) |
| {term}`Data quality flag(s)` | How much should I trust it? | `reach_q`, `wse_qual`, … | none per value (model output) | approval status (provisional / approved), qualifiers |
| {term}`Version / provenance` | Which release, from where? | product version (e.g. `D`), collection DOI | model version (e.g. v3.0), run configuration | service, retrieval date |
| {term}`Data unit` | What is one "file" or record? | {term}`granule <Granule>` | one output file per timestep | one time series per location + parameter |

## Important concepts and terminology

- **{term}`API`** (application programming interface). A web API is a set of URLs that return data, rather than web pages, in response to a request. A request is usually a base URL plus _query parameters_. For example, the PO.DAAC `hydrocron` API takes a reach ID, a start time and an end time, and returns a table. Your browser, `curl` or Python's `requests` can all send requests.
- **Agency libraries.** Python packages such as `earthaccess` (NASA-supported), `hydrotools` (NOAA Office of Water Prediction) and `dataretrieval` (USGS) wrap these APIs. They handle authentication, paging and file formats, and return familiar objects like `pandas` DataFrames. APIs change: endpoints move, parameters are renamed, and old services retire. When that happens, the library is updated, and your code often keeps working after a simple upgrade. Code that calls URLs directly has to be fixed by hand. USGS's move from the legacy Water Services to the modernized Water Data APIs is a current example.
- **Discovery vs. download.** Discovery queries _metadata_ (which sites, files or time ranges exist) and is cheap. Download retrieves the data values themselves and can be expensive. Always discover first, check what you found, and then download only what you need.
- **Authentication and {term}`API keys <API key>`.** Some services need an account (NASA Earthdata login), and some work without one but give higher limits with a key (the USGS Water Data APIs). Keep credentials in environment variables or a `.netrc` file, never in code, notebooks or version control.
- **Rate limits and paging.** Services limit how many requests you can make in a period of time. Going over typically returns an HTTP `429 Too Many Requests` error. Large results are split into _pages_. Agency libraries page for you, but each page still counts as a request.
- **Files vs. services.** Some data are best retrieved as whole files (SWOT granules, NWM output files) and some through a query service that returns only the rows you ask for (`hydrocron`, the USGS Water Data APIs). Knowing which one you are using tells you how cost grows: with the number of files touched, or with the number of requests sent.
- **Scaling and cloud-native access.** Very large analyses often run fastest _next to the data_: on a cloud computer in the same region as the archive, streaming only the needed parts of files instead of downloading them. The SWOT and NWM lessons point out when this is worth it. Service-based access, such as the USGS Water Data APIs, returns only the rows you ask for, so where your code runs matters much less.
- **Reproducibility.** Every lesson pins a {term}`conda environment <Conda environment>`, keeps its query (places, IDs, dates, codes) in variables, names the data version it used, keeps raw downloads separate from derived results, and shows how to cite the data. These ideas come from Module 1: [Open Science](../01-data-best-practices/01_open_science.md), [Data Management](../01-data-best-practices/02_data_management.md) and [Data Publishing](../01-data-best-practices/03_data_publishing.md).

:::{admonition} Partner review (NASA): Important concepts and terminology
:class: important
Confirm the module framing about access patterns and provider recommendations, and the description of each agency's preferred tools.
:::

:::{admonition} Partner review (NOAA): Important concepts and terminology
:class: important
Confirm the module framing about access patterns and provider recommendations, and the description of each agency's preferred tools.
:::

:::{admonition} Partner review (USGS): Important concepts and terminology
:class: important
Confirm the module framing about access patterns and provider recommendations, and the description of each agency's preferred tools.
:::
