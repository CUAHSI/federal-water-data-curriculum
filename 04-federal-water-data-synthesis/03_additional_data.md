# Additional Federal water data

Now that you have worked with NASA Surface Water and Ocean Topography (SWOT) water surface elevation, NOAA National Water Model (NWM) streamflow, and USGS Water Data for the Nation (WDFN) discharge data products, you are more equipped to broaden your use of other Federal water data products and tools. Consider the following:

- NASA SWOT data in the browser: SWOTViz, a CUAHSI viewer (in development)
- NASA SWOT discharge (in development)
- NOAA AORC precipitation
- NOAA NextGen hydrofabric

_Note that there are other Federal agencies producing or using water data, including the Environmental Protection Agency (EPA) and US Army Corps of Engineers (USACE)._

Below is a short pointer to SWOTViz, then short tours of three related products. Each tour covers what the product is, how it connects to the three products in this course, and a first step for getting it. Each one points to a CUAHSI notebook with a full worked example. These products build on the skills from Module 3: the same `earthaccess` login and the same habit of discovering before downloading. The AORC example also introduces a new pattern, opening a cloud-optimized Zarr store lazily with `xarray`. The code runs in the Module 4 {term}`conda environment <Conda environment>`, `environments/m04-synthesis.yml` (in the course repository); the outputs below came from `earthaccess` 0.19.0, `xarray` 2026.9.0 and `zarr` 3.4.0 on Python 3.14.

## Exploring SWOT data in the browser: SWOTViz

Before writing code, it often helps to *look*: which SWOT reaches cover your river, how often they were observed, and whether the time series look sensible. [SWOTViz](https://swotviz.cuahsi.io/) is a CUAHSI web viewer for SWOT river and lake data. It shows SWORD {term}`reaches <Reach>` and {term}`nodes <Node>` and Prior Lake Database lakes on a map, along with SWOT orbit tracks and pass counts, and plots a selected feature's time series from {term}`hydrocron`, with options to download the data. It is a quick way to find reach IDs and check data coverage before you use the code patterns from Module 3. Its source code is on GitHub ([CUAHSI/SWOT-Data-Viewer](https://github.com/CUAHSI/SWOT-Data-Viewer), GPL-3.0).

:::{admonition} TODO (dev team): SWOTViz readiness
:class: attention
SWOTViz is in development; confirm it's ready to point learners to. If it is, add a screenshot (for example, the Skagit reaches used in the case study) with alt text, and check the feature description above against the current release.
:::

## NASA SWOT discharge: the SWORD of Science (SoS)

SWOT measures water surface elevation, width and slope, not discharge. Discharge is estimated afterwards by the SWOT Discharge Algorithm Working Group (DAWG), which runs several discharge algorithms over SWORD reaches in a cloud workflow called Confluence. The **SWORD of Science (SoS)** collects the results: the prior information each algorithm used (for example, gage records and model estimates) and the discharge estimates themselves, for every reach, organized by continent ([PO.DAAC SoS tutorial](https://podaac.github.io/tutorials/notebooks/datasets/SWOT_L4_DAWG_SOS_DISCHARGE.html)). It is a Level 4 product, and the discharge estimates are still being developed and validated.

SoS files are found with {term}`earthaccess`, like every other SWOT product. `earthaccess.login()` reads `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` from the environment (see the Module 3 SWOT lesson for setup). The short name below is the Version 3 collection, as listed by `earthaccess.search_datasets(keyword="SWOT SoS discharge")`; older notebooks use the earlier name `SWOT_L4_DAWG_SOS_DISCHARGE`.

```python
import earthaccess

earthaccess.login()
sos = earthaccess.search_data(short_name="SWOT_L4_HR_DAWG_SOS_DISCHARGE_V3")
for g in sos:
    print(g["umm"]["GranuleUR"], round(g.size / 1024, 1), "GB")  # g.size is in MB
```

```text
na_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 9.2 GB
af_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 4.1 GB
eu_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 6.9 GB
sa_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 8.5 GB
as_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 26.6 GB
oc_sword_v16_SOS_results_unconstrained_20230502T204408_20250502T204408_20251219T163700 1.9 GB
```

Three things to notice before you download:

- **One file per continent, and they are large.** The North America file alone is about 9 GB, and Asia's about 27 GB. If you work outside the cloud, read only the groups and reaches you need (see the notebooks below), or work on a cloud JupyterHub in AWS `us-west-2`.
- **Know what is inside.** Each file is NetCDF with one group per algorithm (plus the priors and validation data), indexed by SWORD `reach_id`, with discharge in m³/s. `unconstrained` in the name means the algorithms ran without using gage data; Module 2 describes the gauge-constrained alternative.
- **Check the time period and version.** These Version 3 files cover May 2023 to May 2025 (it's in the file name), so they do not include the December 2025 Skagit flood used in this module. `hydrocron` can also return SoS discharge fields (for example `sos_consensus_q`) for a single reach, using `collection_name=SWOT_L2_HR_RiverSP_2.0` ([Hydrocron timeseries docs](https://podaac.github.io/hydrocron/timeseries)). That is the Version C collection, a different version from the Version D data in the case study, so don't mix values from the two without checking. Cite the collection by its DOI ([10.5067/SWOT-SOS-RD3](https://doi.org/10.5067/SWOT-SOS-RD3)), and record the collection short name (it carries the version) and the file name with any SoS results, since each new version reprocesses the whole record.

:::{admonition} Partner review (NASA): NASA SWOT discharge: the SWORD of Science (SoS)
:class: important
Confirm the description of SoS, its development status, and the recommended way to get discharge for a few reaches (SoS files vs. `hydrocron`).
:::

**Go further:** the CUAHSI notebooks [SWOT - Visualizing SOS Discharge with Xarray](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/SWOT%20-%20Visualizing%20SOS%20Discharge%20with%20Xarray) and [SWOT - Compare Observed and SoS Discharge](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/SWOT%20-%20Compare%20Observed%20and%20SoS%20Discharge) open the SoS groups with `xarray` and compare SoS discharge with community gage data.

:::{admonition} TODO (dev team): confirm this link
:class: attention
Both SoS notebooks are on the CUAHSI/notebooks `develop` branch. Confirm these are the links learners should use (branch, path and notebook name); keep the attribution either way.
:::

## NOAA AORC precipitation

The **Analysis of Record for Calibration (AORC)** is a gridded, hourly record of precipitation and other near-surface weather (temperature, humidity, wind, radiation) over the contiguous United States. The copy used here, in the NWM retrospective archive, is on the 1 km NWM grid. It is the historical weather forcing used to calibrate the National Water Model and to drive its retrospective simulation ([AWS Registry of Open Data: NWM archive](https://registry.opendata.aws/nwm-archive/)). That makes it the natural precipitation dataset to pair with NWM streamflow, and a good first look at what "caused" a hydrograph. NOAA publishes it as cloud-optimized Zarr stores in the NWM retrospective archive on the [AWS Registry of Open Data](https://registry.opendata.aws/nwm-archive/). No account or key is needed.

:::{admonition} TODO (dev team): AORC native resolution
:class: attention
Verify native AORC resolution.
:::

Zarr lets `xarray` open the whole dataset _lazily_: only metadata is read until you ask for values. This example pulls hourly precipitation for December 2022 (the last full December in this copy, which ends in January 2023) at the grid cell nearest USGS 12200500. The month isn't tied to a particular flood; it simply demonstrates access. To look at what caused a hydrograph, choose a high-flow event inside the record (1979 to January 2023) and plot it next to the gage's discharge. The gage coordinates come from its [USGS monitoring-location record](https://api.waterdata.usgs.gov/ogcapi/v0/collections/monitoring-locations/items/USGS-12200500).

```python
import fsspec
import pyproj
import xarray as xr

store = fsspec.get_mapper("s3://noaa-nwm-retrospective-3-0-pds/CONUS/zarr/forcing/precip.zarr", anon=True)
aorc = xr.open_zarr(store)
print(aorc.sizes, aorc.time.values[[0, -1]])

# The grid is Lambert Conformal Conic; convert the gage location into grid coordinates
lcc = pyproj.CRS.from_proj4(aorc["RAINRATE"].attrs["proj4"])
# USGS 12200500 (Skagit River near Mount Vernon), from its USGS monitoring-location record
gage_lon, gage_lat = -122.3354, 48.4448
x, y = pyproj.Transformer.from_crs("EPSG:4326", lcc, always_xy=True).transform(gage_lon, gage_lat)

rain = aorc["RAINRATE"].sel(x=x, y=y, method="nearest").sel(time=slice("2022-12-01", "2022-12-31"))
mm_per_hour = (rain * 3600).load()  # RAINRATE is in mm/s
print(mm_per_hour.size, "hours, total", round(float(mm_per_hour.sum()), 1), "mm")
```

```text
Frozen({'time': 385704, 'y': 3840, 'x': 4608}) ['1979-02-01T00:00:00.000000000' '2023-01-31T23:00:00.000000000']
744 hours, total 151.1 mm
```

`aorc` is a lazy `xarray` Dataset of 1 km grid cells (`x`, `y` in the model's Lambert Conformal Conic projection, in meters) and hourly `time` steps. `RAINRATE` is the precipitation rate in mm/s, so multiplying by 3,600 gives millimeters per hour; `mm_per_hour` is a 744-value DataArray, one value per hour of December 2022 in UTC. AORC has no per-value quality flag. Its {term}`version and provenance <Version / provenance>` are in the path: this is the copy published with the NWM v3.0 retrospective (`noaa-nwm-retrospective-3-0-pds`), so record that path with any results.

To see what the data look like, plot the hourly series:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 3.5))
ax.bar(mm_per_hour["time"].values, mm_per_hour.values, width=1 / 24, color="#2a78d6")  # one bar per hour
ax.set_ylabel("Precipitation (mm/h)")
ax.set_xlabel("Time (UTC)")
ax.set_title("AORC hourly precipitation at the grid cell nearest USGS 12200500, December 2022")
fig.autofmt_xdate()
plt.show()
```

:::{figure} ../images/m04/additional-aorc-precipitation.png
:alt: Bar chart of hourly precipitation through December 2022 at the AORC grid cell nearest the Skagit River gage near Mount Vernon. Most hours are dry or under 1 millimeter per hour; rain falls in several multi-day storms, with the largest hourly values a few millimeters per hour.
:width: 100%

Hourly AORC precipitation at the 1 km grid cell nearest USGS 12200500, December 2022 (151 mm in total). Data: AORC forcing from the NOAA NWM v3.0 retrospective archive (`s3://noaa-nwm-retrospective-3-0-pds/CONUS/zarr/forcing/precip.zarr`), Registry of Open Data on AWS, accessed 2026-10-08.
:::

The full dataset is about 27 TB, but this request reads only the few chunks that contain the one grid cell and one month. It still takes about a minute from a laptop, because each chunk holds 28 days for a 350 × 350 km block. This **retrospective** copy ends in January 2023, so it does not cover the December 2025 flood. For recent events, NOAA distributes AORC through other channels.

:::{admonition} TODO (dev team): Post-2023 AORC access
:class: attention
Verify the current access route for post-2023 AORC data.
:::

:::{admonition} Partner review (NOAA): NOAA AORC precipitation
:class: important
Confirm the AORC description, its role in NWM calibration and retrospective forcing, and the recommended source for recent AORC data.
:::

**Go further:** the CUAHSI notebook [Collecting and Manipulating AORC Data](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/AORC%20-%20Data%20Collection%20and%20Manipulation%20Primer) by Tony Castronova, Irene Garousi-Nejad, Danielle Tijerina-Kreuzer and Abner Bogan shows how to subset AORC by watershed with `dask` and `geopandas`. The example above is adapted from it (CUAHSI notebooks, GPL-3.0).

:::{admonition} TODO (dev team): confirm this link
:class: attention
The AORC notebook link points to a folder on the CUAHSI/notebooks `develop` branch. Confirm it is the link learners should use (branch, path and notebook name); keep the attribution either way.
:::

## NOAA NextGen hydrofabric

The National Water Model routes water over the NHDPlus river network (Module 2). NOAA's **Next Generation Water Resources Modeling Framework (NextGen)** uses a new network, the **hydrofabric**: a consistent set of catchments (_divides_), flowpaths, nexus points, lakes and attributes, built so that different models can run on the same river network. If you work with NextGen output, or need catchment boundaries and flowpath attributes that line up with future NOAA products, the hydrofabric is where you start. It also links back to NHDPlus COMIDs and to gage locations (_hydrolocations_), which is how you would connect it to the USGS and NWM data in this course.

The hydrofabric is distributed as GeoPackage files by Lynker Spatial. **At time of writing, the files at the public path used in the CUAHSI notebook (`s3://lynker-spatial/hydrofabric/v2.2/conus/conus_nextgen.gpkg`) are listed but no longer readable anonymously**, and the v2.2 data carry a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 license (per `license.txt` in `s3://lynker-spatial/hydrofabric/v2.2/`). Check the [Lynker Spatial data page](https://www.lynker-spatial.com/data) for current access terms before building a workflow on it.

:::{admonition} TODO (dev team): NextGen hydrofabric access route
:class: attention
Confirm the current public access route for the NextGen hydrofabric (NOAA-hosted copy? registration?) and add a runnable discovery example.
:::

:::{admonition} Partner review (NOAA): NOAA NextGen hydrofabric
:class: important
Confirm the description of the hydrofabric and the recommended source for researchers.
:::

:::{admonition} TODO (dev team): Lynker Spatial and hydrolocations
:class: attention
Verify Lynker Spatial's role and the NHDPlus/hydrolocation links described above.
:::

**Go further:** the CUAHSI notebook [Accessing the NGEN HydroFabric on S3](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/NGEN%20-%20Hydrofabric%20Exploration) by Tony Castronova and Irene Garousi-Nejad shows how to read hydrofabric layers for a bounding box with `geopandas`, without downloading the whole file. Its data path currently returns a permission error (see the note above).

:::{admonition} TODO (dev team): confirm this link
:class: attention
The hydrofabric notebook link points to a folder on the CUAHSI/notebooks `develop` branch. Confirm it is the link learners should use (branch, path and notebook name); keep the attribution either way.
:::

## Further reading

- [PO.DAAC SWOT Cookbook](https://podaac.github.io/tutorials/quarto_text/SWOT.html), including the [SoS discharge tutorial](https://podaac.github.io/tutorials/notebooks/datasets/SWOT_L4_DAWG_SOS_DISCHARGE.html).
- [NWM retrospective archive, including AORC forcing (AWS Registry of Open Data)](https://registry.opendata.aws/nwm-archive/).
- [NextGen framework (NOAA-OWP on GitHub)](https://github.com/NOAA-OWP/ngen).
- Adapted from [Collecting and Manipulating AORC Data](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/AORC%20-%20Data%20Collection%20and%20Manipulation%20Primer) by Tony Castronova, Irene Garousi-Nejad, Danielle Tijerina-Kreuzer and Abner Bogan, CUAHSI notebooks (GPL-3.0).
- Adapted from [SWOT - Visualizing SOS Discharge with Xarray](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/SWOT%20-%20Visualizing%20SOS%20Discharge%20with%20Xarray), CUAHSI notebooks (GPL-3.0).
- Adapted from [SWOT - Compare Observed and SoS Discharge](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/SWOT%20-%20Compare%20Observed%20and%20SoS%20Discharge), CUAHSI notebooks (GPL-3.0).

  :::{admonition} TODO (dev team): SoS notebook authors
  :class: attention
  Verify authors of both SoS notebooks (shallow clone shows no author list).
  :::

- [Accessing the NGEN HydroFabric on S3](https://github.com/CUAHSI/notebooks/tree/develop/Data%20Access%20Examples/NGEN%20-%20Hydrofabric%20Exploration) by Tony Castronova and Irene Garousi-Nejad, CUAHSI notebooks (GPL-3.0).
- [SWOTViz](https://swotviz.cuahsi.io/) (CUAHSI), source code at [CUAHSI/SWOT-Data-Viewer](https://github.com/CUAHSI/SWOT-Data-Viewer) (GPL-3.0).

:::{admonition} TODO (dev team): confirm this link
:class: attention
The four CUAHSI notebook links in this list (AORC, both SoS notebooks and the hydrofabric notebook) point on the CUAHSI/notebooks `develop` branch. Confirm it is the link learners should use (branch, path and notebook name); keep the attribution either way.
:::

