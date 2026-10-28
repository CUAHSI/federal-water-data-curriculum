---
name: build-instructor-guide
description: Build or rebuild the instructor guide that gets a substitute or new instructor ready to teach the course, from the slides, learner bundle, lessons and open flags. Use when asked to make or update instructor prep material, or when check_stale.py lists the guide.
---

# Build the instructor guide

The reader is someone competent in Python and water science who has never seen this course and may teach a
session next week. Write for them. It's instructor-facing, so internal callouts and repo links are fine.
Build after the slides, readings, learner bundle and quizzes exist; read STYLE_GUIDE.md §11 first.

Output: `teaching-materials/instructor-guide/`

1. **`00_start-here.md`** (one page):
    - what the course is, who it's for, and the six objectives
    - the session map
    - where everything lives (website, repo, Canvas, HydroShare bundle, slides and readings, quizzes) and
      what pilot learners can and can't see (they get slides, readings, quizzes and the bundle, not the website)
    - who to ask about what (by role; Lindsay supplies the names)
2. **`01_prepare-to-teach.md`**: a checklist with time estimates.
    - **Two weeks out:** read the module's lessons; get the accounts (Earthdata Login, USGS API token); open
      the hosted environment.
    - **One week out:** run every notebook for your session, solutions included. Do each "Now you try it"
      yourself. Read the deck, its notes and its readings, and present the deck once to time it. Take the module quiz.
    - **Within 48 hours:** re-run the date-sensitive cells (list them, from the bundle's test results), and
      check Zoom, Canvas and the slide upload.
    - **On the day:** the order of windows to have open, a fallback if a data service is down (screenshots
      or saved outputs), and what to post in Canvas afterwards.
3. **`session-NN_<deck slug>.md`**, one per session:
    - the objectives covered, and the timing table (from the deck)
    - the key points per section (from the speaker notes)
    - the live-coding plan: notebook, sections, what to show, what usually goes wrong
    - "Now you try it", with the expected answer and common mistakes
    - likely questions with short answers, grounded in the lessons
    - known issues: open `TODO (dev team)` and `Partner review` callouts on these pages, open GitHub issues
      labelled for these lessons (`gh issue list`), and reviewer findings
    - the quiz: which module quiz, the objectives it covers (from its `_key.md`), and the questions learners
      most often miss (after the pilot, from Canvas reports)
    - the module reading (Modules 2–4 only): what's in it and when to post it in Canvas; the session's topic
      list (`teaching-materials/deck-prompts/topics/`) says what was left out of the deck and where it went
4. **`02_how-the-course-is-built.md`**: how content flows (lesson pages → skills → teaching materials), how to
   fix a mistake (edit the lesson, rebuild, check stale), and the review process.

## Rules
- Ground everything in the lessons, decks, notebooks and issues. Don't invent pitfalls; where you expect one
  but can't confirm it, mark it "(unverified)".
- Keep each session file to what fits on about 3 printed pages.
- Update `manifest.json` (`check_stale.py --update`) with the decks, notebooks and lesson pages each file was
  built from. Draft PR.
