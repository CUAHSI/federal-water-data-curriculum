# Meet NOAA NWM

| Location Identifier | River variable | River variable unit | Time / resolution | Data Quality Flag(s) |
|---|---|---|---|---|
| `feature_id` (NHDPlus reach/COMID) | streamflow | m³/s | Hourly (Analysis & Short-Range); 3-hourly (Medium-Range); ~daily cycling, 3-hr steps (Long-Range); hourly (Retrospective, 1979–present) | No per-value flag — quality is tied to model version (v1.2 → v2.0 → v2.1 → v3.0); see [version history](#dataset-derivation) |
 
The National Water Model (NWM) is produced by NOAA's [Office of Water Prediction](https://water.noaa.gov/about/nwm) (OWP), part of the National Weather Service. NWM is a hydrologic modeling framework, not an observational network — it simulates and forecasts streamflow (along with soil moisture, snowpack, and other water-budget variables) for over 3.4 million miles of rivers and streams across the U.S. and its territories by combining weather forecasts, land surface physics, and channel routing. It exists to fill the huge gap between the roughly 8,000 USGS streamgages and the 2.7+ million reaches that make up the U.S. river network, giving forecasters, emergency managers, and floodplain managers guidance in places with no gage at all. Learn more at the [NWM landing page](https://water.noaa.gov/about/nwm), [National Water Prediction Service](https://water.noaa.gov/) viewer, and [CIROH's NWM overview](https://hub.ciroh.org/docs/products/national-water-model/).

## Terminology

For this training, we'll map NWM's own vocabulary onto the shared terms used across all dataset pages:
 
- **Location Identifier → `feature_id`**: Each stream reach in the model has a unique `feature_id`, which corresponds to a COMID in the NHDPlus stream network. This is *not* the same as a USGS gage number (`site_no`). If you want to compare NWM output to observed data, you need a `feature_id`-to-`site_no` crosswalk.
- **River variable → streamflow**: Channel discharge at a reach. NWM also outputs many other variables (soil moisture, snowpack, evapotranspiration, reservoir levels) that aren't the focus of this training.
- **River variable unit → m³/s**: Cubic meters per second, consistent across all NWM configurations.
- **Data Quality Flag(s) → model version**: NWM has no per-observation QA/QC flag the way a sensor network does. Instead, "quality" is a function of *which model version and configuration* produced the value — see below.

## Dataset derivation

NWM output is entirely modeled, not measured directly. It couples a land-surface model (calculating snowmelt, infiltration, and runoff on a grid) with channel and reservoir routing along the NHDPlus stream network, then assimilates real-time observations (including USGS gage data) to correct the simulation. It has gone through several major versions since becoming operational in August 2016: v1.0, v1.2 (2018, with expanded calibration to ~1,000+ basins), v2.0, v2.1, and v3.0. Version 3.0 introduced several significant changes: first-time Total Water Level guidance for coastal CONUS, Hawaii, and Puerto Rico/USVI (via a coupled ocean model, SCHISM); domain expansion into south-central Alaska; a switch to the National Blend of Models as a forcing source for medium-range CONUS and Alaska forecasts; use of Multi-Radar Multi-Sensor precipitation for Puerto Rico/USVI; expanded ingestion of reservoir outflow forecasts (77 additional sites, bringing the total to 392); and calibration/parameter improvements. Each version can meaningfully change streamflow values at the same `feature_id`, and studies have found that v3.0 tends to underestimate peak flows and struggle with peak timing relative to v2.1 during storm events. Always check the [OWP version documentation](https://water.noaa.gov/about/nwm) or release notes before combining data across versions.

## Spatial coverage

- **Extent:** CONUS + hydrologically-contributing areas, plus separate domains for Hawaii, Puerto Rico/USVI, and southern Alaska (Cook Inlet, Copper River Basin, Prince William Sound)
- **Type:** Point/vector network output for streamflow and reservoirs (one value per `feature_id`, over 2.7 million reaches); paired with 1 km gridded NetCDF for land-surface variables and 100–250 m gridded NetCDF for ponded water depth and soil saturation
- **Resolution:** Reach-based routing follows NHDPlus (medium-resolution, 1:100,000-scale network); grids are 1 km (land surface) and 100/250 m (near-surface hydrology)
- **CRS:** NWM itself doesn't publish output in a single named CRS the way a GIS layer would — the streamflow/reach output is indexed to NHDPlus `feature_id`s rather than gridded coordinates. The underlying NHDPlus network uses the USA Contiguous Albers Equal Area Conic (USGS version); the gridded land-surface output uses its own Lambert Conformal Conic grid definition, documented in the NWM configuration files.

## Temporal coverage

- **Period of record:** Retrospective/reanalysis simulation covers 1979–present (continuously extended); operational forecasts have run since August 2016
- **Frequency/resolution:** Varies by configuration — Analysis & Assimilation and Short-Range are hourly; Medium-Range is 3-hourly; Long-Range is 6-hourly; the Retrospective dataset is hourly throughout
- **Update cadence:** Short-Range forecasts cycle hourly over CONUS; Medium- and Long-Range forecasts are produced four times a day; forecast latency is roughly 1–2 hours after cycle time (mostly driven by the lag in incoming weather-forcing data), not a fixed multi-hour push like some sensor networks

## Data content
- **Primary variable:** streamflow (m³/s) at each `feature_id`
- **Related variables available in the same output:** velocity, reservoir inflow/outflow/elevation, ponded water depth, depth to soil saturation, soil moisture, snowpack, evapotranspiration
- **Known limitations:** No formal per-value QA/QC flag exists; quality is instead governed by model version and configuration, and by how well any given basin was calibrated. Documented version-specific issues (e.g., v3.0's tendency to underestimate storm peaks) should be treated as caveats on the whole time series, not flags on individual values. As with any model, output quality also degrades in ungaged, heavily-regulated, or poorly-calibrated basins.

## Usage and support

- **Citation:** NOAA provides a standard citation format for its NWM datasets. For example, "NOAA National Water Model [dataset name] was accessed on [DATE] from [dataset URL]." Cite the specific product/version and access URL you used (operational NOMADS feed, AWS, or Google Cloud archive).
- **License/access:** NWM output is open data, distributed through the NOAA Open Data Dissemination (NODD) program via AWS and Google Cloud, as well as a 48-hour rolling window on NOAA's NOMADS server.
- **Change over time:** Values can shift not just with new observations (in Analysis & Assimilation) but with model version upgrades — treat any long time series spanning a version change as non-homogeneous.
- **Contact:** For questions about data content, quality, or model methodology, contact NOAA's Office of Water Prediction (contacts listed on the [NWM about page](https://water.noaa.gov/about/nwm)). For questions specifically about data delivery via NODD (AWS/Google Cloud access), email nodd@noaa.gov.

## Further reading

- [About the National Water Model (NOAA OWP)](https://water.noaa.gov/about/nwm)
- [National Water Prediction Service viewer](https://water.noaa.gov/)
- [NWM Short-Range Forecast — Registry of Open Data on AWS](https://registry.opendata.aws/noaa-nwm-pds/)
- [NWM CONUS Retrospective Dataset — Registry of Open Data on AWS](https://registry.opendata.aws/nwm-archive/)
- [CIROH Hub: What is the National Water Model?](https://hub.ciroh.org/docs/products/national-water-model/) — plain-language overview, good for orienting new trainees
- [CIROH NWM BigQuery API](https://hub.ciroh.org/docs/products/data-management/bigquery-api/) — a practical SQL-queryable access point for streamflow by `feature_id`
- [CIROH Hydrofabric documentation](https://hub.ciroh.org/docs/products/Hydrofabric/) — background on the reach/catchment network NWM routes over
- [CIROH RIVR App](https://hub.ciroh.org/docs/products/mobile-apps/RIVR/#background-of-the-us-nwm-streamflow-forecasts) - tool for real-time and forecast riverflow information