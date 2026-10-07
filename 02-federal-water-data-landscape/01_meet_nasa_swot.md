# Meet NASA SWOT

| Location Identifier | Variable | Variable unit | Time / resolution | Data Quality Flag(s) |
|---|---|---|---|---|
| `reach_id` / `node_id` (defined by the SWOT River Database, SWORD) | water surface elevation (WSE), width, slope, discharge | WSE: meters; width: meters; slope: m/km; discharge: m³/s | 21-day repeat orbit (science phase); reaches ~10 km long, nodes ~200 m spacing | Per-variable quality flags (e.g. `reach_q`, `node_q`, and variable-specific `*_qual` flags) — see [quality flag guidance](#data-content) |

The Surface Water and Ocean Topography (SWOT) mission is a satellite jointly developed by NASA and Centre National D'Etudes Spatiales (CNES), with contributions from the Canadian Space Agency (CSA) and United Kingdom Space Agency (UKSA). Rather than measuring streamflow at fixed points, SWOT uses a Ka-band Radar Interferometer (KaRIn) to make the first global survey of surface water — measuring the elevation, width, and slope of rivers, lakes, and reservoirs worldwide, which can then be used to estimate discharge. It exists to close major observation gaps: most of the world's rivers have no streamgage at all, and SWOT's stated requirement is to observe rivers 100 m wide and wider nearly everywhere on Earth (PO.DAAC staff have noted usable estimates as low as ~50 m in practice, though that's not the guaranteed spec). Learn more at the [SWOT resources page](https://www.earthdata.nasa.gov/data/platforms/space-based-platforms/swot/resources) and [NASA's SWOT mission page](https://science.nasa.gov/mission/swot/).


## Terminology

- **Location Identifier → `reach_id` / `node_id`**: SWOT river measurements are reported for reaches (~10 km river segments) and nodes (~200 m spacing along a reach), both predefined in the **SWOT River Database (SWORD)** — a global river network built ahead of launch so that repeat SWOT passes can be tied back to the same features over time.
- **River variable → water surface elevation (WSE), width, slope, discharge**: WSE, width, and slope are direct radar-derived measurements; discharge is a derived estimate (see Data content below).
- **River variable unit → meters (WSE, width), m/km (slope), m³/s (discharge)**: WSE is referenced to the WGS84 ellipsoid and corrected for geoid height and solid Earth, load, and pole tides.
- **Data Quality Flag(s) → per-variable `*_qual`/`*_q` flags**: SWOT products carry explicit quality flags attached to individual variables in each granule — e.g. overall reach quality is `reach_q`, water surface elevation quality is `wse_qual`. These are often bitwise-encoded integers representing combinations of underlying quality categories rather than a single pass/fail value (for example, the pixel-cloud product's `classification_qual` field packs 15 separate quality categories into combinable values, so you'll see more than 15 unique numbers in the data even though there are only 15 base categories). Don't guess at meaning from the number alone — check the product description document (PDD) for the specific product/version.

| Shared term | SWOT equivalent | Notes |
|---|---|---|
| Location Identifier | `reach_id` / `node_id` | Reported for reaches (~10 km river segments) and nodes (~200 m spacing along a reach), both predefined in the SWOT River Database (SWORD), a global river network built ahead of launch so repeat SWOT passes can be tied back to the same features over time.
| Variable | water surface elevation (WSE), width, slope, discharge | WSE, width, and slope are direct radar-derived measurements; discharge is a derived estimate (see Data content below). |
| Variable unit | meters (WSE, width), m/km (slope), m³/s (discharge) | WSE is referenced to the WGS84 ellipsoid and corrected for geoid height and solid Earth, load, and pole tides. |
| Data Quality Flag(s) | per-variable `*_qual`/`*_q` flags | SWOT products carry explicit quality flags attached to individual variables in each granule, e.g. overall reach quality is `reach_q`, water surface elevation quality is `wse_qual`. These are often bitwise-encoded integers representing combinations of underlying quality categories rather than a single pass/fail value (for example, the pixel-cloud product's `classification_qual` field packs 15 separate quality categories into combinable values, so you'll see more than 15 unique numbers in the data even though there are only 15 base categories). Don't guess at meaning from the number alone, check the product description document (PDD) for the specific product/version. |

## Dataset derivation

SWOT launched December 16, 2022, and does not measure streamflow directly — it derives WSE, width, and slope from raw radar returns collected as the satellite passes overhead, then aggregates lower-level pixel detections (the `PIXC` product) up to reach- and node-scale values using the predefined SWORD network. Discharge is a further derived product, available in both "unconstrained" (algorithm-only) and "gauge-constrained" (using historical gage records to calibrate the algorithm) versions, produced through a community workflow (SWOT-Confluence) run by the mission's Discharge Algorithm Working Group. Note that discharge maturity has evolved across releases: in the initial post-launch data releases, discharge fields in the river vector product were still placeholder/fill values while the algorithms were finalized, and became a standard reported output only in later versions — check the release notes for whichever version you're using to confirm discharge is actually populated, not just present as a column. The mission has two phases: a 1-day repeat "fast-sampling"/calibration orbit (Dec. 2022–July 2023), and the current 21-day repeat "science phase" orbit that began in August 2023, which is what most hydrology use cases rely on. Product versions have also evolved (e.g., Beta Pre-Validated → Version C → Version D), moving from "pre-validated" toward fully validated status over time, so check the version and validation status of any dataset you're using; see the [SWOT documentation page](https://www.earthdata.nasa.gov/data/platforms/space-based-platforms/swot/resources) for release notes.

## Spatial coverage

- **Extent:** Global — SWOT surveys at least 90% of Earth's surface, observing most lakes, rivers, reservoirs, and the ocean at least once every 21 days
- **Type:** Vector (reach polylines and node points) for the hydrology river product, distributed as shapefiles (also available as NetCDF); a separate raster product exists for water surface extent
- **Resolution:** Reaches are ~10 km long; nodes are spaced ~200 m apart; SWORD (the underlying river network) targets rivers roughly 30 m wide and greater, though the operational river product effectively resolves rivers around 50-100m and wider
- **CRS:** Vector product coordinates are geographic (latitude/longitude), with elevations referenced to the WGS84 ellipsoid
- **Coverage caveat:** A seasonal mask removes part of the Canadian Arctic Archipelago from collection each year (roughly December 1–March 1), so the satellite can prioritize sea ice observation there instead — worth knowing if your training touches high-latitude basins
## Temporal coverage

- **Period of record:** Science-phase data (the 21-day repeat orbit most hydrology applications use) begins August 2023 and is ongoing; the mission is currently in extended operations, so check the [SWOT mission page](https://science.nasa.gov/mission/swot/) for current status
- **Frequency/resolution:** Each location is revisited on a 21-day repeat cycle during the science phase (some locations more often due to swath overlap); the earlier 1-day repeat calibration phase (Dec. 2022–July 2023) is also available but was designed for instrument validation, not routine monitoring
- **Update cadence:** Data are released per-granule (one satellite pass over one or more continents) as they're processed — not a fixed daily/hourly push like a hydrologic model

## Data content

- **Primary variables:** water surface elevation, width, slope, area, and both unconstrained and gauge-constrained discharge estimates, at both reach and node scale
- **Accuracy:** SWOT's commonly cited target is ~10 cm vertical (WSE) precision, though this is a mission-level target rather than a per-observation guarantee — actual performance varies by river width, roughness, and other local factors, and PO.DAAC staff have pointed users to the product description documents (PDDs) rather than a single number for rigorous accuracy claims
- **Related products not covered here:** SWOT also produces lake (`LakeSP`) and ocean/sea-surface height products, plus lower-level pixel-cloud (`PIXC`) data that the river product is built from
- **Known limitations:** Complex or braided river geometries (multiple channels) are not well represented by the standard reach/node product, since SWORD reaches assume a single centerline. Quality flags are attached per-variable (not a single blanket flag), so a location can have good WSE but a flagged discharge value, or vice versa, so always check the specific flag for the variable you're using, not just whether the reach "has data."

## Usage and support

- **Citation:** NASA/PO.DAAC recommends citing SWOT products by DOI, e.g. for the River Single-Pass Vector product: *SWOT (2025). SWOT Level 2 River Single-Pass Vector Data Product [Dataset]. NASA Physical Oceanography Distributed Active Archive Center.* Cite the specific product DOI and version you used, plus access date, following [EOSDIS Data Use and Citation Guidance](https://www.earthdata.nasa.gov/data/platforms/space-based-platforms/swot/resources).
- **License/access:** Open data, but most SWOT collections require a free NASA Earthdata Login to download. Data lives in the NASA Earthdata Cloud (hosted on AWS) and is distributed through PO.DAAC — accessible via the `podaac-data-downloader`/`podaac-data-subscriber` command-line tools, the [`earthaccess`](https://earthaccess.readthedocs.io/en/latest/) Python library (PO.DAAC's own staff describe it as their preferred way to authenticate and search/download any NASA Earthdata, not just SWOT), a GUI tool called HiTIDE for browsing and subsetting the ocean/KaRIn products, or the [Hydrocron API](https://podaac.github.io/tutorials/quarto_text/SWOT.html), which repackages the per-pass river and lake shapefiles into CSV/GeoJSON time series so you don't have to stitch together potentially thousands of individual granules yourself (Hydrocron was still in development as of PO.DAAC's 2024 webinar on SWOT access, so double-check current reach/lake coverage before building a workflow around it). For custom-resolution raster output beyond the standard 100 m/250 m products, PO.DAAC also offers an on-demand tool called SWODLR.
- **Change over time:** Product version upgrades (not just new observations) can change values for the same reach/node — treat multi-version time series as non-homogeneous.
- **Contact:** For questions about SWOT data content or quality, contact PO.DAAC at podaac@podaac.jpl.nasa.gov, or post in the [Earthdata Forum](https://www.earthdata.nasa.gov/data/platforms/space-based-platforms/swot/resources).

## Further reading

- [SWOT Documentation and Resources (NASA Earthdata)](https://www.earthdata.nasa.gov/data/platforms/space-based-platforms/swot/resources)
- [PO.DAAC SWOT Cookbook (tutorials, data access via `earthaccess` quality flag demo, Hydrocron walkthrough)](https://podaac.github.io/tutorials/quarto_text/SWOT.html)
- [SWOT River Database (SWORD)](https://zenodo.org/records/10013982)