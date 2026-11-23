---
name: build-assessment
description: Build or update the course's final assessment for a cohort - the learner page for Canvas (options, submission, README template, demo steps, rubric), the dry runs that check every option, the grader packet and scoring sheet for the demo event, the staff review checklist, and PDFs of the learner page and grader packet. Built locally and never committed. Use when asked to make, update or check the final assessment or its grader materials.
---

# Build the final assessment

The final assessment closes Module 4. Each learner picks one of several small, reproducible data-combining
tasks, submits code and a README in Canvas, and walks graders through it in a short live demo. Graders score
the demo; CUAHSI staff score reproducibility afterwards from the submission.
Read STYLE_GUIDE.md §3 (audience) and §11 first, and ask Lindsay for this cohort's dates, number of learners and
graders, and anything that changed since the last cohort. If a previous cohort's files exist, start from them.

## Inputs
- **Learning objectives of record:** each session deck's objectives slide (`teaching-materials/materials/slides/`),
  not the original objectives document.
- **What was taught:** the decks and notebooks (`teaching-materials/materials/notebooks/`, including
  `module_04_helpers.py`). Every step the assessment asks for must be taught there. This cohort can't see the
  website, so never point learners to lesson pages.
- **Logistics from Lindsay:** due date, peer-review date, demo date, certificate date, group sizes, who grades.

## Outputs (all in `teaching-materials/materials/assessment/`, git-ignored)

| File | Who it's for |
|---|---|
| `final-assessment_canvas.html` | Learners: the page pasted into Canvas's HTML editor |
| `final-assessment_learner-instructions.pdf` | Graders: the learner page, attached for context |
| `final-assessment_grader-key.md` → `final-assessment_grader-packet.pdf` | Demo graders |
| `final-assessment_scoring-sheet.xlsx` | Demo graders: one prefilled copy each |
| `final-assessment_staff-friday-review.md` | CUAHSI staff: the post-demo review |
| `dryrun-figures/*.png` | One dry-run figure per option, used in the grader packet |

Build the PDFs with `python teaching-materials/how-to-build/tools/assessment_pdfs.py teaching-materials/materials/assessment`
and the sheet with `teaching-materials/how-to-build/tools/assessment_scoring_sheet.ps1` (usage at the top of each).
Check the PDFs page by page: headings not stranded at a page end, tables and figures not cut.

## 1. Design the options
- **Eight options: four question types × two places**, each with a code (1A, 1B, 2A, …) so graders can say
  "so-and-so did 2B", peer review can pair similar options and demo groups can mix them. The 2026 types were:
  NWM forecast vs. USGS observations; SWOT vs. USGS (change, and absolute with a datum conversion); SWOT
  Raster extent at high flow; scaling in space (many gages/reaches) and in time (a long record).
- Each option needs **two federal products** and states **the products and the skills it tests**, tied to the
  deck objectives.
- **Timebox 4–5 hours** including demo prep, using only course materials. Say which options take longer.
- **Give every ID and time openly** (USGS site, COMID, SWORD reach and version, scene tile and date, UTM zone
  only where the option needs a distance or grid). **Answering the question is a bonus, never graded.**
- **Avoid the course's own example sites.** Use places not used in any session.
- **Product limits:** NWM v3.0 only (check `NWM_version_number` in the files: older events are v2.x) and only
  products the course taught (e.g. short range, not medium range or retrospective, unless taught). Check that
  SWOT passes have usable `reach_q`, that Raster scenes clearly cover the gage at the dates chosen, and that
  VDatum answers at a datum-conversion site (it fails in some tidal areas). Give a fallback offset with its date.
- Code snippets on the page only for steps the course didn't show; otherwise point to the session and notebook
  that did.

## 2. Dry-run every option
Do each option as a learner would, using only the course notebooks and `module_04_helpers.py`, in the course
environment (`open-water-data`). Record crest values and times, pass counts, offsets and anything confusing;
save one figure per option to `dryrun-figures/`. Swap any option that fails the limits above or doesn't fit the
timebox. Then run the `learner-reviewer` agent on the learner page and fix every Must fix. Also run an alignment
sweep. Every step must:
1. Support a deck objective.
2. Be taught in a deck or notebook.
3. Have obvious steps and outputs.

## 3. The learner page (`final-assessment_canvas.html`)
Canvas-pasteable HTML (inline styles only, tables with merged cells). Order:
1. Intro: what they do, the timebox, what's assessed; the answer is a bonus.
2. Dates table and certificate requirements.
3. **Choose one option:** a table of question | products | skills it tests | option code | place and period.
4. **What everyone does:**
   - What to submit in Canvas: code, environment and README. "Reproducible" means someone can run the code
     top to bottom and get the figure.
   - No credentials in code.
   - The README template: Figure, Data used (with versions and access dates), How I got it, How to reproduce,
     Limitations and strengths, Publishing plan.
   - The publishing plan: per dataset, a copy vs. download instructions plus a citation, and whether the
     product can change between downloads; plus the derived data to provide.
   - Peer review: for help, not grading.
   - **The demo:** at most 10 minutes, no slides, a walk through the notebook or script and README in rubric
     order, with minutes per step.
   - **The rubric.**
5. **Option details** at the bottom: IDs, times, "Your figure must show", "Watch for".

No demo logistics (shared at peer review).

**Rubric:** five criteria, scored 4 Exemplary → 1 Beginning; pass = average of all scores ≥ 3.0; no resubmissions.
1. Data selection
2. Data access and management
3. Combining products
4. Data characteristics and limitations
5. Reproducibility and provenance

Criteria 1–4 are scored in the demo (steps 1–4). Criterion 5 is scored by staff afterwards from the Canvas
submission. It covers whether the code reproduces with no credentials, and whether the publishing plan
correctly says which products can change.

## 4. The grader packet (`final-assessment_grader-key.md`)
Graders may not have taken the course but generally know the products. They need to grade by listening, with
little prep, so **everything they look for must be obvious and short.** Structure:
- Title, then *"Built by Claude and Lindsay Platt (CUAHSI)."*
- **Their role:** only the demo event; they score criteria 1–4; staff finalize grades afterwards (criterion 5).
  Read sections 1–2 beforehand (about 20 minutes); keep 3–5 open while grading; the learner instructions PDF is
  attached.

Then five sections:
1. **Course highlights (≤ 1 page):** what was taught per product (IDs, configurations, times, units, quality
   flags, access routes and alternatives), the combining skills, the helpers table (helper → what it wraps), and
   Module 1–2 practices.
2. **What learners were asked to do:** the demo steps table (step → what they cover → criterion), "the answer is
   a bonus", the pass rule.
3. **The rubric**, word for word from the learner page, criterion 5 marked as staff-scored.
4. **Grading live:**
   - one logistics paragraph (group size, blocks with a break, timing, screen-share trouble)
   - **How to score:** one table (criterion | 3 if they… | 4 if they also… | 2 or below if…)
   - "Questions are very rare"
   - **Is it their own work?** Five one-line flags (words don't match the code or figure; can't find their own
     steps; only reads; generic reasons; can't explain code shown). One flag is normal; flags go in Notes;
     flags in two or more criteria are reported to Lindsay.
   - **Scoring sheet:** "we'll send each of you a prefilled Excel sheet", with an example table of made-up
     learners.
5. **The options: examples of what a demo might show:** per option, the figure asked for; one line each for
   Data, Access, Combining, Limitation and Dry run (key numbers, common wrong results); the dry-run figure(s).
   Each option starts a new page in the PDF.

Keep it condensed: one-line bullets, no paragraphs explaining the rubric twice.

## 5. Scoring sheet and staff review
- **Scoring sheet:** columns Learner, Option, 1. Data selection, 2. Data access, 3. Combining, 4. Limitations,
  Notes; one row per learner; scores validated as whole numbers 1–4. Staff send each grader a copy prefilled
  with their group's learners and options.
- **Staff review** (`final-assessment_staff-friday-review.md`): steps per submission (fresh folder, course
  environment, run top to bottom, compare figure, read README) and the criterion 5 checks:
  - **Reproduces**
  - **No credentials**
  - **README complete**, with versions
  - **Publishing plan: provenance:**
    - USGS values can be revised, so keep a copy.
    - NWM archived forecasts are fixed per model version, so instructions plus a citation are enough.
    - SWOT is versioned, so either choice works with a reason.
  - **Derived data**, with file names

  Add what to do when an outside service is down (retry; don't penalize), scoring criterion 4 from the README
  for anyone who ran out of time, and following up on learners flagged in two or more criteria.

## 6. Introduce it in the last session's deck
Two slides via `/build-slides N update`:
1. The options table (question, products, skills), with the answer-is-a-bonus line.
2. What they hand in (Canvas submission, README with publishing plan) and the demo steps in rubric order.

Update the deck in place (memory: update reviewed decks in place).

## Report
Report to Lindsay in chat, not in a PR or issue (the files contain answers):
- the file paths
- the options with their dry-run results and any swaps
- the reviewer summary lines
- open decisions: dates, grader assignments, how scoring sheets come back

Commit only changes to this skill and the tools.
