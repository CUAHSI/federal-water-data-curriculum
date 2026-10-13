# Data Management

Imagine you finished an analysis months ago for a paper currently in review, and the associated data products are archived. Then you get a message: one of your monitoring sites had a sensor malfunction, and the provider has corrected the record. How you feel about that message depends almost entirely on how you managed your data, workflows, and documentation along the way.

![](../figures/scenario_sensor_malfunction.png)
_Your colleague informs you of an unfortunate scenario where you are required to reproduce your analyses that you finished months ago using corrected data._

That is what this page is about. **Data management** is the set of actions you take *during* a research project (not just at the end) so that your methods are credible and you (including your future self), and everyone else, can have confidence in your results. These practices are also what make the data publishing step in the next module possible. Tidy data, solid documentation, and complete metadata don't appear at publication time. They get built in as you go.

![](../figures/reproducibility_overview.jpg)
_An illustration demonstrating the value of documenting at each stage of the data lifecycle for improving research reproducibility ([The Turing Way Community and Scriberia, 2024](https://zenodo.org/records/13882307))._

## It's really data *and* information management

When we say "data", we mean more than the numbers in your spreadsheet. Good management covers everything around the data too:

- **The data itself:** raw data (e.g., direct output from a sensor), quality controlled data (e.g., data manually screened for outliers), and derived data (e.g., model outputs).
- **The data about the data (metadata):** data collection protocols, spatial and temporal coverage, permissions or sensitivity restrictions, and other information around how the data was generated.
- **The code:** if you wrote scripts, notebooks, or models to clean, analyze, or present the data, that code is a research product too and needs the same care.

The FAIR principles you saw earlier for data have also been adapted for research software ([Barker, 2022](https://doi.org/10.1038/s41597-022-01710-x)) and more recently for computational workflows ([Wilkinson, 2022](https://doi.org/10.1038/s41597-025-04451-9)). Treating your codebase as something others (including your future self) will need to be able to access, understand, and implement is a big part of how this page is organized. 

This page covers three things, in order: planning for your data up front with a **data management plan**, understanding what **reproducibility** is and how to build toward it, and **three simple approaches** you can start using today to make meaningful strides towards making your research reproducible.

## Data Management Plans

[Introduce what a DMP is and common requirements from funders. See some of our existing DMP content, including Kimmy's figure from Nov 2025]

## Reproducibility techniques

[define: reproducibility is fundamental for science, at the core of how we think of science and the peer review/publication process working; give additional definition of things being "rebuildable" throughout the project. Introduce "future you".]

[barriers (time, publication bias, promotion incentives, skills gap) & benefits (reoding analyses, testing ideas, having confidence in results, writing papers faster, extending methods to others and future you)]

[can be overwhelming to try to move towards total reproducibility all at once (see barriers); tiers of reproducibility figure and progression up to automation; introduce more advanced techniques for consideration: modular code/functions, version control, dependency management (`targets`/Snakemake/GNU Make), containerization, testing]

## Improving data management with three simple approaches

[three simple ways to start: 1. Project organization (ordered folders, naming conventions, single source of truth);  2. Machine-readable / tidy data (avoid merged cells, color-as-data, mixed types);  3. Documentation (README, in-line comments, metadata, "future you" framing)]

## Further reading

[links out to some of the tools/people/orgs referenced along the way]
