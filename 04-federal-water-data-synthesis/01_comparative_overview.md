# Comparative overview of Federal data products

In this lesson, we will compare and contrast the three Federal data products using helpful data dimensions, including data accuracy, temporal availability, and spatial coverage. We will wrap up this lesson with a section describing the best applications and uses for each of the data products. Understanding the similarities and differences can help you design research to appropriately leverage or adapt to existing data products.

## Spatial coverage

The three Federal datasets used in this course are built from very different spatial models. Below are the data products described in order of most spatially limited with high spatial specificity to most spatially expansive.

* **USGS NWIS streamflow** data are available at discrete points along the river network. These data represent observed measurements from sensors in the streams themselves, and are collected at a limited number of locations in the contiguous United States, Alaska, Hawaii, and US territories. Streams with streamflow data in USGS NWIS vary greatly in size, from intermittent and ephemeral streams to the mouth of the Mississippi. Some locations are also in coastal zones, where tides can impact streamflow data. 
* **NOAA NWM streamflow** data are available for every river reach in the model's stream network, which is built on the National Hydrography Dataset (NHDPlus): over 2.7 million reaches in the contiguous United States, plus separate domains for southern Alaska, Hawaii, Puerto Rico and the U.S. Virgin Islands ([NOAA OWP](https://water.noaa.gov/about/nwm)). Each reach has one value per time step, identified by its `feature_id` (the NHDPlus COMID). Because the NWM is a model, it has values for ungaged headwater streams as well as large rivers. That spatial completeness is its main strength, but values in ungaged, heavily regulated or poorly calibrated basins deserve extra caution (see Module 2).
* **NASA SWOT water surface elevation** data are derived from a remotely-sensed raster of water extent. In their more raw form, these data are not spatially limited and can exist for every pixel across the globe. In the hydrology-linked data product `L2_HR_RiverSP`, the data are mapped to 10km river reaches based on NASA's underlying river geometries (SWORD) and are available for rivers globally. NASA SWOT produces water surface elevation data for streams at least 100m wide. [TODO: verify: Module 2 says the river product effectively resolves rivers about 50–100 m and wider, and SWORD targets ~30 m]

## Temporal availability

Much like their spatial coverage, the three data products also represent vastly different temporal landscapes. Below they are described in order of the most limited timeseries and shortest period of record to the most temporally robust.

* **NASA SWOT water surface elevation** data are only available when the SWOT satellite is passing over the location of interest. So while data are being continuously collected across the globe, data at any one location will be limited by SWOT satellite's orbit. Timeseries for a single location are available every 21 days starting in August 2023. While higher latitudes may have more observations over the 21-day cycle, the data are compiled such that there is one record every 21 days. [TODO: verify: hydrocron and RiverSP return one record per overpass, e.g. four observations of the lower Skagit reach in December 2025, and 22 of an upper Mississippi reach in March–July 2026 (Module 3), and Module 3 says the science orbit began in July 2023] 
* **NOAA NWM streamflow** data are produced continuously, as several _configurations_ that each answer a different question ([NOAA OWP](https://water.noaa.gov/about/nwm)):
  * an **analysis** of current conditions, updated through the day;
  * **short-range** forecasts out to 18 hours, issued every hour (CONUS);
  * **medium-range** forecasts out to 8.5–10 days, issued four times per day;
  * **long-range** ensemble forecasts out to 30 days.

  Operational forecasts have run since August 2016. A separate **retrospective** simulation re-runs the model over historical weather back to 1979, which makes it the main source of long, reach-level streamflow records where there is no gage (Module 2). Many distribution channels keep only recent runs: the NOAA forecast API (NWPS), for example, serves only recent runs [TODO: confirm the API's archive window from Lane A's P1.3 spike]. Past forecasts, like the December 2025 forecasts used in this module, come from cloud archives [TODO: depends on Lane A's P4.1 Module 3 NWM page]. Module 2 notes that NOAA's NOMADS server keeps a 48-hour rolling window.
* **USGS NWIS streamflow** is considered a "real-time" data product. At currently active gages, data are collected every 15 minutes from sensors located at each streamgage. Under normal operational status, data are pushed up from the gages to NWIS at least every 6 hours. The 15-min, instantaneous data are available for gages beginning in 2007. [TODO: verify: the time-series metadata for 12200500 lists continuous discharge from 1988, and Module 2 says instantaneous data go back to October 1, 1950] The instantaneous data are also rolled up to _daily_ values (most commonly a _mean daily_ value). Daily records are available back to when the USGS streamgaging program began in 1889. While the data are "real-time", these in-situ sensors are subject to unexpected monitoring challenges (e.g. equipment malfunctions, critter invasions, biofouling, etc) and while mitigated, data gaps are present in the records.

## Accuracy

The three products are very different kinds of data: an in-stream observation (USGS), a model (NOAA NWM), and an observation from space (NASA SWOT). Each agency describes accuracy in its own terms, so rather than ranking them, this section summarizes what each says about its product and what that means for a researcher.

**USGS streamflow** is the reference most researchers compare against, but discharge is not measured directly. The sensor records gage height, and discharge is computed from it with a _rating curve_ fitted to periodic field measurements of discharge (Module 2). Accuracy therefore depends on how well the rating is defined at the flow you care about. During floods the river can go out of bank, the channel can scour or fill, and field measurements are hard and dangerous to make. The top of the rating curve often rests on only a few measurements, so peak discharges are usually more uncertain than typical flows ([USGS: How streamflow is measured](https://www.usgs.gov/water-science-school/science/how-streamflow-measured)). [TODO: cite USGS rating-curve guidance for high-flow uncertainty] Each field measurement carries the hydrographer's own accuracy rating. At USGS 12200500, the measurement of 111,000 ft³/s at the December 12, 2025 peak was rated "Fair", compared with "Good" for a calmer November measurement (USGS field measurements from the [Water Data API](https://api.waterdata.usgs.gov/ogcapi/v0/); see the case study in the next lesson). Module 3 shows how to retrieve field measurements and their ratings. Values are `Provisional`, and can be revised, until USGS approves them ([USGS provisional data statement](https://waterdata.usgs.gov/provisional-data-statement/)).
[PARTNER REVIEW: USGS] Confirm the description of rating-curve uncertainty at high flows, and what the field-measurement ratings (e.g. Good, Fair) represent in percent terms.

**NOAA NWM streamflow** has no per-value quality flag. Its accuracy depends on the configuration, the weather forcing (especially forecast precipitation), how well the basin is calibrated, and the model version (Module 2). USGS and U.S. Army Corps of Engineers observations are assimilated into several of the analysis configurations; the others run without observations ([NOAA OWP](https://water.noaa.gov/about/nwm)). Forecast skill falls as lead time grows. The practical way to judge NWM accuracy for your question is to compare past forecasts with USGS observations for similar events, which is what Module 4 does for the Skagit.
[PARTNER REVIEW: NOAA] Confirm this summary of NWM error sources and of how observations are assimilated.

**NASA SWOT water surface elevation** comes with a per-observation uncertainty (`wse_u`, in meters) and with summary and bitwise quality flags (`reach_q`, `node_q`, `*_qual`). The mission's commonly cited goal of about 10 cm precision for water surface elevation is a mission-level target, not a guarantee for every reach and overpass (Module 2). Performance varies with river width, roughness and other local factors; the product description documents give the details (Module 2). On the lower Skagit, every December 2025 reach observation is flagged degraded, and one overpass reads about 12 m higher than December 1 at almost the same discharge (SWOT RiverSP via `hydrocron`; see the case study in the next lesson). [TODO: confirm Lane B's 04/02 includes these SWOT findings] Always check `wse_u` and the quality flags, and compare with an independent source where you can.
[PARTNER REVIEW: NASA] Confirm the precision-target wording and the main factors that affect WSE accuracy.

## Side-by-side comparison

The table lines the three products up using the course's shared vocabulary.

| | NASA SWOT (RiverSP) | NOAA NWM | USGS streamflow |
|---|---|---|---|
| What it is | Satellite observation | Hydrologic model (analysis and forecasts) | In-stream observation |
| **Location Identifier** | `reach_id` / `node_id` (SWORD) | `feature_id` (NHDPlus COMID) | `monitoring_location_id` (e.g. `USGS-12200500`) |
| **Variable** (rivers) | Water surface elevation, width, slope; derived discharge | Streamflow (plus land-surface variables) | Discharge (`00060`), gage height (`00065`) |
| **Variable unit** | m (WSE, width), m/km (slope), m³/s (discharge) | m³/s | ft³/s (discharge), ft (gage height) |
| **Data Quality Flag(s)** | `reach_q` / `node_q`, bitwise flags, `wse_u` uncertainty | None per value; depends on configuration and model version | `approval_status`, `qualifier`; `measurement_rated` for field measurements |
| Spatial coverage | Global rivers roughly 50–100 m wide and wider | Every NHDPlus reach (2.7M+), CONUS plus AK, HI, PR/USVI | About 9,000 stream gages with discharge |
| Temporal coverage | An overpass every few days to 21 days, since 2023 | Hourly to 6-hourly; forecasts since 2016, retrospective since 1979 | Typically 15-minute; daily records back to 1889 at the oldest sites |
| Typical latency | Days after an overpass [TODO: verify RiverSP latency] | About 1–2 hours after each cycle | Minutes to hours (provisional) |
| Main strength | Sees rivers anywhere, and floodplain water (Raster) | Complete network; forecasts | Highest-quality local record |
| Main caution | Sparse in time; quality varies by reach and pass | Model error; no per-value flag | Point locations only; ratings uncertain at extreme flows |

Sources: Module 2 agency pages, [NOAA OWP](https://water.noaa.gov/about/nwm), and the Module 3 lessons.

## Data Providers Recommendations

Each agency publishes guidance on how its data should and should not be used. The recommendations below are drafted from those sources, each one linked to its source, and are waiting for confirmation from the agencies.

### NASA (SWOT)

- **Use the programmatic tools PO.DAAC documents.** PO.DAAC lists `earthaccess` for searching and downloading SWOT granules, and its `hydrocron` API for river and lake time series in CSV or GeoJSON ([PO.DAAC SWOT Cookbook](https://podaac.github.io/tutorials/quarto_text/SWOT.html); [Hydrocron documentation](https://podaac.github.io/hydrocron/)). [PARTNER REVIEW: NASA]
- **Know which product version you are using, and don't mix versions without checking.** Version D supersedes Version C (`2.0`), and some reach and node IDs differ between them ([Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf); [Hydrocron versioning](https://podaac.github.io/hydrocron/)). [PARTNER REVIEW: NASA]
- **Use the quality flags and uncertainties for your application.** Check `reach_q` / `node_q` and the per-variable `*_qual` flags and `wse_u` rather than treating every value as equally reliable. The PO.DAAC Cookbook links a general quality-flag tutorial ([PO.DAAC SWOT Cookbook](https://podaac.github.io/tutorials/quarto_text/SWOT.html)). [PARTNER REVIEW: NASA] Is there an official recommended filter for research use, and how should users treat "degraded" (`reach_q` = 2) observations?
- **Ask for a `hydrocron` API key for heavy use.** Keys are optional, but PO.DAAC asks heavy or recurring users to request one ([Hydrocron timeseries docs](https://podaac.github.io/hydrocron/timeseries)). [PARTNER REVIEW: NASA]

### NOAA (National Water Model)

- **Treat NWM output as guidance, not the official forecast.** The NWM "complements official NWS river forecasts at approximately 4000 locations" ([NOAA OWP](https://water.noaa.gov/about/nwm)). For decisions at a forecast point, the official NWS river forecast is the authoritative source. [PARTNER REVIEW: NOAA]
- **Expect the data format to change between model versions.** NCEP encourages users to make sure their decoders are flexible, because output elements "may change with future NCEP model implementations" ([NOAA OWP](https://water.noaa.gov/about/nwm)). Record the model version with any NWM data you use. [PARTNER REVIEW: NOAA]
- **Cite the specific product and access date.** Cite the configuration you used from the [Registry of Open Data on AWS](https://registry.opendata.aws/noaa-nwm-pds/) listing (see Module 2). [PARTNER REVIEW: NOAA]

_Course note (not agency guidance):_ NWM output can be reached several ways, and they differ a lot in cost as your question grows. Module 3's NWM lesson compares access routes by use case. [TODO: link the Module 3 "Which access route for which use case?" table once Lane A's P4.1 page lands]

### USGS (Water Data for the Nation)

- **Check whether data are provisional before relying on them.** Provisional information "is subject to revision", and USGS cautions users to "consider carefully the provisional nature of the information" ([USGS provisional data statement](https://waterdata.usgs.gov/provisional-data-statement/)). [PARTNER REVIEW: USGS]
- **Use the modernized Water Data APIs.** The legacy NWISWeb pages and WaterServices are being retired (the final decommission campaign runs November 2026 to February 2027). Use the `waterdata` module of `dataretrieval` for new code ([NWISWeb decommission summary](https://waterdata.usgs.gov/blog/nwisweb-decommission-summary/)). [PARTNER REVIEW: USGS]
- **Get a free API key for repeated or large requests**, and keep it out of your code ([API keys](https://api.waterdata.usgs.gov/docs/ogcapi/keys/)). [PARTNER REVIEW: USGS]
- **Cite the data with the publication year, access date and DOI** ([How should I cite USGS Water Data for the Nation data?](https://waterdata.usgs.gov/citation/)). [PARTNER REVIEW: USGS]

## Further reading

- [About the National Water Model (NOAA OWP)](https://water.noaa.gov/about/nwm)
- [USGS provisional data statement](https://waterdata.usgs.gov/provisional-data-statement/)
- [PO.DAAC SWOT Cookbook](https://podaac.github.io/tutorials/quarto_text/SWOT.html)
- [Hydrocron documentation](https://podaac.github.io/hydrocron/) and [timeseries endpoint](https://podaac.github.io/hydrocron/timeseries)
- [SWOT Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf)
- [NWM on the AWS Registry of Open Data](https://registry.opendata.aws/noaa-nwm-pds/)
- [NWISWeb decommission summary](https://waterdata.usgs.gov/blog/nwisweb-decommission-summary/)
- [USGS Water Data API keys](https://api.waterdata.usgs.gov/docs/ogcapi/keys/)
- [How should I cite USGS Water Data for the Nation data?](https://waterdata.usgs.gov/citation/)
- [USGS Water Science School: How streamflow is measured](https://www.usgs.gov/water-science-school/science/how-streamflow-measured)
- [NASA's SWOT River Database (SWORD)](https://github.com/SWORD-Global/SWORD)
- [USGS Gages through the Ages](https://labs.waterdata.usgs.gov/visualizations/gages-through-the-ages/index.html)
