---
name: build-notebooks
description: Build or update a session's notebooks (one per Module 3 and 4 lesson with code, with the "Now you try it" example answer collapsed under each starter) and the one course environment file, for HydroShare, from the lesson and the session's deck, using teaching-materials/how-to-build/notebook-prompt.md. Notebooks are built locally and never committed. Run after build-slides. Arguments - a session number (3–6), or "N update".
---

# Build a session's notebooks

The prompt and the lesson notes live in `teaching-materials/how-to-build/notebook-prompt.md`; read it and
`how-to-build/guide.md` first. This skill runs the same prompt a person would paste into Claude, with the setup
done for them. The lessons are the source of truth. If a notebook needs different content, change the lesson
(or flag it), not the notebook.

## Build (`/build-notebooks N`)

1. **Check the inputs.**
    - The session has a notebook: sessions 3, 4 and 5 have one each, session 6 has two (the table at the top
      of the prompt). Sessions 1 and 2 have none: say so and stop.
    - `python teaching-materials/how-to-build/tools/check_topics.py N` passes.
    - **The session's deck exists** in `teaching-materials/materials/slides/` (the file name in the topic
      list's header). If it doesn't, stop and say to run `/build-slides N` first: the notebook is written
      around the deck's live-coding slides and leaves out what the deck explains.
    - The course environment `open-water-data` exists with papermill (`guide.md`, "Before you build"), and the credentials
      the lesson notes list are set.
2. **Make a learner copy** of the lesson page with `prepare_learner_copy.py`, into a scratch directory outside
   the repo. Note the counts for the report.
3. **Read the deck** with `python-pptx` (in a scratch environment, never a lesson environment): every slide's
   title, text, speaker notes, and the Comments property.
4. **Follow the Build prompt** in `notebook-prompt.md` for each of the session's notebooks.
    - After step 2 of the prompt (the plan), stop and show it unless the user said to go straight through.
    - Run `python teaching-materials/how-to-build/tools/merge_environments.py` to write the course
      environment. If its packages changed, update `open-water-data` from it before testing.
    - Test with papermill in `open-water-data`, from a short working folder (`--cwd`, e.g.
      `%LOCALAPPDATA%\Temp\fwr\<notebook>`): SWOT file names overflow Windows' 260-character path limit in deep folders.
5. **Save, don't commit.** Notebooks and `environment.yml` live in `teaching-materials/materials/notebooks/`,
   which is git-ignored: never commit them or add them to `manifest.json`. The notebook's `fwdc` metadata records
   the build commit and the deck. Commit only changes to the prompt, the lesson notes or this skill.
6. **Report** (to the user, and in a PR if there is one): the prompt's report, the learner-copy counts, and the
   cells you'd most like a person to look at.

## Update (`/build-notebooks N update`)

Use this when the session's notebook already exists, after a lesson, topic-list or deck change. Default to it
whenever a notebook exists and the user asks to "rebuild", and say so.

1. Check the inputs as for a build.
2. Make a learner copy and read the deck.
3. Follow the **Update** prompt. Stop after its plan unless the user said to go straight through. Never change
   cells tagged `keep`; never overwrite the file in `how-to-build/to-update/`.
4. Save and report as for a build, with the prompt's change log.

## Rules
- Only content from the lesson page and the lesson notes: no invented claims, numbers, code or links.
- No internal course links or repo links; no `TODO (dev team)` or `Partner review` content.
- Credentials only from environment variables or prompts at run time. Never write real values into a notebook,
  a file or the output, and clear outputs before saving.
- When a fix in the lesson notes is no longer needed because the lesson was fixed, delete it from the notes.
