# Glossary

Terms used across the course, defined once. As pages are revised, the first use of each term on a page will link here. For example,
NOAA identifies a river reach by its {term}`COMID`, while USGS uses a {term}`monitoring location ID <Monitoring location ID>`.

To link a term from a page, use the MyST `term` role: `` {term}`COMID` ``, or `` {term}`reaches <Reach>` `` to show
different text. Add new terms to the section where they fit, keeping each section alphabetical.

## Shared concepts

Every data product in the course is introduced with these seven concepts (see the style guide's shared-concept table).

```{glossary}
Data quality flag(s)
: A value attached to a measurement that says how much to trust it. Examples: SWOT's `reach_q` and `wse_qual`,
  and USGS's approval status and qualifiers. NWM model output has no per-value quality flag.

Data unit
: What one "file" or record of a product is: a SWOT granule, one NWM output file per time step,
  or one USGS time series per monitoring location and parameter.

Location identifier
: The ID that says *where* a value applies: a SWOT `reach_id` or `node_id`, an NWM COMID (`feature_id`),
  or a USGS monitoring location ID such as `USGS-12200500`.

Time
: *When* a value applies, and how often values are produced: a SWOT overpass time, an NWM {term}`forecast reference time <Forecast reference time>`
  and {term}`valid time <Valid time>`, or a USGS timestamp (continuous or daily).

Variable
: *What* was measured or modeled, for example water surface elevation (SWOT), streamflow (NWM),
  or discharge and gage height (USGS).

Variable unit
: The units a variable is reported in, for example meters (SWOT water surface elevation), m³/s (NWM streamflow)
  or ft³/s (USGS discharge).

Version / provenance
: Which release of a product a value came from, and from where: a SWOT product version (e.g. `D`) and collection DOI,
  an NWM model version and configuration, or the USGS service and retrieval date.
```

## General data and code terms

```{glossary}
API
: Application programming interface. Here, a web service that returns data in response to a request URL,
  so code can retrieve data without a point-and-click website.

API key
: A personal token that identifies you to an API, often allowing higher request limits. Also called a token or
  personal access token (PAT); the USGS key goes in the `API_USGS_PAT` environment variable. Keep keys in environment
  variables, never in your code.

Conda environment
: An isolated set of Python packages, defined by a file such as `environments/m03-swot.yml`, so a lesson's code
  runs with known package versions.

CONUS
: The contiguous United States: the 48 adjoining states and the District of Columbia, without Alaska, Hawaii
  or the territories.

CRS
: Coordinate reference system: how coordinates map to places on Earth, for example longitude and latitude on the
  WGS84 datum (EPSG:4326) or a projected grid such as UTM. Data from different sources must share a CRS before you overlay them.

Discharge
: The volume of water flowing past a point per unit time, for example in ft³/s or m³/s. Also called streamflow.

DOI
: Digital Object Identifier: a permanent link (`https://doi.org/...`) to a dataset, paper or piece of software. Cite
  datasets by DOI where one exists, with the version and the date you accessed them.

Geoid
: The shape the ocean surface would take under gravity alone, extended under the land; the reference for heights
  "above sea level". SWOT water surface elevations are given relative to a geoid model (EGM2008).

Lead time
: How far ahead a forecast value is: its {term}`valid time <Valid time>` minus its
  {term}`forecast reference time <Forecast reference time>`.

Streamflow
: See {term}`Discharge`.
```

## NASA SWOT

```{glossary}
Cycle and pass
: SWOT's orbit repeats every 21 days; each repeat is a *cycle*. Within a cycle, each numbered *pass* is one
  half-orbit (ascending or descending). A place on the ground is seen by one or more passes per cycle.

earthaccess
: A Python library for logging in to NASA Earthdata and searching, downloading or streaming NASA data granules.

Granule
: The smallest unit of data NASA distributes for a product, usually one file: for SWOT, one product covering
  part of one satellite pass.

hydrocron
: A PO.DAAC web API that returns time series of SWOT river reach and node data (and lake data) as CSV or GeoJSON,
  without downloading whole granules.

KaRIn
: The Ka-band Radar Interferometer, SWOT's main instrument. It measures the height of water surfaces across two
  swaths, one on each side of the satellite's path.

Node
: A point about every 200 m along a SWORD reach. SWOT river data are reported for nodes and reaches.

Pixel cloud (PIXC)
: SWOT's lower-level product of individual radar pixels classified as water or land, with their heights. The river
  ({term}`RiverSP`) and {term}`Raster <SWOT Raster product>` products are built from it.

PO.DAAC
: NASA's Physical Oceanography Distributed Active Archive Center, which distributes SWOT data.

Product description document (PDD)
: The technical document for one SWOT product and version, defining every variable, unit and quality flag.
  Check it before interpreting a flag value.

Reach
: A river segment, typically about 10 km long, defined in SWORD. SWOT river data are reported per reach (`reach_id`).

RiverSP
: SWOT's River Single-Pass Vector product: one record per {term}`reach <Reach>` (or {term}`node <Node>`) per
  overpass, with water surface elevation, width, slope, discharge and quality flags. Collection short names
  look like `SWOT_L2_HR_RiverSP_reach_D`.

Science orbit
: SWOT's 21-day repeat orbit, used since 2023 for routine observations. It followed a 1-day repeat
  calibration ("fast-sampling") orbit used after launch.

SWORD
: The SWOT River Database: a global river network, built before launch, that defines the reaches and nodes
  SWOT river measurements are mapped to.

SWOT
: The Surface Water and Ocean Topography satellite mission (NASA and CNES), which measures water surface elevation,
  width and extent of rivers and lakes from space.

SWOT Raster product
: A gridded SWOT product (100 m or 250 m UTM grid) with water surface elevation, water area and water fraction
  per cell, for one scene of one pass. Collection short names look like `SWOT_L2_HR_Raster_100m_D`.

Water surface elevation
: The height of the water surface above a reference surface. SWOT reports it in meters (`wse`), relative to a geoid
  model (see the SWOT lessons for the exact reference).
```

## NOAA NWM

```{glossary}
COMID
: Common Identifier: the unique numeric ID of a stream reach in the NHDPlus network. In the contiguous U.S. (CONUS),
  NWM's `feature_id` values are the same numbers.

Configuration
: One of the NWM's standard model runs, for example `short_range`, `medium_range`, `long_range`
  or `analysis_assim`, each with its own length (forecast horizon or lookback) and issue schedule.

Data assimilation
: Adjusting a model while it runs so it stays close to observations. The NWM analysis configuration
  assimilates USGS streamflow observations, among others.

Ensemble member
: One of several runs of the same forecast with slightly different inputs. The NWM medium-range forecast has
  six members; their spread is a rough guide to forecast uncertainty.

feature_id
: NWM's name for a reach identifier. In CONUS it is the same number as the NHDPlus {term}`COMID`.

Forcing
: The weather inputs that drive a hydrologic model, such as precipitation, temperature and radiation.

Forecast reference time
: When an NWM forecast was issued (UTC). Also called the reference time. Each forecast value also has a
  {term}`valid time <Valid time>`.

kerchunk
: A Python library that builds reference files describing where each variable sits inside existing files
  (such as NWM NetCDF files), so `xarray` can read only the parts it needs from cloud storage.

NHDPlus
: The National Hydrography Dataset Plus: a geospatial dataset of the U.S. stream network, broken into reaches
  each with a COMID. The NWM runs on this network.

NLDI
: The Network Linked Data Index, a USGS web service that links features such as monitoring locations to NHDPlus
  reaches (COMIDs) and navigates up- or downstream along the network.

NODD
: NOAA Open Data Dissemination, the program that publishes NOAA data, including NWM output, on commercial
  clouds such as AWS and Google Cloud.

NWM
: The National Water Model, NOAA's hydrologic model that simulates and forecasts streamflow for millions of
  river reaches across the United States.

Retrospective simulation
: A long NWM run over historical weather, used for reach-level streamflow records where there is no gage.
  It is a simulation, not archived forecasts.

Valid time
: The time an NWM forecast value applies to (UTC). Valid time minus reference time is the forecast's lead time.
```

## USGS WDFN

```{glossary}
Approval status
: Whether a USGS value is provisional (subject to revision) or approved (reviewed and final).

Continuous values
: USGS sensor values recorded at a fixed interval, typically every 15 minutes. Also called instantaneous values.

Daily values
: USGS values summarized per day, most often the daily mean (statistic code, `statistic_id`, `00003`).

dataretrieval
: A USGS Python package for retrieving USGS water data. Its modernized `waterdata` module uses the
  USGS Water Data APIs; the legacy `nwis` module uses the older services.

Field measurement
: A direct measurement of discharge (or gage height) made by USGS staff at a monitoring location,
  used to build and check the rating curve.

Gage height
: The height of the water surface above a local reference point (the gage datum) at a monitoring location.
  Also called stage.

Monitoring location ID
: The USGS identifier for a place where data are collected, such as `USGS-12200500`.

NWIS
: The National Water Information System, the USGS database behind WDFN. Its older website and web services
  (NWISWeb, WaterServices) are being retired.

Parameter code
: A five-digit USGS code for a variable, for example `00060` for discharge and `00065` for gage height.

Provisional data
: Recent USGS data that have not yet been reviewed and approved, and can change.

Qualifier
: A remark attached to an individual USGS value, for example `ESTIMATED` when ice affected the gage. In
  `dataretrieval` output it is the `qualifier` column, often empty.

Rating curve
: The relationship between gage height and discharge at a monitoring location, fitted to field measurements.
  USGS computes continuous discharge from gage height with it.

Streamgage
: A monitoring location on a stream or river that records {term}`gage height <Gage height>` continuously and
  reports discharge computed from it.

WDFN
: Water Data for the Nation, the USGS website and APIs that publish USGS water data (data stored in NWIS).
```
