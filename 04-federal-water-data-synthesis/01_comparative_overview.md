# Comparative overview of Federal data products

In this lesson, we will compare and contrast the three Federal data products using helpful data dimensions, including data accuracy, temporal availability, and spatial coverage. We will wrap up this lesson with a section describing the best applications and uses for each of the data products. Understanding the similarities and differences can help you design research to appropriately leverage or adapt to existing data products.

## Spatial coverage

The three Federal datasets used in this course are built from very different spatial models. Below are the data products described in order of most spatially limited with high spatial specificity to most spatially expansive.

* **USGS NWIS streamflow** data are available at discrete points along the river network. These data represent observed measurements from sensors in the streams themselves, and are collected at a limited number of locations in the contiguous United States, Alaska, Hawaii, and US territories. Streams with streamflow data in USGS NWIS vary greatly in size, from intermittent and ephemeral streams to the mouth of the Mississippi. Some locations are also in coastal zones, where tides can impact streamflow data. 
* **NOAA NWM streamflow** data are available for all river reaches in the National Hydrography Dataset (NHD) [TODO: ADD MORE]
* **NASA SWOT water surface elevation** data are derived from a remotely-sensed raster of water extent. In their more raw form, these data are not spatially limited and can exist for every pixel across the globe. In the hydrology-linked data product `L2_HR_RiverSP`, the data are mapped to 10km river reaches based on NASA's underlying river geometries (SWORD) and are available for rivers globally. NASA SWOT produces water surface elevation data for streams at least 100m wide.

## Temporal availability

Much like their spatial coverage, the three data products also represent vastly different temporal landscapes. Below they are described in order of the most limited timeseries and shortest period of record to the most temporally robust.

* **NASA SWOT water surface elevation** data are only available when the SWOT satellite is passing over the location of interest. So while data are being continuously collected across the globe, data at any one location will be limited by SWOT satellite's orbit. Timeseries for a single location are available every 21 days starting in August 2023. While higher latitudes may have more observations over the 21-day cycle, the data are compiled such that there is one record every 21 days. 
* **NOAA NWM streamflow** data [TODO: COMPLETE THIS]
* **USGS NWIS streamflow** is considered a "real-time" data product. At currently active gages, data are collected every 15 minutes from sensors located at each streamgage. Under normal operational status, data are pushed up from the gages to NWIS at least every 6 hours. The 15-min, instantaneous data are available for gages beginning in 2007. The instantaneous data are also rolled up to _daily_ values (most commonly a _mean daily_ value). Daily records are available back to when the USGS streamgaging program began in 1889. While the data are "real-time", these in-situ sensors are subject to unexpected monitoring challenges (e.g. equipment malfunctions, critter invasions, biofouling, etc) and while mitigated, data gaps are present in the records.

## Accuracy

[details here, can we compare/contrast here? They are wildly different bc of observed vs modeled vs observed from space. Maybe just some accuracy statements unique to each is what would be helpful.]

[limitation of gage measurements in out-of-bank flood conditions, rating curve accuracy/adjustments]

[NASA provides uncertainty per measurement via `wse_u`]

## Data Providers Recommendations

[add content from data providers here]

## Further reading

- [NASA's SWOT River Database (SWORD)](https://github.com/SWORD-Global/SWORD)
- [USGS Gages through the Ages](https://labs.waterdata.usgs.gov/visualizations/gages-through-the-ages/index.html)
