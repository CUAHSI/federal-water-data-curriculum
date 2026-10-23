# Data Management

Imagine you finished an analysis months ago for a paper currently in review, and the associated data products are archived. Then you get a message: one of your monitoring sites had a sensor malfunction, and the provider has corrected the record. How you feel about that message depends almost entirely on how you managed your data, workflows, and documentation along the way.

:::{figure} ../figures/scenario_sensor_malfunction.png
:alt: A chat exchange. A colleague writes that a monitoring site had a sensor malfunction and the data have since been corrected, after the analysis and data release were finished. The reply: "Umm... I think I can figure out which results are impacted," then "Never mind. I can just re-run the whole thing. Might take some time though."
:width: 100%

Your colleague informs you of an unfortunate scenario where you are required to reproduce your analyses that you finished months ago using corrected data.
:::

That is what this page is about. **Data management** is the set of actions you take *during* a research project (not just at the end) so that your methods are credible and you (including your future self), and everyone else, can have confidence in your results. These practices are also what make the data publishing step in the [next lesson](03_data_publishing.md) possible. Tidy data, solid documentation, and complete metadata don't appear at publication time. They get built in as you go.

:::{figure} ../figures/reproducibility_overview.jpg
:alt: Illustration of a winding path from a person holding The Turing Way book, past bubbles labelled "Here are my data", "Here is my code" and "Here are my tools", up to a person on a hilltop presenting "Here are my results".
:width: 100%

An illustration demonstrating the value of documenting at each stage of the data lifecycle for improving research reproducibility ([The Turing Way Community and Scriberia, 2024](https://zenodo.org/records/13882307), CC BY 4.0).
:::

## It's really data *and* information management

When we say "data", we mean more than the numbers in your spreadsheet. Good management covers everything around the data too:

- **The data itself:** raw data (e.g., direct output from a sensor), quality controlled data (e.g., data manually screened for outliers), and derived data (e.g., model outputs).
- **The data about the data ({term}`metadata <Metadata>`):** data collection protocols, spatial and temporal coverage, permissions or sensitivity restrictions, and other information around how the data was generated.
- **The code:** if you wrote scripts, notebooks, or models to clean, analyze, or present the data, that code is a research product too and needs the same care.
- **The methods:** field and lab protocols, standard operating procedures (SOPs), and notes on your approach. These record the steps that don't happen in code, like how a sensor was calibrated or how a sample was collected, and they need the same care too.

The {term}`FAIR principles <FAIR principles>` you saw earlier for data have also been adapted for research software ([Barker, 2022](https://doi.org/10.1038/s41597-022-01710-x)) and more recently for computational workflows ([Wilkinson et al., 2025](https://doi.org/10.1038/s41597-025-04451-9)). Treating your code as something others (including your future self) will need to access, understand, and run is an idea that runs through the rest of this page.

This page covers three things, in order: planning for your data up front with a **data management plan**, understanding what {term}`reproducibility <Reproducibility>` is and how to build toward it, and **three simple approaches** you can start using today to make meaningful strides towards making your research reproducible.

## Data Management Plans

A **{term}`Data Management Plan <Data management plan>` (DMP; or DMSP for Data Management and Sharing Plan)** is a short document that describes what data your project will create or use and how you will handle them from start to finish ([Wong, 2026](https://www.cuahsi.org/uploads/pages/doc/DMP_guide_digital.pdf)). Think of it as a roadmap you write *before* the work starts so that decisions about file formats, storage, documentation, and sharing aren't made in a panic at the end of the project.

Planning ahead also makes reproducibility easier. [Rosenberg et al. (2020)](https://doi.org/10.1061/%28ASCE%29WR.1943-5452.0001215) recommend building reproducibility into a project from the beginning, including budgeting the time and storage it takes.

Many funders now require a DMP or DMSP as part of a proposal. While the specifics differ by agency and program, most ask you to address a similar set of questions outlined in the table below.

| A DMP or DMSP often provides answers to... | What that can look like in a water project |
| --- | --- |
| What data will you create or collect? | Continuous sensor records, grab samples, field notes, model output |
| What formats and standards will you use? | CSV for tabular data, standard units and variable codes (for example, USGS parameter codes), a documented file naming scheme |
| How will you document and describe the data? | A data dictionary, site metadata table, and a {term}`README` |
| Where will data be stored and backed up during the project? | A project folder with a single source of truth, version-controlled code, and a backup plan |
| How will data be shared and preserved? | A data repository such as HydroShare, with a {term}`DOI` |
| Who is responsible for what? | Named people for QA/QC, data release, and updates |
| Are there access, privacy, or licensing considerations? | Sensitive locations, data-sharing agreements, an open license for what *can* be shared |

_A summary table describing key elements of a Data Management Plan (DMP) or Data Management and Sharing Plan (DMSP) and what this can look like in a water project._

A few tips that make DMPs and DMSPs more useful than a box to check:

- **Treat it as a living document.** Projects change. Revisit your plan when your sensors, collaborators, or questions change.
- **Plan for the sharing step early.** Choosing a repository and a license at the *start* of a project means you can organize and document with the end in mind.
- **Use existing tools and resources to help get you started.** There are many existing materials and services dedicated to helping you get your Data Management Plan started. Many university library and research offices offer their own data management plan tools, templates, and one-on-one support.

[![Illustration of the DMP guide, showing key steps and linked resources](../figures/dmp_guide.png)](https://www.cuahsi.org/uploads/pages/doc/DMP_guide_digital.pdf)

_Click the image to open the full DMP guide (PDF). The links to templates, tools, and other resources are clickable in the PDF, but not in the image above._

## Reproducibility techniques

### What do we mean by "reproducible"?

Reproducibility is at the core of how we think science works. We trust a result because the people who produced it can show their work, and others can check it. Peer review and publication both rest on that idea.

The words themselves are used in different ways. The National Academies define reproducibility as obtaining consistent computational results using the same input data, code, methods, and conditions of analysis, and {term}`replicability <Replicability>` as obtaining consistent results across studies that ask the same question, each with its own data ([NASEM, 2019](https://doi.org/10.17226/25303)). The Turing Way uses a two-by-two view: a result is reproducible when the same analysis on the same data gives the same answer, replicable when the same analysis on different data gives qualitatively similar answers, and robust when different analysis workflows on the same data give qualitatively similar answers ([The Turing Way Community, n.d.](https://book.the-turing-way.org/reproducible-research/overview/overview-definitions)). Some fields even use the two terms the opposite way round ([Barba, 2018](https://arxiv.org/abs/1802.03311)).

In this course, we build on these definitions (e.g., [The Turing Way Community, 2025](https://zenodo.org/records/15213042)) and use a broader working definition: reproducibility means that **methods can be easily rebuilt using the same data to recreate results or new data to update an analysis** ([Platt, 2025](https://youtu.be/74GjxHnhlr0)). Rebuildability also depends on something easy to overlook: the people most likely to need to rebuild your work include **your future self**. If you have ever opened a project from six months ago and wondered what `final_v3_USE_THIS_ONE.xlsx` was, this point will hit home.

This understanding of reproducibility also allows for _tiers of reproducibility_, which show that reproducibility is on a continuum rather than an all-or-nothing property:

:::{figure} ../figures/continuum_of_reproducibility.png
:alt: A three-tier pyramid titled Continuum of reproducibility. Bottom tier: document and rebuild your own analysis (documentation, scripts). Middle tier: rebuild, reuse, and debug analyses plus track changes through time (scripted data access, version control, modular code). Top tier: build and collaborate on automated analyses (dependency tracking, automated workflows).
:width: 100%

Continuum of reproducibility, where more time and technical skill is required as you go up each tier ([Platt, 2025](https://youtu.be/74GjxHnhlr0)).
:::

It all starts with documentation and capturing data transformations in scripts. As projects become more data-intensive and our skills grow more technical, the next step is often to track code changes with a version control tool like Git (hosted on platforms like [GitHub](https://github.com/)), saving changes in small, labeled steps called commits, and to break code into reusable functions. Eventually, we may adopt automation and dependency-tracking tools (e.g., [`targets`](https://docs.ropensci.org/targets/) in R or [`Snakemake`](https://snakemake.readthedocs.io/en/stable/) in Python) to build full data pipelines that reliably and efficiently run every step, using a recorded list of the software and versions the workflow needs (an environment).

### Why it's worth it

Reproducibility isn't yet the norm in water research. When [Stagge et al. (2019)](https://doi.org/10.1038/sdata.2019.30) assessed 360 articles published in six hydrology and water resources journals in 2017, they could reproduce results for only 1.6% of the articles they tested. Working reproducibly pays off in several ways (for a similar argument, see [Markowetz, 2015](https://doi.org/10.1186/s13059-015-0850-7)):

- You can redo an analysis quickly when new or corrected data arrive.
- You can be confident that a change made anywhere in the workflow carried through to your results.
- Others can use and build on your methods.
- Papers, reports, and responses to reviewers come together faster because your steps are already recorded.

The barriers to reproducible research are real and non-trivial: added time, extra effort, and potential lack of recognition ([Gomes, 2022](https://doi.org/10.1098/rspb.2022.1113); [Whitaker, 2019](https://doi.org/10.5281/zenodo.2669547)). The [Open Science lesson](01_open_science.md#barriers-to-open-science) covers these and other barriers in more detail. Still, the payoff is worth it: reproducibility is an investment in yourself and your work, and the journey can begin in a meaningful way **today**.

Remember the message about the corrected sensor record at the start of this page? When your steps are captured in scripts, and especially once a pipeline tracks which steps depend on which data, the corrected record flows through to your results without redoing everything by hand. The reply becomes: *"No problem. Easy fix on our end!"*


## Improving data management with three simple approaches

Thankfully, you don't need to consider yourself as a programmer, or to adopt every tool mentioned above, to make real progress on reproducibility. The three approaches described in this section are the foundation of the first tier of the continuum: documentation and well-organized, well-structured files, which come before (and alongside) capturing your steps in scripts. Each one takes some thought and a little time, not advanced technical skill, and each pays off both for you and for anyone who later reuses your work (including your future self). They also build toward the [FAIR principles](01_open_science.md#fair-and-care): organization and naming help make data findable and reusable (F and R), machine-readable files make them interoperable (I), and documentation makes them reusable (R). FAIR is built during the project and cashed in when you publish.

(m01-project-organization)=
### 1. Project organization

Good organization makes it easier for you and others to find files and products later. The goal is to be intentional: even if you land on a different pattern than the one below, spend some time thinking through how your project is structured and how your files are named.

**Define an ordered folder structure.** Think about your project in terms of steps or phases, and create a numbered folder for each so it is clear what order they run in and what happens in each one. Inside each phase folder, use consistent subfolders to keep code, input data, output data, and intermediate files separated.

**Keep raw data untouched.** Store data exactly as you received or collected them, in their own folder, and never edit those files by hand. Make corrections in code, or save corrected copies to a separate folder, so you can always start again from the raw values.

**Converge on file naming conventions.** The exact convention matters less than having one: pick a pattern deliberately, write it down, and use it consistently. A good naming convention lets you understand a file without opening it. One approach is to prefix input and output files with a date (e.g., `YYMMDD`, or the unambiguous ISO 8601 form `YYYY-MM-DD`) so you can track when a file was generated from the filename alone. Matching output file names to the code that produced them (e.g., `regression_model_v1.R` creates `regression_model_v1_output.csv`) makes it easy to trace a result back to its source.

:::{figure} ../figures/project_organization.png
:alt: Left: five numbered phase folders, 01_fetch, 02_clean, 03_model, 04_summarize and 05_visualize. Middle: each phase holds in, out, src and tmp subfolders. Right: output files named with a YYMMDD date prefix, such as 240818_regression_model_v1_output.csv, next to the scripts with matching names, such as regression_model_v1.R.
:width: 100%

An example folder structure organized by numbered project phases (left), where each phase contains subfolders for inputs (`in`), outputs (`out`), code (`src`), and intermediate files (`tmp`) (right). Example file names within the folders using a `YYMMDD` date prefix and matching code and output names, so that each output can be traced back to the script that created it.
:::

**Agree on practices as a team.** When several people work on a project, a few shared habits prevent most mix-ups:

- Keep one source of truth in a central, shared location, and avoid emailing or messaging copies of files around.
- Agree on folder and file naming conventions before the files pile up.
- When people enter data by hand, use controlled fields (drop-down lists or fixed codes) instead of free text, so everyone records the same thing the same way.

### 2. Machine-readable data

Spreadsheet software like Excel is intuitive and keeps your data right at your fingertips. But it also gives you a lot of freedom to customize how your data look, which can make the data difficult for others to publish or reuse. **Machine-readable** data are structured so that code can easily load them into a usable state. Avoid these common spreadsheet habits, which make data hard for code to read:

- **Merged cells:** these break the one-value-per-cell structure that code expects.
- **Color as the only indicator of information:** a color (e.g., blue to flag a data point collected during a storm) is lost as soon as the file is read by code or converted to a plain-text format.
- **Mixing data types in the same column:** combining text and numbers (e.g., `12.4 cfs`) means the column is read as text rather than as numbers.
- **Including metadata in the same sheet as the data:** notes, site descriptions, and other context above or beside your data make it hard to tell where the data actually start.

:::{figure} ../figures/excel_poor_practices.png
:alt: A spreadsheet of daily discharge, temperature and specific conductance for one site. Site notes sit in the top rows above the data, storm days are marked only by blue shading, merged cells label a site visit, and the units are in a row below the data. Labels list the four problems: merged cells, color as an indicator, mixed types in a column, and contextual information mixed with the data.
:width: 100%

An example spreadsheet with several common practices that make data publishing and reuse challenging: merged cells (indicating a site visit), color as the indicator of information (blue means the data point occurred during a storm), units in the same column as the values, and metadata above the data.
:::

A more reusable approach is to store the data in a tidy, rectangular table where every column holds one type of information and every row is one observation. Information that was previously encoded by color gets its own column (e.g., `storm_day` as a TRUE/FALSE value), and the site metadata move to a separate sheet or file. You can still add fill colors with conditional formatting, but the information lives in the data itself and the color is just a bonus. Keeping site metadata separate also means you can add new sites in the future without restructuring anything.

:::{figure} ../figures/excel_recommended_practices.png
:alt: The same data as one tidy table with columns site, Date, streamflow_cfs, stream_temperature_degC, specific_conductance_uSpercm, site_visit and storm_day (TRUE or FALSE), and a separate small table of site metadata with columns site, sensor and date_installed.
:width: 100%

The same data stored in a machine-readable format: one table with columns for `site`, `Date`, `streamflow_cfs`, `stream_temperature_degC`, `specific_conductance_uSpercm`, `site_visit`, and `storm_day` (left), and a separate table of site metadata (right).
:::

Setting up these habits early in a project helps you avoid headaches later when it is time to analyze or publish your data.

### 3. Documentation

Documenting your code and process in detail is wonderful when you share it with others, but it is helpful even if you are the only person who will ever use it. Below is a list of helpful tips for documenting your code:

- **Add helpful in-line comments.** Guide a reader through what your code is doing. Not every line needs a comment, but there should be enough information for someone to understand the code and troubleshoot issues, especially around clever or complex lines.
- **Describe your data with metadata.** Metadata describe the contents of a data file, such as units, definitions, and sources, so that the values can be interpreted correctly without needing to ask you.
- **Include a `README.md` file.** A README is a documentation file that gives an overview of the project, workflow, and code. Think of it as the front page of your project. It can include instructions for running the code, required external packages and their versions, scenarios where your model can be applied, and other notes.
- **Test the usability of your code with a colleague.** Ask a friend or colleague to try running your code and use their feedback to improve your instructions. There is nothing more humbling than watching someone else try to follow the run instructions you thought were perfectly clear, and it is much better to find those issues while you are still in the middle of the project than to be caught by surprises at the very end.

Many of us start with standalone scripts for tasks like data cleaning or modeling. As a project grows, though, you may find yourself juggling dozens of scripts that need to run in a specific order, and keeping track of what to run and when can quickly become overwhelming. That is why it is important to commit to documentation early. Simple steps like these make your work more accessible and reduce the likelihood of confusion months down the line.

These three approaches are the first tier of the continuum. As your projects grow, they are also the foundation for the more advanced tools in the upper tiers, like version control, modular code, and automated pipelines. This module doesn't cover those tools in depth ([The Turing Way](https://book.the-turing-way.org/reproducible-research/reproducible-research) is a good place to start), but the habits here make them much easier to adopt later.


## Now you try it

Apply the three simple approaches to a project someone else left behind.

A colleague who has moved to another job (or a student who has graduated) leaves you their project on how a small watershed's stream responded to a summer storm. Your manager or PI wants the analysis updated with this year's storm. The folder holds:

```text
storm_project/
  data.xlsx
  data_FINAL.xlsx
  final_v3_USE_THIS_ONE.xlsx
  Copy of gage data (2).csv
  rain gauge.csv
  analysis.py
  analysis_new_TRY.py
  fig1.png
  figure for report.png
  notes.docx
```

**Your task:**

1. List what makes this project hard to reproduce.
2. Sketch a cleaner folder structure, using the numbered phases from [project organization](#m01-project-organization).
3. Rename the files so that a stranger could tell what each one is.

**What you should see:** At least four problems: several "final" copies and no single source of truth; raw records that can't be told apart from edited copies; scripts that aren't linked to the outputs they make; vague file names with spaces; and no README.

:::{dropdown} Example answer
```text
storm_response/
  README.md
  01_raw/
    in/240715_stream_gage_discharge_raw.csv      # never edited by hand
    in/240715_rain_gauge_precip_raw.csv
  02_process/
    src/align_rain_and_discharge.py
    out/240720_align_rain_and_discharge_output.csv
  03_figures/
    src/plot_storm_hydrograph.py
    out/240720_plot_storm_hydrograph_output.png
```

Check your version against this list:

- One copy of each file: the three "final" spreadsheets are resolved into one raw file and code that processes it.
- Raw data kept separate and untouched.
- Each output named after the script that made it.
- Dates in file names, and no spaces.
- A README that says what the project is and the order to run the steps in.

Your names and folders don't have to match these. Any convention is fine as long as you choose it deliberately and use it consistently.
:::

*Optional:* sketch the same structure for one of your own projects.

## Further reading

- [Data Management Plan guide (CUAHSI)](https://www.cuahsi.org/uploads/pages/doc/DMP_guide_digital.pdf)
- [DataONE data management training resources](https://www.dataone.org/training/), from DataONE
- [The Turing Way: Guide for Reproducible Research](https://book.the-turing-way.org/reproducible-research/reproducible-research)
- [National Academies (2019), *Reproducibility and Replicability in Science*](https://doi.org/10.17226/25303)
- [Stagge et al. (2019), Assessing data availability and research reproducibility in hydrology and water resources](https://doi.org/10.1038/sdata.2019.30)
- [Coding strategies for building robust and reproducible water data analyses (Platt, 2025, talk recording)](https://youtu.be/74GjxHnhlr0)
