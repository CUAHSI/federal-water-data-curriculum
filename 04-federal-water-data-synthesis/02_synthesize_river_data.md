# Synthesizing Federal data products to build hydrologic confidence

One way that these datasets are leveraged to improve hydrologic understanding and confidence is through the flood analyses. Floods are one of the most visible ways that communities benefit from improved hydrologic confidence and water research investments. Each of the three Federal water data products unlock different capabilities and mitigate limitations for measuring and understanding hydrologic conditions, especially in flood events. In this lesson, we will explore a specific prior flood and learn how each Federal dataset contributes to improving our understanding of flood events from a surface water perspective. You will also learn ancillary skills that are needed to work with these datasets together given their different temporal and spatial extents.

## Flood event context

We are going to explore a flood from December 2025 in the Skagit River in Washington state. A long-lasting Category 5 atmospheric river brought heavy precipitation to the Pacific Northwest causing widespread flooding (see [more from NASA's Scientific Visualization Studio](https://svs.gsfc.nasa.gov/5596)). On December, 12 2025, the Skagit River near Mt Vernon surpassed a 1990 record peak (Source: [NOAA gauge information](https://water.noaa.gov/gauges/MVEW1)). While our lesson will be focused on exploring the flood through the lens of data, it is important to remember that floods impact real people and can have devestating impacts. The December 2025 Skagit River historic flooding event led to evacuation orders for over 75,000 people (Source: [Northwest Public Broadcasting](https://www.nwpb.org/local/2025-12-11/100-000-evacuated-in-historic-skagit-valley-flood-in-washington-state)), and significantly damaged homes and businesses.

[TODO: INSERT PICTURE OF SKAGIT RIVER, flood and not flood?]

_The idea for using the Skagit River flooding event came from [the PO.DAAC SWOT tutorial "Hydrocron API: Getting Started with SWOT Time Series"](https://podaac.github.io/tutorials/notebooks/datasets/Hydrocron_SWOT_timeseries_examples_basic.html) authored by Nikki Tebaldi, Cassandra Nickles, and Brandi Downs._

[TODO: Maybe the following sections are just informational and then the coded more prescriptive step-by-step analysis comes in the form of the lab assignment?]

## Defining the area of interest

[bounding boxes and identifying spatial features and then linking them programmatically between usgs locations, SWORD and NHD river reaches]

## Starting on the ground: observations from USGS

[programmatically gathering obversations, but knowing and realizing the limits of 'out-of-bank' measurements]

[Data viewer: https://waterdata.usgs.gov/monitoring-location/USGS-12200500/#dataTypeId=continuous-00060-0&showFieldMeasurements=true&startDT=2025-12-01&endDT=2025-12-31]

## Looking ahead: forecasts from NOAA NWM

[using NOAA's NWM forecasts to see what might happen in the future + connect what is happening in the stream reaches between USGS gages]

[Data viewer: https://water.noaa.gov/gauges/MVEW1]

## A view from above: surface water extent from NASA SWOT

[TODO: THIS MIGHT NOT BE THE RIGHT USE ... we have been focused on SWOT `wse`, which I don't think spills out beyond the channel? Though maybe that means we should focus on a different one of their products?]

## Conclusions

[add some wrap-up thoughts here]
