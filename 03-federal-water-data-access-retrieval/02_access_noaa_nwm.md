# Retrieve NOAA NWM data

The NOAA National Water Model (NWM) simulates and forecasts {term}`streamflow <Streamflow>` for about 2.8 million river {term}`reaches <Reach>` across the United States. This lesson shows you how to find the reach you care about and retrieve its forecasts in Python. If you haven't met the NWM yet, start with [Meet NOAA NWM](../02-federal-water-data-landscape/02_meet_noaa_nwm.md), which covers how the model works, its {term}`configurations <Configuration>` and its known limitations.

**Main example: the Ohio River at Louisville, Kentucky.** The Ohio is one of the largest rivers in the country, and at Louisville it carries the drainage of much of the Ohio Valley. In early April 2025, days of heavy rain sent it into a large spring flood. You will retrieve NWM forecasts for the reach of the Ohio at Louisville, both today's forecast and archived forecasts issued during the April 2025 flood. At the end, you will repeat the steps on a second river, the Willamette at Salem, Oregon.

NWM output is stored as NetCDF files, one per forecast hour, each covering every reach in the model. The full model output has no general-purpose query service in front of it: you read the files from NOAA's archive, mirrored on Google Cloud and AWS. Two NOAA services serve slices of it:

* NOAA's experimental [NWM API](https://api.water.noaa.gov/nwm/v1/docs) serves individual reaches, but only the most recent few days of forecasts.
* The [National Water Prediction Service (NWPS) API](https://api.water.noaa.gov/nwps/v1/docs/) serves NWM output only at NWPS's established forecast locations, not the full domain, so this lesson doesn't use it.

The steps are:

1. **Programmatic data discovery.** The NWM identifies reaches by {term}`COMID`, a number from the {term}`NHDPlus` stream network. Before you can download a forecast, you find the COMID for your location. You do this with the {term}`NLDI` (Network Linked Data Index), a separate web service from wherever the NWM files live.
1. **Programmatic data downloads.** With COMIDs in hand, you retrieve forecast values. There are several routes, and the best one depends on how much data you need (see the table below).

This lesson focuses on NWM **forecasts** (short, medium and long range), because forecasting is what sets the NWM apart: it predicts what rivers will do, everywhere, rather than recording what they did at a few places. If you already know your COMID(s), you can skip discovery.

(nwm-access-routes)=
## Choosing an access route

NWM output is big: every forecast hour is a file covering all ~2.8 million reaches. How you should access it depends mostly on **how many forecast runs (issue times) you need**, and much less on how many reaches. None of these routes needs an {term}`API key`.

| Use case | Recommended route | Key needed? | Scaling limits |
|---|---|---|---|
| Today's or the last few days' forecasts for a few reaches | [NOAA NWM API](#nwm-api) | No | Keeps only ~3–5 days of runs; labelled experimental; built for a few reaches per request |
| Past forecasts, a few reaches, a few issue times | [`hydrotools`](#nwm-hydrotools) (Google Cloud archive) | No | Downloads whole {term}`CONUS` (contiguous U.S.) files (~250–280 MB per short-range run); cost grows with the number of runs, not reaches |
| Past forecasts for many reaches or a region, or many issue times | [Kerchunk references](#nwm-kerchunk) + `xarray`/`dask`, ideally run in the cloud | No | Reads only the `streamflow` chunk (~7× fewer bytes than whole files) with less memory, but each read is still a CONUS-wide chunk; building references is a one-time step per run |
| Long historical record (simulation, not forecasts) | NWM {term}`retrospective simulation <Retrospective simulation>` (cloud Zarr) | No | A different product (see [Temporal scaling](#nwm-temporal-scaling)) |

The numbers behind these recommendations are in [Why NWM downloads cost what they cost](#nwm-cost).

## Tools and environment setup

This lesson has its own {term}`conda environment <Conda environment>`, so its packages don't collide with other lessons' packages and so the code runs with known versions.

:::{admonition} TODO (dev team): One environment per lesson?
:class: attention
For consideration: should we use environments to avoid dependency collisions? Or try to actually address any dependency collisions? We ultimately want people to be able to use all three datasets on their computers, and give them the knowledge and tools to do so.
:::

The environment file [`environments/m03-nwm.yml`](../environments/m03-nwm.yml) lists everything this page uses. From the root of the course repository:

```bash
conda env create -f environments/m03-nwm.yml
conda activate m03-nwm

# Optional: register this environment as a Jupyter kernel, then pick "Python (m03-nwm)" in Jupyter
python -m ipykernel install --user --name m03-nwm --display-name "Python (m03-nwm)"
```

This installs everything for discovery (`pynhd`) and for all three download routes (`requests` for the NWM API, `hydrotools.nwm_client`, and `kerchunk` + `xarray` + `fsspec`), plus `matplotlib` for the figures and `ipykernel` for Jupyter. If you work in Jupyter, choose the `Python (m03-nwm)` kernel; otherwise your notebook runs in a different environment and imports such as `pynhd` fail. None of the routes on this page needs an API key or account.

The environment file pins the Python version but lets most packages float to their latest release, so a year from now `conda env create` may give you newer versions than the ones we tested. When you finish an analysis, record exactly what you ran with `conda env export > environment-lock.yml` and keep that file with your results. [Data Management](../01-data-best-practices/02_data_management.md) (Module 1) explains why this matters for reproducibility. The examples on this page were tested with Python 3.14, `pynhd` 0.20.0, `hydrotools.nwm_client` 9.2.1, `kerchunk` 0.2.10, `xarray` 2026.9.0, `zarr` 3.4.0 and `fsspec` 2026.9.0.

## Programmatic data discovery

Before you download anything, *discover* the reach (or reaches) you need. You don't want to page through the whole NWM domain to learn which COMID matches your location. Doing discovery first also lets you build a COMID list once and reuse it, which matters once you scale up to many reaches (see [Spatial scaling](#nwm-spatial-scaling)).

**The point-and-click way.** NOAA's [National Water Prediction Service map](https://water.noaa.gov/map) lets you click a river and read off its reach ID, which is the same number as the COMID. That's a fine way to explore or spot-check. Capture the lookup in code as well, even if you first found the reach by clicking around, so that you (or a reader of your paper) can repeat it.

:::{admonition} Partner review (NOAA): Programmatic data discovery
:class: important
Confirm the map's reach ID is the NWM `feature_id`.
:::

### Finding COMIDs with the NLDI

The NWM's *{term}`Location identifier`* is the **COMID** of a reach (also called `feature_id`, `nwm_feature_id` or ComID; see the shared concepts in [Meet NOAA NWM](../02-federal-water-data-landscape/02_meet_noaa_nwm.md)). The NLDI can:

* find the COMID for a point on the map (a lookup against NHDPlus catchments),
* find the COMID that a known monitoring site sits on, and
* navigate the river network upstream or downstream from a COMID (upstream mainstem, upstream with tributaries, downstream mainstem, downstream with diversions), which is useful for "every reach in this watershed" questions.

We call the NLDI from Python with the [`pynhd`](https://docs.hyriver.io/readme/pynhd.html) package (part of HyRiver).

**Example: what's the COMID of the Ohio River at Louisville?**

Keep the place you are asking about in a variable at the top of your script, rather than typing coordinates into the middle of a call. That way your query is recorded in one spot and is easy to change. `feature_byloc` takes a `(longitude, latitude)` pair in EPSG:4326 (ordinary longitude and latitude) and finds the NHDPlus reach whose catchment contains it, using the NLDI `position` endpoint.

```python
from pynhd import NLDI

# the place we're asking about: the Ohio River at Louisville, KY (longitude, latitude; EPSG:4326)
POINT = (-85.7991, 38.2803)

nldi = NLDI()
comid_gdf = nldi.feature_byloc(POINT)   # snap the point to an NHDPlus reach
comid = int(comid_gdf["comid"].iloc[0])

print(comid_gdf.drop(columns="geometry"))
print(f"COMID: {comid}")
```

```text
  identifier                                                             navigation source     sourceName     comid
0   10164004  https://api.water.usgs.gov/nldi/linked-data/comid/10164004/navigation  comid  NHDPlus comid  10164004
COMID: 10164004
```

It returns a one-row `GeoDataFrame` with the matching `comid` and the reach's geometry (dropped from the printout). The Ohio at Louisville is COMID **10164004**.

The same lookup with the raw NLDI web address, which you can paste into a browser:

```text
https://api.water.usgs.gov/nldi/linked-data/comid/position?coords=POINT(-85.7991 38.2803)
```

**Example: the COMID of a reach with a monitoring site on it**

If a river has a stream gage, you can also ask the NLDI for the reach the gage sits on. Here we use the ID of the gage at Louisville, `USGS-03294500`, *only as a way to name the location*: this lesson doesn't use the gage's measurements. NLDI lists stream gages as the `nwissite` source.

```python
# look up the reach by the ID of the monitoring site on it (used here only to locate the reach)
site = nldi.getfeature_byid("nwissite", "USGS-03294500")
print(site[["identifier", "name", "comid"]])
```

```text
      identifier                          name     comid
0  USGS-03294500  OHIO RIVER AT LOUISVILLE, KY  10164004
```

Both routes give the same COMID, which is a useful check that you found the right reach.

**Example: every reach upstream of Louisville, up to 100 km**

For regional questions you want a *list* of COMIDs. `navigate_byid` walks the network from a starting COMID. `upstreamTributaries` follows every tributary, and `distance` (in km) caps how far to go.

```python
# every NHDPlus reach upstream of the Louisville reach, tributaries included, up to 100 km away
upstream = nldi.navigate_byid(fsource="comid", fid=str(comid),
                              navigation="upstreamTributaries", source="flowlines", distance=100)
upstream_comids = upstream["nhdplus_comid"].astype(int).tolist()
print(f"{len(upstream_comids)} reaches upstream of (and including) the Louisville reach")
```

```text
498 reaches upstream of (and including) the Louisville reach
```

This returns a `GeoDataFrame` of reach lines with an `nhdplus_comid` column and a `geometry` column: **498 reaches** within 100 km upstream, including the Louisville reach itself. We reuse `upstream_comids` in [Spatial scaling](#nwm-spatial-scaling). On the Ohio, going farther upstream adds reaches quickly (the whole basin has tens of thousands), so set `distance` to what your question needs.

**Map: where these reaches are**

Plotting what discovery returned is a quick check that you have the right river. The geometries come back with the reaches, so the map needs no other data:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 6))
upstream.plot(ax=ax, color="#9fb7d9", linewidth=0.8)                   # all 498 upstream reaches
comid_gdf.plot(ax=ax, color="#eb6834", linewidth=4)                    # the Louisville reach
ax.plot(*POINT, marker="*", color="#eb6834", markersize=16, markeredgecolor="white")
ax.annotate(f"COMID {comid}\nOhio River at Louisville, KY", POINT, xytext=(15, -45),
            textcoords="offset points", fontsize=10)
ax.set_aspect(1 / 0.786)                                               # roughly equal km in x and y at 38° N
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("NHDPlus reaches up to 100 km upstream of Louisville", loc="left", fontsize=12)
fig.tight_layout()
fig.savefig("nwm-ohio-louisville-map.png", dpi=150)
```

:::{figure} ../images/m03/nwm-ohio-louisville-map.png
:alt: Map of thin blue river lines branching to the northeast and east of Louisville, Kentucky, with the main stem of the Ohio River running from the upper right to a highlighted orange reach and star at Louisville in the lower left.
:width: 90%

The 498 NHDPlus reaches up to 100 km upstream of the Ohio River reach at Louisville (COMID 10164004, orange), from the NLDI `upstreamTributaries` navigation. The long line is the Ohio's main stem; the branches are tributaries. Data: USGS NLDI via `pynhd`, accessed 2026-10-09.
:::

Once you have your COMID(s), move on to downloads.

## Programmatic data downloads

This section covers three routes, in order of how much data they're built for: the NOAA NWM API, `hydrotools`, and kerchunk references read with `xarray`. All three return the NWM's *{term}`Variable`* `streamflow`, in m³/s (the API labels it `CMS`), for each COMID. The NWM has no per-value *{term}`Data quality flag(s)`*, so you record the configuration, reference time and model version with your data instead (see [Understanding what you downloaded](#nwm-understanding)).

:::{admonition} Partner review (NOAA): Programmatic data downloads
:class: important
Confirm: “All three return NWM's *Variable* `streamflow` in m³/s (the API labels it `CMS`) for each COMID; NWM has no per-value *Data Quality Flag*”.
:::

Two terms you'll see in every route:

* **{term}`Configuration`**: which forecast product, e.g. `short_range` (hourly out to 18 hours, issued every hour), `medium_range` (out to 10 days, issued every 6 hours, with several *ensemble members*: parallel runs from slightly different inputs, numbered by `member_id`, that show the spread of possible outcomes), `long_range`, or `analysis_assim` (the model's best estimate of current conditions).

  :::{admonition} Partner review (NOAA): Programmatic data downloads
  :class: important
  Confirm cadences, horizons and ensemble sizes for NWM v3.0.
  :::

* **{term}`Reference time <Forecast reference time>`**: when a forecast was issued, in UTC (Coordinated Universal Time). NWM shorthand writes the issue hour with a Z for UTC: `00Z` is 00:00 UTC, and file names write it as `t00z`. The time each forecast value applies to is its **{term}`valid time <Valid time>`** (`valid_datetime` in the API, `value_time` in `hydrotools`, `time` in the files).

(nwm-api)=
### NOAA NWM API: today's forecasts for a few reaches

NOAA's [NWM API](https://api.water.noaa.gov/nwm/v1/docs) returns forecasts for one or more reaches as JSON (a text format that Python reads as lists and dictionaries), with no key and no files to manage. It is labelled **experimental**, and it keeps only roughly the **last 3–5 days** of forecasts (on 2026-10-09 the oldest short-range run it held was from 2026-10-05 00Z). Use it for "what is the model predicting now?", not for past events.

:::{admonition} Partner review (NOAA): NOAA NWM API: today's forecasts for a few reaches
:class: important
Confirm the API's retention window and whether it is intended for research use.
:::

**Example: the latest short-range forecast for the Ohio at Louisville**

```python
import requests
import pandas as pd

comid = 10164004  # from the discovery step
url = f"https://api.water.noaa.gov/nwm/v1/streamflow/forecast/nwm_feature_id/{comid}/"

# ask for the most recent short-range forecast for this reach
resp = requests.get(url, params={"configuration": "short_range", "latest": "true"}, timeout=60)
resp.raise_for_status()                 # stop with an error if the request failed
run = resp.json()[0]                    # one entry per configuration + reference time

forecast = pd.DataFrame(run["forecast"][0]["timeseries"])
forecast["valid_datetime"] = pd.to_datetime(forecast["valid_datetime"])
print(run["configuration"], run["reference_datetime"], run["units"])
print(forecast.head())
```

```text
short_range 2026-10-09T02:00:00Z CMS
             valid_datetime    value
0 2026-10-09 03:00:00+00:00   948.47
1 2026-10-09 04:00:00+00:00   961.04
2 2026-10-09 05:00:00+00:00  1000.92
3 2026-10-09 06:00:00+00:00  1044.88
4 2026-10-09 07:00:00+00:00  1084.42
```

Your numbers will differ: this is whatever run is newest when you ask. The response is a list with one entry per forecast run. Each entry has `nwm_feature_id` (the COMID), `configuration`, `reference_datetime`, `data_type`, `units` and a `forecast` list with one item per ensemble member (`member_id`). Each member holds a `timeseries` of `valid_datetime`/`value` pairs: 18 hourly values for a short-range run. To ask about several reaches at once, separate the COMIDs with commas in the URL.

**Example: every recent medium-range run, all ensemble members**

Leave out `latest` and use `min_reference_datetime` (and `max_reference_datetime`) to get several runs in one request:

```python
# every medium-range run issued in the last 2 days (the API only keeps the last few days)
since = (pd.Timestamp.now(tz="UTC") - pd.Timedelta("2D")).strftime("%Y-%m-%dT%H:00:00Z")
resp = requests.get(url, params={"configuration": "medium_range", "min_reference_datetime": since}, timeout=120)
resp.raise_for_status()

# flatten the nested JSON into one row per run, member and valid time
rows = []
for run in resp.json():
    for member in run["forecast"]:
        for step in member["timeseries"]:
            rows.append({"reference_time": run["reference_datetime"], "member": member["member_id"],
                         "valid_time": step["valid_datetime"], "streamflow_cms": step["value"]})

runs = pd.DataFrame(rows)
print(runs.groupby("reference_time")["member"].nunique())
```

```text
reference_time
2026-10-07T06:00:00Z    6
2026-10-07T12:00:00Z    6
2026-10-07T18:00:00Z    6
2026-10-08T00:00:00Z    6
2026-10-08T06:00:00Z    6
2026-10-08T12:00:00Z    6
2026-10-08T18:00:00Z    6
Name: member, dtype: int64
```

`runs` is a long-format table (one row per value) with columns `reference_time`, `member`, `valid_time` and `streamflow_cms`. Each medium-range run had 6 ensemble members in the API response: member 1 runs out to 240 hours, the others to 204 hours. The whole response for seven runs was about 0.6 MB, and every short-range run the API held for this reach (99 runs) came back in one 0.13 MB response in under a second.

(nwm-hydrotools)=
### `hydrotools`: past forecasts from the cloud archive

For anything older than a few days, such as the April 2025 flood, you need NOAA's archive of the raw NWM output files. The operational archive is mirrored, with no key or account needed, on [Google Cloud](https://console.cloud.google.com/marketplace/product/noaa-public/national-water-model) (`gs://national-water-model`) and on [AWS](https://registry.opendata.aws/noaa-nwm-pds/) (`s3://noaa-nwm-pds`). Each forecast hour is a separate NetCDF file covering all ~2.8 million reaches (about 13–16 MB for a short-range {term}`channel_rt` file (the channel-routing output, which holds `streamflow`)).

`hydrotools` (OWPHydroTools, from NOAA's Office of Water Prediction) finds those files, downloads them, and hands you a `pandas.DataFrame` for just the COMIDs you asked for. You never open a NetCDF file yourself.

**Key pieces**

* `hydrotools.nwm_client`: retrieves NWM streamflow forecasts. Older tutorials use `hydrotools.nwm_client_new`; its last release was 8.0.0 in December 2024, and development continues as [`hydrotools.nwm_client`](https://pypi.org/project/hydrotools.nwm-client/) (currently 9.x), with the same `NWMFileClient` interface.
* Canonical column names shared across the `hydrotools` subpackages: `value`, `value_time`, `variable_name`, `nwm_feature_id` (the COMID) and so on. Because every `hydrotools` table uses the same names, tables from different sources join easily.

**Example: the short-range forecast issued at 00Z on 6 April 2025**

Before you run this: `.get()` downloads all 18 files of the run (about 270 MB) and needs about 1.7 GB of memory, and took about 2–3 minutes on our home connection. Let it finish; interrupting it can leave a broken file behind (see "If `.get()` fails" below). **In Jupyter**, run `import nest_asyncio; nest_asyncio.apply()` once first (the first line of the block, commented out); plain Python scripts don't need it.

```python
# import nest_asyncio; nest_asyncio.apply()   # uncomment in Jupyter only
from hydrotools.nwm_client.NWMFileClient import NWMFileClient

comid = 10164004  # from the discovery step

# downloads go to ./hydrotools_data/NWMFileClient_NetCDF_files; results are cached in ./hydrotools_data/nwm_store.parquet
client = NWMFileClient()   # default catalog: Google Cloud

forecast_data = client.get(
    configurations=["short_range"],
    reference_times=["2025-04-06T00:00"],   # forecast issue time (UTC)
    nwm_feature_ids=[comid],
)
print(forecast_data[["reference_time", "nwm_feature_id", "value_time", "value", "measurement_unit"]].head().to_string())
```

```text
  reference_time nwm_feature_id          value_time         value measurement_unit
0     2025-04-06       10164004 2025-04-06 01:00:00  15580.569336           m3 s-1
1     2025-04-06       10164004 2025-04-06 02:00:00  15429.159180           m3 s-1
2     2025-04-06       10164004 2025-04-06 03:00:00  15097.709961           m3 s-1
3     2025-04-06       10164004 2025-04-06 04:00:00  14626.569336           m3 s-1
4     2025-04-06       10164004 2025-04-06 05:00:00  14026.239258           m3 s-1
```

The result is a long-format `pandas.DataFrame`, one row per COMID and valid time (18 rows here), with columns `reference_time`, `nwm_feature_id`, `value_time`, `value`, `measurement_unit`, `variable_name`, `configuration` and `usgs_site_code` (a gage code that `hydrotools` fills in for reaches it maps to a stream gage; it is empty, `<NA>`, for this reach). Times are in UTC. Values are in SI units (`m3 s-1`); pass `unit_system=MeasurementUnitSystem.US` (from `hydrotools.nwm_client.NWMClientDefaults`) to `NWMFileClient` for cubic feet per second.

**If `.get()` fails:**

* **In Jupyter or another notebook**, `hydrotools` raises `RuntimeError: asyncio.run() cannot be called from a running event loop`, because its downloader starts its own event loop and the notebook already runs one. Run `import nest_asyncio; nest_asyncio.apply()` once before calling `.get()` (`nest-asyncio` is in the course environment). Plain Python scripts don't need it.
* **With errors about reading a NetCDF/HDF file**, an earlier run was probably interrupted (a timeout, a lost connection or a stopped cell), leaving a half-downloaded file in `hydrotools_data/`. `hydrotools` treats files already in that folder as downloaded, so it tries to open the broken one instead of fetching it again. Delete the `hydrotools_data/` folder in your working directory and run the call again.
* The `FutureWarning` and `UserWarning` messages printed during `.get()` (from `xarray`, `dask` and Google's libraries) are harmless: if the table prints, it worked.

What happens behind `.get()` matters for cost: `hydrotools` downloads **every file of every forecast run you ask for, in full**, then extracts your COMIDs. One short-range run is 18 files (~250–280 MB); one medium-range member is 240 files (~3 GB or more). Results are cached in `hydrotools_data/nwm_store.parquet`, so asking for the same run again is fast. Just importing `NWMFileClient` creates the `hydrotools_data/` folder in the current directory, so keep it out of version control (add it to `.gitignore`) and delete it when you're done. You can pass `file_directory=` to choose where files go, or `cleanup_files=True` to delete the downloaded NetCDF files after each `get()`.

**On a slow connection, large requests can time out.** `hydrotools` queues every file of a run at once and gives each download 900 seconds, including time spent waiting in the queue. In an earlier test of a medium-range member (~3 GB) on a shared home connection, the download timed out after ~15 minutes in both clean attempts. Rerunning the same call did *not* recover cleanly: the half-written file was skipped as "already downloaded" and then failed to open (see "If `.get()` fails" above). Retry on a faster connection, or use kerchunk references (below), which fetch about 7× less.

(nwm-kerchunk)=
### Kerchunk references: lazy, cloud-native reads with `xarray`

First, two terms. Inside a NetCDF file, each variable is stored in compressed blocks called *chunks*; a reader has to fetch and decompress a whole chunk to get any value in it, like having to take a whole box off the shelf to get one book. *Zarr* is a storage format that keeps each chunk as a separate object, so cloud tools can fetch exactly the chunks they need. NetCDF files aren't designed to be read piece by piece over the internet. {term}`Kerchunk <kerchunk>` fixes that without copying the data: it scans each file once and writes a small JSON "reference" file that records *where inside the original file* each chunk of each variable lives (byte offset and length). `xarray` can then open the references as if they were one Zarr dataset and fetch **only the chunks you touch**, straight from the cloud bucket. See the [kerchunk documentation](https://fsspec.github.io/kerchunk/) and Element 84's write-up, [Using Kerchunk to make NOAA's National Water Model dataset more accessible](https://element84.com/software-engineering/using-kerchunk-to-make-noaas-national-water-model-dataset-more-accessible/) (2023).

Two kinds of reference are available:

1. **NOAA-published references.** NOAA's Open Data Dissemination program publishes ready-made references in `s3://noaa-nodd-kerchunk-pds` ([registry entry](https://registry.opendata.aws/noaa-nodd-kerchunk/)) for NWM `short_range` and `medium_range_mem1` (plus the Alaska, Hawaii and Puerto Rico short range), built automatically as new files arrive. On 2026-10-07 they started at **2026-01-01**, so they don't cover the April 2025 flood.

   :::{admonition} Partner review (NOAA): Kerchunk references: lazy, cloud-native reads with xarray
   :class: important
   Confirm how far back these references are kept.
   :::

2. **References you build yourself** for any files in the archive. This is a one-time step per forecast run, and the result is small (about 20 KB of JSON for an 18-file short-range run).

**Example: build references for the 6 April 2025 00Z short-range run**

The first step is a list of the run's files. CIROH's [`nwmurl`](https://hub.ciroh.org/docs/products/data-management/dataaccess/NWMURL%20Library) library builds NWM file URLs from a date, issue time, forecast hours, configuration and archive, so you don't have to know the archive's folder and file-naming scheme. It only builds URLs; it doesn't download anything. Its arguments are numeric codes, listed on that page (and in the comments below).

The code defines two small functions, `index_one` (scan one file) and `build_refs` (scan every file of one run and stitch the results together), so you can reuse them for other runs.

```python
import fsspec
import nwmurl
from concurrent.futures import ThreadPoolExecutor
from kerchunk.hdf import SingleHdf5ToZarr
from kerchunk.combine import MultiZarrToZarr

def index_one(url):
    """Scan one NetCDF file's internal layout and return its byte-range references."""
    with fsspec.open(url, "rb", block_size=2**20) as f:   # read in 1 MB blocks (see below)
        return SingleHdf5ToZarr(f, url, inline_threshold=500).translate()

def build_refs(day, cycle, runinput=1, meminput=None, hours=18):
    """References for one forecast run: day "YYYYMMDD", cycle = issue hour (UTC)."""
    urls = nwmurl.generate_urls_operational(
        start_date=f"{day}0000", end_date=f"{day}0000",  # YYYYMMDDHHMM; one day
        fcst_cycle=[cycle],                 # issue time (UTC hour)
        lead_time=list(range(1, hours + 1)),  # forecast hours 1..hours
        varinput=1,                         # 1 = channel_rt (streamflow)
        geoinput=1,                         # 1 = CONUS
        runinput=runinput,                  # 1 = short_range, 2 = medium_range
        urlbaseinput=3,                     # 3 = https://storage.googleapis.com/national-water-model/
        meminput=meminput,                  # ensemble member (None for short_range)
    )
    with ThreadPoolExecutor(8) as pool:     # one request per file: run them in parallel
        singles = list(pool.map(index_one, urls))
    # stitch the per-file references into one dataset along the time dimension
    return MultiZarrToZarr(singles, remote_protocol="https", concat_dims=["time"],
                           identical_dims=["feature_id", "reference_time", "crs"]).translate()

refs = build_refs("20250406", 0)
print(len(refs["refs"]), "reference entries")
```

```text
134 reference entries
```

`refs` is a Python dictionary: a map from each chunk of each variable to a URL, byte offset and length. A few choices in this code are deliberate:

* `urlbaseinput=3` asks `nwmurl` for the public HTTPS address of each file in the Google Cloud archive, so both scanning and later reads use plain HTTPS with no cloud account. In our tests, reading through `gcsfs` with the current `zarr`/`kerchunk` versions stalled, while HTTPS worked. `nwmurl` can also point at the AWS copy (`urlbaseinput=7`) or other configurations (e.g. `runinput=2` and `meminput=1` for medium-range member 1, as in the figure below).

  :::{admonition} TODO (dev team): gcsfs stall on Windows
  :class: attention
  Verify whether the gcsfs stall is Windows-only.
  :::

* `inline_threshold=500` stores tiny variables (like the single `time` value in each file) directly in the JSON, so the combine step doesn't need to download anything.
* `block_size=2**20` makes each file's scan one 1 MB request, which covers the file's metadata. fsspec's default 5 MB block read about 5× more data for no benefit, and smaller blocks took many more requests and were slower. In our test, building references for three runs took 16 s and 57 MB.
* Save `refs` to a JSON file (`json.dump(refs, open("refs_20250406_00z.json", "w"))`) and reuse it, rather than rebuilding.

Check that `nwmurl` gave you files that exist: a URL for a run that isn't in the archive fails when `index_one` opens it. `generate_urls_operational(..., enforce_valid_outputs=1)` checks each URL first and drops missing ones.

**Example: read the Louisville reach from the references**

```python
import xarray as xr

def open_refs(refs):
    """Open kerchunk references lazily: nothing is downloaded until values are needed."""
    return xr.open_dataset("reference://", engine="zarr", chunks={}, consolidated=False, zarr_format=2,
                           storage_options={"fo": refs, "remote_protocol": "https",
                                            "remote_options": {"asynchronous": True}})

ds = open_refs(refs)
print(ds)
print(ds.attrs["NWM_version_number"], ds.attrs["model_configuration"])

# pull one reach: reads 1 chunk per forecast hour (~2 MB each), not the whole files
q = ds["streamflow"].sel(feature_id=comid).load()
print(q.to_series().head())
```

```text
<xarray.Dataset> Size: 2GB
Dimensions:         (time: 18, feature_id: 2776734, reference_time: 1)
Coordinates:
  * time            (time) datetime64[ns] 144B 2025-04-06T01:00:00 ... 2025-0...
  * feature_id      (feature_id) int64 22MB 101 179 ... 1180001803 1180001804
  * reference_time  (reference_time) datetime64[ns] 8B 2025-04-06
Data variables:
    streamflow      (time, feature_id) float64 400MB dask.array<chunksize=(1, 2776734), meta=np.ndarray>
    ...
Attributes: (12/19)
    TITLE:                      OUTPUT FROM NWM v3.0
    ...
v3.0 short_range
time
2025-04-06 01:00:00    15580.569652
2025-04-06 02:00:00    15429.159655
2025-04-06 03:00:00    15097.709663
2025-04-06 04:00:00    14626.569673
2025-04-06 05:00:00    14026.239686
Name: streamflow, dtype: float64
```

`ds` is an `xarray.Dataset` with dimensions `time` (the 18 forecast hours, i.e. valid times) and `feature_id` (2,776,734 reaches), and variables `streamflow` (m³/s), `velocity`, `nudge` and a few runoff terms. Its attributes (`ds.attrs`) record the model version (`v3.0`) and configuration. The "2GB" size is what the full dataset *would* be in memory; nothing is downloaded until `.load()`. Note `chunksize=(1, 2776734)`: one chunk per hour holding every reach. The values match `hydrotools` to within rounding (the two tools store the numbers at slightly different precision).

**Example: use NOAA's published references for a recent run**

For runs since January 2026 you can skip the build step. NOAA's references are one JSON file per forecast hour and point at the AWS copy of the files (`s3://noaa-nwm-pds`). This example combines them the same way and reads them over HTTPS. It uses `open_refs` from the previous example, so run that block first (you don't need to build any references yourself).

```python
import json
import fsspec
import pandas as pd
from kerchunk.combine import MultiZarrToZarr

comid = 10164004                                # Ohio River at Louisville

s3 = fsspec.filesystem("s3", anon=True)        # public bucket: no AWS account needed

# NOAA publishes one reference file per forecast hour; pick yesterday's 12Z short-range run
day = (pd.Timestamp.now(tz="UTC") - pd.Timedelta("1D")).strftime("%Y%m%d")
paths = sorted(s3.glob(f"noaa-nodd-kerchunk-pds/nwm/short_range/"
                       f"nwm.short_range.channel_rt.conus.{day}.t12z.f*.nc.zarr"))

def load_ref(path):
    """Read one NOAA reference file and point it at the same NWM files over HTTPS."""
    text = json.dumps(json.loads(s3.cat(path)))
    return json.loads(text.replace("s3://noaa-nwm-pds/", "https://noaa-nwm-pds.s3.amazonaws.com/"))

recent = MultiZarrToZarr([load_ref(p) for p in paths], remote_protocol="https", concat_dims=["time"],
                         identical_dims=["feature_id", "reference_time", "crs"]).translate()
ds_recent = open_refs(recent)
print(len(paths), "reference files;", dict(ds_recent.sizes))
print(ds_recent["streamflow"].sel(feature_id=comid).load().to_series().head(3))
```

```text
18 reference files; {'time': 18, 'feature_id': 2776734, 'reference_time': 1}
time
2026-10-08 13:00:00    996.369978
2026-10-08 14:00:00    984.489978
2026-10-08 15:00:00    956.629979
Name: streamflow, dtype: float64
```

(nwm-understanding)=
## Understanding what you downloaded

Whichever route you used, you now have NWM streamflow forecasts for one reach. Here is what each part means, using the shared concepts from [Meet NOAA NWM](../02-federal-water-data-landscape/02_meet_noaa_nwm.md):

| Shared concept | What it is in your download | Where to find it |
|---|---|---|
| {term}`Location identifier` | COMID / `feature_id` `10164004` (the NHDPlus reach of the Ohio at Louisville) | `nwm_feature_id` (API, `hydrotools`), `feature_id` (files) |
| {term}`Variable` | `streamflow`: modeled discharge through the reach | variable name in each route |
| {term}`Variable unit` | m³/s | `units` = `CMS` (API), `measurement_unit` = `m3 s-1` (`hydrotools`), `ds["streamflow"].attrs["units"]` (files) |
| {term}`Time` | reference time (when the forecast was issued) and valid time (when each value applies), both UTC | `reference_datetime`/`valid_datetime` (API), `reference_time`/`value_time` (`hydrotools`), `reference_time`/`time` (files) |
| {term}`Data quality flag(s)` | None. The NWM is a model, so there is no per-value flag. Judge forecasts by lead time (valid time minus reference time) and by comparing runs | – |
| {term}`Version / provenance` | NWM v3.0, configuration `short_range` (or `medium_range` member 1), from the Google Cloud or AWS archive | `ds.attrs["NWM_version_number"]`, `ds.attrs["model_configuration"]`; the API's `configuration` field |
| {term}`Data unit` | One NetCDF file per forecast hour, covering every reach; a short-range run is 18 files, a medium-range member 240 | file names in the archive (e.g. `nwm.t00z.short_range.channel_rt.f001.conus.nc`) |

**What the forecasts look like.** Each forecast run is a separate guess about the future, so a useful picture plots several runs together. The code below builds references for two more short-range runs and for medium-range member 1 issued on 3 April 2025 (240 files, about a minute to build), then plots them. It reuses `build_refs`, `open_refs` and `comid` from above.

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import StrMethodFormatter

# three short-range runs (18 h each) and one medium-range run (member 1, 240 h)
short_runs = {"2025-04-06 00Z": refs, "2025-04-06 12Z": build_refs("20250406", 12),
              "2025-04-07 00Z": build_refs("20250407", 0)}
medium = build_refs("20250403", 0, runinput=2, meminput=1, hours=240)

fig, ax = plt.subplots(figsize=(8, 4.2))
q_med = open_refs(medium)["streamflow"].sel(feature_id=comid).load().to_series()
ax.plot(q_med.index, q_med.values, color="#52514e", linewidth=2, label="Medium range, issued 2025-04-03 00Z (member 1)")
for (label, r), color in zip(short_runs.items(), ["#2a78d6", "#eb6834", "#1baf7a"]):
    q_short = open_refs(r)["streamflow"].sel(feature_id=comid).load().to_series()
    ax.plot(q_short.index, q_short.values, color=color, linewidth=2, label=f"Short range, issued {label}")

ax.set_ylabel("Streamflow (m³/s)")
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.set_xlabel("Valid time, 2025 (UTC)")
ax.set_title(f"NWM v3.0 forecasts, Ohio River at Louisville (COMID {comid})", loc="left", fontsize=12)
ax.legend(frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig("nwm-ohio-louisville-forecasts.png", dpi=150)
```

:::{figure} ../images/m03/nwm-ohio-louisville-forecasts.png
:alt: Line chart of NWM streamflow forecasts for the Ohio River at Louisville, 3 to 13 April 2025. A gray medium-range line issued on 3 April rises from about 3,000 to a peak near 13,900 cubic meters per second on 8 April, then eases to about 10,000. Three short colored lines, the short-range runs issued on 6 and 7 April, each start between 15,000 and 18,000; the two from 6 April fall to about 8,000 to 9,000 within 18 hours, and the one from 7 April falls to about 13,000 and turns back up.
:width: 100%

NWM v3.0 streamflow forecasts for the Ohio River reach at Louisville (COMID 10164004): the medium-range forecast (member 1) issued 3 April 2025 00Z, and three short-range forecasts issued 6 April 00Z, 6 April 12Z and 7 April 00Z. Each line is a separate forecast run. Here they disagree a lot: every short-range run starts near 15,000–18,000 m³/s and falls quickly (the two 6 April runs by about half within 18 hours, the 7 April run by about a quarter before turning up), while the medium-range run issued three days earlier peaks near 13,900 m³/s on 8 April. Data: NOAA NWM operational archive on Google Cloud, read with kerchunk references, accessed 2026-10-09.
:::

If your plot looks like this, your code is right: these are model forecasts, not measurements, and this is what the archive holds (we've asked NOAA why the short-range runs drop so fast; see the note below). That disagreement is part of what you downloaded: the NWM gives you each run as issued, and different runs and configurations can tell different stories about the same river. Record exactly which runs you used, and look at several before drawing conclusions from one.

:::{admonition} Partner review (NOAA): Short-range forecasts at the Ohio River at Louisville
:class: important
In the April 2025 short-range runs for COMID 10164004, each run starts at 15,000–18,000 m³/s and drops quickly (the 6 April 00Z and 12Z runs by about half within 18 hours, the 7 April 00Z run by about a quarter), while the medium-range run issued 3 April stays lower until 8 April. Is this expected behavior at this reach (for example, from data assimilation in the initial conditions, or the McAlpine Locks and Dam), and how should learners interpret it?
:::

**Keep raw and derived data apart.** The files in the NOAA archive are your raw data, and they stay where they are. What you create, the reference JSON and the table of values you extracted, is derived. Save it in a separate folder (for example `data/derived/`) together with the COMIDs, configuration and reference times you asked for, so anyone can rebuild it from the archive. See [Data Management](../01-data-best-practices/02_data_management.md) in Module 1.

**Cite what you used.** The operational NWM forecasts don't have a DOI. Cite the model and version (NWM v3.0), the configuration and reference times, the archive you read from (with its URL), and the date you accessed it. Old forecasts don't change once issued, but the archives' retention can, so the access date matters. [Data Publishing](../01-data-best-practices/03_data_publishing.md) in Module 1 covers citing data.

:::{admonition} Partner review (NOAA): Citing NWM forecasts
:class: important
Confirm the recommended citation for NWM operational forecast output (is there a preferred citation or DOI?).
:::

## Best practices FAQs

The sections below answer these questions, with code examples. All three answers follow from how NWM files are stored, so we start with [why NWM downloads cost what they cost](#nwm-cost).

* What is the recommended way to download data for **one location across the full period of record**? See [Temporal scaling](#nwm-temporal-scaling).
* What is the recommended way to download data across **all locations for a small time range**? See [Spatial scaling](#nwm-spatial-scaling).
* If I am working on improving efficiency through **code parallelization**, what should I do vs avoid? See [Parallelization](#nwm-parallelization).

(nwm-cost)=
### Why NWM downloads cost what they cost

One fact about the files explains almost every recommendation below. Inside each NWM `channel_rt` file, `streamflow` is stored as **one compressed chunk per forecast hour that contains all 2,776,734 reaches** (about 2 MB compressed). There is no way to read "just my reach" from a file: any tool that reads the files has to fetch at least that whole chunk. A service such as the NOAA NWM API is different: it returns just the reaches you ask for, and whatever reading of the underlying data that takes happens on its side. For the files themselves:

* **Cost grows with the number of forecast hours (files) you touch, not with the number of reaches.**
* `hydrotools` downloads whole files (~13–16 MB each, every variable). Kerchunk references fetch only the `streamflow` chunk you need (~2 MB per hour), so they move fewer bytes, but the bytes are still CONUS-sized.

:::{admonition} TODO (dev team): How the NWM API stores data
:class: attention
Verify how the NOAA NWM API stores NWM data.
:::

We measured this for the Louisville reach, using three short-range runs before the April 2025 crest (issued 6 April 00Z and 12Z and 7 April 00Z: 54 hourly files), from a home internet connection, on 2026-10-08:

| Route | Reaches | Data transferred | Peak memory | Wall time |
|---|---|---|---|---|
| NOAA NWM API (today's data; all 99 short-range runs it held) | 1 | 0.13 MB | 0.1 GB | < 1 s |
| `hydrotools` (Google Cloud) | 1 | 844 MB (saved to disk) | 1.7 GB | 2.6 min |
| `hydrotools` (Google Cloud) | 498 | 844 MB (saved to disk) | 1.8 GB | 2.7 min |
| Kerchunk references + `xarray` | 1 | 125 MB | 0.5 GB | 10 s |
| Kerchunk references + `xarray` | 498 | 125 MB | 1.0 GB* | 19 s |
| *Building the references (one time), as in the example above* | – | 57 MB, in 54 requests | 0.2 GB | 19 s |

\* This run also loaded the NLDI navigation (`pynhd`, `geopandas`) to get the 498 COMIDs, which accounts for part of the extra memory.

Going from 1 reach to 498 reaches changed neither the data transferred nor, for `hydrotools`, the memory (1.7 vs 1.8 GB). Wall times vary a lot with network conditions; treat them as rough. These flood-time files were larger than files from quiet periods (844 MB for 54 files here, versus about 700 MB in an earlier test of a different period), because high, changing flows compress less well.

:::{admonition} TODO (dev team): Re-time the kerchunk measurements
:class: attention
Re-time on a quiet connection and in-cloud.
:::

One **medium-range** member (issued 2025-04-03 00Z: 240 hourly files) scales the same way, about 13× a short-range run:

| Route | Reaches | Data transferred | Peak memory | Wall time |
|---|---|---|---|---|
| `hydrotools` (Google Cloud) | 1 | ~3 GB or more (240 whole files); not re-measured, see the timeout note above | – | – |
| Kerchunk references + `xarray` | 1 | 520 MB | 0.4 GB | 38 s |
| *Building the references (one time)* | – | 252 MB, in 240 requests | 0.2 GB | 92 s |

(nwm-temporal-scaling)=
### Temporal scaling

What is the recommended way to download data for one location but a long period?

**Recent forecasts (last few days):** use the NOAA NWM API. One request returns every run it still holds.

**Past forecasts (NWM forecast history):** every reference time is a separate set of files, so cost grows linearly with the number of forecast runs: ~280 MB per short-range run and ~3 GB per medium-range member with `hydrotools`, or ~40 MB per short-range run with kerchunk references. Short range is issued every hour, so a month of every short-range run is 720 runs: ~200 GB of downloads with `hydrotools`, or ~30 GB of chunk reads with references. Before you start, ask whether you need *every* run. For "how did the forecast change approaching the crest?", a handful of issue times is usually enough, as in the figure above.

For more than a handful of runs, use kerchunk references (built once, reused), ideally from a cloud machine in the same region as the bucket (Google Cloud's `US` multi-region for `gs://national-water-model`; AWS `us-east-1` for `s3://noaa-nwm-pds`), so the CONUS-sized chunks never cross your home connection. `NWMFileClient.get()` does accept a list of reference times, but it processes them one at a time, keeps every downloaded file on disk until you delete it, and used ~1.7 GB of memory in our test (the documentation recommends at least a 4-core processor and 8 GB of RAM).

Availability depends on the source. According to the [hydrotools NWM Client documentation](https://github.com/NOAA-OWP/hydrotools/tree/main/python/nwm_client), Google Cloud holds the largest amount of operational forecast data, which is why `hydrotools` uses it by default. On 2026-10-07 the AWS bucket `noaa-nwm-pds` held every day from 2025-01-01 onward (earlier descriptions call it a rolling four-week archive). Not every configuration covers the whole archive (the Alaska configurations, for example, only became available after August 2023).

:::{admonition} Partner review (NOAA): Temporal scaling
:class: important
Confirm the retention policy of each mirror.
:::

**NWM retrospective.** If you need a long *simulated* record rather than forecasts, use the NWM retrospective simulations: multi-decade model runs over historical weather, not archived forecasts. They cover every reach, so they are the way to get a long streamflow record for a reach with no gage. Version 3.0 covers February 1979 through January 2023, and version 2.1 covers February 1979 through December 2020. Their output frequency and fields differ from the operational forecast model. Zarr versions are available on AWS for version 2.1, and NCAR describes Zarr stores for version 3.0 (see the [NWM retrospective registry entry](https://registry.opendata.aws/nwm-archive/)).

:::{admonition} TODO (dev team): NWM retrospective dates and Zarr source
:class: attention
Verify retrospective date ranges and link the NCAR v3.0 Zarr source.
:::

(nwm-spatial-scaling)=
### Spatial scaling

What is the recommended way to download data for all locations but a small time range?

Start with **discovery** to build your list of COMIDs (e.g. every reach up to 100 km upstream of Louisville, as above), then pass the whole list to the download step in one call rather than looping one COMID at a time. Looping over COMIDs re-reads the same CONUS-wide chunks for every reach.

* **`hydrotools`:** `NWMFileClient.get()` accepts a list of COMIDs. In our test, 498 reaches cost the same downloads and memory as 1 reach. If you omit `nwm_feature_ids`, it returns a default set: channel reaches that `hydrotools` maps to stream gages (8,866 in `hydrotools.nwm_client` 9.2.1).
* **Kerchunk references:** keep only the COMIDs that are NWM reaches (almost all NHDPlus reaches are, but check), then select them all at once (example below). Again, 498 reaches fetched exactly the same 125 MB as one reach.

* **NOAA NWM API:** accepts a comma-separated list of COMIDs, but it is built for a few reaches. For hundreds or thousands, use one of the file-based routes.

  :::{admonition} TODO (dev team): NWM API limit on IDs per request
  :class: attention
  Verify any documented limit on IDs per API request.
  :::

Here is the kerchunk version, reusing `ds` (the 6 April 00Z run) and `upstream_comids` from above:

```python
import numpy as np

# keep only COMIDs that exist in the NWM output, then read them all in one selection
ids = np.array(upstream_comids)
ids = ids[np.isin(ids, ds["feature_id"].values)]
basin = ds["streamflow"].sel(feature_id=ids).load()
print(basin.shape)   # (forecast hours, reaches)
```

```text
(18, 498)
```

`basin` is an `xarray.DataArray` with one row per forecast hour and one column per reach.

`hydrotools` results come back as pandas DataFrames that use categorical columns to save memory. The documentation notes that categorical columns can behave unexpectedly in groupby operations, are incompatible with fixed-format HDF files (use `format="table"`), and may cause problems when writing to geospatial formats with geopandas. Casting a categorical column to `str` resolves these issues. Setting `compute=False` returns a dask DataFrame instead of a pandas one.

(nwm-parallelization)=
### Parallelization

* **Parallelize over files (forecast hours or runs), not over reaches.** Reaches share chunks, so splitting COMIDs across workers multiplies the bytes; splitting files across workers doesn't.
* **Kerchunk + dask:** opening references with `chunks={}` gives you dask arrays with one task per chunk, so `.load()` fetches chunks concurrently. Building references makes one request per file (with 1 MB blocks), so a thread pool (as in the example above, 8 threads) helps a lot. We saw intermittent SSL errors from too many simultaneous connections at 16 threads (with `gcsfs`); fewer threads plus a retry fixed it.
* **`hydrotools`:** downloads are already asynchronous. The `FileDownloader` class has `limit` (default 10 concurrent downloads) and `timeout` (default 900 seconds) settings. Files for a single forecast cycle are processed in groups of 20 by default (the `group_size` parameter of `get_files()`); the documentation says this accommodates the xarray, dask, and HDF5 backends, which may struggle to open too many files at once, and that it matters mostly for medium-range forecasts. Running several `NWMFileClient.get()` calls at once mostly multiplies disk use and memory (~1.7 GB each in our test).
* **Run next to the data** when the job is big. Moving compute to a cloud machine in the bucket's region does more for large NWM jobs than any amount of local parallelism.

## Now you try it

Repeat the main steps on the course's second river: the **Willamette River at Salem, Oregon**. The Willamette drains the valley between Oregon's Coast Range and Cascades and runs high in winter, when Pacific storms bring heavy rain.

**Your task**

1. Find the COMID of the Willamette at Salem with `nldi.feature_byloc`. Change `POINT` to `(-123.0429, 44.9443)`.
2. Get the latest short-range forecast for that COMID from the NOAA NWM API. Change `comid` in the API example.
3. The Willamette ran high in late February 2026. Read the short-range forecast issued at 12Z on 25 February 2026 from NOAA's published references. Change `day` to `"20260225"` in the published-references example (keep `t12z`).

**What you should see:** COMID **23791093**; an API response with 18 hourly values in `CMS` (the API's `name` field is blank for this reach); and 18 published reference files for 25 February, with streamflow of about 1,700–1,800 m³/s, rising through the run.

:::{dropdown} Answer
```python
from pynhd import NLDI
import requests

POINT = (-123.0429, 44.9443)        # Willamette River at Salem, OR
comid = int(NLDI().feature_byloc(POINT)["comid"].iloc[0])
print("COMID:", comid)

url = f"https://api.water.noaa.gov/nwm/v1/streamflow/forecast/nwm_feature_id/{comid}/"
resp = requests.get(url, params={"configuration": "short_range", "latest": "true"}, timeout=60)
resp.raise_for_status()
run = resp.json()[0]
print(run["reference_datetime"], run["units"], len(run["forecast"][0]["timeseries"]), "values")

# NOAA-published references for the 2026-02-25 12Z short-range run (uses s3, load_ref, open_refs from above)
paths = sorted(s3.glob("noaa-nodd-kerchunk-pds/nwm/short_range/"
                       "nwm.short_range.channel_rt.conus.20260225.t12z.f*.nc.zarr"))
feb = MultiZarrToZarr([load_ref(p) for p in paths], remote_protocol="https", concat_dims=["time"],
                      identical_dims=["feature_id", "reference_time", "crs"]).translate()
q_feb = open_refs(feb)["streamflow"].sel(feature_id=comid).load().to_series()
print(len(paths), "reference files")
print(q_feb.iloc[[0, 8, 17]])
```

```text
COMID: 23791093
2026-10-09T02:00:00Z CMS 18 values
18 reference files
time
2026-02-25 13:00:00    1717.849962
2026-02-25 21:00:00    1807.389960
2026-02-26 06:00:00    1816.159959
Name: streamflow, dtype: float64
```
:::

:::{admonition} TODO (dev team): Learner-review friction items (P6.5.4)
:class: attention
From the integration-pass learner review (2026-10-09). Not yet fixed:
- Decision for Lindsay: the NLDI lookup by gage ID (`USGS-03294500`) is the one other-agency mention in Module 3. Either drop it (the point lookup already finds the COMID) or record it as an allowed exception in STYLE_GUIDE §2.
- Move the environments TODO callout to the end of "Tools and environment setup" so learners don't read it as "skip this step".
- Add one query block (`POINT`, reference day, cycle) and stop re-typing `comid = 10164004` in later blocks (needs a re-run).
- Add an "Explore by clicking" row (NWPS map) to the access-route table; `json.dump` with `with open(...)` and an explicit `import json`; explain `nudge`.
- Link first uses of glossary terms: ensemble member, long-format table, chunk, lead time.
:::

## Further reading

* [Meet NOAA NWM](../02-federal-water-data-landscape/02_meet_noaa_nwm.md) (Module 2): what the model is and how its configurations differ.
* NLDI documentation: https://api.water.usgs.gov/docs/nldi
* `pynhd` (HyRiver) documentation: https://docs.hyriver.io/readme/pynhd.html; cite HyRiver as https://doi.org/10.21105/joss.03175
* NOAA NWM API (experimental) documentation: https://api.water.noaa.gov/nwm/v1/docs
* National Water Prediction Service API documentation: https://api.water.noaa.gov/nwps/v1/docs/
* OWPHydroTools (hydrotools) GitHub repo: https://github.com/NOAA-OWP/hydrotools
* OWPHydroTools NWM Client documentation: https://noaa-owp.github.io/hydrotools/hydrotools.nwm_client.html and package page: https://pypi.org/project/hydrotools.nwm-client/
* NWM operational archive on Google Cloud: https://console.cloud.google.com/marketplace/product/noaa-public/national-water-model
* NWM operational data on AWS (Registry of Open Data): https://registry.opendata.aws/noaa-nwm-pds/
* NOAA Cloud Optimized Zarr Reference Files (Kerchunk), Registry of Open Data: https://registry.opendata.aws/noaa-nodd-kerchunk/
* Kerchunk documentation: https://fsspec.github.io/kerchunk/
* `nwmurl` (CIROH), builds NWM file URLs: https://hub.ciroh.org/docs/products/data-management/dataaccess/NWMURL%20Library and source: https://github.com/CIROH-UA/nwmurl
* Tuhinanshu, T. (2023), *Using Kerchunk to make NOAA's National Water Model dataset more accessible*, Element 84: https://element84.com/software-engineering/using-kerchunk-to-make-noaas-national-water-model-dataset-more-accessible/
* NWM retrospective archive (Zarr, AWS): https://registry.opendata.aws/nwm-archive/
* Example code for `hydrotools` adapted from the [OWPHydroTools NWM Client README](https://github.com/NOAA-OWP/hydrotools/tree/main/python/nwm_client) (NOAA-OWP).

  :::{admonition} TODO (dev team): hydrotools attribution
  :class: attention
  Verify license/attribution wording for adapted hydrotools examples.
  :::
