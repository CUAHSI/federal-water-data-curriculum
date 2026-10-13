# Synthesizing Federal data products to build hydrologic confidence

One way that these datasets are leveraged to improve hydrologic understanding and confidence is through the flood analyses. Floods are one of the most visible ways that communities benefit from improved hydrologic confidence and water research investments. Each of the three Federal water data products unlock different capabilities and mitigate limitations for measuring and understanding hydrologic conditions, especially in flood events. In this lesson, we will explore a specific prior flood and learn how each Federal dataset contributes to improving our understanding of flood events from a surface water perspective. You will also learn ancillary skills that are needed to work with these datasets together given their different temporal and spatial extents.

## Flood event context

We are going to explore a flood from December 2025 in the Skagit River in Washington state. A long-lasting Category 5 atmospheric river brought heavy precipitation to the Pacific Northwest causing widespread flooding (see [more from NASA's Scientific Visualization Studio](https://svs.gsfc.nasa.gov/5596)). On December 12, 2025, the Skagit River near Mt Vernon passed its 1990 record crest (stage) (Source: [NOAA gauge information](https://water.noaa.gov/gauges/MVEW1)). While our lesson will be focused on exploring the flood through the lens of data, it is important to remember that floods impact real people and can have devastating impacts. The December 2025 Skagit River historic flooding event led to evacuation orders affecting more than 75,000 people in Skagit County (Source: [Northwest Public Broadcasting](https://www.nwpb.org/local/2025-12-11/100-000-evacuated-in-historic-skagit-valley-flood-in-washington-state)), and significantly damaged homes and businesses.

:::{figure} https://svs.gsfc.nasa.gov/vis/a000000/a005500/a005596/PacificNorthwestFlooding_Dec2025_1920x1080.png
:alt: Map of the North Pacific from Japan to North America. Water vapor is shaded from blue (dry) to yellow (moist); a labeled "Atmospheric River" band of moist air stretches from the tropics to the coast of Washington and British Columbia. An inset along the coast shades precipitation totals, heaviest (red) over British Columbia and western Washington.
:label: fig-skagit-ar

The December 2025 atmospheric river that drove the Skagit River flood, shown in a NASA GEOS analysis for 06:00 UTC on 9 December 2025: total precipitable water over the North Pacific, with accumulated precipitation along the Pacific Northwest coast. Credit: NASA's Global Modeling and Assimilation Office and NASA's Scientific Visualization Studio ([Tracking Weather Extremes: December 2025 Pacific Northwest Flooding](https://svs.gsfc.nasa.gov/5596)).
:::

:::{admonition} TODO (dev team): Skagit valley photo
:class: attention
Consider adding a before/after photo of the Skagit valley with a reuse-cleared credit.
:::

_The idea for using the Skagit River flooding event came from [the PO.DAAC SWOT tutorial "Hydrocron API: Getting Started with SWOT Time Series"](https://podaac.github.io/tutorials/notebooks/datasets/Hydrocron_SWOT_timeseries_examples_basic.html) authored by Nikki Tebaldi, Cassandra Nickles, and Brandi Downs._

The sections below walk through the data you would collect for this flood, product by product. Run the code blocks in order, in one Python session (later blocks reuse variables from earlier ones), using the Module 4 environment ([environments/m04-synthesis.yml](../environments/m04-synthesis.yml)):

```bash
# From the root of the course repository
conda env create -f environments/m04-synthesis.yml
conda activate m04-synthesis
# Optional: register this environment as a Jupyter kernel, then pick "Python (m04-synthesis)" in Jupyter
python -m ipykernel install --user --name m04-synthesis --display-name "Python (m04-synthesis)"
# Record the exact package versions next to your results, so you (or a reviewer) can rebuild this environment later
conda env export > m04-synthesis-versions.yml
```

A pinned {term}`conda environment <Conda environment>` is what lets someone re-run this analysis next year and get the same answer; Module 1's [reproducibility techniques](../01-data-best-practices/02_data_management.md#reproducibility-techniques) explain why. The outputs on this page came from `dataretrieval` 1.4.0, `pynhd` 0.20.0, `earthaccess` 0.19.0, `xarray` 2026.9.0 and `kerchunk` 0.2.10 on Python 3.14.

You will need the same credentials as in Module 3: a USGS Water Data {term}`API key` stored in the `API_USGS_PAT` environment variable (optional, but it raises your rate limit), and an Earthdata Login stored in `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` (required for the SWOT raster download). Keep both in environment variables, never in your code. If you stored the USGS key with `conda env config vars set` in Module 3, it belongs to the `m03-wdfn` environment only: repeat that step after `conda activate m04-synthesis`, then re-activate. If the Earthdata variables aren't set, `earthaccess.login()` prompts you, as in Module 3.

:::{admonition} TODO (dev team): Informational sections vs. lab assignment
:class: attention
Maybe the following sections are just informational and then the coded more prescriptive step-by-step analysis comes in the form of the lab assignment?
:::

## Defining the area of interest

This lesson follows the flood in the order you would meet it: the gage on the ground first, then the forecasts, then the satellite. (Elsewhere the course lists agencies NASA → NOAA → USGS; this page keeps its storyline order.)

Each agency describes "the river at Mount Vernon" with its own {term}`location identifier <Location identifier>`:

| Agency | Product | Location identifier for this lesson | What it represents |
|---|---|---|---|
| USGS | Water Data for the Nation ({term}`WDFN`) | {term}`monitoring location ID <Monitoring location ID>` `USGS-12200500` | A single gage on the riverbank |
| NOAA | National Water Model ({term}`NWM`) | {term}`feature_id` / {term}`NHDPlus` {term}`COMID` `24270288` | A stream segment (reach) in the NHDPlus network |
| NASA | SWOT RiverSP | {term}`SWORD` {term}`reach <Reach>` `78310800031` | A ~10 km reach of the SWOT River Database (SWORD) centerline |

Before we start, we write the whole query down in one place: the identifiers, time windows and product choices this page uses. Keeping them in variables, rather than scattered through the code, means you can record exactly what you asked for next to your results, and see at a glance what to change for another event (Module 1, [reproducibility techniques](../01-data-best-practices/02_data_management.md#reproducibility-techniques)).

```python
# The query for this case study, in one place. Save a copy of these values with your results.
site = "USGS-12200500"                                     # USGS monitoring location: Skagit River near Mount Vernon, WA
usgs_window = "2025-12-01T00:00:00Z/2025-12-31T23:59:59Z"  # continuous values, UTC
daily_window = "2025-12-01/2025-12-31"                     # daily values (local calendar days)
measurement_window = "2025-11-01/2026-01-31"               # field measurements
nwm_issue_times = [("20251211", "00"), ("20251211", "12"), ("20251211", "18")]  # short-range forecasts (YYYYMMDD, HH in UTC)
sword_reaches = ["78310800041", "78310800031", "78310800021", "78310800015"]   # lowest four SWORD reaches, upstream to downstream
swot_window = ("2025-11-01T00:00:00Z", "2026-01-15T00:00:00Z")                # RiverSP time series (UTC)
raster_window = ("2025-11-25", "2025-12-20")                                   # SWOT Raster granule search
raster_short_name = "SWOT_L2_HR_Raster_100m_D"                                 # Raster product, 100 m grid, version D
```

Nothing is downloaded yet; the sections below explain where each value comes from. A few event-specific details (the 1 December baseline date, the December filters, the Raster tile and the floodplain box) stay in the later blocks, where they are explained; the checklist at the end of the page lists them.

We need to link these identifiers before we can compare anything. We start from the gage because its location is surveyed and fixed. The modernized USGS Water Data API returns the gage's coordinates along with metadata such as drainage area and the vertical datum of the gage.

```python
import pandas as pd
from dataretrieval import waterdata

gage, _ = waterdata.get_monitoring_locations(monitoring_location_id=site)
gage_lon, gage_lat = gage.geometry.iloc[0].x, gage.geometry.iloc[0].y
print(gage[["monitoring_location_name", "drainage_area", "altitude", "vertical_datum"]])
print(f"Gage location: {gage_lat:.4f}, {gage_lon:.4f}")
```

The result is a one-row GeoDataFrame. `drainage_area` is in square miles (3,093 mi²) and `altitude` is the elevation of the gage datum (3.8, in feet) in the `vertical_datum` NAVD88. Keep that datum in mind: USGS gage height is measured from the gage datum, while SWOT water surface elevation is measured from a global geoid, so the two can't be compared directly without first converting between datums (the CUAHSI SWOT longitudinal-profile notebook in Further reading shows one way, using NOAA's VDatum service). In this lesson we sidestep that by comparing *changes* in water level.

:::{admonition} TODO (dev team): Unit of `altitude`
:class: attention
Verify unit of `altitude` in the monitoring-locations collection.
:::

The USGS [Network Linked Data Index (NLDI)](https://api.water.usgs.gov/nldi/swagger-ui/index.html) ({term}`NLDI`) indexes gages to the NHDPlus network that the National Water Model uses. The `pynhd` package wraps it; the NWM `feature_id` for a reach is its NHDPlus COMID.

```python
from pynhd import NLDI

nldi = NLDI()
gage_feature = nldi.getfeature_byid("nwissite", site)
comid = int(gage_feature["comid"].iloc[0])
print("NWM feature_id (NHDPlus COMID):", comid)
```

This returns COMID `24270288`. NOAA's own gauge page for the same site ([MVEW1](https://water.noaa.gov/gauges/MVEW1)) lists the same NWM reach, which is a useful cross-check.

SWOT river products are organized by the [SWOT River Database (SWORD)](https://www.swordexplorer.com/). We took the reach IDs in `sword_reaches` from the [PO.DAAC Hydrocron Skagit tutorial](https://podaac.github.io/tutorials/notebooks/datasets/Hydrocron_SWOT_timeseries_examples_basic.html) and looked for the one nearest the gage. The small helper below queries the PO.DAAC {term}`hydrocron` API (no login needed) for one reach at a time. We'll reuse it in the SWOT section.

```python
import io
import requests

HYDROCRON = "https://soto.podaac.earthdatacloud.nasa.gov/hydrocron/v1/timeseries"

def get_swot_reach(reach_id, start, end,
                   fields="reach_id,time_str,wse,wse_u,width,reach_q,reach_q_b,p_lat,p_lon"):
    """Return the SWOT RiverSP time series for one SWORD reach as a DataFrame."""
    params = {"feature": "Reach", "feature_id": reach_id, "start_time": start,
              "end_time": end, "output": "csv", "fields": fields}
    response = requests.get(HYDROCRON, params=params, timeout=60)
    response.raise_for_status()
    csv_text = response.json()["results"]["csv"]
    return pd.read_csv(io.StringIO(csv_text), dtype={"reach_id": str})

# One request per reach in sword_reaches (set in the query block), stacked into one table
swot = pd.concat([get_swot_reach(r, *swot_window) for r in sword_reaches], ignore_index=True)
print(swot.groupby("reach_id")[["p_lat", "p_lon"]].first())
```

`p_lat`/`p_lon` are the reach's prior (SWORD) center point, which isn't enough on its own to tell which reach holds the gage. We compared the reach centerlines instead (hydrocron returns them when you request `output=geojson` with the `geometry` field). The centerline of reach `78310800031` passes within a few tens of meters of the gage, about 1.2 km above the reach's downstream end, so that is the gage's reach. Reaches `…021` and `…015` continue downstream to Skagit Bay.

:::{admonition} TODO (dev team): SWORD spatial lookup
:class: attention
Replace the hard-coded reach list with a SWORD spatial lookup.
:::

A map makes the crosswalk concrete. The block below draws the three identifiers on one map: the Skagit main stem from the NLDI (the NHDPlus network the NWM runs on, 40 km up- and downstream of the gage), the NWM reach for our COMID, the four SWORD reach centerlines from `hydrocron` (asking for `output="geojson"` adds each reach's geometry), and the gage. A Washington State outline from the U.S. Census Bureau's [cartographic boundary files](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html) gives the shoreline of Skagit Bay for context.

```python
import geopandas as gpd
import matplotlib.pyplot as plt

# Skagit main stem on the NHDPlus network: 40 km upstream and 40 km downstream of the gage
river = pd.concat([nldi.navigate_byid("nwissite", site, nav, "flowlines", distance=40)
                   for nav in ("upstreamMain", "downstreamMain")], ignore_index=True)
nwm_reach = river[river["nhdplus_comid"].astype(int) == comid]

def get_swot_reach_line(reach_id):
    """Return one SWORD reach centerline (the same on every pass) as a one-row GeoDataFrame."""
    params = {"feature": "Reach", "feature_id": reach_id, "start_time": swot_window[0],
              "end_time": swot_window[1], "output": "geojson", "fields": "reach_id,geometry"}
    response = requests.get(HYDROCRON, params=params, timeout=60)
    response.raise_for_status()
    features = response.json()["results"]["geojson"]["features"]
    return gpd.GeoDataFrame.from_features(features[:1], crs="EPSG:4326")

sword_lines = pd.concat([get_swot_reach_line(r) for r in sword_reaches], ignore_index=True)

# Washington State outline (U.S. Census Bureau cartographic boundary file, 1:500,000, 2023)
states = gpd.read_file("https://www2.census.gov/geo/tiger/GENZ2023/shp/cb_2023_us_state_500k.zip")
wa = states[states["STUSPS"] == "WA"].to_crs("EPSG:4326")

fig, ax = plt.subplots(figsize=(8, 7))
wa.plot(ax=ax, color="#f2f1ec", edgecolor="#9a988f", lw=0.8)
river.plot(ax=ax, color="#9a988f", lw=1.5, label="NHDPlus main stem")
colors = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]  # one color per SWORD reach, upstream to downstream
for (_, row), color in zip(sword_lines.iterrows(), colors):
    gpd.GeoSeries([row.geometry], crs="EPSG:4326").plot(ax=ax, color=color, lw=4, alpha=0.8,
                                                        label=f"SWORD reach {row['reach_id']}")
nwm_reach.plot(ax=ax, color="black", lw=1.5, linestyle="--", label=f"NWM reach (COMID {comid})")
ax.plot(gage_lon, gage_lat, marker="^", color="black", markersize=10, linestyle="none", label=site)
xmin, ymin, xmax, ymax = sword_lines.total_bounds
ax.set_xlim(xmin - 0.05, xmax + 0.05)
ax.set_ylim(ymin - 0.04, ymax + 0.04)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Skagit River near Mount Vernon, WA: one river, three location identifiers")
ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8)  # legend outside the map
plt.show()
```

:::{figure} ../images/m04/synthesize-study-area.png
:alt: Map of the lower Skagit River in Washington State from Mount Vernon to Skagit Bay. A gray line traces the river main stem from the NHDPlus network, and the Washington shoreline is drawn in the upper left. Four thick colored lines mark the four lowest SWOT SWORD reaches, from reach 78310800041 above Mount Vernon to reach 78310800015 at the river mouth. A short dashed black line marks the NWM reach, COMID 24270288, and a black triangle marks the USGS gage 12200500, which sits on SWORD reach 78310800031.
:width: 100%

The study area. The USGS gage (triangle), the NWM reach that NLDI indexes it to (dashed) and the SWORD reach that holds it (`…031`) all describe "the Skagit at Mount Vernon", but at different sizes: a point, one NHDPlus segment and a ~10 km SWOT reach. Below the point where the river splits, the two networks also part ways: SWORD reach `…015` follows the western branch to Skagit Bay, while NLDI's downstream main stem follows the southern branch. Data: USGS NLDI flowlines and monitoring location; SWOT RiverSP reach centerlines from PO.DAAC `hydrocron`; U.S. Census Bureau cartographic boundary file (2023). Accessed 2026-10-08.
:::

## Starting on the ground: observations from USGS

The USGS gage is our reference: it records continuously, and USGS staff periodically measure the flow directly to check it. You can explore the same data in the [USGS Water Data viewer for 12200500](https://waterdata.usgs.gov/monitoring-location/USGS-12200500/#dataTypeId=continuous-00060-0&showFieldMeasurements=true&startDT=2025-12-01&endDT=2025-12-31). Here we request December 2025 {term}`continuous <Continuous values>` {term}`discharge <Discharge>` ({term}`parameter code <Parameter code>` `00060`) and {term}`gage height <Gage height>` (`00065`), plus {term}`daily <Daily values>` mean discharge (statistic code `00003` = mean), using the modernized `waterdata` module (see [Module 3](../03-federal-water-data-access-retrieval/03_access_usgs_wdfn.md) for setup and API keys).

```python
# 15-minute discharge (00060) and gage height (00065), and daily mean (00003) discharge, for December 2025
discharge, _ = waterdata.get_continuous(monitoring_location_id=site, parameter_code="00060", time=usgs_window)
stage, _ = waterdata.get_continuous(monitoring_location_id=site, parameter_code="00065", time=usgs_window)
daily, _ = waterdata.get_daily(monitoring_location_id=site, parameter_code="00060",
                               statistic_id="00003", time=daily_window)
print(discharge[["time", "value", "unit_of_measure", "approval_status", "qualifier"]].head())
```

Each table is a pandas DataFrame with one row per value (every 15 minutes for the continuous tables). In the course's shared vocabulary: the {term}`variable <Variable>` is identified by `parameter_code`, the {term}`variable unit <Variable unit>` is in `unit_of_measure` (`ft^3/s` for discharge, `ft` for gage height), and the {term}`data quality flags <Data quality flag(s)>` are `approval_status` (`Provisional` or `Approved`; see {term}`approval status <Approval status>`) and `qualifier` (for example, estimated or ice-affected values). The {term}`time <Time>` is in `time`, in UTC. When we accessed these data (2026-10-08), all December 2025 values at this gage were `Approved` with no qualifiers. Had they been {term}`provisional <Provisional data>`, they could change after you downloaded them, so record the approval status and your access date with any result (Module 1, [publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data)).

Finding the peak is a one-liner on each table:

```python
peak_q = discharge.loc[discharge["value"].idxmax()]
peak_h = stage.loc[stage["value"].idxmax()]
print(f"Peak discharge: {peak_q['value']:,.0f} {peak_q['unit_of_measure']} at {peak_q['time']}")
print(f"Peak stage:     {peak_h['value']} {peak_h['unit_of_measure']} at {peak_h['time']}")
```

The river peaked at **133,000 ft³/s at 08:00 UTC on 12 December 2025** (midnight local time), with a gage height of **37.73 ft** at 08:15 UTC. That stage is the highest on [NOAA's list of historic crests at this gauge](https://water.noaa.gov/gauges/MVEW1) (37.37 ft in November 1990), but the discharge isn't: NOAA's list shows 152,000 ft³/s for that 1990 crest. A record *stage* without a record *flow* is a clue that the relationship between stage and flow at this site isn't fixed.

:::{admonition} Partner review (USGS): Starting on the ground: observations from USGS
:class: important
Confirm interpretation of record stage vs. non-record discharge at 12200500.
:::

### Field measurements and the limits of out-of-bank flow

USGS doesn't measure discharge continuously. It records stage and converts it to discharge with a {term}`rating curve <Rating curve>` built from occasional {term}`field measurements <Field measurement>` of flow ([USGS: How streamflow is measured](https://www.usgs.gov/water-science-school/science/how-streamflow-measured)). So during a flood, check which field measurements support the numbers.

```python
measurements, _ = waterdata.get_field_measurements(monitoring_location_id=site, time=measurement_window)
q_meas = measurements[measurements["parameter_code"] == "00060"]
print(q_meas[["time", "time_of_day", "value", "unit_of_measure", "measurement_rated", "observing_procedure"]]
      .to_string(index=False))
```

Field measurements come back as one row per reading, with gage-height readings and discharge readings from the same `field_visit_id`. `time` holds only the date, and `time_of_day` only the time of day in UTC (for example `17:07:50+00:00`). To place a measurement on a timeline, join the two; converting `time_of_day` on its own would fill in today's date. `measurement_rated` is the hydrographer's rating of the measurement's accuracy (for example `Good` or `Fair`), and `observing_procedure` records how it was made.

USGS crews measured **111,000 ft³/s** with an acoustic Doppler current profiler (ADCP) at 17:07 UTC on 12 December, about nine hours after the crest, at a gage height of about 35.9 ft; the measurement was rated `Fair`. That is the highest discharge measured during the event. The reported peak of 133,000 ft³/s is therefore **above any flow measured in this flood**; it was computed from stage through the rating curve, not measured. Whether that part of the rating is supported by measurements from earlier floods is worth checking. When the river spills out of its banks or over levees, the stage–discharge relationship can change, and some water may bypass the gage entirely.

:::{admonition} TODO (dev team): Rating measurements above 111,000 ft³/s
:class: attention
Verify whether the 12200500 rating has measurements above 111,000 ft³/s from earlier floods, e.g. via `waterdata.get_ratings`.
:::

:::{admonition} Partner review (USGS): Field measurements and the limits of out-of-bank flow
:class: important
Wording on rating extrapolation and out-of-bank flow at this site.
:::

Plot the continuous and daily discharge, with the December field measurement overlaid:

```python
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(discharge["time"], discharge["value"], color="#2a78d6", lw=1.5, label="Continuous (15-minute)")
# Continuous times carry a UTC time zone; daily dates don't, so label them UTC before plotting them together
ax.step(pd.to_datetime(daily["time"]).dt.tz_localize("UTC"), daily["value"], where="post",
        color="#eb6834", lw=1.5, label="Daily mean")
dec_meas = q_meas[(q_meas["time"] >= "2025-12-01") & (q_meas["time"] < "2026-01-01")]
# Join the date (time) and the UTC time of day (time_of_day) into one timestamp
meas_time = pd.to_datetime(dec_meas["time"].dt.strftime("%Y-%m-%d") + "T" + dec_meas["time_of_day"])
ax.plot(meas_time, dec_meas["value"], "ko", label="Field measurement")
ax.set_ylabel("Discharge (ft³/s)")
ax.set_xlabel("Time (UTC)")
ax.set_title("USGS 12200500 Skagit River near Mount Vernon, WA")
ax.legend()
fig.autofmt_xdate()  # tilt the date labels so they don't overlap
plt.show()
```

The plot shows the flood rising from about 14,000 ft³/s in early December, the sharp crest on 12 December and a second, smaller rise around 17 December. The daily mean for 12 December is 112,000 ft³/s. That is well below the 15-minute peak, so daily values understate flood peaks. Daily values are computed over local (Pacific) calendar days, so plotting them at UTC midnight shifts the steps about 8 hours early; that's fine for a quick look.

:::{figure} ../images/m04/synthesize-usgs-hydrograph.png
:alt: Line chart of discharge at USGS gage 12200500, Skagit River near Mount Vernon, through December 2025. The 15-minute line rises from about 14,000 cubic feet per second in early December to a sharp crest of 133,000 on 12 December, falls, and rises again to a smaller peak around 17 December. Daily-mean steps follow the same shape but peak lower, at 112,000. A black dot marks the one December field measurement, 111,000 cubic feet per second, just after the crest.
:width: 100%

December 2025 discharge at USGS 12200500, Skagit River near Mount Vernon, WA: 15-minute continuous values, daily means and field measurements. The daily mean flattens the crest, and the highest field measurement sits well below the 15-minute peak. (The daily line ends with a short vertical drop only because the last daily step has no following day to extend to.) Data: USGS Water Data for the Nation (continuous and daily parameter `00060`, field measurements), all values `Approved`, accessed 2026-10-08.
:::

## Looking ahead: forecasts from NOAA NWM

The gage tells us what happened. The National Water Model (NWM) tells us what was *expected* to happen, on every NHDPlus reach, gaged or not. NOAA runs a **short-range** forecast every hour that looks 18 hours ahead. Here we ask: in the day before the crest, what did those forecasts say the Skagit at Mount Vernon would do? (NOAA's [National Water Prediction Service page for MVEW1](https://water.noaa.gov/gauges/MVEW1), the National Weather Service's ID for this gauge, shows a different product: the official National Weather Service river forecast for this gauge, issued by the Northwest River Forecast Center, not raw NWM output.)

:::{admonition} Partner review (NOAA): Looking ahead: forecasts from NOAA NWM
:class: important
Confirm this description of the NWPS gauge forecast vs. NWM.
:::

**Choosing an access route.** Module 3 compares the ways to get NWM forecasts ([Retrieve NOAA NWM data](../03-federal-water-data-access-retrieval/02_access_noaa_nwm.md#nwm-access-routes)). Two facts decide it for a past event. First, the no-key NOAA NWM API only keeps the last few days of forecasts, so it can't reach December 2025. Second, past forecasts are kept as NetCDF files in public cloud buckets (Google Cloud's `national-water-model` and AWS's `noaa-nwm-pds`). Each hourly file covers all ~2.8 million reaches. `hydrotools` downloads those whole files: about 250–280 MB per short-range forecast in Module 3's measurements, even for one reach. Building {term}`kerchunk` references instead indexes where each variable sits inside each file. `xarray` can then read only the `streamflow` chunks it needs, directly from the cloud. In Module 3's measurements this read about 7× fewer bytes with far less memory, and it needs no key.

The first block builds references for three short-range forecasts (the `short_range` {term}`configuration <Configuration>`) issued on 11 December, at 00Z, 12Z and 18Z (Z means UTC): the `nwm_issue_times` from the query block. Each issue time is a {term}`forecast reference time <Forecast reference time>`. We chose three issue times spread across the day before the crest, so you can see how the forecast changed as the flood approached; only the 18Z forecast's 18-hour window reaches past the crest. The two blocks below follow the [Module 3 kerchunk pattern](../03-federal-water-data-access-retrieval/02_access_noaa_nwm.md#nwm-kerchunk); most arguments (`inline_threshold`, `concat_dims`, `zarr_format` and so on) are explained there, and to reuse them you only change `nwm_issue_times` and `comid`. As in Module 3, CIROH's [`nwmurl`](https://hub.ciroh.org/docs/products/data-management/dataaccess/NWMURL%20Library) library builds the public HTTPS address of each hourly file, and building references reads about 1 MB of metadata from each of the 18 files per forecast. In our test (2026-10-08, home connection) all three took about 20 seconds together; expect it to vary with your connection.

```python
import fsspec
import nwmurl
from concurrent.futures import ThreadPoolExecutor
from kerchunk.hdf import SingleHdf5ToZarr
from kerchunk.combine import MultiZarrToZarr

def index_one(url):
    """Scan one NetCDF file's internal layout and return its kerchunk references."""
    with fsspec.open(url, "rb", block_size=2**20) as f:  # one 1 MB read covers the file's metadata
        return SingleHdf5ToZarr(f, url, inline_threshold=500).translate()

def build_refs(day, hour):
    """Index the 18 hourly files of one NWM short-range forecast and return combined kerchunk references."""
    urls = nwmurl.generate_urls_operational(
        start_date=f"{day}0000", end_date=f"{day}0000",  # YYYYMMDDHHMM; one day
        fcst_cycle=[int(hour)], lead_time=list(range(1, 19)),  # issue time; forecast hours 1-18
        varinput=1, geoinput=1, runinput=1,  # channel_rt (streamflow), CONUS, short_range
        urlbaseinput=3,                      # https://storage.googleapis.com/national-water-model/ (no account or key)
        meminput=None,                       # short_range has no ensemble members
    )
    with ThreadPoolExecutor(8) as pool:  # one request per file: run them in parallel
        singles = list(pool.map(index_one, urls))
    return MultiZarrToZarr(singles, remote_protocol="https", concat_dims=["time"],
                           identical_dims=["feature_id", "reference_time", "crs"]).translate()

# The short-range forecasts in nwm_issue_times, all issued before the 08:00 UTC 12 Dec crest
refs = {f"{day} {hour}Z": build_refs(day, hour) for day, hour in nwm_issue_times}
print({k: len(v["refs"]) for k, v in refs.items()})
```

Each forecast becomes a dictionary of references (`refs`), about 20 KB of JSON per forecast, which you could save and reuse instead of rebuilding. Next we open each forecast lazily with `xarray` and pull out our reach. Selecting `feature_id=comid` reads one ~1.8 MB `streamflow` chunk per forecast hour, the chunk holding that hour for every reach in the country, rather than the whole file.

```python
import xarray as xr

def open_refs(r):
    """Open kerchunk references lazily: data are read only when values are needed."""
    return xr.open_dataset("reference://", engine="zarr", chunks={}, consolidated=False, zarr_format=2,
                           storage_options={"fo": r, "remote_protocol": "https",
                                            "remote_options": {"asynchronous": True}})

forecasts = {}
for issued, r in refs.items():
    nwm = open_refs(r)
    nwm_version = nwm.attrs.get("NWM_version_number")  # provenance: which model version made this forecast
    q = nwm["streamflow"].sel(feature_id=comid).load()
    forecasts[issued] = q.to_series() * 35.3147  # m³/s -> ft³/s, to match USGS
    print(issued, "| model version:", nwm_version, "| units:", q.attrs.get("units"),
          "| max:", f"{forecasts[issued].max():,.0f} ft³/s", "at", forecasts[issued].idxmax())
```

Each entry in `forecasts` is a pandas Series of 18 hourly values. The {term}`variable <Variable>` is `streamflow`, the {term}`variable unit <Variable unit>` is `m3 s-1` (we convert to ft³/s to match USGS), and the index is each value's {term}`valid time <Valid time>` in UTC. NWM output has no per-value {term}`data quality flag <Data quality flag(s)>` like USGS's `approval_status` or SWOT's `reach_q`. What it does have is {term}`provenance <Version / provenance>`: the file attribute `NWM_version_number` says these forecasts came from NWM `v3.0`. Record it with your results, because a later model version would forecast the same storm differently.

:::{admonition} Partner review (NOAA): Looking ahead: forecasts from NOAA NWM
:class: important
Confirm there is no per-value quality flag in NWM channel output.
:::

Finally, we overlay the three forecasts on the USGS observations from earlier:

```python
fig, ax = plt.subplots(figsize=(10, 4))
obs = discharge.set_index("time")["value"]["2025-12-10":"2025-12-13"]
ax.plot(obs.index, obs.values, "k", lw=2, label="USGS observed (15-minute)")
forecast_colors = ["#2a78d6", "#eb6834", "#1baf7a"]  # one color per issue time, in order
for (issued, series), color in zip(forecasts.items(), forecast_colors):
    # NWM valid times are UTC but carry no time zone; label them so they line up with the USGS times
    ax.plot(series.index.tz_localize("UTC"), series.values, color=color, lw=2,
            label=f"NWM short range, issued {issued}")

ax.set_ylabel("Discharge (ft³/s)")
ax.set_xlabel("Time (UTC)")
ax.set_title(f"NWM forecasts at COMID {comid} vs. USGS 12200500")
ax.legend(loc="lower right", fontsize=8)
fig.autofmt_xdate()
plt.show()
```

:::{figure} ../images/m04/synthesize-nwm-forecasts.png
:alt: Line chart from 10 to 13 December 2025 comparing observed discharge at USGS 12200500 (black) with three NWM short-range forecasts issued at 00Z, 12Z and 18Z on 11 December. The observed line rises to a crest of 133,000 cubic feet per second early on 12 December. Each forecast line rises faster and peaks higher, between 142,000 and 160,000, several hours before the observed crest.
:width: 100%

Three NWM short-range forecasts for the Skagit at Mount Vernon (COMID 24270288), issued on 11 December 2025, against the USGS 15-minute record. Each forecast covers the 18 hours after it was issued. Data: NOAA National Water Model v3.0 short-range forecasts (`channel_rt`, CONUS) from the Google Cloud `national-water-model` archive; USGS Water Data for the Nation continuous discharge (`00060`, `Approved`). Accessed 2026-10-08.
:::

All three forecasts called for a bigger flood, sooner, than the gage recorded:

| Forecast issued (UTC) | Forecast peak (ft³/s) | Forecast peak time (UTC) | USGS observed at that time (ft³/s) |
|---|---|---|---|
| 11 Dec 00Z | 142,000 | 11 Dec 16:00 | 87,500 |
| 11 Dec 12Z | 160,000 | 12 Dec 00:00 | 116,000 |
| 11 Dec 18Z | 154,000 | 12 Dec 04:00 | 127,000 |

The observed crest was 133,000 ft³/s at 08:00 UTC on 12 December. Two cautions before reading this as "the model was wrong by 20%". The observed peak is itself computed from the rating curve above the highest flow measured in this flood (see the USGS section). And an NWM reach value is a model estimate for a whole reach, not a point measurement. What these forecasts did give, many hours ahead, is a consistent signal of an exceptional flood on a reach that, unlike most NWM reaches, also has a gage to check against.

:::{admonition} Partner review (NOAA): Looking ahead: forecasts from NOAA NWM
:class: important
Interpretation of the short-range forecasts against the observed hydrograph for this event.
:::

:::{admonition} TODO (dev team): Medium-range forecast member
:class: attention
Add a medium-range member to show multi-day lead time.
:::

## A view from above: surface water from NASA SWOT

SWOT doesn't measure the river continuously. It passes over a given spot a few times in each 21-day orbit cycle, so the first question is always *which passes saw the river during the flood?* We'll use the two SWOT products introduced in [Module 3](../03-federal-water-data-access-retrieval/01_access_nasa_swot.md), which answer different questions:

- **RiverSP (via `hydrocron`)**: {term}`water surface elevation <Water surface elevation>` (WSE), width and slope per SWORD reach. It answers "how high was the river?"
- **Raster 100 m (via {term}`earthaccess`)**: gridded water surface elevation, water area and water fraction. It answers "where was the water?"

Both are **Version D** products, each with its own DOI to cite: RiverSP [10.5067/SWOT-RIVERSP-D](https://doi.org/10.5067/SWOT-RIVERSP-D) and Raster 100 m [10.5067/SWOT-RASTER-D](https://doi.org/10.5067/SWOT-RASTER-D). Version D replaced Version C in 2025, and some reach IDs and values differ between versions, so note the version you used alongside your results ([SWOT Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf)).

### River water surface elevation through the event (RiverSP)

We already downloaded the RiverSP reach time series with `get_swot_reach()` while defining the area of interest. Missing passes come back with `time_str` of `no_data` and fill values, so we drop those first.

Before using any values, decide which passes to trust. RiverSP gives three quality fields per reach and pass, all defined in the [RiverSP product description, JPL D-56413 Rev C](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/pdd/D-56413_SWOT_Product_Description_L2_HR_RiverSP_20250224a_RevC_clean_sig_final.pdf):

- **`reach_q`**, the summary {term}`data quality flag <Data quality flag(s)>` (§4.1.7, p. 28):
  - **0 = good**
  - **1 = suspect:** "may have large errors"
  - **2 = degraded:** "very likely do have large errors"
  - **3 = bad:** may be nonsensical and "should be ignored"
- **`reach_q_b`**, an "expert" bit flag recording *why* `reach_q` is set (p. 28; bit names and values on pp. 60–61, details in Appendix C). For example, bit 2048 is `few_wse_observations`, 32768 is `partially_observed` and 262144 is `classification_qual_degraded`. The flag value is a sum of powers of two, one per problem, so `value & bit` is nonzero when that problem is present. Any bit at or above 262144 makes the pass at least degraded.
- **`wse_u`**: the total (random plus systematic) uncertainty of the reach WSE in meters (p. 22).

How many December passes would each threshold keep? The cross-tabulation below counts reach-passes by `reach_q`:

```python
swot = swot[swot["time_str"] != "no_data"].copy()
swot["time"] = pd.to_datetime(swot["time_str"])
december = swot[(swot["time"] >= "2025-12-01") & (swot["time"] < "2026-01-01")]
print(pd.crosstab(december["reach_id"], december["reach_q"], margins=True))
print("Passes kept with reach_q <= 1:", (december["reach_q"] <= 1).sum(),
      "| with reach_q <= 2:", (december["reach_q"] <= 2).sum())
```

December has 18 valid reach-passes: 4 flagged suspect (1) and 14 flagged degraded (2), with none good or bad. A strict `reach_q` ≤ 1 filter would leave **4 of 18**:
- **No passes at all for the gage's reach (`…031`)** or for `…041`.
- Only the 12 December pass for `…021`, which also loses its 1 December baseline, so we couldn't measure its rise.
- Three passes for `…015` at the river mouth.

That's why this lesson keeps **`reach_q` ≤ 2** and then checks the degraded values instead of trusting them: against the gage, and with `wse_u` and `reach_q_b`.

:::{admonition} Partner review (NASA): River water surface elevation through the event (RiverSP)
:class: important
Confirm that keeping `reach_q` = 2 (degraded) passes, with the checks below, is reasonable for the ~200 m wide tidal lower Skagit, and whether NASA recommends a different threshold for flood analyses.
:::

```python
swot = swot[swot["reach_q"] <= 2]
# One row per overpass (rounded to the hour), one column per reach
print(swot.pivot_table(index=swot["time"].dt.strftime("%Y-%m-%d %H:00"), columns="reach_id", values="wse"))
```

`wse` is in meters above the EGM2008 geoid (PDD p. 29) and `width` is in meters. The pivot covers the whole `swot_window` (November to mid-January); this lesson focuses on December. (The 29.5 m value for `…021` on 2 January is another implausible degraded value, outside our window.) The pivot shows five December passes over these reaches: 1 Dec, 4 Dec, **12 Dec at 09:00 UTC (one hour after the crest)**, 22 Dec and 25 Dec. On 12 December only the two downstream reaches were observed. Reach `…031`, where the gage sits, has no data for that pass. On 4 December, reach `…031` reports 17.3 m, up from 5.5 m three days earlier, while the gage was still at baseflow. Its `reach_q` is 2, the same as most of the good-looking passes, so the summary flag alone can't separate it. The other two fields can. A few `reach_q_b` bits, decoded:

```python
reach_q_bits = {2048: "few_wse_observations", 32768: "partially_observed",
                262144: "classification_qual_degraded", 524288: "geolocation_qual_degraded"}

def describe_bits(value):
    """Name the selected reach_q_b bits that are set in one flag value."""
    return ", ".join(name for bit, name in reach_q_bits.items() if int(value) & bit)

december = swot[(swot["time"] >= "2025-12-01") & (swot["time"] < "2026-01-01")]
print(december[["reach_id", "time_str", "wse", "wse_u", "reach_q"]]
      .assign(why=december["reach_q_b"].apply(describe_bits)).to_string(index=False))
```

All 14 degraded passes carry `classification_qual_degraded`, and 11 also carry `geolocation_qual_degraded`. These flags are common across this stretch of river, so they don't single out the bad values. Two things do:
- **`few_wse_observations` is set only on the 4 and 25 December passes** (on every reach except `…041`). On 4 December the gage reach has a `wse_u` of 0.66 m, the largest of the month, and on 25 December 0.32 m. Typical values are about 0.1 m.
- **The same passes look wrong against the gage** in the next step.

`wse_u` and `reach_q_b` give you the reason; the gage confirms it.

:::{admonition} Partner review (NASA): River water surface elevation through the event (RiverSP)
:class: important
Confirm this reading of `few_wse_observations` and `wse_u` for these passes.
:::

Because SWOT WSE and USGS gage height use different vertical references, we compare **changes** from a common baseline (the 1 December pass) instead of raw values. `stage_at()` looks up the gage height closest in time to each SWOT overpass:

```python
stage_series = stage.set_index("time")["value"].sort_index() * 0.3048  # feet to meters
def stage_at(t):
    """Return the gage height (m) at the 15-minute timestamp nearest to time t."""
    return stage_series.iloc[stage_series.index.get_indexer([t], method="nearest")[0]]

baseline = swot[swot["time"].dt.strftime("%Y-%m-%d") == "2025-12-01"].set_index("reach_id")["wse"]
swot["wse_change_m"] = swot["wse"] - swot["reach_id"].map(baseline)
first_pass = swot.loc[swot["time"].dt.strftime("%Y-%m-%d") == "2025-12-01", "time"].min()  # 1 Dec SWOT overpass
gage_baseline = stage_at(first_pass)
swot["gage_change_m"] = [stage_at(t) - gage_baseline for t in swot["time"]]
dec = swot[(swot["time"] >= "2025-12-01") & (swot["time"] < "2026-01-01")]
print(dec[["reach_id", "time", "wse_change_m", "gage_change_m", "reach_q", "wse_u"]]
      .round({"wse_change_m": 2, "gage_change_m": 2}).to_string(index=False))
```

The printed table has one row per reach and pass: the SWOT change and the gage's change at the same moment, both in meters, with `reach_q` and `wse_u` alongside. It is easier to read as a picture. The plot below draws the gage's rise as a continuous line and each SWOT reach-pass as a point, with `wse_u` as an error bar and the same reach colors as the study-area map:

```python
fig, ax = plt.subplots(figsize=(10, 4.5))
gage_change = (stage_series - gage_baseline)["2025-12-01":"2025-12-31"]
ax.plot(gage_change.index, gage_change.values, color="black", lw=1.5, label=f"{site} gage height change")
for reach_id, color in zip(sword_reaches, colors):  # colors: from the study-area map
    r = dec[dec["reach_id"] == reach_id]
    ax.errorbar(r["time"], r["wse_change_m"], yerr=r["wse_u"], fmt="o", ms=8, color=color,
                capsize=3, label=f"SWOT reach {reach_id}")
ax.axhline(0, color="#9a988f", lw=0.8)
ax.set_ylabel("Change since the 1 Dec pass (m)")
ax.set_xlabel("Time (UTC)")
ax.set_title("SWOT water surface elevation change vs. USGS gage height change, December 2025")
ax.legend(fontsize=8, loc="upper right")
fig.autofmt_xdate()
plt.show()
```

:::{figure} ../images/m04/synthesize-swot-wse-change.png
:alt: Chart of water-level change since 1 December 2025, in meters. A black line shows the USGS gage rising about 7 meters to a peak on 12 December, then falling with a second smaller rise. Colored points with error bars show SWOT reach changes on five passes. On 12 December two downstream reaches show rises of about 6 and 3 meters. On 4 December the gage's own reach sits about 12 meters above zero while the gage line is near zero, and on 25 December two reaches sit about 2 meters above the gage line.
:width: 100%

Change in water level since the 1 December 2025 SWOT pass: USGS gage height (line) and SWOT RiverSP reach water surface elevation (points, error bars = `wse_u`). Points close to the line agree with the gage; the 4 and 25 December outliers are the passes flagged `few_wse_observations`. Data: SWOT RiverSP Version D via PO.DAAC `hydrocron` (`reach_q` ≤ 2); USGS Water Data for the Nation gage height (`00065`, `Approved`). Accessed 2026-10-08.
:::

Near the peak, the gage had risen 7.2 m since 1 December. SWOT saw the reach just downstream (`…021`) up 6.0 m and the reach at the river mouth (`…015`) up 3.1 m. The rise shrinks toward Skagit Bay, where the tide sets the water level. On 22 December the gage's reach (`…031`) and the next reach down (`…021`) agree with the gage within about 0.2 m (+2.5 and +2.4 m vs. +2.5 m). On 25 December they don't: both reaches read about 2 m higher than the gage's change. Those are the passes flagged `few_wse_observations` (and `partially_observed`), and the gage reach's `wse_u` (0.32 m) is about three times its usual value. Treat single degraded values with caution, and let `wse_u` and `reach_q_b` tell you which ones to doubt first. Note what the error bars in the plot are *not*: `wse_u` is the product's own error estimate, and on degraded passes the actual error can be many times larger (the 4 December point is about 12 m off with a `wse_u` of 0.66 m). Treat an unusually large `wse_u` as a warning sign, not as the size of the error. RiverSP is a good record of *how high* the river got, along the whole river and not just at the gage. What it can't tell us is *where the water went* once it left the channel. RiverSP reports one value per fixed SWORD reach.

:::{admonition} Partner review (NASA): River water surface elevation through the event (RiverSP)
:class: important
Confirm how RiverSP handles floodplain (out-of-bank) water pixels near a reach.
:::

### Water extent before and near the peak (Raster)

The Raster product maps water across the whole swath on a 100 m grid. {term}`Granules <Granule>` are searched and downloaded with `earthaccess` (Earthdata Login required). A point search at the gage over late November to mid-December returns dozens of granules. Most are **false matches**: tiles that straddle the antimeridian (the 180° longitude line, {term}`UTM zones <UTM zone>` 60 and 1) have metadata footprints that wrap around the globe, so they wrongly match a point search, as in Module 3. We keep only granules in UTM zone 10, latitude band U (`UTM10U` in the granule name), which is where the Skagit is.

```python
import earthaccess

earthaccess.login()  # reads EARTHDATA_USERNAME / EARTHDATA_PASSWORD if set
results = earthaccess.search_data(
    short_name=raster_short_name,  # SWOT_L2_HR_Raster_100m_D: Raster product, 100 m grid, version D
    temporal=raster_window,        # late November to mid-December 2025
    point=(gage_lon, gage_lat),  # (longitude, latitude)
)
print(len(results), "granules returned")
skagit = [g for g in results if "_UTM10U_" in g["umm"]["GranuleUR"]]
for g in skagit:
    print(g["umm"]["GranuleUR"])
```

Three granules remain: 1 Dec 10:37, 4 Dec 23:59 and 12 Dec 09:00 UTC (about 70 MB each). We download them and open the before-flood and near-peak scenes with `xarray` (`earthaccess.download()` returns file paths; the timestamp in each file name identifies the pass). The files go to `data/raw/swot_raster/` and are never edited: anything we compute from them is a derived result, kept separately (Module 1, [publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data)). The granule names include the product version and processing counter, so they also document exactly which files you used.

```python
files = earthaccess.download(skagit, local_path="data/raw/swot_raster")  # raw downloads: keep unchanged
before = xr.open_dataset([f for f in files if "20251201T" in str(f)][0])
peak = xr.open_dataset([f for f in files if "20251212T" in str(f)][0])
print(peak[["water_frac", "water_area", "water_area_qual", "wse", "wse_qual"]])
```

Each granule is a ~1,600 × 1,600 grid in UTM zone 10N meters (`x`, `y`). `water_frac` is the fraction of each 100 m cell covered by water (unitless), `water_area` is water area in m², and `water_area_qual` is the data quality flag for both (0 good, 1 suspect, 2 degraded, 3 bad); `wse` and its flag `wse_qual` work the same way for water surface elevation. The near-peak pass stops about 4 km west of Mount Vernon (see the results below), so we look at the part of the floodplain both passes saw: a box of delta farmland west of the gage. We keep cells that are good or suspect in *both* passes, and count cells that are more than half water:

```python
import pyproj

# Longitude/latitude (EPSG:4326) -> UTM zone 10N meters (EPSG:32610), the grid of these granules
to_utm = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32610", always_xy=True)
gage_x, gage_y = to_utm.transform(gage_lon, gage_lat)
# A 15 km x 18 km box of delta farmland, from ~17 km to ~2 km west of the gage
delta = dict(x=slice(gage_x - 17_000, gage_x - 2_000), y=slice(gage_y - 11_000, gage_y + 7_000))
b, p = before.sel(**delta), peak.sel(**delta)
good = (b["water_area_qual"] <= 1) & (p["water_area_qual"] <= 1)
wet_before = (b["water_frac"] > 0.5) & good
wet_peak = (p["water_frac"] > 0.5) & good
print("Cells in box:", good.size, "| good or suspect in both passes:", int(good.sum()))
print("Wet in both:", int((wet_before & wet_peak).sum()),
      "| newly wet:", int((wet_peak & ~wet_before).sum()),
      "| newly dry:", int((wet_before & ~wet_peak).sum()))
gage_cell = peak.sel(x=gage_x, y=gage_y, method="nearest")
print("Near-peak pass at the gage: wse =", float(gage_cell["wse"]), "| wse_qual =", float(gage_cell["wse_qual"]))
```

Map water fraction for the two passes, showing only cells that are good or suspect in both:

```python
fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
for ax, ds, title in [(axes[0], b, "1 Dec 2025 (before)"), (axes[1], p, "12 Dec 2025 09:00 UTC (near peak)")]:
    # Express the grid as km east/north of the gage, which is easier to read than raw UTM meters
    km = ds["water_frac"].where(good).assign_coords(x=(ds["x"] - gage_x) / 1000, y=(ds["y"] - gage_y) / 1000)
    km.clip(0, 1).plot(ax=ax, vmin=0, vmax=1, cmap="Blues", cbar_kwargs={"label": "Water fraction"})
    ax.set_facecolor("#b8b6ae")  # grey = cells masked out (not good or suspect in both passes)
    ax.set_title(title)
    ax.set_xlabel("km east of the gage (negative = west)")
    ax.set_ylabel("km north of the gage")
    ax.set_aspect("equal")

plt.show()
```

:::{figure} ../images/m04/synthesize-swot-water-extent.png
:alt: Two side-by-side maps of SWOT water fraction over the Skagit delta west of Mount Vernon, on 1 December 2025 (before the flood) and 12 December 2025 at 09:00 UTC (near the peak). Dark blue cells are mostly water and white cells mostly land; grey cells were masked out because they were not good or suspect in both passes, and they cover about two thirds of the box. Axes are kilometers from the gage, which lies 2 km east of the box's right edge. Open water in the bays to the north and southwest and the river channels look nearly the same in both maps, with no broad new area of water on the farmland.
:width: 100%

SWOT Raster water fraction over the Skagit delta before the flood and about one hour after the crest, showing only cells whose `water_area_qual` is good or suspect in both passes; grey cells are masked, not dry. Axes are kilometers from the gage (which is just east of the box). Data: SWOT Level 2 KaRIn high-rate Raster, 100 m, Version D (`SWOT_L2_HR_Raster_100m_D`) via `earthaccess`, accessed 2026-10-08.
:::

The results are a lesson in what a single satellite pass can and can't show:

- **The near-peak pass missed the gage.** The edge of the 12 December swath falls about 4 km west of Mount Vernon. The gage cell is empty (`wse` is NaN, `wse_qual` = 3), matching the missing RiverSP value for reach `…031`.
- **In the delta it did see, extent barely changed.** Of the cells good or suspect in both passes, about 5,800 were wet in both, about 340 became wet and about 450 became dry, mostly along channel margins and field edges. This pass shows no broad sheet of new floodwater over the delta farmland.

  :::{admonition} TODO (dev team): Where the delta flooded
  :class: attention
  Verify against agency or news reports of where the delta flooded on 12 Dec, and check the tide at 09:00 UTC; levees may have kept water in the channel here.
  :::

- **Quality flags matter.** Only about a third of the cells in the box (about 9,300 of 27,000) are good or suspect in both passes. The 4 December scene (not plotted) shows striped false "water" across dry land near the gage, and `water_area_qual` flags most of it.

:::{admonition} TODO (dev team): 4 December Raster scene
:class: attention
Consider adding the 4 Dec scene to illustrate how `water_area_qual` flags false water.
:::

### Saving what you derived

Before moving on, save the comparison you built, separately from the raw downloads, with the identifiers and versions that produced it. This is the "recipe plus snapshot" idea from Module 1's [publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data): someone can rerun the query block, or check your numbers against the saved table.

```python
from pathlib import Path

derived = Path("data/derived")
derived.mkdir(parents=True, exist_ok=True)
# SWOT reach changes alongside the gage's change at each overpass (meters)
dec.drop(columns="time_str").to_csv(derived / "skagit_swot_vs_gage_dec2025.csv", index=False)
# The NWM forecasts, one column per issue time (ft³/s, valid time in UTC)
pd.DataFrame(forecasts).to_csv(derived / "skagit_nwm_short_range_dec2025.csv", index_label="valid_time")
# Provenance: what was asked for, which versions came back, and when
(derived / "provenance.txt").write_text(
    f"Accessed {pd.Timestamp.now(tz='UTC'):%Y-%m-%d} UTC\n"
    f"USGS {site}: continuous {usgs_window}; approval status {sorted(discharge['approval_status'].unique())}\n"
    f"NWM {nwm_version} short_range, COMID {comid}, issued {list(forecasts)}\n"
    f"SWOT RiverSP (hydrocron) reaches {sword_reaches}, {swot_window}; Raster {raster_short_name}: "
    f"{[g['umm']['GranuleUR'] for g in skagit]}\n")
print(sorted(p.name for p in derived.iterdir()))
```

The folder now holds two small CSV files and a `provenance.txt` that names the gage, approval status, NWM model version and SWOT granules. Cite the sources when you share results: USGS asks for the publication year, access date and DOI ([citing Water Data for the Nation](https://waterdata.usgs.gov/citation/); the DOI is [10.5066/F7P55KJN](https://doi.org/10.5066/F7P55KJN)), each SWOT collection has its own DOI (above, and on each collection's [PO.DAAC](https://podaac.jpl.nasa.gov/) landing page), and the NWM forecasts are cited by product, model version and access date ([NOAA NWM on AWS](https://registry.opendata.aws/noaa-nwm-pds/)).

## Conclusions

:::{admonition} TODO (dev team): Tighten prose in this section
:class: attention
Tighten prose.
:::

- **USGS** gives the most reliable, highest-frequency record *at a point*: the crest timing (08:00–08:15 UTC on 12 Dec), stage and discharge. Its field measurements show how far the flood peak was extrapolated beyond direct measurement.
- **NOAA NWM** short-range forecasts gave many hours' warning of an exceptional flood. At this reach they ran high and early, peaking at 142,000–160,000 ft³/s against an observed 133,000. They cover every reach, including reaches with no gage, and past forecasts can be read cheaply from the cloud with kerchunk references.
- **NASA SWOT** adds a spatial view. On the passes not flagged `few_wse_observations`, RiverSP's WSE changes matched the gage and showed the rise shrinking toward the bay; the gage's own reach was not observed at the peak. The Raster product can map water extent, but only when a pass lines up with the flood. Here the one near-peak pass stopped short of Mount Vernon.
- Linking the products takes deliberate work: three location identifiers (gage ID, COMID, SWORD reach), different vertical references (gage datum vs. geoid), different time steps (15-minute, hourly forecasts, a few passes per cycle) and different data quality flags. Each product fills gaps the others leave.

### Adapting this case study to another river

The query block holds the main choices, but a new event needs a few more decisions. Event dates also appear as literals in
later blocks; if you miss one, the code still runs but gives an empty baseline (`NaN` changes) or the wrong window, with no
error. Search the page's code for `2025-12`, `202512` and `_UTM10U_` after your edits. In order:

1. **Find the gage** and set `site` and the USGS windows. Check `approval_status`: a recent event will be provisional.
   In "Field measurements and the limits of out-of-bank flow", change the December filter on `q_meas` (`dec_meas`).
2. **Get the COMID** from the NLDI (the `getfeature_byid` block needs no changes).
3. **Find the SWORD reaches** near the gage: [SWORD Explorer](https://www.swordexplorer.com/), SWOTViz (see [Additional Federal water data](03_additional_data.md)) or the reach-finding steps in [Retrieve NASA SWOT data](../03-federal-water-data-access-retrieval/01_access_nasa_swot.md). Then confirm them with the study-area map.
4. **Check that SWOT passes exist** before and during the event. In the RiverSP section, change the December filters
   (the two `december = ...` lines and `dec = ...`), the baseline date (`"2025-12-01"`, used twice: `baseline` and
   `first_pass`) and the gage window in `gage_change`.
5. **For the Raster**, change the tile filter (`"_UTM10U_"`), the two file dates (`"20251201T"`, `"20251212T"`) and the
   `delta` box. To find your tile, print the `GranuleUR` of every search result first: your river's tile is the
   `_UTM<zone><band>_` code in the granules over your area (see {term}`UTM zone`), and the EPSG code in `to_utm` (just above the `delta` box)
   changes with the zone.
6. **For NWM**, pick `nwm_issue_times` before your crest and change the observation window in the forecast plot
   (`obs = ...["2025-12-10":"2025-12-13"]`). Past events come from the cloud archive, as here; for the last few days, the NOAA NWM API is simpler ([Retrieve NOAA NWM data](../03-federal-water-data-access-retrieval/02_access_noaa_nwm.md)).

:::{admonition} TODO (dev team): Learner-review friction items (P6.5.4)
:class: attention
From the integration-pass learner review (2026-10-09). Not yet fixed:
- Move the remaining event literals (baseline date, December filters, Raster tile and file dates, forecast-plot window) into the query block; the adaptation checklist lists them for now (needs a re-run).
- Add a short, reproducible check that the gage sits on SWORD reach `78310800031` (distance from the gage to each reach), for learners adapting the case study (needs a run).
- Explain or source "Category 5 atmospheric river"; replace the generic opening paragraph with what the learner will do; link statistic code and qualifier; comment that `zip` drops reaches beyond the four colors; use "gage" except in names and quotes.
:::

## Further reading

- Adapted from [Notebook to Demonstrate Collecting USGS Data (collect-usgs-streamflow.ipynb)](https://github.com/CUAHSI/notebooks/blob/develop/Data%20Access%20Examples/USGS%20-%20Plotting%20Streamflow%20using%20NWIS%20DataRetrieval/collect-usgs-streamflow.ipynb), CUAHSI notebooks (GPL-3.0); ported from the legacy `nwis` module to `waterdata`.

  :::{admonition} TODO (dev team): confirm this link
  :class: attention
  This link points to the CUAHSI/notebooks `develop` branch (collect-usgs-streamflow.ipynb). Confirm it is the link learners should use (branch, path and notebook name); keep the attribution either way.
  :::

  :::{admonition} TODO (dev team): Notebook authors
  :class: attention
  Verify notebook author(s) for attribution.
  :::

- Adapted from [Notebook to visualize SWOT longitudinal profile data (LongProfileVerticalDatum.ipynb)](https://github.com/CUAHSI/notebooks/blob/develop/Data%20Access%20Examples/SWOT%20-%20River%20Longitudinal%20Profiles%20for%20Water%20Resources/LongProfileVerticalDatum.ipynb) by Mike Durand with contributions from Bidhya Yadav (Ohio State University), CUAHSI notebooks (GPL-3.0); hydrocron request pattern and quality-flag filtering.

  :::{admonition} TODO (dev team): confirm this link
  :class: attention
  This link points to the CUAHSI/notebooks `develop` branch (LongProfileVerticalDatum.ipynb). Confirm it is the link learners should use (branch, path and notebook name); keep the attribution either way.
  :::

- [SWOT Version D KaRIn products release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf), PO.DAAC: what changed from Version C.
- [PO.DAAC](https://podaac.jpl.nasa.gov/), NASA's archive for SWOT data, where each collection's landing page gives its DOI.
- [Hydrocron API: Getting Started with SWOT Time Series](https://podaac.github.io/tutorials/notebooks/datasets/Hydrocron_SWOT_timeseries_examples_basic.html), PO.DAAC: Skagit River SWORD reach IDs.
- [Hydrocron documentation](https://podaac.github.io/hydrocron/), PO.DAAC.
- [`earthaccess` documentation](https://earthaccess.readthedocs.io/).
- [NASA SWOT mission site](https://swot.jpl.nasa.gov/), NASA/JPL: mission overview, data and documents.
- [SWOT Product Description: Level 2 KaRIn high rate river single pass vector product (L2_HR_RiverSP), JPL D-56413 Rev C, 24 Feb 2025](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/pdd/D-56413_SWOT_Product_Description_L2_HR_RiverSP_20250224a_RevC_clean_sig_final.pdf): `reach_q`, `reach_q_b`, `wse_u` and geoid definitions.
- [`dataretrieval-python` documentation](https://doi-usgs.github.io/dataretrieval-python/) and the [USGS Water Data APIs](https://api.waterdata.usgs.gov/).
- [USGS Water Science School: How streamflow is measured](https://www.usgs.gov/water-science-school/science/how-streamflow-measured).
- [How should I cite USGS Water Data for the Nation data?](https://waterdata.usgs.gov/citation/), USGS.
- [USGS Network Linked Data Index (NLDI)](https://api.water.usgs.gov/nldi/swagger-ui/index.html) and [`pynhd`](https://docs.hyriver.io/readme/pynhd.html).
- [NOAA National Water Prediction Service: Skagit River near Mount Vernon (MVEW1)](https://water.noaa.gov/gauges/MVEW1).
- NWM forecast archive on Google Cloud: the public `national-water-model` bucket, readable without an account at `https://storage.googleapis.com/national-water-model/<path>` (the code above reads it this way); also on AWS as [NOAA National Water Model Short-Range Forecast (`noaa-nwm-pds`)](https://registry.opendata.aws/noaa-nwm-pds/), Registry of Open Data on AWS.
- [`nwmurl`](https://hub.ciroh.org/docs/products/data-management/dataaccess/NWMURL%20Library) (CIROH), which builds the NWM file URLs used above ([source](https://github.com/CIROH-UA/nwmurl)).
- [`kerchunk` documentation](https://fsspec.github.io/kerchunk/). The reference-building pattern follows Module 3's NWM lesson ([03/02](../03-federal-water-data-access-retrieval/02_access_noaa_nwm.md)).
- [Tracking Weather Extremes: December 2025 Pacific Northwest Flooding](https://svs.gsfc.nasa.gov/5596), NASA Scientific Visualization Studio.
- [Cartographic Boundary Files](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html), U.S. Census Bureau: the state outline in the study-area map.
- Module 1: [reproducibility techniques](../01-data-best-practices/02_data_management.md#reproducibility-techniques) and [publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data).
