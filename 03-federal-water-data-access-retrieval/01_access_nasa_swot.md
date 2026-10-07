# Retrieve NASA SWOT water surface elevation data

There are many ways to find, access, and download NASA SWOT data. This module is going to spend the most time focusing on the recommended patterns for hydrology applications using the water surface elevation (`wse`) data from the SWOT mission. To help build the framework, you need to know that there are two ways to programmatically get access to SWOT data:

1. `earthaccess`: this is a Python library that allows users to access all of the NASA Earthdata stored in the cloud, including SWOT mission data. It streamlined what used to be complex access patterns across different systems and tools in order to help scientists get to the data faster (see more in [this blog post](https://nasa-openscapes.github.io/news/2024-03-04-earthaccess-tech-spotlight/)). Using `earthaccess`, a user can easily authenticate using the Earthdata login, find what data is available, and download or access a variety of products in NASA's cloud storage buckets.
1. `hydrocron`: this is an API built specifically to help streamline timeseries data access to the `SWOT_L2_HR_RIVERSP` data product. The queries allow users to access data across temporal ranges for specific locations, which is in contrast to how the SWOT data are archived (individual shapefiles per timestamp). It allows users who may be interested in a timeseries of data at a small number of locations the ability to easily retrieve that without a lot of extra effort. More on how `hydrocron` works is available in [this NASA news article](https://www.earthdata.nasa.gov/news/hydrocron-new-tool-swot-time-series-analysis).

This lesson uses two SWOT hydrology products. They answer different questions, so pick the product before you pick the tool:

| Your question | Product | Short name (Version D) | What you get | Tool |
|---|---|---|---|---|
| How did the water surface elevation (and width) of a river reach change over time? | River single-pass vector (RiverSP) | `SWOT_L2_HR_RiverSP_reach_D` / `_node_D` | One row per reach (~10 km) or node (~200 m) per overpass: `wse`, `width`, quality flags | `hydrocron` for time series at a few reaches; `earthaccess` for every reach in an area |
| Where was there water, and how much area did it cover, on a given overpass? | Water mask raster (Raster) | `SWOT_L2_HR_Raster_100m_D` (also `_250m_D`) | A gridded (UTM, 100 m or 250 m) scene per overpass: `water_area`, `water_frac`, `wse` and their quality flags | `earthaccess` + `xarray` |

RiverSP is tied to the [SWOT River Database (SWORD)](https://www.swordexplorer.com/) river centerlines, so it describes the channel. It does not tell you how far water spread out of bank. Raster is not tied to a river network, so it can show water anywhere in the scene, including floodplains. We use both for the December 2025 Skagit River flood in [Module 4](../04-federal-water-data-synthesis/02_synthesize_river_data.md).
[PARTNER REVIEW: NASA] Confirm this "which product for which question" framing and the description of what RiverSP does not capture out of bank.

## Tools and environment setup

In order to complete this lesson about accessing NASA SWOT water surface elevation data, you first need to install a few libraries and create an account.

1. **Make an Earthdata Login account.** In order to _access_ data from the NASA Earthdata system, you will need to create an Earthdata Login account. Please visit [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov) to register and setup your login. 
2. **Create the course environment.** We will be using the NASA `earthaccess` Python library for programmatic authentication to NASA Earthdata systems, data discovery, and data downloads, plus `xarray`, `geopandas` and `requests` for reading the files and calling `hydrocron`. The course provides a conda environment file, `environments/swot.yml` (in the course repository), with everything this lesson uses. `mamba` is faster, but `conda` works the same way. To install `earthaccess` on its own instead, see its [user quick start guide](https://earthaccess.readthedocs.io/en/latest/user/quick-start/#installing-earthaccess).

```bash
# From the root of the course repository
mamba env create -f environments/swot.yml   # or: conda env create -f environments/swot.yml
conda activate fwdc-swot
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
# Find available granules (aka "files") in June 2026 that cover the headwaters of the Mississippi River
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

A few things to know about `search_data` (see the [`earthaccess` API docs](https://earthaccess.readthedocs.io/en/latest/api/) for every option):

- **`temporal`** takes a `(start, end)` pair of strings or `datetime` objects. A month such as `("2026-06", "2026-06")` covers the whole month (42 granules here, the same as `("2026-06-01", "2026-06-30T23:59:59")`), but a single day written as `("2026-06-01", "2026-06-01")` means one instant at midnight and finds nothing. Write full dates and times when you need to be precise.
- **`bounding_box`** is `(west, south, east, north)` in decimal degrees. Swapping the order is a common mistake.
- **`count`** limits how many granules are returned, which is handy while you are exploring.
- **A query that matches nothing returns an empty list, not an error.** A misspelled `short_name`, a bounding box with latitude and longitude swapped, or a date before the mission began all give `[]`. Always check `len()` before moving on. (Short names are not case-sensitive, so `_reach_d` still works; a misspelling does not.)

```python
# A typo in the short name does not raise an error -- it just finds nothing
len(earthaccess.search_data(short_name="SWOT_L2_HR_RiverSP_rech_D", count=5))  # 0
```

The water-area product is discovered the same way. Here we search the 100 m Raster product around USGS gage 12200500 on the Skagit River near Mount Vernon, WA, for the weeks around the December 2025 flood that we study in Module 4:

```python
# A small box (about 3 km across) around USGS 12200500, Skagit River near Mount Vernon, WA
skagit_bbox = (-122.355, 48.425, -122.315, 48.465)

skagit_raster = earthaccess.search_data(
    short_name="SWOT_L2_HR_Raster_100m_D",
    bounding_box=skagit_bbox,
    temporal=("2025-11-15", "2025-12-31"),
)
print(len(skagit_raster), "granules")
print(sorted({g["umm"]["GranuleUR"].split("_")[5] for g in skagit_raster}))  # the UTM zone + band of each scene
```

```
49 granules
['UTM01C', 'UTM01W', 'UTM10U', 'UTM60C', 'UTM60V', 'UTM60W']
```

About 50 granules (49 at time of writing) is far more than SWOT could have seen over one gage in six weeks. The UTM zone in each name gives the problem away: Mount Vernon, WA is in UTM zone **10**, but most results are in zones 01 and 60, on either side of the antimeridian (180° longitude). Their footprints wrap around the globe, so they falsely "intersect" almost any bounding box. Always sanity-check search results before downloading: here that would have been about 3 GB of files from the wrong side of the planet. Keep only the zone-10 scenes, and where a scene was processed more than once, keep the highest processing counter:

```python
# Keep scenes in UTM zone 10 (the Skagit), then keep the latest processing of each scene
zone10 = [g for g in skagit_raster if "_UTM10" in g["umm"]["GranuleUR"]]
latest = {}
for g in sorted(zone10, key=lambda g: g["umm"]["GranuleUR"]):
    scene = g["umm"]["GranuleUR"].rsplit("_", 2)[0]  # name without the processing counter
    latest[scene] = g
skagit_raster = list(latest.values())
for g in skagit_raster:
    print(g["umm"]["GranuleUR"], round(g.size, 1), "MB")
```

```
SWOT_L2_HR_Raster_100m_UTM10U_N_x_x_x_041_552_035F_20251121T121537_20251121T121558_PID0_01_swot 65.1 MB
SWOT_L2_HR_Raster_100m_UTM10U_N_x_x_x_042_246_035F_20251201T103754_20251201T103815_PID0_01_swot 62.8 MB
SWOT_L2_HR_Raster_100m_UTM10U_N_x_x_x_042_345_120F_20251204T235932_20251204T235953_PID0_01_swot 67.4 MB
SWOT_L2_HR_Raster_100m_UTM10U_N_x_x_x_042_552_035F_20251212T090040_20251212T090101_PID0_01_swot 68.8 MB
SWOT_L2_HR_Raster_100m_UTM10U_N_x_x_x_043_246_035F_20251222T072258_20251222T072319_PID0_02_swot 62.7 MB
SWOT_L2_HR_Raster_100m_UTM10U_N_x_x_x_043_345_120F_20251225T204438_20251225T204459_PID0_01_swot 68.1 MB
```

The Raster name adds the UTM zone and latitude band (`UTM10U`) and a scene number (`035F`, `120F`) to the cycle, pass and time.

[PARTNER REVIEW: NASA] Is the antimeridian false-match behavior a known CMR/`earthaccess` issue with a recommended fix (for example, a polygon search, or a granule-name filter like the one above)?

Behind the scenes, `earthaccess` is querying NASA's [Common Metadata Repository (CMR)](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html) and, when you download, reading from the PO.DAAC cloud archive in Amazon Web Services (AWS) `us-west-2`. You don't need to know either system to use `earthaccess`, but it helps when you read other tutorials that call them directly.

## Programmatic data downloads

Discovery told us _which_ granules exist. Now we get the data. The two tools behave differently:

- `earthaccess` gives you **whole files**: one granule per overpass, covering a large area. `earthaccess.download()` copies them to your computer. `earthaccess.open()` streams them instead. Streaming is most efficient when your code runs in the same cloud region as the data (AWS `us-west-2`), which is why NASA calls this _cloud-native_ access. On a laptop, downloading a handful of files is usually simpler and just as fast.
- `hydrocron` gives you **just the rows you ask for**: the values for one reach or node, across many overpasses, in a single web request. Nothing is downloaded but the answer.

### `earthaccess`

`earthaccess` works for every SWOT product. The file format depends on the product: RiverSP granules are zipped shapefiles (read them with `geopandas`), and Raster granules are NetCDF files (read them with `xarray`).

**RiverSP reaches.** We download one RiverSP reach granule over the Skagit gage and find the SWORD reach closest to it. This is also how you find a `reach_id` to use with `hydrocron` below if you don't already have one. (You can also look up reach IDs interactively in [SWORD Explorer](https://www.swordexplorer.com/).)

```python
import geopandas as gpd
from shapely.geometry import Point

skagit_reach_granules = earthaccess.search_data(
    short_name="SWOT_L2_HR_RiverSP_reach_D",
    bounding_box=skagit_bbox,
    temporal=("2025-12-01", "2025-12-31"),
)
files = earthaccess.download(skagit_reach_granules[:1], local_path="data/swot")

reaches = gpd.read_file(files[0])  # geopandas reads the zipped shapefile directly
print(len(reaches), "reaches in this granule")

# Distance from each reach to the gage, in meters (UTM zone 10N)
gage = gpd.GeoSeries([Point(-122.3354, 48.4448)], crs="EPSG:4326").to_crs(32610).iloc[0]
reaches_utm = reaches.to_crs(32610)
reaches_utm["dist_to_gage_m"] = reaches_utm.distance(gage)
reaches_utm.nsmallest(3, "dist_to_gage_m")[["reach_id", "river_name", "dist_to_gage_m", "wse", "width", "reach_q", "time_str"]]
```

```
303 reaches in this granule
        reach_id    river_name  dist_to_gage_m     wse       width  reach_q              time_str
117  78310800031  Skagit River        3.386485  5.4848  189.069678        2  2025-12-01T10:37:59Z
116  78310800021  Skagit River     1151.133741  3.1370  189.720561        2  2025-12-01T10:37:59Z
103  78310700025       no_data     6776.970430  1.3255  120.554252        1  2025-12-01T10:38:01Z
```

The gage sits on reach **`78310800031`**, the Skagit River reach just upstream of the delta (it is one of the reaches used in the PO.DAAC Hydrocron tutorial listed under Further reading). The granule itself holds every reach SWOT observed along this pass, 303 in total. RiverSP granules carry many more columns than shown here (about 130); the [product description document](https://podaac.github.io/tutorials/quarto_text/SWOT.html) defines them all.

Each row is one SWORD reach seen on this overpass. Key columns:
- `reach_id` is the **Location Identifier**.
- `wse` (water surface elevation, meters above the EGM2008 geoid) and `width` (meters) are the main **Variables**.
- `wse_u` and `width_u` give each value's uncertainty.
- `reach_q` is the summary **Data Quality Flag**: 0 = good, 1 = suspect, 2 = degraded, 3 = bad.
- Missing values are stored as `-999999999999`, not as `NaN`. Filter them out before plotting.

[PARTNER REVIEW: NASA] Confirm the reach_q value meanings and the EGM2008 vertical reference for Version D RiverSP `wse`.

**Raster water area.** Next, download the six Raster granules we kept (about 400 MB in total) and open one with `xarray`. Each file is a fixed scene, about 160 km on a side, on a 100 m UTM grid. A single file therefore covers the whole lower Skagit floodplain, if the overpass saw it.

```python
import xarray as xr

raster_files = earthaccess.download(skagit_raster, local_path="data/swot")
ds = xr.open_dataset(raster_files[1])  # the December 1 overpass
ds[["water_area", "water_frac", "wse", "water_area_qual"]]
```

```
<xarray.Dataset> Size: 41MB
Dimensions:          (y: 1596, x: 1597)
Coordinates:
  * y                (y) float64 13kB 5.261e+06 5.261e+06 ... 5.42e+06 5.42e+06
  * x                (x) float64 13kB 4.953e+05 4.954e+05 ... 6.549e+05
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
    x_min:                         495300.0
    x_max:                         654900.0
    y_min:                         5260800.0
    y_max:                         5420300.0
    institution:                   CNES
```

For each 100 m pixel:
- `water_area` (m²) is the surface area of water in the pixel. A pixel that is fully water is about 10,000 m².
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

def water_area_near(path, lon=-122.3354, lat=48.4448, half_width_m=5000):
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
0  2025-11-21T12:15                0                   0             0.0
1  2025-12-01T10:37             6175                   3            17.9
2  2025-12-04T23:59             8208                1318            64.4
3  2025-12-12T09:00                0                   0             0.0
4  2025-12-22T07:22             7683                   2            35.5
5  2025-12-25T20:44             8414                1595            71.2
```

There are three lessons in this small table:

1. **A granule in your search results is not a guaranteed observation of your site.** The November 21 and December 12 scenes (pass 552) intersect the search box in their metadata, but neither has a single observed pixel within 5 km of the gage. Unfortunately, December 12 was the day of the flood peak (USGS daily mean discharge of about 112,000 ft³/s). SWOT did not see the gage reach that day.
2. **Compare like with like.** The gage sits in the overlap of two different passes: pass 246 (scene `035F`; Dec 1 and Dec 22) and pass 345 (scene `120F`; Dec 4 and Dec 25). The pass-345 scenes show far more water and many more bad-flagged pixels. On December 4, USGS reported a daily mean of about 13,600 ft³/s, slightly *less* than on December 1 (about 14,200 ft³/s), yet that scene shows 64 km² of water against 18 km² on December 1. Within pass 246, water area roughly doubles from December 1 to December 22, when discharge was about 36,400 ft³/s on the falling limb of the flood.
3. **Check satellite numbers against an independent source.** A gage, an aerial image, or simply the other pass will tell you when a value is physically implausible.

USGS discharge values are from the [USGS Water Data API](https://api.waterdata.usgs.gov/ogcapi/v0/) daily values for 12200500 (approved). Module 3's USGS lesson shows how to retrieve them.
[PARTNER REVIEW: NASA] Why do the pass-345 (scene 120F) Raster and RiverSP values over the lower Skagit read so much higher than pass 246 at similar discharge, e.g. layover, near-nadir geometry, or wet floodplain soils? Is there a recommended way to screen this beyond `water_area_qual`?

[PARTNER REVIEW: NASA] Confirm the interpretation of `water_area` values far above pixel area when `water_area_qual` = 3, and whether `water_area_qual <= 1` is the recommended filter for flood-extent work.

Module 4 maps these scenes to show how far the Skagit spread out of bank during the flood.

### `hydrocron`

While a user can access SWOT data through `earthaccess`, if timeseries data for specific rivers are the desired outcome, then the `hydrocron` API is the tool for the job. As the [`hydrocron` documentation](https://podaac.github.io/hydrocron) states, 

> SWOT data is archived as individually timestamped shapefiles, which would otherwise require users to perform potentially thousands of file IO operations per river feature to view the data as a timeseries. Hydrocron makes this possible with a single API call.

`hydrocron` is a web API, so there is nothing extra to install: any HTTP client works, and we use `requests`. You do not need an Earthdata login or an API key for normal use. PO.DAAC offers optional keys for heavy use, sent in an `x-hydrocron-key` header. One request returns one feature (a reach, node or lake) over a time range, and responses are capped at 6 MB. See the [`hydrocron` timeseries documentation](https://podaac.github.io/hydrocron/timeseries) for every parameter. The main ones:

| Parameter | Example | Notes |
|---|---|---|
| `feature` | `Reach` | `Reach`, `Node` or `PriorLake` |
| `feature_id` | `78310800041` | SWORD reach or node ID (the **Location Identifier**) |
| `start_time`, `end_time` | `2025-11-01T00:00:00Z` | UTC |
| `fields` | `reach_id,time_str,wse,wse_u,width,reach_q` | Only the columns you need |
| `output` | `csv` | `csv` or `geojson`, returned inside a JSON response |
| `collection_name` | `SWOT_L2_HR_RiverSP_D` | Optional; defaults to Version D. Version C (`2.0`) reach IDs can differ |

The function below, adapted from the CUAHSI longitudinal-profile notebook (see Further reading), wraps one request and returns a `pandas` DataFrame. It drops overpasses with no valid measurement (fill values), and by default keeps everything else. Pass `max_reach_q` to also drop observations whose quality flag is worse than you can accept.

```python
import io
import pandas as pd
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

skagit = get_reach_timeseries("78310800031", "2025-11-01T00:00:00Z", "2026-01-15T00:00:00Z")
skagit[["time_str", "wse", "wse_u", "width", "reach_q"]]
```

```
               time_str      wse    wse_u       width  reach_q
0  2025-11-10T13:52:55Z   5.7195  0.10003  204.727292        2
1  2025-11-14T03:14:43Z   8.9412  0.25796  423.549286        2
3  2025-12-01T10:37:59Z   5.4848  0.09484  189.069678        2
4  2025-12-04T23:59:47Z  17.2989  0.66000  648.645378        2
6  2025-12-22T07:23:03Z   7.9524  0.09502  340.979469        2
7  2025-12-25T20:44:52Z   8.7892  0.32216  381.462596        2
9  2026-01-12T04:08:08Z   6.0671  0.11089  242.501993        2
```

Every row is one SWOT overpass of the reach, with `wse`, `wse_u` (its uncertainty) and `width` in meters. Hydrocron also returns a row for each overpass that produced no valid measurement. Those rows have `time_str` = `no_data`, a fill value for `wse` and `reach_q` = 3; the function drops them, which is why the index skips 2, 5 and 8.

Two things stand out:

- **Every observation of this reach is flagged `reach_q` = 2 (degraded).** If you had filtered to `reach_q <= 1`, as many tutorials do (`get_reach_timeseries(..., max_reach_q=1)`), you would get an empty table. Quality flags are reach-specific. For a narrow (~200 m) reach like this one, "degraded" may be the best SWOT offers. Keep the flag in your analysis and decide what to trust, rather than silently filtering everything away. The Raster results above for the same overpasses are a helpful cross-check.
- **The December 4 value (17.3 m, ±0.66 m) is about 12 m higher than December 1 at almost the same discharge.** It is the same pass-345 overpass whose Raster scene over-detected water. Its uncertainty, `wse_u`, is also the largest in the table. Treat it as an outlier.

[PARTNER REVIEW: NASA] Confirm why this reach is consistently `reach_q` = 2 and how NASA recommends researchers use degraded observations.

If a reach ID does not exist in the collection, `hydrocron` answers with an HTTP 400 and a message such as `Results with the specified Feature ID ... were not found`. The function raises that as an error, so a typo doesn't pass silently.

## Best practices FAQs

See sections below for answers and code examples to the following questions.

* What is the recommended way to download data for **one location across the full period of record**?
* What is the recommended way to download data across **all locations for a small time range**?
* If I am working on improving efficiency through **code parallelization**, what should I do vs avoid?

### Temporal scaling

What is the recommended way to download data for one location but the full period of record?

Use `hydrocron`, one request per reach or node. Set `start_time` to the start of the mission's science orbit (July 2023 [TODO: verify exact date of first science-orbit RiverSP data]) and `end_time` to today, and ask only for the `fields` you need. Fewer fields keep each response under the 6 MB limit. This replaces downloading every RiverSP granule that ever covered your reach (one per overpass, each covering a whole continent-scale pass) only to keep a single row from each. The CUAHSI longitudinal-profile notebook in Further reading follows this pattern for a single reach.

### Spatial scaling

What is the recommended way to download data for all locations but a small time range?

Use `earthaccess`. Search by `bounding_box` and a short `temporal` window, then download or stream the granules. One RiverSP granule holds every reach in a half-orbit pass over a continent, and one Raster granule holds a scene about 160 km on a side. That makes a few files the cheapest way to get many locations at once. Looping `hydrocron` over thousands of reach IDs is the wrong tool here: it sends thousands of requests for data that sit in a few files.

### Parallelization

If I am working on improving efficiency of my code through parallelization, what should I do vs avoid?

- **Do** let `earthaccess.download()` handle parallel downloads. It already fetches several files at once (see its `threads` argument).
- **Do** run large `earthaccess` workflows in AWS `us-west-2` (for example, a cloud JupyterHub) and use `earthaccess.open()` to stream data instead of downloading it.
- **Avoid** firing many `hydrocron` requests in parallel. Send them one after another, or a few at a time, and request a `hydrocron` API key from PO.DAAC if you have a heavy or recurring workload.
- **Avoid** re-downloading the same granules every time you run your code. Save them locally (`local_path=`) and check for the file first.

[PARTNER REVIEW: NASA] Confirm these recommendations, in particular the guidance on parallel `hydrocron` requests and when to request an API key.

## Further reading

- [`earthaccess` documentation](https://earthaccess.readthedocs.io/en/latest/), including the [authentication how-to](https://earthaccess.readthedocs.io/en/latest/user/howto/authenticate/).
- [`hydrocron` documentation](https://podaac.github.io/hydrocron/) and the [timeseries endpoint reference](https://podaac.github.io/hydrocron/timeseries).
- [PO.DAAC Cookbook: SWOT tutorials](https://podaac.github.io/tutorials/quarto_text/SWOT.html), including [Hydrocron API: Getting Started with SWOT Time Series](https://podaac.github.io/tutorials/notebooks/datasets/Hydrocron_SWOT_timeseries_examples_basic.html) by Nikki Tebaldi, Cassandra Nickles and Brandi Downs, which uses the same Skagit River reaches.
- [SWOT Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf) (PO.DAAC).
- [Hydrocron: a new tool for SWOT time series analysis](https://www.earthdata.nasa.gov/news/hydrocron-new-tool-swot-time-series-analysis) (NASA Earthdata).
- [earthaccess tech spotlight](https://nasa-openscapes.github.io/news/2024-03-04-earthaccess-tech-spotlight/) (NASA Openscapes).
- [SWORD Explorer](https://www.swordexplorer.com/) for finding reach and node IDs interactively.
- The `get_reach_timeseries` function is adapted from `PullReachTimeseries` in [SWOT - River Longitudinal Profiles for Water Resources](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/SWOT%20-%20River%20Longitudinal%20Profiles%20for%20Water%20Resources) by Mike Durand, with contributions from Bidhya Yadav (Ohio State University), CUAHSI notebooks (GPL-3.0).
