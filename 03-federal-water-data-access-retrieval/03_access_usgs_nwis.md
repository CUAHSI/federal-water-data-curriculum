# Retrieve USGS NWIS streamflow data
 
USGS's National Water Information System (NWIS) is the authoritative source for observed, gauged streamflow.
 
USGS currently has two generations of that service running side by side:
 
1. **Legacy NWIS Water Services** (waterservices.usgs.gov): the original, stable API most existing tutorials and packages are built around.
2. **Modernized Water Data APIs** (api.waterdata.usgs.gov): USGS's newer replacement, covering daily values, instantaneous values, field measurements, and water quality (Samples database). USGS is actively encouraging migration to this one, and it supports API keys for higher rate limits.
This module uses the `dataretrieval` Python package, which wraps both generations.
 
1. **Programmatic data discovery**: before pulling values, you typically need a site number (an 8 to 15 digit USGS site ID). Discovery here means searching by region, HUC, or parameter rather than looking up a single known ID.
1. **Programmatic data downloads**: once you have site number(s), `dataretrieval` retrieves the actual values, daily, instantaneous, statistical, or peak-flow, depending on what you need.
If you already know your site number(s), you can skip programmatic data discovery.
 
## Tools and environment setup
 
### USGS Water Data API Token
NWIS is public and doesn't require an account for the legacy service. The modernized Water Data API works without a key too, but USGS recommends getting one for higher rate limits, so we will demonstrate that.

1. Request a USGS Water Data API Token: https://api.waterdata.usgs.gov/signup/
2. Save it in a safe place (KeyPass or other password management tool)
3. Add it as environment variable
4. Restart
 
USGS documents how keys work on its [API keys page](https://api.waterdata.usgs.gov/docs/ogcapi/keys/). Requests over the limit get an HTTP `429 Too Many Requests` error, and a key raises how many requests you can make per hour. `dataretrieval` reads the key from the `API_USGS_PAT` environment variable and sends it for you, so it never needs to appear in your code.

### Create a Conda environment

The course provides an environment file, `environments/nwis.yml` (in the course repository), with `dataretrieval` and the other packages this lesson uses:

```bash
# From the root of the course repository
conda env create -f environments/nwis.yml   # or: mamba env create -f environments/nwis.yml
conda activate fwdc-nwis

# Store your token in the environment. We'll pretend the token you created is 'abc123'.
conda env config vars set API_USGS_PAT="abc123"
conda activate fwdc-nwis   # re-activate so the variable takes effect

# Optional: register this environment as a Jupyter kernel
python -m ipykernel install --user --name fwdc-nwis --display-name "Python (fwdc-nwis)"
```

You can check that the token is available. Check only that it exists; don't print the token itself, because printed output ends up in notebooks, logs and screenshots.
```python
import os

print("API_USGS_PAT is set:", bool(os.getenv("API_USGS_PAT")))
```

## Programmatic data discovery

### dataRetrieval help:

The Water Data APIs use codes for many query arguments: `00060` is discharge and `00003` is the daily mean statistic, for example. `get_reference_table` returns the list of allowed values for each kind of code as a `pandas` DataFrame, so you can look them up in code rather than on a web page:

```python
from dataretrieval import waterdata

parameter_codes, _ = waterdata.get_reference_table("parameter-codes")
statistic_codes, _ = waterdata.get_reference_table("statistic-codes")
# Others:
agency_codes, _ = waterdata.get_reference_table("agency-codes")
aquifer_codes, _ = waterdata.get_reference_table("aquifer-codes")
aquifer_types, _ = waterdata.get_reference_table("aquifer-types")
coordinate_datum_codes, _ = waterdata.get_reference_table("coordinate-datum-codes")
huc_codes, _ = waterdata.get_reference_table("hydrologic-unit-codes")
national_aquifer_codes, _ = waterdata.get_reference_table("national-aquifer-codes")
reliability_codes, _ = waterdata.get_reference_table("reliability-codes")
site_types, _ = waterdata.get_reference_table("site-types")
topographic_codes, _ = waterdata.get_reference_table("topographic-codes")
time_zone_codes, _ = waterdata.get_reference_table("time-zone-codes")
counties, _ = waterdata.get_reference_table("counties")
states, _ = waterdata.get_reference_table("states")
```
 
Before downloading values, a common first step is to *discover* which site(s) match your question, by location, HUC, or the parameter you care about, rather than assuming you already know the exact site number.
 
A GUI approach exists here too: the [NWIS Mapper](https://maps.waterdata.usgs.gov/mapper/) lets you click around, search by location name, street address, state/territory, or even watershed regions to find sites visually. This is fine for exploring, but a programmatic discovery step keeps your work reproducible.
 
**Example: What are the USGS stream sites in the Suffolk County, MA area?**
 
```python
from dataretrieval import waterdata

site_info, md = waterdata.get_monitoring_locations(
    state_name = "Massachusetts",
    county_name = "Suffolk County",
    site_type="Stream",
)

site_info
```

This returns a GeoDataFrame with one row per monitoring location (156 at time of writing), including inactive sites. Key columns are `monitoring_location_id` (the **Location Identifier**), `monitoring_location_name`, `site_type`, `drainage_area` and `geometry` (a point you can map).
  
Once you have site number(s), move on to downloads below.
 
## Programmatic data downloads
 
### `dataretrieval`
 
**Key pieces**

* `dataretrieval.waterdata` (modernized, API key recommended for heavier use): the actively developed replacement, covering the same data types plus discrete water quality (Samples database).
* Canonical outputs are `pandas.DataFrame`s alongside a metadata object describing the query, similar in spirit to hydrotools' canonical columns for NWM/NWIS joins.

**Example: Which Suffolk County, MA stream sites have daily mean discharge?**
 
```python
sites_available, md = waterdata.get_combined_metadata(
  state_name = "Massachusetts",
  county_name = "Suffolk County",
  site_type= "Stream",
  parameter_code = "00060", # discharge parameter code
  statistic_id = "00003" # mean statistic code
)
```

`get_combined_metadata` combines monitoring-location details with the list of time series each location records. At time of writing, it returns two Suffolk County stream sites with daily mean discharge.

**Example: The December 2025 Skagit River flood at USGS 12200500**

Module 4 uses one gage, USGS 12200500 (Skagit River near Mount Vernon, WA), to study the December 2025 atmospheric-river flood. Here is how to get its observations. Every function below returns a `(DataFrame, metadata)` pair. The data services (continuous values, daily values, field measurements) share these core columns, which map onto the course's shared vocabulary:

| Column | Shared term | Notes |
|---|---|---|
| `monitoring_location_id` | **Location Identifier** | Agency prefix plus site number, e.g. `USGS-12200500` |
| `parameter_code` | **Variable** | `00060` = discharge, `00065` = gage height |
| `unit_of_measure` | **Variable unit** | e.g. `ft^3/s`, `ft` |
| `approval_status`, `qualifier` | **Data Quality Flags** | `Provisional` data can still change; `Approved` data have been reviewed. `qualifier` flags things such as ice or estimated values |
| `time`, `value` | | Continuous timestamps are in UTC; daily `time` is a calendar date [TODO: verify whether daily dates are local-standard-time days] |

First, ask which time series the gage records. This is discovery for a single site:

```python
site = "USGS-12200500"
series, md = waterdata.get_time_series_metadata(monitoring_location_id=site)
series[["parameter_code", "parameter_name", "statistic_id", "computation_period_identifier", "begin", "end"]]
```

```
   parameter_code       parameter_name statistic_id computation_period_identifier                     begin                       end
0           63680       Turbidity, FNU        00002                         Daily 2016-09-20 07:00:00+00:00 2017-10-02 07:00:00+00:00
1           00010   Temperature, water        00003                         Daily 1974-02-01 07:00:00+00:00 2026-10-05 07:00:00+00:00
...
3           00065          Gage height        00011                        Points 2007-10-01 08:00:00+00:00 2026-10-07 08:15:00+00:00
...
7           00060            Discharge        00003                         Daily 1940-10-01 08:00:00+00:00 2026-10-05 07:00:00+00:00
8           00060            Discharge        00011                        Points 1988-10-01 07:00:00+00:00 2026-10-07 06:45:00+00:00
9           00065          Gage height        00003                         Daily 1988-04-11 07:00:00+00:00 2026-10-05 07:00:00+00:00
...
```

**Continuous (instantaneous) values** are the sensor record, typically every 15 minutes. `get_continuous` accepts up to three years per call. Here we request one month of discharge and gage height together:

```python
cont, md = waterdata.get_continuous(
    monitoring_location_id=site,
    parameter_code=["00060", "00065"],  # discharge and gage height
    time="2025-12-01T00:00:00Z/2026-01-01T00:00:00Z",
)
print(cont.shape)
cont[["time", "parameter_code", "value", "unit_of_measure", "approval_status", "qualifier"]].head()
```

```
(5954, 13)
                       time parameter_code     value unit_of_measure approval_status qualifier
0 2025-12-01 00:00:00+00:00          00065     14.35              ft        Approved      None
1 2025-12-01 00:00:00+00:00          00060  14700.00          ft^3/s        Approved      None
2 2025-12-01 00:15:00+00:00          00065     14.35              ft        Approved      None
3 2025-12-01 00:15:00+00:00          00060  14700.00          ft^3/s        Approved      None
4 2025-12-01 00:30:00+00:00          00065     14.34              ft        Approved      None
```

To find the flood peak, take the row with the largest value for each parameter:

```python
peaks = cont.loc[cont.groupby("parameter_code")["value"].idxmax()]
peaks[["parameter_code", "time", "value", "unit_of_measure", "approval_status"]]
```

```
     parameter_code                      time      value unit_of_measure approval_status
2177          00060 2025-12-12 08:00:00+00:00  133000.00          ft^3/s        Approved
2178          00065 2025-12-12 08:15:00+00:00      37.73              ft        Approved
```

The continuous record peaked at **133,000 ft³/s** at 08:00 UTC on December 12, 2025 (midnight Pacific time), with a gage height of **37.73 ft** fifteen minutes later. The whole month is already `Approved`. Recent data are `Provisional` until USGS reviews them and may be revised ([USGS provisional data statement](https://waterdata.usgs.gov/provisional-data-statement/)), so check `approval_status` before you publish numbers.

**Daily values** are summaries of the continuous record, here the daily mean (`statistic_id="00003"`) discharge. Note that the `time` argument can be a plain date range:

```python
daily, md = waterdata.get_daily(
    monitoring_location_id=site,
    parameter_code="00060",
    statistic_id="00003",
    time="2025-12-01/2025-12-31",
)
daily.sort_values("time")[["time", "value", "unit_of_measure", "approval_status"]].iloc[8:16]
```

```
         time     value unit_of_measure approval_status
8  2025-12-09   54100.0          ft^3/s        Approved
9  2025-12-10   62000.0          ft^3/s        Approved
10 2025-12-11  102000.0          ft^3/s        Approved
11 2025-12-12  112000.0          ft^3/s        Approved
12 2025-12-13   82400.0          ft^3/s        Approved
13 2025-12-14   69000.0          ft^3/s        Approved
14 2025-12-15   62100.0          ft^3/s        Approved
15 2025-12-16   73600.0          ft^3/s        Approved
```

**Field measurements** are the discharge and gage-height measurements that hydrographers make in person at the gage. USGS uses them to build and check the rating curve that turns the sensor's gage height into the continuous discharge record. They are the closest thing to "ground truth" for discharge:

```python
fm, md = waterdata.get_field_measurements(
    monitoring_location_id=site,
    time="2025-11-01T00:00:00Z/2026-01-31T00:00:00Z",
)
discharge_fm = fm[fm["parameter_code"] == "00060"].sort_values("time")
discharge_fm[["time", "value", "unit_of_measure", "observing_procedure", "measurement_rated", "approval_status"]]
```

```
         time     value unit_of_measure                observing_procedure measurement_rated approval_status
4  2025-11-14   43800.0          ft^3/s  Acoustic Doppler Current Profiler              Good        Approved
7  2025-12-12  111000.0          ft^3/s  Acoustic Doppler Current Profiler              Fair        Approved
13 2026-01-28   20000.0          ft^3/s  Acoustic Doppler Current Profiler              Fair        Approved
```

Field measurements include both discharge (`00060`) and gage-height (`00065`) readings; we kept only discharge. A hydrographer measured **111,000 ft³/s** with an acoustic Doppler current profiler (ADCP) on December 12, the day of the peak. `measurement_rated` is that measurement's **Data Quality Flag**: the hydrographer's own rating of its accuracy (here `Fair`, compared with `Good` for the calmer November measurement). Measurements in the middle of a large flood are hard to make, and they are exactly what anchors the top of the rating curve. That matters when we compare USGS observations to the NWM and SWOT in Module 4.

[PARTNER REVIEW: USGS] Confirm the description of field measurements and rating curves, and how the course should describe discharge accuracy for out-of-bank flows at 12200500.

**For contrast: the legacy `nwis` module.** Most older tutorials, including the CUAHSI notebook this lesson draws on, use `dataretrieval.nwis`, which calls the legacy Water Services. The same daily request looks like this:

```python
from dataretrieval import nwis

legacy_daily, legacy_md = nwis.get_dv(sites="12200500", parameterCd="00060", start="2025-12-01", end="2025-12-31")
legacy_daily.head(3)
```

```
DeprecationWarning: `nwis.get_dv` is deprecated and will be removed from `dataretrieval` on or after 2027-05-06; use `waterdata.get_daily()` instead.
                           00060_Mean 00060_Mean_cd   site_no
datetime
2025-12-01 00:00:00+00:00       14200             A  12200500
2025-12-02 00:00:00+00:00       14100             A  12200500
2025-12-03 00:00:00+00:00       13700             A  12200500
```

Notice the differences:
- a bare site number instead of `USGS-12200500`;
- legacy column names, where `00060_Mean` is the value and `00060_Mean_cd` a one-letter approval code (`A` = approved);
- the date as the index.

The values match the `waterdata` daily values (December 1–3: 14,200, 14,100 and 13,700 ft³/s). `dataretrieval` itself now warns that `nwis.get_dv` will be removed on or after 2027-05-06. Write new code with `waterdata`, and recognize the legacy pattern so you can update older code.
[PARTNER REVIEW: USGS] Confirm the retirement timeline for the legacy Water Services to cite here.
 
## Best practices FAQs
 
See sections below for answers and code examples to the following questions.
 
* What is the recommended way to download data for **one location across the full period of record**?
* What is the recommended way to download data across **all locations for a small time range**?
* If I am working on improving efficiency through **code parallelization**, what should I do vs avoid?

### Temporal scaling
 
**What is the recommended way to access data for one location but the full period of record?**

Make one request per site and leave out `time`. For daily values, `get_daily` then returns the whole record, and `dataretrieval` handles the paging. Continuous values are limited to three years per call, so request a long continuous record in three-year windows. The example below uses USGS 05427930, Dorn (Spring) Creek near Waunakee, WI, a small stream with a record that starts in 2012:
 
```python
daily_data, md = waterdata.get_daily(
    monitoring_location_id= "USGS-05427930", # Dorn (Spring) Creek at CT Highway M near Waunakee, WI
    parameter_code="00060",
    statistic_id="00003"
)

daily_data
```

At time of writing, this one request returns about 5,190 rows: one per day from July 2012 to the present. Note the `qualifier` column, where some values are marked `[ESTIMATED]`.

### Spatial scaling
 
**What is the recommended way to download data across all locations but a small time range?**

Leave out `monitoring_location_id` and set a short `time` instead. One request for one day returns that day's value for every site with daily mean discharge. Looping over thousands of site IDs one request at a time would send thousands of requests and quickly use up your rate limit. To narrow the area, add `bbox` or a list of sites rather than looping.
 
```python
nonspecific_location, md = waterdata.get_daily(
    parameter_code="00060",
    statistic_id="00003",
    time="2022-01-01", # specific date, but you can give time parameter as a bounded interval, half-bounded interval, or duration object
)

nonspecific_location
```

At time of writing, this returns about 8,700 rows, one per site, from a single request.

### Parallelization
 
If I am working on improving efficiency of my code through parallelization, what should I do vs avoid?

- **Do** ask for more in each request before reaching for parallel code. Most `waterdata` functions accept lists (several `monitoring_location_id`s or `parameter_code`s), a `bbox`, or a time interval. One request that returns 10,000 rows is cheaper for you and for USGS than 100 requests that return 100 rows each.
- **Do** use an API key (`API_USGS_PAT`) for any repeated or large workflow, and expect HTTP `429 Too Many Requests` if you go over your hourly limit.
- **Do** let `dataretrieval` handle paging (`limit` sets the page size, `max_rows` caps the total) instead of writing your own loop of requests.
- **Avoid** launching many simultaneous requests from your own threads or processes. Each request spends your rate-limit quota, and a burst of parallel calls is the quickest way to get throttled. Recent versions of `dataretrieval` can split a large pull into chunks and run them concurrently for you. Use that sparingly, and only for pulls you know are large.
- **Avoid** re-downloading the same historical record every time you run your code. Approved data rarely change, so save results to a file and only request what is new (the `last_modified` argument helps).

[PARTNER REVIEW: USGS] Confirm these recommendations, especially the guidance on concurrency and on using `last_modified` for incremental updates.
  
## Further reading
 
* `dataretrieval` (Python) GitHub repo: https://github.com/DOI-USGS/dataretrieval-python
* `dataretrieval` documentation: https://doi-usgs.github.io/dataretrieval-python/
* Modernized Water Data API docs: https://api.waterdata.usgs.gov/
* NWIS Mapper (GUI): https://maps.waterdata.usgs.gov/mapper/
* USGS Water Data API keys: https://api.waterdata.usgs.gov/docs/ogcapi/keys/
* Adapted from [Notebook to Demonstrate Collecting USGS Data](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/USGS%20-%20Plotting%20Streamflow%20using%20NWIS%20DataRetrieval) by CUAHSI, CUAHSI notebooks (GPL-3.0). Its legacy `nwis` calls are ported to `waterdata` here. [TODO: verify notebook author(s) for credit]