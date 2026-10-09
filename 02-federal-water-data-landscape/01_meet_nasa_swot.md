# Meet NASA SWOT

The *NASA Surface Water and Ocean Topography ({term}`SWOT`)* mission is a satellite jointly developed by NASA and Centre National D'Etudes Spatiales (CNES), with contributions from the Canadian Space Agency (CSA) and United Kingdom Space Agency (UKSA). Rather than measuring streamflow at fixed points, SWOT uses a Ka-band Radar Interferometer ({term}`KaRIn`) to make the first global survey of surface water — measuring the elevation, width, and slope of rivers, lakes, and reservoirs worldwide, which can then be used to estimate discharge. It exists to close major observation gaps: most of the world's rivers have no streamgage at all, and SWOT's stated requirement is to observe rivers 100 m wide and wider nearly everywhere on Earth (PO.DAAC staff have noted usable estimates as low as ~50 m in practice, though that's not the guaranteed spec). Learn more at the [SWOT resources page](https://www.earthdata.nasa.gov/data/platforms/space-based-platforms/swot/resources) and [NASA's SWOT mission page](https://science.nasa.gov/mission/swot/).

(swot-terminology)=
## Terminology

This table maps SWOT's own vocabulary onto the course's [shared concepts](00_introduction.md#m02-shared-concepts). It describes the river product most hydrology work uses, the River Single-Pass Vector product ({term}`RiverSP`).

| Shared concept | SWOT equivalent | Notes |
|---|---|---|
| {term}`Location identifier` | `reach_id` / `node_id` | Reported for {term}`reaches <Reach>` (~10 km river segments) and {term}`nodes <Node>` (~200 m spacing along a reach), both predefined in the SWOT River Database ({term}`SWORD`), a global river network built ahead of launch so repeat SWOT passes can be tied back to the same features over time. |
| {term}`Variable` | {term}`water surface elevation <Water surface elevation>` (WSE), width, slope, discharge | WSE, width, and slope are direct radar-derived measurements; discharge is a derived estimate (see [Dataset derivation](#swot-dataset-derivation)). |
| {term}`Variable unit` | meters (WSE, width), m/km (slope), m³/s (discharge) | WSE is reported as height above the {term}`geoid <Geoid>` (EGM2008), with the geoid height and tide corrections provided alongside (see the partner-review note below). |
| {term}`Time` | overpass time | The time the satellite observed that reach (UTC), for example `time_str` = `2025-01-09T11:18:10Z`. A location is seen a few times per 21-day {term}`cycle <Cycle and pass>`, not on a regular schedule. |
| {term}`Data quality flag(s)` | per-variable `*_qual`/`*_q` flags | SWOT products carry explicit quality flags attached to individual variables in each granule, e.g. overall reach quality is `reach_q`, water surface elevation quality is `wse_qual`. These are often bitwise-encoded integers representing combinations of underlying quality categories rather than a single pass/fail value (for example, the pixel-cloud product's `classification_qual` field packs 15 separate quality categories into combinable values, so you'll see more than 15 unique numbers in the data even though there are only 15 base categories). Don't guess at meaning from the number alone, check the {term}`product description document <Product description document (PDD)>` (PDD) for the specific product/version. |
| {term}`Version / provenance` | product version (e.g. `D`) and collection DOI | The version letter is part of each collection's short name, e.g. `SWOT_L2_HR_RiverSP_reach_D`. Version D of the RiverSP product has the {term}`DOI` [10.5067/SWOT-RIVERSP-D](https://doi.org/10.5067/SWOT-RIVERSP-D). |
| {term}`Data unit` | {term}`granule <Granule>` | One file for one stretch of one satellite pass. A RiverSP granule holds every reach (or node) observed in one pass over one continent; a Raster granule holds one scene. |

:::{admonition} Partner review (NASA): Vertical reference for water surface elevation
:class: important
An earlier draft said WSE "is referenced to the WGS84 ellipsoid and corrected for geoid height and solid Earth, load, and pole tides." In the Version D files used in Module 3, the Raster `wse` variable's `long_name` is "water surface elevation above geoid", and RiverSP provides `geoid_hght` alongside `wse`. Confirm that both RiverSP and Raster WSE are heights above the EGM2008 geoid, with tide corrections applied.
:::

(swot-dataset-derivation)=
## Dataset derivation

SWOT launched December 16, 2022, and does not measure streamflow directly — it derives WSE, width, and slope from raw radar returns collected as the satellite passes overhead, then aggregates lower-level pixel detections (the {term}`PIXC <Pixel cloud (PIXC)>` product) up to reach- and node-scale values using the predefined SWORD network. Discharge is a further derived product, available in both "unconstrained" (algorithm-only) and "gauge-constrained" (using historical gage records to calibrate the algorithm) versions, produced through a community workflow (SWOT-Confluence) run by the mission's Discharge Algorithm Working Group. Note that discharge maturity has evolved across releases: in the initial post-launch data releases, discharge fields in the river vector product were still placeholder/fill values while the algorithms were finalized, and became a standard reported output only in later versions — check the release notes for whichever version you're using to confirm discharge is actually populated, not just present as a column. (On 2026-10-08, `hydrocron` returned only fill values, `-999999999999`, for both discharge fields on the Ohio River reach in the figure below, for every 2025–2026 observation.)

The mission has two phases: a 1-day repeat "fast-sampling"/calibration orbit (Dec. 2022–July 2023), and the current 21-day repeat {term}`science orbit <Science orbit>` that began in mid-2023, which is what most hydrology use cases rely on. Product versions have also evolved (e.g., Beta Pre-Validated → Version C → Version D), moving from "pre-validated" toward fully validated status over time, so check the version and validation status of any dataset you're using; see the [SWOT documentation page](https://www.earthdata.nasa.gov/data/platforms/space-based-platforms/swot/resources) for release notes. Because a new version reprocesses old observations, the version is part of your data's provenance: record it, as Module 1's [Publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data) recommends.

:::{admonition} Partner review (NASA): Science-orbit start date
:class: important
This page has said the science phase began in August 2023, and the Module 3 SWOT lesson has said July 2023. Confirm the date the 21-day science orbit (and its data record) began, so both modules can state it.
:::

## Spatial coverage

- **Extent:** Global — SWOT surveys at least 90% of Earth's surface, observing most lakes, rivers, reservoirs, and the ocean at least once every 21 days
- **Type:** Vector (reach polylines and node points) for the hydrology river product (RiverSP), distributed as shapefiles; a separate gridded product, the {term}`Raster <SWOT Raster product>` product (`SWOT_L2_HR_Raster_100m_D` and `_250m_D`), gives water surface elevation (`wse`), water area (`water_area`) and water fraction (`water_frac`) on 100 m and 250 m UTM grids. The Module 3 lesson [Retrieve NASA SWOT data](../03-federal-water-data-access-retrieval/01_access_nasa_swot.md) shows when to use each.
- **Resolution:** Reaches are ~10 km long; nodes are spaced ~200 m apart; SWORD (the underlying river network) targets rivers roughly 30 m wide and greater, though the operational river product effectively resolves rivers around 50-100m and wider
- **{term}`CRS`:** Vector product coordinates are geographic (latitude/longitude); Raster scenes are on UTM grids. Elevations are heights above the geoid (see [Terminology](#swot-terminology)).
- **Coverage caveat:** A seasonal mask removes part of the Canadian Arctic Archipelago from collection each year (roughly December 1–March 1), so the satellite can prioritize sea ice observation there instead — worth knowing if your training touches high-latitude basins

## Temporal coverage

- **Period of record:** Science-orbit data (the 21-day repeat orbit most hydrology applications use) begin in mid-2023 and are ongoing; the mission is currently in extended operations, so check the [SWOT mission page](https://science.nasa.gov/mission/swot/) for current status
- **Frequency/resolution:** Each location is revisited on a 21-day repeat cycle during the science phase; many locations are seen more often because neighboring swaths overlap. The Ohio River reach in the figure below sits under four passes and was observed 118 times between January 2025 and October 2026, a median of about 9 days apart. The earlier 1-day repeat calibration phase (Dec. 2022–July 2023) is also available but was designed for instrument validation, not routine monitoring
- **Update cadence:** Data are released per-granule (one satellite pass over one or more continents) as they're processed — not a fixed daily/hourly push like a hydrologic model

## Data content

- **Primary variables:** water surface elevation, width, slope, area, and both unconstrained and gauge-constrained discharge estimates, at both reach and node scale
- **Accuracy:** SWOT's commonly cited target is ~10 cm vertical (WSE) precision, though this is a mission-level target rather than a per-observation guarantee — actual performance varies by river width, roughness, and other local factors, and PO.DAAC staff have pointed users to the product description documents (PDDs) rather than a single number for rigorous accuracy claims
- **Related products not covered here:** SWOT also produces lake (`LakeSP`) and ocean/sea-surface height products, plus lower-level pixel-cloud (`PIXC`) data that the river product is built from
- **Known limitations:** Complex or braided river geometries (multiple channels) are not well represented by the standard reach/node product, since SWORD reaches assume a single centerline. Quality flags are attached per-variable (not a single blanket flag), so a location can have good WSE but a flagged discharge value, or vice versa, so always check the specific flag for the variable you're using, not just whether the reach "has data." Summary flags are also reach-specific: at some reaches *no* observation is flagged good (`reach_q` = 0), so a strict filter can remove every value. Look at the flag distribution for your reach before choosing a threshold.

**What the data look like.** Each dot below is one SWOT observation of one reach of the Ohio River at Louisville, Kentucky: a single overpass, reduced to a single water surface elevation for the ~10 km reach. Notice three things: the observations are irregular in time (several per cycle, sometimes two within a day from neighboring passes); the river's rises, such as the April 2025 flood, show up as jumps of several meters; and no observation is flagged good (`reach_q` = 0). Almost all are `reach_q` = 1 ("suspect"), the best this reach gets.

:::{figure} ../images/m02/01_meet_nasa_swot-ohio-reach-wse.png
:alt: Scatter plot of SWOT water surface elevation for reach 74267300251 from January 2025 to September 2026. Most points lie between 119 and 124 meters, with high values near 131 meters in February and April 2025. 114 points are blue (reach_q = 1, suspect) and 4 are orange squares (reach_q = 2, degraded); none are flagged good.
:width: 100%

SWOT water surface elevation for SWORD reach `74267300251`, Ohio River at Louisville, KY, colored by the reach quality flag `reach_q`. 118 observations, 2025-01-01 to 2026-10-01. Data: SWOT Level 2 River Single-Pass Vector Reach product, Version D ([doi:10.5067/SWOT-RIVERSP-D](https://doi.org/10.5067/SWOT-RIVERSP-D)), retrieved with PO.DAAC `hydrocron`, accessed 2026-10-08.
:::

:::{dropdown} How this figure was made
This script asks PO.DAAC's [`hydrocron` API](https://podaac.github.io/hydrocron/) for every observation of one reach in a date range, as CSV, and plots it. `hydrocron` needs no login. The query (reach ID, dates and fields) is kept in variables at the top so you can see exactly what was asked for. It runs in the course's `m03-swot` environment (`environments/m03-swot.yml`); Module 3 covers `hydrocron` in detail.

```python
import io
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Record the query in one place: reach, dates, fields
REACH_ID = "74267300251"          # SWORD reach on the Ohio River at Louisville, KY
START, END = "2025-01-01T00:00:00Z", "2026-10-01T00:00:00Z"

params = {
    "feature": "Reach", "feature_id": REACH_ID,
    "start_time": START, "end_time": END,
    "output": "csv", "fields": "reach_id,time_str,wse,width,reach_q",
}
resp = requests.get("https://soto.podaac.earthdatacloud.nasa.gov/hydrocron/v1/timeseries",
                    params=params, timeout=60)
resp.raise_for_status()
# The CSV text sits inside the JSON response
df = pd.read_csv(io.StringIO(resp.json()["results"]["csv"]))

# Drop rows with no valid observation ("no_data" times, fill values)
df = df[df["time_str"] != "no_data"].copy()
df["time"] = pd.to_datetime(df["time_str"])
df = df[df["wse"] > -1e9]

# One marker style per quality-flag value
fig, ax = plt.subplots(figsize=(9, 3.6))
labels = {0: "0 (good)", 1: "1 (suspect)", 2: "2 (degraded)", 3: "3 (bad)"}
styles = {0: ("#1baf7a", "o"), 1: ("#2a78d6", "o"), 2: ("#eb6834", "s"), 3: ("#e34948", "x")}
for q, grp in df.groupby("reach_q"):
    color, marker = styles[q]
    ax.scatter(grp["time"], grp["wse"], s=22, color=color, marker=marker, label=f"reach_q = {labels[q]}")
ax.set_ylabel("Water surface elevation (m)")
ax.set_title("SWOT reach 74267300251, Ohio River at Louisville, KY", loc="left", fontsize=11)
ax.grid(alpha=0.3)
ax.legend(frameon=False, fontsize=9, loc="upper right")
fig.tight_layout()
fig.savefig("01_meet_nasa_swot-ohio-reach-wse.png", dpi=150)
```

`df` has one row per overpass: `reach_id`, `time_str` (UTC), `wse` (m), `width` (m) and `reach_q` (0 good, 1 suspect, 2 degraded, 3 bad), plus a units column for each variable (`wse_units`, `width_units`). `hydrocron` reports missing values with the fill value `-999999999999`, which is why the code drops very negative `wse`.
:::

## Usage and support

- **Citation:** NASA/PO.DAAC recommends citing SWOT products by DOI, e.g. for the River Single-Pass Vector product: *SWOT (2025). SWOT Level 2 River Single-Pass Vector Data Product, Version D [Dataset]. NASA Physical Oceanography Distributed Active Archive Center.* https://doi.org/10.5067/SWOT-RIVERSP-D Cite the specific product DOI and version you used, plus access date, following NASA's [Data Use Guidance](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance). Each collection's PO.DAAC landing page (reached through its DOI) gives the recommended citation. Module 1's [Data Publishing](../01-data-best-practices/03_data_publishing.md) page explains why DOIs make your work findable and reusable.
- **License/access:** Open data, but most SWOT collections require a free NASA Earthdata Login to download. Data lives in the NASA Earthdata Cloud (hosted on AWS) and is distributed through {term}`PO.DAAC` — accessible via the `podaac-data-downloader`/`podaac-data-subscriber` command-line tools, the [`earthaccess`](https://earthaccess.readthedocs.io/en/latest/) Python library (PO.DAAC's own staff describe it as their preferred way to authenticate and search/download any NASA Earthdata, not just SWOT), a GUI tool called HiTIDE for browsing and subsetting the ocean/KaRIn products, or the [Hydrocron API](https://podaac.github.io/tutorials/quarto_text/SWOT.html), which repackages the per-pass river and lake shapefiles into CSV/GeoJSON time series so you don't have to stitch together potentially thousands of individual granules yourself (check the [`hydrocron` documentation](https://podaac.github.io/hydrocron/) for which product versions and features it currently serves before building a workflow around it). For custom-resolution raster output beyond the standard 100 m/250 m products, PO.DAAC also offers an on-demand tool called SWODLR. The Module 3 lesson [Retrieve NASA SWOT data](../03-federal-water-data-access-retrieval/01_access_nasa_swot.md) shows when to use {term}`earthaccess` and when to use {term}`hydrocron`.
- **Change over time:** Product version upgrades (not just new observations) can change values for the same reach/node — treat multi-version time series as non-homogeneous. Record the collection short name (which includes the version letter) and your access date with every download, so you or someone else can re-run your analysis against the same version later.
- **Contact:** For questions about SWOT data content or quality, contact PO.DAAC at podaac@podaac.jpl.nasa.gov, or post in the [Earthdata Forum](https://forum.earthdata.nasa.gov/).

## Further reading

- [SWOT Documentation and Resources (NASA Earthdata)](https://www.earthdata.nasa.gov/data/platforms/space-based-platforms/swot/resources)
- [NASA SWOT mission page](https://science.nasa.gov/mission/swot/)
- [PO.DAAC SWOT Cookbook (tutorials, data access via `earthaccess` quality flag demo, Hydrocron walkthrough)](https://podaac.github.io/tutorials/quarto_text/SWOT.html)
- [`hydrocron` documentation (PO.DAAC)](https://podaac.github.io/hydrocron/)
- [`earthaccess` documentation](https://earthaccess.readthedocs.io/en/latest/)
- [SWOT Level 2 River Single-Pass Vector Data Product, Version D](https://doi.org/10.5067/SWOT-RIVERSP-D) (dataset landing page)
- [SWOT River Database (SWORD)](https://zenodo.org/records/10013982)
- [NASA Data Use Guidance](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance), including how to cite data
