# Module overview

Three Federal agencies publish open river data that researchers use every day, and each one answers a different
question. The *NASA Surface Water and Ocean Topography (SWOT)* satellite measures rivers from space. The *NOAA National
Water Model (NWM)* simulates and forecasts streamflow for millions of river reaches. *USGS Water Data for the Nation
(WDFN)* publishes measurements from thousands of monitoring locations on the ground.

Before you write any code to retrieve these data (Module 3) or combine them (Module 4), it helps to know what each product
*is*: what it measures or models, how the values are made, where and when they exist, and what can go wrong. That is the
job of this module. Each page introduces one product, and you can read them in any order.

## Learning objectives

By the end of this module, learners should be able to:
- Characterize the river data products from NASA SWOT, NOAA NWM, and USGS WDFN, including relevant variables, derivation, spatial and temporal resolution, and known limitations.

(m02-shared-concepts)=
## One framework for three products

Each agency has its own vocabulary. SWOT talks about {term}`granules <Granule>` and {term}`reaches <Reach>`, the NWM
about {term}`COMIDs <COMID>` and model {term}`configurations <Configuration>`, and USGS about
{term}`monitoring locations <Monitoring location ID>` and {term}`parameter codes <Parameter code>`. Underneath, they all
answer the same seven questions. This course calls these the **shared concepts**, and every "Meet" page starts with a
table that maps the agency's terms onto them.

| Shared concept | Question it answers | NASA SWOT | NOAA NWM | USGS WDFN |
|---|---|---|---|---|
| {term}`Location identifier` | *Where* is this value? | `reach_id`, `node_id` (SWORD) | COMID / `feature_id` (NHDPlus) | monitoring location ID (`USGS-03294500`) |
| {term}`Variable` | *What* was measured or modeled? | water surface elevation, width, … | streamflow | discharge, gage height, … |
| {term}`Variable unit` | In what units? | m, m/km, m³/s | m³/s | ft³/s, ft |
| {term}`Time` | *When*, and how often? | overpass time | forecast reference time + valid time | timestamp (continuous / daily) |
| {term}`Data quality flag(s)` | How much should I trust it? | `reach_q`, `wse_qual`, … | none per value (model output) | approval status (provisional / approved), qualifiers |
| {term}`Version / provenance` | Which release, from where? | product version (e.g. `D`), collection DOI | model version (e.g. v3.0), run configuration | service, retrieval date |
| {term}`Data unit` | What is one "file" or record? | granule | one output file per timestep | one time series per location + parameter |

A few points deserve a closer look before you start:

- **Data quality flags mean different things for each product.** A SWOT flag describes one satellite observation. A USGS
  approval status says whether a person has reviewed the value yet. NWM output has no per-value flag at all, because it is
  a model: its quality depends on the model version and how well the basin is calibrated.
- **Units and reference points differ, so values don't compare directly.** NWM "streamflow" and USGS "discharge" are the same quantity, the volume of water passing per second, but NWM streamflow is in m³/s and USGS
  discharge in ft³/s (1 m³/s ≈ 35.31 ft³/s). SWOT water surface elevation is in meters above a global {term}`geoid <Geoid>`,
  while USGS {term}`gage height <Gage height>` is in feet above a local {term}`gage datum <Gage datum>`, so a SWOT elevation of
  120 m and a gage height of 20 ft can describe the same water surface. Module 4 returns to this when it compares the products.
- **"Reach" means different things.** A SWOT {term}`reach <Reach>` (about 10 km, from SWORD) and an NWM reach (an NHDPlus
  segment with a {term}`COMID`, often much shorter) come from two separate river networks. They don't match one to one.
- **Version / provenance is what makes your work repeatable.** Satellite products are reprocessed, models are upgraded and
  provisional observations are revised, so the same query can return different numbers next year. Writing down the version
  you used and the date you retrieved it is the first step toward the provenance record described in Module 1's
  [Publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data).

## How each page is organized

Every "Meet" page has the same sections, in the same order, so you can compare products side by side:

1. **Terminology:** the shared-concept table for that product.
2. **Dataset derivation:** how the values are produced, from raw radar returns, model physics or field measurements.
3. **Spatial coverage** and **Temporal coverage:** where and when data exist, and at what resolution.
4. **Data content:** the main variables, accuracy, known limitations, and an example of what the data look like.
5. **Usage and support:** how to cite the data, how to access it, how it changes over time, and whom to contact.
6. **Further reading.**

The pages are:

- [Meet NASA SWOT](01_meet_nasa_swot.md): river water surface elevation, width and slope measured from space.
- [Meet NOAA NWM](02_meet_noaa_nwm.md): modeled streamflow for every river reach in the National Water Model network.
- [Meet USGS WDFN](03_meet_usgs_wdfn.md): measured discharge and gage height at USGS monitoring locations.

## The course's example rivers

The example figures in this module all come from the **Ohio River at Louisville, Kentucky**, a large river where all
three products have good data. Module 3 uses the same river for its main examples and the **Willamette River at Salem,
Oregon** for its "Now you try it" exercises. Module 4 brings the products together for a flood on the
**Skagit River, Washington**, in December 2025.

:::{figure} ../images/m02/00_introduction-course-rivers-map.png
:alt: Map of the contiguous United States with three labeled points: USGS-12200500, Skagit River near Mount Vernon, Washington (Module 4 case study), in the far northwest; USGS-14191000, Willamette River at Salem, Oregon (Module 3 "Now you try it"), just south of it; and USGS-03294500, Ohio River at Louisville, Kentucky (Module 3 main example), in the east.
:width: 100%

Where the course's examples are. Points are the USGS monitoring locations used for each river. Locations: USGS Water Data
for the Nation monitoring-location records, accessed 2026-10-08. State outlines: U.S. Census Bureau 2023 cartographic
boundary file (1:20,000,000).
:::

:::{dropdown} How this map was made
This short script asks the USGS Water Data APIs for the coordinates of the three monitoring locations, using the
`dataretrieval` package, and plots them over U.S. state outlines from the
[U.S. Census Bureau cartographic boundary files](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html).
It runs in the course's `m03-wdfn` environment (`environments/m03-wdfn.yml`); you'll set that up in Module 3.

```python
import geopandas as gpd
import matplotlib.pyplot as plt
from dataretrieval import waterdata

# The three course example monitoring locations, with map labels
SITES = {
    "USGS-03294500": "Ohio River at Louisville, KY\n(Module 3 main example)",
    "USGS-14191000": "Willamette River at Salem, OR\n(Module 3 \"Now you try it\")",
    "USGS-12200500": "Skagit River near Mount Vernon, WA\n(Module 4 case study)",
}
# Coordinates come from each site's USGS monitoring-location record (a GeoDataFrame of points)
# md is a metadata object about the request, not used here
sites, md = waterdata.get_monitoring_locations(monitoring_location_id=list(SITES))

# U.S. state outlines: Census Bureau cartographic boundary file (1:20,000,000), contiguous states only
states = gpd.read_file("https://www2.census.gov/geo/tiger/GENZ2023/shp/cb_2023_us_state_20m.zip")
conus = states[~states["STUSPS"].isin(["AK", "HI", "PR"])]

# Plot in an equal-area projection (EPSG:5070, CONUS Albers)
crs = "EPSG:5070"
fig, ax = plt.subplots(figsize=(9, 5.2))
conus.to_crs(crs).plot(ax=ax, color="#f0efec", edgecolor="#b5b4ae", linewidth=0.5)
pts = sites.to_crs(crs)
pts.plot(ax=ax, color="#2a78d6", markersize=45, edgecolor="white", linewidth=1, zorder=3)
offsets = {"USGS-03294500": (8, -22), "USGS-14191000": (8, -18), "USGS-12200500": (8, 4)}
for _, row in pts.iterrows():
    sid = row["monitoring_location_id"]
    ax.annotate(f"{sid}\n{SITES[sid]}", (row.geometry.x, row.geometry.y),
                xytext=offsets[sid], textcoords="offset points", fontsize=8)
ax.set_axis_off()
fig.tight_layout()
fig.savefig("00_introduction-course-rivers-map.png", dpi=150)
```

`sites` is a GeoDataFrame with one row per monitoring location: its ID (`monitoring_location_id`), name and a point
`geometry` in longitude and latitude (WGS84). Without a USGS API key this works fine for three sites; Module 3 explains keys.
:::

## Where this leads

Module 3 turns each "Meet" page into code: one lesson per product, in the same NASA → NOAA → USGS order, showing how to
find and retrieve the data with each agency's recommended tools. Module 4 then compares the three products for a single
flood event, which is where the differences you read about here (measured vs. modeled, snapshot vs. continuous, reviewed
vs. provisional) start to matter.

:::{admonition} TODO (dev team): Learner-review friction items (P6.5.4)
:class: attention
From the integration-pass learner review (2026-10-09). Not yet fixed:
- Shared-concept table: label the SWOT flags by product, e.g. `reach_q` (RiverSP), `wse_qual` (Raster) (same in the glossary's "Data quality flag(s)" entry).
:::
