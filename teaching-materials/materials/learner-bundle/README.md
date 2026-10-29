# Reproducible Workflows with Open Water Data: learner notebooks

This resource holds the hands-on notebooks for *Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access*, a CUAHSI course on finding,
retrieving and combining open water data from three Federal agencies: NASA (the SWOT satellite mission), NOAA (the
National Water Model, NWM) and USGS (Water Data for the Nation, WDFN). Each notebook follows one lesson, so a slide
that says "notebook section *Programmatic data downloads*" means the section with that heading.

The slides and the pre- and post-session readings come from the live sessions and are shared in Canvas. This resource
holds only the code you run.

## What's here

```
module-03_federal-water-data-access-retrieval/
    module-03_lesson-01_retrieve-nasa-swot-data.ipynb              student notebook
    module-03_lesson-01_retrieve-nasa-swot-data_solutions.ipynb    with the example answer
    module-03_lesson-01_retrieve-nasa-swot-data_environment.yml    conda environment (m03-swot)
    module-03_lesson-02_retrieve-noaa-nwm-data[.ipynb | _solutions.ipynb | _environment.yml]     (m03-nwm)
    module-03_lesson-03_retrieve-usgs-wdfn-data[.ipynb | _solutions.ipynb | _environment.yml]    (m03-wdfn)
module-04_federal-water-data-synthesis/
    module-04_lesson-02_synthesizing-federal-data-products[.ipynb | _solutions.ipynb | _environment.yml]   (m04-synthesis)
    module-04_lesson-03_additional-federal-water-data[.ipynb | _solutions.ipynb | _environment.yml]        (m04-synthesis)
README.md       this file
```

Modules 1 and 2, and Module 4 lesson 1, have no notebooks: their short examples are on the slides.

| Notebook | Module and lesson | Session | Environment | Time to run (solutions, top to bottom) | Data and accounts |
|---|---|---|---|---|---|
| `module-03_lesson-01_retrieve-nasa-swot-data` | Module 3, lesson 1: Retrieve NASA SWOT data | 3 (Tue Nov 10) | `m03-swot` | about 2 minutes | NASA Earthdata Login. Downloads about 230 MB of SWOT files |
| `module-03_lesson-02_retrieve-noaa-nwm-data` | Module 3, lesson 2: Retrieve NOAA NWM data | 4 (Thu Nov 12) | `m03-nwm` | about 3–4 minutes | No account. Downloads about 270 MB of NWM files and streams roughly 1 GB more from the cloud. The `hydrotools` example needs about 2 GB of memory; skip that cell if your environment has less (nothing later uses it) |
| `module-03_lesson-03_retrieve-usgs-wdfn-data` | Module 3, lesson 3: Retrieve USGS WDFN data | 5 (Tue Nov 17) | `m03-wdfn` | about 1 minute | USGS Water Data API key (optional) |
| `module-04_lesson-02_synthesizing-federal-data-products` | Module 4, lesson 2: Synthesizing Federal data products to build hydrologic confidence | 6 (Thu Nov 19) | `m04-synthesis` | about 1–2 minutes | NASA Earthdata Login; USGS Water Data API key (optional). Downloads about 200 MB of SWOT files |
| `module-04_lesson-03_additional-federal-water-data` | Module 4, lesson 3: Additional Federal water data | 6 (Thu Nov 19) | `m04-synthesis` | about 1 minute | NASA Earthdata Login (search only; nothing large is downloaded) |

## Before you run

- **Run the cells in order.** Later cells reuse variables from earlier ones. If you restart the kernel, run from the
  top again.
- **Times are from a test run on a home internet connection** (October 2026), downloads included. A second run is
  faster, because files already downloaded aren't fetched again.
- **Some results depend on the day you run them**, so your numbers can differ from the ones in the notebook text:
    - **NWM:** the NOAA NWM API keeps only the last few days of forecasts, so the API examples always return the
      newest runs, and the example with NOAA's published kerchunk references (in "Going further") reads yesterday's
      forecast. The April 2025 and February 2026 forecasts come from the archive and don't change.
    - **USGS:** provisional values can still be revised, and lists of monitoring locations and the ends of records
      grow over time. Check `approval_status`.
    - **SWOT:** search results and values can change when NASA reprocesses the data (a new CRID or version), and
      recent overpasses are added as they are processed.
    - **AORC and SoS** (Module 4, lesson 3): the file listings change when new versions are published.
- **Downloads land next to the notebook**, in folders such as `data/` and `hydrotools_data/`, about 700 MB for all
  five notebooks. The four conda environments take a few GB more. Delete what you're done with if your hosted
  environment's storage is limited.
- **On Windows, keep the folder path short** (for example `C:\fwdc\`). SWOT file names are about 100 characters
  long, and Windows refuses paths longer than 260 characters, so a download into a deeply nested folder fails with
  `FileNotFoundError: [WinError 3]`.

## Open the notebooks

**In a hosted Jupyter environment (for example, from this HydroShare resource's "Open with" menu).** Each notebook
needs its own conda environment, made from the `_environment.yml` file next to it. Open a terminal in Jupyter
(File → New → Terminal) and `cd` to the folder that holds the notebook: the Jupyter file browser shows its path. Then
run, for the SWOT notebook:

```bash
conda env create -f module-03_lesson-01_retrieve-nasa-swot-data_environment.yml
conda run -n m03-swot python -m ipykernel install --user --name m03-swot --display-name "Python (m03-swot)"
```

Then open the notebook and choose the **Python (m03-swot)** kernel (Kernel → Change kernel). Do the same for the
other Module 3 notebooks with their own environment files and names (`m03-nwm`, `m03-wdfn`). The two Module 4
notebooks share one environment, `m04-synthesis`: create it once, from either Module 4 environment file (creating it
a second time fails with "prefix already exists"). Creating an environment takes a few minutes and only needs doing
once. If you open a notebook with the wrong kernel, imports such as `import earthaccess` fail. If your hosted
environment doesn't keep conda environments between sessions and a kernel disappears, run the two commands again.

**On your own computer.** Install [Miniforge](https://github.com/conda-forge/miniforge) (or another conda), download
this resource, and run the same two commands in a terminal, then open the notebooks in JupyterLab or VS Code with the
matching kernel.

The environment files pin the Python version but let most packages update to their latest release, so you may get
newer versions than the ones we tested. When you use these patterns in your own research,
record what you ran with `conda env export > environment-lock.yml` and keep it with your results.

## Accounts and credentials

Never type a password or key into a code cell: notebooks are saved with their cells, and are easy to share by
accident. Each notebook's **Credentials** section, near the top, shows the safe way to sign in.

- **NASA Earthdata Login** (SWOT notebooks): a free account from [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov).
  `earthaccess.login()` asks for your username and password when you run it. To save them for later sessions, run
  `earthaccess.login(persist=True)` once; it writes them, as plain text, to a `.netrc` file in your home folder (fine
  for your own account, not on a shared one). On your own computer
  you can instead set the `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` environment variables. See the
  [`earthaccess` authentication how-to](https://earthaccess.readthedocs.io/en/latest/user/howto/authenticate/).
- **USGS Water Data API key** (USGS notebooks; optional): request one at the
  [USGS Water Data API signup page](https://api.waterdata.usgs.gov/signup/). It raises your hourly rate limit; everything
  runs without it, but over the limit requests fail with HTTP `429 Too Many Requests` until the hour is up. `dataretrieval` reads it from the `API_USGS_PAT` environment
  variable. In a hosted environment, uncomment the two lines in the notebook's Credentials cell and paste the key when
  asked; it is kept only until the kernel stops. On your own computer, set `API_USGS_PAT` as an environment variable
  before you start Jupyter.
- **NOAA NWM**: no account or key.

## Student and solutions notebooks

Each Module 3 lesson ends with a **Now you try it** task that repeats the main steps on a second river, the Willamette River at
Salem, Oregon. In the student notebook the task's code cell is a starter: lines you shouldn't have to retype are
filled in, and the parts that practise the lesson's skill are left as `...` with a `# TODO:` hint. The cell
raises an error until every `...` is filled in. Make your changes in that cell rather than in the earlier ones. Work through the
student notebook, then compare your answer with the `_solutions` notebook, which has a complete example answer. The
task text says what you should get.

The NWM and USGS notebooks end with an optional **Going further** section, after the task: an extra example the
session doesn't cover. It doesn't use any earlier results, only the packages imported in the first code cells. In the student notebook,
the unfinished task cell stops a "Run All", so run the Going further cells one by one.

The Module 4 lessons have no "Now you try it" task, so their student and solutions notebooks are the same. The Module
4 lesson 2 notebook ends with a checklist for adapting the case study to another river, a good exercise of its own.

## License

The notebooks are released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html)
(GPL-3.0). They adapt code from the CUAHSI notebooks repository
([github.com/CUAHSI/notebooks](https://github.com/CUAHSI/notebooks), GPL-3.0) and from agency tutorials; each
notebook credits its sources in its "Attribution and license" section and lists them under "Further reading".

## How to cite

Platt, L., Wong, K., Vaarre-Lamoureux, K., and Bogan, A. *Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access* (version
pilot-2026-11) [Learning material (online course)]. CUAHSI. GPL-3.0.

When you publish results made with these notebooks, also cite the datasets you used. The Module 3 notebooks' "Understanding
what you downloaded" sections and the Module 4 lesson 2 notebook's "Saving what you derived" section say how: the SWOT
collection DOIs, the NWM model version, configuration and access date, and the USGS Water Data for the Nation DOI
([10.5066/F7P55KJN](https://doi.org/10.5066/F7P55KJN)).

## Acknowledgements

*Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access* was developed by CUAHSI with contributions from colleagues at NOAA, USGS and
NASA: Lindsay Platt, Kimberlee Wong, Kaysa Vaarre-Lamoureux, Abner Bogan, Julia Masterman, Irene Garousi-Nejad, Tony
Castronova and Danielle Tijerina-Kreuzer (CUAHSI); Jason Regina (NOAA); Elise Hinman, Cee Nell and Michael Mahoney
(USGS); and NASA staff. Contributions from federal agency staff are acknowledged with thanks. Acknowledgment does not imply endorsement
of this course by NASA, NOAA or USGS.

This material is based upon work supported by the U.S. National Science Foundation under
[Award No. 2535162](https://www.nsf.gov/awardsearch/show-award?AWD_ID=2535162). Any opinions, findings, and
conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect
the views of the National Science Foundation.

Generative AI tools (Anthropic's Claude) were used to help draft lesson text, code examples, figures and the teaching
materials, including these notebooks, from outlines, existing CUAHSI notebooks and contributors' materials.
Contributors reviewed, edited and tested all content, ran every code example, and are responsible for the course as
published.
