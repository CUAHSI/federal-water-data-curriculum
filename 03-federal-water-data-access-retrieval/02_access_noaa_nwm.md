# Retrieve NOAA NWM streamflow data

NOAA National Water Model (NWM) streamflow data lives in a few different places depending on what you need. The full model output has no general-purpose REST API behind it: it's stored as NetCDF files, made available through file listings and mirrored to cloud storage (Google Cloud Platform, AWS). NOAA does host a separate, official API, [NWPS](https://api.water.noaa.gov/nwps/v1/docs/), but it only covers NWM output at NWPS's ~4,000 established forecast locations, not the full 2.7-million-reach domain, so we're not going to focus on that here. NOAA's experimental [NWM API](https://api.water.noaa.gov/nwm/v1/docs) does serve individual reaches, but only for the most recent few days of forecasts (see below).

1. **Programmatic data discovery**: NWM identifies reaches using COMIDs, which come from the NHDPlusV2 hydrography dataset (a USGS product, not a NOAA one). Before you can download streamflow for a location, you first need to find the COMID that corresponds to it. This is handled by USGS's Network Linked Data Index (NLDI), a separate service from wherever the NWM output files live.
1. **Programmatic data downloads**: once you have COMID(s) in hand, there are several ways to retrieve forecast values, and the best one depends on *how much* data you need (see the table below). This module focuses on **forecast** data. NWM's forecast products (short/medium/long range) are what set it apart from other streamflow datasets, since they predict rather than just record. For historical, observed streamflow, USGS NWIS is the recommended source instead; however, see the note at the end of this section for how NWM's historical/retrospective archive is relevant for ungauged reaches.

If you already know your COMID(s), you can skip programmatic data discovery.

(nwm-access-routes)=
## Which access route for which use case?

NWM output is big: every forecast hour is a file covering all ~2.8 million reaches. How you should access it depends mostly on **how many forecast runs (issue times) you need**, and much less on how many reaches. Except for the CIROH BigQuery API (last row), none of these routes needs an API key.

| Use case | Recommended route | Key? | Caveat |
|---|---|---|---|
| Today's / the last few days' forecasts for a few reaches | [NOAA NWM API](#nwm-api) | No | Keeps only ~3–5 days; labelled experimental |
| Past forecasts, a few reaches, a few issue times | [`hydrotools`](#nwm-hydrotools) (Google Cloud archive) | No | Downloads whole CONUS files (~235 MB per short-range run); cost grows with the number of runs, not reaches |
| Past forecasts for many reaches or a region, or many issue times | [Kerchunk references](#nwm-kerchunk) + `xarray`/`dask`, ideally run in the cloud | No | Lazy reads, ~7× fewer bytes and less memory than whole files, but each read is still a CONUS-wide chunk; building references is a one-time step |
| Long historical record (simulation, not forecasts) | NWM retrospective (cloud Zarr) | No | Different product (see [Temporal scaling](#nwm-temporal-scaling)) |
| Researchers working on CIROH projects | [CIROH NWM BigQuery API](https://hub.ciroh.org/docs/products/data-management/bigquery-api/) | Yes, by request | Free for CIROH members and partners with active CIROH projects; request access and estimate query costs first (see the CIROH page). Not covered further in this lesson |

The numbers behind these recommendations are in [Why NWM downloads cost what they cost](#nwm-cost).

## Tools and environment setup

We're using a dedicated `conda` environment to manage dependency collisions with other lessons. [TODO / for consideration: should we use environments to avoid dependency collisions? Or try to actually address any dependency collisions? We ultimately want people to be able to use all three datasets on their computers, and give them the knowledge and tools to do so]

The environment file [`environments/nwm.yml`](../environments/nwm.yml) lists everything this page uses. From the root of the course repository:

```bash
conda env create -f environments/nwm.yml
conda activate nwm
```

This installs everything needed for discovery (`pynhd`), all three download routes (`requests` for the NWM API, `hydrotools.nwm_client`, and `kerchunk` + `xarray` + `fsspec`) in one place, so you don't have to juggle separate environments to go from "find a COMID" to "pull its forecast" within the same script or notebook. None of the routes on this page need an API key or account.

## Programmatic data discovery

Before you download or try to access the data itself, a common first step is to *discover* or *find* the specific reach(es) you need. You don't want to page through the whole NWM domain just to learn which COMID matches your location. Doing this discovery step first also lets you build a COMID list once and reuse it, which matters more once you get to spatially scaling (see [Spatial scaling](#nwm-spatial-scaling)).

A GUI (graphic user interface) approach exists here too: NOAA's own [interactive map](https://water.noaa.gov/map) lets you click a point and read off a reach ID directly, which is functionally the same identifier as a COMID [PARTNER REVIEW: NOAA] confirm the map's reach ID is the NWM `feature_id`. That's a fine way to explore or spot-check, but a programmatic discovery step keeps your work reproducible and reusable, and it's worth capturing in code even if you first found the reach by clicking around.

### USGS Network Linked Data Index (NLDI)

NOAA NWM identifies stream reaches using **COMIDs** (also called `feature_id`, `nwm_feature_id` or ComID). This is NWM's *Location Identifier* (see the shared vocabulary in Module 2). The NLDI can:

* Find the COMID for a point on the map (point-in-polygon lookup against NHDPlusV2 catchments)
* Find the COMID(s) associated with a known site, e.g. a USGS gage
* Navigate the river network upstream/downstream from a starting COMID (upstream mainstem, upstream with tributaries, downstream mainstem, downstream with diversions), useful for "all reaches in this watershed" style questions

We use the [`pynhd`](https://docs.hyriver.io/readme/pynhd.html) package (part of HyRiver) to call the NLDI from Python.

**Example: what's the COMID for the stream closest to the CUAHSI office?**

`feature_byloc` takes a `(longitude, latitude)` pair (EPSG:4326 by default) and snaps it to the nearest NHDPlus flowline using the NLDI `position` endpoint.

```python
from pynhd import NLDI

nldi = NLDI()

# (longitude, latitude) of the CUAHSI office, in EPSG:4326
comid_gdf = nldi.feature_byloc((-71.1739, 42.4238))
comid = int(comid_gdf.comid.iloc[0])

print(comid_gdf.drop(columns="geometry"))
print(f"Nearest COMID: {comid}")
```

It returns a one-row GeoDataFrame with the matching `comid` and the flowline geometry; here the nearest COMID is `5867673`.

The same lookup with the raw NLDI REST endpoint (point-in-polygon lookup), which you can paste into a browser:

```text
https://api.water.usgs.gov/nldi/linked-data/comid/position?coords=POINT(-71.1739 42.4238)
```

**Example: what's the COMID for a USGS gage?**

[TODO: switch example: per Lindsay (2026-10-08), the Skagit River / December 2025 flood is reserved for the Module 4 case study. Replace the Skagit gage, reaches and dates throughout this page (discovery, API, hydrotools, kerchunk, cost tables) with a Module 3 example, and re-run the measurements.]

Throughout the rest of this page (and in Module 4) we use USGS gage 12200500, *Skagit River near Mount Vernon, WA*, which saw major flooding in December 2025. NLDI indexes USGS gages as the `nwissite` source, so you can ask for the reach the gage sits on directly:

```python
from pynhd import NLDI

nldi = NLDI()

# USGS gage 12200500, Skagit River near Mount Vernon, WA (the Module 4 case study)
gage = nldi.getfeature_byid("nwissite", "USGS-12200500")
comid = int(gage.comid.iloc[0])
print(gage[["identifier", "name", "comid"]])
print(f"COMID for the gage reach: {comid}")
```

```text
      identifier                                name     comid
0  USGS-12200500  SKAGIT RIVER NEAR MOUNT VERNON, WA  24270288
COMID for the gage reach: 24270288
```

**Example: every reach upstream of the gage**

For regional questions you want a *list* of COMIDs. `navigate_byid` walks the network from a starting COMID; `upstreamTributaries` follows every tributary, and `distance` (km) caps how far to go.

```python
# every NHDPlus flowline upstream of the gage, tributaries included, up to 500 km
upstream = nldi.navigate_byid(fsource="comid", fid=str(comid),
                              navigation="upstreamTributaries", source="flowlines", distance=500)
upstream_comids = upstream["nhdplus_comid"].astype(int).tolist()
print(f"{len(upstream_comids)} reaches upstream of (and including) the gage")
```

This returns a GeoDataFrame of flowlines with an `nhdplus_comid` column: **2,540 reaches** for the whole Skagit basin above Mount Vernon. We reuse `upstream_comids` in [Spatial scaling](#nwm-spatial-scaling).

Once you have your desired COMID(s), move on to downloads below.

## Programmatic data downloads

While the discovery step above uses a USGS service, the forecast values come from NOAA. This section covers three routes, in order of how much data they're built for: the NOAA NWM API, `hydrotools`, and kerchunk references read with `xarray`. All three return NWM's *Variable* `streamflow` in m³/s (the API labels it `CMS`) for each COMID; NWM has no per-value *Data Quality Flag* [PARTNER REVIEW: NOAA] confirm, so record the configuration, reference time and model version with your data instead (see Module 2).

Two terms you'll see in every route:

* **Configuration**: which forecast product, e.g. `short_range` (hourly out to 18 hours, issued every hour), `medium_range` (out to 10 days, issued every 6 hours, with several ensemble members), `long_range`, or `analysis_assim` (the model's best estimate of current conditions). [PARTNER REVIEW: NOAA] confirm cadences, horizons and ensemble sizes for NWM v3.0.
* **Reference time**: when a forecast was issued (UTC). The time each forecast value applies to is the *valid time* (`value_time` in `hydrotools`).

(nwm-api)=
### NOAA NWM API: today's forecasts for a few reaches

NOAA's [NWM API](https://api.water.noaa.gov/nwm/v1/docs) returns forecasts for one or more reaches as JSON, with no key and no files to manage. It is labelled **experimental**, and it only keeps roughly the **last 3–5 days** of forecasts (on 2026-10-07 the oldest short-range run it held was from 2026-10-03, and the oldest medium-range run from 2026-10-04). Use it for "what is the model predicting now?", not for past events. [PARTNER REVIEW: NOAA] confirm the API's retention window and whether it is intended for research use.

**Example: the latest short-range forecast at the Skagit gage reach**

```python
import requests
import pandas as pd

comid = 24270288  # from the discovery step
url = f"https://api.water.noaa.gov/nwm/v1/streamflow/forecast/nwm_feature_id/{comid}/"

# latest short-range forecast for this reach
resp = requests.get(url, params={"configuration": "short_range", "latest": "true"}, timeout=60)
resp.raise_for_status()
run = resp.json()[0]  # one entry per configuration + reference time

forecast = pd.DataFrame(run["forecast"][0]["timeseries"])
forecast["valid_datetime"] = pd.to_datetime(forecast["valid_datetime"])
print(run["configuration"], run["reference_datetime"], run["units"])
print(forecast.head())
```

```text
short_range 2026-10-07T23:00:00Z CMS
             valid_datetime   value
0 2026-10-08 00:00:00+00:00  216.91
1 2026-10-08 01:00:00+00:00  215.99
...
```

The response is a list with one entry per forecast run. Each entry carries `nwm_feature_id`, `configuration`, `reference_datetime`, `units` and a `forecast` list with one item per ensemble member (`member_id`), each holding a `timeseries` of `valid_datetime`/`value` pairs. You can pass several COMIDs separated by commas in the URL.

**Example: every recent medium-range run, all ensemble members**

Leave out `latest` and use `min_reference_datetime` / `max_reference_datetime` to get several runs at once:

```python
import requests
import pandas as pd

comid = 24270288
url = f"https://api.water.noaa.gov/nwm/v1/streamflow/forecast/nwm_feature_id/{comid}/"

# every medium-range run issued in the last 2 days (the API only keeps the last few days)
since = (pd.Timestamp.now(tz="UTC") - pd.Timedelta("2D")).strftime("%Y-%m-%dT%H:00:00Z")
resp = requests.get(url, params={"configuration": "medium_range",
                                 "min_reference_datetime": since}, timeout=120)
resp.raise_for_status()

rows = []
for run in resp.json():
    for member in run["forecast"]:
        for step in member["timeseries"]:
            rows.append({"reference_time": run["reference_datetime"], "member": member["member_id"],
                         "valid_time": step["valid_datetime"], "streamflow_cms": step["value"]})

runs = pd.DataFrame(rows)
print(runs.groupby("reference_time").member.nunique())
```

Each medium-range run had 6 ensemble members in the API response (member 1 runs out to 240 hours, the others to 204 hours). In our test, every short-range run the API held for one reach (116 runs) came back in a single **0.15 MB** response in under 10 seconds.

(nwm-hydrotools)=
### `hydrotools`: past forecasts from the cloud archive

For anything older than a few days, such as the December 2025 Skagit flood, you need NOAA's archive of the raw NWM output files. The operational archive is mirrored, with no key or account needed, on [Google Cloud](https://console.cloud.google.com/marketplace/product/noaa-public/national-water-model) (`gs://national-water-model`) and on [AWS](https://registry.opendata.aws/noaa-nwm-pds/) (`s3://noaa-nwm-pds`). Each forecast hour is a separate NetCDF file covering all ~2.8 million reaches (about 13 MB for a short-range `channel_rt` file).

`hydrotools` (OWPHydroTools, from NOAA-OWP) finds those files, downloads them, and hands you a `pandas.DataFrame` for just the COMIDs you asked for. You never need to open a NetCDF file yourself.

**Key pieces**

* `hydrotools.nwm_client`: retrieve NWM streamflow forecasts. (Older tutorials use `hydrotools.nwm_client_new`; its last release was 8.0.0 in December 2024, and development continues as [`hydrotools.nwm_client`](https://pypi.org/project/hydrotools.nwm-client/), currently 9.x, with the same `NWMFileClient` interface.)
* `hydrotools.waterdata_client`: the modernized replacement for the legacy `nwis_client`, for pulling matching USGS observations for forecast evaluation (see the USGS lesson).
* Canonical column names used across all subpackages: `value`, `value_time`, `variable_name`, `nwm_feature_id` (the COMID), `usgs_site_code`, etc. This consistency makes it easy to join NWM and USGS data.

**Example: the short-range forecast issued at 00Z on December 11, 2025**

```python
from hydrotools.nwm_client.NWMFileClient import NWMFileClient

comid = 24270288  # from the discovery step

# downloads go to ./hydrotools_data/NWMFileClient_NetCDF_files; results are cached in ./hydrotools_data/nwm_store.parquet
client = NWMFileClient()   # default catalog: Google Cloud Platform

forecast_data = client.get(
    configurations=["short_range"],
    reference_times=["2025-12-11T00:00"],   # forecast issue time (UTC)
    nwm_feature_ids=[comid],
)
print(forecast_data[["reference_time", "value_time", "value", "measurement_unit", "usgs_site_code"]].head().to_string())
```

```text
  reference_time          value_time        value measurement_unit usgs_site_code
0     2025-12-11 2025-12-11 01:00:00  1864.630005           m3 s-1       12200500
1     2025-12-11 2025-12-11 02:00:00  1943.659912           m3 s-1       12200500
2     2025-12-11 2025-12-11 03:00:00  2066.820068           m3 s-1       12200500
...
```

The result is a long-format `pandas.DataFrame`, one row per COMID and valid time, with columns `reference_time`, `nwm_feature_id`, `value_time`, `value`, `measurement_unit`, `variable_name`, `configuration` and `usgs_site_code` (filled in where NWM maps the reach to a USGS gage, as here). Values are in SI units (`m3 s-1`); pass `unit_system=MeasurementUnitSystem.US` (from `hydrotools.nwm_client.NWMClientDefaults`) to `NWMFileClient` for cubic feet per second.

**If `.get()` fails:**

* **In Jupyter or another notebook**, `hydrotools` raises `RuntimeError: asyncio.run() cannot be called from a running event loop`, because its downloader starts its own event loop. Run `import nest_asyncio; nest_asyncio.apply()` once before calling `.get()` (`nest-asyncio` is in the course environment).
* **With errors about reading a NetCDF/HDF file**, an earlier run was probably interrupted (a timeout, a lost connection or a stopped cell), leaving a half-downloaded file in `hydrotools_data/`. `hydrotools` treats files already in that folder as downloaded, so it tries to open the broken one instead of fetching it again. Delete the `hydrotools_data/` folder in your working directory and run the call again.
* The `FutureWarning` and `UserWarning` messages printed during `.get()` (from `xarray`, `dask` and Google's libraries) are harmless: if the table prints, it worked.

`hydrotools` downloads files asynchronously. If you run it inside Jupyter (which already runs an event loop) and get an event-loop error, add `import nest_asyncio; nest_asyncio.apply()` at the top of the notebook (`nest-asyncio` is in the environment file). This is a known issue on JupyterHub; plain Python scripts don't need it.

What happens behind the `.get()` call matters for cost: `hydrotools` downloads **every file of every forecast run you ask for, in full**, to `hydrotools_data/NWMFileClient_NetCDF_files/` in your working directory, then extracts your COMIDs. One short-range run is 18 files (~235 MB); one medium-range member is 240 files (~3.1 GB). Results are cached in `hydrotools_data/nwm_store.parquet`, so asking for the same run again is fast. Just importing `NWMFileClient` creates the `hydrotools_data/` folder in the current directory, so keep it out of version control (e.g. add it to `.gitignore`) and delete it when you're done. You can also pass `file_directory=` to choose where files go, or `cleanup_files=True` to delete the downloaded NetCDF files after each `get()`.

**On a slow connection, large requests can time out.** `hydrotools` queues every file of a run at once and gives each download 900 seconds, including time spent waiting in the queue. In our test, a medium-range member (3.1 GB) on a shared home connection timed out after ~15 minutes in both clean attempts (138 of 240 files downloaded in the first). Rerunning the same call did *not* recover cleanly: the half-written file was skipped as "already downloaded" and then failed to open (see "If `.get()` fails" above). Retry on a faster connection, or use kerchunk references (below), which fetch about 7× less.

(nwm-kerchunk)=
### Kerchunk references: lazy, cloud-native reads with `xarray`

NetCDF files aren't designed to be read piece by piece over the internet. **Kerchunk** fixes that without copying the data: it scans each file once and writes a small JSON "reference" file that records *where inside the original file* each chunk of each variable lives (byte offset and length). `xarray` can then open the references as if they were one Zarr dataset and fetch **only the chunks you touch**, straight from the cloud bucket. See the [kerchunk documentation](https://fsspec.github.io/kerchunk/) and Element 84's write-up, [Using Kerchunk to make NOAA's National Water Model dataset more accessible](https://element84.com/software-engineering/using-kerchunk-to-make-noaas-national-water-model-dataset-more-accessible/) (2023).

Two kinds of reference are available:

1. **NOAA-published references.** NOAA's Open Data Dissemination program publishes ready-made references in `s3://noaa-nodd-kerchunk-pds` ([registry entry](https://registry.opendata.aws/noaa-nodd-kerchunk/)) for NWM `short_range` and `medium_range_mem1` (plus the Alaska, Hawaii and Puerto Rico short range), built automatically as new files arrive. On 2026-10-07 they started at **2026-01-01**, so they don't cover the December 2025 case study. [PARTNER REVIEW: NOAA] confirm how far back these references are kept.
2. **References you build yourself** for any files in the archive. This is a one-time step per forecast run, and the result is tiny (22 KB of JSON for an 18-file short-range run).

**Example: build references for the December 11, 2025 00Z short-range run**

The first step is a list of the run's files. CIROH's [`nwmurl`](https://hub.ciroh.org/docs/products/data-management/dataaccess/NWMURL%20Library) library builds NWM file URLs from a date, issue time, forecast hours, configuration and archive, so you don't have to know the archive's folder and file-naming scheme. It only builds URLs; it doesn't download anything. Its arguments are numeric codes, listed on that page (and in the comments below).

```python
import fsspec
import nwmurl
from concurrent.futures import ThreadPoolExecutor
from kerchunk.hdf import SingleHdf5ToZarr
from kerchunk.combine import MultiZarrToZarr

# the 18 hourly files of the 2025-12-11 00Z short-range forecast, as public HTTPS URLs
urls = nwmurl.generate_urls_operational(
    start_date="202512110000", end_date="202512110000",  # YYYYMMDDHHMM; one day
    fcst_cycle=[0],                  # issue time: 00Z
    lead_time=list(range(1, 19)),    # forecast hours 1-18
    varinput=1,                      # 1 = channel_rt (streamflow)
    geoinput=1,                      # 1 = CONUS
    runinput=1,                      # 1 = short_range
    urlbaseinput=3,                  # 3 = https://storage.googleapis.com/national-water-model/
    meminput=None,                   # short_range has no ensemble members
)
print(urls[0])

def index_one(url):
    """Scan one NetCDF file's internal layout and return its byte-range references."""
    with fsspec.open(url, "rb", block_size=2**20) as f:   # read in 1 MB blocks (see below)
        return SingleHdf5ToZarr(f, url, inline_threshold=500).translate()

with ThreadPoolExecutor(8) as pool:          # one request per file: run them in parallel
    singles = list(pool.map(index_one, urls))

# stitch the 18 per-file references into one dataset along the time dimension
refs = MultiZarrToZarr(singles, remote_protocol="https", concat_dims=["time"],
                       identical_dims=["feature_id", "reference_time", "crs"]).translate()
print(len(urls), "files indexed;", len(refs["refs"]), "reference entries")
```

```text
https://storage.googleapis.com/national-water-model/nwm.20251211/short_range/nwm.t00z.short_range.channel_rt.f001.conus.nc
18 files indexed; 134 reference entries
```

A few choices in this code are deliberate:

* `urlbaseinput=3` asks `nwmurl` for the public HTTPS address of each file in the Google Cloud archive, so both scanning and later reads use plain HTTPS with no cloud account. In our tests, reading through `gcsfs` with the current `zarr`/`kerchunk` versions stalled, while HTTPS worked. [TODO: verify whether the gcsfs stall is Windows-only] `nwmurl` can also point at the AWS copy (`urlbaseinput=7`) or other configurations (e.g. `runinput=2` and `meminput=1` for medium-range member 1).
* `inline_threshold=500` stores tiny variables (like the single `time` value in each file) directly in the JSON, so the combine step doesn't need to download anything.
* `block_size=2**20` makes each file's scan one 1 MB request, which covers the file's metadata. fsspec's default 5 MB block read about 5× more data for no benefit, and smaller blocks took many more requests and were slower. In our test the build took 4 s and 19 MB for this run.
* Save `refs` to a JSON file (`json.dump`) and reuse it, rather than rebuilding.

Check that `nwmurl` gave you files that exist: a URL for a run that isn't in the archive fails when `index_one` opens it. `generate_urls_operational(..., enforce_valid_outputs=1)` checks each URL first and drops missing ones.

**Example: read the gage reach from the references**

```python
import xarray as xr

def open_refs(refs):
    """Open kerchunk references lazily: nothing is downloaded until values are needed."""
    return xr.open_dataset("reference://", engine="zarr", chunks={}, consolidated=False, zarr_format=2,
                           storage_options={"fo": refs, "remote_protocol": "https",
                                            "remote_options": {"asynchronous": True}})

ds = open_refs(refs)
print(ds)

# pull one reach: reads 1 chunk per forecast hour (~1.8 MB each), not the whole 13 MB files
q = ds["streamflow"].sel(feature_id=comid).load()
print(q.to_series().head())
```

```text
<xarray.Dataset> Size: 2GB
Dimensions:         (time: 18, feature_id: 2776734, reference_time: 1)
Coordinates:
  * time            (time) datetime64[ns] 144B 2025-12-11T01:00:00 ... 2025-1...
  * feature_id      (feature_id) int64 22MB 101 179 ... 1180001803 1180001804
  * reference_time  (reference_time) datetime64[ns] 8B 2025-12-11
Data variables:
    streamflow      (time, feature_id) float64 400MB dask.array<chunksize=(1, 2776734), meta=np.ndarray>
    velocity        (time, feature_id) float64 400MB dask.array<chunksize=(1, 2776734), meta=np.ndarray>
    ...
time
2025-12-11 01:00:00    1864.629958
2025-12-11 02:00:00    1943.659957
2025-12-11 03:00:00    2066.819954
...
```

`ds` is an `xarray.Dataset` with dimensions `time` (the 18 forecast hours, i.e. valid times) and `feature_id` (2,776,734 reaches), and variables `streamflow` (m³/s), `velocity`, `nudge` and a few runoff terms. The "2GB" size is what the full dataset *would* be in memory; nothing is downloaded until `.load()`. Note `chunksize=(1, 2776734)`: one chunk per hour holding every reach. The values match `hydrotools` exactly.

**Example: use NOAA's published references for a recent run**

For runs since January 2026 you can skip the build step. NOAA's references are one JSON file per forecast hour and point at the AWS copy of the files (`s3://noaa-nwm-pds`). This example combines them the same way and reads them over HTTPS:

```python
import json
import fsspec
import pandas as pd
import xarray as xr
from kerchunk.combine import MultiZarrToZarr

comid = 24270288
s3 = fsspec.filesystem("s3", anon=True)        # public bucket: no AWS account needed

# NOAA publishes one reference file per forecast hour; pick yesterday's 12Z short-range run
day = (pd.Timestamp.now(tz="UTC") - pd.Timedelta("1D")).strftime("%Y%m%d")
paths = sorted(s3.glob(f"noaa-nodd-kerchunk-pds/nwm/short_range/"
                       f"nwm.short_range.channel_rt.conus.{day}.t12z.f*.nc.zarr"))

def load_ref(path):
    """Read one NOAA reference file and point it at the same NWM files over HTTPS."""
    text = json.dumps(json.loads(s3.cat(path)))
    return json.loads(text.replace("s3://noaa-nwm-pds/", "https://noaa-nwm-pds.s3.amazonaws.com/"))

refs = MultiZarrToZarr([load_ref(p) for p in paths], remote_protocol="https", concat_dims=["time"],
                       identical_dims=["feature_id", "reference_time", "crs"]).translate()

ds = xr.open_dataset("reference://", engine="zarr", chunks={}, consolidated=False, zarr_format=2,
                     storage_options={"fo": refs, "remote_protocol": "https",
                                      "remote_options": {"asynchronous": True}})
print(len(paths), "reference files;", dict(ds.sizes))
print(ds["streamflow"].sel(feature_id=comid).load().to_series().head())
```

```text
18 reference files; {'time': 18, 'feature_id': 2776734, 'reference_time': 1}
time
2026-10-07 13:00:00    214.079995
2026-10-07 14:00:00    213.229995
...
```

**A note on historical data:** for observed, historical streamflow, use USGS NWIS rather than NWM's own retrospective archive. NWIS is the authoritative source for gauged, historical data and doesn't require the model-file access patterns covered above. The one exception is **ungauged reaches**: NWIS only has data where a physical gauge exists, so if your analysis needs historical streamflow at a reach with no gauge, NWM's retrospective archive (Zarr, on AWS; see Further reading) is the only source for that, since it's a modeled reconstruction covering every reach in the network, not just gauged ones.

## Best practices FAQs

The sections below answer these questions, with code examples. All three answers follow from how NWM files are stored, so we start with [why NWM downloads cost what they cost](#nwm-cost).

* What is the recommended way to download data for **one location across the full period of record**? See [Temporal scaling](#nwm-temporal-scaling).
* What is the recommended way to download data across **all locations for a small time range**? See [Spatial scaling](#nwm-spatial-scaling).
* If I am working on improving efficiency through **code parallelization**, what should I do vs avoid? See [Parallelization](#nwm-parallelization).

(nwm-cost)=
### Why NWM downloads cost what they cost

One fact about the files explains almost every recommendation below. Inside each NWM `channel_rt` file, `streamflow` is stored as **one compressed chunk per forecast hour that contains all 2,776,734 reaches** (about 1.8 MB compressed). There is no way to read "just my reach" from a file: any tool that reads the files has to fetch at least that whole chunk. Services such as the NOAA NWM API and the CIROH BigQuery API are different: they return just the reaches you ask for, and whatever reading of the underlying data that takes happens on their side (CIROH asks BigQuery users to estimate each query's cost before running it). [TODO: verify how the NWM API and BigQuery store NWM data] For the files themselves:

* **Cost grows with the number of forecast hours (files) you touch, not with the number of reaches.**
* `hydrotools` downloads whole files (~13 MB each, every variable). Kerchunk references fetch only the `streamflow` chunk you need (~1.8 MB per hour), so they move fewer bytes, but the bytes are still CONUS-sized.

We measured this for the Skagit gage reach, using three short-range runs before the December 2025 peak (54 hourly files), from a home internet connection (~13 MB/s):

| Route | Reaches | Data transferred | Peak memory | Wall time |
|---|---|---|---|---|
| NOAA NWM API (today's data; all 116 short-range runs it held) | 1 | 0.15 MB | 0.1 GB | < 10 s |
| `hydrotools` (GCP) | 1 | 707 MB (saved to disk) | 1.7 GB | 4–13 min |
| `hydrotools` (GCP) | 2,540 | 707 MB (saved to disk) | 1.7 GB | 4–13 min |
| Kerchunk references + `xarray` | 1 | 96 MB | 0.7 GB | 27 s |
| Kerchunk references + `xarray` | 2,540 | 96 MB | 0.6 GB | 64 s |
| *Building the references (one time), as in the example above* | – | 57 MB, in 54 requests | – | 14 s |

Going from 1 reach to the whole basin above the gage (2,540 reaches) changed neither the data transferred nor the memory. Wall times vary a lot with network conditions; treat them as rough. The reference build was measured on 2026-10-08. An earlier build through `gcsfs` (~100 small requests per file) moved only 2.8 MB but took 7–11 min on a busy connection, and 16 s per run on a quiet one. [POLISH: re-time on a quiet connection and in-cloud; measure build memory]

One **medium-range** member (issued 2025-12-09 00Z: 240 hourly files) scales the same way, about 13× a short-range run:

| Route | Reaches | Data transferred | Peak memory | Wall time |
|---|---|---|---|---|
| `hydrotools` (GCP) | 1 | 3.1 GB needed (did not finish) | – | **timed out** after 15 min (2 of 2 attempts on our connection) |
| Kerchunk references + `xarray` | 1 | 417 MB | 0.8 GB | 100 s |
| *Building the references (one time), as in the example above* | – | 252 MB, in 240 requests | – | 69 s |

Building with `gcsfs` and its default read-ahead on 2026-10-07 moved 1.3 GB and took 6 min for the same member. Reading 1 MB blocks over HTTPS (as above) cut that to about 1 MB per file.

(nwm-temporal-scaling)=
### Temporal scaling

What is the recommended way to download data for one location but a long period?

**Recent forecasts (last few days):** use the NOAA NWM API. One request returns every run it still holds.

**Past forecasts (NWM forecast history):** every reference time is a separate set of files, so cost grows linearly with the number of forecast runs: ~235 MB per short-range run and ~3.1 GB per medium-range member with `hydrotools`, or ~32 MB per short-range run with kerchunk references. Short range is issued every hour, so a month of every short-range run is 720 runs: ~170 GB of downloads with `hydrotools`, or ~23 GB of chunk reads with references. Before you start, ask whether you need *every* run. For "how did the forecast change approaching the peak?", a handful of issue times is usually enough (Module 4 does exactly this).

For more than a handful of runs, use kerchunk references (built once, reused), ideally from a cloud machine in the same region as the bucket (Google Cloud's `US` multi-region for `gs://national-water-model`; AWS `us-east-1` for `s3://noaa-nwm-pds`), so the CONUS-sized chunks never cross your home connection. `NWMFileClient.get()` does accept a list of reference times, but it processes them one at a time, keeps every downloaded file on disk until you delete it, and its intermediate processing used ~1.7 GB of memory in our test (the documentation recommends at least a 4-core processor and 8 GB of RAM).

Availability depends on the source. According to the [hydrotools NWM Client documentation](https://github.com/NOAA-OWP/hydrotools/tree/main/python/nwm_client), Google Cloud holds the largest amount of operational forecast data, which is why `hydrotools` uses it by default. On 2026-10-07 the AWS bucket `noaa-nwm-pds` held every day from 2025-01-01 onward (earlier descriptions call it a rolling four-week archive). [PARTNER REVIEW: NOAA] confirm the retention policy of each mirror. Not every configuration covers the whole archive (the Alaska configurations, for example, only became available after August 2023).

**NWM retrospective.** If you need a long *simulated* record rather than forecasts, use the NWM retrospective simulations: multi-decade model runs, not archived forecasts. Version 3.0 covers February 1979 through January 2023, and version 2.1 covers February 1979 through December 2020. Their output frequency and fields differ from the operational forecast model. Zarr versions are available on AWS for version 2.1, and NCAR describes Zarr stores for version 3.0 (see the [NWM retrospective registry entry](https://registry.opendata.aws/nwm-archive/)). [TODO: verify retrospective date ranges and link the NCAR v3.0 Zarr source]

(nwm-spatial-scaling)=
### Spatial scaling

What is the recommended way to download data for all locations but a small time range?

Start with **discovery** to build your list of COMIDs (e.g. all reaches upstream of a gage, as above), then pass the whole list to the download step in one call rather than looping one COMID at a time. Looping over COMIDs re-reads the same CONUS-wide chunks for every reach.

* **`hydrotools`:** `NWMFileClient.get()` accepts an array of COMIDs. In our test, 2,540 reaches cost the same downloads and memory as 1 reach. If you omit `nwm_feature_ids`, it returns the default set: channel features with a known USGS mapping (8,866 in `hydrotools.nwm_client` 9.2.1).
* **Kerchunk references:** `ds["streamflow"].sel(feature_id=upstream_comids)` (drop any COMIDs that aren't NWM reaches first, e.g. with `numpy.isin`). Again, 2,540 reaches fetched exactly the same 96 MB as one reach.
* **NOAA NWM API:** accepts a comma-separated list of COMIDs, but it is built for a few reaches. For hundreds or thousands, use one of the file-based routes. [TODO: verify any documented limit on IDs per API request]

`hydrotools` results come back as pandas DataFrames that use categorical columns to save memory. The documentation notes that categorical columns can behave unexpectedly in groupby operations, are incompatible with fixed-format HDF files (use `format="table"`), and may cause problems when writing to geospatial formats with geopandas. Casting a categorical column to `str` resolves these issues. Setting `compute=False` returns a dask DataFrame instead of a pandas one.

(nwm-parallelization)=
### Parallelization

* **Parallelize over files (forecast hours / runs), not over reaches.** Reaches share chunks, so splitting COMIDs across workers multiplies the bytes; splitting files across workers doesn't.
* **Kerchunk + dask:** opening references with `chunks={}` gives you dask arrays with one task per chunk, so `.load()` fetches chunks concurrently. Building references makes one request per file (with 1 MB blocks), so a thread pool (as in the example above, 8 threads) helps a lot. We saw intermittent SSL errors from too many simultaneous connections at 16 threads (with `gcsfs`); fewer threads plus a retry fixed it.
* **`hydrotools`:** downloads are already asynchronous. The `FileDownloader` class has `limit` (default 10 concurrent downloads) and `timeout` (default 900 seconds) settings. Files for a single forecast cycle are processed in groups of 20 by default (the `group_size` parameter of `get_files()`); the documentation says this accommodates the xarray, dask, and HDF5 backends, which may struggle to open too many files at once, and that it matters mostly for medium-range forecasts. Running several `NWMFileClient.get()` calls at once mostly multiplies disk use and memory (~1.7 GB each in our test).
* **Run next to the data** when the job is big. Moving compute to a cloud machine in the bucket's region does more for large NWM jobs than any amount of local parallelism.

## Further reading

* NLDI documentation: https://api.water.usgs.gov/docs/nldi
* `pynhd` (HyRiver) documentation: https://docs.hyriver.io/readme/pynhd.html
* NOAA NWM API (experimental) documentation: https://api.water.noaa.gov/nwm/v1/docs
* OWPHydroTools (hydrotools) GitHub repo: https://github.com/NOAA-OWP/hydrotools
* OWPHydroTools NWM Client documentation: https://noaa-owp.github.io/hydrotools/hydrotools.nwm_client.html and package page: https://pypi.org/project/hydrotools.nwm-client/
* NWM operational archive on Google Cloud: https://console.cloud.google.com/marketplace/product/noaa-public/national-water-model
* NWM operational data on AWS (Registry of Open Data): https://registry.opendata.aws/noaa-nwm-pds/
* NOAA Cloud Optimized Zarr Reference Files (Kerchunk), Registry of Open Data: https://registry.opendata.aws/noaa-nodd-kerchunk/
* Kerchunk documentation: https://fsspec.github.io/kerchunk/
* `nwmurl` (CIROH), builds NWM file URLs: https://hub.ciroh.org/docs/products/data-management/dataaccess/NWMURL%20Library and source: https://github.com/CIROH-UA/nwmurl
* Tuhinanshu, T. (2023), *Using Kerchunk to make NOAA's National Water Model dataset more accessible*, Element 84: https://element84.com/software-engineering/using-kerchunk-to-make-noaas-national-water-model-dataset-more-accessible/
* USGS NWIS (recommended source for historical, gauged streamflow): https://waterdata.usgs.gov/nwis
* NWM retrospective archive (Zarr, AWS, for the ungauged-reach case only): https://registry.opendata.aws/nwm-archive/
* CIROH NWM BigQuery API (CIROH members and partners with active CIROH projects; access by request): https://hub.ciroh.org/docs/products/data-management/bigquery-api/
* Example code for `hydrotools` adapted from the [OWPHydroTools NWM Client README](https://github.com/NOAA-OWP/hydrotools/tree/main/python/nwm_client) (NOAA-OWP). [TODO: verify license/attribution wording for adapted hydrotools examples]
