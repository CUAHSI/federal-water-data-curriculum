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

## Programmatic data discovery

Before you download or try to access the data itself, a common first step in any open data analysis is to first _discover_ or _find_ data in the data system that can meet your research needs. You don't want to download all of the database just to learn which dates are available, that would be incredibly inefficient. Instead, we can do the _discovery_ step and then adjust our data download approach using that information. As you will learn later, this discovery stage can also be a way to initialize information such as locations or times that allows you to build more efficient and scalable data download workflows.

As with many of the methods, a GUI (Graphical User Interface) approach to data discovery does exist. However, programmatic implementations support reproducibility and future extensions or applications of your work. So, while you can navigate to [Earthdata Search](https://search.earthdata.nasa.gov/), know that it would be a good idea to capture your search and discovery steps in code as documentation of the methods. 

There are ways to search Earthdata broadly using general terms if you are unsure of what data product to use, see `seach_datasets` and `search_services` methods in the API documentation [here](https://earthaccess.readthedocs.io/en/latest/api/#earthaccess.api.search_datasets). However, in this lesson, we know that we are specifically interested in searching the available data for within the data product `L2_HR_RiverSP`. That is considered the "short name", which we can use along with a few other criteria in the `search_data` method.

```python
# Find available granules (aka "files") during 2025 that cover the headwaters of the Mississippi River
mississippi_headwaters_2025 = earthaccess.search_data(
    short_name="L2_HR_RiverSP",
    bounding_box=(-95.355620, 46.950262, -93.465587, 47.739323),
    temporal=("2025-01", "2025-12")
)
```

[TODO NEXT: show what this returns; talk about the options for this function and how to format different temporal ranges, point to docs, show two more examples.]

[*could add more here* CMR, Amazon AWS S3 bucket access all packaged up in `earthaccess`]

[As of 2026-07-23, LPlatt is getting an error with the installed earthaccess tool. Apparently related to [this GitHub issue for something with openssl](https://github.com/python/cpython/issues/151504). Probably upgrading some stuff will help, but I don't have time today. I can't test the code I wrote above, so need to do some verification still.]

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
