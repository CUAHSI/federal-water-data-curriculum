# Retrieve USGS NWIS streamflow data
 
USGS's National Water Information System (NWIS) is the authoritative source for observed, gauged streamflow.
 
USGS currently has two generations of that service running side by side:
 
1. **Legacy NWIS Water Services** (waterservices.usgs.gov): the original, stable API most existing tutorials and packages are built around.
2. **Modernized Water Data APIs** (api.waterdata.usgs.gov): USGS's newer replacement, covering daily values, instantaneous values, field measurements, and water quality (Samples database). USGS is actively encouraging migration to this one, and it supports API keys for higher rate limits.
This module uses the `dataretrieval` Python package, which wraps both generations.
 
1. **Programmatic data discovery**: before pulling values, you typically need a site number (an 8 to 15 digit USGS site ID). Discovery here means searching by region, HUC, or parameter rather than looking up a single known ID.
1. **Programmatic data downloads**: once you have site number(s), `dataretrieval` retrieves the actual values, daily, instantaneous, statistical, or peak-flow, depending on what you need.
If you already know your site number(s), you can skip programmatic data discovery.
 
## Tools and environment setup
 
### USGS Water Data API Token
NWIS is public and doesn't require an account for the legacy service. The modernized Water Data API works without a key too, but USGS recommends getting one for higher rate limits, so we will demonstrate that.

1. Request a USGS Water Data API Token: https://api.waterdata.usgs.gov/signup/
2. Save it in a safe place (KeyPass or other password management tool)
3. Add it as environment variable
4. Restart
 
 ### Create a Conda environment
```bash
conda create -n nwis-env python=3.11 -y
conda activate nwis-env
python3 -m pip install --upgrade pip wheel
python3 -m pip install dataretrieval

# we'll pretend the token that was created is 'abc123'
conda env config vars set API_USGS_PAT="abc123"
conda activate nwis-env

# install and register this environment as a kernel option
python3 -m pip install ipykernel
python3 -m ipykernel install --user --name nwis-env --display-name "Python (nwis-env)"
```
You can test that the token saved to your environment.
```Python
import os

print(os.getenv("API_USGS_PAT"))
```

## Programmatic data discovery

### dataRetrieval help:
```python

parameter_codes = waterdata.get_reference_table("parameter-codes")
statistic_codes = waterdata.get_reference_table("statistic-codes")
# Others:
agency_codes = waterdata.get_reference_table("agency-codes")
aquifer_codes = waterdata.get_reference_table("aquifer-codes")
aquifer_types = waterdata.get_reference_table("aquifer-types")
coordinate_datum_codes = waterdata.get_reference_table("coordinate-datum-codes")
huc_codes = waterdata.get_reference_table("hydrologic-unit-codes")
national_aquifer_codes = waterdata.get_reference_table("national-aquifer-codes")
reliability_codes = waterdata.get_reference_table("reliability-codes")
site_types = waterdata.get_reference_tablea("site-types")
topographic_codes = waterdata.get_reference_table("topographic-codes")
time_zone_codes = waterdata.get_reference_table("time-zone-codes")
counties = waterdata.get_reference_table("counties")
states = waterdata.get_reference_table("states")
```
 
Before downloading values, a common first step is to *discover* which site(s) match your question, by location, HUC, or the parameter you care about, rather than assuming you already know the exact site number.
 
A GUI approach exists here too: the [NWIS Mapper](https://maps.waterdata.usgs.gov/mapper/) lets you click around, search by location name, street address, state/territory, or even watershed regions to find sites visually. This is fine for exploring, but a programmatic discovery step keeps your work reproducible.
 
**Example: What are the USGS stream sites in the Suffolk County, MA area?**
 
```python
from dataretrieval import waterdata

site_info, md = waterdata.get_monitoring_locations(
    state_name = "Massachusetts",
    county_name = "Suffolk County",
    site_type="Stream",
)

site_info
```
  
Once you have site number(s), move on to downloads below.
 
## Programmatic data downloads
 
### `dataretrieval`
 
**Key pieces**

* `dataretrieval.waterdata` (modernized, API key recommended for heavier use): the actively developed replacement, covering the same data types plus discrete water quality (Samples database).
* Canonical outputs are `pandas.DataFrame`s alongside a metadata object describing the query, similar in spirit to hydrotools' canonical columns for NWM/NWIS joins.

**Example: Daily mean values of discharge for stream sites in Suffolk County, MA**
 
```python
sites_available, md = waterdata.get_combined_metadata(
  state_name = "Massachusetts",
  county_name = "Suffolk County",
  site_type= "Stream",
  parameter_code = "00060", # discharge parameter code
  statistic_id = "00003" # mean statistic code
)
```
 
## Best practices FAQs
 
See sections below for answers and code examples to the following questions.
 
* What is the recommended way to download data for **one location across the full period of record**?
* What is the recommended way to download data across **all locations for a small time range**?
* If I am working on improving efficiency through **code parallelization**, what should I do vs avoid?

### Temporal scaling
 
**What is the recommended way to access data for one location but the full period of record?**
 
```Python
daily_data, md = waterdata.get_daily(
    monitoring_location_id= "USGS-05427930", # random monitoring location
    parameter_code="00060",
    statistic_id="00003"
)

daily_data
```

### Spatial scaling
 
**What is the recommended way to download data across all locations but a small time range?**
 
```python
nonspecific_location, md = waterdata.get_daily(
    parameter_code="00060",
    statistic_id="00003",
    time="2022-01-01", # specific date, but you can give time parameter as a bounded interval, half-bounded interval, or duration object
)

nonspecific_location
```

### Parallelization
 
If I am working on improving efficiency of my code through parallelization, what should I do vs avoid?
  
## Further reading
 
* `dataretrieval` (Python) GitHub repo: https://github.com/DOI-USGS/dataretrieval-python
* `dataretrieval` documentation: https://doi-usgs.github.io/dataretrieval-python/
* Modernized Water Data API docs: https://api.waterdata.usgs.gov/
* NWIS Mapper (GUI): https://maps.waterdata.usgs.gov/mapper/