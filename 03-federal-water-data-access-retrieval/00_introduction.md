# Module overview

In Module 2 you met three Federal water data products: NASA SWOT water surface elevation, NOAA National Water Model (NWM) streamflow, and USGS streamflow observations. This module is about getting those data into your own code: finding what exists (_discovery_) and retrieving it (_download_ or _access_), using the tools each agency recommends.

Getting the data is only half of the goal. How you get it matters too. A workflow that downloads a whole national file to read one value, or that sends thousands of requests where a few would do, wastes your time and loads shared agency systems. It also tends to break when those systems change, which creates support work for the agencies. The access patterns researchers use are often out of step with what data providers recommend. Each lesson therefore ends with best practices for scaling across **time** (one place, a long record) and **space** (many places, a short window), and for parallel code. We hope you will pass these practices on to others in the water community.

Each agency lesson follows the same structure:

1. **Tools and environment setup:** accounts or keys you need, and a conda environment file (`environments/*.yml` in the course repository) with everything the lesson uses.
2. **Programmatic data discovery:** the point-and-click (GUI) way to explore, then the code that does the same thing reproducibly.
3. **Programmatic data downloads:** retrieving values, and what comes back (columns, units, quality flags).
4. **Best practices FAQs:** temporal scaling, spatial scaling and parallelization.

The examples in this module use the upper Mississippi River in Minnesota (and a few other sites). In Module 4, you will apply the same access patterns together in a flood case study.

## Learning objectives

By the end of this module, learners should be able to:
- Adapt provided Python scripts to retrieve data from NASA SWOT, NOAA NWM, and USGS WDFN using their recommended APIs and libraries.
- Select the most appropriate programmatic approach for downloading data at large temporal and spatial scales for different hydrologic applications.

These break down into:
- Explain what a web API is, and why agency-maintained Python libraries (`earthaccess`, `dataretrieval`, `hydrotools`) are usually a better starting point than calling the API directly.
- Set up credentials (NASA Earthdata login, USGS API key) safely, using environment variables rather than writing secrets into code.
- Use each agency's discovery tools to find which datasets, sites, river reaches or files cover a place and time, and check that the results are what you expect before downloading.
- Retrieve SWOT, NWM and USGS data for a location of interest, and describe what comes back: the Location Identifier, Variable, Variable unit and Data Quality Flag(s).
- Choose an access pattern that scales with your question (one location over a long record, versus many locations over a short window), and avoid patterns that overload agency services.

## Important concepts and terminology

- **API (Application Programming Interface).** A web API is a set of URLs that return data, rather than web pages, in response to a request. A request is usually a base URL plus _query parameters_. For example, the PO.DAAC `hydrocron` API takes a reach ID, a start time and an end time, and returns a table. Your browser, `curl` or Python's `requests` can all send requests.
- **Agency libraries.** Python packages such as `earthaccess` (NASA-supported), `dataretrieval` (USGS) and `hydrotools` (NOAA OWP) wrap these APIs. They handle authentication, paging and file formats, and return familiar objects like `pandas` DataFrames. APIs change: endpoints move, parameters are renamed, and old services retire. When that happens, the library is updated, and your code often keeps working after a simple upgrade. Code that calls URLs directly has to be fixed by hand. USGS's move from the legacy Water Services to the modernized Water Data APIs is a current example.
- **Discovery vs. download.** Discovery queries _metadata_ (which sites, files or time ranges exist) and is cheap. Download retrieves the data values themselves and can be expensive. Always discover first, check what you found, and then download only what you need.
- **Authentication and API keys.** Some services need an account (NASA Earthdata login), and some work without one but give higher limits with a key (the USGS Water Data API). Keep credentials in environment variables or a `.netrc` file, never in code, notebooks or version control.
- **Rate limits and paging.** Services limit how many requests you can make in a period of time. Going over typically returns an HTTP `429 Too Many Requests` error. Large results are split into _pages_. Agency libraries page for you, but each page still counts as a request.
- **Files vs. services.** Some data are best retrieved as whole files (SWOT granules, NWM output files) and some through a query service that returns only the rows you ask for (`hydrocron`, the USGS Water Data API). Knowing which one you are using tells you how cost grows: with the number of files touched, or with the number of requests sent.
- **Scaling and cloud-native access.** Very large analyses often run fastest _next to the data_: on a cloud computer in the same region as the archive, streaming only the needed parts of files instead of downloading them. The SWOT and NWM lessons point out when this is worth it. Service-based access, such as the USGS Water Data API, returns only the rows you ask for, so where your code runs matters much less.

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

