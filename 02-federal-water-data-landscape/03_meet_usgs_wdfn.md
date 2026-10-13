# Meet USGS WDFN

*USGS Water Data for the Nation ({term}`WDFN`)* is how the U.S. Geological Survey's Water Resources Mission Area publishes its water data, with the ultimate goal of providing high-quality and discoverable water data for everyone. This water data is collected at monitoring locations across the United States using automated sensors and manual data collection. Each monitoring location has unique location information, including the location name and identifier, the agency responsible for it, and geographic information. Water data provided by these monitoring locations covers a wide breadth of variables from chemical, to physical, to biological. This data is available as continuous data, daily data, field measurements, and discrete sample data (results from water samples collected on a given day and analyzed in a lab, such as water-quality measurements).

You will still see the name *NWIS*. The National Water Information System ({term}`NWIS`) is the USGS database behind WDFN. Its older website (NWISWeb) and web services ("WaterServices") are being decommissioned, and USGS is moving to the modernized equivalents: the WDFN website and the USGS Water Data APIs, which the USGS Python package {term}`dataretrieval` reaches through its `waterdata` module. This course uses these modernized equivalents. Learn more at the [WDFN home page](https://waterdata.usgs.gov/) and in [NWISWeb Decommission Campaign Summary](https://waterdata.usgs.gov/blog/nwisweb-decommission-summary/).

## Terminology

This table maps WDFN's own vocabulary onto the course's [shared concepts](00_introduction.md#m02-shared-concepts), for the discharge data this course uses.

| Shared concept | WDFN equivalent | Notes |
|---|---|---|
| {term}`Location identifier` | `monitoring_location_id` | Geographical location where data is collected, usually a USGS {term}`streamgage <Streamgage>`. Can be plotted as points on a map. The ID combines the agency and site number, for example `USGS-03294500`. See {term}`monitoring location ID <Monitoring location ID>`. |
| {term}`Variable` | Discharge, also referred to as streamflow by USGS | Stream discharge at a monitoring location, offered as continuous or daily values. Referred to with the {term}`parameter code <Parameter code>` `00060`. {term}`Gage height` (`00065`) is measured at the same locations. |
| {term}`Variable unit` | ft³/s | Cubic feet per second (`ft^3/s` in the `unit_of_measure` column). Gage height is in feet. |
| {term}`Time` | timestamp (continuous or daily) | {term}`Continuous values <Continuous values>` have a timestamp, usually every 15 minutes, in UTC. {term}`Daily values <Daily values>` have a date and a statistic, such as the daily mean ({term}`statistic code <Statistic code>` `00003`). The day is the monitoring location's local day, not a UTC day. |
| {term}`Data quality flag(s)` | `approval_status`, `qualifier` | `approval_status` is either `Provisional` or `Approved` (see {term}`approval status <Approval status>`). The {term}`qualifier <Qualifier>` column adds remarks about individual values, for example `['ESTIMATED']` when USGS had to estimate a value, such as during ice or equipment problems (it is empty, `None`, for most values). The possible codes are listed in the USGS Water Data APIs reference lists (see Further reading). Field measurements carry their own rating, `measurement_rated` (for example Poor, Fair or Good). |
| {term}`Version / provenance` | service and retrieval date | The data have no version number. Instead, record which service you used (for example the daily-values collection of the USGS Water Data APIs), the date you retrieved the data, and the approval status at that time. Each row also has a `last_modified` timestamp. |
| {term}`Data unit` | one time series per location + parameter | Every combination of monitoring location, parameter and statistic is a separate time series with its own `time_series_id`. |

## Dataset derivation

Discharge is available as continuous or daily data, also referred to as instantaneous values (IV) and daily values (DV) by USGS. Continuous discharge is usually recorded every 15 minutes, and daily data is the mean (average) of all continuously sampled data for that day.

Discharge is not directly measured every 15 minutes, but is calculated using the gage height. This is because it's easier to continuously measure the height of water than the volume of water passing by a point. Below are the three steps used to calculate continuous discharge data and ensure its accuracy. For further detail, see: [How Streamflow is Measured](https://www.usgs.gov/water-science-school/science/how-streamflow-measured) and [Why we use gage height](https://waterdata.usgs.gov/blog/gage_height/).

**Gage height → discharge**

1. Measuring gage height: at a location along a stream or river, direct measurements of the height of the water surface are taken. This is done every 15 minutes to create a continuous record over time.
2. Measuring discharge: then, direct measurements of discharge, called {term}`field measurements <Field measurement>`, are taken periodically at a wide range of gage heights (stream depths).
3. Establishing the gage height-discharge relationship: with these measurements, gage height and discharge are plotted to determine the relationship between them, called the {term}`rating curve <Rating curve>`. Once that relationship is determined, gage height can be converted to discharge. The continuous record of gage height allows continuous determination of streamflow discharge.

Field measurements are published too, so you can see how well the rating is supported at high flows. The Module 3 lesson [Retrieve USGS WDFN data](../03-federal-water-data-access-retrieval/03_access_usgs_wdfn.md) shows how to retrieve them alongside continuous and daily values.

## Spatial coverage

- **Extent:** Mainly CONUS + Alaska, Hawaii, and Puerto Rico. There are international monitoring locations which can be explored alongside all other monitoring locations here: [Monitoring locations - USGS Water Data for the Nation](https://waterdata.usgs.gov/monitoring-location/).
- **Type:** Point data for monitoring locations, returned as point geometries when querying monitoring location information from the API (`dataretrieval` returns them as a GeoDataFrame). Locations can also be found as coordinates (latitude and longitude) on monitoring location webpages
- **Resolution:** There are 9,011 monitoring locations with discharge data across CONUS + Alaska, Hawaii, and Puerto Rico. The spread of these monitoring locations is uneven, but easily explored using the [National Water Dashboard](https://dashboard.waterdata.usgs.gov/app/nwd/en/).
- **{term}`CRS`:** Point geometries from the API are longitude and latitude on the WGS84 datum, also referred to as EPSG 4326.

## Temporal coverage

- **Period of record:**
    - The first streamgage was established in 1889 on the Rio Grande in Embudo, New Mexico. However, instantaneous water data is only available as far back as October 1st, 1950. The availability of that historic record is dependent on the type of water data and the history of the monitoring location collecting that data. For example, the Ohio River at Louisville, KY (USGS-03294500) has continuous discharge from 2009 and daily values from 1928.
    - Historical continuous data may have gaps in availability due to instrument problems, environmental conditions, or other factors. Daily data can be used for a more complete record.
    - Recent data are {term}`provisional <Provisional data>`: they have not yet been reviewed and may be revised. USGS reviews and approves them later (see the [USGS provisional data statement](https://waterdata.usgs.gov/provisional-data-statement/)).
- **Frequency/resolution:** Most monitoring locations provide both continuous and daily discharge data. Continuous data is usually measured every 15 minutes, and daily data is the mean of all continuous data from that day.
- **Update cadence:** Continuous data may be available within minutes of collection, while other times there may be a delay if the monitoring location cannot automatically transmit data. Daily data is usually available same-day.

:::{admonition} Partner review (USGS): Coverage figures and provisional data
:class: important
Confirm: (1) the count of 9,011 monitoring locations with discharge data; (2) that instantaneous (continuous) data are available back to October 1, 1950; (3) that daily values are usually available the same day; (4) the provisional-data wording, and a typical lag between collection and approval (at USGS-03294500 on 2026-10-08, values from 9 April 2025 onward were still provisional); and (5) that daily values are computed over the monitoring location's local day (standard time). An earlier draft said provisional data are "only available for the last 120 days"; the provisional data statement describes provisional data as subject to revision, not limited to 120 days, and the 120-day window we found applies to certain parameters on some legacy station pages.
:::

## Data content

- **Primary variables:** discharge (ft³/s) at each `monitoring_location_id`, referred to with the parameter code `00060`.
- **Accuracy:** Discharge is not directly measured, but calculated using gage height. Monitoring locations that are streamgages operated by USGS maintain gage height measurements to the nearest 0.01 foot or 0.2 percent of stage, whichever is greater. The accuracy of the conversion from gage height to discharge is calibrated with direct measurements of discharge taken periodically. Discharge is therefore less certain than gage height, especially at very high flows, where there may be few field measurements and the rating curve is extended beyond them. Check the field measurements near the flows you care about.
- **Related products not covered here:** USGS publishes water data not just for streams, but also for lakes, ground water, coastal conditions, wetlands, etc. The variables provided by monitoring locations are referred to by parameter code/name and fall under categories such as informational, chemical, physical, and biological.
- **Known limitations:** The availability and quality of discharge data can be inconsistent between monitoring locations. Module 3 shows how to check what a location offers before you download.
    - Geographic coverage in an area is dependent on the quantity and spread of monitoring locations, which can be spotty.
    - Approval depends mostly on *when* a value was recorded: recent values are provisional everywhere, and older values become approved after review, which can take months and varies by location. The data quality flag `approval_status` can be used to only return approved data when querying discharge data from the USGS Water Data APIs.
    - Some data searches may return monitoring locations that are no longer operational.

**What the data look like.** The figure shows two years of daily mean discharge at the Ohio River at Louisville, Kentucky, drawn by approval status. The monitoring location ID `USGS-03294500` comes from the WDFN monitoring-location search; Module 3 shows how to find IDs in code. Everything up to 8 April 2025 was approved when we retrieved it; everything from 9 April 2025 on, including the crest of the April 2025 flood (712,000 ft³/s on 9 April), was still provisional. Provisional values can change when USGS reviews them, so a number you download today may not match the approved value later.

:::{figure} ../images/m02/03_meet_usgs_wdfn-ohio-daily-approval.png
:alt: Line chart of daily mean discharge at USGS-03294500 from October 2024 to October 2026. A solid blue line (approved) runs from October 2024 to 8 April 2025, with a peak near 600,000 cubic feet per second in February and a rise to about 710,000 on 8 April. A dashed orange line (provisional) starts at the 712,000 crest on 9 April 2025, falls, and has later peaks of about 250,000 to 380,000 through October 2026.
:width: 100%

Daily mean discharge at USGS-03294500, Ohio River at Louisville, KY, 1 October 2024 to 7 October 2026, by `approval_status`. Data: USGS Water Data for the Nation daily values (parameter `00060`, statistic `00003`), accessed 2026-10-08; 190 days were approved and 528 provisional at access; 19 days had no value, and the line connects across those gaps.
:::

:::{dropdown} How this figure was made
This script asks the USGS Water Data APIs for daily mean discharge at one monitoring location, using the `waterdata` module of `dataretrieval`. The query (location, parameter code, statistic code and dates) is kept in variables at the top. It runs in the course's `m03-wdfn` environment (`environments/m03-wdfn.yml`). An API key is optional; if you have one in the `API_USGS_PAT` environment variable, `dataretrieval` uses it for you. Module 3 explains keys.

```python
import pandas as pd
import matplotlib.pyplot as plt
from dataretrieval import waterdata

# Record the query in one place
SITE = "USGS-03294500"            # Ohio River at Louisville, KY
PARAM, STAT = "00060", "00003"    # discharge; daily mean
TIME = "2024-10-01/2026-10-07"

# get_daily returns the data and a metadata object (md) about the request, not used here
daily, md = waterdata.get_daily(monitoring_location_id=SITE, parameter_code=PARAM,
                                statistic_id=STAT, time=TIME)
daily["time"] = pd.to_datetime(daily["time"])
print(daily["approval_status"].value_counts())

# One line per approval status: solid for approved, dashed for provisional
fig, ax = plt.subplots(figsize=(9, 3.6))
styles = {"Approved": ("#2a78d6", "-"), "Provisional": ("#eb6834", "--")}
for status, grp in daily.sort_values("time").groupby("approval_status"):
    color, ls = styles[status]
    ax.plot(grp["time"], grp["value"] / 1000, color=color, ls=ls, lw=1.5, label=status)
ax.set_ylabel("Daily mean discharge\n(thousand ft³/s)")
ax.set_title("USGS-03294500, Ohio River at Louisville, KY", loc="left", fontsize=11)
ax.grid(alpha=0.3)
ax.legend(frameon=False, fontsize=9, title="approval_status", title_fontsize=9)
fig.tight_layout()
fig.savefig("03_meet_usgs_wdfn-ohio-daily-approval.png", dpi=150)
```

`daily` is a GeoDataFrame with one row per day that has a value, including `monitoring_location_id`, `time`, `value`, `unit_of_measure` (`ft^3/s`), `approval_status`, `qualifier`, `time_series_id` and `last_modified`. On 2026-10-08 it had 718 rows for a 737-day window, 190 `Approved` and 528 `Provisional`: daily records can have gaps, so check for missing days before computing statistics. If you run it later, more days will have become approved.
:::

## Usage and support

- **Citation:** USGS recommends citing WDFN data with the publication year, access date, and DOI. More information can be found at [How should I cite USGS Water Data for the Nation data?](https://waterdata.usgs.gov/citation/) Because recent values are provisional, also note the approval status of the data you used; if you publish results based on provisional data, say so. Module 1's [Publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data) covers recording the source, the retrieval date and how you processed it.
- **License/access:** Data accessed through the USGS Water Data APIs is completely open access. Acquiring an {term}`API key` is recommended and completely free, see [Get a USGS Water Data API Key](https://api.waterdata.usgs.gov/signup/) for more information. If you do not have an API key your queries have an hourly limit.
- **Change over time:** The USGS Water Data APIs will see newer versions released over time, but USGS maintains consistency in the water data offered across time. So a new API version does not by itself change the data. Values change for a different reason: provisional data are revised when they are approved, and approved data are occasionally revised too. Still, it is a good idea to check the [Water Data Blog](https://waterdata.usgs.gov/blog/) regularly for important updates.
- **Contact:** For questions about WDFN data, you can fill out the form at [Questions and Comments](https://waterdata.usgs.gov/questions-comments/).

:::{admonition} TODO (dev team): Learner-review friction items (P6.5.4)
:class: attention
From the integration-pass learner review (2026-10-09). Not yet fixed:
- Dataset derivation: add a bold "Key point:" line, as on the SWOT and NWM pages.
- The provisional-data partner-review callout quotes the old "120 days" claim; keep the question, drop the history.
- Say how big the no-key hourly limit is, or that it is fine for this module's examples; add the "you don't need to run this now" note to the figure dropdown.
- "Daily data is usually available same-day": revisit once USGS answers the partner review.
:::

## Further reading

- [WDFN home page](https://waterdata.usgs.gov/) - home page for Water Data For the Nation
- [USGS Water Data Collection Categories](https://waterdata.usgs.gov/data-collection-categories) - documentation and general info for the data types
- [Collections](https://api.waterdata.usgs.gov/ogcapi/v0/collections#ref-lists) - reference lists with information related to data types and possible values for meta data
- [USGS | National Water Dashboard](https://dashboard.waterdata.usgs.gov/app/nwd/en/) - interactive web mapper to explore monitoring locations and different water data variables in real time
- [Current and Historical Instantaneous Data Availability](https://waterdata.usgs.gov/iv-data-availability-statement/) - data availability statement
- [USGS provisional data statement](https://waterdata.usgs.gov/provisional-data-statement/) - what "provisional" means and why the values can change
- [What's new with WDFN APIs?](https://waterdata.usgs.gov/blog/api-whats-new-wdfn-apis/) - detailed information about the difference between the legacy NWIS API and the new WDFN API
- [NWISWeb Decommission Campaign Summary | Water Data Blog](https://waterdata.usgs.gov/blog/nwisweb-decommission-summary/) - detailed information about the decommissioning of NWIS web services and the transition to new WDFN web services.
- [Get a USGS Water Data API Key](https://api.waterdata.usgs.gov/signup/) - How to get a USGS Water Data API key
- [`dataretrieval` for Python](https://github.com/DOI-USGS/dataretrieval-python) - the USGS Python package used in this course
- [Water Data Blog](https://waterdata.usgs.gov/blog/) - WDFN blog posts. It is good to visit this page regularly since important updates to the water data, WDFN API, and WDFN web services will be posted here.
