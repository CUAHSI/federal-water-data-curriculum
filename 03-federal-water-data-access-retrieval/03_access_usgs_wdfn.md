# Retrieve USGS WDFN data

USGS Water Data for the Nation ({term}`WDFN`) publishes the observations USGS collects at thousands of {term}`monitoring locations <Monitoring location ID>` across the country: river {term}`discharge <Discharge>` and {term}`gage height <Gage height>`, groundwater levels, water quality and more. This lesson shows you how to find monitoring locations and retrieve their streamflow data in Python. For what these data are, how they're collected and their limitations, start with [Meet USGS WDFN](../02-federal-water-data-landscape/03_meet_usgs_wdfn.md).

**Main example: the Ohio River at Louisville, Kentucky.** The Ohio is one of the largest rivers in the country, and at Louisville it carries the drainage of much of the Ohio Valley. In early April 2025, days of heavy rain sent it into a large spring flood. You will find the stream monitoring locations around Louisville, then retrieve the sensor record, daily values and field measurements from the gage on the Ohio, monitoring location `USGS-03294500`, for 15 March to 15 May 2025. At the end, you will repeat the steps on a second river, the Willamette at Salem, Oregon.

**A note on names.** The data you'll retrieve are stored in the National Water Information System ({term}`NWIS`), the USGS database behind WDFN. Many older tutorials say "NWIS" for the whole system, and its older web services carry that name. USGS currently runs two generations of web service side by side:

1. **Legacy Water Services** (`waterservices.usgs.gov`): the original API that most existing tutorials and packages were built on. USGS is retiring it.
2. **Modernized Water Data APIs** (`api.waterdata.usgs.gov`): USGS's replacement, covering monitoring locations, daily values, continuous values, field measurements and more. USGS encourages everyone to migrate, and it supports {term}`API keys <API key>` for higher rate limits.

This lesson uses the modernized APIs through the {term}`dataretrieval` Python package and its `waterdata` module. The steps are:

1. **Programmatic data discovery.** Before pulling values, you need the monitoring location ID (for example `USGS-03294500`) and the codes for what you want. Discovery means searching by place, parameter or other criteria rather than assuming you know the ID.
1. **Programmatic data downloads.** With IDs in hand, `dataretrieval` retrieves the values: continuous, daily or field measurements, depending on your question.

If you already know your monitoring location ID(s), you can skip discovery.

(wdfn-access-routes)=
### Choosing an access route

All the routes below use the same Water Data APIs, so the choice is mostly about *which function* matches your question. None of them needs a key, but USGS recommends one for repeated or large requests.

| Use case | Recommended route | Key needed? | Scaling limits |
|---|---|---|---|
| Explore by clicking, spot-check a site | [WDFN website](https://waterdata.usgs.gov/) and the [NWIS Mapper](https://apps.usgs.gov/nwismapper/) | No | Manual; not reproducible on its own |
| Find monitoring locations and what they record | `waterdata.get_monitoring_locations`, `get_time_series_metadata`, `get_combined_metadata` | No (key recommended) | Results come in pages; each page is one request |
| Daily values (e.g. daily mean discharge), any length of record | `waterdata.get_daily` | No (key recommended) | The whole record for a site in one call (paged for you) |
| The sensor record (every 5–15 minutes) | `waterdata.get_continuous` | No (key recommended) | Up to three years per call |
| Discharge measured by hydrographers in the field | `waterdata.get_field_measurements` | No (key recommended) | About one measurement a month per site |
| One day (or a short window) at many sites | `waterdata.get_daily` with no site, optionally a `bbox` | No (key recommended) | One request instead of thousands; mind the page count |
| Code that uses the legacy Water Services | `dataretrieval.nwis` | No | Being retired; port it to `waterdata` (see [the note below](#wdfn-legacy)) |

## Tools and environment setup

### USGS Water Data API key

The Water Data APIs work without a key, but USGS recommends one (USGS calls it a token) for higher rate limits, so this lesson uses one. If you don't have a key yet, skip this step: every example on this page runs without one, just with lower rate limits.

1. Request a key at the [USGS Water Data API signup page](https://api.waterdata.usgs.gov/signup/).
2. Save it in a safe place, such as a password manager.
3. Store it in the `API_USGS_PAT` environment variable (below).

USGS explains how keys work on its [API keys page](https://api.waterdata.usgs.gov/docs/ogcapi/keys/). Requests over the limit get an HTTP `429 Too Many Requests` error, and a key raises how many requests you can make per hour. `dataretrieval` reads the key from the `API_USGS_PAT` environment variable and sends it for you, so it never appears in your code.

### Create the conda environment

This lesson has its own {term}`conda environment <Conda environment>`, [`environments/m03-wdfn.yml`](../environments/m03-wdfn.yml), with `dataretrieval` and the other packages this lesson uses:

```bash
# From the root of the course repository
conda env create -f environments/m03-wdfn.yml   # or: mamba env create -f environments/m03-wdfn.yml
conda activate m03-wdfn

# Store your key in the environment. Replace the placeholder with your own key.
conda env config vars set API_USGS_PAT="paste-your-key-here"
conda activate m03-wdfn   # re-activate so the variable takes effect

# Optional: register this environment as a Jupyter kernel
python -m ipykernel install --user --name m03-wdfn --display-name "Python (m03-wdfn)"
```

Check that the key is available. Check only that it exists; don't print the key itself, because printed output ends up in notebooks, logs and screenshots.

```python
import os

print("API_USGS_PAT is set:", bool(os.getenv("API_USGS_PAT")))
```

```text
API_USGS_PAT is set: True
```

The environment file lets most packages float to their latest release, so a year from now you may get newer versions than the ones we tested. When you finish an analysis, record exactly what you ran with `conda env export > environment-lock.yml` and keep that file with your results ([Data Management](../01-data-best-practices/02_data_management.md), Module 1). The examples on this page were tested with Python 3.14, `dataretrieval` 1.4.0, `pandas` 3.0.6, `geopandas` 1.2.0 and `matplotlib` 3.11.2.

## Programmatic data discovery

### Codes: parameters and statistics

The Water Data APIs use codes for many query arguments. A {term}`parameter code <Parameter code>` says what was measured (`00060` is discharge, `00065` is gage height), and a statistic code says how values were summarized (`00003` is the daily mean). `get_reference_table` returns each list of codes as a `pandas` DataFrame, so you can look them up in code rather than on a web page. Like every `waterdata` function, it returns a pair, `(DataFrame, metadata)`; `_` or `md` catches the metadata:

```python
from dataretrieval import waterdata

parameter_codes, _ = waterdata.get_reference_table("parameter-codes")
statistic_codes, _ = waterdata.get_reference_table("statistic-codes")

print(parameter_codes.loc[parameter_codes["parameter_code"].isin(["00060", "00065"]),
                          ["parameter_code", "parameter_name", "unit_of_measure"]])
print(statistic_codes.loc[statistic_codes["statistic_code"].isin(["00003", "00011"])])
```

```text
   parameter_code parameter_name unit_of_measure
42          00060      Discharge           ft3/s
47          00065    Gage height              ft
   statistic_code statistic_name        statistic_description
2           00003           MEAN                  MEAN VALUES
10          00011  INSTANTANEOUS  RANDOM INSTANTANEOUS VALUES
```

`parameter_codes` has about 19,600 rows and `statistic_codes` about 3,200. Other reference tables work the same way, for example `"site-types"`, `"states"`, `"counties"`, `"hydrologic-unit-codes"` and `"agency-codes"`.

### Finding monitoring locations

**The point-and-click way.** The [WDFN website](https://waterdata.usgs.gov/) and the [NWIS Mapper](https://apps.usgs.gov/nwismapper/) let you search by place name, address, state or watershed and click on sites. That's fine for exploring. A programmatic discovery step keeps your search reproducible, so capture it in code too.

Keep what you're asking for (place, site type, codes, dates) in variables at the top of your script, rather than typing them into the middle of each call. Your query is then recorded in one spot and easy to change.

**Example: which stream monitoring locations are in Jefferson County, Kentucky (Louisville)?**

```python
# what we're asking for
STATE, COUNTY = "Kentucky", "Jefferson County"
site = "USGS-03294500"                    # Ohio River at Louisville, KY (found below)
START, END = "2025-03-15", "2025-05-15"   # the April 2025 flood

site_info, md = waterdata.get_monitoring_locations(
    state_name=STATE,
    county_name=COUNTY,
    site_type="Stream",
)
print(site_info.shape)
print(site_info[["monitoring_location_id", "monitoring_location_name", "drainage_area"]].head())
```

```text
(120, 44)
  monitoring_location_id            monitoring_location_name  drainage_area
0          USGS-02380002  STUDENT2 CREEK NEAR LOUSYVILLE, KY            NaN
1          USGS-02380003  STUDENT3 CREEK NEAR LOUISVILLE, KY            NaN
2          USGS-02380004  STUDENT4 CREEK NEAR LOUISVILLE, KY            NaN
3          USGS-02380005  STUDENT5 CREEK NEAR LOUISVILLE, KY            NaN
4          USGS-02380006  STUDENT6 CREEK NEAR LOUISVILLE, KY            NaN
```

This returns a `GeoDataFrame` with one row per monitoring location (120 on 2026-10-08) and 44 columns. Key columns are `monitoring_location_id` (the *{term}`Location identifier`*), `monitoring_location_name`, `site_type`, `drainage_area` (square miles) and `geometry` (a point you can map). The list includes inactive sites, and, as the first rows show, a few entries that aren't real gages: on 2026-10-08, ten "STUDENT" creeks and five "TEST" entries (such as "SANDY TEST NO 1" and "LOUISVILLE TEST SITE"). This is one reason to look at discovery results before you download anything.

:::{admonition} Partner review (USGS): Test entries in monitoring-location results
:class: important
Confirm what the "STUDENT… CREEK", "SANDY TEST" and "LOUISVILLE TEST SITE" monitoring locations in Jefferson County, KY are (training or test records?), and whether users should filter them out.
:::

**Example: which of those have daily mean discharge?**

`get_combined_metadata` combines monitoring-location details with the list of time series each location records, so you can filter on parameter and statistic codes in the same call:

```python
sites_with_q, md = waterdata.get_combined_metadata(
    state_name=STATE,
    county_name=COUNTY,
    site_type="Stream",
    parameter_code="00060",   # discharge
    statistic_id="00003",     # daily mean
)
print(len(sites_with_q), "time series at", sites_with_q["monitoring_location_id"].nunique(), "locations")
print(sites_with_q[["monitoring_location_id", "monitoring_location_name", "begin", "end"]].head())
```

```text
29 time series at 27 locations
  monitoring_location_id                            monitoring_location_name                     begin                       end
0          USGS-03301900    FERN CREEK AT OLD BARDSTOWN RD AT LOUISVILLE, KY 1997-09-18 04:00:00+00:00 2026-10-06 04:00:00+00:00
1          USGS-03292555  S FK BEARGRASS CK AT E BRECKINRIDGE ST AT LSVL, KY 2017-01-23 05:00:00+00:00 2022-12-18 05:00:00+00:00
2          USGS-03292480           LITTLE GOOSE CREEK NEAR HARRODS CREEK, KY 1998-12-01 05:00:00+00:00 2026-10-07 04:00:00+00:00
3          USGS-03302000                      POND CREEK NEAR LOUISVILLE, KY 1944-08-01 04:00:00+00:00 2026-10-06 04:00:00+00:00
4          USGS-03292500        SOUTH FORK BEARGRASS CREEK AT LOUISVILLE, KY 1939-12-12 05:00:00+00:00 2026-10-07 04:00:00+00:00
```

Each row is one *time series*, not one location, so a location with two daily-discharge series appears twice (here, 29 rows for 27 locations; `USGS-03292555` in row 1 is one of them). `begin` and `end` show the period each series covers: a series whose `end` is years ago belongs to a gage that no longer reports. One of these is `USGS-03294500`, Ohio River at Louisville, KY, with daily discharge from 1928 to the present.

**Map: where these locations are**

A quick map is a good check that discovery found what you meant. The river line on this map comes from the USGS {term}`NLDI` web service, which returns the stream network up- and downstream of a monitoring location as GeoJSON:

```python
import pandas as pd
import geopandas as gpd
import requests
import matplotlib.pyplot as plt

# site (Ohio River at Louisville) is set in the query block above

# leave out the 15 entries that are not real gages (names such as "STUDENT1 CREEK" or "SANDY TEST NO 1")
real = site_info[~site_info["monitoring_location_name"].str.contains("STUDENT|TEST")]
with_q = sites_with_q.drop_duplicates("monitoring_location_id")

# the Ohio River, 60 km up- and downstream of the gage (UM = upstream mainstem, DM = downstream mainstem)
parts = []
for nav in ["UM", "DM"]:
    url = f"https://api.water.usgs.gov/nldi/linked-data/nwissite/{site}/navigation/{nav}/flowlines"
    r = requests.get(url, params={"distance": 60}, timeout=120)
    r.raise_for_status()
    parts.append(gpd.GeoDataFrame.from_features(r.json()["features"], crs="EPSG:4326"))

river = pd.concat(parts)
fig, ax = plt.subplots(figsize=(7, 6))
river.plot(ax=ax, color="#2a78d6", linewidth=2)
real.plot(ax=ax, color="#b9b8b2", markersize=14, label=f"Stream monitoring locations ({len(real)})")
with_q.plot(ax=ax, color="#52514e", markersize=24, label=f"With daily mean discharge ({len(with_q)})")
gage = with_q[with_q["monitoring_location_id"] == site]
gage.plot(ax=ax, color="#eb6834", markersize=220, marker="*", edgecolor="white", linewidth=0.8, zorder=5,
          label=f"{site}, Ohio River at Louisville, KY")
ax.annotate("Ohio River", (-85.97, 38.03), fontsize=10, color="#2a78d6", style="italic")
ax.annotate("Louisville gage", gage.geometry.iloc[0].coords[0], xytext=(-100, 14), textcoords="offset points", fontsize=10)
ax.set_xlim(-86.05, -85.35)
ax.set_ylim(37.95, 38.42)
ax.set_aspect(1 / 0.786)   # roughly equal km in x and y at 38° N
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("USGS stream monitoring locations, Jefferson County, KY", fontsize=12, loc="left")
ax.legend(loc="lower right", fontsize=9)
fig.tight_layout()
fig.savefig("wdfn-ohio-louisville-map.png", dpi=150)
```

:::{figure} ../images/m03/wdfn-ohio-louisville-map.png
:alt: Map of Jefferson County, Kentucky, with the Ohio River as a blue line curving along the north and west edge. About a hundred gray and dark gray dots mark stream monitoring locations spread east of the river; an orange star marks the Louisville gage on the river.
:width: 90%

Stream monitoring locations in Jefferson County, KY (gray; 105 after removing test entries), those with a daily mean discharge record (dark gray; 27, active or not) and the Ohio River at Louisville gage, USGS-03294500 (orange star). Data: USGS Water Data APIs via `dataretrieval`; river line from the USGS NLDI. Accessed 2026-10-08.
:::

**Example: what does the Louisville gage record?**

Once you've picked a location, ask which time series it records. This is discovery for a single site:

```python
series, md = waterdata.get_time_series_metadata(monitoring_location_id=site)
print(series[["parameter_code", "parameter_name", "statistic_id", "computation_period_identifier", "begin", "end"]])
```

```text
  parameter_code       parameter_name statistic_id computation_period_identifier                     begin                       end
0          80154   Suspnd sedmnt conc        00003                         Daily 1979-10-01 04:00:00+00:00 1983-09-29 04:00:00+00:00
1          00065          Gage height        00011                        Points 2007-10-01 05:00:00+00:00 2026-10-08 06:00:00+00:00
2          00065          Gage height        00003                         Daily 1991-09-30 04:00:00+00:00 2026-10-07 04:00:00+00:00
3          00060            Discharge        00011                        Points 2009-09-21 04:00:00+00:00 2026-10-08 07:45:00+00:00
4          00045        Precipitation          NaN                        Points 2026-06-08 00:00:00+00:00 2026-10-08 06:00:00+00:00
5          00060            Discharge          NaN                    Water Year 1832-02-21 05:00:00+00:00 2024-04-17 04:00:00+00:00
6          80155  Suspnd sedmnt disch        00003                         Daily 1979-10-01 04:00:00+00:00 1983-09-29 04:00:00+00:00
7          00060            Discharge        00003                         Daily 1928-01-01 05:00:00+00:00 2026-10-06 04:00:00+00:00
8          00065          Gage height          NaN                    Water Year 1832-02-21 05:00:00+00:00 2024-04-17 04:00:00+00:00
```

Each row is one time series. `statistic_id` `00011` with period `Points` is the continuous sensor record (gage height since 2007, discharge since 2009), and `00003` with period `Daily` is the daily mean (discharge since 1928). The `Water Year` rows are annual summaries (they start in 1832, long before the sensor record), the sediment series ran only from 1979 to 1983, and `00045` is a precipitation record added in June 2026. Your `end` dates will be later.

Once you have your monitoring location ID(s) and codes, move on to downloads.

## Programmatic data downloads

Every `waterdata` function returns a `(DataFrame, metadata)` pair. The DataFrame holds the values; the metadata object records the request (`md.url`) and when it was made, which is useful when you write down how you got your data.

**{term}`Continuous values <Continuous values>`** are the sensor record, typically every 15 minutes. `get_continuous` accepts up to three years per call. Here we request two months of discharge and gage height together:

```python
# START and END (the April 2025 flood) are set in the query block above
cont, md = waterdata.get_continuous(
    monitoring_location_id=site,
    parameter_code=["00060", "00065"],    # discharge and gage height
    time=f"{START}T00:00:00Z/{END}T00:00:00Z",
)
print(cont.shape)
print(cont[["time", "parameter_code", "value", "unit_of_measure", "approval_status", "qualifier"]].head())
```

```text
(11697, 13)
                       time parameter_code     value unit_of_measure approval_status qualifier
0 2025-03-15 00:00:00+00:00          00065     16.92              ft        Approved      None
1 2025-03-15 00:00:00+00:00          00060  79900.00          ft^3/s        Approved      None
2 2025-03-15 00:15:00+00:00          00065     16.85              ft        Approved      None
3 2025-03-15 00:15:00+00:00          00060  77200.00          ft^3/s        Approved      None
4 2025-03-15 00:30:00+00:00          00065     16.80              ft        Approved      None
```

The result is a long-format `GeoDataFrame`: one row per timestamp and parameter (about 5,850 rows for each of the two parameters, every 15 minutes), with columns including `monitoring_location_id`, `parameter_code`, `statistic_id`, `time` (UTC), `value`, `unit_of_measure`, `approval_status` and `qualifier`.

To find the flood crest, take the row with the largest value for each parameter:

```python
peaks = cont.loc[cont.groupby("parameter_code")["value"].idxmax()]
print(peaks[["parameter_code", "time", "value", "unit_of_measure", "approval_status"]])
```

```text
     parameter_code                      time      value unit_of_measure approval_status
4900          00060 2025-04-09 14:30:00+00:00  719000.00          ft^3/s        Approved
4895          00065 2025-04-09 14:00:00+00:00      67.98              ft        Approved
```

The Ohio crested at **719,000 ft³/s** at 14:30 UTC on 9 April 2025 (10:30 a.m. in Louisville), with a gage height of **67.98 ft** half an hour earlier. Gage height is measured above the gage's own reference point (its datum), not from the riverbed, so it isn't the water depth. Times are in UTC: convert them before comparing with local records.

Look at `approval_status`, too. On 2026-10-08, values up to 9 April 2025 17:15 UTC were `Approved`, and everything after that was still {term}`provisional <Provisional data>`. Provisional data can still be revised when USGS reviews them ([USGS provisional data statement](https://waterdata.usgs.gov/provisional-data-statement/)), so check `approval_status` before you publish numbers, and expect values after the crest to change. No values in this window carry a `qualifier`.

**{term}`Daily values <Daily values>`** are summaries of the continuous record, here the daily mean (`statistic_id="00003"`) discharge. The `time` argument can be a plain date range:

```python
daily, md = waterdata.get_daily(
    monitoring_location_id=site,
    parameter_code="00060",
    statistic_id="00003",     # daily mean
    time=f"{START}/{END}",
)
daily = daily.sort_values("time")
print(daily["approval_status"].value_counts().to_dict())
print(daily[["time", "value", "unit_of_measure", "approval_status", "qualifier"]].iloc[[0, 17, 25, 30, 61]])
```

```text
{'Provisional': 37, 'Approved': 25}
         time     value unit_of_measure approval_status qualifier
0  2025-03-15   97000.0          ft^3/s        Approved      None
17 2025-04-01  165000.0          ft^3/s        Approved      None
25 2025-04-09  712000.0          ft^3/s     Provisional      None
30 2025-04-14  322000.0          ft^3/s     Provisional      None
61 2025-05-15  157000.0          ft^3/s     Provisional      None
```

There are 62 daily values, one per day. The daily mean peaked at 712,000 ft³/s on 9 April, slightly below the 719,000 ft³/s continuous peak, as expected for an average. That day is `Provisional` even though its morning values are approved, because the daily mean includes the provisional afternoon. Daily `time` is a calendar date, not a timestamp.

:::{admonition} TODO (dev team): Daily-value dates and time zone
:class: attention
Verify whether daily dates are local-standard-time days.
:::

**{term}`Field measurements <Field measurement>`** are the discharge and gage-height measurements that hydrographers make in person at the gage. USGS uses them to build and check the {term}`rating curve <Rating curve>` that turns the sensor's gage height into the continuous discharge record, so they are the closest thing to "ground truth" for discharge:

```python
fm, md = waterdata.get_field_measurements(
    monitoring_location_id=site,
    time="2025-01-01T00:00:00Z/2025-12-31T00:00:00Z",
)
discharge_fm = fm[fm["parameter_code"] == "00060"].sort_values("time")
print(discharge_fm[["time", "value", "unit_of_measure", "observing_procedure", "measurement_rated", "approval_status"]])
```

```text
         time     value unit_of_measure                observing_procedure measurement_rated approval_status
1  2025-01-15   68300.0          ft^3/s  Acoustic Doppler Current Profiler              Good        Approved
3  2025-02-20  606000.0          ft^3/s  Acoustic Doppler Current Profiler              Fair        Approved
5  2025-04-09  738000.0          ft^3/s  Acoustic Doppler Current Profiler              Poor        Approved
7  2025-08-14    9500.0          ft^3/s  Acoustic Doppler Current Profiler              Poor     Provisional
12 2025-12-04   46900.0          ft^3/s  Acoustic Doppler Current Profiler              Good     Provisional
```

Field measurements include both discharge (`00060`) and gage-height (`00065`) readings; we kept only discharge. In 2025, hydrographers measured discharge five times, including on the day of the crest. `observing_procedure` records how each measurement was made, here always with an acoustic Doppler current profiler (ADCP) towed across the river. `measurement_rated` is each measurement's quality rating: the hydrographer's judgment of its accuracy. The crest-day measurement (738,000 ft³/s) is rated `Poor`, which is common for measurements in fast, debris-laden flood water. It is about 3% above the continuous record's peak, well within what a `Poor` rating allows. The field measurement `time` is a date; the time of day is in a separate `time_of_day` column.

:::{admonition} Partner review (USGS): Field measurements and ratings
:class: important
Confirm the description of field measurements, measurement ratings and rating curves, and the statement that `Poor` ratings are common for flood measurements (and what accuracy each rating implies).
:::

**What the data look like.** Plotting the continuous record by approval status, with the field measurement on top, shows the flood, the crest and where provisional data begin:

```python
import matplotlib.dates as mdates

fig, ax = plt.subplots(figsize=(8, 4.2))
q = cont[cont["parameter_code"] == "00060"].sort_values("time")
colors = {"Approved": "#2a78d6", "Provisional": "#eb6834"}
for status, part in q.groupby("approval_status"):
    ax.plot(part["time"], part["value"] / 1000, color=colors[status], linewidth=2, label=f"Continuous discharge ({status})")

in_window = discharge_fm[(discharge_fm["time"] >= START) & (discharge_fm["time"] <= END)]
ax.scatter(in_window["time"], in_window["value"] / 1000, s=60, color="#0b0b0b", zorder=5, label="Field measurement")
crest = q.loc[q["value"].idxmax()]
ax.annotate(f"Crest {crest['value']:,.0f} ft³/s\n{crest['time']:%d %b %H:%M} UTC", (crest["time"], crest["value"] / 1000),
            xytext=(18, -8), textcoords="offset points", fontsize=9)
ax.set_ylabel("Discharge (thousand ft³/s)")
ax.set_ylim(0, 800)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.set_title(f"Ohio River at Louisville, KY ({site}), spring 2025", fontsize=12, loc="left")
ax.legend(frameon=False, fontsize=9, loc="center right", bbox_to_anchor=(1.0, 0.62))
fig.tight_layout()
fig.savefig("wdfn-ohio-louisville-discharge.png", dpi=150)
```

:::{figure} ../images/m03/wdfn-ohio-louisville-discharge.png
:alt: Line chart of discharge at the Ohio River at Louisville from 15 March to 15 May 2025. Flow is around 100,000 to 200,000 cubic feet per second in March, rises steeply in early April to a crest of 719,000 on 9 April, then falls back to about 100,000 by late April. The line is blue (approved) up to the crest and orange (provisional) after it; a black dot marks a field measurement of 738,000 at the crest.
:width: 100%

Continuous discharge at USGS-03294500, Ohio River at Louisville, KY, 15 March to 15 May 2025, colored by approval status, with the crest-day field measurement (plotted at the date; the measurement is rated `Poor`). Data: USGS Water Data APIs via `dataretrieval` (parameter `00060`), accessed 2026-10-08; values after 9 April 2025 17:15 UTC were provisional at access.
:::

(wdfn-legacy)=
**A note on the legacy `nwis` module.** Many older tutorials, including the CUAHSI notebook this lesson draws on, use `dataretrieval.nwis`, which calls the legacy Water Services. For contrast, here is the same daily-mean request the old way:

```python
from dataretrieval import nwis

# legacy Water Services: bare site number, parameter in the column name, approval as a code
legacy, md = nwis.get_dv(sites="03294500", parameterCd="00060", start="2025-04-08", end="2025-04-10")
print(legacy)
```

```text
DeprecationWarning: `nwis.get_dv` is deprecated and will be removed from `dataretrieval` on or after 2027-05-06; use `waterdata.get_daily()` instead.
                           00060_Mean 00060_Mean_cd   site_no
datetime
2025-04-08 00:00:00+00:00      710000             A  03294500
2025-04-09 00:00:00+00:00      712000             P  03294500
2025-04-10 00:00:00+00:00      691000             P  03294500
```

The values are the same, but the shape differs: a bare site number (`03294500` instead of `USGS-03294500`), one column per parameter and statistic (`00060_Mean`), and approval as a one-letter code (`A` approved, `P` provisional) in a `_cd` column. `dataretrieval` warns that `nwis.get_dv` will be removed on or after 2027-05-06. Write new code with `waterdata`, as in this lesson.

:::{admonition} Partner review (USGS): Legacy Water Services retirement
:class: important
Confirm the retirement timeline for the legacy Water Services to cite here.
:::

(wdfn-understanding)=
## Understanding what you downloaded

The continuous values, daily values and field measurements share their core columns. Here is how they map onto the course's shared concepts (see [Meet USGS WDFN](../02-federal-water-data-landscape/03_meet_usgs_wdfn.md)), using what came back for Louisville:

| Shared concept | What it is in your download | Column(s) |
|---|---|---|
| {term}`Location identifier` | `USGS-03294500`: agency prefix plus site number | `monitoring_location_id` |
| {term}`Variable` | discharge (`00060`) and gage height (`00065`) | `parameter_code`, plus `statistic_id` (`00011` continuous, `00003` daily mean) |
| {term}`Variable unit` | `ft^3/s` for discharge, `ft` for gage height | `unit_of_measure` |
| {term}`Time` | continuous: UTC timestamps every 15 minutes; daily: a calendar date; field measurements: a date plus `time_of_day` | `time` |
| {term}`Data quality flag(s)` | {term}`approval status <Approval status>` (`Approved`, or `Provisional` and subject to revision); `qualifier` for special conditions (e.g. `[ESTIMATED]`, `[ICE]`); `measurement_rated` (`Good`, `Fair`, `Poor`) for field measurements | `approval_status`, `qualifier`, `measurement_rated` |
| {term}`Version / provenance` | No version number: the service you called, the request URL and the date you retrieved the data. Values can change until they're approved; `last_modified` says when each was last changed | `md.url`, your retrieval date, `last_modified` |
| {term}`Data unit` | one time series per monitoring location, parameter and statistic | `time_series_id` |

**Provisional data and re-running later.** Because provisional values can change, the same request run next year may return different numbers for April 2025. Record the date you retrieved the data, and save what you downloaded.

**Keep raw and derived data apart.** Save each download unchanged (for example `data/raw/usgs_03294500_continuous_2025-03-15_2025-05-15.csv`), and write anything you compute from it, such as the crest table or a cleaned series, to a separate folder (`data/derived/`). Then you can always trace a number back to the download it came from ([Data Management](../01-data-best-practices/02_data_management.md), Module 1).

**Cite what you used.** USGS water data have a DOI, [https://doi.org/10.5066/F7P55KJN](https://doi.org/10.5066/F7P55KJN) (U.S. Geological Survey, National Water Information System). Cite it with the monitoring location IDs, parameter codes, dates and your access date, and cite `dataretrieval` too: Hodson and Hariharan, [https://doi.org/10.5066/P94I5TX3](https://doi.org/10.5066/P94I5TX3). [Data Publishing](../01-data-best-practices/03_data_publishing.md) in Module 1 covers citing data.

:::{admonition} Partner review (USGS): Data citation
:class: important
Confirm the recommended citation for data retrieved through the Water Data APIs (DOI 10.5066/F7P55KJN, and the preferred wording now that NWISWeb is replaced by WDFN).
:::

## Best practices FAQs

See the sections below for answers and code examples to the following questions.

* What is the recommended way to download data for **one location across the full period of record**?
* What is the recommended way to download data across **all locations for a small time range**?
* If I am working on improving efficiency through **code parallelization**, what should I do vs avoid?

### Temporal scaling

**What is the recommended way to access data for one location but the full period of record?**

Make one request per site and leave out `time`. For daily values, `get_daily` then returns the whole record, and `dataretrieval` handles the paging. The Louisville gage has daily discharge back to 1928:

```python
daily_record, md = waterdata.get_daily(
    monitoring_location_id=site,
    parameter_code="00060",
    statistic_id="00003",
)
print(len(daily_record), daily_record["time"].min(), daily_record["time"].max())
print(daily_record.loc[daily_record["value"].idxmax(), ["time", "value"]])
```

```text
36054 1928-01-01 00:00:00 2026-10-07 00:00:00
time     1937-01-27 00:00:00
value              1110000.0
Name: 3314, dtype: object
```

On 2026-10-08 this one request returned 36,054 rows, one per day from 1 January 1928 to the day before, in about 6 seconds. The largest daily mean in the record is 1,110,000 ft³/s on 27 January 1937. Look at the `qualifier` column on long records: about 1,100 of these days are marked `[ESTIMATED]` (count them with `daily_record["qualifier"].astype(str).str.contains("ESTIMATED").sum()`), some together with `[ICE]` or `[EQUIP]` (equipment problems).

Continuous values are limited to three years per call, so request a long continuous record in three-year windows (the Louisville record starts in 2009, so that's six requests). Approved data rarely change, so save each window to a file and only request new data next time.

### Spatial scaling

**What is the recommended way to download data across all locations but a small time range?**

Leave out `monitoring_location_id` and set a short `time` instead. One request for one day returns that day's value for every site with daily mean discharge. Looping over thousands of site IDs one request at a time would send thousands of requests and quickly use up your rate limit.

```python
one_day, md = waterdata.get_daily(
    parameter_code="00060",
    statistic_id="00003",
    time="2025-04-09",    # one date; also accepts an interval such as "2025-04-01/2025-04-10"
)
print(len(one_day), "rows at", one_day["monitoring_location_id"].nunique(), "locations")
```

```text
9041 rows at 9029 locations
```

On 2026-10-08 this returned 9,041 daily values at 9,029 locations (a few locations have more than one discharge series) in a couple of seconds. To narrow the area, add a `bbox` (west, south, east, north, in decimal degrees) or a list of sites rather than looping:

```python
around_louisville, md = waterdata.get_daily(
    parameter_code="00060",
    statistic_id="00003",
    time="2025-04-09",
    bbox=[-86.5, 37.8, -85.0, 38.8],
)
print(around_louisville.sort_values("value", ascending=False)[["monitoring_location_id", "value", "approval_status"]].head(3))
```

```text
   monitoring_location_id     value approval_status
9           USGS-03294500  712000.0     Provisional
4           USGS-03292494  668000.0     Provisional
34          USGS-03371500   64300.0        Approved
```

That returned 36 locations in the box. The two largest are the Louisville gage and a second Ohio River location in Louisville, at the water tower.

### Parallelization

If I am working on improving efficiency of my code through parallelization, what should I do vs avoid?

- **Do** ask for more in each request before reaching for parallel code. Most `waterdata` functions accept lists (several `monitoring_location_id`s or `parameter_code`s), a `bbox`, or a time interval. One request that returns 10,000 rows is cheaper for you and for USGS than 100 requests that return 100 rows each.
- **Do** use an API key (`API_USGS_PAT`) for any repeated or large workflow, and expect HTTP `429 Too Many Requests` if you go over your hourly limit.
- **Do** let `dataretrieval` handle paging (`limit` sets the page size, `max_rows` caps the total) instead of writing your own loop of requests.
- **Avoid** launching many simultaneous requests from your own threads or processes. Each request spends your rate-limit quota, and a burst of parallel calls is the quickest way to get throttled. Recent versions of `dataretrieval` can split a large pull into chunks and run them concurrently for you. Use that sparingly, and only for pulls you know are large.
- **Avoid** re-downloading the same historical record every time you run your code. Approved data rarely change, so save results to a file and only request what is new (the `last_modified` argument helps).

:::{admonition} Partner review (USGS): Parallelization
:class: important
Confirm these recommendations, especially the guidance on concurrency and on using `last_modified` for incremental updates.
:::

## Now you try it

Repeat the main steps on the course's second river: the **Willamette River at Salem, Oregon**, monitoring location `USGS-14191000`. The Willamette drains the valley between Oregon's Coast Range and Cascades and runs high in winter, when Pacific storms bring heavy rain.

**Your task**

1. Get the daily mean discharge for 1 February to 31 March 2026. Change `site` and the dates (`START`, `END`) in the daily-values example.
2. Find the highest daily mean, and check its approval status.
3. Get the continuous discharge and gage height for the same window and find the crest, as in the continuous-values example.

**What you should see:** 59 daily values, almost all `Provisional`; the highest daily mean is **62,200 ft³/s** on 25 February 2026. The continuous record crests at **64,000 ft³/s** (gage height 16.86 ft) at 23:45 UTC on 25 February. Because these values are provisional, your numbers may differ slightly.

:::{dropdown} Answer
```python
site = "USGS-14191000"                  # Willamette River at Salem, OR
START, END = "2026-02-01", "2026-03-31"

daily_w, md = waterdata.get_daily(monitoring_location_id=site, parameter_code="00060",
                                  statistic_id="00003", time=f"{START}/{END}")
print(len(daily_w), daily_w["approval_status"].value_counts().to_dict())
print(daily_w.loc[daily_w["value"].idxmax(), ["time", "value", "unit_of_measure", "approval_status"]])

cont_w, md = waterdata.get_continuous(monitoring_location_id=site, parameter_code=["00060", "00065"],
                                      time=f"{START}T00:00:00Z/2026-04-01T00:00:00Z")
peaks_w = cont_w.loc[cont_w.groupby("parameter_code")["value"].idxmax()]
print(peaks_w[["parameter_code", "time", "value", "unit_of_measure", "approval_status"]])
```

```text
59 {'Provisional': 58, 'Approved': 1}
time               2026-02-25 00:00:00
value                          62200.0
unit_of_measure                 ft^3/s
approval_status            Provisional
Name: 24, dtype: object
      parameter_code                      time     value unit_of_measure approval_status
14392          00060 2026-02-25 23:45:00+00:00  64000.00          ft^3/s     Provisional
14393          00065 2026-02-25 23:45:00+00:00     16.86              ft     Provisional
```
:::

## Further reading

* [Meet USGS WDFN](../02-federal-water-data-landscape/03_meet_usgs_wdfn.md) (Module 2): what these data are and how they're collected.
* `dataretrieval` (Python) GitHub repo: https://github.com/DOI-USGS/dataretrieval-python
* `dataretrieval` documentation: https://doi-usgs.github.io/dataretrieval-python/
* USGS Water Data APIs documentation: https://api.waterdata.usgs.gov/
* USGS Water Data API keys: https://api.waterdata.usgs.gov/docs/ogcapi/keys/
* USGS Water Data for the Nation: https://waterdata.usgs.gov/
* NWIS Mapper (GUI): https://apps.usgs.gov/nwismapper/
* USGS provisional data statement: https://waterdata.usgs.gov/provisional-data-statement/
* Adapted from [Notebook to Demonstrate Collecting USGS Data](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/USGS%20-%20Plotting%20Streamflow%20using%20NWIS%20DataRetrieval) by CUAHSI, CUAHSI notebooks (GPL-3.0). Its legacy `nwis` calls are ported to `waterdata` here.

  :::{admonition} TODO (dev team): confirm this link
  :class: attention
  This links to the CUAHSI/notebooks `develop` branch. Confirm the link (and whether it should point to `main`) before release.
  :::

  :::{admonition} TODO (dev team): Notebook authors
  :class: attention
  Verify notebook author(s) for credit.
  :::
