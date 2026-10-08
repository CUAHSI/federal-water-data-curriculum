# Additional Federal water data

Now that you have gained a deep knowledge of NASA SWOT water surface elevation, NOAA NWM streamflow, and USGS NWIS discharge data products, you are more equipped to broaden your use of other Federal water data products from these agencies. Consider the following list of related data products:

- NASA SWOT discharge (in development)
- NOAA AORC precipitation
- NOAA NextGen hydrofabric

_Note that there are other Federal agencies producing or using water data, including the Environmental Protection Agency (EPA) and US Army Corps of Engineers (USACE)._

Below are short tours of three related products. Each tour covers what the product is, how it connects to the three products in this course, and a first step for getting it. Each one points to a CUAHSI notebook with a full worked example. These products build on the skills from Module 3: the same `earthaccess` login and the same habit of discovering before downloading. The AORC example also introduces a new pattern, opening a cloud-optimized Zarr store lazily with `xarray`. The code runs in the Module 4 environment, `environments/synthesis.yml` (in the course repository) [TODO: confirm synthesis.yml includes earthaccess, xarray, fsspec, s3fs, zarr and pyproj].

## NASA SWOT discharge: the SWORD of Science (SoS)

SWOT measures water surface elevation, width and slope, not discharge. Discharge is estimated afterwards by the SWOT Discharge Algorithm Working Group (DAWG), which runs several discharge algorithms over SWORD reaches in a cloud workflow called Confluence. The **SWORD of Science (SoS)** collects the results: the prior information each algorithm used (for example, gage records and model estimates) and the discharge estimates themselves, for every reach, organized by continent ([PO.DAAC SoS tutorial](https://podaac.github.io/tutorials/notebooks/datasets/SWOT_L4_DAWG_SOS_DISCHARGE.html)). It is a Level 4 product, and the discharge estimates are still being developed and validated.

SoS files are found with `earthaccess`, like every other SWOT product. `earthaccess.login()` reads `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` from the environment (see the Module 3 SWOT lesson for setup). The short name below is the Version 3 collection, as listed by `earthaccess.search_datasets(keyword="SWOT SoS discharge")`; older notebooks use the earlier name `SWOT_L4_DAWG_SOS_DISCHARGE`.

```python
import earthaccess

earthaccess.login()
sos = earthaccess.search_data(short_name="SWOT_L4_HR_DAWG_SOS_DISCHARGE_V3")
for g in sos:
    print(g["umm"]["GranuleUR"], round(g.size / 1024, 1), "GB")  # g.size is in MB
```

```
na_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 9.2 GB
af_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 4.1 GB
eu_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 6.9 GB
sa_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 8.5 GB
as_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 26.6 GB
oc_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 1.9 GB
```

Two things to notice before you download:

- **One file per continent, and they are large.** The North America file alone is about 9 GB, and Asia's about 27 GB. If you work outside the cloud, read only the groups and reaches you need (see the notebooks below), or work on a cloud JupyterHub in AWS `us-west-2`.
- **Know what is inside.** Each file is NetCDF with one group per algorithm (plus the priors and validation data), indexed by SWORD `reach_id`, with discharge in m³/s. `unconstrained` in the name means the algorithms ran without using gage data; Module 2 describes the gauge-constrained alternative.
- **Check the time period.** These Version 3 files cover May 2023 to May 2025 (it's in the file name), so they do not include the December 2025 Skagit flood used in this module. `hydrocron` can also return SoS discharge fields (for example `sos_consensus_q`) for a single reach, using `collection_name=SWOT_L2_HR_RiverSP_2.0` ([Hydrocron timeseries docs](https://podaac.github.io/hydrocron/timeseries)).

[PARTNER REVIEW: NASA] Confirm the description of SoS, its development status, and the recommended way to get discharge for a few reaches (SoS files vs. `hydrocron`).

**Go further:** the CUAHSI notebooks [SWOT - Visualizing SOS Discharge with Xarray](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/SWOT%20-%20Visualizing%20SOS%20Discharge%20with%20Xarray) and [SWOT - Compare Observed and SoS Discharge](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/SWOT%20-%20Compare%20Observed%20and%20SoS%20Discharge) open the SoS groups with `xarray` and compare SoS discharge with community gage data.

## NOAA AORC precipitation

The **Analysis of Record for Calibration (AORC)** is a gridded, hourly record of precipitation and other near-surface weather (temperature, humidity, wind, radiation) over the contiguous United States. The copy used here, in the NWM retrospective archive, is on the 1 km NWM grid [TODO: verify native AORC resolution]. It is the historical weather forcing used to calibrate the National Water Model and to drive its retrospective simulation ([AWS Registry of Open Data: NWM archive](https://registry.opendata.aws/nwm-archive/)). That makes it the natural precipitation dataset to pair with NWM streamflow, and a good first look at what "caused" a hydrograph. NOAA publishes it as cloud-optimized Zarr stores in the NWM retrospective archive on the [AWS Registry of Open Data](https://registry.opendata.aws/nwm-archive/). No account or key is needed.

Zarr lets `xarray` open the whole dataset _lazily_: only metadata is read until you ask for values. This example pulls hourly precipitation for December 2022 (the last full December in this copy, which ends in January 2023) at the grid cell nearest USGS 12200500. The gage coordinates come from its [USGS monitoring-location record](https://api.waterdata.usgs.gov/ogcapi/v0/collections/monitoring-locations/items/USGS-12200500).

```python
import fsspec
import pyproj
import xarray as xr

store = fsspec.get_mapper("s3://noaa-nwm-retrospective-3-0-pds/CONUS/zarr/forcing/precip.zarr", anon=True)
aorc = xr.open_zarr(store)
print(aorc.sizes, aorc.time.values[[0, -1]])

# The grid is Lambert Conformal Conic; convert the gage location into grid coordinates
lcc = pyproj.CRS.from_proj4(aorc["RAINRATE"].attrs["proj4"])
x, y = pyproj.Transformer.from_crs("EPSG:4326", lcc, always_xy=True).transform(-122.3354, 48.4448)

rain = aorc["RAINRATE"].sel(x=x, y=y, method="nearest").sel(time=slice("2022-12-01", "2022-12-31"))
mm_per_hour = (rain * 3600).load()  # RAINRATE is in mm/s
print(mm_per_hour.size, "hours, total", round(float(mm_per_hour.sum()), 1), "mm")
```

```
Frozen({'time': 385704, 'y': 3840, 'x': 4608}) ['1979-02-01T00:00:00.000000000' '2023-01-31T23:00:00.000000000']
744 hours, total 151.1 mm
```

The full dataset is about 27 TB, but this request reads only the few chunks that contain the one grid cell and one month. It still takes about a minute from a laptop, because each chunk holds 28 days for a 350 × 350 km block. This **retrospective** copy ends in January 2023, so it does not cover the December 2025 flood. For recent events, NOAA distributes AORC through other channels [TODO: verify the current access route for post-2023 AORC data].

[PARTNER REVIEW: NOAA] Confirm the AORC description, its role in NWM calibration and retrospective forcing, and the recommended source for recent AORC data.

**Go further:** the CUAHSI notebook [Collecting and Manipulating AORC Data](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/AORC%20-%20Data%20Collection%20and%20Manipulation%20Primer) by Tony Castronova, Irene Garousi-Nejad, Danielle Tijerina-Kreuzer and Abner Bogan shows how to subset AORC by watershed with `dask` and `geopandas`. The example above is adapted from it (CUAHSI notebooks, GPL-3.0).

## NOAA NextGen hydrofabric

The National Water Model routes water over the NHDPlus river network (Module 2). NOAA's **Next Generation Water Resources Modeling Framework (NextGen)** uses a new network, the **hydrofabric**: a consistent set of catchments (_divides_), flowpaths, nexus points, lakes and attributes, built so that different models can run on the same river network. If you work with NextGen output, or need catchment boundaries and flowpath attributes that line up with future NOAA products, the hydrofabric is where you start. It also links back to NHDPlus COMIDs and to gage locations (_hydrolocations_), which is how you would connect it to the USGS and NWM data in this course.

The hydrofabric is distributed as GeoPackage files by Lynker Spatial [TODO: verify Lynker Spatial's role and the NHDPlus/hydrolocation links described above]. **At time of writing, the files at the public path used in the CUAHSI notebook (`s3://lynker-spatial/hydrofabric/v2.2/conus/conus_nextgen.gpkg`) are listed but no longer readable anonymously**, and the v2.2 data carry a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 license (per `license.txt` in `s3://lynker-spatial/hydrofabric/v2.2/`). Check the [Lynker Spatial data page](https://www.lynker-spatial.com/data) for current access terms before building a workflow on it.
[TODO: confirm the current public access route for the NextGen hydrofabric (NOAA-hosted copy? registration?) and add a runnable discovery example]
[PARTNER REVIEW: NOAA] Confirm the description of the hydrofabric and the recommended source for researchers.

**Go further:** the CUAHSI notebook [Accessing the NGEN HydroFabric on S3](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/NGEN%20-%20Hydrofabric%20Exploration) by Tony Castronova and Irene Garousi-Nejad shows how to read hydrofabric layers for a bounding box with `geopandas`, without downloading the whole file. Its data path currently returns a permission error (see the note above).

## Further reading

- [PO.DAAC SWOT Cookbook](https://podaac.github.io/tutorials/quarto_text/SWOT.html), including the [SoS discharge tutorial](https://podaac.github.io/tutorials/notebooks/datasets/SWOT_L4_DAWG_SOS_DISCHARGE.html).
- [NWM retrospective archive, including AORC forcing (AWS Registry of Open Data)](https://registry.opendata.aws/nwm-archive/).
- [NextGen framework (NOAA-OWP on GitHub)](https://github.com/NOAA-OWP/ngen).
- Adapted from [Collecting and Manipulating AORC Data](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/AORC%20-%20Data%20Collection%20and%20Manipulation%20Primer) by Tony Castronova, Irene Garousi-Nejad, Danielle Tijerina-Kreuzer and Abner Bogan, CUAHSI notebooks (GPL-3.0).
- Adapted from [SWOT - Visualizing SOS Discharge with Xarray](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/SWOT%20-%20Visualizing%20SOS%20Discharge%20with%20Xarray), CUAHSI notebooks (GPL-3.0).
- Adapted from [SWOT - Compare Observed and SoS Discharge](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/SWOT%20-%20Compare%20Observed%20and%20SoS%20Discharge), CUAHSI notebooks (GPL-3.0). [TODO: verify authors of both SoS notebooks (shallow clone shows no author list)]
- [Accessing the NGEN HydroFabric on S3](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/NGEN%20-%20Hydrofabric%20Exploration) by Tony Castronova and Irene Garousi-Nejad, CUAHSI notebooks (GPL-3.0).
