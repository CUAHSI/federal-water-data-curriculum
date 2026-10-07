---
name: port-notebook
description: Repurpose a source Jupyter notebook (local path or URL) into content for a MyST lesson page in this course — extract its data discovery/download pattern, rewrite in the course voice, and credit it. Use whenever a ROADMAP task names a source notebook.
---

# Port a notebook into a lesson page

## 1. Locate and inventory
- Get the notebook from the "Source material" table in `ROADMAP.md`. For CUAHSI/notebooks:
  `git clone --depth 1 -b develop https://github.com/CUAHSI/notebooks.git <scratch-dir>/cuahsi-notebooks`
  (outside this repo — never commit source notebooks).
- Convert for reading: `jupyter nbconvert --to markdown <nb> --output-dir /tmp/nb-port`
  (or read the JSON with NotebookEdit/Read).
- Record: title, author/org, URL, license, last-updated date, packages + versions imported.
- CUAHSI/notebooks is GPL-3.0, the same as this course repo, so cells may be adapted directly.
  For any other source, check its license; stop and ask if it doesn't allow adaptation or is missing.

## 2. Map it to the target page
Write a short mapping before editing (share it with Lindsay if the task is large):

| Notebook cells | Target page section | Keep / adapt / drop | Why |
|---|---|---|---|

Rules of thumb:
- **Keep**: authentication pattern, discovery query, download call, the first look at the result.
- **Adapt**: site/region/date choices to match the course examples (check what the page already
  uses — e.g. Suffolk County MA for NWIS, CUAHSI office COMID for NWM, Skagit River Dec 2025 / USGS 12200500 for Module 04).
- **Drop**: long plotting/analysis cells, notebook-specific setup, cells duplicating existing page content.
- Prefer the course's tool choices (see CLAUDE.md). The USGS notebook uses legacy `nwis` — port it to
  `waterdata`. The NWM notebook uses the CIROH NWM API, which the course does not recommend — borrow its
  narrative and plots, but use the no-key access route chosen in ROADMAP P1.3 and the Module 3 access-route guidance.

## 3. Write
- Fill the matching section of the page, resolving the relevant `[TODO]` placeholders.
- Each code block gets 1–3 sentences before it (what/why) and, where useful, a sentence after
  describing the output (columns, units, quality flags, gotchas such as rate limits or pagination).
- Pin nothing in prose that will go stale fast (exact result counts) unless labelled "at time of writing".
- Add an attribution line in **Further reading**:
  `Adapted from [<title>](<url>) by <authors>, CUAHSI notebooks (GPL-3.0).`
  Credit agency docs/figures where they're used, too, and add every source to the L1 credits list.
- If you add a page, add it to `myst.yml` `toc`.

## 4. Verify
- `myst build --html` passes with no new warnings.
- Run each changed code block in a scratch script in the matching `environments/*.yml` env
  (`conda run -n <env> python ...`). If it can't run (missing credential, service down), mark it
  "reviewed, not executed" with the reason. Never put credentials in files.
- `rg "TODO" <page>` — list what remains.

## 5. Report
Summarize: sections changed, notebook cells used, executed vs. reviewed code, remaining TODOs,
questions. Then follow the approval steps in CLAUDE.md before committing.
