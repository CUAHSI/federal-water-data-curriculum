# Retrieve NASA SWOT water surface elevation data

There are many ways to find, access, and download NASA SWOT data. This module is going to spend the most time focusing on the recommended patterns for hydrology applications using the water surface elevation (`wse`) data from the SWOT mission. To help build the framework, you need to know that there are two ways to programmatically get access to SWOT data:

1. `earthaccess`: this is a Python library that allows users to access all of the NASA Earthdata stored in the cloud, including SWOT mission data. It streamlined what used to be complex access patterns across different systems and tools in order to help scientists get to the data faster (see more in [this blog post](https://nasa-openscapes.github.io/news/2024-03-04-earthaccess-tech-spotlight/)). Using `earthaccess`, a user can easily authenticate using the Earthdata login, find what data is available, and download or access a variety of products in NASA's cloud storage buckets.
1. `hydrocron`: this is an API built specifically to help streamline timeseries data access to the `SWOT_L2_HR_RIVERSP` data product. The queries allow users to access data across temporal ranges for specific locations, which is in contrast to how the SWOT data are archived (individual shapefiles per timestamp). It allows users who may be interested in a timeseries of data at a small number of locations the ability to easily retrieve that without a lot of extra effort. More on how `hydrocron` works is available in [this NASA news article](https://www.earthdata.nasa.gov/news/hydrocron-new-tool-swot-time-series-analysis).

This lesson uses two SWOT hydrology products. They answer different questions, so pick the product before you pick the tool:

| Your question | Product | Short name (Version D) | What you get | Tool |
|---|---|---|---|---|
| How did the water surface elevation (and width) of a river reach change over time? | River single-pass vector (RiverSP) | `SWOT_L2_HR_RiverSP_reach_D` / `_node_D` | One row per reach (~10 km) or node (~200 m) per overpass: `wse`, `width`, quality flags | `hydrocron` for time series at a few reaches; `earthaccess` for every reach in an area |
| Where was there water, and how much area did it cover, on a given overpass? | Water mask raster (Raster) | `SWOT_L2_HR_Raster_100m_D` (also `_250m_D`) | A gridded (UTM, 100 m or 250 m) scene per overpass: `water_area`, `water_frac`, `wse` and their quality flags | `earthaccess` + `xarray` |

RiverSP is tied to the [SWOT River Database (SWORD)](https://www.swordexplorer.com/) river centerlines, so it describes the channel. It does not tell you how far water spread out of bank. Raster is not tied to a river network, so it can show water anywhere in the scene, including floodplains. This lesson uses both on the upper Mississippi River in Minnesota. [Module 4](../04-federal-water-data-synthesis/02_synthesize_river_data.md) uses both again in a flood case study.

:::{admonition} Partner review (NASA): Retrieve NASA SWOT water surface elevation data
:class: important
Confirm this "which product for which question" framing and the description of what RiverSP does not capture out of bank.
:::

## Tools and environment setup

In order to complete this lesson about accessing NASA SWOT water surface elevation data, you first need to install a few libraries and create an account.

1. **Make an Earthdata Login account.** In order to _access_ data from the NASA Earthdata system, you will need to create an Earthdata Login account. Please visit [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov) to register and setup your login.
2. **Create the course environment.** We will be using the NASA `earthaccess` Python library for programmatic authentication to NASA Earthdata systems, data discovery, and data downloads, plus `xarray`, `geopandas` and `requests` for reading the files and calling `hydrocron`. The course provides a conda environment file, `environments/m03-swot.yml` (in the course repository), with everything this lesson uses. `mamba` is faster, but `conda` works the same way. To install `earthaccess` on its own instead, see its [user quick start guide](https://earthaccess.readthedocs.io/en/latest/user/quick-start/#installing-earthaccess).

```bash
# From the root of the course repository
mamba env create -f environments/m03-swot.yml   # or: conda env create -f environments/m03-swot.yml
conda activate m03-swot
```

To log in with `earthaccess`, run the following. If you have not stored your credentials, it will prompt you for your Earthdata username and password. To avoid typing them each time, set the `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` environment variables (or use a `.netrc` file); `earthaccess.login()` finds them automatically. Never write your password into a script or notebook. You can learn more in the [`earthaccess` authentication docs](https://earthaccess.readthedocs.io/en/latest/user/howto/authenticate/).

```python
# Log in to NASA Earthdata. Uses EARTHDATA_USERNAME/EARTHDATA_PASSWORD or .netrc if set, otherwise prompts.
import earthaccess
auth = earthaccess.login()
auth.authenticated  # True once you are logged in
```

> **Known install issue:** `import earthaccess` can fail with an SSL error (`ASN1: NOT_ENOUGH_DATA`) on older Python + newer OpenSSL combos ([details](https://github.com/python/cpython/issues/151504)). **Fix:** use Python 3.12+ (or OpenSSL < 3.5.7 with an older Python).

## Programmatic data discovery

Before you download or try to access the data itself, a common first step in any open data analysis is to first _discover_ or _find_ data in the data system that can meet your research needs. You don't want to download all of the database just to learn which dates are available, that would be incredibly inefficient. Instead, we can do the _discovery_ step and then adjust our data download approach using that information. As you will learn later, this discovery stage can also be a way to initialize information such as locations or times that allows you to build more efficient and scalable data download workflows.

As with many of the methods, a GUI (Graphical User Interface) approach to data discovery does exist. However, programmatic implementations support reproducibility and future extensions or applications of your work. So, while you can navigate to [Earthdata Search](https://search.earthdata.nasa.gov/), know that it would be a good idea to capture your search and discovery steps in code as documentation of the methods.

There are ways to search Earthdata broadly using general terms if you are unsure of what data product to use, see the `search_datasets` and `search_services` methods in the API documentation [here](https://earthaccess.readthedocs.io/en/latest/api/#earthaccess.api.search_datasets). The object returned from a search can be inspected to extract key information, including the dataset's shorthand name which is critical for querying and downloading the data itself. Below is an example of what you could do to search any Earthdata dataset that is linked to a "river" keyword.

```python
river_datasets_all = earthaccess.search_datasets(
    keyword="river"
)
len(river_datasets_all)  # 1539 at time of writing
```

At time of writing, this returned over 1500 datasets from a variety of data providers and locations. Let's add more specific querying parameters, such as a spatial and temporal filter to get only cloud-available datasets for an analysis of Minnesota rivers during 2023-2025.

```python
river_datasets_MN = earthaccess.search_datasets(
    keyword="river",
    cloud_hosted=True,
    bounding_box=(-97.5, 43.5, -89.5, 49.5),
    temporal=("2023", "2025")
)
len(river_datasets_MN) # 47 returned
```

This more specific query returned only 47 datasets. With a smaller set of datasets, we can inspect their shorthand names to get a sense of what is available and it looks like it includes a number of SWOT datasets but also Sentinel and some others.

```python
[r.get('umm').get('ShortName') for r in river_datasets_MN]
```

```
['SWOT_L2_HR_RiverSP_D', 'DLEM_C_N_Export_1699', 'SWOT_L2_HR_RiverAvg_2.0', 'SWOT_L2_HR_RiverAvg_D', 'SWOT_L2_HR_RiverSP_2.0', 'SWOT_L2_HR_RiverSP_node_2.0', 'SWOT_L2_HR_RiverSP_node_D', 'SWOT_L2_HR_RiverSP_reach_2.0', 'SWOT_L2_HR_RiverSP_reach_D', 'SWOT_L4_HR_DAWG_SOS_DISCHARGE_V3', 'SENTINEL-1A_SLC', 'SENTINEL-1A_DP_GRD_HIGH', 'SENTINEL-1A_META_RAW', 'SWOT_L2_HR_PIXC_D', 'SENTINEL-1A_RAW', 'SENTINEL-1A_META_SLC', 'SENTINEL-1A_DP_GRD_MEDIUM', 'SENTINEL-1A_SP_GRD_HIGH', 'SENTINEL-1A_DP_META_GRD_HIGH', 'ABI_G16-STAR-L3C-v2.70', 'AERDB_D3_VIIRS_NOAA20', 'AERDB_D3_VIIRS_SNPP', 'AERDB_M3_VIIRS_NOAA20', 'AERDB_M3_VIIRS_SNPP', 'AVHRRF_MB-STAR-L3U-v2.80', 'AVHRRF_MC-STAR-L3U-v2.80', 'VIIRS_N20-STAR-L3U-v2.80', 'VIIRS_NPP-STAR-L3U-v2.80', 'ABI_G16-STAR-L2P-v2.70', 'AERDB_L2_VIIRS_NOAA20', 'AERDB_L2_VIIRS_SNPP', 'SWOT_L2_HR_LakeSP_2.0', 'SWOT_L2_HR_LakeSP_obs_2.0', 'SWOT_L2_HR_LakeSP_prior_2.0', 'SWOT_L2_HR_LakeSP_unassigned_2.0', 'SWOT_L2_HR_PIXCVec_2.0', 'SWOT_L2_HR_PIXCVec_D', 'SENTINEL-1A_DP_GRD_FULL', 'SENTINEL-1A_SP_GRD_MEDIUM', 'SENTINEL-1A_DP_META_GRD_FULL', 'SENTINEL-1A_DP_META_GRD_MEDIUM', 'SENTINEL-1A_SP_META_GRD_HIGH', 'SENTINEL-1A_SP_META_GRD_MEDIUM', 'AERDB_D3_VIIRS_NOAA21', 'AERDB_M3_VIIRS_NOAA21', 'AERDB_L2_VIIRS_NOAA21', 'N21-VIIRS-L3U-ACSPO-v2.80']
```

In this lesson, we know that we are specifically interested in searching the available data for within the data product `L2_HR_RiverSP`. As this is a SWOT product, its "short name" would be `SWOT_L2_HR_RiverSP`. You will see 6 different datasets prefixed with `SWOT_L2_HR_RiverSP`:
- `SWOT_L2_HR_RiverSP_2.0` with children:
   - `SWOT_L2_HR_RiverSP_node_2.0`
   - `SWOT_L2_HR_RiverSP_reach_2.0`
- `SWOT_L2_HR_RiverSP_D` with children:
   - `SWOT_L2_HR_RiverSP_node_D`
   - `SWOT_L2_HR_RiverSP_reach_D`.

The `2.0` vs `D` distinction is referring to the _version_ of the data. `2.0` refers to "Version C", which has now been superseded by "Version D" (see the [Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf)). In addition, each _version_ has two different spatial variants available, "node" (one file per 200m node along a reach) and "reach" (one file per 10km river reach).

In our example here, we are interested in the most up-to-date, reach-level data so we would use the `search_data` method to find files within the `SWOT_L2_HR_RiverSP_reach_D` dataset:

```python
# Find available granules (aka "files") in June 2026 whose footprint intersects a box at the Mississippi headwaters
mississippi_headwaters_2026 = earthaccess.search_data(
    short_name="SWOT_L2_HR_RiverSP_reach_D",
    bounding_box=(-95.26, 47.17, -95.15, 47.25),
    temporal=("2026-06", "2026-06")
)
len(mississippi_headwaters_2026)
```

At time of writing, this returns 42 granules for June 2026.

Each item in the list is a _granule_, the term NASA uses for one file (or a small bundle of files) in a dataset. You can look inside a granule's metadata before downloading anything. The granule name packs in useful information, such as the cycle, pass, continent code and start/end time of the overpass, and the `size` attribute gives the file size in MB:

```python
for g in mississippi_headwaters_2026[:5]:
    print(g["umm"]["GranuleUR"], g["umm"]["TemporalExtent"]["RangeDateTime"]["BeginningDateTime"], round(g.size, 2), "MB")
```

```
SWOT_L2_HR_RiverSP_Reach_051_121_NA_20260602T183346_20260602T184459_PID0_01_swot 2026-06-02T18:33:46.886Z 4.71 MB
SWOT_L2_HR_RiverSP_Reach_051_160_NA_20260604T033529_20260604T035110_PID0_01_swot 2026-06-04T03:35:29.878Z 7.62 MB
SWOT_L2_HR_RiverSP_Reach_051_188_NA_20260605T033600_20260605T035158_PID0_01_swot 2026-06-05T03:36:00.826Z 7.59 MB
SWOT_L2_HR_RiverSP_Reach_051_188_NA_20260605T033600_20260605T035158_PID0_02_swot 2026-06-05T03:36:00.826Z 7.59 MB
SWOT_L2_HR_RiverSP_Reach_051_216_NA_20260606T033652_20260606T035154_PID0_01_swot 2026-06-06T03:36:52.017Z 8.6 MB
```

Reading the first name: `Reach` granule, cycle `051`, pass `121`, continent `NA` (North America), start and end time in UTC, and a processing counter (`01`). Notice the two granules for June 5 that differ only in that last counter (`_01` and `_02`): the same overpass was processed more than once. Usually you keep the highest counter.

:::{admonition} Partner review (NASA): Programmatic data discovery
:class: important
Confirm that keeping the highest processing counter is the recommended way to de-duplicate granules.
:::

A few things to know about `search_data` (see the [`earthaccess` API docs](https://earthaccess.readthedocs.io/en/latest/api/) for every option):

- **`temporal`** takes a `(start, end)` pair of strings or `datetime` objects. A month such as `("2026-06", "2026-06")` covers the whole month (42 granules here, the same as `("2026-06-01", "2026-06-30T23:59:59")`), but a single day written as `("2026-06-01", "2026-06-01")` means one instant at midnight and finds nothing. Write full dates and times when you need to be precise.
- **`bounding_box`** is `(west, south, east, north)` in decimal degrees. Swapping the order is a common mistake.
- **`count`** limits how many granules are returned, which is handy while you are exploring.
- **A query that matches nothing returns an empty list, not an error.** A misspelled `short_name`, a bounding box with latitude and longitude swapped, or a date before the mission began all give `[]`. Always check `len()` before moving on. (Short names are not case-sensitive, so `_reach_d` still works; a misspelling does not.)

```python
# A typo in the short name does not raise an error -- it just finds nothing
len(earthaccess.search_data(short_name="SWOT_L2_HR_RiverSP_rech_D", count=5))  # 0
```

**A granule in your results is not a guaranteed observation of your site.** Each RiverSP granule covers a whole pass across a continent, so its footprint "intersects" the headwaters box even when SWOT measured no river there. Download one and look:

```python
import geopandas as gpd
from shapely.geometry import box

files = earthaccess.download(mississippi_headwaters_2026[:1], local_path="data/swot")
reaches = gpd.read_file(files[0])  # geopandas reads the zipped shapefile directly
print(len(reaches), "reaches; extent", reaches.total_bounds.round(1))
print(int(reaches.intersects(box(-95.26, 47.17, -95.15, 47.25)).sum()), "reaches inside the headwaters box")
```

```
650 reaches; extent [-109.4   25.3  -94.8   59.7]
0 reaches inside the headwaters box
```

None of the reaches in this granule are in the box, and the same is true for every June 2026 granule. The most likely reason is not SWOT's orbit: the SWOT River Database (SWORD) does not appear to include the narrow headwater channels near Lake Itasca. Along the Mississippi, SWORD reaches begin farther downstream, near Aitkin, MN.

:::{admonition} TODO (dev team): Verify the upstream end of SWORD's Mississippi…
:class: attention
Verify the upstream end of SWORD's Mississippi River reaches with SWORD Explorer
:::

For the rest of this lesson we move downstream to **USGS 05227500, Mississippi River at Aitkin, MN**, during the spring 2026 snowmelt rise. This is a river SWOT does observe, and a gage the [USGS lesson](03_access_usgs_wdfn.md) uses too.

:::{admonition} TODO (dev team): Confirm the Aitkin site and spring 2026…
:class: attention
Confirm the Aitkin site and spring 2026 period, or name another Module 3 example
:::

The water-area product is discovered the same way. Here we search the 100 m Raster product in a small box around the gage, for the weeks around the snowmelt peak:

```python
# USGS 05227500, Mississippi River at Aitkin, MN (coordinates from its USGS monitoring-location record),
# plus or minus 0.02 degrees: a box about 3 x 4 km
aitkin_lon, aitkin_lat = -93.7074, 46.5407
aitkin_bbox = (aitkin_lon - 0.02, aitkin_lat - 0.02, aitkin_lon + 0.02, aitkin_lat + 0.02)

aitkin_raster = earthaccess.search_data(
    short_name="SWOT_L2_HR_Raster_100m_D",
    bounding_box=aitkin_bbox,
    temporal=("2026-04-15", "2026-05-10"),
)
print(len(aitkin_raster), "granules")
print(sorted({g["umm"]["GranuleUR"].split("_")[5] for g in aitkin_raster}))  # the UTM zone + band of each scene
```

```
39 granules
['UTM01C', 'UTM01W', 'UTM15T', 'UTM60C', 'UTM60F', 'UTM60K', 'UTM60L', 'UTM60U', 'UTM60V', 'UTM60W']
```

Thirty-nine granules in less than four weeks is far more than SWOT could have seen over one gage. The UTM zone in each name gives the problem away. Aitkin is in UTM zone **15**, but most results are in zones 01 and 60, on either side of the antimeridian (180° longitude). The metadata footprints of those granules wrap around the whole globe, so they falsely "intersect" almost any bounding box. Always sanity-check search results before downloading. Here, downloading everything would have meant 2.7 GB, including 1.5 GB of files from the wrong side of the planet (at time of writing).

A more reliable check than the bounding box is each granule's footprint _polygon_ (`GPolygons` in its metadata). The false matches have no polygon, only a global rectangle. Even among the zone-15 scenes, neighboring scenes from the same pass (for example `036F` and `037F`) both match the box, but only one of them actually contains the gage. The function below keeps the granules whose footprint polygon contains the gage, then keeps only the latest processing of each scene:

```python
from shapely.geometry import Point, Polygon

def footprint_covers(granule, lon, lat):
    """True if one of the granule's footprint polygons contains the point (lon, lat)."""
    geometry = granule["umm"]["SpatialExtent"]["HorizontalSpatialDomain"]["Geometry"]
    for polygon in geometry.get("GPolygons", []):
        points = [(p["Longitude"], p["Latitude"]) for p in polygon["Boundary"]["Points"]]
        if Polygon(points).contains(Point(lon, lat)):
            return True
    return False

covering = [g for g in aitkin_raster if footprint_covers(g, aitkin_lon, aitkin_lat)]

# Where a scene was processed more than once, keep the highest processing counter
latest = {}
for g in sorted(covering, key=lambda g: g["umm"]["GranuleUR"]):
    scene = g["umm"]["GranuleUR"].rsplit("_", 2)[0]  # name without the processing counter
    latest[scene] = g

aitkin_raster = list(latest.values())
for g in aitkin_raster:
    print(g["umm"]["GranuleUR"], round(g.size, 1), "MB")
```

```
SWOT_L2_HR_Raster_100m_UTM15T_N_x_x_x_048_522_037F_20260415T114827_20260415T114849_PID0_01_swot 82.1 MB
SWOT_L2_HR_Raster_100m_UTM15T_N_x_x_x_049_009_118F_20260418T010816_20260418T010837_PID0_01_swot 85.1 MB
SWOT_L2_HR_Raster_100m_UTM15T_N_x_x_x_049_216_036F_20260425T101025_20260425T101046_PID0_01_swot 80.1 MB
SWOT_L2_HR_Raster_100m_UTM15T_N_x_x_x_049_522_037F_20260506T083332_20260506T083353_PID0_03_swot 83.4 MB
SWOT_L2_HR_Raster_100m_UTM15T_N_x_x_x_050_009_118F_20260508T215320_20260508T215341_PID0_01_swot 83.8 MB
```

The Raster name adds the UTM zone and latitude band (`UTM15T`) and a scene number (for example `036F`) to the cycle, pass and time.

:::{admonition} Partner review (NASA): Programmatic data discovery
:class: important
Is the antimeridian false-match behavior a known CMR/`earthaccess` issue, and is checking the granule's `GPolygons` footprint (as above) the recommended workaround?
:::

Behind the scenes, `earthaccess` is querying NASA's [Common Metadata Repository (CMR)](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html) and, when you download, reading from the PO.DAAC cloud archive in Amazon Web Services (AWS) `us-west-2`. You don't need to know either system to use `earthaccess`, but it helps when you read other tutorials that call them directly.

## Programmatic data downloads

Discovery told us _which_ granules exist. Now we get the data. The two tools behave differently:

- `earthaccess` gives you **whole files**: one granule per overpass, covering a large area. `earthaccess.download()` copies them to your computer. `earthaccess.open()` streams them instead. Streaming is most efficient when your code runs in the same cloud region as the data (AWS `us-west-2`), which is why NASA calls this _cloud-native_ access. On a laptop, downloading a handful of files is usually simpler and just as fast.
- `hydrocron` gives you **just the rows you ask for**: the values for one reach or node, across many overpasses, in a single web request. Nothing is downloaded but the answer.

### `earthaccess`

`earthaccess` works for every SWOT product. The file format depends on the product: RiverSP granules are zipped shapefiles (read them with `geopandas`), and Raster granules are NetCDF files (read them with `xarray`).

**RiverSP reaches.** We download one RiverSP reach granule from an overpass that saw the Aitkin gage, and find the SWORD reach closest to the gage. RiverSP granule metadata only has a bounding rectangle for the whole pass, so `footprint_covers` can't screen them. Instead we keep the RiverSP granules from the same cycle and pass as the Raster scenes that do cover the gage. This is also how you find a `reach_id` to use with `hydrocron` below if you don't already have one. (You can also look up reach IDs interactively in [SWORD Explorer](https://www.swordexplorer.com/).) The gage coordinates come from the [USGS monitoring-location record for 05227500](https://api.waterdata.usgs.gov/ogcapi/v0/collections/monitoring-locations/items/USGS-05227500). Printing the granule name before downloading confirms what you are getting.

```python
aitkin_reach_granules = earthaccess.search_data(
    short_name="SWOT_L2_HR_RiverSP_reach_D",
    bounding_box=aitkin_bbox,
    temporal=("2026-04-15", "2026-05-10"),
)
# (cycle, pass) of the Raster scenes that cover the gage, e.g. ("049", "009")
seen_passes = {tuple(g["umm"]["GranuleUR"].split("_")[10:12]) for g in aitkin_raster}
covering = [g for g in aitkin_reach_granules if tuple(g["umm"]["GranuleUR"].split("_")[5:7]) in seen_passes]
print(len(aitkin_reach_granules), "granules found,", len(covering), "from passes that saw the gage; downloading", covering[0]["umm"]["GranuleUR"])
files = earthaccess.download(covering[:1], local_path="data/swot")

reaches = gpd.read_file(files[0])
print(len(reaches), "reaches in this granule")

# Distance from each reach to the gage, in meters (UTM zone 15N)
gage = gpd.GeoSeries([Point(aitkin_lon, aitkin_lat)], crs="EPSG:4326").to_crs(32615).iloc[0]
reaches_utm = reaches.to_crs(32615)
reaches_utm["dist_to_gage_m"] = reaches_utm.distance(gage)
reaches_utm.nsmallest(3, "dist_to_gage_m")[["reach_id", "river_name", "dist_to_gage_m", "p_width", "wse", "width", "reach_q", "time_str"]]
```

```
44 granules found, 7 from passes that saw the gage; downloading SWOT_L2_HR_RiverSP_Reach_048_522_NA_20260415T114417_20260415T115921_PID0_01_swot
1371 reaches in this granule
         reach_id         river_name  dist_to_gage_m  p_width       wse      width  reach_q              time_str
1255  74289700111  Mississippi River       38.873441     36.0  361.5908   3.333258        2  2026-04-15T11:48:30Z
1254  74289700101  Mississippi River     4054.308625     36.0  361.1173  11.358914        2  2026-04-15T11:48:29Z
1256  74289700121  Mississippi River     4855.032971     42.0  362.5025  10.784087        2  2026-04-15T11:48:29Z
```

The gage sits on reach **`74289700111`**, about 40 m from its centerline. The granule itself holds every reach SWOT observed along this pass across North America, 1,371 in total. RiverSP granules carry many more columns than shown here (about 130); the product description documents (PDDs), linked from the [PO.DAAC Cookbook SWOT page](https://podaac.github.io/tutorials/quarto_text/SWOT.html), define them all.

Notice `p_width`: SWORD expects this reach to be about 36 m wide. That is narrower than the roughly 50–100 m rivers SWOT reliably resolves (Module 2), and the measured `width` of 3 m on this overpass is not believable. Keep that in mind when we look at the time series below.

Each row is one SWORD reach seen on this overpass. Key columns:
- `reach_id` is the **Location Identifier**.
- `wse` (water surface elevation) and `width` are the main **Variables**. Their **Variable unit** is meters; `wse` is relative to the EGM2008 geoid.
- `wse_u` and `width_u` give each value's uncertainty.
- `p_width` is SWORD's prior (expected) width for the reach, useful for judging whether a measured `width` is plausible.
- `reach_q` is the summary **Data Quality Flag**: 0 = good, 1 = suspect, 2 = degraded, 3 = bad.
- Missing values are stored as `-999999999999`, not as `NaN`. Filter them out before plotting.

:::{admonition} Partner review (NASA): earthaccess
:class: important
Confirm the reach_q value meanings and the EGM2008 vertical reference for Version D RiverSP `wse`.
:::

**Raster water area.** Next, download the Raster granules we kept and open one with `xarray`. Each file is a fixed scene, about 160 km on a side, on a 100 m UTM grid.

```python
import xarray as xr

raster_files = earthaccess.download(aitkin_raster, local_path="data/swot")
ds = xr.open_dataset(raster_files[0])
ds[["water_area", "water_frac", "wse", "water_area_qual"]]
```

```
<xarray.Dataset> Size: 39MB
Dimensions:          (y: 1560, x: 1560)
Coordinates:
  * y                (y) float64 12kB 5.016e+06 5.016e+06 ... 5.172e+06
  * x                (x) float64 12kB 3.48e+05 3.481e+05 ... 5.038e+05 5.039e+05
Data variables:
    water_area       (y, x) float32 10MB ...
    water_frac       (y, x) float32 10MB ...
    wse              (y, x) float32 10MB ...
    water_area_qual  (y, x) float32 10MB ...
Attributes: (12/49)
    Conventions:                   CF-1.7
    title:                         Level 2 KaRIn High Rate Raster Data Product
    source:                        Ka-band radar interferometer
    ...                            ...
    x_min:                         348000.0
    x_max:                         503900.0
    y_min:                         5016100.0
    y_max:                         5172000.0
    institution:                   CNES
```

For each 100 m pixel:
- `water_area` (**Variable unit**: m²) is the surface area of water in the pixel. A pixel that is fully water is about 10,000 m².
- `water_frac` (unitless) is the fraction of the pixel covered by water.
- `wse` (m above the geoid) is the water surface elevation.
- `water_area_qual` is the **Data Quality Flag** for `water_area`: 0 = good, 1 = suspect, 2 = degraded, 3 = bad. `wse_qual` and the other `_qual` variables work the same way.

Pixels outside the swath are `NaN`. The `x` and `y` coordinates are UTM meters, and the full projection is in the `crs` variable's `crs_wkt` attribute.

To compare overpasses, add up `water_area` in a 10 km × 10 km box around the gage in each file. Two details matter:
- **Use the file's own projection.** Converting the gage location into each file's UTM coordinates keeps the box in the same place.
- **Apply the quality flag.** Pixels flagged bad (3) can report a `water_area` many times larger than the pixel itself. Keep only good and suspect pixels (`water_area_qual <= 1`).

```python
import pandas as pd
import pyproj

def water_area_near(path, lon=aitkin_lon, lat=aitkin_lat, half_width_m=5000):
    """Open-water area (km^2) in a square box centred on (lon, lat), using good/suspect pixels only."""
    ds = xr.open_dataset(path)
    utm = pyproj.CRS.from_wkt(ds["crs"].attrs["crs_wkt"])
    x, y = pyproj.Transformer.from_crs("EPSG:4326", utm, always_xy=True).transform(lon, lat)
    box = ds.sel(x=slice(x - half_width_m, x + half_width_m), y=slice(y - half_width_m, y + half_width_m))
    good = box["water_area"].where(box["water_area_qual"] <= 1)
    return {
        "time": ds.attrs["time_granule_start"][:16],
        "pixels_observed": int(box["water_area"].notnull().sum()),
        "pixels_flagged_bad": int(((box["water_area_qual"] == 3) & box["water_area"].notnull()).sum()),
        "water_area_km2": round(float(good.sum()) / 1e6, 1),
    }

pd.DataFrame([water_area_near(f) for f in raster_files])
```

```
               time  pixels_observed  pixels_flagged_bad  water_area_km2
0  2026-04-15T11:48                5304                   0             4.6
1  2026-04-18T01:08                6835                   3            20.3
2  2026-04-25T10:10                3534                   0             2.2
3  2026-05-06T08:33                5807                   0             6.1
4  2026-05-08T21:53                6255                   0            15.3
```

The 10 km box holds about 10,000 pixels, but no overpass observed all of them (`pixels_observed`). The numbers also jump between overpasses in a way discharge can't explain. USGS daily mean discharge at Aitkin ([USGS daily mean discharge for 05227500](https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily/items?monitoring_location_id=USGS-05227500&parameter_code=00060&statistic_id=00003&time=2026-03-01/2026-07-31), approved as of October 2026) rose from about 2,100 ft³/s on April 15 to a peak of 4,950 ft³/s on May 1, then fell to about 3,500 ft³/s by May 8. Yet the April 18 and May 8 scenes (pass 009, scene `118F`) show roughly two and a half to four times more water than the April 15 and May 6 scenes (pass 522, scene `037F`). Two lessons follow:

1. **Compare like with like.** Different passes view the area from different geometries and cover different parts of the box, so compare water area within the same pass and scene, and check `pixels_observed` before comparing totals.
2. **Check satellite numbers against an independent source.** A gage, an aerial image, or the other pass will tell you when a change is not physically plausible. The [USGS lesson](03_access_usgs_wdfn.md) shows how to get the discharge record used here.

:::{admonition} Partner review (NASA): earthaccess
:class: important
Why do pass 009 (scene 118F) and pass 522 (scene 037F) give such different water areas around Aitkin at similar discharge, and what is the recommended way to compare water extent across passes?
:::

:::{admonition} Partner review (NASA): earthaccess
:class: important
Confirm the interpretation of `water_area` values far above pixel area when `water_area_qual` = 3, and whether `water_area_qual <= 1` is the recommended filter for water-extent work.
:::

### `hydrocron`

While a user can access SWOT data through `earthaccess`, if timeseries data for specific rivers are the desired outcome, then the `hydrocron` API is the tool for the job. As the [`hydrocron` documentation](https://podaac.github.io/hydrocron) states,

> SWOT data is archived as individually timestamped shapefiles, which would otherwise require users to perform potentially thousands of file IO operations per river feature to view the data as a timeseries. Hydrocron makes this possible with a single API call.

`hydrocron` is a web API, so there is nothing extra to install: any HTTP client works, and we use `requests`. You do not need an Earthdata login or an API key for normal use. PO.DAAC offers optional keys for heavy use, sent in an `x-hydrocron-key` header. One request returns one feature (a reach, node or lake) over a time range, and responses are capped at 6 MB. See the [`hydrocron` timeseries documentation](https://podaac.github.io/hydrocron/timeseries) for every parameter. The main ones:

| Parameter | Example | Notes |
|---|---|---|
| `feature` | `Reach` | `Reach`, `Node` or `PriorLake` |
| `feature_id` | `74289700111` | SWORD reach or node ID (the **Location Identifier**) |
| `start_time`, `end_time` | `2026-03-01T00:00:00Z` | UTC |
| `fields` | `reach_id,time_str,wse,wse_u,width,reach_q` | Only the columns you need |
| `output` | `csv` | `csv` or `geojson`, returned inside a JSON response |
| `collection_name` | `SWOT_L2_HR_RiverSP_D` | Optional; defaults to Version D. Version C (`2.0`) reach IDs can differ |

The function below, adapted from the CUAHSI longitudinal-profile notebook (see Further reading), wraps one request and returns a `pandas` DataFrame. It drops overpasses with no valid measurement (fill values), and by default keeps everything else. Pass `max_reach_q` to also drop observations whose quality flag is worse than you can accept.

```python
import io
import requests

HYDROCRON_URL = "https://soto.podaac.earthdatacloud.nasa.gov/hydrocron/v1/timeseries"
FILL_VALUE = -999999999999.0

def get_reach_timeseries(reach_id, start, end, fields="reach_id,time_str,wse,wse_u,width,reach_q", max_reach_q=3):
    params = {
        "feature": "Reach",
        "feature_id": reach_id,
        "start_time": start,
        "end_time": end,
        "output": "csv",
        "fields": fields,
    }
    response = requests.get(HYDROCRON_URL, params=params, timeout=60)
    body = response.json()
    if response.status_code != 200:
        raise RuntimeError(body.get("error", response.text))
    df = pd.read_csv(io.StringIO(body["results"]["csv"]))
    df = df[(df["wse"] != FILL_VALUE) & (df["reach_q"] <= max_reach_q)].copy()
    df["time"] = pd.to_datetime(df["time_str"])
    return df

aitkin_reach = get_reach_timeseries("74289700111", "2026-03-01T00:00:00Z", "2026-07-31T00:00:00Z")
print(len(aitkin_reach), "observations;", aitkin_reach["reach_q"].value_counts().sort_index().to_dict())
aitkin_reach[["time_str", "wse", "wse_u", "width", "reach_q"]]
```

```
22 observations; {1: 15, 2: 7}
                time_str       wse    wse_u      width  reach_q
0   2026-03-04T18:18:19Z  361.3576  0.11020  22.158395        2
1   2026-03-07T07:38:25Z  361.4130  0.13219  16.726829        1
2   2026-03-14T16:40:33Z  363.4491  0.17728   5.955160        1
4   2026-03-25T15:03:24Z  361.7851  0.09722  39.063225        1
5   2026-03-28T04:23:30Z  361.6605  0.09878  67.644206        1
6   2026-04-04T13:25:36Z  363.0315  0.20770  12.528737        1
8   2026-04-15T11:48:30Z  361.5908  0.22554   3.333258        2
9   2026-04-18T01:08:35Z  361.7071  0.09536  94.875687        1
10  2026-04-25T10:10:43Z  362.6727  0.25572   1.683885        1
12  2026-05-06T08:33:34Z  362.3976  0.10424  16.826053        1
13  2026-05-08T21:53:40Z  362.1075  0.09628  83.190460        1
14  2026-05-16T06:55:46Z  361.5462  0.31004   2.148680        1
16  2026-05-27T05:18:38Z  361.3725  0.21452   3.368566        2
17  2026-05-29T18:38:43Z  361.1404  0.09993  34.073105        1
18  2026-06-06T03:40:50Z  361.7221  0.61913   3.423401        1
20  2026-06-17T02:03:43Z  361.1029  0.27695   3.176168        2
21  2026-06-19T15:23:49Z  360.4889  0.11741  39.218237        2
22  2026-06-27T00:25:56Z  362.1417  0.56198   3.645788        1
24  2026-07-07T22:48:47Z  361.5381  0.16648  11.238259        2
25  2026-07-10T12:08:53Z  361.6257  0.15038  32.341170        2
26  2026-07-17T21:10:59Z  360.7636  0.10550  22.531951        1
28  2026-07-28T19:33:50Z  360.4434  0.14849   5.672208        1
```

Every row is one SWOT overpass of the reach, with `wse`, `wse_u` (its uncertainty) and `width` in meters. Hydrocron also adds a `<field>_units` column (for example `wse_units`) giving each **Variable unit**, and the function adds a `time` column parsed as a timestamp for plotting. Hydrocron also returns a row for each overpass that produced no valid measurement. Those rows have `time_str` = `no_data`, a fill value for `wse` and `reach_q` = 3; the function drops them, which is why the index skips some numbers.

SWOT saw this reach 22 times in five months, often in pairs a few days apart, because the reach sits where several passes overlap. Three things stand out:

- **The broad pattern follows the river.** Water surface elevation is higher around the snowmelt peak (362.4 m on May 6, when USGS reported about 3,900 ft³/s) than in late July (360.4 m on July 28, about 490 ft³/s).
- **Some values are clearly off.** On March 14, SWOT reports 363.4 m, the highest in the table, when USGS reported only about 900 ft³/s (USGS marks its March discharge values as estimated; see [USGS daily mean discharge for 05227500](https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily/items?monitoring_location_id=USGS-05227500&parameter_code=00060&statistic_id=00003&time=2026-03-01/2026-07-31)). Most suspicious values share a sign: a measured `width` far below SWORD's expected 36 m (6 m on March 14, 1.7 m on April 25). For a narrow river like this one, comparing `width` with `p_width` is a useful extra screen.
- **No observation is flagged good.** Fifteen are suspect (`reach_q` = 1) and seven degraded (2). A strict `reach_q == 0` filter (`get_reach_timeseries(..., max_reach_q=0)`) would return an empty table. Quality flags are reach-specific, so keep the flag in your analysis and decide what to trust rather than silently filtering everything away.

:::{admonition} TODO (dev team): Verify whether the March 2026 record at…
:class: attention
Verify whether the March 2026 record at 05227500 is ice-affected
:::

:::{admonition} Partner review (NASA): hydrocron
:class: important
Confirm how researchers should use suspect and degraded observations on narrow rivers, and whether screening on `width` versus `p_width` is a reasonable extra check.
:::

:::{admonition} TODO (dev team): Plot the SWOT WSE series against the…
:class: attention
Plot the SWOT WSE series against the USGS NAVD88 stream level (parameter 63160) at 05227500
:::

If a reach ID does not exist in the collection, `hydrocron` answers with an HTTP 400 and a message such as `Results with the specified Feature ID ... were not found`. The function raises that as an error, so a typo doesn't pass silently.

## Best practices FAQs

See sections below for answers and code examples to the following questions.

* What is the recommended way to download data for **one location across the full period of record**?
* What is the recommended way to download data across **all locations for a small time range**?
* If I am working on improving efficiency through **code parallelization**, what should I do vs avoid?

### Temporal scaling

What is the recommended way to download data for one location but the full period of record?

Use `hydrocron`, one request per reach or node. Set `start_time` to the start of the mission's science orbit (July 2023) and `end_time` to today, and ask only for the `fields` you need. Fewer fields keep each response under the 6 MB limit. This replaces downloading every RiverSP granule that ever covered your reach (one per overpass, each covering a whole continent-scale pass) only to keep a single row from each. The CUAHSI longitudinal-profile notebook in Further reading follows this pattern for a single reach.

:::{admonition} TODO (dev team): Verify exact date of first science-orbit RiverSP…
:class: attention
Verify exact date of first science-orbit RiverSP data
:::

### Spatial scaling

What is the recommended way to download data for all locations but a small time range?

Use `earthaccess`. Search by `bounding_box` and a short `temporal` window, then download or stream the granules. One RiverSP granule holds every reach in a half-orbit pass over a continent, and one Raster granule holds a scene about 160 km on a side. That makes a few files the cheapest way to get many locations at once. Looping `hydrocron` over thousands of reach IDs is the wrong tool here: it sends thousands of requests for data that sit in a few files.

### Parallelization

If I am working on improving efficiency of my code through parallelization, what should I do vs avoid?

- **Do** let `earthaccess.download()` handle parallel downloads. It already fetches several files at once (see its `threads` argument).
- **Do** run large `earthaccess` workflows in AWS `us-west-2` (for example, a cloud JupyterHub) and use `earthaccess.open()` to stream data instead of downloading it.
- **Avoid** firing many `hydrocron` requests in parallel. Send them one after another, or a few at a time, and request a `hydrocron` API key from PO.DAAC if you have a heavy or recurring workload.
- **Avoid** re-downloading the same granules every time you run your code. Keep a fixed `local_path=`: `earthaccess.download()` skips files that are already there unless you pass `force=True`.

:::{admonition} Partner review (NASA): Parallelization
:class: important
Confirm these recommendations, in particular the guidance on parallel `hydrocron` requests and when to request an API key.
:::

## Further reading

- [`earthaccess` documentation](https://earthaccess.readthedocs.io/en/latest/), including the [authentication how-to](https://earthaccess.readthedocs.io/en/latest/user/howto/authenticate/).
- [`hydrocron` documentation](https://podaac.github.io/hydrocron/) and the [timeseries endpoint reference](https://podaac.github.io/hydrocron/timeseries).
- [PO.DAAC Cookbook: SWOT tutorials](https://podaac.github.io/tutorials/quarto_text/SWOT.html), including [Hydrocron API: Getting Started with SWOT Time Series](https://podaac.github.io/tutorials/notebooks/datasets/Hydrocron_SWOT_timeseries_examples_basic.html) by Nikki Tebaldi, Cassandra Nickles and Brandi Downs, which works through Skagit River reaches in Washington.
- [SWOT Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf) (PO.DAAC).
- [Hydrocron: a new tool for SWOT time series analysis](https://www.earthdata.nasa.gov/news/hydrocron-new-tool-swot-time-series-analysis) (NASA Earthdata).
- [earthaccess tech spotlight](https://nasa-openscapes.github.io/news/2024-03-04-earthaccess-tech-spotlight/) (NASA Openscapes).
- [SWORD Explorer](https://www.swordexplorer.com/) for finding reach and node IDs interactively.
- Adapted from [SWOT - River Longitudinal Profiles for Water Resources](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/SWOT%20-%20River%20Longitudinal%20Profiles%20for%20Water%20Resources) by Mike Durand, with contributions from Bidhya Yadav (Ohio State University), CUAHSI notebooks (GPL-3.0). The `get_reach_timeseries` function adapts its `PullReachTimeseries` helper.
