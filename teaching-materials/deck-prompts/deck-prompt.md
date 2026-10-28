# Prompt: build one session deck

Copy everything below the line into Claude, replacing `{N}` with the session number (1–6). See README.md for
what to attach and how to run it. In Claude Code, `/build-slides {N}` does the same thing.

---

You are building the slide deck for **Session {N}** of *Federal Open Water Data for Researchers*, a CUAHSI
course for researchers and graduate students who know some Python but are new to federal water data APIs. The
instructor presents this deck live; for pilot learners, the deck *is* the lesson, so it must stand on its own.
It must look like the instructor built it herself in PowerPoint.

## Inputs

1. **Topic list:** `teaching-materials/deck-prompts/topics/session-0{N}.md`. It lists every topic the deck
   covers, the lesson section it comes from, the minutes it gets, and what the slides should show. It is the
   plan: cover every row whose "Where" includes `deck`, in that order, within its minutes. Don't add topics,
   and don't put `reading`, `notebook`-only, `how-to`-only or `cut` rows on slides.
2. **Lesson pages:** the learner copies of the pages the topic list names (made with
   `teaching-materials/tools/prepare_learner_copy.py`). They are the only source of content.
3. **Figures:** the files in `images/` that the topic list and the pages name.
4. **Design rules:** `teaching-materials/deck-prompts/design-rules.md`. Follow them exactly; where they say
   **DECIDE**, use the default.
5. **Template:** `teaching-materials/deck-prompts/reference-decks/template.pptx` (or `.potx`). It contains one example
   slide for each slide type in the design rules, plus the slide masters and layouts.
6. **Example decks** (optional): the other files in `teaching-materials/deck-prompts/reference-decks/`. Use them to
   see how the instructor paces, builds up and highlights ideas. Never copy their content.

## Content rules

- Use only what the lesson pages say. Don't invent claims, numbers, quotes, code, dates or links. If a topic
  row asks for something the lesson doesn't have, leave a visible placeholder on the slide
  ("CONTENT NEEDED: …") and list it in the report.
- Code on slides is copied from the lesson, at most 12 lines per slide. Shorten only by leaving lines out
  (and say so in the notes); never change what a line does.
- Define a term on the slide where it first appears, in the lesson's or glossary's words.
- No internal course links (other pages, the glossary, the repo); external links are fine. Nothing from
  `TODO (dev team)` or `Partner review` callouts (the learner copies have already removed them).
- Agency order is always NASA → NOAA → USGS. Write "WDFN" (Water Data for the Nation), not "NWIS", except when
  contrasting with the legacy services.
- Live-coding slides follow STYLE_GUIDE §11: they name the notebook file and the notebook sections (which match
  the lesson headings), 2–3 things to point out, the minutes, and when to come back.

## Steps

### 1. Study the style (no output yet)

Open the template and look at every example slide: which layout it uses, where the title and body sit, the
fonts, sizes and colours, and how the emphasis is done. Skim the example decks for pacing and for how ideas are
built up across several slides. Read the design rules in full.

### 2. Plan the deck and stop

Write a slide plan as a table: slide number, topic-list row, slide type (design rules §4), title, what's on it
(text summary, figure file or code lines), and any build (which slides repeat with one change). Then check it:

- the slides for each row fit its minutes (design rules §8: about 1–2 ideas for 3 minutes; a build counts as
  one idea);
- every `deck` row is covered, in order;
- each block of concepts ends in an activity, a live-coding switch or a question.

Show me the plan and wait for my go-ahead before building anything. I may move, merge or drop slides.

### 3. Build the deck

Work from a copy of the template so the masters, layouts, theme fonts and colours carry over:

- For each planned slide, **duplicate the template's example slide of that type** and replace its text and
  pictures. Keep every position, size and format; change only the content. If a slide type has no example in the
  template, use the template layout with that name and its placeholders, and nothing else.
- Put text in the existing placeholders and text boxes. Don't add new text boxes, shapes or groups, except the
  emphasis devices in design rules §5 (one per slide) and arrows or brackets on code slides.
- Insert figures as single pictures at their own aspect ratio, with a credit line where the lesson gives one,
  and alt text.
- Make builds by duplicating the finished slide and changing one thing on each copy, never with PowerPoint
  animations or transitions.
- Write speaker notes for every slide (design rules §9).
- Delete the template's example slides when you're done.

Save the deck as the file name in the topic list's header. If you're writing the file with code, use
`python-pptx`, and copy slides by deep-copying the example slide's XML along with its picture relationships.

### 4. Check every slide

Render the deck to images (PowerPoint, LibreOffice or the PPTX skill's renderer) and look at every slide:

- Nothing overflows, overlaps or is cut off, and no text is below 16 pt except credit lines.
- Each slide matches its template example: same positions, fonts and colours.
- No slide breaks a "Never" rule (design rules §10).
- Builds line up: the parts that stay the same don't move between slides.

Fix what you find, then render again.

### 5. Report

Give me a short report:

- the slide count, and slides and minutes per topic row, next to the topic list's minutes;
- every `CONTENT NEEDED` or `FIGURE NEEDED` placeholder, and why;
- lesson content that was hard to present, as a suggested lesson edit (not a slide workaround);
- any design rule you couldn't follow, and why.
