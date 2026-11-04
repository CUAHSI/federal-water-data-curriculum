# Meet NOAA NWM

The *NOAA National Water Model ({term}`NWM`)* is produced by NOAA's [Office of Water Prediction](https://water.noaa.gov/about/nwm) (OWP), part of the National Weather Service (NWS). The NWM is a continental-scale hydrologic model, not an observational network — it simulates and forecasts streamflow (along with soil moisture, snowpack, and other water-budget variables) for over 3.4 million miles of rivers and streams across the U.S. and its territories by combining weather forecasts, land surface physics, and channel routing. 

NWM output is supplemental guidance. Official river forecasts are provided at approximately 4,000 locations by the NWS River Forecast Centers. The NWM provides model guidance that complements official NWS river forecasts across the contiguous U.S. ({term}`CONUS`), giving forecasters, emergency managers, and floodplain managers guidance in places that lack official forecast points ([About the NWM](https://water.noaa.gov/about/nwm)).

Learn more at the [NWM landing page](https://water.noaa.gov/about/nwm), [National Water Prediction Service](https://water.noaa.gov/) viewer, the NWS story map [Using the National Water Model Within NWPS](https://storymaps.arcgis.com/stories/c4964f08ffcf4d9286bd1fd545ddfbab), and [CIROH's NWM overview](https://hub.ciroh.org/docs/products/national-water-model/).

## Terminology

This table maps NWM's own vocabulary onto the course's [shared concepts](00_introduction.md#m02-shared-concepts):

| Shared concept | NWM equivalent | Notes |
|---|---|---|
| {term}`Location identifier` | `feature_id` (= {term}`COMID`) | For streamflow in the CONUS domain, each stream reach in the model has a unique {term}`feature_id`, which corresponds to a COMID in the {term}`NHDPlus` stream network (see below). Outside CONUS, the NWM uses arbitrary reach identifiers. The NOAA NWM API and `hydrotools` call it `nwm_feature_id`. |
| {term}`Variable` | streamflow | Channel discharge at a reach. NWM also outputs many other variables (soil moisture, snowpack, evapotranspiration, reservoir levels) that aren't the focus of this course. |
| {term}`Variable unit` | m³/s | Cubic meters per second, consistent across all NWM configurations. The NOAA NWM API labels it `CMS`. |
| {term}`Time` | {term}`reference time <Forecast reference time>` + {term}`valid time <Valid time>` | Every forecast value has two times (UTC): the model initialization time (reference time) and the time it predicts (valid time). The same valid time appears in many forecasts issued at different reference times. |
| {term}`Data quality flag(s)` | none per value | NWM has no per-observation QA/QC flag the way a sensor network does. Instead, quality is a function of which model version and configuration produced the value, see below. |
| {term}`Version / provenance` | model version and {term}`configuration <Configuration>` | For example v3.1, `medium_range`, reference time 2026-10-08 18:00 UTC. Values for the same reach and valid time differ between versions and between configurations. |
| {term}`Data unit` | one output file per timestep | Each configuration's run writes one NetCDF file per valid time (for streamflow, a `channel_rt` file), holding every reach in the domain. |

Two network terms come up constantly with the NWM's streamflow output. They identify reaches in the river network, so they apply to streamflow (and other values reported per reach). Other variables are reported on different units: soil moisture and snowpack, for example, are reported on a structured grid (see Spatial coverage).

- **{term}`NHDPlus`** is short for "National Hydrography Dataset Plus." A USGS-maintained geospatial dataset that breaks the entire U.S. stream and river network into individual reaches, each with its own COMID, plus catchment boundaries and upstream/downstream connectivity. NWM doesn't define its own river network, it runs on top of NHDPlus, which is also why tools like {term}`NLDI` can look up COMIDs by location.
- **{term}`COMID`** is short for "Common Identifier." A unique numeric ID assigned to each individual stream segment (reach) in the NHDPlus stream network. In the CONUS domain, NWM's `feature_id` values generally correspond directly to NHDPlusV2 COMIDs, though some variation may exist, so the two terms are often used interchangeably across NWM documentation and tools.

## Dataset derivation

**Key point: NWM values are model output, and a new model version can change the estimates for the same reach and time.**

NWM output is entirely modeled, not measured directly. It couples a land-surface model (calculating snowmelt, infiltration, and runoff on a grid) with channel and reservoir routing along the NHDPlus stream network, driven by weather inputs called {term}`forcing <Forcing>`. The analysis configuration then uses {term}`data assimilation <Data assimilation>` of real-time observations (including USGS gage data) to correct the simulation.

It has gone through several major versions since becoming operational in August 2016: v1.0, v1.2 (2018, with expanded calibration to ~1,000+ basins), v2.0, v2.1, v3.0, and v3.1. Each version can meaningfully change streamflow values at the same `feature_id`. A Texas-focused comparison of v2.1 and v3.0 across 610 USGS gages ([Journal of Hydrology: Regional Studies, 2025](https://doi.org/10.1016/j.ejrh.2025.102196)) found real gains in v3.0 overall, but during storm events specifically, both versions still struggle to capture peak flow magnitude and timing accurately. Always check the OWP version documentation or release notes before combining data across versions, and record the version you used (Module 1, [Publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data)). The NWM version is found in the NetCDF files by accessing the "NWM_version_number" attribute (i.e. `ds.attrs['NWM_version_number']` in `xarray`).

:::{dropdown} What changed in v3.0
- First-time Total Water Level guidance for coastal CONUS, Hawaii, and Puerto Rico/USVI (via a coupled ocean model, SCHISM).
- Domain expansion into south-central Alaska.
- The addition of the National Blend of Models as a forcing source for medium-range CONUS and Alaska forecasts.
- Use of Multi-Radar Multi-Sensor precipitation for Puerto Rico/USVI.
- Expanded ingestion of reservoir outflow forecasts (77 additional sites, bringing the total to 392).
- Calibration/parameter improvements.
:::

:::{dropdown} What changed in v3.1
Changes from v3.0, which was operational until about 18 August 2026:

- Use of Multi-Radar/Multi-Sensor (MRMS) and numerical weather prediction (NWP) precipitation-type information in CONUS Analysis & Assimilation, Short-Range and GFS-based Medium-Range configurations.
- Improved downscaling of temperature forcing data, using a dynamic lapse-rate approach based on NWP model data.
- Representation of the flow diversion between the Mississippi and Atchafalaya Rivers at the Old River Control Structure, using observation-based flow persistence.
- Assimilation of USGS streamflow observations available at forecast time into the first hours of the short-, medium- and long-range forecasts.
- Updated CONUS hydrofabric with location refinements for 311 USGS stream gages.
- Shorter Medium-Range coastal forecasts for the Atlantic-Gulf and Pacific domains (5 days, down from 10).
- Puerto Rico/USVI: National Blend of Models (NBM) precipitation replaces WRF-ARW as supplemental forcing in Short-Range configurations, and new 00Z and 12Z Short-Range cycles.
As announced in [NWS Service Change Notice 26-64](https://www.weather.gov/media/notification/pdf_2026/scn26-64_Updated_National_Water_Model_V3.1_aaa.pdf).
:::

## Spatial coverage

- **Extent:** In the current version (v3.1): CONUS + hydrologically-contributing areas, plus separate domains for Hawaii, Puerto Rico/USVI, and southern Alaska (Cook Inlet, Copper River Basin, Prince William Sound). The extent depends on the model version: for example, only the v3.0 retrospective simulation and v3.0+ operational NWM cover the Alaska, Hawaii and Puerto Rico/USVI domains ([AWS Registry of Open Data](https://registry.opendata.aws/nwm-archive/)).
- **Type:** Point/vector network output for streamflow and reservoirs (one value per `feature_id`, about 2.8 million reaches); paired with 1 km gridded NetCDF for land-surface variables and 100–250 m gridded NetCDF for ponded water depth and soil saturation
- **Resolution:** Reach-based routing follows NHDPlus (medium-resolution, 1:100,000-scale network); grids are 1 square km (land surface) and 250 square m (near-surface hydrology)
- **{term}`CRS`:** Streamflow outputs do not include coordinate information in the format the NWM reports them: each value is tied to a `feature_id`, and you get its location by joining the `feature_id` to the NHDPlus reach with the same COMID. The underlying NHDPlus network uses the USA Contiguous Albers Equal Area projection (datum NAD83), as noted in the [USGS user guide for NHDPlus](https://pubs.usgs.gov/publication/sir20255031/full). The NWM gridded land-surface output uses its own Lambert Conformal Conic grid definition, documented in the NWM configuration files. Note that Module 3 tools take and return EPSG:4326.

## Temporal coverage

- **Period of record:** The NWM offers different types of simulation, and each covers a different period. Operational forecasts have run since August 2016. A {term}`retrospective simulation <Retrospective simulation>` is a single, continuous model run over multiple decades that lets you examine past hydrologic events. "Retrospective" here means a run over the full historical period using historical weather data as input rather than real-time observations or forecasts. It's not a collection of old forecasts: it is the model's best available reconstruction of what streamflow likely was at every `feature_id`, given current modeling knowledge and datasets, including reaches with no gage. The v3.0 retrospective on AWS covers February 1979 – January 2023 ([AWS Registry of Open Data](https://registry.opendata.aws/nwm-archive/)). This makes it the main source of long-term, reach-level historical streamflow for ungauged locations.
- **Frequency/resolution:** Varies by configuration. Analysis & Assimilation and Short-Range are hourly, and the Retrospective dataset is hourly throughout. Medium-Range consists of two configurations: a 10-day Deterministic configuration (member 1, a single run) and an 8.5-day {term}`ensemble <Ensemble member>` of six members. Member 1 belongs to both: the ensemble uses its first 8.5 days alongside members 2–6, which stop there. Output is hourly for all six members, in the NOAA NWM API (checked 2026-10-08) and in the archive files. Long-Range output is 6-hourly.
- **Update cadence:** Short-Range forecasts cycle hourly over CONUS; Medium- and Long-Range forecasts are produced four times a day; forecast latency is roughly 1–2 hours after cycle time (mostly driven by the lag in incoming weather-forcing data)

**Which configuration do I want?** It depends on what you mean by "history":

- To see how well we can digitally reproduce a past event, such as a flood from 15 years ago, or to get a long record at an ungaged reach, use the retrospective simulation. It shows what current modeling knowledge and tools can reproduce, not what was forecast at the time.
- To assess the NWM's forecasting skill for a past flood, use the archived forecasts from the forecast configurations (for floods since forecasts began to be archived). These are also historical data, but they show what the model actually predicted at the time.
- For what the model predicts now, use a current forecast configuration.

Each configuration also has its own model inputs. For example, the retrospective simulation is driven by the AORC (Analysis of Record for Calibration) weather dataset, while short-range forecasts use operational weather forecast products such as HRRR and RAP. See the QPF forcings section of [Using the National Water Model Within NWPS](https://storymaps.arcgis.com/stories/c4964f08ffcf4d9286bd1fd545ddfbab). In CONUS:

| Configuration | What it's for | Horizon | Output interval | Initialized |
|---|---|---|---|---|
| Retrospective | Long historical record, ungaged reaches | Feb 1979 – Jan 2023 (v3.0) | hourly | one-off run per model version |
| Analysis & Assimilation (`analysis_assim`) | Best estimate of current conditions | the last 3 hours (look-back) | hourly | hourly |
| Short-Range (`short_range`) | Next-day forecasts | 18 hours | hourly | hourly |
| Medium-Range Deterministic (`medium_range`) | Single-valued forecasts for the coming week | 10 days (member 1) | hourly, in the NOAA NWM API and in the archive files | four times a day |
| Medium-Range Ensemble (`medium_range`) | Ensemble forecasts for the coming week; six ensemble members | 8.5 days (all six members; member 1 continues to 10 days as the Deterministic forecast) | hourly, in the NOAA NWM API and in the archive files | four times a day |
| Long-Range (`long_range`) | Monthly outlooks; four ensemble members | 30 days | 6-hourly | four times a day |

There are four operational Medium-Range products for CONUS:

- 10-day deterministic (GFS), `medium_range_mem1`.
- 10-day deterministic (NBM), `medium_range_blend`.
- Ensemble (GFS): the first 8.5 days of `medium_range_mem1` plus `medium_range_mem2` through `medium_range_mem6`.
- 10-day deterministic (GFS, no data assimilation), `medium_range_no_da`, initialized by `analysis_assim_no_da`.


## Data content

- **Primary variable:** streamflow (m³/s) at each `feature_id`
- **Related variables available in the same output:** velocity, reservoir inflow/outflow/elevation, ponded water depth, depth to soil saturation, soil moisture, snowpack, evapotranspiration
- **Known limitations:** No formal per-value QA/QC flag exists; quality is instead governed by model version and configuration, and by how well any given basin was calibrated. Documented issues (e.g., both v2.1 and v3.0 struggle to capture storm peak magnitude and timing in the Texas comparison above) should be treated as caveats on the whole time series, not flags on individual values. As with any model, output quality also degrades in ungaged, heavily-regulated, or poorly-calibrated basins.

**What the data look like.** The figure puts the configurations in the table above on a single timeline, using one set of runs that share a reference time, for the NHDPlus reach of the Ohio River at Louisville, Kentucky (COMID `10164004`), during the April 2025 flood. The strip along the top shows how far each configuration reaches from the reference time (the dotted line). The hydrograph below shows the streamflow each one gave. Members 1–6 of the Medium-Range forecast start from the same conditions and spread apart as {term}`lead time <Lead time>` grows, and the Deterministic forecast (member 1) runs a day and a half longer than the others. Medium-range forecasts are issued four times a day, so six hours later a new forecast replaces this one; a forecast is identified by both its reach and its reference time.

**Imagine it's 3 April 2025.** This figure was built later from NOAA's forecast archive, because the API keeps only the latest few days of forecasts, but you can read it as if you were standing at the dotted line. That reference time, 00:00 UTC, was the evening of 2 April in Louisville, and the flood's crest was still days away.

Analysis & Assimilation works differently from the forecasts: it doesn't predict. Each hourly run goes back over the last 3 hours and adjusts them using observations, so the run ending at the dotted line gave only the three black dots (22:00, 23:00 and 00:00 UTC), enlarged in the zoom. The gray dots are the newest value from each earlier hourly run, joined into a longer record. Consecutive runs overlap by 2 hours, so taking one value from each avoids repeating an hour. Black and gray dots alike are model output, not gage readings.

To the right of the line is what each forecast predicted from that moment. The Retrospective panel is a separate simulation that ended in January 2023, shown for its place in time and not as part of this forecast.

:::{figure} ../images/m02/02_meet_noaa_nwm-ohio-configurations.png
:alt: Figure with a horizon strip above a hydrograph for COMID 10164004, with a dotted line at the reference time, 3 April 2025 00:00 UTC. The strip shows Analysis and Assimilation reaching 3 hours back, Short-Range 18 hours ahead, the Medium-Range Ensemble 8.5 days, Medium-Range Deterministic 10 days and Long-Range 30 days. A separate panel on the left, after an axis break, shows the last month of the Retrospective in violet, January 2023, between about 3,500 and 6,500 cubic meters per second. In the hydrograph, gray dots rise to about 5,000 before the reference time and three black dots sit at about 4,750 at the reference time. A zoomed panel shows those three hourly values, with a band marking the look-back, and the 18 hourly Short-Range values, which fall to about 3,240. Six blue Medium-Range lines then rise to peaks between about 12,400 and 15,100 around 8 and 9 April. Members 2 to 6 stop on 11 April and member 1 continues to 13 April. Four dashed green Long-Range lines fall to about 3,000, peak near 6,000 around 9 and 10 April, and stay above about 3,400 until 3 May.
:width: 100%

Runs from NWM v3.0 for COMID `10164004`, Ohio River at Louisville, KY. The dotted line is the forecasts' reference time (model initialization time), 2025-04-03 00:00 UTC. Notice how the horizons differ: 3 hours back for Analysis & Assimilation, then 18 hours, 8.5 days, 10 days and 30 days ahead. On the main plot the three black dots overlap, so use the zoom to see them. The gray band in the zoom marks the look-back: the run ending at the dotted line starts at 21:00 UTC and writes its first value at 22:00. Its files store that 21:00 start as `reference_time`, 3 hours before the `t00z` in their names. The axis break skips more than two years. Data: NOAA NWM operational archive on Google Cloud (`analysis_assim`, `short_range`, `medium_range_mem1` to `mem6`, `long_range_mem1` to `mem4`) and the NWM v3.0 retrospective Zarr store on AWS, accessed 2026-11-04.
:::

This is model output, not an observation, and it is not checked against the gage here; Module 4 shows how to compare forecasts with observations. Use this figure to compare what each configuration covers, not how well it did. The differences between the forecasts come from this one set of runs, so don't read them as a test of any configuration.

:::{admonition} Partner review (NOAA): look-back and ensemble members
:class: important
Please check two points for these NWM v3.0 runs:

1. We describe each Analysis & Assimilation run as going back over the last 3 hours. The `t00z` files store `reference_time` 21:00 UTC, while the NOAA NWM API reports the cycle time. Is that description right?
2. We say that Medium-Range members start from the same conditions, and the glossary says members have slightly different inputs. Is the difference between them in the forcing, not the initial state?
:::

Past forecasts, including those issued during the April 2025 flood, are kept in NOAA's public forecast archive on [Google Cloud](https://console.cloud.google.com/marketplace/product/noaa-public/national-water-model), which is free to use without an account and which `hydrotools` reads by default (it is also mirrored on AWS). Module 3 shows how to retrieve short- and medium-range forecasts from it.

The COMID `10164004` was found by asking the {term}`NLDI` which NHDPlus reach the Louisville USGS gage sits on; Module 3 shows how.

:::{dropdown} How this figure was made
*You don't need to run this now.* It's here so you can see exactly how the figure was made and reproduce it later. It runs in the course's `m03-nwm` environment (`environments/m03-nwm.yml`), needs no account or key, and has two steps. Module 3 explains this approach for short- and medium-range forecasts; this dropdown is the course's example for `analysis_assim` and `long_range`.

The first step reads Louisville's streamflow from about 2,000 archive files, because the archive holds one file for the whole country at each time. The code uses the same references approach as Module 3, so it reads only the pieces it needs rather than whole files. It then adds the last month of the Retrospective and saves everything to one CSV file. Expect this step to take about 12 minutes.

In the Analysis & Assimilation file names, `tmNN` means NN hours before the hour in the file name (`t00z` here), so `tm02`, `tm01` and `tm00` are the three black dots, and `tm00` from each earlier run gives the gray dots.

```python
import time
import aiohttp
import fsspec
import pandas as pd
import s3fs
import xarray as xr
from concurrent.futures import ThreadPoolExecutor
from kerchunk.combine import MultiZarrToZarr
from kerchunk.hdf import SingleHdf5ToZarr

# Record the query in one place
COMID = 10164004                              # NHDPlus reach (NWM feature_id), Ohio River at Louisville, KY
REF = pd.Timestamp("2025-04-03 00:00")        # reference time of the forecast cycle (UTC)
ARCHIVE = "https://storage.googleapis.com/national-water-model"

def nwm_url(cycle, folder, product, lead, member=""):
    """Build the archive address of one streamflow file."""
    return f"{ARCHIVE}/nwm.{cycle:%Y%m%d}/{folder}/nwm.t{cycle:%H}z.{product}.channel_rt{member}.{lead}.conus.nc"

def with_retries(read, tries=4):
    """Try again after a network error, because a full set of runs needs thousands of requests."""
    for attempt in range(tries):
        try:
            return read()
        except (OSError, aiohttp.ClientError):
            if attempt == tries - 1:
                raise
            time.sleep(2 * (attempt + 1))

def index_one(url):
    """Scan one file's layout. Module 3 explains the block_size and inline_threshold settings."""
    def scan():
        with fsspec.open(url, "rb", block_size=2**20) as f:
            return SingleHdf5ToZarr(f, url, inline_threshold=500).translate()
    return with_retries(scan)

def read_reach(urls):
    """Read one reach from many files without downloading the whole files."""
    with ThreadPoolExecutor(16) as pool:
        singles = list(pool.map(index_one, urls))
    def combine():
        # stack the files along time; the listed variables are the same in every file
        return MultiZarrToZarr(singles, remote_protocol="https", concat_dims=["time"],
                               identical_dims=["feature_id", "reference_time", "crs"]).translate()
    with ThreadPoolExecutor(1) as pool:   # own thread, so this also works inside Jupyter
        refs = pool.submit(combine).result()
    # open lazily through the references: nothing downloads until .load() below
    ds = xr.open_dataset("reference://", engine="zarr", chunks={}, consolidated=False, zarr_format=2,
                         storage_options={"fo": refs, "remote_protocol": "https",
                                          "remote_options": {"asynchronous": True}})
    return with_retries(lambda: ds["streamflow"].sel(feature_id=COMID).load().to_series())

def tidy(series, config, member=0):
    """One row per value: configuration, member (0 if none), valid time, streamflow."""
    return pd.DataFrame({"config": config, "member": member, "time": series.index, "q": series.values})

tables = []

# Analysis & Assimilation: the newest value (tm00) of each hourly run for 9 days, joined by valid time
cycles = pd.date_range(REF - pd.Timedelta(days=9), REF, freq="h")
tables.append(tidy(read_reach([nwm_url(c, "analysis_assim", "analysis_assim", "tm00") for c in cycles]), "ana_joined"))

# Analysis & Assimilation: all 3 values of the one run at the reference time
tables.append(tidy(read_reach([nwm_url(REF, "analysis_assim", "analysis_assim", f"tm{k:02d}") for k in (2, 1, 0)]), "ana_run"))

# Short-Range: 18 hourly values
tables.append(tidy(read_reach([nwm_url(REF, "short_range", "short_range", f"f{h:03d}") for h in range(1, 19)]), "short"))

# Medium-Range: member 1 has 240 hourly values, members 2-6 have 204
for m in range(1, 7):
    urls = [nwm_url(REF, f"medium_range_mem{m}", "medium_range", f"f{h:03d}", f"_{m}")
            for h in range(1, (240 if m == 1 else 204) + 1)]
    tables.append(tidy(read_reach(urls), "medium", m))

# Long-Range: 4 members, 120 values 6 hours apart
for m in range(1, 5):
    urls = [nwm_url(REF, f"long_range_mem{m}", "long_range", f"f{h:03d}", f"_{m}") for h in range(6, 721, 6)]
    tables.append(tidy(read_reach(urls), "long", m))

# Retrospective v3.0: its last month, from the public Zarr store on AWS
fs = s3fs.S3FileSystem(anon=True)
retro = xr.open_zarr(s3fs.S3Map("noaa-nwm-retrospective-3-0-pds/CONUS/zarr/chrtout.zarr", s3=fs), consolidated=True)
retro_q = retro["streamflow"].sel(feature_id=COMID).sel(time=slice("2023-01-01", None)).load().to_series()
tables.append(tidy(retro_q, "retrospective"))

# Save, so the plot can be redrawn without reading the archive again
q = pd.concat(tables, ignore_index=True)
q.to_csv("nwm_configurations_louisville.csv", index=False)
print(q.groupby(["config", "member"])["q"].agg(["size", "max"]).round())
```

```text
                      size      max
config        member               
ana_joined    0        217   4994.0
ana_run       0          3   4783.0
long          1        120   5947.0
              2        120   6192.0
              3        120   5761.0
              4        120   6168.0
medium        1        240  13902.0
              2        204  14418.0
              3        204  12402.0
              4        204  12791.0
              5        204  14195.0
              6        204  15091.0
retrospective 0        745   6477.0
short         0         18   4742.0
```

`q` is a table with one row per value. Its columns are `config` (which configuration), `member` (0 for configurations without members), `time` (valid time, UTC) and `q` (streamflow, m³/s). The printed summary shows the number of values and the highest flow for each. Member 1 has 240 hourly values and members 2–6 have 204 each, which is why member 1 runs longer in the figure. The `ana_joined` rows have 217 values because they cover 9 days of hourly runs, one value from each, while `ana_run` has the 3 values of a single run.

The second step reads the saved table and draws the figure, so you can change the plot without reading the archive again.

```python
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import ConnectionPatch

q = pd.read_csv("nwm_configurations_louisville.csv", parse_dates=["time"])
REF = pd.Timestamp("2025-04-03 00:00")
hrs = lambda h: REF + pd.Timedelta(hours=h)
pick = lambda config: q[q["config"] == config]
ana_joined, ana_run, short, medium, long_range, retro = map(pick, ["ana_joined", "ana_run", "short", "medium", "long", "retrospective"])
member_1 = medium[medium["member"] == 1]
INK, MUTED, GRID, GRAY = "#0b0b0b", "#52514e", "#e4e3df", "#8a8986"
ORANGE, BLUE, GREEN, VIOLET = "#eb6834", "#2a78d6", "#1baf7a", "#6250d6"
txt = dict(color=INK, fontsize=8.5)
lead = dict(arrowstyle="-", color=MUTED, lw=0.7)
plt.rcParams.update({"font.size": 9.5, "axes.edgecolor": GRAY, "xtick.color": MUTED, "ytick.color": MUTED})

# Two columns (Retrospective, then the forecast cycle) and two rows (horizon strip above, hydrograph below)
fig, ((strip_l, strip_r), (hyd_l, hyd_r)) = plt.subplots(
    2, 2, figsize=(10.5, 6.3), sharex="col", sharey="row",
    gridspec_kw={"width_ratios": [1, 5.2], "height_ratios": [1.15, 3], "wspace": 0.05, "hspace": 0.04})
fig.subplots_adjust(left=0.075, right=0.985, top=0.92, bottom=0.11)

# Hydrograph: gray dots are the joined record, black dots are the one run at the reference time
hyd_l.plot(retro["time"], retro["q"], color=VIOLET, lw=1.8)
hyd_r.plot(ana_joined["time"], ana_joined["q"], ls="none", marker="o", ms=2.2, mew=0, color=GRAY, zorder=3)
hyd_r.plot(ana_run["time"], ana_run["q"], ls="none", marker="o", ms=5, color=INK, zorder=6)
for member, run in medium[medium["member"] > 1].groupby("member"):
    hyd_r.plot(run["time"], run["q"], color=BLUE, lw=0.9, alpha=0.75)

hyd_r.plot(member_1["time"], member_1["q"], color=BLUE, lw=2)
for member, run in long_range.groupby("member"):
    hyd_r.plot(run["time"], run["q"], color=GREEN, lw=1.1, ls=(0, (4, 1.5)))

hyd_r.plot(short["time"], short["q"], color=ORANGE, lw=3, solid_capstyle="round", zorder=5)

# Axes: the reference time is a dotted line through the strip and the hydrograph
for ax in (strip_r, hyd_r):
    ax.axvline(REF, color=INK, lw=1, ls=":")

hyd_r.set_xlim(hrs(-9 * 24), hrs(30.5 * 24))
hyd_l.set_xlim(retro["time"].min(), pd.Timestamp("2023-02-02"))
hyd_l.set_ylim(0, 16500)
hyd_l.set_ylabel("Streamflow (m³/s)", color=INK)
hyd_l.yaxis.set_major_formatter(lambda v, _: f"{v:,.0f}")
day_month = lambda v, _: f"{mdates.num2date(v).day} {mdates.num2date(v):%b}"
hyd_r.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.TH))
hyd_r.xaxis.set_major_formatter(day_month)
hyd_l.set_xticks(pd.to_datetime(["2023-01-01", "2023-01-15"]))
hyd_l.xaxis.set_major_formatter(day_month)
hyd_l.set_xlabel("Valid time, 2023 (UTC)", color=INK)
hyd_r.set_xlabel("Valid time, 2025 (UTC)", color=INK)
for ax in (hyd_l, hyd_r):
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

hyd_r.spines["left"].set_visible(False)
hyd_r.tick_params(axis="y", length=0)

# Marks showing that years are skipped between the two panels
cut = dict(marker=[(-1, -1.6), (1, 1.6)], markersize=9, linestyle="none", color=MUTED, clip_on=False, mew=1)
hyd_l.plot([1], [0], transform=hyd_l.transAxes, **cut)
hyd_r.plot([0], [0], transform=hyd_r.transAxes, **cut)

# Labels on the lines
left_edge = pd.Timestamp("2025-03-25 00:30")
hyd_l.text(pd.Timestamp("2023-01-16"), 7200, "Retrospective", ha="center", **txt)
hyd_r.annotate("Short-Range", (short["time"].iloc[-1], short["q"].iloc[-1]),
               xytext=(pd.Timestamp("2025-04-06 12:00"), 1500), ha="center", arrowprops=lead, **txt)
hyd_r.annotate("Medium-Range members 2–6 (thin)\nstop at 8.5 days", (hrs(204), 11150),
               xytext=(pd.Timestamp("2025-04-14"), 14300), arrowprops=lead, **txt)
hyd_r.annotate("Medium-Range member 1 (thick)\ncontinues to 10 days", (hrs(240), member_1["q"].iloc[-1]),
               xytext=(pd.Timestamp("2025-04-15"), 10000), va="center", arrowprops=lead, **txt)
hyd_r.text(pd.Timestamp("2025-04-24"), 6500, "Long-Range (dashed, 4 members)", ha="center", **txt)
hyd_r.annotate("Black: A&A as of 3 Apr 00:00", (hrs(-3), 4800), xytext=(left_edge, 5600),
               va="center", arrowprops=lead, **txt)
hyd_r.text(left_edge, 850, "Gray: earlier A&A runs\njoined into a longer record", va="center", **txt)

# Horizon strip: how far each configuration reaches from the reference time
rows = [("Analysis & Assimilation · 3-hour look-back (black dots; see zoom)", -3, 0, INK, 1),
        ("Short-Range · 18 hours", 0, 18, ORANGE, 1),
        ("Medium-Range Ensemble · 8.5 days, 6 members (includes member 1)", 0, 204, BLUE, 0.55),
        ("Medium-Range Deterministic · 10 days (member 1)", 0, 240, BLUE, 1),
        ("Long-Range · 30 days, 4 members", 0, 720, GREEN, 1)]
for row, (label, start, end, color, alpha) in enumerate(rows):
    y = len(rows) - row
    strip_r.barh(y, hrs(end) - hrs(start), left=hrs(start), height=0.62, color=color, alpha=alpha)
    inside = end == 720   # the Long-Range bar fills the panel, so its label goes inside
    strip_r.text(hrs(8) if inside else hrs(end + 10), y, label, va="center", **txt)

strip_l.barh(1, pd.Timestamp("2023-02-01") - retro["time"].min(), left=retro["time"].min(), height=0.62, color=VIOLET)
strip_l.text(retro["time"].min(), 3.2, "Retrospective\nFeb 1979 – Jan 2023\n(last month shown)", va="center", **txt)
strip_r.text(hrs(6), 5.95, "Reference time: 3 Apr 2025 00:00 UTC", va="center", **txt)
strip_l.set_ylim(0.4, 6.4)
strip_r.patch.set_alpha(0)
strip_l.set_yticks([])
for ax in (strip_l, strip_r):
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.tick_params(axis="both", length=0, labelleft=False, labelbottom=False)

# Zoom: the only scale where 3 hours and 18 hours can be seen
zoom = hyd_r.inset_axes([0.012, 0.42, 0.195, 0.50])
zoom.axvspan(hrs(-3), hrs(0), color=INK, alpha=0.08, lw=0)
zoom.axvline(REF, color=INK, lw=1, ls=":")
zoom.plot(ana_run["time"], ana_run["q"], color=INK, lw=2, marker="o", ms=4.5, zorder=4)
zoom.plot(short["time"], short["q"], color=ORANGE, lw=2, marker="o", ms=2.8, zorder=3)
zoom.set_xlim(hrs(-4), hrs(19))
zoom.set_ylim(2900, 5600)
zoom.set_xticks([hrs(h) for h in (-3, 0, 6, 12, 18)], ["−3 h", "0", "+6 h", "+12 h", "+18 h"], fontsize=7.5)
zoom.set_yticks([3000, 4000, 5000], ["3,000", "4,000", "5,000"], fontsize=7.5)
zoom.tick_params(length=2, pad=1.5)
zoom.set_title("Zoom (m³/s), −3 to +18 h", fontsize=8.5, color=INK, loc="left", pad=3)
zoom.annotate("Analysis &\nAssimilation:\n3 hourly values", (hrs(-1), 4770), xytext=(hrs(2), 5170),
              va="center", arrowprops=lead, color=INK, fontsize=7.8)
zoom.text(hrs(-1.5), 4050, "look-back", rotation=90, ha="center", va="center", color=INK, fontsize=7.5)
zoom.text(hrs(0.6), 3250, "Short-Range:\n18 hourly values", color=INK, fontsize=7.8, va="center")
fig.add_artist(ConnectionPatch(xyA=(1, 0), coordsA=zoom.transAxes, xyB=(mdates.date2num(REF), ana_run["q"].iloc[-1]),
                               coordsB=hyd_r.transData, color=MUTED, lw=0.7))

fig.suptitle("NWM configurations on one timeline, Ohio River at Louisville, KY (COMID 10164004)",
             x=0.075, ha="left", fontsize=11.5, color=INK, y=0.955)
fig.savefig("02_meet_noaa_nwm-ohio-configurations.png", dpi=150)
```

The result is the figure above, saved as a PNG file in your working folder. All of its numbers come from the CSV file, so it will match the figure above. The Long-Range values are 6 hours apart, and every other forecast value is 1 hour apart.
:::

## Usage and support

- **Citation:** NOAA publishes a standard format on each dataset's AWS Registry of Open Data listing, e.g. for the Short-Range Forecast: *"NOAA National Water Model Short-Range Forecast was accessed on [DATE] from https://registry.opendata.aws/noaa-nwm-pds."* Swap in the specific product name, version, and dataset URL you actually used (e.g. the [Retrospective archive](https://registry.opendata.aws/nwm-archive/) instead of the Short-Range Forecast).
- **License/access:** NWM output is open data, distributed through the NOAA Open Data Dissemination ({term}`NODD`) program via AWS and Google Cloud, as well as a rolling window of about 48 hours on NOAA's {term}`NOMADS` server.
- **Which access route should I use?** It depends on what you need:
  - **Current forecasts:** the NOAA NWM API, which keeps only the last few days.
  - **Past forecasts:** NOAA's public cloud archive on [Google Cloud](https://console.cloud.google.com/marketplace/product/noaa-public/national-water-model) (also on [AWS](https://registry.opendata.aws/noaa-nwm-pds/)), stored as NetCDF files, one per forecast hour. {term}`hydrotools` downloads whole files. {term}`kerchunk`/{term}`virtual Zarr <Virtual Zarr>` references are small index files that tell tools where each variable's chunks sit inside those NetCDF files, so they read only the chunks they need, which helps with many reaches or many forecasts.
  - **Long historical simulations (retrospective):** NOAA's public archive in NetCDF or Zarr format ([AWS Registry of Open Data](https://registry.opendata.aws/nwm-archive/)).

  They differ a lot in cost as your question grows. The Module 3 lesson [Retrieve NOAA NWM data](../03-federal-water-data-access-retrieval/02_access_noaa_nwm.md#nwm-access-routes) compares them.
- **Change over time:** Values can shift not just with new observations (in Analysis & Assimilation) but with model version upgrades — treat any long time series spanning a version change as non-homogeneous. Forecasts also *expire* from some services: the NOAA NWM API and NOMADS keep only the last few days. If your work depends on a specific forecast, record its configuration, reference time and model version, and keep a copy of the values you used; Module 1's [Publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data) discusses exactly this case.
- **Contact:** For questions about data content, quality, or model methodology, contact NOAA's Office of Water Prediction (contacts listed on the [NWM about page](https://water.noaa.gov/about/nwm)). For questions specifically about data delivery via NODD (AWS/Google Cloud access), email nodd@noaa.gov.

## Further reading

- [About the National Water Model (NOAA OWP)](https://water.noaa.gov/about/nwm)
- [National Water Prediction Service viewer](https://water.noaa.gov/)
- [NOAA NWM API documentation (experimental)](https://api.water.noaa.gov/nwm/v1/docs)
- [NWM Short-Range Forecast — Registry of Open Data on AWS](https://registry.opendata.aws/noaa-nwm-pds/)
- [NWM CONUS Retrospective Dataset — Registry of Open Data on AWS](https://registry.opendata.aws/nwm-archive/)
- [CIROH Hub: What is the National Water Model?](https://hub.ciroh.org/docs/products/national-water-model/) — plain-language overview, good for a first orientation
- [CIROH Hydrofabric documentation](https://hub.ciroh.org/docs/products/Hydrofabric/) — background on the reach/catchment network NWM routes over
- [CIROH RIVR App](https://hub.ciroh.org/docs/products/mobile-apps/RIVR/#background-of-the-us-nwm-streamflow-forecasts) - tool for real-time and forecast riverflow information
- Comparison of NWM v2.1 and v3.0 in Texas: [Journal of Hydrology: Regional Studies (2025)](https://doi.org/10.1016/j.ejrh.2025.102196)
- [USGS user guide for the National Hydrography Dataset](https://pubs.usgs.gov/publication/sir20255031/full)
- [Using the National Water Model Within NWPS](https://storymaps.arcgis.com/stories/c4964f08ffcf4d9286bd1fd545ddfbab) (NWS story map, updated September 2024)
- [NWM operational archive on Google Cloud](https://console.cloud.google.com/marketplace/product/noaa-public/national-water-model)
