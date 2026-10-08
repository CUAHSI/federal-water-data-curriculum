# Retrieve USGS WDFN data

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

The course provides an environment file, `environments/m03-wdfn.yml` (in the course repository), with `dataretrieval` and the other packages this lesson uses:

```bash
# From the root of the course repository
conda env create -f environments/m03-wdfn.yml   # or: mamba env create -f environments/m03-wdfn.yml
conda activate m03-wdfn

# Store your token in the environment. We'll pretend the token you created is 'abc123'.
conda env config vars set API_USGS_PAT="abc123"
conda activate m03-wdfn   # re-activate so the variable takes effect

# Optional: register this environment as a Jupyter kernel
python -m ipykernel install --user --name m03-wdfn --display-name "Python (m03-wdfn)"
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

**Example: Spring snowmelt on the upper Mississippi River at USGS 05227500**

USGS 05227500 is the Mississippi River at Aitkin, MN, the same site the SWOT lesson uses. Spring snowmelt raised the river there in April and May 2026. Here is how to get its observations for spring 2026. Every function below returns a `(DataFrame, metadata)` pair. The data services (continuous values, daily values, field measurements) share these core columns, which map onto the course's shared vocabulary:

:::{admonition} TODO (dev team): Confirm after content/03-swot-raster merges
:class: attention
Confirm after content/03-swot-raster merges
:::

:::{admonition} TODO (dev team): Confirm the Aitkin site and spring 2026…
:class: attention
Confirm the Aitkin site and spring 2026 period, or name another Module 3 example
:::

| Column | Shared term | Notes |
|---|---|---|
| `monitoring_location_id` | **Location Identifier** | Agency prefix plus site number, e.g. `USGS-05227500` |
| `parameter_code` | **Variable** | `00060` = discharge, `00065` = gage height |
| `unit_of_measure` | **Variable unit** | e.g. `ft^3/s`, `ft` |
| `approval_status`, `qualifier` | **Data Quality Flags** | `Provisional` data can still change; `Approved` data have been reviewed. `qualifier` flags special conditions, for example estimated values (`[ESTIMATED]`) |
| `time`, `value` | | Continuous timestamps are in UTC; daily `time` is a calendar date |

:::{admonition} TODO (dev team): Verify whether daily dates are local-standard-time days
:class: attention
Verify whether daily dates are local-standard-time days
:::

First, ask which time series the gage records. This is discovery for a single site:

```python
site = "USGS-05227500"
series, md = waterdata.get_time_series_metadata(monitoring_location_id=site)
series[["parameter_code", "parameter_name", "statistic_id", "computation_period_identifier", "begin", "end"]]
```

```
  parameter_code        parameter_name statistic_id computation_period_identifier                     begin                       end
0          63160  Stream level, NAVD88        00011                        Points 2019-10-01 06:00:00+00:00 2026-10-07 05:30:00+00:00
1          00065           Gage height          NaN                    Water Year 1888-06-01 06:00:00+00:00 2025-07-29 05:00:00+00:00
2          00065           Gage height        00011                        Points 2007-10-01 06:00:00+00:00 2026-10-07 05:30:00+00:00
3          00060             Discharge        00003                         Daily 1945-03-01 05:00:00+00:00 2026-10-05 05:00:00+00:00
4          00045         Precipitation          NaN                        Points 2026-06-08 00:00:00+00:00 2026-10-07 05:30:00+00:00
5          00060             Discharge          NaN                    Water Year 1888-06-01 06:00:00+00:00 2025-07-29 05:00:00+00:00
6          00060             Discharge        00011                        Points 2013-10-01 05:00:00+00:00 2026-10-07 05:30:00+00:00
```

Each row is one time series. `statistic_id` `00011` with period `Points` is the continuous record (here gage height since 2007 and discharge since 2013), and `00003` with period `Daily` is the daily mean (discharge since 1945). This gage also reports `63160`, stream level relative to the NAVD88 vertical datum, which is handy for comparisons with other elevation data. Comparing it with SWOT water surface elevation needs a datum conversion, because SWOT heights are relative to a geoid model rather than NAVD88. The `Water Year` rows are annual summaries that end in 2025, and `00045` is a precipitation record added in June 2026.

:::{admonition} Partner review (NASA): dataretrieval
:class: important
Confirm the conversion needed to compare parameter 63160 (NAVD88) with SWOT `wse`.
:::

:::{admonition} Partner review (USGS): dataretrieval
:class: important
Confirm the conversion needed to compare parameter 63160 (NAVD88) with SWOT `wse`.
:::

**Continuous (instantaneous) values** are the sensor record, typically every 15 minutes. `get_continuous` accepts up to three years per call. Here we request two months of discharge and gage height together:

```python
cont, md = waterdata.get_continuous(
    monitoring_location_id=site,
    parameter_code=["00060", "00065"],  # discharge and gage height
    time="2026-04-01T00:00:00Z/2026-06-01T00:00:00Z",
)
print(cont.shape)
cont[["time", "parameter_code", "value", "unit_of_measure", "approval_status", "qualifier"]].head()
```

```
(11465, 13)
                       time parameter_code    value unit_of_measure approval_status    qualifier
0 2026-04-01 00:00:00+00:00          00065     5.61              ft        Approved         None
1 2026-04-01 00:15:00+00:00          00065     5.60              ft        Approved         None
2 2026-04-01 00:22:00+00:00          00060  1400.00          ft^3/s        Approved  [ESTIMATED]
3 2026-04-01 00:30:00+00:00          00065     5.60              ft        Approved         None
4 2026-04-01 00:45:00+00:00          00065     5.58              ft        Approved         None
```

To find the snowmelt peak, take the row with the largest value for each parameter:

```python
peaks = cont.loc[cont.groupby("parameter_code")["value"].idxmax()]
peaks[["parameter_code", "time", "value", "unit_of_measure", "approval_status"]]
```

```
     parameter_code                      time    value unit_of_measure approval_status
5722          00060 2026-05-02 02:15:00+00:00  5000.00          ft^3/s        Approved
5721          00065 2026-05-02 02:15:00+00:00     9.58              ft        Approved
```

The continuous record first reached its peak of **5,000 ft³/s**, with a gage height of **9.58 ft**, at 02:15 UTC on May 2, 2026, which is the evening of May 1 in Minnesota. Note that times are in UTC: convert them before comparing with local records. Two other things are visible above. First, the discharge and gage-height rows don't always share timestamps: during the estimated period in early April, discharge is reported every 4 hours rather than every 15 minutes. Second, discharge on April 1 is flagged `[ESTIMATED]` while gage height is not. When ice affects the relationship between stage and flow, USGS estimates discharge instead of computing it from the rating curve. The whole period is already `Approved`. Recent data are `Provisional` until USGS reviews them and may be revised ([USGS provisional data statement](https://waterdata.usgs.gov/provisional-data-statement/)), so check `approval_status` before you publish numbers.

:::{admonition} TODO (dev team): Verify that the April estimates at 05227500…
:class: attention
Verify that the April estimates at 05227500 are ice-related
:::

**Daily values** are summaries of the continuous record, here the daily mean (`statistic_id="00003"`) discharge. Note that the `time` argument can be a plain date range. We start in March to see what late-winter values look like:

```python
daily, md = waterdata.get_daily(
    monitoring_location_id=site,
    parameter_code="00060",
    statistic_id="00003",
    time="2026-03-01/2026-05-31",
)
daily = daily.sort_values("time")
print(daily["qualifier"].astype(str).value_counts().to_dict())
daily[["time", "value", "unit_of_measure", "approval_status", "qualifier"]].iloc[[0, 30, 31, 45, 60, 61, 91]]
```

```
{"['ESTIMATED']": 34}
         time   value unit_of_measure approval_status    qualifier
0  2026-03-01   786.0          ft^3/s        Approved  [ESTIMATED]
30 2026-03-31  1390.0          ft^3/s        Approved  [ESTIMATED]
31 2026-04-01  1420.0          ft^3/s        Approved  [ESTIMATED]
45 2026-04-15  2100.0          ft^3/s        Approved         None
60 2026-04-30  4780.0          ft^3/s        Approved         None
61 2026-05-01  4950.0          ft^3/s        Approved         None
91 2026-05-31  1400.0          ft^3/s        Approved         None
```

Thirty-four daily values (March 1 through early April) carry the `[ESTIMATED]` qualifier, and the rest have none. The daily mean peaked at 4,950 ft³/s on May 1, slightly below the 5,000 ft³/s continuous peak, as expected for an average. If your analysis is sensitive to estimated values, filter or flag them using `qualifier`.

**Field measurements** are the discharge and gage-height measurements that hydrographers make in person at the gage. USGS uses them to build and check the rating curve that turns the sensor's gage height into the continuous discharge record. They are the closest thing to "ground truth" for discharge:

```python
fm, md = waterdata.get_field_measurements(
    monitoring_location_id=site,
    time="2026-01-01T00:00:00Z/2026-10-01T00:00:00Z",
)
discharge_fm = fm[fm["parameter_code"] == "00060"].sort_values("time")
discharge_fm[["time", "value", "unit_of_measure", "observing_procedure", "measurement_rated", "approval_status"]]
```

```
         time   value unit_of_measure                observing_procedure measurement_rated approval_status
1  2026-02-11   776.0          ft^3/s                        Mid-section              Poor        Approved
3  2026-02-11   769.0          ft^3/s                        Mid-section              Poor        Approved
7  2026-04-15  2170.0          ft^3/s  Acoustic Doppler Current Profiler              Good        Approved
10 2026-05-14  2260.0          ft^3/s  Acoustic Doppler Current Profiler              Fair        Approved
14 2026-06-16   768.0          ft^3/s  Acoustic Doppler Current Profiler              Fair        Approved
21 2026-07-31   514.0          ft^3/s  Acoustic Doppler Current Profiler              Good        Approved
26 2026-08-26   394.0          ft^3/s  Acoustic Doppler Current Profiler              Good     Provisional
```

Field measurements include both discharge (`00060`) and gage-height (`00065`) readings; we kept only discharge. Hydrographers visited about once a month. `observing_procedure` records how each measurement was made: the February measurements used the mid-section method (likely through the ice), and the later ones used an acoustic Doppler current profiler (ADCP). `measurement_rated` is each measurement's **Data Quality Flag**: the hydrographer's own rating of its accuracy, from `Poor` in February to `Good` in April and July. The April 15 measurement (2,170 ft³/s) agrees closely with that day's daily mean from the continuous record (2,100 ft³/s). The August measurement is still `Provisional`, like the continuous record from that time.

:::{admonition} TODO (dev team): Verify the February measurement method
:class: attention
Verify — “`observing_procedure` records how each measurement was made: the February measurements used the mid-section method (likely through the ice)”
:::

:::{admonition} Partner review (USGS): dataretrieval
:class: important
Confirm the description of field measurements, measurement ratings and rating curves, including how under-ice measurements are made and rated.
:::

**A note on the legacy `nwis` module.** Many older tutorials, including the CUAHSI notebook this lesson draws on, use `dataretrieval.nwis`, which calls the legacy Water Services. You can recognize it by bare site numbers (`05227500` instead of `USGS-05227500`) and function names such as `nwis.get_dv`. `dataretrieval` now warns that `nwis.get_dv` will be removed on or after 2027-05-06. Write new code with `waterdata`, as in this lesson.

## Best practices FAQs

See sections below for answers and code examples to the following questions.

* What is the recommended way to download data for **one location across the full period of record**?
* What is the recommended way to download data across **all locations for a small time range**?
* If I am working on improving efficiency through **code parallelization**, what should I do vs avoid?

:::{admonition} Partner review (USGS): dataretrieval
:class: important
Confirm the retirement timeline for the legacy Water Services to cite here.
:::

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

## Further reading

* `dataretrieval` (Python) GitHub repo: https://github.com/DOI-USGS/dataretrieval-python
* `dataretrieval` documentation: https://doi-usgs.github.io/dataretrieval-python/
* Modernized Water Data API docs: https://api.waterdata.usgs.gov/
* NWIS Mapper (GUI): https://maps.waterdata.usgs.gov/mapper/
* USGS Water Data API keys: https://api.waterdata.usgs.gov/docs/ogcapi/keys/
* Adapted from [Notebook to Demonstrate Collecting USGS Data](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/USGS%20-%20Plotting%20Streamflow%20using%20NWIS%20DataRetrieval) by CUAHSI, CUAHSI notebooks (GPL-3.0). Its legacy `nwis` calls are ported to `waterdata` here.

:::{admonition} Partner review (USGS): Parallelization
:class: important
Confirm these recommendations, especially the guidance on concurrency and on using `last_modified` for incremental updates.
:::

:::{admonition} TODO (dev team): Verify notebook author(s) for credit
:class: attention
Verify notebook author(s) for credit
:::