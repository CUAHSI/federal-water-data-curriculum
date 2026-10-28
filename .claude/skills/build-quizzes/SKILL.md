---
name: build-quizzes
description: Draft or rebuild the module quizzes (one per module, multiple choice with some select-all-that-apply, aligned to the module's learning objectives) as text2qti files and QTI zips for Canvas New Quizzes. Use when asked to make or update quizzes, or when check_stale.py lists a quiz.
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
1. **Coverage plan first.** A table: objective → the lesson sections that teach it → the number of questions.
   Every objective gets at least 2 questions. Weight objectives by how much of the module teaches them.
2. **Length:** 10–12 questions, so it takes 10–15 minutes. A question with code counts as about 2 minutes.
3. **Questions test concepts and judgement, not recall of trivia.**
    - **Use:** applying an idea to a new case, interpreting an output, choosing an approach for a scenario,
      reading a quality flag, spotting an error in a short code snippet ("Which line causes the error?").
    - **Don't use:** a value only memorisation would answer (exact IDs, version numbers, URLs); "all/none of
      the above"; trick wording; negatives unless bolded (**not**).
    - Code in questions: ≤ 10 lines, from or closely modelled on the lessons, never needing to be run. Use
      fenced code blocks.
4. **Question types:** mostly single-answer (`a)` / `*b)`). Use "select all that apply" (`[*]` / `[ ]`) for
   2–3 questions per quiz, where the concept really has several correct parts (e.g. which practices support
   reproducibility). Say "Select all that apply." in the question, use 4–5 options with 2–3 correct, and make
   sure each option is clearly right or wrong on its own.
   **Options:** for single-answer questions, 4 per question, one clearly correct. The three distractors are plausible misconceptions a
   learner might actually hold (from the lessons' caveats and best-practice sections). Options should be of
   similar length and in a logical order (numbers ascending, agencies NASA → NOAA → USGS).
5. **Feedback on every question** (for select-all, the feedback names every correct option): a general `...` line that explains why the correct answer is right, in 1–2
   sentences that teach. Add a `-` line where a distractor reflects a common misconception worth naming.
6. **Self-contained:** no links to the course website or repo; external links only if essential. No
   `TODO`/`Partner review` content. Module 3 questions use the course's example rivers, but never the
   Module 4 case study.

## Files
- Source: `teaching-materials/materials/quizzes/module-NN_quiz_<module-slug>.txt` in `text2qti` format:
    - title `Module N Quiz: <module title>`
    - a description: "About 10–15 minutes. Unlimited attempts; your highest score counts. The correct answer
      and an explanation are shown after each attempt."
    - `shuffle answers: true` if the installed `text2qti` supports it (check `text2qti --help` or its docs)
    - one point per question
- Build: `text2qti <file>.txt` → `<file>.zip` (commit both). Fix any parse errors.
- Key: `teaching-materials/materials/quizzes/module-NN_quiz_<module-slug>_key.md`, containing the coverage table plus,
  per question, its objective, the correct option and the lesson section it draws on. It's for spot-checking
  and for the instructor guide.

## Review before the PR
Re-read each question as the target learner (STYLE_GUIDE §3):
- Is it answerable from the session plus its readings alone?
- Is exactly one option defensible (or, for select-all, is each option clearly right or wrong)?
- Does the feedback teach?

Run `learner-reviewer` on the quiz files if time allows.

## Record and report
Update `manifest.json` for each `.txt` and `.zip` (`check_stale.py --update`), with the overview, lesson pages
and deck as `sources`. The PR reports the coverage tables, question counts, estimated minutes per quiz, and
anything you couldn't test because the lessons don't teach it clearly (a lesson gap).
