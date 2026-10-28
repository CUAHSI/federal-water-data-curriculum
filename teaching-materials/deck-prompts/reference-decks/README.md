# reference/: your template and example decks

Everything in this folder except this README is git-ignored. Your decks stay on your machine and aren't
published with the course repo.

## What to put here

1. **`template.pptx`** (or `template.potx`): the most important file. Make it from one of your own decks:
   1. Open a recent deck in your usual style (the course lead used the 2026 Data Publishing cohort deck).
   2. **Save As** `template.pptx` in this folder.
   3. Delete slides until exactly **one example of each slide type** in `../design-rules.md` §4 is left: session
      title, program schedule, lingering questions, goals for today, content (one with a figure, one text-only),
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
| `template.pptx` | DECIDE: made from … |
| | |

## Why a template made from real slides

The generator copies your example slides and replaces their content, so every position, font, colour and
emphasis comes from something you made. That keeps the decks looking like yours: it doesn't build slides up
from shapes, which is what makes generated decks look generated.
