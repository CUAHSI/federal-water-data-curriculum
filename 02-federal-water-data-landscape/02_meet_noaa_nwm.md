# Meet NOAA NWM

The *NOAA National Water Model ({term}`NWM`)* is produced by NOAA's [Office of Water Prediction](https://water.noaa.gov/about/nwm) (OWP), part of the National Weather Service (NWS). NWM is a hydrologic modeling framework, not an observational network — it simulates and forecasts streamflow (along with soil moisture, snowpack, and other water-budget variables) for over 3.4 million miles of rivers and streams across the U.S. and its territories by combining weather forecasts, land surface physics, and channel routing. It exists to fill the huge gap between official river forecast points and the entire river network: NOAA describes the NWM as complementing official NWS river forecasts at approximately 4,000 locations across the contiguous U.S. ({term}`CONUS`), giving forecasters, emergency managers, and floodplain managers guidance in places with no forecast point ([About the NWM](https://water.noaa.gov/about/nwm)). NWM output is supplemental guidance: official river forecasts at forecast points come from the NWS River Forecast Centers. Learn more at the [NWM landing page](https://water.noaa.gov/about/nwm), [National Water Prediction Service](https://water.noaa.gov/) viewer, and [CIROH's NWM overview](https://hub.ciroh.org/docs/products/national-water-model/).

:::{admonition} Partner review (NOAA): Official forecasts and model guidance
:class: important
Confirm the wording that NWM output is supplemental guidance and that official river forecasts at forecast points come from the NWS River Forecast Centers, and the figure of approximately 4,000 official forecast locations.
:::

## Terminology

This table maps NWM's own vocabulary onto the course's [shared concepts](00_introduction.md#m02-shared-concepts):

| Shared concept | NWM equivalent | Notes |
|---|---|---|
| {term}`Location identifier` | `feature_id` (= {term}`COMID`) | Each stream reach in the model has a unique {term}`feature_id`, which corresponds to a COMID in the {term}`NHDPlus` stream network (see below). |
| {term}`Variable` | streamflow | Channel discharge at a reach. NWM also outputs many other variables (soil moisture, snowpack, evapotranspiration, reservoir levels) that aren't the focus of this course. |
| {term}`Variable unit` | m³/s | Cubic meters per second, consistent across all NWM configurations. The NOAA NWM API labels it `CMS`. |
| {term}`Time` | {term}`reference time <Forecast reference time>` + {term}`valid time <Valid time>` | Every forecast value has two times (UTC): when the forecast was issued (reference time) and the time it predicts (valid time). The difference is the {term}`lead time <Lead time>`. The same valid time appears in many forecasts issued at different reference times. |
| {term}`Data quality flag(s)` | none per value | NWM has no per-observation QA/QC flag the way a sensor network does. Instead, quality is a function of which model version and configuration produced the value, see below. |
| {term}`Version / provenance` | model version and {term}`configuration <Configuration>` | For example v3.0, `medium_range`, issued 2026-10-08 18:00 UTC. Values for the same reach and valid time differ between versions and between configurations. |
| {term}`Data unit` | one output file per timestep | Each configuration's run writes one NetCDF file per valid time (for streamflow, a `channel_rt` file), holding every reach in the domain. |

Two network terms come up constantly with the NWM:

- **{term}`NHDPlus`** is short for "National Hydrography Dataset Plus." A USGS-maintained geospatial dataset that breaks the entire U.S. stream and river network into individual reaches, each with its own COMID, plus catchment boundaries and upstream/downstream connectivity. NWM doesn't define its own river network, it runs on top of NHDPlus, which is also why tools like {term}`NLDI` can look up COMIDs by location.
- **{term}`COMID`** is short for "Common Identifier." A unique numeric ID assigned to each individual stream segment (reach) in the NHDPlus stream network. NWM's `feature_id` values are the same numbers as COMIDs, just under a different name, so the two terms are used interchangeably across NWM documentation and tools.

## Dataset derivation

**Key point: NWM values are model output, and a new model version can change the numbers for the same reach and time.**

NWM output is entirely modeled, not measured directly. It couples a land-surface model (calculating snowmelt, infiltration, and runoff on a grid) with channel and reservoir routing along the NHDPlus stream network, driven by weather inputs called {term}`forcing <Forcing>`. The analysis configuration then uses {term}`data assimilation <Data assimilation>` of real-time observations (including USGS gage data) to correct the simulation.

It has gone through several major versions since becoming operational in August 2016: v1.0, v1.2 (2018, with expanded calibration to ~1,000+ basins), v2.0, v2.1, and v3.0. Each version can meaningfully change streamflow values at the same `feature_id`. A Texas-focused comparison of v2.1 and v3.0 across 610 USGS gages ([Journal of Hydrology: Regional Studies, 2025](https://doi.org/10.1016/j.ejrh.2025.102196)) found real gains in v3.0 overall, but during storm events specifically, both versions still struggle to capture peak flow magnitude and timing accurately. Always check the OWP version documentation or release notes before combining data across versions, and record the version you used (Module 1, [Publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data)).

:::{dropdown} What changed in v3.0
- First-time Total Water Level guidance for coastal CONUS, Hawaii, and Puerto Rico/USVI (via a coupled ocean model, SCHISM)
- Domain expansion into south-central Alaska
- A switch to the National Blend of Models as a forcing source for medium-range CONUS and Alaska forecasts
- Use of Multi-Radar Multi-Sensor precipitation for Puerto Rico/USVI
- Expanded ingestion of reservoir outflow forecasts (77 additional sites, bringing the total to 392)
- Calibration/parameter improvements
:::

:::{admonition} Partner review (NOAA): Current model version
:class: important
This page and the course's shared-concept table use v3.0 as the example model version. Confirm the operational NWM version as of October 2026, and where researchers should look to find which version produced a given file.
:::

## Spatial coverage

- **Extent:** CONUS + hydrologically-contributing areas, plus separate domains for Hawaii, Puerto Rico/USVI, and southern Alaska (Cook Inlet, Copper River Basin, Prince William Sound)
- **Type:** Point/vector network output for streamflow and reservoirs (one value per `feature_id`, over 2.7 million reaches); paired with 1 km gridded NetCDF for land-surface variables and 100–250 m gridded NetCDF for ponded water depth and soil saturation
- **Resolution:** Reach-based routing follows NHDPlus (medium-resolution, 1:100,000-scale network); grids are 1 km (land surface) and 100/250 m (near-surface hydrology)
- **{term}`CRS`:** Streamflow output has no coordinates: each value is tied to a `feature_id`, and you get its location by joining the `feature_id` to the NHDPlus reach with the same COMID. The underlying NHDPlus network uses the USA Contiguous Albers Equal Area Conic (USGS version); the gridded land-surface output uses its own Lambert Conformal Conic grid definition, documented in the NWM configuration files.

## Temporal coverage

- **Period of record:** A {term}`retrospective simulation <Retrospective simulation>` covers the historical period, and operational forecasts have run since August 2016. "Retrospective" here means a single, continuous model run over the full historical period, using historical weather data as input rather than real-time observations or forecasts. It's not a collection of old forecasts, it's NWM re-simulating what streamflow likely was at every `feature_id`, including reaches with no gage. The v3.0 retrospective on AWS covers February 1979 – January 2023 ([AWS Registry of Open Data](https://registry.opendata.aws/nwm-archive/), checked 2026-10-07). This makes it the main source of long-term, reach-level historical streamflow for ungauged locations.
- **Frequency/resolution:** Varies by configuration. Analysis & Assimilation and Short-Range are hourly, and the Retrospective dataset is hourly throughout. Medium-Range runs as an {term}`ensemble <Ensemble member>`: member 1 runs out to 10 days and members 2–6 out to 8.5 days; the NOAA NWM API returned hourly streamflow for all six members on 2026-10-08 (see the figure below). Long-Range output is 6-hourly.
- **Update cadence:** Short-Range forecasts cycle hourly over CONUS; Medium- and Long-Range forecasts are produced four times a day; forecast latency is roughly 1–2 hours after cycle time (mostly driven by the lag in incoming weather-forcing data)

**Which configuration do I want?** For history (a past flood, a long record at an ungaged reach), use the retrospective simulation. For what the model predicted or predicts about an event, use a forecast configuration. In CONUS:

| Configuration | What it's for | Horizon | Output interval | Issued |
|---|---|---|---|---|
| Retrospective | Long historical record, ungaged reaches | Feb 1979 – Jan 2023 (v3.0) | hourly | one-off run per model version |
| Analysis & Assimilation (`analysis_assim`) | Best estimate of current conditions | the last few hours | hourly | hourly |
| Short-Range (`short_range`) | Next-day forecasts | 18 hours | hourly | hourly |
| Medium-Range (`medium_range`) | Forecasts for the coming week; six ensemble members | 10 days (member 1); 8.5 days (members 2–6) | hourly in the NOAA NWM API (the archive files' interval is still being confirmed) | four times a day |
| Long-Range (`long_range`) | Monthly outlooks; four ensemble members | 30 days | 6-hourly | four times a day |

:::{admonition} Partner review (NOAA): Retrospective period and output intervals
:class: important
Confirm (1) the period covered by the current retrospective simulation, and the horizons in the configuration table (Short-Range 18 hours and Long-Range 30 days for CONUS) (an earlier draft said "1979–present (continuously extended)"; the AWS listing for v3.0 shows February 1979 – January 2023), and (2) the streamflow output interval for each configuration, in particular whether medium-range channel output is hourly for all members (an earlier draft said 3-hourly) and long-range output is 6-hourly.
:::

## Data content

- **Primary variable:** streamflow (m³/s) at each `feature_id`
- **Related variables available in the same output:** velocity, reservoir inflow/outflow/elevation, ponded water depth, depth to soil saturation, soil moisture, snowpack, evapotranspiration
- **Known limitations:** No formal per-value QA/QC flag exists; quality is instead governed by model version and configuration, and by how well any given basin was calibrated. Documented issues (e.g., both v2.1 and v3.0 struggle to capture storm peak magnitude and timing in the Texas comparison above) should be treated as caveats on the whole time series, not flags on individual values. As with any model, output quality also degrades in ungaged, heavily-regulated, or poorly-calibrated basins.

**What the data look like.** The figure shows one medium-range forecast for the NHDPlus reach of the Ohio River at Louisville, Kentucky (COMID `10164004`). Everything to the right of the dotted line is a prediction issued at a single reference time. Members 1–6 start from the same conditions and spread apart as lead time grows, and member 1 runs a day and a half longer than the others. Medium-range forecasts are issued four times a day, so six hours later a new forecast replaces this one; a forecast is identified by both its reach and its reference time.

This is model output, not an observation, and it is not checked against the gage here. The quick dip and rise in the first day may reflect the river's real behavior (Louisville sits at a lock and dam) or the forecast settling in from its starting conditions; Module 4 shows how to compare forecasts with observations. This figure also can't be lined up with the April 2025 flood shown on the SWOT and USGS pages, because the API only keeps the latest few days of forecasts. Past forecasts come from archives, as Module 3 explains.

The COMID `10164004` was found by asking the {term}`NLDI` which NHDPlus reach the Louisville USGS gage sits on; Module 3 shows how.

:::{figure} ../images/m02/02_meet_noaa_nwm-ohio-medium-range.png
:alt: Line chart of NWM medium-range streamflow forecasts for COMID 10164004 issued 2026-10-08 18:00 UTC. Flow dips to about 930 cubic meters per second, rises to about 1,890 on October 10, then declines to about 1,050 by October 17. Member 1 (blue) continues to October 18; members 2 to 6 (gray) end on October 17 and spread slightly, between about 1,020 and 1,150.
:width: 100%

NWM medium-range streamflow forecast for COMID `10164004`, Ohio River at Louisville, KY, issued (reference time) 2026-10-08 18:00 UTC. Data: NOAA NWM API (experimental), `configuration=medium_range`, accessed 2026-10-08. The API keeps only the most recent few days of forecasts, so this exact forecast can't be retrieved from it later.
:::

:::{dropdown} How this figure was made
This script asks NOAA's [NWM API](https://api.water.noaa.gov/nwm/v1/docs) for the latest medium-range forecast at one reach. The API needs no key. It returns JSON, which the script flattens into one row per ensemble member and valid time. It runs in the course's `m03-nwm` environment (`environments/m03-nwm.yml`); the Module 3 lesson explains this and the other NWM access routes.

```python
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Record the query in one place
COMID = 10164004                  # NHDPlus reach (NWM feature_id), Ohio River at Louisville, KY
url = f"https://api.water.noaa.gov/nwm/v1/streamflow/forecast/nwm_feature_id/{COMID}/"
resp = requests.get(url, params={"configuration": "medium_range", "latest": "true"}, timeout=60)
resp.raise_for_status()
run = resp.json()[0]              # one forecast run for this reach
print(run["configuration"], run["reference_datetime"], run["units"])

# Flatten to one row per member and valid time
rows = [{"member": m["member_id"], "valid_time": p["valid_datetime"], "streamflow": p["value"]}
        for m in run["forecast"] for p in m["timeseries"]]
fc = pd.DataFrame(rows)
fc["valid_time"] = pd.to_datetime(fc["valid_time"])

# Member 1 in blue, members 2-6 in gray, and a dotted line at the reference time
fig, ax = plt.subplots(figsize=(9, 3.6))
for member, grp in fc.groupby("member"):
    ax.plot(grp["valid_time"], grp["streamflow"], lw=2 if member == 1 else 1,
            color="#2a78d6" if member == 1 else "#8a8986",
            label="member 1 (to 10 days)" if member == 1 else ("members 2–6" if member == 2 else None))
ref = pd.to_datetime(run["reference_datetime"])
ax.axvline(ref, color="#0b0b0b", lw=1, ls=":")
ax.annotate("reference time\n" + ref.strftime("%Y-%m-%d %H:%M UTC"), (ref, ax.get_ylim()[1]),
            xytext=(4, -4), textcoords="offset points", va="top", fontsize=8)
ax.set_ylabel("Streamflow (m³/s)")
ax.set_xlabel("Valid time (UTC)")
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.set_title(f"NWM medium-range forecast, COMID {COMID} (Ohio River at Louisville, KY)", loc="left", fontsize=11)
ax.grid(alpha=0.3)
ax.legend(frameon=False, fontsize=9, loc="upper right")
fig.tight_layout()
fig.savefig("02_meet_noaa_nwm-ohio-medium-range.png", dpi=150)
```

The `print` line shows the run's configuration, reference time and units, for example `medium_range 2026-10-08T18:00:00Z CMS`. `fc` has one row per member and valid time: `member` (1–6), `valid_time` (UTC) and `streamflow` (m³/s). On 2026-10-08 member 1 had 240 hourly values and members 2–6 had 204 each. Because the API always serves the *latest* run, your numbers will differ from the figure.
:::

## Usage and support

- **Citation:** NOAA publishes a standard format on each dataset's AWS Registry of Open Data listing, e.g. for the Short-Range Forecast: *"NOAA National Water Model Short-Range Forecast was accessed on [DATE] from https://registry.opendata.aws/noaa-nwm-pds."* Swap in the specific product name, version, and dataset URL you actually used (e.g. the [Retrospective archive](https://registry.opendata.aws/nwm-archive/) instead of the Short-Range Forecast).
- **License/access:** NWM output is open data, distributed through the NOAA Open Data Dissemination ({term}`NODD`) program via AWS and Google Cloud, as well as a 48-hour rolling window on NOAA's {term}`NOMADS` server.
- **Which access route should I use?** NWM output can be reached several ways: the NOAA NWM API for current forecasts, {term}`hydrotools` for past forecasts, and {term}`kerchunk`/{term}`virtual Zarr <Virtual Zarr>` references for many reaches. They differ a lot in cost as your question grows. The Module 3 lesson [Retrieve NOAA NWM data](../03-federal-water-data-access-retrieval/02_access_noaa_nwm.md#nwm-access-routes) compares them.
- **Change over time:** Values can shift not just with new observations (in Analysis & Assimilation) but with model version upgrades — treat any long time series spanning a version change as non-homogeneous. Forecasts also *expire* from some services: the NOAA NWM API and NOMADS keep only the last few days. If your work depends on a specific forecast, record its configuration, reference time and model version, and keep a copy of the values you used; Module 1's [Publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data) discusses exactly this case.
- **Contact:** For questions about data content, quality, or model methodology, contact NOAA's Office of Water Prediction (contacts listed on the [NWM about page](https://water.noaa.gov/about/nwm)). For questions specifically about data delivery via NODD (AWS/Google Cloud access), email nodd@noaa.gov.

:::{admonition} TODO (dev team): Learner-review friction items (P6.5.4)
:class: attention
From the integration-pass learner review (2026-10-09). Not yet fixed:
- Terminology: say that `feature_id` = COMID holds for the CONUS domain (the glossary already does); Alaska, Hawaii and Puerto Rico domains need a NOAA check before stating what they use.
- CRS bullet: the Albers claim for NHDPlus needs a check (NHDPlusV2 is often distributed in NAD83 geographic); add that the Module 3 tools take and return EPSG:4326.
- Partner-review callouts still describe earlier drafts ("an earlier draft said 3-hourly", "1979–present"); keep the questions, drop the history.
- Mention `nwm_feature_id` (the NOAA NWM API's name for the ID); make the NOMADS window wording match the glossary (about 48 hours); give the Analysis & Assimilation lookback in hours.
- Split the opening paragraph; add the "you don't need to run this now" note to the figure dropdown.
:::

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
