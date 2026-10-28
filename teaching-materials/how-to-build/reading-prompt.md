# Prompts: build or update one module reading

Modules 2, 3 and 4 each have at most one reading: the extra detail and nuance that's useful but not needed in
the session. Module 1 has none. A reading is a **Word document** (`.docx`) written in the reading template's
styles, exported to PDF for Canvas. Both files are built locally and **never committed**, like the decks.

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

1. **Topic lists** for the module's sessions in `teaching-materials/how-to-build/topics/` (Module 2: session 2;
   Module 3: sessions 3–5; Module 4: session 6). Cover every row whose "Where" is `reading`, and nothing else.
2. **Lesson pages:** the learner copies of the pages those rows name. They are the only source of content.
3. **Figures** in `images/` that those sections use.
4. **Reading template:** `teaching-materials/how-to-build/templates/reading-template.docx`. Its styles set the look:
   Title, Subtitle, "Why it matters", Heading 1, Heading 2, Normal, List Bullet, Caption, Credit, Code and the
   Link character style. It contains one sample paragraph of each.

### Rules

- Use only what the lesson pages say: no new claims, numbers, quotes, code or links. Move the lesson text with
  light edits so each section stands alone; keep headings, figures (with captions and credits), code and
  external links as they are.
- The course is called **Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access**.
- No internal course links, nothing from `TODO (dev team)` or `Partner review` callouts.
- Agency order NASA → NOAA → USGS; "WDFN", not "NWIS".
- About 1,500–2,500 words of prose. If the `reading` rows need more, list what doesn't fit in your report
  rather than cutting it silently.
- **Format only with the template's styles.** Don't set fonts, sizes or colours by hand, and don't add text
  boxes, shapes or tables for layout. Bold and italics inside a paragraph are fine.

### Steps

1. **Plan, then stop.** List the sections you'll write (one per `reading` row, grouped by lesson), the lesson
   section each comes from, any figures and code, and an estimated word count. Wait for my go-ahead.
2. **Write** `teaching-materials/materials/readings/module-0{M}_reading_<module slug>.docx` (the file name in the topic list
   header), starting from a copy of the template so its styles carry over, and delete the template's sample
   paragraphs:
   - **Title:** "<Module title>: more detail". **Subtitle:** "Reproducible Workflows with Open Water Data: NASA,
     NOAA, USGS River Data Access · Module {M} · Read after the session(s)".
   - **Why it matters:** one sentence on why this reading is worth the time.
   - One **Heading 1** per lesson, and a **Heading 2** per `reading` row under it.
   - **Figures** inserted inline at up to 6 inches wide, with a **Caption** paragraph below and a **Credit**
     paragraph for borrowed images, and alt text on the picture.
   - **Code** copied from the lesson, one **Code** paragraph per line, keeping indentation.
   - End with **Key terms** (glossary terms the reading uses, in the glossary's words) and **Further reading**
     (the lessons' external links, as real hyperlinks in the Link style).
   - In the document properties, set **Comments** to `Built from <commit> with topics/session-NN.md` (and any other
     topic lists used), using the repo commit the lessons were read from (`git rev-parse --short HEAD`) if you
     know it.
   If you're writing the file with code, use `python-docx`, opening the template as the starting document.
3. **Export and check.** Save a PDF next to it (in Word: File → Save As → PDF). Check the PDF: figures appear,
   code lines don't wrap mid-token or run off the page, headings aren't left alone at the bottom of a page.
4. **Report** the word count, the sections and their lesson sources, and anything you couldn't place.

Both files stay in `teaching-materials/materials/readings/`, which is git-ignored. Don't commit them.

---

## Update

---

You are updating the reading for **Module {M}** of *Reproducible Workflows with Open Water Data: NASA, NOAA, USGS
River Data Access*. It already exists and the instructor likes it. Change only what needs changing.

### Inputs

1. **The reading to update:** `module-0{M}_reading_*.docx` in `teaching-materials/how-to-build/to-update/` if there is one,
   otherwise the one in `teaching-materials/materials/readings/`. (A reading you have only as a PDF: put it in
   `how-to-build/to-update/`, and the first step is to rebuild it as a `.docx` in the template's styles with the same text and
   structure.)
2. The same topic lists, lesson pages, figures and reading template as for a build.

### Rules

The build rules apply to everything you add or change. A section whose Heading 2 (or Heading 1) carries a Word
comment starting `KEEP` is never changed, moved or removed.

### Steps

1. **Inventory and plan, then stop.** List every Heading 1 and Heading 2 section: the topic-list row and lesson
   section it covers (or "none"), and whether it's marked KEEP. If the document's Comments property says
   `Built from <commit>` and you can run git, list what changed in the lessons and topic lists since then
   (`git diff <commit> -- <pages> <topic lists>`). For each section decide **keep**, **update** (quote the lesson
   line it now follows), **move** or **remove**, and list the `reading` rows with no section (**add**). Show me
   the plan and wait for my go-ahead.
2. **Make the changes** in place, keeping the reading's wording and styles wherever the lesson hasn't changed.
   Update the Comments property to the new commit. Save to `teaching-materials/materials/readings/`; never overwrite the
   file in `how-to-build/to-update/`.
3. **Export and check** the PDF as for a build.
4. **Report** a change log (one line per section: kept, updated, added, removed or moved, and why) and the new
   word count.

---
