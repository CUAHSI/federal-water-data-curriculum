---
name: build-slides
description: Build or rebuild a session's PowerPoint deck (in the instructor's style, from the session's topic list) or a module's reading PDF, using the prompts in teaching-materials/deck-prompts/. Use when asked to make, update or rebuild slides or a reading, or when check_stale.py lists one. Arguments - a session number (1–6) for a deck, or "reading M" (M = 2–4) for a reading.
---

# Build a session deck or a module reading

The prompts, topic lists and design rules live in `teaching-materials/deck-prompts/`; read its README first.
This skill runs the same prompts a person would paste into Claude, with the setup done for them. The lessons
are the source of truth. If a deck needs different content, change the lesson (or flag it), not the slide.

## A deck (`/build-slides N`)

1. **Check the inputs.**
    - `python teaching-materials/tools/check_topics.py N` passes. If it doesn't, stop and report: a topic list
      that names a missing section needs a person to decide.
    - `teaching-materials/deck-prompts/reference-decks/` has a `template.pptx` (or `.potx`). If it doesn't, stop and
      say so: the deck can't match the instructor's style without it (see `reference-decks/README.md`).
2. **Make learner copies** of the lesson pages the topic list names, with
   `teaching-materials/tools/prepare_learner_copy.py`, into a scratch directory outside the repo. Note the
   counts for the PR.
3. **Follow `deck-prompts/deck-prompt.md`** with `{N}` = N, reading the files from the repo (topic list,
   learner copies, `images/`, design rules, `reference-decks/`).
    - After step 2 of the prompt (the slide plan), stop and show the plan unless the user said to go straight
      through.
    - Write the deck with `python-pptx`, copying the template's example slides (see the prompt). Install it in
      a scratch environment if needed, never in a lesson environment.
    - Render every slide to images to check it: PowerPoint (`SaveAs` PDF through COM on Windows) or LibreOffice
      (`soffice --headless --convert-to pdf`), then look at each page.
4. **Record** the deck with `check_stale.py --update` as in the README (step 6), with the topic list, design
   rules, lesson pages and image folders as sources.
5. **Report in the PR:** the prompt's report (step 5), the learner-copy counts, and which slides you'd most like
   a person to look at.

## A reading (`/build-slides reading M`)

1. Run `check_topics.py` for the module's sessions (Module 2: 2; Module 3: 3 4 5; Module 4: 6).
2. Make learner copies of the pages the `reading` rows name.
3. Follow `deck-prompts/reading-prompt.md` with `{M}` = M. Render with `quarto render <file>` and check the
   PDF.
4. Record it with `--kind reading` and the module's topic lists and lesson pages as sources.

## Rules
- Only content from the lesson pages: no invented claims, numbers, quotes, code or figures. Gaps become
  visible placeholders and go in the report.
- No internal course links, glossary links or repo links; no `TODO (dev team)` or `Partner review` content.
- Agency order NASA → NOAA → USGS; WDFN naming.
- A deck that has been edited by hand since it was generated: ask before overwriting it. Offer to rebuild only
  the slides for the topic rows that changed.
