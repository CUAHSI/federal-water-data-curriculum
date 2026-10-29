---
name: build-quizzes
description: Draft or rebuild the module quizzes (one per module, multiple choice with some select-all-that-apply, aligned to the module's learning objectives) as text2qti files and QTI zips for Canvas New Quizzes. Quizzes are built locally and never committed. Use when asked to make or update quizzes.
---

# Build module quizzes

One formative quiz per module, for Canvas (issue #32): low stakes, unlimited retakes, and the correct answer
always shown with an explanation. Grading is automatic, so every question is multiple choice: mostly single
answer, with a few "select all that apply" questions mixed in.
Read STYLE_GUIDE.md §11 and the module's overview page first.

## Inputs
- The module's learning objectives (top of its `00_introduction.md`).
- The module's lesson pages (learner copies via `prepare_learner_copy.py`) and the session deck(s), so
  questions only ask about what learners were taught.

## Design
1. **Start from the objectives, not the lessons.** The quiz measures whether learners met the module's
   learning objectives. Use the main objectives ("By the end of this module, learners should be able to"); the
   "These break down into" list shows how the lessons teach them, not separate targets. For each main
   objective, write down what a learner who has met it can do (e.g. "decide whether a dataset is FAIR, open,
   both or neither"), then write questions that ask them to do that.
    - Every question tests one objective directly. If answering it mainly depends on remembering a smaller
      point, a named framework, a figure or a lesson's example (e.g. where a practice sits on a diagram), cut it
      or rewrite it around the objective the point supports.
    - Test an idea with a new example, not the one the lesson used to teach it. If the lesson shows a
      spreadsheet with storm days shaded blue, ask about a different spreadsheet with different problems. The
      course's example rivers and code modelled on the lessons can still be the setting.
    - Test the general idea, not a comparison of specific named tools, services or organizations, unless the
      objective names them. Ask why you'd choose a domain repository over a generalist one, not HydroShare vs.
      EDI. In Modules 2–4 the three agencies' products are what the objectives name, so naming them is fine.
    - Keep each question in its own module's objective. Module 2 characterizes each product on its own, so its
      questions stay with one product at a time (a select-all question can mix products if each option is about
      one). Questions that compare products (units, vertical references, which one gives hourly values) belong
      in Module 4.
2. **Coverage plan.** A table: objective → what a learner who meets it can do → the lesson sections that teach
   it → the number of questions. Every objective gets at least 2 questions, spread roughly evenly; give an
   objective more only when it has several distinct skills to test.
3. **Length:** 10–12 questions, so it takes 10–15 minutes. A question with code counts as about 2 minutes.
4. **Questions test concepts and judgement, not recall of trivia.**
    - **Use:** applying an idea to a new case, interpreting an output, choosing an approach for a scenario,
      reading a quality flag, spotting an error in a short code snippet ("Which line causes the error?").
    - **Don't use:** a value only memorisation would answer (exact IDs, version numbers, URLs); "all/none of
      the above"; trick wording; negatives unless bolded (**not**).
    - Code in questions: ≤ 10 lines, from or closely modelled on the lessons, never needing to be run. Use
      fenced code blocks.
5. **Question types:** mostly single-answer (`a)` / `*b)`). Use "select all that apply" (`[*]` / `[ ]`) for
   2–3 questions per quiz, where the concept really has several correct parts (e.g. which practices support
   reproducibility). Say "Select all that apply." in the question, use 4–5 options with 2–3 correct, and make
   sure each option is clearly right or wrong on its own.
   **Options:** for single-answer questions, 4 per question, one clearly correct. The three distractors are plausible misconceptions a
   learner might actually hold (from the lessons' caveats and best-practice sections). Options should be of
   similar length and in a logical order (numbers ascending, agencies NASA → NOAA → USGS).
6. **Feedback on every question** (for select-all, the feedback names every correct option): a general `...` line that explains why the correct answer is right, in 1–2
   sentences that teach. Add a `-` line where a distractor reflects a common misconception worth naming.
7. **Self-contained:** no links to the course website or repo; external links only if essential. No
   `TODO`/`Partner review` content. Module 3 questions use the course's example rivers, but never the
   Module 4 case study.

## Files
- Source: `teaching-materials/materials/quizzes/module-NN_quiz_<module-slug>.txt` in `text2qti` format:
    - title `Module N Quiz: <module title>`
    - a description: "About 10–15 minutes. Unlimited attempts; your highest score counts. The correct answer
      and an explanation are shown after each attempt."
    - `shuffle answers: true` if the installed `text2qti` supports it (check `text2qti --help` or its docs)
    - one point per question
- Build: `text2qti <file>.txt` → `<file>.zip`. Fix any parse errors.
- Key: `teaching-materials/materials/quizzes/module-NN_quiz_<module-slug>_key.md`, containing the coverage table plus,
  per question, its objective, the correct option and the lesson section it draws on. It's for spot-checking
  and for the instructor guide. Its first lines record `Built from <short commit>` and the build date. Build on
  an `upstream/dev` commit (one that's already pushed), so anyone can later check whether the lessons changed
  since, e.g. `git diff abc1234 HEAD -- 03-federal-water-data-access-retrieval`.
- The key ends with the "In Canvas after import" checklist below.
- **Save, don't commit.** `teaching-materials/materials/quizzes/` is git-ignored, like the slides and readings:
  quiz questions and answer keys never go into the repo, a PR, an issue or `manifest.json`. Commit only changes
  to these instructions.
- Keep all three files (`.txt`, `.zip`, `_key.md`) together in `teaching-materials/materials/quizzes/`. Canvas can't give
  back the `.txt`, so to update a quiz someone else built, get the three files from them first.

## In Canvas after import
Import each `.zip` into the module's Canvas course as a QTI package (Settings → Import course content →
QTI .zip file); it arrives as a New Quiz. Then check, and set by hand where needed:
- **Allowed attempts:** Unlimited. The installed `text2qti` (0.8.0 at the time of writing) always writes one
  attempt into the zip, so this always needs changing.
- **Score to keep:** Highest.
- **What students see after an attempt:** their responses, the correct answers and the feedback, as the quiz
  description promises.
- **Shuffle answers** is on, each question is worth one point, and code blocks, superscripts and the general
  and incorrect-answer feedback display.
- Any course-wide passing score for the module (issue #32) is set as decided for the course.

## Review before handing over
Re-read each question as the target learner (STYLE_GUIDE §3):
- Does it test an objective directly? Would a learner who met that objective, but doesn't remember this
  particular example or detail, get it right?
- Is it answerable from the session plus its readings alone?
- Is exactly one option defensible (or, for select-all, is each option clearly right or wrong)?
- Does the feedback teach?

Run `learner-reviewer` on the quiz files if time allows.

## Report
Report in your Claude Code chat or directly to Lindsay, not in a PR or issue (they're public; unlike decks,
whose report can go in a PR): where the files were saved, the build commit,
question counts, estimated minutes per quiz, the reviewers' summary lines, and anything you couldn't test
because the lessons don't teach it clearly (a lesson gap). Lesson gaps can go in a PR or issue, as long as
they don't quote or give away quiz questions.

## Update
To update a quiz after lesson changes, run `git diff <built-from commit> HEAD -- <module folder>` with the
commit from the key. A changed deck or reading for that module can also call for a quiz review. Revise only the
questions those changes affect, rebuild the zip, record the new commit in the key. In Canvas, import the new zip as a new quiz and work through the checklist above; if learners have
already taken the old one, ask Lindsay before unpublishing or deleting it, since that affects their scores.
