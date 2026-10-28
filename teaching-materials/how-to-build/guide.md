# Deck prompts: guide

Everything a person needs to have Claude build or update a session deck (PowerPoint) or a module reading (PDF)
from the lesson pages, in the instructor's own style, for *Reproducible Workflows with Open Water Data:
NASA, NOAA, USGS River Data Access*.

The lessons stay the source of truth. Three kinds of output come from them, each with its own job:

| Output | Its job | Where |
|---|---|---|
| **Deck** | The important concepts and points, presented live | `teaching-materials/materials/slides/`, one `.pptx` per session, **built locally and never committed** (git-ignored); shared through Canvas |
| **Notebook** | Practising the code | the learner bundle (`teaching-materials/materials/learner-bundle/`) |
| **Reading** | Extra detail and nuance that's useful but not needed in the session (Modules 2–4 only, at most one per module) | `teaching-materials/materials/readings/`, a Word document exported to PDF, **built locally and never committed** (git-ignored); the PDF is shared through Canvas |

What goes where is decided per topic in the **topic lists**, not by whoever runs the prompt.

## What's where

```
teaching-materials/
├── materials/               WHAT YOU USE
│   ├── slides/              the decks you build (local only)
│   └── readings/            the readings you build, Word and PDF (local only)
└── how-to-build/            HOW IT'S MADE (this folder)
    ├── guide.md             this file
    ├── topics/
    │   └── session-01.md …  one editable topic list per session
    ├── design-rules.md      how the decks look and move (seeded from the instructor's decks)
    ├── deck-prompt.md       the prompt that builds one session deck from scratch
    ├── update-prompt.md     the prompt that updates an existing deck, slide by slide
    ├── reading-prompt.md    the prompts that build or update one module reading (Word)
    ├── review-checklist.md  what to check before a deck is used
    ├── templates/           your deck and reading templates and example decks (local only; see below)
    └── to-update/           existing decks or readings to update rather than rebuild (local only)
```

The four local-only folders are git-ignored by the repo's root `.gitignore`. Create them yourself; nothing in
them is ever committed.

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

`teaching-materials/how-to-build/templates/` holds what the generator copies its style from. Each person who builds
decks needs their own copy (ask the course lead for theirs).

1. **`template.pptx`** (or `template.potx`): the most important file. To make one from your own deck by hand:
   1. Open a recent deck in your usual style (the course lead used the 2026 Data Publishing cohort deck).
   2. **Save As** `template.pptx` in `how-to-build/templates/`.
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

## When something changes

- **A lesson changed:** `check_topics.py` says whether a section the topic list names was renamed or removed.
  Update the topic list, then **update** the deck and reading (`/build-slides N update`, `/build-slides reading M
  update`) rather than rebuilding them, so hand edits survive. Each update compares the lessons with the commit
  the deck or reading was built from.
- **You want a different style:** edit `design-rules.md` or the template, then update each deck.
