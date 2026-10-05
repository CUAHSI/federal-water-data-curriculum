# Meet USGS NWIS

The National Water Information System (NWIS) is produced by USGS’s Water Resources Mission Area. NWIS collects many different types of water data with the ultimate goal of providing high-quality and discoverable water data for everyone. This water data is collected at monitoring locations across the United States using automated sensors and manual data collection. Each monitoring location has unique location information, including the location name and identifier, the agency responsible for it, and geographic information. Water data provided by these monitoring locations covers a wide breadth of variables from chemical, to physical, to biological. This data is available as continuous data, daily data, field measurements, and discrete sample data. 

NWIS web services and the NWIS API `waterservices` are in the process of being decommissioned. USGS is moving to the modernized equivalents; Water Data For the Nation (WDFN) web services and the WDFN API `waterdata`. This training will be utilizing these modernized equivalents. Learn more about NWIS/WDFN at the [WDFN home page](https://waterdata.usgs.gov/).


## Terminology

| Shared term | NWIS equivalent | Notes |
|---|---|---|
| Location Identifier | `monitoring_location_id` | Geographical location where data is collected, usually a USGS streamgage. Can be plotted as points on a map. |
| Variable | Discharge, also referred to as streamflow by USGS | Stream discharge at a monitoring location, offered as continuous or daily values. Referred to with the parameter code 00060. |
| Variable unit | ft³/s | Cubic feet per second |
| Data Quality Flag(s) | `approval_status` | Variable specific approval status unique to each monitoring location. Can be either approved or provisional. |

## Dataset derivation

Discharge is available as continuous or daily data, also referred to as instantaneous values (IV) and daily values (DV) by USGS. Continuous discharge is usually recorded every 15 minutes, and daily data is the mean (average) of all continuously sampled data for that day.

Discharge is not directly measured every 15 minutes, but is calculated using the gage height. This is because it’s easier to continuously measure the height of water than the volume of water passing by a point. Below are the three steps used to calculate continuous discharge data and ensure its accuracy. For further detail, see: [How Streamflow is Measured](https://www.usgs.gov/water-science-school/science/how-streamflow-measured?qt-science_center_objects=0#qt-science_center_objects) and [Why we use gage height](https://waterdata.usgs.gov/blog/gage_height/).

**Gage height → discharge**

1. Measuring gage height: at a location along a stream or river, direct measurements of the height of the water surface are taken. This is done every 15 minutes to create a continuous record over time. 
2. Measuring discharge: then, direct measurements of discharge are taken periodically at a wide range of gage heights (stream depths).
3. Establishing the gage height-discharge relationship: with these measurements, gage height and discharge are plotted to determine the relationship between them. Once that relationship is determined, gage height can be converted to discharge. The continuous record of gage height allows continuous determination of streamflow discharge.


## Spatial coverage

- **Extent:** Mainly CONUS + Alaska, Hawaii, and Puerto Rico. There are international monitoring locations which can be explored alongside all other monitoring locations here: [Monitoring locations - USGS Water Data for the Nation](https://waterdata.usgs.gov/monitoring-location/). 
- **Type:** Point data for monitoring locations, included as shapefile geometries when querying monitoring location information from the API. Locations can also be found as coordinates (latitude and longitude) on monitoring location webpages
- **Resolution:** There are 9,011 monitoring locations with discharge data across CONUS + Alaska, Hawaii, and Puerto Rico. The spread of these monitoring locations is uneven, but easily explored using the [National Water Dashboard](https://dashboard.waterdata.usgs.gov/app/nwd/en/).
- **CRS:** Shapefile point geometries are referenced to the WGS84 ellipsoid. This projection can also be referred to as EPSG 4326.


## Temporal coverage

- **Period of record:**
     - The first streamgage was established in 1889 on the Rio Grande in Embudo, New Mexico. However, instantaneous water data is only available as far back as October 1st, 1950. The availability of that historic record is dependent on the type of water data and the history of the monitoring location collecting that data.
    - Historical continuous data may have gaps in availability due to instrument problems, environmental conditions, or other factors. Daily data can be used for a more complete record.
     - Some monitoring locations provide provisional water data, which is only available for the last 120 days.
- **Frequency/resolution:** Most monitoring locations provide both continuous and daily discharge data. Continuous data is usually measured every 15 minutes, and daily data is the mean of all continuous data from that day.
- **Update cadence:** Continuous data may be available within minutes of collection, while other times there may be a delay if the monitoring location cannot automatically transmit data. Daily data is usually available same-day.


## Data content

- **Primary variables:** discharge (ft^3/s) at each `monitoring_location_id`, referred to with the parameter code `00060`.
- **Accuracy:** Discharge is not directly measured, but calculated using gage height. Monitoring locations that are streamgages operated by USGS maintain gage height measurements to the nearest 0.01 foot or 0.2 percent of stage, whichever is greater. The accuracy of the conversion from gage height to discharge is calibrated with direct measurements of discharge taken periodically.
- **Related products not covered here:** NWIS provides water data not just for streams, but also for lakes, ground water, coastal conditions, wetlands, etc. The variables provided by monitoring locations are referred to by parameter code/name and fall under categories such as informational, chemical, physical, and biological. 
- **Known limitations:** The availability and quality of discharge data can be inconsistent between monitoring locations. In this training we will introduce workflows that mitigate this inconsistency and utilize the rich water data NWIS provides to its full potential.
     - Geographic coverage in an area is dependent on the quantity and spread of monitoring locations, which can be spotty. 
     - Discharge data quality is monitoring location dependent, providing either approved or provisional data. The data quality flag `approval_status` can be used to only return approved data when querying discharge data from the WDFN API.
     - Some data searches may return monitoring locations that are no longer operational.


## Usage and support

- **Citation:** USGS recommends citing WDFN data with the publication year, access date, and DOI. More information can be found at [How should I cite USGS Water Data for the Nation data?](https://waterdata.usgs.gov/citation/)
- **Licence/access:** Data accessed through the WDFN API is completely open access. Acquiring an API key is recommended and completely free, see [Get a USGS Water Data API Key](https://api.waterdata.usgs.gov/signup/) for more information. If you do not have an API key your queries have an hourly limit.
- **Change over time:** The WDFN API will see newer versions released over time, but USGS maintains consistency in the water data offered across time. So, if a new API version is released, the underlying data has not changed. Still, it is a good idea to check the [Water Data Blogs](https://waterdata.usgs.gov/blog/) regularly for important updates. 
- **Contact:** For questions about NWIS/WDFN, you can fill out the form at [Questions and Comments](https://waterdata.usgs.gov/questions-comments?referrerUrl=https://waterdata.usgs.gov/).


## Further reading

- [WDFN home page](https://waterdata.usgs.gov/) - home page for Water Data For the Nation
- [USGS Water Data Collection Categories](https://waterdata.usgs.gov/data-collection-categories) - documentation and general info for the data types
- [Collections](https://api.waterdata.usgs.gov/ogcapi/v0/collections#ref-lists) - reference lists with information related to data types and possible values for meta data
- [USGS | National Water Dashboard](https://dashboard.waterdata.usgs.gov/app/nwd/en/) - interactive web mapper to explore monitoring locations and different water data variables in real time
- [Current and Historical Instantaneous Data Availability](https://waterdata.usgs.gov/iv-data-availability-statement/) - data availability statement
- [What's new with WDFN APIs?](https://waterdata.usgs.gov/blog/api-whats-new-wdfn-apis/)  - detailed information about the difference between the legacy NWIS API and the new WDFN API
- [NWISWeb Decommission Campaign Summary | Water Data Blog](https://waterdata.usgs.gov/blog/nwisweb-decommission-summary/) - detailed information about the decommissioning of NWIS web services and the transition to new WDFN web services.
- [Get a USGS Water Data API Key](https://api.waterdata.usgs.gov/signup/)  - How to get a WDFN API key
- [Water Data Blog](https://waterdata.usgs.gov/blog/) - WDFN blog posts. It is good to visit this page regularly since important updates to the water data, WDFN API, and WDFN web services will be posted here.

