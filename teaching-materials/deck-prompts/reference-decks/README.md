# reference-decks/: your template and example decks

Everything in this folder except this README is git-ignored. Your decks stay on your machine and aren't
published with the course repo.

## What to put here

1. **`template.pptx`** (or `template.potx`): the most important file. To make one from your own deck by hand:
   1. Open a recent deck in your usual style (the course lead used the 2026 Data Publishing cohort deck).
   2. **Save As** `template.pptx` in this folder.
   3. Delete slides until exactly **one example of each slide type** in `../design-rules.md` §4 is left: session
      title, program schedule, goals for today, content (one with a figure, one text-only),
      statement, section divider, activity, live coding (copy the activity slide and retitle it), code,
      before → after, final questions.
   4. On each example slide, type the slide type in the speaker notes (for example `TYPE: activity`), so the
      generator knows which is which.
   5. Remove anything that shouldn't be reused: other presenters' photos, old dates, talk-specific logos.
      Leave the CUAHSI branding, the schedule slide's icons and your own photo for the title slide.
2. **Two or three example decks** (`.pptx` or `.pdf`) that show your pacing and how you build ideas up across
   slides. Teaching decks are better than conference talks.

Then list the files here so others know what you used (names only):

| File | What it is |
|---|---|
| `template.pptx` | Made from `260518_lplatt&kwong_DataPubCohort.pptx` by `make_template.py` (October 2026), then edited by hand. 14 example slides, each tagged `TYPE: …` in its notes |
| `make_template.py` | The script that made the first version of the template (needs `python-pptx`); only useful to start over |
| `260518_lplatt&kwong_DataPubCohort.pptx` | 2026 Data Publishing cohort sessions: the session structure, activities and builds |
| `251112_Slides_LPlatt_Wk2_ConfigContent_READMEs.pdf` | 2025 pilot cohort, week 2: a full teaching session |
| `250313_lplatt_NMC_reproducibility_slides.pptx` | Conference talk: statement slides, highlight outlines, code |
| `260624_lplatt_TBEP_PracticalOpenScience.pdf` | Most recent talk (2026): statement slides, spotlight and grow-a-figure builds |

## Why a template made from real slides

The generator copies your example slides and replaces their content, so every position, font, colour and
emphasis comes from something you made. That keeps the decks looking like yours: it doesn't build slides up
from shapes, which is what makes generated decks look generated.
