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

A **Data Management Plan (DMP; or DMSP for Data Management and Sharing Plan)** is a short document that describes what data your project will create or use and how you will handle them from start to finish ([Wong, 2026](https://www.cuahsi.org/uploads/pages/doc/DMP_guide_digital.pdf)). Think of it as a roadmap you write *before* the work starts so that decisions about file formats, storage, documentation, and sharing aren't made in a panic at the end of the project.

Many funders now require a DMP or DMSP as part of a proposal. While the specifics differ by agency and program, most ask you to address a similar set of questions outlined in the table below.

| A DMP or DMSP often provides answers to... | What that can look like in a water project |
| --- | --- |
| What data will you create or collect? | Continuous sensor records, grab samples, field notes, model output |
| What formats and standards will you use? | CSV for tabular data, community units and parameter codes, a documented file naming scheme |
| How will you document and describe the data? | A data dictionary, site metadata table, and a README |
| Where will data be stored and backed up during the project? | A project folder with a single source of truth, version-controlled code, and a backup plan |
| How will data be shared and preserved? | A data repository such as HydroShare, with a DOI |
| Who is responsible for what? | Named people for QA/QC, data release, and updates |
| Are there access, privacy, or licensing considerations? | Sensitive locations, data-sharing agreements, an open license for what *can* be shared |

_A summary table describing key elements of a Data Management Plan (DMP) or Data Management and Sharing Plan (DMSP) and what this can look like in a water project._

A few tips that make DMPs and DMSPs more useful than a box to check:

- **Treat it as a living document.** Projects change. Revisit your plan when your sensors, collaborators, or questions change.
- **Plan for the sharing step early.** Choosing a repository and a license at the *start* of a project means you can organize and document with the end in mind. [Rosenberg et al. (2020)](https://doi.org/10.1061/(ASCE)WR.1943-5452.0001215) recommend building reproducibility into a project from the beginning, including budgeting the time and storage it takes.
- **Use existing tools and resources to help get you started.** There are many existing materials and services dedicated to helping you get your Data Management Plan started. Many university library and research offices offer their own data management plan tools, templates, and one-on-one support.


## Reproducibility techniques

[define: reproducibility is fundamental for science, at the core of how we think of science and the peer review/publication process working; give additional definition of things being "rebuildable" throughout the project. Introduce "future you".]

[barriers (time, publication bias, promotion incentives, skills gap) & benefits (reoding analyses, testing ideas, having confidence in results, writing papers faster, extending methods to others and future you)]

[can be overwhelming to try to move towards total reproducibility all at once (see barriers); tiers of reproducibility figure and progression up to automation; introduce more advanced techniques for consideration: modular code/functions, version control, dependency management (`targets`/Snakemake/GNU Make), containerization, testing]

## Improving data management with three simple approaches

[three simple ways to start: 1. Project organization (ordered folders, naming conventions, single source of truth);  2. Machine-readable / tidy data (avoid merged cells, color-as-data, mixed types);  3. Documentation (README, in-line comments, metadata, "future you" framing)]

## Further reading

[links out to some of the tools/people/orgs referenced along the way]
