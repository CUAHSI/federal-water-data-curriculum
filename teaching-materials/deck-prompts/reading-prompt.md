# Prompt: build one module reading

Modules 2, 3 and 4 each have at most one reading: the extra detail and nuance that's useful but not needed in
the session. Module 1 has none. Copy everything below the line into Claude, replacing `{M}` with the module
number (2–4). Run it after the module's decks, so it only holds what the decks left out.

---

You are writing the reading for **Module {M}** of *Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access*, for researchers
and graduate students who know some Python but are new to federal water data APIs. Learners read it after the
module's sessions, in about 15 minutes. It isn't required for the sessions; it holds detail the slides left out.

## Inputs

1. **Topic lists** for the module's sessions in `teaching-materials/deck-prompts/topics/` (Module 2: session 2;
   Module 3: sessions 3–5; Module 4: session 6). Cover every row whose "Where" is `reading`, and nothing else.
2. **Lesson pages:** the learner copies of the pages those rows name. They are the only source of content.
3. **Figures** in `images/` that those sections use.

## Rules

- Use only what the lesson pages say: no new claims, numbers, quotes, code or links. Move the lesson text with
  light edits so each section stands alone; keep headings, figures (with captions and credits), code and
  external links as they are.
- No internal course links, nothing from `TODO (dev team)` or `Partner review` callouts.
- Agency order NASA → NOAA → USGS; "WDFN", not "NWIS".
- About 1,500–2,500 words of prose. If the `reading` rows need more, list what doesn't fit in your report
  rather than cutting it silently.

## Output

Write `teaching-materials/readings/module-0{M}_reading_<module slug>.qmd` (the file name in the topic list
header):

```yaml
---
title: "<Module title>: more detail"
subtitle: "Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data Access · Module {M} · Read after the session(s)"
format: typst
---
```

- First line: one sentence on why this reading is worth the time.
- Then one `##` section per `reading` row (group rows from the same lesson under the lesson's name).
- Figures use paths from the repo root's `images/` folder written relative to the reading
  (`../../images/m03/…`). Shared page settings come from the repo's `_quarto.yml`.
- End with "Key terms" (glossary terms the reading uses, defined in the glossary's words) and "Further reading"
  (the lessons' external links).

Render it with `quarto render <file>` and check the PDF: figures appear, nothing runs off the page. Report the
word count and anything you couldn't place.
