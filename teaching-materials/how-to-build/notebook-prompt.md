# Prompts: build or update one notebook

Each lesson with code has one notebook, the place learners run the code. They get it on HydroShare, with only the
session's slides to go with it: no website, no repo, no README. The notebook and its `_environment.yml` are built
locally and **never committed**, like the decks.

| Session | Notebook (`materials/notebooks/<module folder>/`) | Lesson page | Environment |
|---|---|---|---|
| 3 | `module-03_lesson-01_retrieve-nasa-swot-data` | `03-federal-water-data-access-retrieval/01_access_nasa_swot.md` | `m03-swot` |
| 4 | `module-03_lesson-02_retrieve-noaa-nwm-data` | `03-federal-water-data-access-retrieval/02_access_noaa_nwm.md` | `m03-nwm` |
| 5 | `module-03_lesson-03_retrieve-usgs-wdfn-data` | `03-federal-water-data-access-retrieval/03_access_usgs_wdfn.md` | `m03-wdfn` |
| 6 | `module-04_lesson-02_synthesizing-federal-data-products` | `04-federal-water-data-synthesis/02_synthesize_river_data.md` | `m04-synthesis` |
| 6 | `module-04_lesson-03_additional-federal-water-data` | `04-federal-water-data-synthesis/03_additional_data.md` | `m04-synthesis` |

The module folders are `module-03_federal-water-data-access-retrieval` and `module-04_federal-water-data-synthesis`.
Modules 1 and 2, and Module 4 lesson 1, have no notebooks.

**Build the session's deck first.** The deck explains the concepts and tells learners when to switch to the
notebook. The notebook is written from the deck, so it doesn't repeat it. If the deck changes, update the notebook.

This file holds two prompts and the lesson notes both use. Use **Build** for a notebook that doesn't exist yet,
and **Update** to bring one up to date. Copy everything between the lines of the one you need into Claude, with
`{N}` (the session) and `{NOTEBOOK}` (the file stem from the table) filled in, and attach the "Lesson notes"
section too. In Claude Code, `/build-notebooks N` and `/build-notebooks N update` do the same.

## Build

---

You are writing the notebook **{NOTEBOOK}** for **Session {N}** of *Reproducible Workflows with Open Water Data:
NASA, NOAA, USGS River Data Access*, a CUAHSI course for researchers and graduate students who know some Python but
are new to federal water data APIs. Learners have the session's slides and this notebook, nothing else. The
slides carry the explanations. The notebook is where learners run the code, during the session's live-coding
stretches and afterwards on their own.

### Inputs

1. **The session's deck:** the `.pptx` named in the topic list's header, in `teaching-materials/materials/slides/`.
   If it doesn't exist, stop: build the deck first. Read every slide's title, text and speaker notes, and its
   Comments property (`Built from <commit> …`).
2. **Topic list:** `teaching-materials/how-to-build/topics/session-0{N}.md`.
3. **Lesson page:** the learner copy of the page (made with `teaching-materials/how-to-build/tools/prepare_learner_copy.py`).
   It is the only source of content.
4. **Environment:** `environments/<env>.yml` (the table above).
5. **Lesson notes:** the section at the end of this file. It gives the notebook's learning goal, its credentials,
   and fixes the notebook needs until the lesson is corrected.

### Rules

**Content**
- Use only what the lesson page and the lesson notes say. Don't invent claims, numbers, code or links. Copy code
  cells unchanged, except for the fixes in the lesson notes.
- The course is called **Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access**. Agency
  order NASA → NOAA → USGS; "WDFN", not "NWIS", except when contrasting with the legacy services.
- No links into the course (other pages, the glossary, the repo). Where the lesson points to another page,
  name the slide or reading that covers it in plain text, or drop the pointer. External links are fine. Nothing
  from `TODO (dev team)` or `Partner review` callouts (the learner copy has already removed them).

**What goes in, and how much text**
- **Sections:** the lesson sections whose topic-list rows include `notebook`, in lesson order. Each heading has the
  same text as the lesson heading, because the slides name notebook sections by their headings. Leave out
  sections whose rows are only `deck`, `reading`, `how-to` or `cut`. If a later cell needs code from one of them
  (an import, a variable), keep that code cell under the nearest included heading, with one sentence saying why.
- **Don't repeat the deck.** If a slide explains an idea (what a COMID is, why kerchunk avoids downloads, what a
  quality flag means), the notebook doesn't explain it again. Point to the slide by its title in a few words,
  e.g. "(slides: *Finding COMIDs with the NLDI*)".
- **Do keep what the deck doesn't have.** The slides show code but don't run it. So for each code cell keep, in
  1–3 sentences, what it does, what you'd change for your own river, and the lesson's "what you should see"
  description of the output (numbers, columns, units). Keep a short definition only when no slide gives it.
- **Text that points at a figure on the page** ("If your plot looks like this…") describes what the plot should
  show instead, from the lesson's text, since the notebook makes the figure itself.

**Following the deck's hand-offs**
- Each "Live coding" slide names the sections to run. At the first of those sections, add a Markdown cell:
  "**Live coding {k}: <the slide's title>.** Run from here to the end of *<last section>*, then go back to the
  slides." After the last of those sections, add "**Back to the slides.**" Use the deck, not the topic list, for
  which sections each stretch covers. If they disagree, follow the deck and report it.
- Sections with code outside a live-coding stretch stay in lesson order with no marker. They're for working
  through after the session.

**Notebook structure**
1. **Title cell:** the lesson title as `#`, the course name, the session number and date, the learning goal
   (lesson notes), and a 2–3 sentence introduction from the lesson's opening paragraph. End with one sentence
   saying how to use it: the slides explain, this notebook is for running the code, run the cells in order.
2. **Before you start** (`##`), short, because the HydroShare "How to" guide walks through setup:
    - the conda environment (`<env>`), the `<stem>_environment.yml` file next to the notebook, and the two
      commands to create it and its kernel, run in a terminal in the notebook's folder, then choosing the
      **Python (<env>)** kernel (the two Module 4 notebooks share `m04-synthesis`: create it once):
      ```bash
      conda env create -f <stem>_environment.yml
      conda run -n <env> python -m ipykernel install --user --name <env> --display-name "Python (<env>)"
      ```
    - downloads (size, where they land) and run time, from the lesson notes;
    - results that depend on the day you run them, from the lesson notes.
3. **Credentials** (`##`): the standard cells in the lesson notes for this notebook's credentials.
4. **The lesson sections**, with the live-coding markers.
5. **Now you try it** (`##`), if the lesson has one:
    - the lesson's task text, and one sentence: "Make your changes in the code cell below. It changes shared
      variables, such as the place and dates, so to go back to the earlier examples, run the notebook again
      from the top."
    - **a starter code cell for each example-answer code block.** Start from the example answer. Keep the lines
      learners shouldn't have to retype (imports, plotting, printing). Replace the values and calls that
      practise the lesson's skill with `...`, each with a `# TODO:` hint that says what goes there (not the
      answer). Running the unfilled starter must fail quickly with an error, never download or plot something
      wrong.
    - **the example answer, collapsed**, in a Markdown cell right after each starter:

      ````markdown
      <details>
      <summary><b>Show the example answer</b></summary>

      ```python
      <the lesson's example-answer code, unchanged>
      ```

      </details>
      ````
    - then the lesson's "what you should see" text for the task.
6. **Going further** (`##`), if the topic list has rows whose "Where" is only `notebook`: one `###` section per
   row, from the lesson section it names. Start with "*Optional.* This goes beyond the session. It runs on its own
   (it doesn't use earlier results). "Run All" stops at the unfinished task above, so run these cells one at a
   time (Shift+Enter)." Each example must run on its own: repeat any import or function it needs. Rows with no
   code in the lesson can't be practised: leave them out and report them.
7. **Further reading** (`##`): the lesson's external links.
8. **About this notebook** (`##`), at the end:
    - license: "Released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html)
      (GPL-3.0). You may use, change and share it under the same license.";
    - the sources it adapts, from the lesson's "Adapted from …" lines;
    - how to cite the course, from `CITATION.cff` (authors, title, version, "[Learning material (online
      course)]. CUAHSI. GPL-3.0."), and the lesson's guidance on citing the datasets used;
    - acknowledgements, from `acknowledgements.md`, in two or three sentences: who developed it, the NSF award
      and disclaimer, and the use of generative AI tools.

**Files**
- `teaching-materials/materials/notebooks/<module folder>/{NOTEBOOK}.ipynb` (git-ignored: never committed).
  nbformat 4.4, outputs cleared, metadata only `kernelspec` (`name` and `display_name` "Python (<env>)") and
  `"fwdc": {"built_from": "<short commit the lesson was read from>", "deck": "<deck file name>",
  "deck_built_from": "<the deck's Comments>"}`. Write it with `nbformat` from a scratch script.
- `{NOTEBOOK}_environment.yml` next to it: `environments/<env>.yml` from its `name:` line on, with a header of
  comment lines: the notebook it's for, the course name, and the two setup commands. Keep the `name:` and the
  packages unchanged; no paths into the repo.

### Steps

1. **Map the deck (no output yet).** List the slides in order with their titles. Mark each "Live coding" slide
   and the notebook sections it names, the "Now you try it" slide, and the slides that explain each `deck +
   notebook` topic.
2. **Plan and stop.** A table: notebook section (heading), topic-list row, live-coding stretch, code cells, and
   the text you'll keep (one line). Below it, list the lesson text you're leaving out because a slide covers it
   (with the slide title), and the starters you'll write (what each blanks). Show me the plan and wait for my
   go-ahead.
3. **Write** the notebook and the environment file.
4. **Test** in the lesson's environment, with credentials set (`teaching-materials/how-to-build/guide.md`,
   "Before you rebuild"):
    - Run the notebook with papermill. It should stop at the first starter with an error, and every cell
      before it should succeed.
    - Run a test copy with each starter replaced by its example answer, top to bottom, Going further included.
    - Check the outputs against the "what you should see" text, and look at every figure.
    - Record the run time and any result that depends on the day you ran it.
5. **Review.** Run the `learner-reviewer` on the notebook, telling it the learner has the deck (give it your deck
   map). Fix every Blocker.
6. **Report:** the notebook's sections and live-coding stretches; the lesson text left out and the slides that
   cover it; the starters; test results with run times and package versions; the reviewer's summary line; and
   any lesson problem the notebook had to work around, as a suggested lesson edit.

---

## Update

---

You are updating the notebook **{NOTEBOOK}** for **Session {N}** of *Reproducible Workflows with Open Water Data:
NASA, NOAA, USGS River Data Access*. It already exists and may have hand edits. Change only what needs changing.

### Inputs

1. **The notebook to update:** `{NOTEBOOK}.ipynb` in `teaching-materials/how-to-build/to-update/` if there is one,
   otherwise the one in `teaching-materials/materials/notebooks/`. Its `fwdc` metadata says which commit and deck it
   was built from.
2. The same deck, topic list, lesson page, environment and lesson notes as for a build.

### Rules

The build rules apply to everything you add or change. A cell whose metadata `tags` include `keep` is never
changed, moved or removed. Keep a starter as it is unless its example answer changed; then rewrite the starter
to match the new answer.

### Steps

1. **Inventory and plan, then stop.** List what changed since the notebook was built: `git diff <built_from> --
   <lesson page> <topic list> environments/<env>.yml`, and, if the deck's Comments differ from the notebook's
   `deck_built_from`, the slide titles and live-coding slides that changed. For each notebook section decide
   **keep**, **update** (say what changed), **move**, **remove** or **add**. Show me the plan and wait for my
   go-ahead.
2. **Make the changes**, keeping the notebook's wording wherever the lesson and deck haven't changed. Update the
   `fwdc` metadata and, if the environment changed, the environment file. Save to
   `teaching-materials/materials/notebooks/`; never overwrite the file in `how-to-build/to-update/`.
3. **Test** as for a build: at least the sections you changed and the task, and the whole notebook if the
   environment changed.
4. **Report** a change log (one line per section: kept, updated, added, removed or moved, and why) and the test
   results.

---

## Lesson notes

What each notebook needs that the lesson page doesn't give it directly. When the lesson is fixed, delete the fix
here.

### Standard credentials cells

Use the cells for the credentials each notebook lists, Earthdata first. A notebook with none gets only the "No
account" text. Never put a password or key in a cell.

**NASA Earthdata Login** (Markdown):
> **NASA Earthdata Login.** Downloading SWOT files needs a free account from
> [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov). `earthaccess.login()` looks for your username and
> password in the `EARTHDATA_USERNAME` and `EARTHDATA_PASSWORD` environment variables, then in a `~/.netrc` file,
> and otherwise asks you for them. In a hosted Jupyter environment, the simplest route is to let it ask: run the
> cell and type your details into the boxes it shows. To avoid typing them every session, run
> `earthaccess.login(persist=True)` once, which saves them to `~/.netrc` in your home folder. Never type your
> password into a code cell: it would be saved in the notebook. See the
> [`earthaccess` authentication how-to](https://earthaccess.readthedocs.io/en/latest/user/howto/authenticate/).

```python
import earthaccess

# Uses EARTHDATA_USERNAME/EARTHDATA_PASSWORD or ~/.netrc if set; otherwise asks you to type them
auth = earthaccess.login()
print("Logged in to NASA Earthdata:", auth.authenticated)
```

**USGS Water Data API key** (Markdown):
> **USGS Water Data API key (optional).** The USGS Water Data APIs work without a key, but a key raises your rate
> limit; over the limit, requests fail with HTTP `429 Too Many Requests` until the hour is up. Request one at the
> [USGS Water Data API signup page](https://api.waterdata.usgs.gov/signup/). `dataretrieval` reads it from the
> `API_USGS_PAT` environment variable and sends it for you. If your environment doesn't set that variable,
> uncomment the two lines below and paste your key when asked: it is kept only for this session and isn't saved
> in the notebook. Don't print the key or write it into a cell.

```python
import os

# Optional: set the key for this session only (it isn't saved in the notebook)
# from getpass import getpass
# os.environ["API_USGS_PAT"] = getpass("USGS API key: ")
print("API_USGS_PAT is set:", bool(os.getenv("API_USGS_PAT")))
```

**No account** (Markdown, NWM): "No account or key is needed for anything in this notebook: the NLDI, the NOAA
NWM API and the NWM archives on Google Cloud and AWS are all public."

### All notebooks

- Leave out the lesson's steps for creating the environment and logging in, and their code cells (`auth =
  earthaccess.login()`, the `API_USGS_PAT` check): "Before you start" and the credentials cells replace them.
- Leave out "For helpful context, refer back to the example rivers we covered in the overview." from the task.
- Environment file: change "noted on the page" to "noted in the notebook", and "# optional: run the lesson in
  Jupyter" to "# needed to run the notebook in Jupyter".
- On Windows, SWOT downloads fail in deeply nested folders (file names are about 100 characters and Windows
  refuses paths over 260), with `FileNotFoundError: [WinError 3]`. SWOT notebooks say so in "Before you start":
  keep the folder path short (e.g. `C:\fwdc\`). For tests, run papermill with `--cwd` in a short folder.

### `module-03_lesson-01_retrieve-nasa-swot-data` (Session 3)

- **Learning goal:** Retrieve NASA SWOT data for a location of interest, describe what comes back using the
  course's shared concepts, and choose an access pattern that scales with your question.
- **Credentials:** Earthdata Login.
- **Downloads and time:** about 230 MB of SWOT files, into `data/`; about 2 minutes.
- **Depends on the day:** search results and values can change when NASA reprocesses the data (a new CRID or
  version), and recent overpasses are added as they're processed.
- **Fixes:** "You can also use SWOTviz, a CUAHSI" → link it: `[SWOTviz](https://swotviz.cuahsi.io/)`. "The
  location map at the top of this page was drawn from this one file:" → "This cell draws a location map from
  this one file:".

### `module-03_lesson-02_retrieve-noaa-nwm-data` (Session 4)

- **Learning goal:** as lesson 1, with "NOAA NWM data".
- **Credentials:** none.
- **Downloads and time:** about 270 MB of NWM files (into `hydrotools_data/`) and about 1 GB more streamed from
  the cloud; about 3–4 minutes. The `hydrotools` cell needs about 2 GB of memory: say it's optional (nothing
  later uses its result) and can be skipped in a smaller environment.
- **Depends on the day:** the NOAA NWM API keeps only the last few days of forecasts, so it always returns the
  newest runs, and NOAA's published references (Going further) read yesterday's run. The April 2025 and
  February 2026 forecasts come from the archive and don't change.
- **`hydrotools` in Jupyter:** importing `hydrotools.nwm_client` starts its own event loop, which fails inside
  the notebook's loop, and the lesson's fix (`nest_asyncio`) fails too with Python 3.14 and current `aiohttp`
  (tested 2026-10-26). Start the `hydrotools` cell with these lines, and replace the lesson's `nest_asyncio`
  advice (in that section and in its troubleshooting list) with "the first lines of the cell handle Jupyter's
  event loop; if you still see the error, restart the kernel and run the notebook again from the top":
  ```python
  # Optional cell: it needs about 2 GB of memory, and nothing later uses its result.
  # In Jupyter, importing hydrotools.nwm_client starts its own event loop, which fails inside the
  # notebook's running loop, so import it once in a separate thread first (plain scripts don't need this).
  import importlib
  from concurrent.futures import ThreadPoolExecutor
  with ThreadPoolExecutor(1) as pool:
      pool.submit(importlib.import_module, "hydrotools.nwm_client.NWMFileClient").result()
  ```
- **Kerchunk:** keep the sentences that say what kerchunk references are, even if they're on a slide too: the
  code doesn't make sense without them.
- **Task "what you should see":** the task builds its own references from the archive, so "18 published
  reference files for 25 February" → "18 hourly values from your references for 25 February". Drop "(the API's
  `name` field is blank for this reach)". The plot check: "If your plot shows the 3 April medium-range run peaking
  near 13,900 m³/s on 8 April, and each short-range run starting near 15,000–18,000 m³/s and falling quickly, your
  code is right"; drop "(we've asked NOAA why the short-range runs drop so fast; see the note below)".
- **Going further (row 20):** the lesson's "Example: use NOAA's published references for a recent run" moves
  here, from that paragraph to the next heading. Where the lesson says it uses `open_refs` from the previous
  example, it gets its own cell that defines it again (with `import xarray as xr`), the same function as in
  "Kerchunk references". In the "Kerchunk references" section, the pointer to this example becomes "Going
  further at the end of this notebook has an example". End with: "**What you should see:** 18 reference files;
  `time` 18 and `feature_id` 2,776,734; and the first three hourly streamflow values (m³/s) at Louisville for
  yesterday's 12Z run (UTC), which change from day to day. Recent runs can be a newer model version than the
  April 2025 archive: check `ds_recent.attrs["NWM_version_number"]` and cite the version you used."

### `module-03_lesson-03_retrieve-usgs-wdfn-data` (Session 5)

- **Learning goal:** as lesson 1, with "USGS WDFN data".
- **Credentials:** USGS Water Data API key.
- **Downloads and time:** small; about 1 minute.
- **Depends on the day:** provisional values can still be revised, and lists of monitoring locations and the
  ends of records grow. Check `approval_status`.
- **Fixes:** the task's "Repeat the main steps for accessing NWM data" → "… USGS WDFN data".
- **Going further, row 23 (counting qualifiers):** the lesson gives the count only as inline code. Replace its
  "(count them with `daily_record[...]...sum()`)" with "("Going further" at the end of this notebook counts
  them)", and add:
  > This downloads the whole daily record for the Ohio River at Louisville again, as in the "Temporal scaling"
  > example (about 6 seconds), and counts its qualifiers:
  ```python
  # the whole daily record, as in "Temporal scaling" (the site is set here, since the task changed `site`)
  daily_record, md = waterdata.get_daily(
      monitoring_location_id="USGS-03294500",
      parameter_code="00060",
      statistic_id="00003",
  )
  print(daily_record["qualifier"].astype(str).str.contains("ESTIMATED").sum(), "days marked [ESTIMATED]")
  daily_record["qualifier"].astype(str).value_counts()
  ```
  > **What you should see:** about 1,100 days marked `[ESTIMATED]`, then one row per combination of qualifiers,
  > most often `['ESTIMATED']` alone. Each day's qualifiers are a list, shown here as text, and days with no
  > qualifier are left out of the counts.
- **Row 22 (legacy `nwis`)** has no code in the lesson: leave it out and report it.

### `module-04_lesson-02_synthesizing-federal-data-products` (Session 6)

- **Learning goal:** Retrieve and line up USGS observations, NWM forecasts and SWOT measurements for one flood,
  accounting for differences in location identifiers, units, vertical reference, time zone and sampling, and
  explain what each product can and cannot show.
- **Credentials:** Earthdata Login, USGS Water Data API key.
- **Downloads and time:** about 200 MB of SWOT files; about 1–2 minutes.
- **No "Now you try it":** the lesson ends with a checklist for adapting the case study to another river; keep
  it as the closing exercise.
- **Fixes:** "(NLDI)](…) (NLDI)" → drop the repeated "(NLDI)". "(`Provisional` or `Approved`; see approval
  status)" → "(`Provisional` or `Approved`)". Drop " (see UTM zone)". "Search the page's code" → "Search this
  notebook's code". Leave out the paragraphs on the pinned environment, on needing the Module 3 credentials, and
  "The sections below walk through the data you would collect".

### `module-04_lesson-03_additional-federal-water-data` (Session 6)

- **Learning goal:** Take a first step with related Federal water data products (SWOT discharge from the SWORD
  of Science and NOAA AORC precipitation) using the same discover-before-download habits as Module 3.
- **Credentials:** Earthdata Login (search only; nothing large is downloaded).
- **Time:** about 1 minute.
- **Depends on the day:** the AORC and SoS file listings change when new versions are published.
- **Fixes:** the USDA and USACE section is a placeholder: leave it out, along with its line in the lesson's
  list of sections and "and a placeholder for USDA and USACE data".
