---
name: build-slides
description: Build or rebuild a session's lecture slides (Quarto reveal.js with speaker notes) and its pre/post-session reading PDFs from the course lesson pages, fitted to the session's time. Use when asked to make, update or rebuild slides or readings for a session, or when check_stale.py lists one.
---

# Build session slides and readings

For pilot learners, the slides *are* the lessons: they meet with an instructor and can't open the website. You
turn the lesson pages into one deck per session. Lesson content the session can't cover goes into a short
pre- or post-session reading. The lessons are the source of truth: if a deck needs different content, change
the lesson (or flag it), then rebuild. Read STYLE_GUIDE.md first, especially §11.

## Inputs
- The session number. The session map in STYLE_GUIDE §11 says which pages it covers and how long it is.
- Those pages in toc order (`myst.yml`), plus the images they use (`images/…`) and `glossary.md` for
  definitions.
- For live-coding slides: the learner bundle's notebook names and section names (§11). If the bundle doesn't
  exist yet, use the names the §11 rules produce.

## Steps
1. **Prepare.** Make learner copies of each page with `teaching-materials/tools/prepare_learner_copy.py`, which
   drops internal callouts and internal course links and keeps external links. Note its counts for the PR.
2. **Plan the time before writing anything.** Make a table: lesson section → minutes → where it goes (in the
   session / pre-reading / post-reading).
    - Session 1 also needs a welcome, logistics (Canvas, quizzes, schedule, office hours) and environment
      setup (the hosted HydroShare environment and credentials).
    - Leave about 5 minutes for questions in every session.
    - Keep the total equal to the session length.
    - **Pre-reading** is background learners need first (definitions, context, account setup). **Post-reading**
      is depth, extra examples, best-practice FAQs and further reading. Keep each reading to about 15 minutes.
      Material is moved, not cut.
3. **Write the deck** at `teaching-materials/slides/<deck name from §11>`:
    - YAML: `format: revealjs` (`embed-resources: true`, `slide-number: true`) **and** `pptx`;
      `execute: enabled: false`; a title slide with the course, session, date and time (ET).
    - Slide 2: the session agenda with minutes. If there's pre-reading, slide 3 recaps it in 3 bullets.
    - **One idea per slide.** At most 6 bullets or about 40 words; a figure from `images/` wherever the
      lesson has one. Code: ≤ 12 lines, shown with ```` ```python ````, never run.
    - **Terms:** define a glossary term on the slide where it first appears (from `glossary.md`), since
      learners have no glossary to click.
    - **Shared framework:** in data-product sessions, show the shared-concepts table (STYLE_GUIDE §1) for that
      product.
    - **Live coding** (§11 limits): a slide titled "Live coding: <what>" naming the notebook file, the
      sections to run, 2–3 things to point out, the minutes, and "back to slides at …".
    - **Now you try it:** a slide with the task as learners will see it, and the notebook cell to use.
    - Final slides: a recap (3 bullets), what's due (the module quiz: "see Canvas"), and the readings by file
      name.
    - **Speaker notes** (`::: notes`) on every slide: 2–5 bullets of points to make, not a script. Add
      "Expect:" with a likely question where there is one, and "If short on time:" where something can be
      skipped.
4. **Write the readings** (only if the plan put content there) at
   `teaching-materials/readings/<deck name>_pre-reading.qmd` and `_post-reading.qmd`:
    - `format: typst`; a title with the course, session and "Read before/after the session"; one line on why
      it matters.
    - The moved lesson sections, from the learner copies, lightly edited to stand alone. Keep headings, figures
      (with captions) and code as shown; keep external links. Add a short "Key terms" list if the section uses
      glossary terms.
5. **Render and check:**
    - `quarto render <deck> --to revealjs` and `--to pptx`; `quarto render <reading>` to PDF.
    - Fix overflowing slides.
    - Count the slides: about 1.5–2 minutes per content slide is a sanity check against the timing table.
6. **Record:** update `teaching-materials/manifest.json` for the deck and each reading
   (`check_stale.py --update`), with all source pages and images as `sources`.
7. **Report in the PR:**
    - the timing table
    - what went into each reading
    - the slide count
    - the callout and internal-link counts from step 1
    - any lesson content that was hard to present (a candidate lesson edit, not a slide workaround)

## Rules
- External links are fine. No links to other course pages, the glossary, the References page or the repo;
  no `TODO (dev team)` or `Partner review` content.
- Don't invent claims, numbers or code that aren't in the lessons. If a slide needs something the lesson
  lacks, list it as a lesson gap in the PR report, not on the slide.
- Agency order NASA → NOAA → USGS (STYLE_GUIDE §1); WDFN naming.
- Rebuilds: regenerate from the lessons, but keep any slide marked `<!-- keep -->` as it is (a human edit to
  preserve), and say so in the report.
