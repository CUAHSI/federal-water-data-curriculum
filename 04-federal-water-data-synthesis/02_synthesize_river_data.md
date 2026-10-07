# Synthesizing Federal data products to build hydrologic confidence

One way that these datasets are leveraged to improve hydrologic understanding and confidence is through the flood analyses. Floods are one of the most visible ways that communities benefit from improved hydrologic confidence and water research investments. Each of the three Federal water data products unlock different capabilities and mitigate limitations for measuring and understanding hydrologic conditions, especially in flood events. In this lesson, we will explore a specific prior flood and learn how each Federal dataset contributes to improving our understanding of flood events from a surface water perspective. You will also learn ancillary skills that are needed to work with these datasets together given their different temporal and spatial extents.

## Flood event context

We are going to explore a flood from December 2025 in the Skagit River in Washington state. A long-lasting Category 5 atmospheric river brought heavy precipitation to the Pacific Northwest causing widespread flooding (see [more from NASA's Scientific Visualization Studio](https://svs.gsfc.nasa.gov/5596)). On December 12, 2025, the Skagit River near Mt Vernon surpassed a 1990 record peak (Source: [NOAA gauge information](https://water.noaa.gov/gauges/MVEW1)). While our lesson will be focused on exploring the flood through the lens of data, it is important to remember that floods impact real people and can have devastating impacts. The December 2025 Skagit River historic flooding event led to evacuation orders affecting more than 75,000 people in Skagit County (Source: [Northwest Public Broadcasting](https://www.nwpb.org/local/2025-12-11/100-000-evacuated-in-historic-skagit-valley-flood-in-washington-state)), and significantly damaged homes and businesses.

:::{figure} https://svs.gsfc.nasa.gov/vis/a000000/a005500/a005596/PacificNorthwestFlooding_Dec2025_1920x1080.png
:alt: Map of the North Pacific from Japan to North America. Water vapor is shaded from blue (dry) to yellow (moist); a labeled "Atmospheric River" band of moist air stretches from the tropics to the coast of Washington and British Columbia. An inset along the coast shades precipitation totals, heaviest (red) over British Columbia and western Washington.
:label: fig-skagit-ar

The December 2025 atmospheric river that drove the Skagit River flood, shown in a NASA GEOS analysis for 06:00 UTC on 9 December 2025: total precipitable water over the North Pacific, with accumulated precipitation along the Pacific Northwest coast. Credit: NASA's Global Modeling and Assimilation Office and NASA's Scientific Visualization Studio ([Tracking Weather Extremes: December 2025 Pacific Northwest Flooding](https://svs.gsfc.nasa.gov/5596)).
:::

[POLISH: consider adding a before/after photo of the Skagit valley with a reuse-cleared credit.]

_The idea for using the Skagit River flooding event came from [the PO.DAAC SWOT tutorial "Hydrocron API: Getting Started with SWOT Time Series"](https://podaac.github.io/tutorials/notebooks/datasets/Hydrocron_SWOT_timeseries_examples_basic.html) authored by Nikki Tebaldi, Cassandra Nickles, and Brandi Downs._

The sections below walk through the data you would collect for this flood, product by product. Each code block runs on its own in the order shown, using the Module 4 environment ([environments/synthesis.yml](https://github.com/CUAHSI/federal-water-data-curriculum/blob/dev/environments/synthesis.yml)):

```bash
conda env create -f environments/synthesis.yml
conda activate fwdc-synthesis
```

You will need the same credentials as in Module 3: a USGS Water Data API key stored in the `API_USGS_PAT` environment variable (optional, but it raises your rate limit), and an Earthdata Login stored in `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` (required for the SWOT raster download).

[TODO: Maybe the following sections are just informational and then the coded more prescriptive step-by-step analysis comes in the form of the lab assignment?]

## Defining the area of interest

Each agency describes "the river at Mount Vernon" with its own **Location Identifier**:

| Agency | Product | Location Identifier for this lesson | What it represents |
|---|---|---|---|
| USGS | Water Data (NWIS) | `USGS-12200500` | A single gage on the riverbank |
| NOAA | National Water Model | feature ID / NHDPlus COMID `24270288` | A stream segment (reach) in the NHDPlus network |
| NASA | SWOT RiverSP | SWORD reach `78310800031` | A ~10 km reach of the SWOT River Database (SWORD) centerline |

Before we can compare anything, we need to link these identifiers. We start from the gage because its location is surveyed and fixed. The modernized USGS Water Data API returns the gage's coordinates along with metadata such as drainage area and the vertical datum of the gage.

```python
import pandas as pd
from dataretrieval import waterdata

site = "USGS-12200500"
gage, _ = waterdata.get_monitoring_locations(monitoring_location_id=site)
gage_lon, gage_lat = gage.geometry.iloc[0].x, gage.geometry.iloc[0].y
print(gage[["monitoring_location_name", "drainage_area", "altitude", "vertical_datum"]])
print(f"Gage location: {gage_lat:.4f}, {gage_lon:.4f}")
```

The result is a one-row GeoDataFrame. `drainage_area` is in square miles (3,093 mi²) and `altitude` is the elevation of the gage datum (3.8, in feet [TODO: verify unit of `altitude` in the monitoring-locations collection]) in the `vertical_datum` NAVD88. Keep that datum in mind: USGS gage height is measured from the gage datum, while SWOT water surface elevation is measured from a global geoid, so the two can't be compared directly without first converting between datums (the CUAHSI SWOT longitudinal-profile notebook in Further reading shows one way, using NOAA's VDatum service). In this lesson we sidestep that by comparing *changes* in water level.

The USGS [Network Linked Data Index (NLDI)](https://api.water.usgs.gov/nldi/swagger-ui/index.html) indexes gages to the NHDPlus network that the National Water Model uses. The `pynhd` package wraps it; the NWM `feature_id` for a reach is its NHDPlus COMID.

```python
from pynhd import NLDI

nldi = NLDI()
gage_feature = nldi.getfeature_byid("nwissite", site)
comid = int(gage_feature["comid"].iloc[0])
print("NWM feature_id (NHDPlus COMID):", comid)
```

This returns COMID `24270288`. NOAA's own gauge page for the same site ([MVEW1](https://water.noaa.gov/gauges/MVEW1)) lists the same NWM reach, which is a useful cross-check.

SWOT river products are organized by the [SWOT River Database (SWORD)](https://www.swordexplorer.com/). We used the reach IDs from the [PO.DAAC Hydrocron Skagit tutorial](https://podaac.github.io/tutorials/notebooks/datasets/Hydrocron_SWOT_timeseries_examples_basic.html) and looked for the one nearest the gage. The small helper below queries the PO.DAAC `hydrocron` API (no login needed) for one reach at a time. We'll reuse it in the SWOT section.

```python
import io
import requests

HYDROCRON = "https://soto.podaac.earthdatacloud.nasa.gov/hydrocron/v1/timeseries"

def get_swot_reach(reach_id, start, end,
                   fields="reach_id,time_str,wse,wse_u,width,reach_q,p_lat,p_lon"):
    """Return the SWOT RiverSP time series for one SWORD reach as a DataFrame."""
    params = {"feature": "Reach", "feature_id": reach_id, "start_time": start,
              "end_time": end, "output": "csv", "fields": fields}
    response = requests.get(HYDROCRON, params=params, timeout=60)
    response.raise_for_status()
    csv_text = response.json()["results"]["csv"]
    return pd.read_csv(io.StringIO(csv_text), dtype={"reach_id": str})

# Lowest four SWORD reaches on the Skagit, upstream to downstream
sword_reaches = ["78310800041", "78310800031", "78310800021", "78310800015"]
swot = pd.concat([get_swot_reach(r, "2025-11-01T00:00:00Z", "2026-01-15T00:00:00Z")
                  for r in sword_reaches])
print(swot.groupby("reach_id")[["p_lat", "p_lon"]].first())
```

`p_lat`/`p_lon` are the reach's prior (SWORD) center point, which isn't enough on its own to tell which reach holds the gage. We compared the reach centerlines instead (hydrocron returns them when you request `output=geojson` with the `geometry` field). The centerline of reach `78310800031` passes within a few tens of meters of the gage, about 1.2 km above the reach's downstream end, so that is the gage's reach. Reaches `…021` and `…015` continue downstream to Skagit Bay. [POLISH: replace the hard-coded reach list with a SWORD spatial lookup, and add a small map of the gage, NWM reach and SWORD reaches.]

## Starting on the ground: observations from USGS

The USGS gage is our reference: it records continuously, and USGS staff periodically measure the flow directly to check it. You can explore the same data in the [USGS Water Data viewer for 12200500](https://waterdata.usgs.gov/monitoring-location/USGS-12200500/#dataTypeId=continuous-00060-0&showFieldMeasurements=true&startDT=2025-12-01&endDT=2025-12-31). Here we request December 2025 **continuous** discharge (parameter code `00060`) and gage height (`00065`), plus **daily** mean discharge (statistic code `00003` = mean), using the modernized `waterdata` module (see [Module 3](../03-federal-water-data-access-retrieval/03_access_usgs_nwis.md) for setup and API keys).

```python
time_window = "2025-12-01T00:00:00Z/2025-12-31T23:59:59Z"
discharge, _ = waterdata.get_continuous(monitoring_location_id=site, parameter_code="00060", time=time_window)
stage, _ = waterdata.get_continuous(monitoring_location_id=site, parameter_code="00065", time=time_window)
daily, _ = waterdata.get_daily(monitoring_location_id=site, parameter_code="00060",
                               statistic_id="00003", time="2025-12-01/2025-12-31")
print(discharge[["time", "value", "unit_of_measure", "approval_status", "qualifier"]].head())
```

Each row is one 15-minute value. The **Variable** is identified by `parameter_code`, the **Variable unit** is in `unit_of_measure` (`ft^3/s` for discharge, `ft` for gage height), and the **Data Quality Flags** are `approval_status` (`Provisional` or `Approved`) and `qualifier` (for example, estimated or ice-affected values). At the time of writing, all December 2025 values at this gage are `Approved` with no qualifiers. Times are in UTC.

Finding the peak is a one-liner on each table:

```python
peak_q = discharge.loc[discharge["value"].idxmax()]
peak_h = stage.loc[stage["value"].idxmax()]
print(f"Peak discharge: {peak_q['value']:,.0f} {peak_q['unit_of_measure']} at {peak_q['time']}")
print(f"Peak stage:     {peak_h['value']} {peak_h['unit_of_measure']} at {peak_h['time']}")
```

The river peaked at **133,000 ft³/s at 08:00 UTC on 12 December 2025** (midnight local time), with a gage height of **37.73 ft** at 08:15 UTC. That stage is the highest on [NOAA's list of historic crests at this gauge](https://water.noaa.gov/gauges/MVEW1) (37.37 ft in November 1990), but the discharge isn't: NOAA's list shows 152,000 ft³/s for that 1990 crest. A record *stage* without a record *flow* is a clue that the relationship between stage and flow at this site isn't fixed. [PARTNER REVIEW: USGS] confirm interpretation of record stage vs. non-record discharge at 12200500.

### Field measurements and the limits of out-of-bank flow

USGS doesn't measure discharge continuously. It records stage and converts it to discharge with a **rating curve** built from occasional field measurements of flow ([USGS: How streamflow is measured](https://www.usgs.gov/water-science-school/science/how-streamflow-measured)). So during a flood, check which field measurements support the numbers.

```python
measurements, _ = waterdata.get_field_measurements(monitoring_location_id=site, time="2025-11-01/2026-01-31")
q_meas = measurements[measurements["parameter_code"] == "00060"]
print(q_meas[["time", "time_of_day", "value", "unit_of_measure", "measurement_rated", "observing_procedure"]])
```

Field measurements come back as one row per reading, with gage-height readings and discharge readings from the same `field_visit_id`. `time` holds the date and `time_of_day` the UTC timestamp. `measurement_rated` is the hydrographer's rating of the measurement's accuracy (for example `Good` or `Fair`), and `observing_procedure` records how it was made.

USGS crews measured **111,000 ft³/s** with an acoustic Doppler current profiler (ADCP) at 17:07 UTC on 12 December, about nine hours after the crest, at a gage height of about 35.9 ft; the measurement was rated `Fair`. That is the highest discharge measured during the event. The reported peak of 133,000 ft³/s is therefore **above any flow measured in this flood**; it was computed from stage through the rating curve, not measured. Whether that part of the rating is supported by measurements from earlier floods is worth checking. When the river spills out of its banks or over levees, the stage–discharge relationship can change, and some water may bypass the gage entirely. [TODO: verify whether the 12200500 rating has measurements above 111,000 ft³/s from earlier floods, e.g. via `waterdata.get_ratings`.] [PARTNER REVIEW: USGS] wording on rating extrapolation and out-of-bank flow at this site.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(discharge["time"], discharge["value"], lw=1, label="Continuous (15-minute)")
ax.step(pd.to_datetime(daily["time"]).dt.tz_localize("UTC"), daily["value"], where="post", label="Daily mean")
dec_meas = q_meas[q_meas["time"].astype(str).str.startswith("2025-12")]
ax.plot(pd.to_datetime(dec_meas["time_of_day"]), dec_meas["value"], "ko", label="Field measurement")
ax.set_ylabel("Discharge (ft³/s)")
ax.set_title("USGS 12200500 Skagit River near Mount Vernon, WA")
ax.legend()
plt.show()
```

The plot shows the flood rising from about 14,000 ft³/s in early December, the sharp crest on 12 December and a second, smaller rise around 17 December. The daily mean for 12 December is 112,000 ft³/s. That is well below the 15-minute peak, so daily values understate flood peaks. Daily values are computed over local (Pacific) calendar days, so plotting them at UTC midnight shifts the steps about 8 hours early; that's fine for a quick look. [POLISH: commit a static copy of this figure with alt text.]

## Looking ahead: forecasts from NOAA NWM

:::{note} Stub: waiting on the NWM access-route measurements
This section will be written from Lane A's access-route measurements (ROADMAP P1.3, `spike/nwm/REPORT.md`), which weren't ready when this rough cut was drafted.
:::

[TODO: NWM section, waiting on P1.3 results. Planned content:]

- **Why forecasts:** NWM short- and medium-range forecasts at COMID `24270288` show what forecasters' model guidance said *before* the 12 December crest. That fills the gap between gages and adds a forward look.
- **How the forecasts changed approaching the peak:** pull 2–3 short-range reference times before 08:00 UTC 12 Dec plus one medium-range member, then overlay them on the USGS observations from the previous section.
- **Access route:** use the no-key route that P1.3 recommends for past forecasts (expected: `hydrotools` GCP archive or kerchunk references). The NOAA NWM API only keeps about three days of forecasts [TODO: verify retention window from P1.3], so it can't reach December 2025.
- **One-paragraph pointer** to Module 3's NWM access-route guidance ([03/02](../03-federal-water-data-access-retrieval/02_access_noaa_nwm.md); a "Which access route for which use case?" table is being added there in ROADMAP P4.1), covering the cost of pulling whole CONUS files and when to use kerchunk.
- Data viewer for comparison: [NOAA National Water Prediction Service — MVEW1](https://water.noaa.gov/gauges/MVEW1).

## A view from above: surface water from NASA SWOT

SWOT doesn't measure the river continuously. It passes over a given spot a few times in each 21-day orbit cycle, so the first question is always *which passes saw the river during the flood?* We'll use the two SWOT products introduced in [Module 3](../03-federal-water-data-access-retrieval/01_access_nasa_swot.md), which answer different questions:

- **RiverSP (via `hydrocron`)**: water surface elevation (WSE), width and slope per SWORD reach. It answers "how high was the river?"
- **Raster 100 m (via `earthaccess`)**: gridded water surface elevation, water area and water fraction. It answers "where was the water?"

### River water surface elevation through the event (RiverSP)

We already downloaded the RiverSP reach time series with `get_swot_reach()` while defining the area of interest. Missing passes come back with `time_str` of `no_data` and fill values, so we drop those. We keep `reach_q` up to 2: the **Data Quality Flag** `reach_q` runs from 0 (good) through 1 (suspect) and 2 (degraded) to 3 (bad) ([SWOT_L2_HR_RiverSP_D at PO.DAAC](https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_RiverSP_D); see the product description document there) [TODO: verify direct link to the RiverSP product description PDF]. Most passes over the three lowest reaches are flagged 2 (degraded), so filtering to 0–1 would discard most of this event. [PARTNER REVIEW: NASA] confirm that `reach_q` ≤ 2 is a reasonable filter for a ~200 m wide tidal river.

```python
swot = swot[swot["time_str"] != "no_data"].copy()
swot["time"] = pd.to_datetime(swot["time_str"])
swot = swot[swot["reach_q"] <= 2]
# One row per overpass (rounded to the hour), one column per reach
print(swot.pivot_table(index=swot["time"].dt.strftime("%Y-%m-%d %H:00"), columns="reach_id", values="wse"))
```

`wse` is in meters above the EGM2008 geoid [TODO: verify against the RiverSP product description], `wse_u` is its uncertainty (m) and `width` is in meters. The pivot shows five December passes over these reaches: 1 Dec, 4 Dec, **12 Dec at 09:00 UTC (one hour after the crest)**, 22 Dec and 25 Dec. On 12 December only the two downstream reaches were observed. Reach `…031`, where the gage sits, has no data for that pass. On 4 December, reach `…031` reports 17.3 m (up from 5.5 m three days earlier) with a large uncertainty, while the gage was still at baseflow. Even a "degraded" flag can hide a bad value, so sanity-check SWOT against another source.

Because SWOT WSE and USGS gage height use different vertical references, we compare **changes** from a common baseline (the 1 December pass) instead of raw values. `stage_at()` looks up the gage height closest in time to each SWOT overpass:

```python
stage_series = stage.set_index("time")["value"].sort_index() * 0.3048  # feet to meters
def stage_at(t):
    return stage_series.iloc[stage_series.index.get_indexer([t], method="nearest")[0]]

baseline = swot[swot["time"].dt.strftime("%Y-%m-%d") == "2025-12-01"].set_index("reach_id")["wse"]
swot["wse_change_m"] = swot["wse"] - swot["reach_id"].map(baseline)
first_pass = swot.loc[swot["time"].dt.strftime("%Y-%m-%d") == "2025-12-01", "time"].min()  # 1 Dec SWOT overpass
gage_baseline = stage_at(first_pass)
swot["gage_change_m"] = [stage_at(t) - gage_baseline for t in swot["time"]]
dec = swot[(swot["time"] >= "2025-12-01") & (swot["time"] < "2026-01-01")]
print(dec[["reach_id", "time", "wse_change_m", "gage_change_m", "reach_q"]]
      .round({"wse_change_m": 2, "gage_change_m": 2}).to_string(index=False))
```

Near the peak, the gage had risen 7.2 m since 1 December. SWOT saw the reach just downstream (`…021`) up 6.0 m and the reach at the river mouth (`…015`) up 3.1 m. The rise shrinks toward Skagit Bay, where the tide sets the water level. On 22 December the gage's reach (`…031`) and the next reach down (`…021`) agree with the gage within about 0.15 m (+2.5 and +2.4 m vs. +2.5 m). On 25 December they don't: both reaches read about 2 m higher than the gage's change, with `reach_q` = 2. Treat single degraded values with caution. RiverSP is a good record of *how high* the river got, along the whole river and not just at the gage. What it can't tell us is *where the water went* once it left the channel. RiverSP reports one value per fixed SWORD reach. [PARTNER REVIEW: NASA] confirm how RiverSP handles floodplain (out-of-bank) water pixels near a reach.

### Water extent before and near the peak (Raster)

The Raster product maps water across the whole swath on a 100 m grid. Granules are searched and downloaded with `earthaccess` (Earthdata Login required). A point search at the gage over late November to mid-December returns dozens of granules. Most are **false matches from tiles near the antimeridian** (UTM zones 60 and 1). We keep only granules in UTM zone 10, latitude band U (`UTM10U` in the granule name), which is where the Skagit is.

```python
import earthaccess

earthaccess.login()  # reads EARTHDATA_USERNAME / EARTHDATA_PASSWORD if set
results = earthaccess.search_data(
    short_name="SWOT_L2_HR_Raster_100m_D",  # Raster product, 100 m grid, collection version D
    temporal=("2025-11-25", "2025-12-20"),
    point=(gage_lon, gage_lat),  # (longitude, latitude)
)
print(len(results), "granules returned")
skagit = [g for g in results if "_UTM10U_" in g["umm"]["GranuleUR"]]
for g in skagit:
    print(g["umm"]["GranuleUR"])
```

Three granules remain: 1 Dec 10:37, 4 Dec 23:59 and 12 Dec 09:00 UTC (about 70 MB each). We download them and open the before-flood and near-peak scenes with `xarray` (`earthaccess.download()` returns file paths; the timestamp in each file name identifies the pass):

```python
import xarray as xr

files = earthaccess.download(skagit, local_path="swot_raster")
before = xr.open_dataset([f for f in files if "20251201T" in str(f)][0])
peak = xr.open_dataset([f for f in files if "20251212T" in str(f)][0])
print(peak[["water_frac", "water_area", "water_area_qual", "wse"]])
```

Each granule is a ~1,600 × 1,600 grid in UTM zone 10N meters (`x`, `y`). `water_frac` is the fraction of each 100 m cell covered by water (unitless), `water_area` is water area in m², and `water_area_qual` is the **Data Quality Flag** for both (0 good, 1 suspect, 2 degraded, 3 bad). Next we subset to the delta farmland west of Mount Vernon, keep cells that are good or suspect in *both* passes, and count cells that are more than half water:

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

```python
fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
for ax, ds, title in [(axes[0], b, "1 Dec 2025 (before)"), (axes[1], p, "12 Dec 2025 09:00 UTC (near peak)")]:
    ds["water_frac"].where(good).clip(0, 1).plot(ax=ax, vmin=0, vmax=1, cmap="Blues")
    ax.set_title(title)
    ax.set_aspect("equal")
plt.show()
```

The results are a lesson in what a single satellite pass can and can't show:

- **The near-peak pass missed the gage.** The edge of the 12 December swath falls about 4 km west of Mount Vernon. The gage cell is empty (`wse` is NaN, `wse_qual` = 3), matching the missing RiverSP value for reach `…031`.
- **In the delta it did see, extent barely changed.** Of the cells good or suspect in both passes, about 5,800 were wet in both, about 340 became wet and about 450 became dry, mostly along channel margins and field edges. This pass shows no broad sheet of new floodwater over the delta farmland. [TODO: verify against agency or news reports of where the delta flooded on 12 Dec, and check the tide at 09:00 UTC; levees may have kept water in the channel here.]
- **Quality flags matter.** Only about a third of the cells in the box (about 9,300 of 27,000) are good or suspect in both passes. The 4 December scene (not plotted) shows striped false "water" across dry land near the gage, and `water_area_qual` flags most of it.

[POLISH: commit a static copy of the before/near-peak figure with alt text; consider adding the 4 Dec scene to illustrate quality flags.]

## Conclusions

[POLISH: tighten once the NWM section is in.]

- **USGS** gives the most reliable, highest-frequency record *at a point*: the crest timing (08:00–08:15 UTC on 12 Dec), stage and discharge. Its field measurements show how far the flood peak was extrapolated beyond direct measurement.
- **NOAA NWM** forecasts (section pending) show what the model expected ahead of the crest, on every reach, including reaches with no gage.
- **NASA SWOT** adds a spatial view. RiverSP's WSE changes matched the gage's rise and showed it shrinking toward the bay. The Raster product can map water extent, but only when a pass lines up with the flood. Here the one near-peak pass stopped short of Mount Vernon.
- Linking the products takes deliberate work: three Location Identifiers (gage ID, COMID, SWORD reach), different vertical references (gage datum vs. geoid), different time steps (15-minute, hourly forecasts, a few passes per cycle) and different Data Quality Flags. Each product fills gaps the others leave.

## Further reading

- Adapted from [Notebook to Demonstrate Collecting USGS Data (collect-usgs-streamflow.ipynb)](https://github.com/CUAHSI/notebooks/blob/develop/Data%20Access%20Examples/USGS%20-%20Plotting%20Streamflow%20using%20NWIS%20DataRetrieval/collect-usgs-streamflow.ipynb), CUAHSI notebooks (GPL-3.0); ported from the legacy `nwis` module to `waterdata`. [TODO: verify notebook author(s) for attribution.]
- Adapted from [Notebook to visualize SWOT longitudinal profile data (LongProfileVerticalDatum.ipynb)](https://github.com/CUAHSI/notebooks/blob/develop/Data%20Access%20Examples/SWOT%20-%20River%20Longitudinal%20Profiles%20for%20Water%20Resources/LongProfileVerticalDatum.ipynb) by Mike Durand with contributions from Bidhya Yadav (Ohio State University), CUAHSI notebooks (GPL-3.0); hydrocron request pattern and quality-flag filtering.
- [Hydrocron API: Getting Started with SWOT Time Series](https://podaac.github.io/tutorials/notebooks/datasets/Hydrocron_SWOT_timeseries_examples_basic.html), PO.DAAC: Skagit River SWORD reach IDs.
- [Hydrocron documentation](https://podaac.github.io/hydrocron/), PO.DAAC.
- [`earthaccess` documentation](https://earthaccess.readthedocs.io/).
- [SWOT mission and product documentation](https://podaac.jpl.nasa.gov/SWOT), PO.DAAC.
- [`dataretrieval-python` documentation](https://doi-usgs.github.io/dataretrieval-python/) and the [USGS Water Data APIs](https://api.waterdata.usgs.gov/).
- [USGS Water Science School: How streamflow is measured](https://www.usgs.gov/water-science-school/science/how-streamflow-measured).
- [USGS Network Linked Data Index (NLDI)](https://api.water.usgs.gov/nldi/swagger-ui/index.html) and [`pynhd`](https://docs.hyriver.io/readme/pynhd.html).
- [NOAA National Water Prediction Service: Skagit River near Mount Vernon (MVEW1)](https://water.noaa.gov/gauges/MVEW1).
- [Tracking Weather Extremes: December 2025 Pacific Northwest Flooding](https://svs.gsfc.nasa.gov/5596), NASA Scientific Visualization Studio.
