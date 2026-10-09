# Retrieve NASA SWOT data

In this lesson you retrieve river data from the *NASA Surface Water and Ocean Topography ({term}`SWOT`)* mission with Python: you find
the files that cover a river, download them, and pull a water surface elevation time series for one river reach. You met
SWOT, its products and its quality flags in [Meet NASA SWOT](../02-federal-water-data-landscape/01_meet_nasa_swot.md). Here
you put that into code.

**The example river.** The main example is the **Ohio River at Louisville, Kentucky**, from 15 March to 15 May 2025. The Ohio
is about 700 m wide here, well above the roughly 100 m that SWOT observes reliably, and SWOT passes over Louisville several times in each
21-day cycle. The window includes the large April 2025 flood, so you can watch the river's water surface rise and fall in
SWOT's own data. At the end you repeat the steps on a second river, the Willamette River at Salem, Oregon.

:::{figure} ../images/m03/swot-location-map.png
:alt: Two maps. Left, a map of thin gray lines tracing rivers across a diagonal strip of North America from Central America to northern Canada, with a red star at Louisville, Kentucky. Right, a close-up of about 40 km of the Ohio River around Louisville, with three river reaches drawn in color and labeled with their reach IDs, and the red star on the middle reach.
:width: 100%

Where the lesson's data come from. **Left:** every SWORD river reach in one SWOT RiverSP granule (cycle 031, pass 175,
13 April 2025; a *cycle* is one 21-day repeat of SWOT's orbit and a *pass* is one numbered track within it). One granule covers a whole pass across a continent. **Right:** the three reaches nearest the example point on
the Ohio River at Louisville (red star). The point lies on reach `74267300251`. Data: NASA SWOT Level 2 River Single-Pass
Vector product, Version D ([doi:10.5067/SWOT-RIVERSP-D](https://doi.org/10.5067/SWOT-RIVERSP-D)), accessed 2026-10-08.
:::

(swot-access-routes)=
## Choosing an access route

SWOT has two hydrology products you will use. They answer different questions, so pick the product before you pick the tool:

| Your question | Product | Collection short name (Version D) | What you get |
|---|---|---|---|
| How did a river reach's water surface elevation (and width) change over time? | River single-pass vector (**RiverSP**) | `SWOT_L2_HR_RiverSP_D` (reaches and nodes) | One row per {term}`reach <Reach>` (~10 km) or {term}`node <Node>` (~200 m) per overpass: `wse`, `width`, quality flags |
| Where was there water, and how much area did it cover, on one overpass? | Water mask raster (**Raster**) | `SWOT_L2_HR_Raster_100m_D` (also `_250m_D`) | A gridded scene (100 m or 250 m pixels) per overpass: `water_area`, `water_frac`, `wse` and their quality flags |

RiverSP is tied to the river centerlines of the {term}`SWOT River Database (SWORD) <SWORD>`, so it describes the channel. It
does not tell you how far water spread out of bank. Raster is not tied to a river network, so it can show water anywhere in
the scene, including floodplains.

There are two ways to get these products with code, and they scale differently:

| Use case | Recommended route | Key needed? | Scaling limits |
|---|---|---|---|
| Explore by clicking: which granules exist for a place and time | [Earthdata Search](https://search.earthdata.nasa.gov/) | Free Earthdata Login to download | Manual; not reproducible on its own |
| Time series for one or a few reaches or nodes, any length of record | {term}`hydrocron` web API (RiverSP only) | No (optional for heavy use) | One request per reach or node; responses are capped at 6 MB; send requests one at a time |
| Every reach in an area, or water extent (Raster), for a short time window | {term}`earthaccess` (search, then download or stream whole files) | No key; free Earthdata Login | Cost grows with the number of files: each RiverSP {term}`granule <Granule>` covers a continent-wide pass, each Raster granule a ~150 km scene |
| Large areas or long periods of Raster or RiverSP files | `earthaccess.open()` running in AWS `us-west-2`, next to the archive | No key; free Earthdata Login | Streams instead of downloading; set up a cloud environment first |

- **`earthaccess`** is NASA's Python library for logging in to NASA Earthdata, searching for data, and downloading or
  streaming the files. It works for every SWOT product. It replaced what used to be several different access patterns
  ([earthaccess tech spotlight](https://nasa-openscapes.github.io/news/2024-03-04-earthaccess-tech-spotlight/)).
- **`hydrocron`** is a web API from NASA's {term}`PO.DAAC` that returns a RiverSP time series for one reach or node in a
  single request. SWOT files are archived one per overpass, so without it you would open one file per overpass to build a
  time series ([Hydrocron: a new tool for SWOT time series analysis](https://www.earthdata.nasa.gov/news/hydrocron-new-tool-swot-time-series-analysis)).

**Only need a time series for one reach?** Find its reach ID in [SWORD Explorer](https://www.swordexplorer.com/), run the
setup and query blocks, and skip to [RiverSP time series with `hydrocron`](#swot-hydrocron). That section doesn't need an
Earthdata login or any downloads.

:::{admonition} Partner review (NASA): Choosing an access route
:class: important
Confirm this "which product, which route" framing, the scaling limits in the table, and the description of what RiverSP does not capture out of bank.
:::

## Tools and environment setup

You need a free account and a Python environment.

1. **Make an Earthdata Login account.** Downloading SWOT files requires one. Register at
   [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov). (`hydrocron` does not need it.)
2. **Create the lesson's environment.** The course provides a {term}`conda environment <Conda environment>` file,
   `environments/m03-swot.yml` (in the course repository), with every package this lesson uses: `earthaccess` for login,
   search and download; `geopandas` for the RiverSP shapefiles; `xarray` for the Raster NetCDF files; `requests` and `pandas`
   for `hydrocron`; and `matplotlib` for plots. The file pins the Python version but lets most packages float to their latest
   release, so you may get newer versions than the ones we tested; record what you actually ran (below) and keep it with
   your results (see [Reproducibility techniques](../01-data-best-practices/02_data_management.md#reproducibility-techniques) in
   Module 1). `mamba` is faster, but `conda` works the same way.

```bash
# From the root of the course repository
mamba env create -f environments/m03-swot.yml   # or: conda env create -f environments/m03-swot.yml
conda activate m03-swot

# Optional: register this environment as a Jupyter kernel, then pick "Python (m03-swot)" in Jupyter
python -m ipykernel install --user --name m03-swot --display-name "Python (m03-swot)"
```

If you work in Jupyter, choose the `Python (m03-swot)` kernel; otherwise your notebook runs in a different environment and
imports such as `earthaccess` fail.

Record the versions you actually ran with, so you (or a reviewer) can rebuild the same setup later. This prints the ones that
matter most here:

```python
# Print the versions of the key packages (save this with your results)
import earthaccess, geopandas, matplotlib, pandas, xarray
for package in (earthaccess, geopandas, matplotlib, pandas, xarray):
    print(package.__name__, package.__version__)
```

```
earthaccess 0.19.0
geopandas 1.2.0
matplotlib 3.11.2
pandas 3.0.6
xarray 2026.9.0
```

To log in with `earthaccess`, run the following. If you have not stored your credentials, it prompts for your Earthdata
username and password. To avoid typing them each time, set the `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` environment
variables (or use a `.netrc` file); `earthaccess.login()` finds them automatically. Never write your password into a script
or notebook. If you're not sure how to set environment variables, let it prompt you; that's fine for this lesson. See the [`earthaccess` authentication how-to](https://earthaccess.readthedocs.io/en/latest/user/howto/authenticate/).

```python
import earthaccess

# Log in to NASA Earthdata. Uses EARTHDATA_USERNAME/EARTHDATA_PASSWORD or .netrc if set, otherwise prompts.
auth = earthaccess.login()
auth.authenticated  # True once you are logged in
```

```
True
```

> **Known install issue:** `import earthaccess` can fail with an SSL error (`ASN1: NOT_ENOUGH_DATA`) on older Python and
> newer OpenSSL combinations ([details](https://github.com/python/cpython/issues/151504)). **Fix:** use Python 3.12 or later
> (the course environment uses 3.14).

Last, put everything that defines your query in one place. Every later block reads these variables, so changing the river or
the dates means editing only this block, and saving it records exactly what you asked for.

```python
# The lesson's query, in one place. Change these to use another river.
site_name = "Ohio River at Louisville, KY"
site_lon, site_lat = -85.799, 38.280          # a point on the river (decimal degrees, WGS84)
site_bbox = (site_lon - 0.02, site_lat - 0.02, site_lon + 0.02, site_lat + 0.02)  # (west, south, east, north), ~3.5 x 4.4 km
start, end = "2025-03-15T00:00:00Z", "2025-05-15T23:59:59Z"   # UTC; the April 2025 flood falls inside
reach_id = "74267300251"                      # SWORD reach at the point (found below, or look it up in SWORD Explorer)
data_dir = "data/swot/raw"                    # downloads go here and are never edited
```

The dates are full UTC timestamps (`Z` means UTC) because both `earthaccess` and `hydrocron` accept that form. You won't
know `reach_id` for a new river yet: the RiverSP download below shows how to find it.

## Programmatic data discovery

Before downloading anything, find out what exists: which datasets cover your river, and which files (granules) fall in your
time window. Downloading a whole archive just to learn which dates it holds would be slow and wasteful. Discovery also gives
you the exact granule names, which you can save as a record of your inputs.

### The point-and-click equivalent

You can do the same search in [Earthdata Search](https://search.earthdata.nasa.gov/): type a collection short name such as
`SWOT_L2_HR_Raster_100m_D` in the search box, draw a rectangle around your river, set the dates, and the page lists the
matching granules. That is a good way to explore. Code is better for research, because the search itself becomes part of
your methods and can be re-run.

### Find datasets

If you don't yet know which dataset you need, search the catalog broadly with `search_datasets` (see the
[`earthaccess` API docs](https://earthaccess.readthedocs.io/en/latest/api/) for every option). A keyword alone matches more
than 1,500 datasets, so add your area and dates and keep only cloud-hosted ones:

```python
# Datasets matching "river" that are in the cloud and cover the site during the window
river_datasets = earthaccess.search_datasets(
    keyword="river",
    cloud_hosted=True,
    bounding_box=site_bbox,
    temporal=(start, end),
)
short_names = [d["umm"]["ShortName"] for d in river_datasets]
print(len(short_names), "datasets;", "SWOT ones:")
sorted(name for name in short_names if name.startswith("SWOT"))
```

```
47 datasets; SWOT ones:
['SWOT_L2_HR_LakeSP_2.0', 'SWOT_L2_HR_LakeSP_obs_2.0', 'SWOT_L2_HR_LakeSP_prior_2.0', 'SWOT_L2_HR_LakeSP_unassigned_2.0',
 'SWOT_L2_HR_PIXCVec_2.0', 'SWOT_L2_HR_PIXCVec_D', 'SWOT_L2_HR_PIXC_D', 'SWOT_L2_HR_RiverAvg_2.0', 'SWOT_L2_HR_RiverAvg_D',
 'SWOT_L2_HR_RiverSP_2.0', 'SWOT_L2_HR_RiverSP_D', 'SWOT_L2_HR_RiverSP_node_2.0', 'SWOT_L2_HR_RiverSP_node_D',
 'SWOT_L2_HR_RiverSP_reach_2.0', 'SWOT_L2_HR_RiverSP_reach_D', 'SWOT_L4_HR_DAWG_SOS_DISCHARGE_V3']
```

Each result is a *collection*. Its **short name** is what you pass to the other `earthaccess` functions. A few patterns help
you read the list:

- **Version.** Names ending in `_D` are **Version D**, the current release. Names ending in `_2.0` are the older Version C.
  Use Version D ([SWOT Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf), section 4.1).
- **Sub-collections.** `SWOT_L2_HR_RiverSP_D` holds both reach and node files; `_reach_D` and `_node_D` are sub-collections
  with one kind each.
- **Raster isn't here**: it doesn't match this keyword search. Searching for `keyword="SWOT"` finds it.

### A river with no SWOT reaches: the Mississippi headwaters

`search_data` finds the granules inside one collection. A quick lesson first: **a granule in your results is not a
guaranteed observation of your site.** Each RiverSP granule covers a whole pass across a continent, so its footprint can
"intersect" a small box even when SWOT measured no river there. Here is a box at the Mississippi River headwaters in
Minnesota, a small stream at that point:

```python
import geopandas as gpd
from shapely.geometry import box

headwaters_box = (-95.26, 47.17, -95.15, 47.25)  # (west, south, east, north) at Lake Itasca, MN
headwaters = earthaccess.search_data(
    short_name="SWOT_L2_HR_RiverSP_D",
    granule_name="*Reach*",          # reach files only (this collection also holds node files)
    bounding_box=headwaters_box,
    temporal=("2026-06-01", "2026-06-30T23:59:59"),
)
print(len(headwaters), "reach granules found")
files = earthaccess.download(headwaters[:1], local_path=data_dir)
reaches = gpd.read_file(files[0])  # geopandas reads the zipped shapefile directly
print(len(reaches), "reaches in the first granule;", int(reaches.intersects(box(*headwaters_box)).sum()), "inside the box")
```

```
42 reach granules found
650 reaches in the first granule; 0 inside the box
```

None of the reaches in this granule are in the box, and the same is true for all 42 June 2026 granules (we checked each one).
The problem is not SWOT's orbit: SWORD, the river network that RiverSP reports on, has no reaches in this box. The Mississippi
here is a small stream, far narrower than the rivers SWOT is built to measure
([Meet NASA SWOT](../02-federal-water-data-landscape/01_meet_nasa_swot.md)). Always open one file and check before you
download many.

:::{admonition} TODO (dev team): SWORD upstream end on the Mississippi
:class: attention
Verify where SWORD's Mississippi River reaches begin (upstream end) with SWORD Explorer, and add it here.
:::

### Find Raster granules over the Ohio at Louisville

Now search the 100 m Raster product in the small box around the example point:

```python
louisville_raster = earthaccess.search_data(
    short_name="SWOT_L2_HR_Raster_100m_D",
    bounding_box=site_bbox,
    temporal=(start, end),
)
print(len(louisville_raster), "granules")
print(sorted({g["umm"]["GranuleUR"].split("_")[5] for g in louisville_raster}))  # the UTM zone + band in each name
```

```
44 granules
['UTM01C', 'UTM01W', 'UTM16S', 'UTM60C', 'UTM60V', 'UTM60W']
```

That is far more than SWOT could have seen over one point in two months. The UTM zone in each granule name gives the problem
away. (UTM, the Universal Transverse Mercator system, divides the globe into 60 numbered zones, each 6° of longitude wide, with a flat x/y grid in meters.) Louisville is in UTM zone **16**, but most results are in zones 01 and 60, on either side of the 180° meridian. The
metadata footprints of those granules wrap around the whole globe, so they falsely "intersect" almost any box. Downloading
them all would waste gigabytes on scenes from the other side of the planet.

A more reliable check is each granule's footprint *polygon* (`GPolygons` in its metadata). The false matches have no polygon,
only a global rectangle. The first function below keeps the granules whose footprint polygon contains your point.

The second function handles duplicates. A granule name ends in two codes: the **CRID** (composite release identifier, for
example `PGD0`) and a **product counter** (`01`, `02`, …). The [Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf)
(sections 3 and 4) explains them: `PGD0` is reprocessed Version D, `PID0` is forward-processed Version D, and codes ending in
`C0`–`C2` are older Version C. Where both exist, use `PGD0`, and use the highest product counter. The same overpass can turn up
under more than one CRID, so the function keeps one granule per overpass:

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

VERSION_D_CRIDS = ["PGD0", "PID0"]  # preferred first: reprocessed, then forward-processed

def keep_best_version_d(granules):
    """Keep one Version D granule per overpass: the preferred CRID, then the highest product counter."""
    best = {}
    for g in granules:
        name = g["umm"]["GranuleUR"].removesuffix("_swot")
        overpass, crid, counter = name.rsplit("_", 2)  # e.g. ..._20250413T095502, PGD0, 01
        if crid not in VERSION_D_CRIDS:
            continue  # skip Version C granules
        rank = (VERSION_D_CRIDS.index(crid), -int(counter))
        if overpass not in best or rank < best[overpass][0]:
            best[overpass] = (rank, g)
    return sorted((g for rank, g in best.values()), key=lambda g: g["umm"]["GranuleUR"])

covering = [g for g in louisville_raster if footprint_covers(g, site_lon, site_lat)]
louisville_raster = keep_best_version_d(covering)
for g in louisville_raster:
    print(g["umm"]["GranuleUR"], round(g.size, 1), "MB")
```

```
SWOT_L2_HR_Raster_100m_UTM16S_N_x_x_x_030_160_044F_20250322T235531_20250322T235552_PGD0_01_swot 69.3 MB
SWOT_L2_HR_Raster_100m_UTM16S_N_x_x_x_030_175_111F_20250323T130937_20250323T130958_PGD0_01_swot 71.0 MB
SWOT_L2_HR_Raster_100m_UTM16S_N_x_x_x_030_466_044F_20250402T221817_20250402T221838_PGD0_01_swot 75.7 MB
SWOT_L2_HR_Raster_100m_UTM16S_N_x_x_x_030_481_111F_20250403T113223_20250403T113244_PGD0_01_swot 82.0 MB
SWOT_L2_HR_Raster_100m_UTM16S_N_x_x_x_031_175_111F_20250413T095441_20250413T095502_PGD0_01_swot 73.7 MB
SWOT_L2_HR_Raster_100m_UTM16S_N_x_x_x_031_466_044F_20250423T190324_20250423T190345_PGD0_01_swot 63.0 MB
SWOT_L2_HR_Raster_100m_UTM16S_N_x_x_x_031_481_111F_20250424T081730_20250424T081751_PGD0_01_swot 62.7 MB
SWOT_L2_HR_Raster_100m_UTM16S_N_x_x_x_032_160_044F_20250503T172540_20250503T172601_PGD0_01_swot 69.3 MB
SWOT_L2_HR_Raster_100m_UTM16S_N_x_x_x_032_175_111F_20250504T063945_20250504T064006_PGD0_01_swot 73.5 MB
```

Read a Raster name from left to right: resolution (`100m`), UTM zone and latitude band (`UTM16S`), **cycle** (`030`, one
21-day repeat of the orbit), **pass** (`175`, one numbered track within the cycle), scene number (`111F`), start and end time
(UTC), CRID and product counter. Four passes see Louisville (`160`, `175`, `466`, `481`), so the point is observed about four
times in each 21-day cycle, in pairs half a day apart.

:::{admonition} Partner review (NASA): Programmatic data discovery
:class: important
Is the 180° meridian false-match behavior a known CMR/`earthaccess` issue, and is checking each granule's `GPolygons` footprint (as above) the recommended workaround? Is the CRID and product-counter de-duplication above the recommended practice?
:::

### Find RiverSP granules over the Ohio at Louisville

RiverSP granule metadata only has a rough rectangle for the whole continental pass, so `footprint_covers` can't screen them.
Instead, keep the RiverSP granules from the same **cycle and pass** as the Raster scenes that cover the point:

```python
louisville_reach_granules = earthaccess.search_data(
    short_name="SWOT_L2_HR_RiverSP_D",
    granule_name="*Reach*",          # reach files only
    bounding_box=site_bbox,
    temporal=(start, end),
)
# Raster name split on "_": [5] UTM zone, [10] cycle, [11] pass, [12] scene. RiverSP: [5] cycle, [6] pass.
# (cycle, pass) of each Raster scene that covers the point, e.g. ("031", "175")
seen_passes = {tuple(g["umm"]["GranuleUR"].split("_")[10:12]) for g in louisville_raster}
louisville_reach_granules = keep_best_version_d(
    [g for g in louisville_reach_granules if tuple(g["umm"]["GranuleUR"].split("_")[5:7]) in seen_passes]
)
print(len(louisville_reach_granules), "reach granules from passes that see the point")
for g in louisville_reach_granules[:3]:
    print(g["umm"]["GranuleUR"], round(g.size, 1), "MB")
```

```
9 reach granules from passes that see the point
SWOT_L2_HR_RiverSP_Reach_030_160_NA_20250322T234851_20250323T000415_PGD0_01 7.7 MB
SWOT_L2_HR_RiverSP_Reach_030_175_NA_20250323T130238_20250323T131705_PGD0_01 8.1 MB
SWOT_L2_HR_RiverSP_Reach_030_466_NA_20250402T221137_20250402T222731_PGD0_01 8.3 MB
```

RiverSP names carry the feature type (`Reach`), cycle, pass, continent (`NA`, North America), start and end time, CRID and
product counter.

:::{admonition} Partner review (NASA): RiverSP reach sub-collection
:class: important
On 2026-10-08, the `SWOT_L2_HR_RiverSP_reach_D` sub-collection returned no granules near Louisville for cycles 030–031 (mid-March to late April 2025), although the parent `SWOT_L2_HR_RiverSP_D` collection and `hydrocron` both had them (CRID `PGD0`). This lesson therefore searches the parent collection with `granule_name="*Reach*"`. Is this a known gap, and which collection should learners search?
:::

Behind the scenes, `earthaccess` queries NASA's [Common Metadata Repository (CMR)](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html)
and, when you download, reads from the PO.DAAC cloud archive in Amazon Web Services (AWS) region `us-west-2`. You don't need
to know either system to use `earthaccess`, but it helps when you read tutorials that call them directly.

## Programmatic data downloads

Discovery told you *which* granules exist. Now get the data. The two tools behave differently:

- `earthaccess` gives you **whole files**: one granule per overpass, covering a large area. `earthaccess.download()` copies
  them to your computer. `earthaccess.open()` streams them instead, which is most efficient when your code runs in the same
  cloud region as the data (AWS `us-west-2`). On a laptop, downloading a handful of files is simpler and just as fast.
- `hydrocron` gives you **just the rows you ask for**: the values for one reach or node, across many overpasses, in one web
  request.

Keep downloads exactly as they arrived in `data_dir`, and write anything you compute from them somewhere else. Then you can
always tell raw data from derived data, and re-create the derived files from the raw ones (see
[Publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data) in Module 1).

### RiverSP reaches with `earthaccess`

RiverSP granules are zipped shapefiles, so you read them with `geopandas`. Download the granule from 13 April 2025 (cycle 031,
pass 175), near the flood crest, and find the SWORD reach closest to the example point. This is also how you find a
`reach_id` to use with `hydrocron` if you don't have one. (You can also look up reach IDs interactively in
[SWORD Explorer](https://www.swordexplorer.com/).)

```python
import geopandas as gpd
from shapely.geometry import Point

flood_granule = [g for g in louisville_reach_granules if "_031_175_" in g["umm"]["GranuleUR"]]
files = earthaccess.download(flood_granule, local_path=data_dir)
reaches = gpd.read_file(files[0])
print(len(reaches), "reaches in this granule")

# Distance from each reach to the point, in meters, in the UTM zone around the point (here zone 16N)
utm_crs = gpd.GeoSeries([Point(site_lon, site_lat)], crs="EPSG:4326").estimate_utm_crs()
site = gpd.GeoSeries([Point(site_lon, site_lat)], crs="EPSG:4326").to_crs(utm_crs).iloc[0]
reaches_utm = reaches.to_crs(utm_crs)
reaches_utm["dist_to_site_m"] = reaches_utm.distance(site).round()
reaches_utm.nsmallest(3, "dist_to_site_m")[["reach_id", "river_name", "dist_to_site_m", "p_width", "wse", "width", "reach_q", "time_str"]]
```

```
1153 reaches in this granule
        reach_id  river_name  dist_to_site_m  p_width       wse       width  reach_q              time_str
965  74267300251  Ohio River           206.0    720.0  131.0050  852.862135        2  2025-04-13T09:54:52Z
964  74267300241  Ohio River          4055.0    466.0  130.5152  434.106853        2  2025-04-13T09:54:51Z
966  74267300261  Ohio River          4878.0    660.0  131.8877  713.954131        2  2025-04-13T09:54:53Z
```

The point sits on reach **`74267300251`**, about 200 m from its centerline (well inside a channel about 720 m wide). Its neighbors are `74267300241` (downstream) and `74267300261` (upstream). Reach
IDs encode position in SWORD: in `74267300251`, the leading `7` is the North America region, and the last digit (`1`) is the
reach type, `1` meaning a river reach. The granule itself holds every reach SWOT observed along this pass across North America.
RiverSP files carry about 130 columns; the product description documents (PDDs), linked from the
[PO.DAAC Cookbook SWOT page](https://podaac.github.io/tutorials/quarto_text/SWOT.html), define them all.

:::{admonition} TODO (dev team): Reach ID structure
:class: attention
Confirm the reach ID digit meanings (region, basin, reach number, type) against the SWORD product description and add a link.
:::

Notice `p_width`: SWORD expects this reach to be about 720 m wide, and SWOT measured 853 m on this overpass, with the river in
flood. Each row is one reach seen on this overpass. The key columns:

- `reach_id` is the **{term}`Location identifier`**.
- `wse` ({term}`water surface elevation <Water surface elevation>`) and `width` are the main **{term}`Variables <Variable>`**.
  Their **{term}`Variable unit`** is meters; `wse` is height above the EGM2008 geoid (a model of mean sea level).
- `wse_u` and `width_u` are each value's estimated uncertainty, in meters.
- `p_width` is SWORD's prior (expected) width for the reach, useful for judging whether a measured `width` is plausible.
- `reach_q` is the summary **{term}`Data quality flag <Data quality flag(s)>`**: 0 = good, 1 = suspect, 2 = degraded, 3 = bad.
- `time_str` is the overpass **{term}`Time`** in UTC.
- Missing values are stored as `-999999999999`, not `NaN`. Filter them out before plotting.

:::{admonition} Partner review (NASA): RiverSP columns
:class: important
Confirm the `reach_q` value meanings and the EGM2008 vertical reference for Version D RiverSP `wse`.
:::

The location map at the top of this page was drawn from this one file:

```python
import matplotlib.pyplot as plt

near = reaches_utm.nsmallest(3, "dist_to_site_m").to_crs(4326)
fig, (ax_pass, ax_zoom) = plt.subplots(1, 2, figsize=(11, 5.5), width_ratios=[1, 1.4])
# Left: every reach in the granule shows the extent of one pass across North America
reaches.plot(ax=ax_pass, color="0.55", linewidth=0.6)
ax_pass.plot(site_lon, site_lat, marker="*", color="#e34948", markersize=14, markeredgecolor="white")
ax_pass.set_title("All reaches in one RiverSP granule (pass 175)")
# Right: the three reaches nearest the point, labeled with their IDs
for (_, reach), color in zip(near.iterrows(), ["#2a78d6", "#eb6834", "#1baf7a"]):
    gpd.GeoSeries([reach.geometry]).plot(ax=ax_zoom, color=color, linewidth=3)
    x, y = reach.geometry.interpolate(0.5, normalized=True).coords[0]
    ax_zoom.annotate(str(reach.reach_id), (x, y), xytext=(0, 12), textcoords="offset points", ha="center", fontsize=9)

ax_zoom.plot(site_lon, site_lat, marker="*", color="#e34948", markersize=16, markeredgecolor="white")
ax_zoom.set_title(f"Nearest SWORD reaches to the point: {site_name}")
for ax in (ax_pass, ax_zoom):
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")

fig.tight_layout()
plt.show()
```

### Raster water area with `earthaccess`

Raster granules are NetCDF files, so you read them with `xarray`. Each file is a fixed scene, about 150 km on a side, on a
100 m grid in UTM coordinates. Comparisons only make sense between scenes seen from the **same pass**, because each pass views
the river from a different angle and covers a different part of the scene. Download the three pass-175 scenes: before the
flood, near the crest, and after.

```python
import xarray as xr

pass_175 = [g for g in louisville_raster if g["umm"]["GranuleUR"].split("_")[11] == "175"]
raster_files = sorted(earthaccess.download(pass_175, local_path=data_dir))  # in time order
ds = xr.open_dataset(raster_files[0])
ds[["water_area", "water_frac", "wse", "water_area_qual"]]
```

```
<xarray.Dataset> Size: 37MB
Dimensions:          (y: 1511, x: 1511)
Coordinates:
  * y                (y) float64 12kB 4.15e+06 4.15e+06 ... 4.301e+06 4.301e+06
  * x                (x) float64 12kB 5.818e+05 5.819e+05 ... 7.328e+05
Data variables:
    water_area       (y, x) float32 9MB ...
    water_frac       (y, x) float32 9MB ...
    wse              (y, x) float32 9MB ...
    water_area_qual  (y, x) float32 9MB ...
Attributes: (12/49)
    Conventions:                   CF-1.7
    title:                         Level 2 KaRIn High Rate Raster Data Product
    institution:                   JPL
    source:                        Ka-band radar interferometer
    history:                       2026-03-19T17:17:20Z : Creation
    platform:                      SWOT
    ...                            ...
    utm_zone_num:                  16
    mgrs_latitude_band:            S
    x_min:                         581800.0
    x_max:                         732800.0
    y_min:                         4150100.0
    y_max:                         4301100.0
```

For each 100 m pixel:

- `water_area` (**Variable unit**: m²) is the surface area of water in the pixel. A pixel that is fully water is about
  10,000 m².
- `water_frac` (unitless) is the fraction of the pixel covered by water.
- `wse` (m above the geoid) is the water surface elevation.
- `water_area_qual` is the **Data quality flag** for `water_area`: 0 = good, 1 = suspect, 2 = degraded, 3 = bad. `wse_qual`
  and the other `_qual` variables work the same way.

Pixels outside the swath (the strip of ground the radar imaged on this overpass) are `NaN`. The `x` and `y` coordinates are UTM meters, and the full projection is in the `crs`
variable's `crs_wkt` attribute.

To compare overpasses, add up `water_area` in a 10 km × 10 km box around the point in each file. Two details matter:

- **Use each file's own projection.** Converting the point into that file's UTM coordinates keeps the box in the same place.
- **Look at the quality flag before you filter on it.** The function counts the pixels at each flag level and reports the
  area two ways: good and suspect pixels only (`water_area_qual <= 1`), and everything except bad pixels (`<= 2`).

```python
import pandas as pd
import pyproj

def water_area_near(path, lon=site_lon, lat=site_lat, half_width_m=5000):
    """Water area (km^2) and pixel counts by quality flag in a square box centred on (lon, lat)."""
    ds = xr.open_dataset(path)
    utm = pyproj.CRS.from_wkt(ds["crs"].attrs["crs_wkt"])
    x, y = pyproj.Transformer.from_crs("EPSG:4326", utm, always_xy=True).transform(lon, lat)
    window = ds.sel(x=slice(x - half_width_m, x + half_width_m), y=slice(y - half_width_m, y + half_width_m))
    area = window["water_area"]
    qual = window["water_area_qual"].where(area.notnull())  # only pixels SWOT observed
    return {
        "time": ds.attrs["time_granule_start"][:16],
        "px_good_suspect": int((qual <= 1).sum()),
        "px_degraded": int((qual == 2).sum()),
        "px_bad": int((qual == 3).sum()),
        "area_good_suspect_km2": round(float(area.where(qual <= 1).sum()) / 1e6, 1),
        "area_not_bad_km2": round(float(area.where(qual <= 2).sum()) / 1e6, 1),
    }

water_area = pd.DataFrame([water_area_near(f) for f in raster_files])
water_area
```

```
               time  px_good_suspect  px_degraded  px_bad  area_good_suspect_km2  area_not_bad_km2
0  2025-03-23T13:09             7325            0       2                   14.2              14.2
1  2025-04-13T09:54                0         7637       0                    0.0              16.4
2  2025-05-04T06:39             7856            0       0                   15.2              15.2
```

The 10 km box holds 10,000 pixels, and about three quarters were observed on each overpass (the `px_` columns add up to
the observed pixels). Two things stand out:

1. **A strict filter would hide the flood.** On 13 April, near the crest, *every* observed pixel is flagged degraded (2), so
   `area_good_suspect_km2` is 0.0. That doesn't mean there was no water. Counting degraded pixels too (`area_not_bad_km2`),
   the water area rose from 14.2 km² on 23 March to 16.4 km² on 13 April and fell back to 15.2 km² on 4 May.
2. **Most of the flood was vertical.** The water area grew by about 15%, while the water surface rose by more than 8 m (you'll
   see that in the `hydrocron` time series below). Water area in a fixed box is a blunt measure on a large river whose
   banks hold most of the rise.

:::{dropdown} Optional: decode why the 13 April scene is degraded
The flag says *that* the 13 April pixels are degraded. The bitwise flag, `water_area_qual_bitwise`, says *why*: each bit is
one reason, and the variable's attributes name them. `values & mask` (bitwise AND) is non-zero when that reason's bit is set. This block counts, across the whole 13 April scene, how many observed
pixels have each "degraded" reason set:

```python
import numpy as np

ds = xr.open_dataset(raster_files[1])   # the 13 April scene
bitwise = ds["water_area_qual_bitwise"].where(ds["water_area"].notnull())   # observed pixels only
values = bitwise.values[np.isfinite(bitwise.values)].astype("int64")
reasons = dict(zip(bitwise.attrs["flag_meanings"].split(), bitwise.attrs["flag_masks"]))
print(len(values), "observed pixels in the scene")
{reason: int(((values & int(mask)) > 0).sum()) for reason, mask in reasons.items() if "degraded" in reason}
```

```
684605 observed pixels in the scene
{'classification_qual_degraded': 0, 'geolocation_qual_degraded': 684605}
```
:::

Every observed pixel in the scene carries `geolocation_qual_degraded`: the whole overpass was flagged because its
geolocation (where each pixel sits on the ground) is less certain, not because of anything about the river. Whether to use
such a scene is your call. Here, the river in the 13 April scene lines up with the river in the other two (see the maps
below), so this lesson keeps it and says so.

Save derived results like this table outside the raw-data folder, with a name that says what they are:

```python
import os
os.makedirs("data/swot/derived", exist_ok=True)
water_area.to_csv("data/swot/derived/louisville_water_area_pass175.csv", index=False)
```

Maps show the change more clearly than totals. This block plots `water_frac` in a 30 km window for each of the three scenes,
leaving out only pixels flagged bad, so the degraded 13 April scene still appears:

```python
fig, axes = plt.subplots(1, 3, figsize=(13, 4.8), sharey=True)
for ax, path in zip(axes, raster_files):
    ds = xr.open_dataset(path)
    utm = pyproj.CRS.from_wkt(ds["crs"].attrs["crs_wkt"])
    x, y = pyproj.Transformer.from_crs("EPSG:4326", utm, always_xy=True).transform(site_lon, site_lat)
    window = ds.sel(x=slice(x - 15000, x + 15000), y=slice(y - 15000, y + 15000))
    frac = window["water_frac"].where(window["water_area_qual"] <= 2)  # drop pixels flagged bad
    image = ax.pcolormesh((window.x - x) / 1000, (window.y - y) / 1000, frac.clip(0, 1), cmap="Blues", vmin=0, vmax=1)
    ax.plot(0, 0, marker="*", color="#e34948", markersize=12, markeredgecolor="white")
    ax.set_title(ds.attrs["time_granule_start"][:10])
    ax.set_xlabel("km east of the point")
    ax.set_aspect("equal")

axes[0].set_ylabel("km north of the point")
fig.colorbar(image, ax=axes, label="Water fraction (pixels not flagged bad)", shrink=0.85)
plt.show()
```

:::{figure} ../images/m03/swot-raster-water-frac.png
:alt: Three side-by-side maps of SWOT water fraction in a 30 km window around Louisville, for 23 March, 13 April and 4 May 2025. The Ohio River shows as a dark blue curving band through each map. On 13 April the band is visibly wider, especially downstream to the southwest, and a few side channels and low areas next to the river are filled.
:width: 100%

SWOT water fraction (0 to 1) in a 30 km × 30 km window centred on the example point (red star), from the same pass (175)
before the flood (23 March 2025), near the crest (13 April) and after (4 May). Pixels flagged bad are left out; the whole
13 April scene is flagged degraded for geolocation (see the text). Data: NASA SWOT Level 2 Water Mask Raster Image 100 m
product, Version D ([doi:10.5067/SWOT-RASTER-D](https://doi.org/10.5067/SWOT-RASTER-D)), CRID `PGD0`, accessed 2026-10-08.
:::

:::{admonition} Partner review (NASA): Raster water area
:class: important
The 13 April 2025 pass-175 scene (`..._031_175_111F_..._PGD0_01`) has `geolocation_qual_degraded` set on every observed pixel. What causes a scene-wide geolocation flag, and is it reasonable to use such a scene for water extent, as this lesson does, after checking it against neighboring scenes? Which `water_area_qual` threshold do you recommend for water-extent work, and is a fixed 10 km box a reasonable way to compare overpasses from one pass?
:::

(swot-hydrocron)=
### RiverSP time series with `hydrocron`

If what you want is a time series for one reach, `hydrocron` is the tool for the job. As the
[`hydrocron` documentation](https://podaac.github.io/hydrocron/) puts it:

> SWOT data is archived as individually timestamped shapefiles, which would otherwise require users to perform potentially
> thousands of file IO operations per river feature to view the data as a timeseries. Hydrocron makes this possible with a
> single API call.

`hydrocron` is a web {term}`API`, so there is nothing extra to install: any HTTP client works, and this lesson uses
`requests`. You don't need an Earthdata login or an {term}`API key` for normal use. PO.DAAC offers optional keys for heavy
use, sent in an `x-hydrocron-key` header. One request returns one feature (a reach, node or lake) over a time range, and
responses are capped at 6 MB. See the [`hydrocron` timeseries documentation](https://podaac.github.io/hydrocron/timeseries)
for every parameter. The main ones:

| Parameter | Example | Notes |
|---|---|---|
| `feature` | `Reach` | `Reach`, `Node` or `PriorLake` |
| `feature_id` | `74267300251` | SWORD reach or node ID (the **Location identifier**) |
| `start_time`, `end_time` | `2025-03-15T00:00:00Z` | UTC |
| `fields` | `reach_id,time_str,wse,wse_u,width,reach_q` | Only the columns you need |
| `output` | `csv` | `csv` or `geojson`, returned inside a JSON response |
| `collection_name` | `SWOT_L2_HR_RiverSP_D` | Optional; defaults to Version D. Version C (`2.0`) reach IDs can differ |

The function below, adapted from the CUAHSI longitudinal-profile notebook (see Further reading), wraps one request and returns
a `pandas` DataFrame. It drops overpasses with no valid measurement (fill values) and, by default, keeps everything else.
Pass `max_reach_q` to also drop observations whose quality flag is worse than you can accept.

```python
import io
import pandas as pd
import requests

HYDROCRON_URL = "https://soto.podaac.earthdatacloud.nasa.gov/hydrocron/v1/timeseries"
FILL_VALUE = -999999999999.0
FIELDS = "reach_id,time_str,wse,wse_u,width,p_width,reach_q,crid"

def get_reach_timeseries(reach_id, start, end, fields=FIELDS, max_reach_q=3):
    """One hydrocron request: a DataFrame of valid RiverSP observations of one reach between start and end (UTC)."""
    params = {
        "feature": "Reach",
        "feature_id": reach_id,
        "start_time": start,
        "end_time": end,
        "output": "csv",
        "fields": fields,
    }
    response = requests.get(HYDROCRON_URL, params=params, timeout=120)
    if response.status_code != 200:
        raise RuntimeError(f"hydrocron returned HTTP {response.status_code}: {response.text[:300]}")
    df = pd.read_csv(io.StringIO(response.json()["results"]["csv"]))
    df = df[(df["wse"] != FILL_VALUE) & (df["reach_q"] <= max_reach_q)].copy()
    df["time"] = pd.to_datetime(df["time_str"])
    return df

louisville = get_reach_timeseries(reach_id, start, end)   # reach_id, start and end come from the query block
print(len(louisville), "observations; reach_q counts:", louisville["reach_q"].value_counts().sort_index().to_dict())
louisville[["time_str", "wse", "wse_u", "width", "reach_q", "crid"]]
```

```
12 observations; reach_q counts: {1: 10, 2: 2}
                time_str       wse    wse_u       width  reach_q  crid
0   2025-03-22T23:55:38Z  120.8400  0.10158  800.442537        2  PGD0
1   2025-03-23T13:09:48Z  122.4912  0.10781  772.133013        1  PGD0
2   2025-04-02T22:18:28Z  123.0559  0.09609  851.840157        1  PGD0
3   2025-04-03T11:32:37Z  123.4468  0.09824  835.697529        1  PGD0
4   2025-04-12T20:40:43Z  131.2465  0.09455  956.352535        1  PGD0
5   2025-04-13T09:54:52Z  131.0050  0.09802  852.862135        2  PGD0
6   2025-04-23T19:03:35Z  121.0550  0.11455  746.324459        1  PGD0
7   2025-04-24T08:17:44Z  120.6820  0.11762  723.413398        1  PGD0
8   2025-05-03T17:25:47Z  122.0728  0.09600  757.907173        1  PGD0
9   2025-05-04T06:39:56Z  122.8724  0.10448  788.556176        1  PGD0
10  2025-05-14T15:48:38Z  121.8829  0.11123  793.597367        1  PGD0
11  2025-05-15T05:02:48Z  121.8344  0.10818  769.943539        1  PGD0
```

Every row is one SWOT overpass of the reach. `wse`, `wse_u` and `width` are in meters; `hydrocron` also adds a
`<field>_units` column (for example `wse_units`) giving each **Variable unit**, and the function adds a `time` column parsed as
a timestamp for plotting. `crid` records which processing produced each value (here, all reprocessed Version D, `PGD0`).
`hydrocron` also returns a row for each overpass that produced no valid measurement, with `time_str` = `no_data`, a fill value
for `wse` and `reach_q` = 3; the function drops those.

A plot shows the flood clearly:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 4))
for q, color, label in [(1, "#2a78d6", "suspect (reach_q = 1)"), (2, "#eb6834", "degraded (reach_q = 2)")]:
    rows = louisville[louisville["reach_q"] == q]
    ax.errorbar(rows["time"], rows["wse"], yerr=rows["wse_u"], fmt="o", color=color, markersize=7, capsize=3, label=label)

ax.plot(louisville["time"], louisville["wse"], color="0.7", linewidth=1, zorder=0)
ax.set_ylabel("WSE (m above the geoid)")
ax.set_title(f"SWOT reach {reach_id}, {site_name}")
ax.legend(title="Quality flag", loc="upper right")
ax.grid(alpha=0.3)
fig.autofmt_xdate()
plt.show()
```

:::{figure} ../images/m03/swot-hydrocron-wse-flood.png
:alt: Scatter plot of SWOT water surface elevation for reach 74267300251 from 22 March to 15 May 2025, with points joined by a thin gray line. Values sit between about 121 and 123.5 m until early April, jump to about 131 m on 12 and 13 April, and drop back to about 121 m by 23 April. Ten points are blue (suspect) and two are orange (degraded): 22 March and 13 April.
:width: 100%

Water surface elevation of SWORD reach `74267300251`, Ohio River at Louisville, from `hydrocron`, 15 March to 15 May 2025.
Colors show the reach quality flag; error bars (about ±0.1 m, smaller than the markers) show the reported `wse_u`. Data:
NASA SWOT Level 2 River Single-Pass Vector product, Version D ([doi:10.5067/SWOT-RIVERSP-D](https://doi.org/10.5067/SWOT-RIVERSP-D)),
CRID `PGD0`, via `hydrocron`, accessed 2026-10-08.
:::

SWOT saw this reach 12 times in two months, in pairs about 13 hours apart (passes 160 and 175, then 466 and 481). Three
things stand out:

- **The flood is obvious.** The water surface sat around 121–123 m in March, jumped to 131.2 m on 12 April, and was back near
  121 m by 23 April. The two overpasses in most pairs agree to within 0.8 m; the biggest gap (1.7 m, 22–23 March) involves a degraded value.
- **No observation is flagged good.** Ten are suspect (`reach_q` = 1) and two degraded (2). That is normal for Version D
  RiverSP (see [Understanding what you downloaded](#swot-understanding)). A `reach_q == 0` filter
  (`get_reach_timeseries(..., max_reach_q=0)`) would return an empty table.
- **Width is a useful sanity check.** The measured `width` stays between about 720 and 960 m, close to SWORD's `p_width` of
  720 m and widest at the crest. A measured width far from `p_width` is a warning sign that SWOT saw only part of the channel
  or counted water outside it, and on narrower rivers it is often the first clue that a `wse` value is off.

If a reach ID does not exist in the collection, `hydrocron` answers with an HTTP 400 and a message such as
`Results with the specified Feature ID ... were not found`. The function raises that as an error, so a typo doesn't pass
silently.

(swot-understanding)=
## Understanding what you downloaded

Every data product in this course is described with the same shared concepts. Here they are for the three things you
retrieved:

| Shared concept | RiverSP reach file (`earthaccess`) | Raster scene (`earthaccess`) | `hydrocron` time series |
|---|---|---|---|
| {term}`Location identifier` | `reach_id` (SWORD), e.g. `74267300251` | none per pixel: UTM `x`, `y` coordinates on a fixed scene grid | the `reach_id` you asked for |
| {term}`Variable` | `wse`, `width` (plus slope, area and ~130 other columns) | `water_area`, `water_frac`, `wse` | the `fields` you asked for |
| {term}`Variable unit` | meters (`wse` above the EGM2008 geoid) | m² (`water_area`), unitless (`water_frac`), m (`wse`) | `<field>_units` columns |
| {term}`Time` | `time_str`, the overpass time (UTC), one value per reach | `time_granule_start` attribute, one per scene | `time_str`, one row per overpass |
| {term}`Data quality flag(s)` | `reach_q` (0–3) and its bitwise version `reach_q_b` | `water_area_qual`, `wse_qual` (0–3) | whichever flags you request (`reach_q`) |
| {term}`Version / provenance` | Version D; CRID in the file name (`PGD0`); collection DOI [10.5067/SWOT-RIVERSP-D](https://doi.org/10.5067/SWOT-RIVERSP-D) | Version D; CRID in the file name; collection DOI [10.5067/SWOT-RASTER-D](https://doi.org/10.5067/SWOT-RASTER-D) | `crid` field; collection name (default Version D) |
| {term}`Data unit` | one granule = one pass over one continent, all reaches | one granule = one ~150 km scene from one pass | one response = one reach over your time range |

Four things are worth keeping in mind:

- **No discharge here yet.** [Meet NASA SWOT](../02-federal-water-data-landscape/01_meet_nasa_swot.md) lists discharge as a
  SWOT variable. RiverSP files have discharge columns (names starting `dschg_`), but the Version D release note says discharge
  estimates "are not provided in the PID0 and PGD0 products" and will be computed after reprocessing is complete
  ([release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf),
  section 4.1). Expect fill values in those columns, and check the current release notes before relying on them.
- **Quality flags are rarely 0.** For RiverSP, "nearly all reach-level quality flags … are non-zero" in Version D, because
  node-level flags are propagated up to the reach ([Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf), table 8).
  A strict `reach_q == 0` filter would usually return an empty table. A reasonable starting rule, used in this lesson: keep
  `reach_q` ≤ 1; look hard at degraded values (2) by comparing `width` with `p_width` and with the neighboring overpass; and
  write down what you kept and why. `reach_q` is the 0–3 summary; `reach_q_b` is the bitwise version that records the reasons.
- **Uncertainties are estimates.** The same release note says the reported uncertainties "have not been validated and should
  not be relied upon for science interpretation" yet. Treat `wse_u` as a rough guide.
- **Versions change values.** A reprocessed version can change the numbers for the same overpass. Record the collection, the
  CRID and your access date, and cite the collection DOI, for example: *SWOT. (2025). SWOT Level 2 River Single-Pass Vector
  Data Product, Version D [Dataset]. NASA Physical Oceanography Distributed Active Archive Center.
  https://doi.org/10.5067/SWOT-RIVERSP-D. Accessed 2026-10-08.* See the citation guidance in
  [Meet NASA SWOT](../02-federal-water-data-landscape/01_meet_nasa_swot.md#usage-and-support).

:::{admonition} Partner review (NASA): Citing SWOT data
:class: important
Confirm the recommended dataset citation format for Version D RiverSP and Raster, and whether Version D RiverSP discharge (`dschg_*`) is now populated.
:::

## Best practices FAQs

See the sections below for answers to these questions:

* What is the recommended way to download data for **one location across the full period of record**?
* What is the recommended way to download data across **all locations for a small time range**?
* If I am working on improving efficiency through **code parallelization**, what should I do vs avoid?

### Temporal scaling

*What is the recommended way to download data for one location but the full period of record?*

Use `hydrocron`, one request per reach or node. Set `start_time` to the start of SWOT's science orbit (21 July 2023; usable data begin 26 July, and the
[Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf),
table 2, notes no useful data before then) and `end_time` to today (the code below uses a fixed end date so the result can be reproduced), and ask only for the `fields` you need. Fewer
fields keep each response under the 6 MB limit. This replaces downloading every RiverSP granule that ever covered your reach,
each holding a whole continental pass, only to keep one row from each.

```python
# The whole science-orbit record for the reach, in one request
full_record = get_reach_timeseries(reach_id, "2023-07-21T00:00:00Z", "2026-10-01T00:00:00Z")
print(len(full_record), "observations from", full_record["time"].min().date(), "to", full_record["time"].max().date())
print("CRIDs:", full_record["crid"].value_counts().to_dict())
fig, ax = plt.subplots(figsize=(10, 3.8))
ax.plot(full_record["time"], full_record["wse"], marker="o", markersize=3, linewidth=0.8, color="#2a78d6")
ax.set_ylabel("WSE (m above the geoid)")
ax.set_title(f"SWOT reach {reach_id}, full record")
ax.grid(alpha=0.3)
plt.show()
```

```
212 observations from 2023-07-26 to 2026-09-27
CRIDs: {'PGD0': 118, 'PID0': 94}
```

:::{figure} ../images/m03/swot-hydrocron-wse-full-record.png
:alt: Line chart of SWOT water surface elevation for reach 74267300251 from July 2023 to September 2026. Most values lie between 119 and 124 m. The highest peaks, about 131.5 m, are in February 2025 and April 2025; smaller peaks of about 127 m appear in January and April 2024.
:width: 100%

The full science-orbit record of SWORD reach `74267300251` from one `hydrocron` request: 212 valid observations,
26 July 2023 to 27 September 2026. Data: NASA SWOT Level 2 River Single-Pass Vector product, Version D
([doi:10.5067/SWOT-RIVERSP-D](https://doi.org/10.5067/SWOT-RIVERSP-D)), CRIDs `PGD0` (to May 2025) and `PID0` (after),
via `hydrocron`, accessed 2026-10-08.
:::

One request returned more than three years of overpasses. Two things to notice:

- **The April 2025 flood was not the only one.** The highest values in the record, about 131.5 m, are from 20 February 2025;
  the April crest (131.2 m) is close behind. A long record puts one event in context.
- **The record mixes two processing streams.** Observations up to 15 May 2025 are reprocessed (`PGD0`); later ones are
  forward-processed (`PID0`). Both are Version D, but keep the `crid` column so you can check whether a shift in your series
  lines up with the switch.

### Spatial scaling

*What is the recommended way to download data for all locations but a small time range?*

Use `earthaccess`. Search by `bounding_box` and a short `temporal` window, screen the results (as above), then download or
stream the granules. One RiverSP granule holds every reach in a pass across a continent, and one Raster granule holds a scene
about 150 km on a side, so a few files are the cheapest way to get many locations at once. Looping `hydrocron` over
thousands of reach IDs is the wrong tool here: it sends thousands of requests for data that sit in a few files.

### Parallelization

*If I am working on improving efficiency of my code through parallelization, what should I do vs avoid?*

- **Do** let `earthaccess.download()` handle parallel downloads. It already fetches several files at once (see its
  `threads` argument).
- **Do** run large `earthaccess` workflows in AWS `us-west-2` (for example, a cloud JupyterHub) and use `earthaccess.open()`
  to stream data instead of downloading it.
- **Avoid** firing many `hydrocron` requests in parallel. Send them one after another, or a few at a time, and request a
  `hydrocron` API key from PO.DAAC if you have a heavy or recurring workload.
- **Avoid** re-downloading the same granules every time you run your code. Keep a fixed `local_path=`:
  `earthaccess.download()` skips files that are already there unless you pass `force=True`.

:::{admonition} Partner review (NASA): Parallelization
:class: important
Confirm these recommendations, in particular the guidance on parallel `hydrocron` requests and when to request an API key.
:::

## Now you try it

Repeat the main steps on a second river: the **Willamette River at Salem, Oregon**, in February and March 2026, during the
wet winter season. The Willamette here is much narrower than the Ohio (SWORD expects about 150 m).

**Your task:** find the SWORD reach at Salem and retrieve its water surface elevation time series with `hydrocron`.

1. In the query block, change `site_name` to `"Willamette River at Salem, OR"`, `site_lon, site_lat` to `-123.043, 44.944`,
   and the dates to `start, end = "2026-02-01T00:00:00Z", "2026-03-31T23:59:59Z"`. Re-run it.
2. Search the Raster collection for the new box and dates, then screen the results with `footprint_covers` and
   `keep_best_version_d`, as you did for Louisville. Salem is in UTM zone **10**, so the real matches are `UTM10T` scenes.
   Collect their `(cycle, pass)` pairs in `seen_passes`.
3. Search the RiverSP collection (`granule_name="*Reach*"`), keep the granules from those passes, download **one** of them,
   and find the reach nearest the point. Any one of them will do: every pass you kept sees the point. `estimate_utm_crs()` picks
the right UTM zone for Salem by itself.
4. Set `reach_id` to that reach and call `get_reach_timeseries(reach_id, start, end)`.

Give the new results new names (for example `salem_raster`), so you can still compare them with the Louisville ones.

**What you should get:** the nearest reach is `78220000131`, about 40 m from the point, with `p_width` = 150 m. `hydrocron`
returns 9 observations from 3 February to 29 March 2026: 6 suspect (`reach_q` = 1) and 3 degraded (2). The suspect values lie between about 32.7 and 35.9 m. The three degraded ones (3 and 23 February, 16 March) are 37–38 m,
several meters higher, and their widths (196–253 m) are well above `p_width`. Before trusting those three, ask whether the
river really rose that much or whether SWOT counted water outside the channel; an independent record for those dates, such
as a stream gage or imagery, would tell you.

:::{dropdown} Show an answer
```python
# Step 1: the new query
site_name = "Willamette River at Salem, OR"
site_lon, site_lat = -123.043, 44.944
site_bbox = (site_lon - 0.02, site_lat - 0.02, site_lon + 0.02, site_lat + 0.02)
start, end = "2026-02-01T00:00:00Z", "2026-03-31T23:59:59Z"

# Step 2: Raster scenes that really cover the point
salem_raster = earthaccess.search_data(short_name="SWOT_L2_HR_Raster_100m_D", bounding_box=site_bbox, temporal=(start, end))
salem_raster = keep_best_version_d([g for g in salem_raster if footprint_covers(g, site_lon, site_lat)])
seen_passes = {tuple(g["umm"]["GranuleUR"].split("_")[10:12]) for g in salem_raster}

# Step 3: RiverSP reach granules from those passes; download one and find the nearest reach
salem_reach_granules = earthaccess.search_data(short_name="SWOT_L2_HR_RiverSP_D", granule_name="*Reach*", bounding_box=site_bbox, temporal=(start, end))
salem_reach_granules = keep_best_version_d([g for g in salem_reach_granules if tuple(g["umm"]["GranuleUR"].split("_")[5:7]) in seen_passes])
files = earthaccess.download(salem_reach_granules[:1], local_path=data_dir)
utm_crs = gpd.GeoSeries([Point(site_lon, site_lat)], crs="EPSG:4326").estimate_utm_crs()   # zone 10N here
reaches_utm = gpd.read_file(files[0]).to_crs(utm_crs)
site = gpd.GeoSeries([Point(site_lon, site_lat)], crs="EPSG:4326").to_crs(utm_crs).iloc[0]
reaches_utm["dist_to_site_m"] = reaches_utm.distance(site).round()
print(reaches_utm.nsmallest(1, "dist_to_site_m")[["reach_id", "river_name", "dist_to_site_m", "p_width"]])

# Step 4: the time series
reach_id = "78220000131"   # the nearest reach printed above
salem = get_reach_timeseries(reach_id, start, end)
print(len(salem), "observations; reach_q counts:", salem["reach_q"].value_counts().sort_index().to_dict())
salem[["time_str", "wse", "wse_u", "width", "reach_q"]]
```

```
        reach_id        river_name  dist_to_site_m  p_width
243  78220000131  Willamette River            42.0    150.0
9 observations; reach_q counts: {1: 6, 2: 3}
               time_str      wse    wse_u       width  reach_q
0  2026-02-03T00:54:47Z  37.7277  0.22021  196.374944        2
1  2026-02-05T14:14:00Z  32.6845  0.13473  134.203809        1
2  2026-02-15T12:36:12Z  32.7385  0.11422  149.050192        1
3  2026-02-23T21:39:53Z  37.6586  0.24157  220.050734        2
4  2026-02-26T10:59:07Z  35.8855  0.10013  199.056973        1
5  2026-03-08T09:21:21Z  33.5984  0.10371  173.744420        1
6  2026-03-16T18:25:00Z  37.0691  0.15634  253.412519        2
7  2026-03-19T07:44:13Z  33.8839  0.12153  159.203658        1
8  2026-03-29T06:06:25Z  33.0157  0.10337  167.558418        1
```
:::

## Further reading

- [`earthaccess` documentation](https://earthaccess.readthedocs.io/en/latest/), including the
  [authentication how-to](https://earthaccess.readthedocs.io/en/latest/user/howto/authenticate/) and the
  [API reference](https://earthaccess.readthedocs.io/en/latest/api/).
- [`hydrocron` documentation](https://podaac.github.io/hydrocron/) and the
  [timeseries endpoint reference](https://podaac.github.io/hydrocron/timeseries).
- [PO.DAAC Cookbook: SWOT tutorials](https://podaac.github.io/tutorials/quarto_text/SWOT.html), including
  [Hydrocron API: Getting Started with SWOT Time Series](https://podaac.github.io/tutorials/notebooks/datasets/Hydrocron_SWOT_timeseries_examples_basic.html)
  by Nikki Tebaldi, Cassandra Nickles and Brandi Downs.
- [SWOT Version D release note](https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf)
  (SWOT Project, NASA JPL and CNES): CRIDs, product counters, known issues.
- Dataset DOIs: [SWOT Level 2 River Single-Pass Vector, Version D](https://doi.org/10.5067/SWOT-RIVERSP-D) and
  [SWOT Level 2 Water Mask Raster, Version D](https://doi.org/10.5067/SWOT-RASTER-D).
- [Hydrocron: a new tool for SWOT time series analysis](https://www.earthdata.nasa.gov/news/hydrocron-new-tool-swot-time-series-analysis) (NASA Earthdata).
- [earthaccess tech spotlight](https://nasa-openscapes.github.io/news/2024-03-04-earthaccess-tech-spotlight/) (NASA Openscapes).
- [Earthdata Search](https://search.earthdata.nasa.gov/) and the [CMR search API](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html).
- [SWORD Explorer](https://www.swordexplorer.com/) for finding reach and node IDs interactively.
- Adapted from [SWOT - River Longitudinal Profiles for Water Resources](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/SWOT%20-%20River%20Longitudinal%20Profiles%20for%20Water%20Resources)
  by Mike Durand, with contributions from Bidhya Yadav (Ohio State University), CUAHSI notebooks (GPL-3.0). The
  `get_reach_timeseries` function adapts its `PullReachTimeseries` helper.

:::{admonition} TODO (dev team): confirm this link
:class: attention
The CUAHSI notebook link above points to the `develop` branch. Confirm the branch and path before publication.
:::
