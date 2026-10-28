---
name: build-slides
description: Build or update a session's PowerPoint deck (in the instructor's style, from the session's topic list) or a module's reading PDF, using the prompts in teaching-materials/how-to-build/. Use when asked to make, update or rebuild slides or a reading. Arguments - a session number (1–6) to build a deck, "N update" to update one, "reading M" (M = 2–4) to build a reading, or "reading M update" to update one.
---

# Build a session deck or a module reading

The prompts, topic lists and design rules live in `teaching-materials/how-to-build/`; read its `guide.md` first.
This skill runs the same prompts a person would paste into Claude, with the setup done for them. The lessons
are the source of truth. If a deck needs different content, change the lesson (or flag it), not the slide.

## A deck (`/build-slides N`)

1. **Check the inputs.**
    - `python teaching-materials/how-to-build/tools/check_topics.py N` passes. If it doesn't, stop and report: a topic list
      that names a missing section needs a person to decide.
    - `teaching-materials/how-to-build/templates/` has a `template.pptx` (or `.potx`). If it doesn't, stop and
      say so: the deck can't match the instructor's style without it (see "Templates" in `how-to-build/guide.md`).
2. **Make learner copies** of the lesson pages the topic list names, with
   `teaching-materials/how-to-build/tools/prepare_learner_copy.py`, into a scratch directory outside the repo. Note the
   counts for the PR.
3. **Follow `how-to-build/deck-prompt.md`** with `{N}` = N, reading the files from the repo (topic list,
   learner copies, `images/`, design rules, `how-to-build/templates/`).
    - After step 2 of the prompt (the slide plan), stop and show the plan unless the user said to go straight
      through.
    - Write the deck with `python-pptx`, copying the template's example slides (see the prompt). Install it in
      a scratch environment if needed, never in a lesson environment.
    - Render every slide to images to check it: PowerPoint (`SaveAs` PDF through COM on Windows) or LibreOffice
      (`soffice --headless --convert-to pdf`), then look at each page.
4. **Save, don't commit.** Decks live in `teaching-materials/materials/slides/`, which is git-ignored: never commit a deck
   or add it to `manifest.json`. Set the deck's Comments property to `Built from <short HEAD commit> with
   topics/session-0N.md`. Commit only topic-list or design-rule edits.
5. **Report** (to the user, and in the PR if there is one): the prompt's report (step 5), the learner-copy
   counts, and which slides you'd most like a person to look at.

## Updating a deck (`/build-slides N update`)

Use this when a deck for the session already exists: one in `teaching-materials/how-to-build/to-update/`, or else the
local deck in `teaching-materials/materials/slides/`. Default to it whenever a deck exists and the user asks
to "rebuild" after a lesson change, and say so.

1. Check the inputs as for a build (`check_topics.py N`; the template is needed only if the deck lacks a slide
   type it must add).
2. Make learner copies of the lesson pages.
3. Follow `how-to-build/update-prompt.md` with `{N}` = N. Stop after its plan (step 2) unless the user said to
   go straight through. Never change slides whose notes start with `KEEP`; never overwrite the file in
   `how-to-build/to-update/`.
4. Save and report as for a build (never commit the deck), with the prompt's change log.

## A reading (`/build-slides reading M`, `/build-slides reading M update`)

1. Run `check_topics.py` for the module's sessions (Module 2: 2; Module 3: 3 4 5; Module 4: 6).
2. Make learner copies of the pages the `reading` rows name.
3. Follow the **Build** or **Update** prompt in `how-to-build/reading-prompt.md` with `{M}` = M. Stop after its
   plan unless the user said to go straight through.
    - Write the `.docx` with `python-docx`, opening `teaching-materials/how-to-build/templates/reading-template.docx` as
      the starting document and using only its styles. Install it in a scratch environment if needed.
    - Export the PDF with Word (`SaveAs` with format 17 through COM on Windows) or LibreOffice
      (`soffice --headless --convert-to pdf`), and look at every page.
4. **Save, don't commit**, as for a deck: `teaching-materials/materials/readings/` is git-ignored, and readings aren't in
   `manifest.json`. The document's Comments property records the commit it was built from.

## Rules
- Only content from the lesson pages: no invented claims, numbers, quotes, code or figures. Gaps become
  visible placeholders and go in the report.
- No internal course links, glossary links or repo links; no `TODO (dev team)` or `Partner review` content.
- Agency order NASA → NOAA → USGS; WDFN naming.
- Never overwrite an existing deck with a fresh build without asking; offer an update instead.
