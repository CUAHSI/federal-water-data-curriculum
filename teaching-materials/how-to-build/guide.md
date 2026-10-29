# Teaching materials: guide

Everything needed to build and update the materials that *run* *Reproducible Workflows with Open Water Data:
NASA, NOAA, USGS River Data Access*: session decks, notebooks, module readings, quizzes and the instructor guide.
They're made from the lesson pages (`0*/`), which stay the single source of truth: to fix content, edit the
lesson, then update the material. `teaching-materials/` isn't part of the website (`myst.yml` excludes it).

Pilot learners can't open the website or this repo. They get the decks, readings and quizzes through Canvas and
the notebooks through HydroShare, so each has to stand on its own.

| Output | Its job | Where (`teaching-materials/materials/`) |
|---|---|---|
| **Deck** | The important concepts and points, presented live | `slides/`, one `.pptx` per session; shared through Canvas |
| **Notebook** | Practising the code, during the session's live coding and after | `notebooks/`, one `.ipynb` and `_environment.yml` per lesson with code; shared through HydroShare |
| **Reading** | Extra detail and nuance that's useful but not needed in the session (Modules 2–4 only, at most one per module) | `readings/`, a Word document exported to PDF; the PDF is shared through Canvas |
| **Quiz** | A formative check per module, aligned to its objectives | `quizzes/`, `text2qti` text, QTI zip and answer key; imported into Canvas |
| **Instructor guide** | Prep for a new or substitute instructor (not for learners) | `instructor-guide/` |

Decks, notebooks, readings and quizzes are **built locally and never committed** (git-ignored). Each records the
commit it was built from in the file itself, so an update can see what changed in the lessons since. The
instructor guide is the one committed output, tracked in `manifest.json`.

What goes where is decided per topic in the **topic lists**, not by whoever runs the prompt.

**Build in this order**, because each output is written around the ones before it:

1. **Decks** (`/build-slides N`): they carry the explanations and say when to switch to the notebook.
2. **Notebooks** (`/build-notebooks N`): written around the deck's live-coding slides, without repeating what
   the deck explains.
3. **Readings** (`/build-slides reading M`): only what the module's decks left out.
4. **Quizzes** (`/build-quizzes`), then the **instructor guide** (`/build-instructor-guide`).

## What's where

```
teaching-materials/
├── materials/               WHAT YOU USE (local only, except the instructor guide)
│   ├── slides/              session decks
│   ├── notebooks/           one notebook and environment file per lesson with code
│   ├── readings/            module readings, Word and PDF
│   ├── quizzes/             Canvas quizzes and answer keys
│   └── instructor-guide/    prep for a new or substitute instructor (committed)
└── how-to-build/            HOW IT'S MADE (nothing here goes to learners)
    ├── guide.md             this file
    ├── topics/
    │   └── session-01.md …  one editable topic list per session
    ├── design-rules.md      how the decks look and move (seeded from the instructor's decks)
    ├── deck-prompt.md       the prompt that builds one session deck from scratch
    ├── update-prompt.md     the prompt that updates an existing deck, slide by slide
    ├── notebook-prompt.md   the prompts that build or update one notebook, and the lesson notes
    ├── reading-prompt.md    the prompts that build or update one module reading (Word)
    ├── review-checklist.md  what to check before a deck is used
    ├── tools/               check_topics, prepare_learner_copy, check_stale
    ├── manifest.json        what each committed output was built from
    ├── templates/           the course deck template (committed); reading template and example decks (local only)
    └── to-update/           existing decks, notebooks or readings to update rather than rebuild (local only)
```

The local-only folders and files are git-ignored by the repo's root `.gitignore`. The rules (names, the session
map, learner-facing outputs, live coding, quizzes) are in [STYLE_GUIDE §11](../../STYLE_GUIDE.md#11-teaching-materials).

Every output is built by a Claude Code skill in `.claude/skills/` (`build-slides`, `build-notebooks`,
`build-quizzes`, `build-instructor-guide`), or by a person pasting the same prompt into Claude on the web or
desktop. Small hand fixes to an output are fine, but make the same fix in the lesson page too, or the next update
undoes it.

## Before you build

Some builders need tools that the lesson environments don't include. Set them up once per machine, in Git Bash
(see [AGENT_SETUP.md](../../AGENT_SETUP.md)).

| Skill | Needs |
|---|---|
| `build-slides` | Your template and example decks in `how-to-build/templates/` (see "Templates" below); `python-pptx` in any scratch Python; `python-docx` too, for readings; PowerPoint and Word (or LibreOffice) to export to PDF for checking |
| `build-notebooks` | The session's deck; `python-pptx` and `nbformat` in any scratch Python; `papermill` in **each** lesson environment; the credentials below |
| `build-quizzes` | [`text2qti`](https://pypi.org/project/text2qti/) |
| `build-instructor-guide` | nothing extra |

Install the scratch tools into any Python on your PATH (conda `base` is fine):
`pip install python-pptx python-docx nbformat text2qti`.

### Lesson environments and papermill

The `environments/*.yml` files are the recipes learners build their environments from, and each notebook ships
with a copy. Your installed environments are your own copies built from those recipes. Add testing tools to your
copies only, never to the `.yml` files.

1. **Make sure your environments match the recipes.** Create any that are missing, and update any built from
   an older `.yml`:
   ```bash
   conda env create -f environments/m03-swot.yml          # if m03-swot doesn't exist yet
   conda env update -n m03-swot -f environments/m03-swot.yml --prune   # if it exists but may be out of date
   ```
   Do the same for `m03-nwm`, `m03-wdfn` and `m04-synthesis` (`conda env list` shows which you have). `--prune`
   removes packages the `.yml` doesn't list, papermill included, so repeat step 2 whenever you repeat step 1.
2. **Add papermill without changing anything else.** `--freeze-installed` stops conda from upgrading or
   downgrading the packages already installed, so your environment keeps the learners' versions. (conda still
   refreshes `ca-certificates` and `certifi`; that's expected and harmless.)
   ```bash
   for e in m03-swot m03-nwm m03-wdfn m04-synthesis; do
     conda install -y -n "$e" -c conda-forge --freeze-installed papermill ipykernel
   done
   ```
   If conda says it can't install without changing other packages, stop and ask: don't remove the flag.
3. **Run each notebook inside its lesson's environment**, from a short working folder (SWOT file names overflow
   Windows' 260-character path limit in deep folders):
   ```bash
   conda run -n m03-swot papermill -k python3 --cwd <short-dir> <notebook>.ipynb <scratch-dir>/<notebook>_out.ipynb
   ```

### Credentials

Testing notebooks logs in to real services. The process running the build needs these environment variables:

| Notebooks | Needs |
|---|---|
| Module 3 lesson 1 (SWOT), Module 4 lessons 2 and 3 | `EARTHDATA_USERNAME`, `EARTHDATA_PASSWORD` (read by `earthaccess.login()`) |
| Module 3 lesson 3 (WDFN), Module 4 lesson 2 | `API_USGS_PAT` (read by `dataretrieval`) |
| Module 3 lesson 2 (NWM) | nothing |

Save them once as Windows user environment variables, following
[AGENT_SETUP.md, "Windows: credentials"](../../AGENT_SETUP.md#windows-credentials), which also shows how to check
them without printing the values. A program only sees environment variables that existed when it started: after
saving them, open a new terminal and start Claude Code from there. Never write the values into a file in this repo.

## Topic lists

Each `topics/session-NN.md` has the session's date, length, deck file name and lesson pages, then one row per
topic:

| Column | Meaning |
|---|---|
| **Topic** | What the slides (or reading, or notebook) cover |
| **Source** | The lesson page and section: `03/01 § Find datasets` means the "Find datasets" heading in `03-…/01_access_nasa_swot.md` |
| **Where** | `deck`, `notebook`, `reading`, `how-to` (the HydroShare "How to" guide), `cut` (website only); `deck + notebook` = a short version on slides and the full code in the notebook |
| **Min** | Minutes of session time, for rows on the deck. They add up to the session length |
| **What the slides should show or do** | Figures, builds, activities, anything the generator should know |

Edit them freely: move a topic from `reading` to `deck` (and take minutes from another row), split a row, add a
figure. Then run the checker from the repo root:

```bash
python teaching-materials/how-to-build/tools/check_topics.py        # or: ... check_topics.py 3
```

It checks that the minutes add up, the "Where" values are valid, and every `§ heading` still exists in its
lesson page. Run it again whenever a lesson changes: a renamed section shows up here before you build from it.

## Templates: your deck and reading templates, and example decks

`teaching-materials/how-to-build/templates/` holds what the generator copies its style from. **`template.pptx` is
committed**, so anyone who builds decks has it. The example decks and the reading template stay local: copy the
course lead's into your `templates/` folder if you build readings or want examples.

1. **`template.pptx`** (or `template.potx`): the most important file. To make one from your own deck by hand:
   1. Open a recent deck in your usual style (the course lead used the 2026 Data Publishing cohort deck).
   2. **Save As** `template.pptx` in `how-to-build/templates/` (this replaces the committed course template;
      commit it only if it should become the course template).
   3. Delete slides until exactly **one example of each slide type** in `design-rules.md` §4 is left: session
      title, program schedule, lesson objectives, content (one with a figure, one text-only), statement,
      section divider, activity, live coding (copy the activity slide and retitle it), code, before → after.
   4. On each example slide, type the slide type in the speaker notes (for example `TYPE: activity`), so the
      generator knows which is which.
   5. Remove anything that shouldn't be reused: other presenters' photos, old dates, talk-specific logos.
      Leave the CUAHSI branding, the schedule slide's icons and your own photo for the title slide.
2. **Two or three example decks** (`.pptx` or `.pdf`) that show your pacing and how you build ideas up across
   slides. Teaching decks are better than conference talks.
3. **`reading-template.docx`:** the Word styles readings are written in (Title, Subtitle, "Why it matters",
   Heading 1–2, Normal, List Bullet, Caption, Credit, Code, and the Link character style), with one sample
   paragraph of each. Change the look by modifying the styles in Word (Home → Styles → Modify), not by
   formatting the samples. `make_reading_template.py` made the first version.

**Why a template made from real slides:** the generator copies your example slides and replaces their content,
so every position, font, colour and emphasis comes from something you made. That keeps the decks looking like
yours: it doesn't build slides up from shapes, which is what makes generated decks look generated.

The course lead's copy (October 2026):

| File | What it is |
|---|---|
| `template.pptx` | Made from `260518_lplatt&kwong_DataPubCohort.pptx` by `make_template.py`, then edited by hand. 12 example slides (one per slide type; further reading uses content-text), each tagged `TYPE: …` in its notes |
| `make_template.py` | The script that made the first version of the template (needs `python-pptx`); only useful to start over |
| `reading-template.docx` | The reading styles: Arial, slate headings, shaded Code style, course name and page number in the footer |
| `make_reading_template.py` | The script that made the first reading template (needs `python-docx`); only useful to start over |
| `260518_lplatt&kwong_DataPubCohort.pptx` | 2026 Data Publishing cohort sessions: the session structure, activities and builds |
| `251112_Slides_LPlatt_Wk2_ConfigContent_READMEs.pdf` | 2025 pilot cohort, week 2: a full teaching session |
| `250313_lplatt_NMC_reproducibility_slides.pptx` | Conference talk: statement slides, highlight outlines, code |
| `260624_lplatt_TBEP_PracticalOpenScience.pdf` | Most recent talk (2026): statement slides, spotlight and grow-a-figure builds |

## Building a deck

### 1. Check the topic list

Read the session's topic list, make your edits, and run `check_topics.py`.

### 2. Run the prompt

**In Claude Code** (in this repo): run `/build-slides N` (N = the session number). The `build-slides` skill
makes the learner copies, then follows `deck-prompt.md`. It stops after the slide plan so you can adjust it.

**In Claude on the web or desktop:**

1. Make learner copies of the session's lesson pages (they drop internal notes and links):
   ```bash
   python teaching-materials/how-to-build/tools/prepare_learner_copy.py 03-federal-water-data-access-retrieval/00_introduction.md 03-federal-water-data-access-retrieval/01_access_nasa_swot.md --out-dir <scratch-dir>/learner
   ```
2. Start a new conversation and attach:
   - the learner copies;
   - the session's topic list and `design-rules.md`;
   - the figures the topic list names (from `images/`);
   - your template and one or two example decks from `how-to-build/templates/`.
3. Paste everything below the line in `deck-prompt.md`, with `{N}` replaced by the session number.
4. Review the slide plan it shows you, reply with changes or "go ahead", and download the `.pptx`.

### 3. Review

Go through [`review-checklist.md`](review-checklist.md). Small fixes are quickest in PowerPoint. If you fix
lesson *content* on a slide, fix the lesson page too, or the next build undoes it. If a fix is about style,
add it to `design-rules.md` so the next deck gets it right.

### 4. Save it

Save the deck in `teaching-materials/materials/slides/` under the file name in the topic list's header. **Decks are never
committed** (they're large, and they carry photos and screenshots). Share the final deck through Canvas, and
keep your own copy.

The deck records what it was built from: its document properties' **Comments** say `Built from <commit> with
topics/session-NN.md` (File → Info → Properties in PowerPoint). Decks aren't in `manifest.json`, because
`check_stale.py` can only track files that are in the repo. The update prompt uses that commit instead to see
what changed in the lessons since the deck was built.

### 5. Commit the topic list

If you edited the topic list or design rules along the way, commit those. Never the deck.

## Updating an existing deck

When a deck already exists and you only want it brought up to date (a deck you made by hand, an earlier
course's deck, or your own deck whose lessons changed), update it instead of rebuilding it:

1. Put the deck in `teaching-materials/how-to-build/to-update/`, named after the session's deck (the file name in its
   topic list header, e.g. `session-03_module-03_lesson-01_retrieve-nasa-swot-data.pptx`), so the prompt can
   find it. Skip this to update your deck in `teaching-materials/materials/slides/`; that's the usual way to bring a deck
   up to date after a lesson changes.
2. Start the speaker notes of any slide that must not change with `KEEP`.
3. Check the topic list, then run `update-prompt.md`: in Claude Code, `/build-slides N update`; on the web or
   desktop, attach the deck plus the same files as for a build.
4. It inventories the deck and shows a slide-by-slide plan (keep, update, move, remove, add). Adjust it, then
   let it go ahead. It saves the updated deck in `teaching-materials/materials/slides/` and never overwrites the file in
   `how-to-build/to-update/`.
5. Review and save the result as for a build.

## Building or updating a reading

Readings work like decks: built locally from the topic lists, never committed, and updated rather than rebuilt
when something changes. `reading-prompt.md` holds both prompts.

- **Build:** after the module's decks are done, run the Build prompt (in Claude Code: `/build-slides reading M`,
  where M is the module number). It collects the `reading` rows from the module's topic lists, shows you a plan,
  then writes `teaching-materials/materials/readings/module-0M_reading_<module slug>.docx` in the reading template's styles
  and saves a PDF next to it. No extra software: Word does the formatting.
- **Update:** run the Update prompt (`/build-slides reading M update`). It works on the reading in
  `teaching-materials/how-to-build/to-update/` if you put one there (a PDF-only reading is rebuilt as Word first), otherwise
  on yours in `materials/readings/`. It shows a section-by-section plan before changing anything. To protect a section, add
  a Word comment starting `KEEP` to its heading.
- **Edit by hand** in Word whenever you like, using the template's styles, then export the PDF again (File → Save
  As → PDF).
- **Save:** the `.docx` and PDF stay in `teaching-materials/materials/readings/` (git-ignored). Share the PDF through
  Canvas. The document's Comments property records the commit it was built from, which the Update prompt uses
  to see what changed.

## Building or updating a notebook

Notebooks come after the session's deck: the deck explains, the notebook is where learners run the code.
`notebook-prompt.md` holds both prompts and the lesson notes (each notebook's learning goal, credentials and the
fixes it needs until its lesson is corrected).

- **Build:** in Claude Code, `/build-notebooks N` (N = 3–6). It reads the deck's live-coding slides, shows you a
  plan, then writes one notebook per lesson with code into `teaching-materials/materials/notebooks/<module
  folder>/`, with the lesson's environment file next to it, and tests it in that environment. On the web or
  desktop, attach the deck, the topic list, the learner copy of the lesson and its environment file, and paste
  the Build prompt and the lesson notes.
- **What's in a notebook:** setup and credentials cells, the lesson sections that have code (with the lesson's
  headings, so the live-coding slides can name them), markers where each live-coding stretch starts and ends,
  short text that doesn't repeat the slides, the "Now you try it" task with a starter cell and the example answer
  collapsed under it, an optional "Going further" section for `notebook`-only topic rows, and the license, how to
  cite and acknowledgements at the end.
- **Update:** `/build-notebooks N update`, after a lesson, topic-list or deck change. It works on the notebook in
  `how-to-build/to-update/` if you put one there, otherwise on yours in `materials/notebooks/`. To protect a cell
  you edited by hand, add the tag `keep` to it (in JupyterLab, the property inspector's "Cell tags").
- **Save:** the notebook and environment file stay in `materials/notebooks/` (git-ignored). Upload both to the
  course's HydroShare resource, keeping the module folders. The notebook's metadata (`fwdc`) records the commit
  and deck it was built from.

## Quizzes and the instructor guide

- **Quizzes:** `/build-quizzes`, after the module's decks and readings; the `build-quizzes` skill covers the
  design, `text2qti` and the Canvas settings. Quiz questions and answer keys never go into the repo, a PR or an
  issue.
- **Instructor guide:** `/build-instructor-guide`, last. It's committed, so record a rebuild in `manifest.json`
  (below).

## Tools

All run from the repo root with any Python 3.9 or later (standard library only).

**`tools/check_topics.py`** checks the topic lists (see "Topic lists" above).

**`tools/prepare_learner_copy.py`.** Every learner-facing build starts from this copy of a page. It removes every
`TODO (dev team)` and `Partner review (…)` callout, turns internal course links (other pages, `{term}`, `{ref}`
and `{doc}` roles, the Glossary and References pages, the repo) into plain text, keeps external links and images,
and reports the counts. If the report ends with `WARNING: ... flag mention(s) left`, a page names a flag outside a
callout: check it by hand before anything built from it goes to learners. Write learner copies to a scratch
directory outside this repo:

```bash
python teaching-materials/how-to-build/tools/prepare_learner_copy.py 03-federal-water-data-access-retrieval/01_access_nasa_swot.md -o <scratch-dir>/01_access_nasa_swot.md
python teaching-materials/how-to-build/tools/prepare_learner_copy.py 03-federal-water-data-access-retrieval/*.md --out-dir <scratch-dir>/learner
```

**`tools/check_stale.py`** lists committed outputs (today, the instructor guide) whose sources changed since they
were built, from `manifest.json`. After rebuilding one, commit the lesson change first, then record it and commit
the output with `manifest.json`:

```bash
python teaching-materials/how-to-build/tools/check_stale.py --update teaching-materials/materials/instructor-guide/00_start-here.md \
    --kind instructor-guide --builder build-instructor-guide --source 03-federal-water-data-access-retrieval
```

`--kind`, `--builder` and `--source` are needed only for a new entry. Merge PRs with merge commits, not squash
merges, so the recorded commits stay reachable. For the local-only outputs, compare the commit recorded in the
file with `git diff <commit> HEAD -- <sources>`; the update prompts do this for you.

## Session map

All sessions are in 2026, at 2:00 pm ET. The Dec 1 peer review and Dec 3 demos have no decks. The same map is
in STYLE_GUIDE §11; change both together.

| Session | Date | Length | Covers | Lesson pages | Notebooks |
|---|---|---|---|---|---|
| 1 | Tue Nov 3 | 90 min | Course welcome, logistics, setup; Module 1 overview + lessons 1–3 | `01-data-best-practices/00`–`03` | none |
| 2 | Thu Nov 5 | 120 min | Module 2 overview + lessons 1–3 | `02-federal-water-data-landscape/00`–`03` | none |
| 3 | Tue Nov 10 | 90 min | Module 3 overview + lesson 1 | `03-federal-water-data-access-retrieval/00`, `01` | SWOT |
| 4 | Thu Nov 12 | 90 min | Module 3 lesson 2 | `03-federal-water-data-access-retrieval/02` | NWM |
| 5 | Tue Nov 17 | 90 min | Module 3 lesson 3 | `03-federal-water-data-access-retrieval/03` | WDFN |
| 6 | Thu Nov 19 | 120 min | Module 4 overview + lessons 1–3 | `04-federal-water-data-synthesis/00`–`03` | lessons 2 and 3 |

## File names

The naming rule is in STYLE_GUIDE §11. **Module slugs** are the module folder names without their number
(`data-best-practices`, `federal-water-data-landscape`, `federal-water-data-access-retrieval`,
`federal-water-data-synthesis`). **Lesson slugs** come from the lesson page's title, lowercased, with spaces
turned into hyphens and punctuation dropped: *Retrieve NASA SWOT data* → `retrieve-nasa-swot-data`. Module 4
lesson 2's slug is shortened to `synthesizing-federal-data-products`.

| Session | Deck (`slides/`) | Notebooks (`notebooks/<module folder>/`, each with `_environment.yml`) |
|---|---|---|
| 1 | `session-01_module-01_data-best-practices.pptx` | |
| 2 | `session-02_module-02_federal-water-data-landscape.pptx` | |
| 3 | `session-03_module-03_lesson-01_retrieve-nasa-swot-data.pptx` | `module-03_lesson-01_retrieve-nasa-swot-data.ipynb` |
| 4 | `session-04_module-03_lesson-02_retrieve-noaa-nwm-data.pptx` | `module-03_lesson-02_retrieve-noaa-nwm-data.ipynb` |
| 5 | `session-05_module-03_lesson-03_retrieve-usgs-wdfn-data.pptx` | `module-03_lesson-03_retrieve-usgs-wdfn-data.ipynb` |
| 6 | `session-06_module-04_federal-water-data-synthesis.pptx` | `module-04_lesson-02_synthesizing-federal-data-products.ipynb`, `module-04_lesson-03_additional-federal-water-data.ipynb` |

The notebook module folders are `module-03_federal-water-data-access-retrieval` and
`module-04_federal-water-data-synthesis`. Readings: `readings/module-NN_reading_<module slug>.docx` (and its
PDF), for Modules 2–4. Quizzes: `quizzes/module-NN_quiz_<module slug>.txt`, its `.zip` and `_key.md`. Instructor
guide: `instructor-guide/00_start-here.md`, `01_prepare-to-teach.md`, `02_how-the-course-is-built.md`, and one
`session-NN_<deck name without .pptx>.md` per session.

## When something changes

- **A lesson changed:** `check_topics.py` says whether a section the topic list names was renamed or removed.
  Update the topic list, then **update**, in order, the deck, the session's notebooks and the reading
  (`/build-slides N update`, `/build-notebooks N update`, `/build-slides reading M update`) rather than rebuilding
  them, so hand edits survive. Each update compares the lessons with the commit the output was built from.
- **A deck changed:** update the session's notebooks too, so their live-coding markers and pointers to slides
  still match.
- **You want a different style:** edit `design-rules.md` or the template, then update each deck.
