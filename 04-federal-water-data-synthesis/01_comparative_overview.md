# Comparative overview of Federal data products

In this lesson, we will compare and contrast the three Federal data products using helpful data dimensions, including data accuracy, temporal availability, and spatial coverage. We will wrap up this lesson with a section describing the best applications and uses for each of the data products. Understanding the similarities and differences can help you design research to appropriately leverage or adapt to existing data products.

## Spatial coverage

The three Federal datasets used in this course are built from very different spatial models: a satellite that sees rivers wherever it passes, a model that covers every reach of a national stream network, and gages at fixed points. They are described below in the course's agency order (NASA, NOAA, USGS); the {term}`location identifier <Location identifier>` each one uses is part of that spatial model.

* **NASA Surface Water and Ocean Topography ({term}`SWOT`) water surface elevation** data are derived from a remotely-sensed raster of water extent. In their more raw form, these data are not spatially limited and can exist for every pixel across the globe. In the hydrology-linked data product `L2_HR_RiverSP`, the data are mapped to ~10 km river {term}`reaches <Reach>` defined in the SWOT River Database ({term}`SWORD`) and are available for rivers globally. Module 2 describes the river product as effectively resolving rivers roughly 50–100 m wide and wider.

  :::{admonition} TODO (dev team): SWOT minimum river width
  :class: attention
  Verify: Module 2 says the river product effectively resolves rivers about 50–100 m and wider, and SWORD targets ~30 m.
  :::

* **NOAA National Water Model ({term}`NWM`) streamflow** data are available for every river reach in the model's stream network, which is built on the National Hydrography Dataset ({term}`NHDPlus`): over 2.7 million reaches in the contiguous United States, plus separate domains for southern Alaska, Hawaii, Puerto Rico and the U.S. Virgin Islands ([NOAA OWP](https://water.noaa.gov/about/nwm)). Each reach has one value per time step, identified by its {term}`feature_id` (the NHDPlus {term}`COMID`). Because the NWM is a model, it has values for ungaged headwater streams as well as large rivers. That spatial completeness is its main strength, but values in ungaged, heavily regulated or poorly calibrated basins deserve extra caution (see Module 2).
* **USGS Water Data for the Nation ({term}`WDFN`) streamflow** data are available at discrete points along the river network, each identified by a {term}`monitoring location ID <Monitoring location ID>`. These data represent observed measurements from sensors in the streams themselves, and are collected at a limited number of locations in the contiguous United States, Alaska, Hawaii, and US territories. Streams with streamflow data in WDFN vary greatly in size, from intermittent and ephemeral streams to the mouth of the Mississippi. Some locations are also in coastal zones, where tides can impact streamflow data.

## Temporal availability

Much like their spatial coverage, the three data products also represent vastly different temporal landscapes. Below they are described in order of the most limited timeseries and shortest period of record to the most temporally robust.

* **NASA SWOT water surface elevation** data are only available when the SWOT satellite passes over the location of interest. Data are collected continuously across the globe, but at any one location they are limited by the satellite's orbit, which repeats every 21 days. A location can fall under more than one swath in each 21-day cycle (higher latitudes more often), and `hydrocron` and RiverSP return **one record per overpass**, not one per cycle. In the Module 4 case study, the lowest Skagit reaches were each observed four or five times in December 2025 (SWOT RiverSP via `hydrocron`, accessed 2026-10-08). Science-orbit time series begin in 2023.

  :::{admonition} TODO (dev team): Start of SWOT science-orbit records
  :class: attention
  Confirm the start date to give here: Module 3 says the science orbit began in July 2023; this page previously said August 2023.
  :::

* **NOAA NWM streamflow** data are produced continuously, as several _configurations_ that each answer a different question ([NOAA OWP](https://water.noaa.gov/about/nwm)):
  * an **analysis** of current conditions, updated through the day;
  * **short-range** forecasts out to 18 hours, issued every hour (CONUS);
  * **medium-range** forecasts out to 8.5–10 days, issued four times per day;
  * **long-range** ensemble forecasts out to 30 days.

  Operational forecasts have run since August 2016. A separate **retrospective** simulation re-runs the model over historical weather back to 1979, which makes it the main source of long, reach-level streamflow records where there is no gage (Module 2). Many distribution channels keep only recent runs: the no-key NOAA NWM API keeps only about the last 3–5 days ([Retrieve NOAA NWM data](../03-federal-water-data-access-retrieval/02_access_noaa_nwm.md)), and Module 2 notes that NOAA's NOMADS server keeps a 48-hour rolling window. Past forecasts, like the December 2025 forecasts used in this module, come from the public cloud archives on Google Cloud (`national-water-model`) and AWS ([`noaa-nwm-pds`](https://registry.opendata.aws/noaa-nwm-pds/)).

* **USGS WDFN streamflow** is published in near real time, as {term}`provisional <Provisional data>` values. At currently active gages, data are collected every 15 minutes from sensors located at each streamgage. Under normal operational status, data are pushed up from the gages to NWIS (the USGS database whose data WDFN publishes) at least every 6 hours. {term}`Continuous values <Continuous values>` (typically every 15 minutes) start on different dates at each site: Module 2 gives the earliest as October 1950, and at USGS 12200500 continuous discharge starts in 1988. Check a site's record with the time-series metadata shown in [Retrieve USGS WDFN data](../03-federal-water-data-access-retrieval/03_access_usgs_wdfn.md). Continuous values are also rolled up to _daily_ values (most commonly a _mean daily_ value). Daily records are available back to when the USGS streamgaging program began in 1889. Because the data arrive in near real time, these in-situ sensors are subject to unexpected monitoring challenges (e.g. equipment malfunctions, critter invasions, biofouling, etc) and while mitigated, data gaps are present in the records.

  :::{admonition} TODO (dev team): Start of USGS continuous records
  :class: attention
  Verify: the time-series metadata for 12200500 lists continuous discharge from 1988, and Module 2 says instantaneous data go back to October 1, 1950.
  :::

## Accuracy

The three products are very different kinds of data: an observation from space (NASA SWOT), a model (NOAA NWM) and an in-stream observation (USGS). Each agency describes accuracy in its own terms, so rather than ranking them, this section summarizes what each says about its product and what that means for a researcher.

**NASA SWOT water surface elevation** comes with a per-observation uncertainty (`wse_u`, in meters) and with summary and bitwise {term}`data quality flags <Data quality flag(s)>` (`reach_q`, `node_q`, `*_qual`). The mission's commonly cited goal of about 10 cm precision for water surface elevation is a mission-level target, not a guarantee for every reach and overpass (Module 2). Performance varies with river width, roughness and other local factors; the product description documents give the details (Module 2). On the lower Skagit, 14 of the 18 December 2025 reach observations are flagged degraded (`reach_q` = 2) and none good, and one overpass reads about 12 m higher than on December 1 while the gage had barely changed (SWOT RiverSP via `hydrocron`; see the case study in the next lesson). Always check `wse_u` and the quality flags, and compare with an independent source where you can.

:::{admonition} Partner review (NASA): Accuracy
:class: important
Confirm the precision-target wording and the main factors that affect WSE accuracy.
:::

**NOAA NWM streamflow** has no per-value quality flag. Its accuracy depends on the configuration, the weather forcing (especially forecast precipitation), how well the basin is calibrated, and the model version (Module 2). USGS and U.S. Army Corps of Engineers observations are assimilated into several of the analysis configurations; the others run without observations ([NOAA OWP](https://water.noaa.gov/about/nwm)). Forecast skill falls as lead time grows. The practical way to judge NWM accuracy for your question is to compare past forecasts with USGS observations for similar events, which is what the [Module 4 case study](02_synthesize_river_data.md) does for the Skagit.

:::{admonition} Partner review (NOAA): Accuracy
:class: important
Confirm this summary of NWM error sources and of how observations are assimilated.
:::

**USGS WDFN streamflow** is the reference most researchers compare against, but discharge is not measured directly. The sensor records gage height, and discharge is computed from it with a {term}`rating curve <Rating curve>` fitted to periodic field measurements of discharge (Module 2). Accuracy therefore depends on how well the rating is defined at the flow you care about. During floods the river can go out of bank, the channel can scour or fill, and field measurements are hard and dangerous to make. The top of the rating curve often rests on only a few measurements, so peak discharges are usually more uncertain than typical flows ([USGS: How streamflow is measured](https://www.usgs.gov/water-science-school/science/how-streamflow-measured)). Each field measurement carries the hydrographer's own accuracy rating. At USGS 12200500, the measurement of 111,000 ft³/s on December 12, 2025, about nine hours after the crest, was rated "Fair", compared with "Good" for a calmer November measurement (USGS field measurements from the [Water Data API](https://api.waterdata.usgs.gov/ogcapi/v0/); see the case study in the next lesson). Module 3 shows how to retrieve field measurements and their ratings. Values are {term}`provisional <Provisional data>`, and can be revised, until USGS approves them ([USGS provisional data statement](https://waterdata.usgs.gov/provisional-data-statement/)).

:::{admonition} Partner review (USGS): Accuracy
:class: important
Confirm the description of rating-curve uncertainty at high flows, and what the field-measurement ratings (e.g. Good, Fair) represent in percent terms.
:::

:::{admonition} TODO (dev team): Rating-curve uncertainty citation
:class: attention
Cite USGS rating-curve guidance for high-flow uncertainty.
:::

## Side-by-side comparison

The table lines the three products up using the course's seven shared concepts (the first seven rows, in the same order as every Module 2 and Module 3 lesson), then adds coverage, latency, strengths and cautions. Each shared-concept name links to its Glossary entry.

| | NASA SWOT (RiverSP) | NOAA NWM | USGS WDFN |
|---|---|---|---|
| What it is | Satellite observation | Hydrologic model (analysis and forecasts) | In-stream observation |
| {term}`Location identifier` | `reach_id` / `node_id` (SWORD) | `feature_id` (NHDPlus COMID) | monitoring location ID, `monitoring_location_id` (e.g. `USGS-12200500`) |
| {term}`Variable` (rivers) | Water surface elevation, width, slope; derived discharge | Streamflow (plus land-surface variables) | Discharge (`00060`), gage height (`00065`) |
| {term}`Variable unit` | m (WSE, width), m/km (slope), m³/s (discharge) | m³/s | ft³/s (discharge), ft (gage height) |
| {term}`Time` | Overpass time (UTC) | Forecast reference time and valid time (UTC) | Timestamp: continuous (typically 15-minute) or daily |
| {term}`Data quality flag(s)` | `reach_q` / `node_q`, bitwise flags, `wse_u` uncertainty | None per value; depends on configuration and model version | `approval_status`, `qualifier`; `measurement_rated` for field measurements |
| {term}`Version / provenance` | Product version (e.g. `D`) and collection DOI | Model version (e.g. `v3.0`) and configuration | Service, approval status and retrieval date |
| {term}`Data unit` | Granule (one pass over one area); `hydrocron` returns one row per reach per overpass | One output file per time step, covering every reach | One time series per monitoring location and parameter |
| Spatial coverage | Global rivers roughly 50–100 m wide and wider | Every NHDPlus reach (2.7M+), CONUS plus AK, HI, PR/USVI | About 9,000 stream gages with discharge |
| Temporal coverage | An overpass every few days to 21 days, since 2023 | Hourly to 6-hourly; forecasts since 2016, retrospective since 1979 | Typically 15-minute; daily records back to 1889 at the oldest sites |
| Typical latency | Days after an overpass | About 1–2 hours after each cycle | Minutes to hours (provisional) |
| Main strength | Sees rivers anywhere, and floodplain water (Raster) | Complete network; forecasts | Highest-quality local record |
| Main caution | Sparse in time; quality varies by reach and pass | Model error; no per-value flag | Point locations only; ratings uncertain at extreme flows |

The version / provenance row is the one most often left out of a methods section, and the one that most affects whether someone can reproduce your result: name the SWOT product version, the NWM model version and configuration, and the USGS approval status and access date for every dataset you use (Module 1, [publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data)).

:::{admonition} TODO (dev team): RiverSP latency
:class: attention
Verify RiverSP latency.
:::

Sources: Module 2 agency pages, [NOAA OWP](https://water.noaa.gov/about/nwm), and the Module 3 lessons.

## Which product for which question?

The comparison above comes down to matching a product to your research question. A starting point (not agency guidance; check each agency's recommendations below):

| If your question needs... | Start with | Why |
|---|---|---|
| Water surface elevation, width or slope along a river, including ungaged rivers | NASA SWOT RiverSP | Reach-by-reach measurements along whole rivers, globally |
| Where the water was (extent, inundation) on a given day | NASA SWOT Raster | Gridded water fraction and area across the swath, when a pass lines up with your date |
| Streamflow on an ungaged reach, or a long simulated record there | NOAA NWM retrospective | Every NHDPlus reach, back to 1979 |
| What was expected to happen (forecasts), or how a forecast changed with lead time | NOAA NWM forecasts | Short-, medium- and long-range forecasts on every reach |
| The best record of flow or stage at a specific site, or a long record | USGS WDFN continuous and daily values | Measured, quality-reviewed, often decades long |
| How much to trust a flood peak | USGS WDFN field measurements, with the rating | Shows how far the peak is from direct measurement |

Most real questions need more than one row, which is what the [case study](02_synthesize_river_data.md) shows.

## Data provider recommendations

Each agency publishes guidance on how its data should and should not be used. The recommendations below are drafted from those sources, each one linked to its source, and are waiting for confirmation from the agencies.

### NASA (SWOT)

- **Use the programmatic tools PO.DAAC documents.** PO.DAAC lists `earthaccess` for searching and downloading SWOT granules, and its `hydrocron` API for river and lake time series in CSV or GeoJSON ([PO.DAAC SWOT Cookbook](https://podaac.github.io/tutorials/quarto_text/SWOT.html); [Hydrocron documentation](https://podaac.github.io/hydrocron/)).
- **Know which product version you are using, and don't mix versions without checking.** Version D supersedes Version C (`2.0`), and some reach and node IDs differ between them ([Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf); [Hydrocron versioning](https://podaac.github.io/hydrocron/)).
- **Use the quality flags and uncertainties for your application.** Check `reach_q` / `node_q` and the per-variable `*_qual` flags and `wse_u` rather than treating every value as equally reliable. The PO.DAAC Cookbook links a general quality-flag tutorial ([PO.DAAC SWOT Cookbook](https://podaac.github.io/tutorials/quarto_text/SWOT.html)).

  :::{admonition} Partner review (NASA): NASA (SWOT)
  :class: important
  Is there an official recommended filter for research use, and how should users treat "degraded" (`reach_q` = 2) observations?
  :::

- **Ask for a `hydrocron` API key for heavy use.** Keys are optional, but PO.DAAC asks heavy or recurring users to request one ([Hydrocron timeseries docs](https://podaac.github.io/hydrocron/timeseries)).

:::{admonition} Partner review (NASA): NASA (SWOT)
:class: important
- Confirm this recommendation: *Use the programmatic tools PO.DAAC documents.*
- Confirm this recommendation: *Know which product version you are using, and don't mix versions without checking.*
- Confirm this recommendation: *Ask for a `hydrocron` API key for heavy use.*
:::

### NOAA (National Water Model)

- **Treat NWM output as guidance, not the official forecast.** The NWM "complements official NWS river forecasts at approximately 4000 locations" ([NOAA OWP](https://water.noaa.gov/about/nwm)). For decisions at a forecast point, the official NWS river forecast is the authoritative source.
- **Expect the data format to change between model versions.** NCEP encourages users to make sure their decoders are flexible, because output elements "may change with future NCEP model implementations" ([NOAA OWP](https://water.noaa.gov/about/nwm)). Record the model version with any NWM data you use.
- **Cite the specific product and access date.** Cite the configuration you used from the [Registry of Open Data on AWS](https://registry.opendata.aws/noaa-nwm-pds/) listing (see Module 2).

:::{admonition} Partner review (NOAA): NOAA (National Water Model)
:class: important
- Confirm this recommendation: *Treat NWM output as guidance, not the official forecast.*
- Confirm this recommendation: *Expect the data format to change between model versions.*
- Confirm this recommendation: *Cite the specific product and access date.*
:::

_Course note (not agency guidance):_ NWM output can be reached several ways, and they differ a lot in cost as your question grows. Module 3's NWM lesson ([Retrieve NOAA NWM data](../03-federal-water-data-access-retrieval/02_access_noaa_nwm.md)) compares access routes by use case.

### USGS (Water Data for the Nation)

- **Check whether data are provisional before relying on them.** Provisional information "is subject to revision", and USGS cautions users to "consider carefully the provisional nature of the information" ([USGS provisional data statement](https://waterdata.usgs.gov/provisional-data-statement/)).
- **Use the modernized Water Data APIs.** The legacy NWISWeb pages and WaterServices are being retired (the final decommission campaign runs November 2026 to February 2027). Use the `waterdata` module of `dataretrieval` for new code ([NWISWeb decommission summary](https://waterdata.usgs.gov/blog/nwisweb-decommission-summary/)).
- **Get a free API key for repeated or large requests**, and keep it out of your code ([API keys](https://api.waterdata.usgs.gov/docs/ogcapi/keys/)).
- **Cite the data with the publication year, access date and DOI** ([How should I cite USGS Water Data for the Nation data?](https://waterdata.usgs.gov/citation/)).

:::{admonition} Partner review (USGS): USGS (Water Data for the Nation)
:class: important
- Confirm this recommendation: *Check whether data are provisional before relying on them.*
- Confirm this recommendation: *Use the modernized Water Data APIs.*
- Confirm this recommendation: *Get a free API key for repeated or large requests.*
- Confirm this recommendation: *Cite the data with the publication year, access date and DOI.*
:::

## Further reading

- [PO.DAAC SWOT Cookbook](https://podaac.github.io/tutorials/quarto_text/SWOT.html)
- [Hydrocron documentation](https://podaac.github.io/hydrocron/) and [timeseries endpoint](https://podaac.github.io/hydrocron/timeseries)
- [SWOT Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf)
- [NASA's SWOT River Database (SWORD)](https://github.com/SWORD-Global/SWORD)
- [About the National Water Model (NOAA OWP)](https://water.noaa.gov/about/nwm)
- [NWM on the AWS Registry of Open Data](https://registry.opendata.aws/noaa-nwm-pds/)
- [USGS provisional data statement](https://waterdata.usgs.gov/provisional-data-statement/)
- [NWISWeb decommission summary](https://waterdata.usgs.gov/blog/nwisweb-decommission-summary/)
- [USGS Water Data API keys](https://api.waterdata.usgs.gov/docs/ogcapi/keys/)
- [How should I cite USGS Water Data for the Nation data?](https://waterdata.usgs.gov/citation/)
- [USGS Water Science School: How streamflow is measured](https://www.usgs.gov/water-science-school/science/how-streamflow-measured)
- [USGS Gages through the Ages](https://labs.waterdata.usgs.gov/visualizations/gages-through-the-ages/index.html)
- Module 1: [publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data)
