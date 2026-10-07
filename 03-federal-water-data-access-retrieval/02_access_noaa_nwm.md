# Retrieve NOAA NWM streamflow data
TODO: LOOK INTO KERCHUNK AND/OR SEE IF THERE'S A BETTER OPTION THAN HYDROTOOLS WITH FEAR OF LACK OF EFFICIENCY, BUT BIGQUERY IS NOT WHAT WE'RE GOING TO SUGGEST

NOAA National Water Model (NWM) streamflow data lives in a few different places depending on what you need. The full model output has no REST API behind it: it's stored as NetCDF files, made available through file listings and mirrored to cloud storage (Google Cloud Platform, AWS). NOAA does host a separate, official API, [NWPS](https://api.water.noaa.gov/nwps/v1/docs/), but it only covers NWM output at NWPS's ~4,000 established forecast locations, not the full 2.7-million-reach domain, so we're not going to focus on that here.


1. **Programmatic data discovery**: NWM identifies reaches using COMIDs, which come from the NHDPlusV2 hydrography dataset (a USGS product, not a NOAA one). Before you can download streamflow for a location, you first need to find the COMID that corresponds to it. This is handled by USGS's Network Linked Data Index (NLDI), a separate service from wherever the NWM output files live.
1. **Programmatic data downloads**: once you have COMID(s) in hand, `hydrotools` (from NOAA-OWP) retrieves forecast values. This module focuses on **forecast** data. NWM's forecast products (short/medium/long range) are what set it apart from other streamflow datasets, since they predict rather than just record. For historical, observed streamflow, USGS NWIS is the recommended source instead; however, see the note at the end of this section for how NWM's historical/retrospective archive is relevant for ungauged reaches.

If you already know your COMID(s), you can skip programmatic data discovery.

## Tools and environment setup

We're using a dedicated `conda` environment to manage dependency collisions with other lessons. [TODO / for consideration: should we use environments to avoid dependency collisions? Or try to actually address any dependency collisions? We ultimately want people to be able to use all three datasets on their computers, and give them the knowledge and tools to do so]

```bash
conda create -n nwm-env python=3.11 -y
conda activate nwm-envpython3 -m
pip install --upgrade pip wheelpython3 -m
pip install pynhd hydrotools.nwm_client_new hydrotools.nwis_client nest_asyncio
``` 

This installs everything needed for both discovery (`pynhd`) and downloads (`hydrotools`) in one place, so you don't have to juggle two separate environments to go from "find a COMID" to "pull its forecast" within the same script or notebook.

## Programmatic data discovery

Before you download or try to access the data itself, a common first step is to *discover* or *find* the specific reach(es) you need. You don't want to page through the whole NWM domain just to learn which COMID matches your location. Doing this discovery step first also lets you build a COMID list once and reuse it, which matters more once you get to spatially scaling (see FAQs below).

A GUI (graphic user interface) approach exists here too: NOAA's own [interactive map](https://water.noaa.gov/map) lets you click a point and read off a reach ID directly, which is functionally the same identifier as a COMID. That's a fine way to explore or spot-check, but a programmatic discovery step keeps your work reproducible and reusable, and it's worth capturing in code even if you first found the reach by clicking around.

### USGS Network Linked Data Index (NLDI)

NOAA NWM identifies stream reaches using **COMIDs** (also called `nwm_feature_id` or ComID). The NLDI can:

* Find the COMID for a point on the map (point-in-polygon lookup against NHDPlusV2 catchments)
* Find the COMID(s) associated with a known site, e.g. a USGS gage
* Navigate the river network upstream/downstream from a starting COMID (upstream mainstem, upstream with tributaries, downstream mainstem, downstream with diversions), useful for "all reaches in this watershed" style questions

**Example: what's the COMID for the stream closest CUAHSI office?**

```python
from pynhd import NLDI
from shapely.geometry import Point
import geopandas as gpd

nldi = NLDI()

point = gpd.GeoSeries([Point(-71.1739, 42.4238)], crs=4326)
comid_gdf = nldi.feature_byloc(point, fsource="comid")
comid = int(comid_gdf.comid.values[0])

print(f"Nearest COMID: {comid}")

```

`feature_byloc` queries the modernized USGS endpoint to snap your spatial point directly to the closest NHDPlus stream segment, returning a comprehensive GeoDataFrame.

A more direct approach using the raw NLDI REST endpoint (point-in-polygon lookup):

```
https://api.water.usgs.gov/nldi/linked-data/comid/position?coords=POINT(-71.1739 42.4238)
```

Once you have your desired COMID(s), move on to downloads below.

## Programmatic data downloads

While the discovery step above uses a USGS service, downloading the actual forecast values is handled by NOAA-OWP tooling.

### `hydrotools`

`hydrotools` (OWPHydroTools, from NOAA-OWP) is the recommended way to pull NWM **forecast** output, short_range, medium_range, long_range, and analysis_assimilation, into a `pandas.DataFrame` once you know which COMID(s) you want. You never need to open or manage a NetCDF file yourself; `hydrotools` fetches and parses the underlying files behind the `.get()` call. 

**Key pieces**

* `hydrotools.nwm_client_new`: retrieve NWM streamflow forecasts 
*note: this will eventually be changed to `hydrotools.nwm_client` for v8.0+*
* `hydrotools.waterdata_client`:  the modernized replacement for the legacy `nwis_client`, optimized to pull matching USGS NWIS real-time and historical streamflow observations for direct forecast evaluation and baseline comparisons.
* Canonical column names used across all subpackages: `value`, `value_time`, `variable_name`, `nwm_feature_id` (the COMID), `usgs_site_code`, etc. This consistency makes it easy to join NWM and USGS data.

**Example: short-range forecast for a single reach**

```python

# prevents a common, known error that can occur in JupyterHub
import nest_asyncio
nest_asyncio.apply()

from hydrotools.nwm_client_new.NWMFileClient import NWMFileClient
from hydrotools.nwm_client_new.HTTPFileCatalog import HTTPFileCatalog
import pandas as pd

# 1. Target the exact production server URL from your index search
catalog = HTTPFileCatalog("https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/")
model_data_client = NWMFileClient(catalog=catalog)

# 2. Set reference time
yesterday = pd.Timestamp.utcnow() - pd.Timedelta("1D")

# 3. Retrieve forecast data
forecast_data = model_data_client.get(
    configurations = ["short_range"],
    reference_times = [yesterday],
    nwm_feature_ids = [comid] # from discovery step
    )

# 4. Look at the data
print(forecast_data.head())
```

**A note on historical data:** for observed, historical streamflow, use USGS NWIS (`hydrotools.nwis_client`) rather than NWM's own retrospective archive. NWIS is the authoritative source for gauged, historical data and doesn't require the model-file access patterns covered above. The one exception is **ungauged reaches**: NWIS only has data where a physical gauge exists, so if your analysis needs historical streamflow at a reach with no gauge, NWM's retrospective archive (Zarr, on AWS, (see Further Reading below)) is the only source for that, since it's a modeled reconstruction covering every reach in the network, not just gauged ones.


### Temporal scaling

What is the recommended way to download data for one location but the full period of record?

NWM forecast history. NWMFileClient.get() accepts a list of reference times (forecast issue times), and files are downloaded one forecast cycle at a time in groups of 20. A single forecast can be spread across hundreds of files, intermediate processing may use several GB of memory, and the recommended minimum system is a 4-core processor with 8 GB of RAM. Colleagues have noted that hydrotools downloads full files, which makes it less efficient for long time series slices.

Availability depends on the source. The default Google Cloud source holds the largest amount of operational forecast data, but not every configuration covers the whole archive (the Alaska configurations, for example, only became available after August 2023). The AWS operational bucket (noaa-nwm-pds) is described as a rolling four-week archive of short-range output.

NWM retrospective. NWM retrospective simulations are multi-decade model runs: version 3.0 covers February 1979 through January 2023, and version 2.1 covers February 1979 through December 2020. Their output frequency and fields differ from the operational forecast model. Zarr versions are available on AWS for version 2.1, and NCAR describes Zarr stores for version 3.0.

### Spatial scaling

What is the recommended way to download data for all locations but a small time range?

Start with **discovery** to build your list of COMIDs (e.g. all reaches in a HUC or bounding box), then pass that list to the download step in a single batched request rather than looping one-COMID-at-a-time.

NWMFileClient.get() accepts an array of NWM feature IDs (COMIDs), so multiple reaches can be requested in a single call. If you omit nwm_feature_ids, it returns the default set: channel features with a known USGS mapping (8,866 in the documented default).

Results come back as pandas DataFrames that use categorical columns to save memory. The documentation notes that categorical columns can behave unexpectedly in groupby operations, are incompatible with fixed-format HDF files (use format="table"), and may cause problems when writing to geospatial formats with geopandas. Casting a categorical column to str resolves these issues. Setting compute=False returns a dask DataFrame instead of a pandas one.

### Parallelization

NWMFileClient retrieves NWM data from file-based sources. By default it saves downloaded NetCDF files to a local directory, and its get() method returns a pandas DataFrame. get() accepts lists of configurations, reference times, and NWM feature IDs. If nwm_feature_ids is omitted, it defaults to channel features with a known USGS mapping. Setting compute=False returns a dask DataFrame instead.

Files for a single forecast cycle are downloaded in groups of 20 by default (the group_size parameter of get_files()). The documentation says this accommodates the xarray, dask, and HDF5 backends, which may struggle to open too many files at once, and that it matters mostly for medium-range forecasts.

The package also includes a FileDownloader class for downloading files asynchronously over HTTP, with limit (default 10) and timeout (default 900 seconds) settings.

A single forecast can be spread across hundreds of files, and intermediate processing may use several GB of memory. The recommended minimum system is a 4-core processor and 8 GB of RAM.

## Further reading

* NLDI documentation: https://api.water.usgs.gov/docs/nldi
* OWPHydroTools (hydrotools) GitHub repo: https://github.com/NOAA-OWP/hydrotools
* OWPHydroTools (NWM Client): https://pypi.org/project/hydrotools.nwm-client/8.0.0/ 
* USGS NWIS (recommended source for historical, gauged streamflow): https://waterdata.usgs.gov/nwis
* NWM retrospective archive (Zarr, AWS, for the ungauged-reach case only): https://registry.opendata.aws/nwm-archive/

## Best practices FAQs

See sections below for answers and code examples to the following questions.

* What is the recommended way to download data for **one location across the full period of record**?
* What is the recommended way to download data across **all locations for a small time range**?
* If I am working on improving efficiency through **code parallelization**, what should I do vs avoid?
* [...]