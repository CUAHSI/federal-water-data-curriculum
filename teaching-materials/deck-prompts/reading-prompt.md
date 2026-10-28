# Prompts: build or update one module reading

Modules 2, 3 and 4 each have at most one reading: the extra detail and nuance that's useful but not needed in
the session. Module 1 has none. A reading is a Quarto file (`.qmd`) rendered to PDF; both are built locally and
**never committed**, like the decks, and the PDF is shared through Canvas.

This file holds two prompts. Use **Build** for a module with no reading yet, and **Update** to bring an existing
reading up to date (after a lesson or topic-list change, or to rework a reading you already have). Copy
everything between the lines of the one you need into Claude, replacing `{M}` with the module number (2–4). In
Claude Code, `/build-slides reading M` and `/build-slides reading M update` do the same. Run them after the
module's decks, so the reading only holds what the decks left out.

## Build

---

You are writing the reading for **Module {M}** of *Reproducible Workflows with Open Water Data: NASA, NOAA, USGS
River Data Access*, for researchers and graduate students who know some Python but are new to federal water
data APIs. Learners read it after the module's sessions, in about 15 minutes. It isn't required for the
sessions; it holds detail the slides left out.

### Inputs

1. **Topic lists** for the module's sessions in `teaching-materials/deck-prompts/topics/` (Module 2: session 2;
   Module 3: sessions 3–5; Module 4: session 6). Cover every row whose "Where" is `reading`, and nothing else.
2. **Lesson pages:** the learner copies of the pages those rows name. They are the only source of content.
3. **Figures** in `images/` that those sections use.

### Rules

- Use only what the lesson pages say: no new claims, numbers, quotes, code or links. Move the lesson text with
  light edits so each section stands alone; keep headings, figures (with captions and credits), code and
  external links as they are.
- The course is called **Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access**.
- No internal course links, nothing from `TODO (dev team)` or `Partner review` callouts.
- Agency order NASA → NOAA → USGS; "WDFN", not "NWIS".
- About 1,500–2,500 words of prose. If the `reading` rows need more, list what doesn't fit in your report
  rather than cutting it silently.

### Steps

1. **Plan, then stop.** List the sections you'll write (one per `reading` row, grouped by lesson), the lesson
   section each comes from, any figures and code, and an estimated word count. Wait for my go-ahead.
2. **Write** `teaching-materials/readings/module-0{M}_reading_<module slug>.qmd` (the file name in the topic list
   header), starting:

   ```yaml
   ---
   # Built from <commit> with topics/session-NN.md (and any other topic lists used)
   title: "<Module title>: more detail"
   subtitle: "Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access · Module {M} · Read after the session(s)"
   format: typst
   ---
   ```

   Use the repo commit the lessons were read from (`git rev-parse --short HEAD`) if you know it.
   - First line: one sentence on why this reading is worth the time.
   - Then one `##` section per `reading` row (group rows from the same lesson under the lesson's name).
   - Figures use paths from the repo root's `images/` folder written relative to the reading
     (`../../images/m03/…`). Shared page settings come from the repo's `_quarto.yml`.
   - End with "Key terms" (glossary terms the reading uses, defined in the glossary's words) and "Further reading"
     (the lessons' external links).
3. **Render and check.** `quarto render <file>` from the repo root; check the PDF: figures appear, code fits,
   nothing runs off the page.
4. **Report** the word count, the sections and their lesson sources, and anything you couldn't place.

Both the `.qmd` and the PDF stay in `teaching-materials/readings/`, which is git-ignored. Don't commit them.

---

## Update

---

You are updating the reading for **Module {M}** of *Reproducible Workflows with Open Water Data: NASA, NOAA, USGS
River Data Access*. It already exists and the instructor likes it. Change only what needs changing.

### Inputs

1. **The reading to update:** `module-0{M}_reading_*.qmd` in `teaching-materials/to-update/` if there is one,
   otherwise the one in `teaching-materials/readings/`. (A reading you have only as a PDF or Word file: put it in
   `to-update/`, and the first step is to turn it into a `.qmd` with the same text and structure.)
2. The same topic lists, lesson pages and figures as for a build.

### Rules

The build rules apply to everything you add or change. Sections that start with a `<!-- KEEP -->` comment are
never changed, moved or removed.

### Steps

1. **Inventory and plan, then stop.** List every `##` section: the topic-list row and lesson section it covers
   (or "none"), and whether it's marked KEEP. If the header comment says `Built from <commit>` and you can run git,
   list what changed in the lessons and topic lists since then (`git diff <commit> -- <pages> <topic lists>`).
   For each section decide **keep**, **update** (quote the lesson line it now follows), **move** or **remove**,
   and list the `reading` rows with no section (**add**). Show me the plan and wait for my go-ahead.
2. **Make the changes** in place, keeping the reading's wording wherever the lesson hasn't changed. Update the
   header comment to the new commit. Save to `teaching-materials/readings/`; never overwrite the file in
   `to-update/`.
3. **Render and check** as for a build.
4. **Report** a change log (one line per section: kept, updated, added, removed or moved, and why) and the new
   word count.

---
