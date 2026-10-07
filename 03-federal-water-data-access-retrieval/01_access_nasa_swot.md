# Retrieve NASA SWOT water surface elevation data

There are many ways to find, access, and download NASA SWOT data. This module is going to spend the most time focusing on the recommended patterns for hydrology applications using the water surface elevation (`wse`) data from the SWOT mission. To help build the framework, you need to know that there are two ways to programmatically get access to SWOT data:

1. `earthaccess`: this is a Python library that allows users to access all of the NASA Earthdata stored in the cloud, including SWOT mission data. It streamlined what used to be complex access patterns across different systems and tools in order to help scientists get to the data faster (see more in [this blog post](https://nasa-openscapes.github.io/news/2024-03-04-earthaccess-tech-spotlight/)). Using `earthaccess`, a user can easily authenticate using the Earthdata login, find what data is available, and download or access a variety of products in NASA's cloud storage buckets.
1. `hydrocron`: this is an API built specifically to help streamline timeseries data access to the `SWOT_L2_HR_RIVERSP` data product. The queries allow users to access data across temporal ranges for specific locations, which is in contrast to how the SWOT data are archived (individual shapefiles per timestamp). It allows users who may be interested in a timeseries of data at a small number of locations the ability to easily retrieve that without a lot of extra effort. More on how `hydrocron` works is available in [this NASA news article](https://www.earthdata.nasa.gov/news/hydrocron-new-tool-swot-time-series-analysis).

## Tools and environment setup

In order to complete this lesson about accessing NASA SWOT water surface elevation data, you first need to install a few libraries and create an account.

1. **Make an Earthdata Login account.** In order to _access_ data from the NASA Earthdata system, you will need to create an Earthdata Login account. Please visit [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov) to register and setup your login. 
2. **Install `earthaccess`.** We will be using the NASA `earthaccess` Python library for programmatic authentication to NASA Earthdata systems, data discovery, and data downloads. The recommendation is to install using `mamba` as that is faster; however, other Python library installers such as `conda` and `pip` should also work. See more in their [user quick start guide](https://earthaccess.readthedocs.io/en/latest/user/quick-start/#installing-earthaccess). 

```python
# Install earthaccess
mamba install -c conda-forge earthaccess
```

To login to `earthaccess`, you can type the following and it will prompt you to enter your credentials. There are methods to store your credentials locally using environment variables. You can learn more in the [`earthaccess` authentication docs here](https://earthaccess.readthedocs.io/en/latest/user/howto/authenticate/).

```python
# Login to NASA's Earth data system using earthaccess interactively
import earthaccess
auth = earthaccess.login()
```

> **Known install issue:** `import earthaccess` can fail with an SSL error (`ASN1: NOT_ENOUGH_DATA`) on older Python + newer OpenSSL combos ([details](https://github.com/python/cpython/issues/151504)). **Fix:** use Python 3.12+ (or OpenSSL < 3.5.7 with an older Python).

## Programmatic data discovery

Before you download or try to access the data itself, a common first step in any open data analysis is to first _discover_ or _find_ data in the data system that can meet your research needs. You don't want to download all of the database just to learn which dates are available, that would be incredibly inefficient. Instead, we can do the _discovery_ step and then adjust our data download approach using that information. As you will learn later, this discovery stage can also be a way to initialize information such as locations or times that allows you to build more efficient and scalable data download workflows.

As with many of the methods, a GUI (Graphical User Interface) approach to data discovery does exist. However, programmatic implementations support reproducibility and future extensions or applications of your work. So, while you can navigate to [Earthdata Search](https://search.earthdata.nasa.gov/), know that it would be a good idea to capture your search and discovery steps in code as documentation of the methods. 

There are ways to search Earthdata broadly using general terms if you are unsure of what data product to use, see `seach_datasets` and `search_services` methods in the API documentation [here](https://earthaccess.readthedocs.io/en/latest/api/#earthaccess.api.search_datasets). The object returned from a search can be inspected to extract key information, including the dataset's shorthand name which is critical for querying and downloading the data itself. Below is an example of what you could do to search any Earthdata dataset that is linked to a "river" keyword. 

```python
river_datasets_all = earthaccess.search_datasets(
    keyword="river"
)
len(river_datasets) # 1568 returned
```

This returned over 1500 datasets from a variety of data providers and locations. Let's add more specific querying parameters, such as a spatial and temporal filter to get only cloud-available datasets for an analysis of Minnesota rivers during 2023-2025. 

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
   
The `2.0` vs `D` distinction is referring to the _version_ of the data. `2.0` refers to "Version C", which has now been superseded by "Version D" (see [release notes](https://deotb6e7tfubr.cloudfront.net/s3-edaf5da92e0ce48fb61175c28b67e95d/podaac-ops-cumulus-docs.s3.us-west-2.amazonaws.com/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf?A-userid=None&Expires=1789770555&Signature=l9~jHPuEZ~4K0eelmbOvpbpyQeVy8l7R7GE7EEYBcjJU4c99o82AxGqzKGIMUkrqqlBD4rj3ZXpvBSfKv3zooKzTlIku4kO241r-u9B7qMEEoEkabt3snajLehfIBuNDXWktj7zNE4PfkkuCdBP~NvJbDhIq~TAb20AnBtRwwj8f2WLMePlYPO0c-PXh8QiZXuttew0UfUvbuK9H6zcxcrwLRdcaOxmmRn17KLtnBB3YvKXG1lwHreXOlrzYBxniHv2-OJ~Y4yIDkiLJYvzfzLaYKQgUn6YyUb8Eas~Zm8Tqj5nw1yCrByLQ~056e36aA~uwxc3fDDJ5l-6OBM0A3g__&Key-Pair-Id=K3JC1CAMJ6YYHT)). In addition, each _version_ has two different spatial variants available, "node" (one file per 200m node along a reach) and "reach" (one file per 10km river reach). 

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
[note that 42 granules are returned, need to show how to explore what those are]

[A key element I am learning is that it doesn't error if you get it wrong ... just returns an empty list, not an error]
[TODO NEXT: show what this returns; talk about the options for this function and how to format different temporal ranges, point to docs, show two more examples.]

[*could add more here* CMR, Amazon AWS S3 bucket access all packaged up in `earthaccess`]

## Programmatic data downloads

[remind about the differences between hydrocron/earthaccess + some info about cloud-native data access vs "downloads"]

### `earthaccess`

[what data types this accesses and how to use the results]

### `hydrocron`

While a user can access SWOT data through `earthaccess`, if timeseries data for specific rivers are the desired outcome, then the `hydrocron` API is the tool for the job. As the [`hydrocron` documentation](https://podaac.github.io/hydrocron) states, 

> SWOT data is archived as individually timestamped shapefiles, which would otherwise require users to perform potentially thousands of file IO operations per river feature to view the data as a timeseries. Hydrocron makes this possible with a single API call.

[get into the use-cases for hydrocron and examples for install, etc]

## Best practices FAQs

See sections below for answers and code examples to the following questions.

* What is the recommended way to download data for **one location across the full period of record**?
* What is the recommended way to download data across **all locations for a small time range**?
* If I am working on improving efficiency through **code parallelization**, what should I do vs avoid?
* [...]

### Temporal scaling

What is the recommended way to download data for one location but the full period of record?

### Spatial scaling

What is the recommended way to download data for all locations but a small time range?

### Parallelization

If I am working on improving efficiency of my code through parallelization, what should I do vs avoid?

### [...]

## Further reading

[links out to agency pages on more information, can be duplicates of pages already referenced above]
