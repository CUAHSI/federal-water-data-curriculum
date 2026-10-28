# Deck prompts

Everything a person needs to have Claude build a session deck (PowerPoint) or a module reading (PDF) from the
lesson pages, in the instructor's own style.

The lessons stay the source of truth. Three kinds of output come from them, each with its own job:

| Output | Its job | Where |
|---|---|---|
| **Deck** | The important concepts and points, presented live | `teaching-materials/slides/`, one `.pptx` per session |
| **Notebook** | Practising the code | the learner bundle (`teaching-materials/learner-bundle/`) |
| **Reading** | Extra detail and nuance that's useful but not needed in the session (Modules 2–4 only, at most one per module) | `teaching-materials/readings/`, rendered to PDF |

What goes where is decided per topic in the **topic lists**, not by whoever runs the prompt.

## What's here

```
deck-prompts/
├── README.md             this file
├── topics/
│   └── session-01.md …   one editable topic list per session
├── design-rules.md       how the decks look and move (seeded from the instructor's decks)
├── deck-prompt.md        the prompt that builds one session deck
├── reading-prompt.md     the prompt that builds one module reading
├── review-checklist.md   what to check before a deck is used
└── reference/            your template and example decks (not committed; see reference/README.md)
```

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
python teaching-materials/tools/check_topics.py        # or: ... check_topics.py 3
```

It checks that the minutes add up, the "Where" values are valid, and every `§ heading` still exists in its
lesson page. Run it again whenever a lesson changes: a renamed section shows up here before you build from it.

## Building a deck

### 1. One time: set up `reference/`

Put the template and two or three example decks in `teaching-materials/deck-prompts/reference/`, as described
in [`reference/README.md`](reference/README.md). This folder isn't committed, so each person who builds decks
needs their own copy (ask the course lead for theirs).

### 2. Check the topic list

Read the session's topic list, make your edits, and run `check_topics.py`.

### 3. Run the prompt

**In Claude Code** (in this repo): run `/build-slides N` (N = the session number). The `build-slides` skill
makes the learner copies, then follows `deck-prompt.md`. It stops after the slide plan so you can adjust it.

**In Claude on the web or desktop:**

1. Make learner copies of the session's lesson pages (they drop internal notes and links):
   ```bash
   python teaching-materials/tools/prepare_learner_copy.py 03-federal-water-data-access-retrieval/00_introduction.md 03-federal-water-data-access-retrieval/01_access_nasa_swot.md --out-dir <scratch-dir>/learner
   ```
2. Start a new conversation and attach:
   - the learner copies;
   - the session's topic list and `design-rules.md`;
   - the figures the topic list names (from `images/`);
   - your template and one or two example decks from `reference/`.
3. Paste everything below the line in `deck-prompt.md`, with `{N}` replaced by the session number.
4. Review the slide plan it shows you, reply with changes or "go ahead", and download the `.pptx`.

### 4. Review

Go through [`review-checklist.md`](review-checklist.md). Small fixes are quickest in PowerPoint. If you fix
lesson *content* on a slide, fix the lesson page too, or the next build undoes it. If a fix is about style,
add it to `design-rules.md` so the next deck gets it right.

### 5. Save it

Save the deck in `teaching-materials/slides/` under the file name in the topic list's header.

### 6. Record it

Record what the deck was built from, so `check_stale.py` can tell you when to rebuild (from the repo root, on
your branch, after committing any lesson or topic-list changes):

```bash
python teaching-materials/tools/check_stale.py --update teaching-materials/slides/session-03_module-03_lesson-01_retrieve-nasa-swot-data.pptx \
    --kind slides --builder build-slides \
    --source teaching-materials/deck-prompts/topics/session-03.md \
    --source teaching-materials/deck-prompts/design-rules.md \
    --source 03-federal-water-data-access-retrieval/00_introduction.md \
    --source 03-federal-water-data-access-retrieval/01_access_nasa_swot.md \
    --source images/m03
```

Commit the deck and `manifest.json` together.

## Building a reading

After the module's decks are done, run `reading-prompt.md` the same way (in Claude Code: `/build-slides
reading M`, where M is the module number). It collects the `reading` rows from the module's topic lists. Render
with `quarto render teaching-materials/readings/<file>.qmd`, or with Actions → Render readings. Record it like a
deck, with `--kind reading` and the topic lists as sources.

## When something changes

- **A lesson changed:** `check_stale.py` lists the decks and readings built from it, and `check_topics.py`
  says whether a section the topic list names was renamed or removed. Update the topic list, then rebuild,
  or fix the affected slides by hand and re-record.
- **You want a different style:** edit `design-rules.md` or the template. Every deck lists the design rules as
  a source, so they'll all show as stale.
