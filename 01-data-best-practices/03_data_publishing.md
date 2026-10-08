# Data Publishing

Publishing is where the data best practices we have covered so far come full circle. Organizing your files, using open formats, and documenting your work are all steps toward one goal: making your data and code usable by someone who has never met you, five years from now, without having to email you. Publishing is the step that makes that possible.
 
You may wonder why data and code should be published on their own, separately from the journal article that first used them. A paper is a summary of your work, and the data and code are the evidence behind it. Publishing them as their own products means they can be checked, reused, and built upon, and it means you receive credit when someone does. Research has also shown that [papers that cite their data are more likely to be cited](https://doi.org/10.1371/journal.pone.0230416). Funders and journals are increasingly asking for it as well. For example, [AGU journals](https://data.agu.org/resources/agu-data-software-sharing-guidance) require an Availability Statement in the Open Research section that points readers to the data (and to software that is central to the research), ideally with a DOI. Statements saying data are "available from the authors" are not accepted.
 
It is important to emphasize that this is not just about getting something posted online. The open science part is about whether your final product can **stand the test of time**: still findable, still openable, and still understandable by the wider scientific community long after your project team has moved on. A file on a lab website, Google Drive, Box, or an FTP server may be convenient, but these are not citable and not permanent storage, so they are not a substitute for publishing in a repository.
 
A helpful way to think about what goes where is share, cite, and mention:
 
- **Share** (with a DOI) the data and code you produced, such as the data behind your figures, the script that makes them, or a model you developed.
- **Cite** the data and software others created that you reused.
- **Mention** the tools you used but can't archive, such as commercial software, including the version.
If you are working alongside a paper, a good rule of thumb is to choose your repository early, since some have review steps that take a few weeks and you don't want data publication to hold up your manuscript. Share a private review link with editors and reviewers if the data aren't public yet, then make everything public and cite the DOIs in your references by the time the paper is accepted.

## FAIR in action

We introduced the FAIR principles in the Open Science section. Here we look at what they actually look like at the moment of publishing. Each letter comes down to a concrete decision you make:
 
- **F:** a persistent identifier is assigned and the data are placed where they can be searched.
- **A:** an access protocol and sharing status are set, and any restrictions are stated.
- **I:** a standard repository and open, non-proprietary formats are chosen.
- **R:** a license and rich metadata are attached.

Many repositories and services can check some of these automatically. [DataONE's MetaDIG engine](https://github.com/NCEAS/metadig-checks) is a good example. It runs a suite of open source checks, such as whether the metadata document is valid against its schema, and sorts the results into F, A, I, and R. Looking at a report like this for a real dataset is a great way to see what FAIR means in practice. One caveat is that these scores measure whether metadata are machine-readable, not whether the data themselves are correct, so they complement careful documentation and human review rather than replace them.


### F = Findable
 
Findability starts with persistent identifiers, which link people and data indefinitely:
 
- **DOIs (Digital Object Identifiers)** for your dataset or software release. A DOI keeps resolving even if a repository redesigns its website, and it is what lets others cite your data.
- **[ORCID iDs](https://orcid.org)** for the authors. These tell people with common names apart, follow you from institution to institution, and connect your data, code, and papers back to you.

It also starts with choosing a good home for your data. Where you publish affects how easily others can find your work, so we cover how to choose, and compare some water-specific options, in the Water domain repositories section below. Whichever repository you pick, look for one that provides a DOI, descriptive metadata, and long-term preservation.

### A = Accessible
 
Accessible does not always mean open, but the rules for access must be explicit. Someone who lands on your record should be able to tell whether the data are public, embargoed until a certain date, or available on request, and who they would ask. Repositories often support embargoes, which let you get a DOI and publish descriptive metadata now and release the files later. For instance, the EarthChem Library [lets contributors embargo files for up to two years](https://earthchem.org/ecl/policies). Even when the data themselves must be restricted, the metadata should remain findable.
 
The CARE principles come back into play here. If your data relate to Indigenous peoples, lands, or communities, open by default may not be appropriate, and decisions about access belong with those communities. A helpful phrase, used in AGU's own data guidance, is "as open as possible, as closed as necessary." Whatever is restricted should be explained in the record.

### I = Interoperable

Interoperable data can be combined with other data and opened with many different tools, by people and by machines. In practice this means choosing common, non-proprietary formats:
 
- **Tabular data:** CSV or TSV rather than an Excel file with merged cells, color-coded meaning, or notes mixed in with the data.
- **Gridded or multidimensional data:** NetCDF (following [CF conventions](https://cfconventions.org)) or Zarr.
- **Spatial data:** GeoTIFF for rasters, and GeoPackage or GeoJSON for vector data. (If you use a shapefile, keep all of its component files together.)
- **Documentation:** plain text, Markdown, or PDF.

Machine-readable data also means following the tidy data rules: one variable per column, one observation per row, one value per cell, with site and variable descriptions kept in a separate metadata table. Clear, consistent file names help too. `WQ_TotalPhosphorus_Tinney_2022.csv` will mean much more to a stranger than `WQ_TP_TINN_2022.csv`. Finally, state your units, time zones, and coordinate reference systems in the metadata so others can combine your data with theirs.

### R = Reusable

Reusable data are well enough described that someone else can understand and trust them in a new setting. The ingredients are:
 
- **A license.** Without one, others have no clear permission to reuse your work, even if it is public. [CC0 or CC BY 4.0](https://creativecommons.org/licenses/) are common for data, and permissive licenses like MIT, BSD, or Apache 2.0 are common for code ([choosealicense.com](https://choosealicense.com) can help).
- **Rich metadata.** Title, abstract, authors with ORCIDs, geographic and temporal coverage, funding, and related publications.
- **A README.** Describe what each file is and how the files relate, define variables, units, and abbreviations, explain how the data were collected or produced (including known issues and missing-value codes), list the software and versions needed, and say how to cite it and who to contact.
- **Shared vocabularies.** Using community conventions, like CF standard names for NetCDF variables, controlled vocabularies for hydrologic variables, and ISO 8601 dates, means your terms mean the same thing to everyone. Where no standard exists, define your terms explicitly.
- **Provenance.** Record where your inputs came from, what you did to them, and which version of the code produced the outputs.
This is where the idea of "future you" returns. Six months from now, you will be the person who doesn't remember the project context, and if your published package would let you rerun your own analysis, it will probably work for others too. If your data are complex to read (a multi-file NetCDF, a database, or a Zarr store), consider also sharing a short script or notebook that loads them and makes one example plot. It doubles as a test that the package works. Asking a colleague to follow your README without any help from you is a great final check.

## Water domain repositories

A very important decision that members of the water science community have to make is where to publish their data and workflows. Let's dive into what should be considered when deciding on a repository, some possible options, and the strengths and weaknesses of them.

**What should be considered when deciding on a repository?**

Broadly, there are two categories of repositories: generalist and domain-specific.
 
- **Generalist repositories** accept data regardless of data type, format, content, or disciplinary focus. You are probably familiar with some, such as [Zenodo](https://zenodo.org), Dataverse (Harvard Dataverse Repository), or Figshare. Many of them issue DOIs and support solid metadata, and they account for a large share of data and software citations, so a generalist choice is not a lesser one. Zenodo's GitHub integration, for example, makes it a common place to archive a release of your code. The trade-off is that they usually offer fewer field-specific metadata options and often have little or no curation of submissions.
- **Domain-specific repositories** host data related to a specific discipline. They tend to offer metadata fields and conventions tailored to the field, may have stricter guidelines for the publication process, and put your data in front of the community most likely to use it. Examples for environmental science include the [HydroShare](https://www.hydroshare.org) and [EDI (Environmental Data Initiative)](https://edirepository.org) data portal.

Some repositories are also run by universities, funders, or governments. These can be a good home for large datasets, so it is worth asking your librarian.

**Comparison of water-specific repositories**
| | **HydroShare** | **EDI** |
|---|---|---|
| **Run by** | CUAHSI | Environmental Data Initiative |
| **Best suited to** | Hydrologic data, models, code, notebooks, and teaching materials | Environmental data, including ecological and long-term monitoring data |
| **Metadata** | Web forms on the resource page, plus extra metadata for content types like time series, rasters, and NetCDF | Ecological Metadata Language (EML), created with tools like ezEML or EMLassemblyline |
| **Review before publishing** | Light review by CUAHSI staff for minimum metadata | Required automated evaluation of the metadata and its match to the data, with curators available for advice |
| **DOIs** | One DOI per published resource | Every version of a data package gets its own DOI and identifier |
| **Collaboration and compute** | Staged sharing with people and groups, linked JupyterHub environments, and the `hsclient` Python package | Primarily a publication and archive step |
 
In short, HydroShare's strengths are collaboration before publication and keeping data, models, and code together with the means to run them. The trade-off is that published content is locked, so you need to finish everything before publishing. EDI's strengths are its structured, standardized metadata and built-in checks. The trade-off is that you need to prepare that metadata in EML, which is an extra step if you haven't worked with it before. Since HydroShare is the repository this course is built around, we will spend a bit more time there.

**Introduction to HydroShare**
[HydroShare](https://www.hydroshare.org) is a domain-specific repository hosted by CUAHSI that holds diverse types of data, models, scripts, and applications related to water research projects and manuscripts. The unit of content is a **resource**, which can hold data, models, code, notebooks, and teaching materials along with metadata. It includes content types for things like time series, rasters, and NetCDF, which come with extra metadata and viewers.
 
A few features make it particularly useful:
 
- **Sharing happens in stages.** A resource can be private, shared with specific people or groups, discoverable (anyone can find the metadata, but only people with permission can get the files), public, and finally published. This makes it easy to collaborate and prepare before anything is final.
- **Publishing is permanent.** Publishing a resource assigns a DOI and locks the content, title, and authorship. A few things, like the abstract and related resources, can still be edited, but users cannot delete a published resource. Take care to finish your resource and metadata before you publish, and don't publish test resources. HydroShare also has [guidance on its minimum metadata requirements](https://help.hydroshare.org/publishing-in-hydroshare/minimum-metadata-requirements-for-publishing-in-hydroshare/): a descriptive title, an abstract, and at least three keywords including geographic ones. A CUAHSI staff member does a light review before publication.
- **Data and compute sit together.** You can open a resource in a linked JupyterHub environment, and the [`hsclient`](https://github.com/hydroshare/hsclient) Python package lets you create resources, edit metadata, and add files from code.
- **It supports the full citation loop.** HydroShare lets you know what your resource's DOI will be before you permanently publish, so you don't have to wait to cite it. [Its recommended workflow](https://help.hydroshare.org/introduction-to-hydroshare/getting-started/permanently-publish-a-resource/) is to make the resource public when you submit the paper and cite it by URL, switch to the DOI in the final text once the paper is accepted, add the paper's full reference to the resource's related resources once the publisher issues its DOI, and only then finalize and permanently publish. That way the paper and the resource each cite the other by DOI.


### EDI and other options
 
The [Environmental Data Initiative (EDI)](https://edirepository.org) is a repository for environmental data, including data from long-term ecological research sites. Data are published as **data packages**, which pair the data files with metadata written in Ecological Metadata Language (EML), typically created with tools like ezEML or the EMLassemblyline R package. Each version of a package gets its own DOI and identifier. Before a package can be published, it must pass an [automated evaluation](https://edirepository.org/resources/evaluating-a-data-package) that checks the metadata and its match with the data, and EDI's curators are available for advice.
 
Other domain repositories may suit parts of your work. The [EarthChem Library](https://www.earthchem.org), for example, curates geochemical data and works with SESAR, which registers physical samples with persistent IDs called IGSNs. 

## Publishing derivative data

Much of water science involves working with data you didn't collect yourself. You might subset a national dataset, reformat it, aggregate it, or combine it with other sources and then analyze it. Later modules introduce the datasets we will work with in this course, and many of them fall into this category, so these are good questions to keep in mind when we get there.
 
- **Check the license first.** Can the source data be redistributed? A CC BY or public domain source can usually be republished with attribution, but restricted or "all rights reserved" sources may not be. You inherit restrictions, and you can't make them looser.
- **Decide whether to publish the data or the recipe.** If the source is large, stable, open, and versioned, you may only need to publish the code that retrieves and processes it, along with a precise pointer to the source. If the source is short-lived, gets revised, or is hard to access, publishing a snapshot of the subset you actually used is a good idea. Often, doing both is best.
- **Avoid problematic duplication.** Mirroring entire archives is costly, goes stale, and splits citations. Make your derived product clearly distinct from the original in its title and description so that nobody mistakes it for the official dataset.
- **Document provenance in detail.** Note the source, its version, when and how you retrieved it, every processing step you applied, the code (and its version) that did it, and any limitations that result.
- **Give credit.** Cite the source data in your metadata and your paper. Many repositories also let you record relationships, like "derived from" another record, which links your data back to the original so credit flows both ways.
- **Plan for change.** Sources get updated and corrected, so record which version you used, and be ready to publish a new version of your product if the source changes in a meaningful way.

To make this concrete, imagine analyzing output from a national hydrologic model. The agency may only post its latest operational output for a short window, while long historical simulations live in stable public archives. A subset of the short-lived output may disappear from its original location before long, so a snapshot is worth publishing. A subset of a stable archive may only need a pointer and code. The USGS data release [*National Water Model V1.2 Retrospective and Operational Model Run Archive for Selected NWIS Gage Locations*](https://www.usgs.gov/node/273527) is a nice real-world example, where streamflow for about 18,000 gage locations was extracted from public model output and reshaped to be quicker to read.

## Peer review process

Peer review of data and code is less standardized than it is for papers, but there are several options, and they can stand alone from a journal article:
 
- **Repository review.** Some repositories check your submission before publishing. The EarthChem Library's curators review metadata completeness and formatting but do not assess data quality, HydroShare staff do a light review for minimum metadata, and EDI requires its automated evaluation to pass. Others, like Zenodo, rely mostly on you, so a checklist and a colleague are a good idea.
- **Data journals.** A data paper is a short, peer-reviewed article that describes a dataset in detail while the data live in a repository. Examples include [Earth System Science Data](https://essd.copernicus.org), [Scientific Data](https://www.nature.com/sdata/), Data in Brief, and Geoscience Data Journal. ESSD, for example, requires the data to be in a [suitable repository](https://www.earth-system-science-data.net/policies/repository_criteria.html) with a DOI and recommends repositories that provide temporary review links, since data can change during review. This is a good route for valuable datasets that don't accompany a research paper.
- **Software review.** The [Journal of Open Source Software (JOSS)](https://joss.theoj.org) peer reviews research software, and [rOpenSci](https://ropensci.org) and [pyOpenSci](https://www.pyopensci.org) run community review of R and Python packages.
- **Review alongside a paper.** When your data and code support a manuscript, editors and reviewers often need access before publication. Use a private or temporary review link from the repository, ask what your journal prefers, or make the data public early.
- **Informal review.** Ask a colleague to open your data or run your code cold. It is often the quickest way to catch problems, and it ties back to the idea we discussed in the Open Science section of sharing work early and often.

## Further reading

- [Generalist Repository Comparison Chart](https://zenodo.org/records/17315963)
 [Wilkinson et al. (2016), The FAIR Guiding Principles](https://doi.org/10.1038/sdata.2016.18)
- [AGU Data and Software Sharing Guidance](https://data.agu.org/resources/agu-data-software-sharing-guidance)
- [AGU list of useful domain repositories](https://data.agu.org/resources/useful-domain-repositories)
- [Technical Skills for Publishing and Sharing Data and Code (AGU/CUAHSI workshop slides)](https://doi.org/10.5281/zenodo.14270999)
- [HydroShare help documentation](https://help.hydroshare.org) and [hsclient](https://github.com/hydroshare/hsclient)
- [Environmental Data Initiative](https://edirepository.org)
- [EarthChem Library](https://www.earthchem.org)
- [re3data: registry of research data repositories](https://www.re3data.org)
- [DataONE MetaDIG FAIR checks](https://github.com/NCEAS/metadig-checks)
- [CF Conventions](https://cfconventions.org)
- [The Turing Way](https://book.the-turing-way.org)
- [Journal of Open Source Software](https://joss.theoj.org)
