# Module 1 quiz: answer key (instructors only)

Quiz: `module-01_quiz_data-best-practices.txt` (QTI: `.zip` of the same name). 12 questions, one point each,
3 "select all that apply". No code. About 12–14 minutes.

Answers are shuffled in Canvas (`shuffle answers: true`), so the letters below are the order in the `.txt` source,
not what learners see.

## Canvas setup after import

`text2qti` 0.8.0 always writes one allowed attempt into the QTI file, and that can't be changed from the `.txt`.
After importing the zip, set **Allowed attempts** to Unlimited and **Score to keep** to Highest (the zip already
sets highest), so the quiz matches its description. Check that code blocks, ³ superscripts and ≤ display, and that
both feedback lines show after an attempt.

## Objective coverage

Module objectives (from `01-data-best-practices/00_introduction.md`), using the five sub-objectives:

| Objective | Taught in | Questions |
|---|---|---|
| O1. Describe open science as a spectrum covering products and processes; definitions vary | Open Science (intro; Putting open science into practice) | 1, 2 |
| O2. Explain FAIR, how FAIR differs from open, and why CARE is a check on data sources | Open Science (FAIR and CARE; Now you try it); Data Publishing (FAIR in action) | 3, 4 |
| O3. Explain reproducibility vs. replicability, and reproducibility as a continuum | Data Management (Reproducibility techniques) | 5, 6 |
| O4. Apply project organization, machine-readable data and documentation | Data Management (Improving data management with three simple approaches; Now you try it) | 7, 8, 9 |
| O5. Choose a repository; publish derived data as a snapshot or a recipe | Data Publishing (Water domain repositories; Publishing derivative data; Now you try it) | 10, 11, 12 |

## Answers

| Q | Objective | Type | Correct answer | Lesson section |
|---|---|---|---|---|
| 1 | O1 | single | b) It also covers how the work is done, such as sharing work in progress | Open Science, intro |
| 2 | O1 | select all | Public repository during the project; peer code review in progress; data and code as citable products | Open Science, Putting open science into practice |
| 3 | O2 | single | b) Largely FAIR, but not fully open | Open Science, FAIR and CARE; Now you try it (dataset 3) |
| 4 | O2 | single | c) Check the terms attached to the data and the CARE guidance before using or sharing | Open Science, FAIR and CARE |
| 5 | O3 | single | a) First reproducible, second replicable | Data Management, What do we mean by "reproducible"? |
| 6 | O3 | single | b) Version control and reusable functions | Data Management, continuum of reproducibility figure and text |
| 7 | O4 | single | c) TRUE/FALSE storm column, numeric discharge, site notes in a separate file | Data Management, 2. Machine-readable data |
| 8 | O4 | select all | Raw data untouched with corrections in code; outputs named after scripts; README with run order | Data Management, 1. Project organization; 3. Documentation; Now you try it |
| 9 | O4 | single | c) `regression_model_v1.py` makes `2024-08-18_regression_model_v1_output.csv` | Data Management, 1. Project organization |
| 10 | O5 | single | d) HydroShare | Data Publishing, Comparison of two water-specific repositories; Introduction to HydroShare |
| 11 | O5 | single | a) Subset of a versioned satellite archive with a collection DOI (recipe) | Data Publishing, Publishing derivative data; Now you try it |
| 12 | O5 | select all | Check the license; record version, retrieval date and processing; make the product distinct from the original | Data Publishing, Publishing derivative data |

## Notes for spot-checking

- Q5 uses The Turing Way's two-by-two wording (same analysis and data: reproducible; same analysis, different data:
  replicable). The course's broader working definition of reproducibility is consistent with this.
- Q10's distractor about generalist repositories is wrong only in its reason (most field-specific metadata). The
  lesson stresses that a generalist choice is "not a lesser one".
