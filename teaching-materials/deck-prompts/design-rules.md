# Design rules for the session decks

These rules describe how the course decks look and move. They were seeded from Lindsay's own decks (the 2025–26
Data Publishing cohort sessions and her 2024–26 conference talks; see "Where these rules came from" at the end).
Every rule is editable.

The aim is a deck that looks like a person built it in PowerPoint: simple slides, one idea each, real figures
and screenshots, and emphasis that does one job. It should never look assembled from decorative parts.

## 1. The template does the styling

- Build every deck from the course template (`reference-decks/template.potx` or `.pptx`; see the README). Use the
  template's **slide layouts and placeholders** for titles, body text, pictures and section slides.
- Don't restyle what the template already defines (fonts, title position, bullet style, colours). If a slide
  needs a look the template lacks, list it in the build report rather than inventing a style.
- Slide size: the template's (16:9; the current template, from a Google Slides deck, is 10 × 5.63 in).

## 2. Colours

Taken from the cohort decks (which share their palette with the talks):

| Role | Colour | Where it's used |
|---|---|---|
| Primary dark | slate `#32475A` | header bars, section/activity/question slide backgrounds, title tabs |
| Text on dark | white `#FFFFFF` | all text on slate or black slides |
| Body text | black `#000000` or dark grey `#3F3F3F` | text on white slides |
| Highlight | green `#00B66C` | the "swoosh" underline under a key word, "UP NEXT", the outline around the current item |
| Secondary | teal `#009F9D` or blue `#2787C0` | link text, a term being defined, a second highlight when one isn't enough |
| "Don't" / problem | dark red `#C00000` (code examples `#980000`) | bad examples, warnings, the "before" in before → after |
| "Do" / fixed | dark green `#274E13` | the "after" in before → after, good examples |
| Pointer | orange `#E97132` | arrows and outline circles that point into a screenshot or figure |

## 3. Type

- Titles and body come from the template. 
- Font: Use **Arial** with **Lato** on the title and schedule slides. When in doubt, default to whatever the template uses.
- Code: **Courier New** (or Aptos Mono), shown on a black background, terminal style, with white text, as on the
  template's code slide.
- Sizes: titles 32–40 pt; body 20–24 pt; never below 16 pt for text the audience must read. Small grey text
  (11–12 pt) is only for image credits and source lines at the bottom of a slide.
- Sentence case for titles ("What makes your data FAIR?"), not Title Case.
- Key words in a sentence are **bold**, not coloured. Italics mark the turn in a statement ("Most of them
  *ignore* it.") and activity prompts.

## 4. Slide types

Use these, and only these. Each maps to a template layout (the layout names are the template's own; list them
in `reference-decks/README.md` once the template exists).

1. **Session title.** Landscape photo banner, CUAHSI logo, session title and subtitle, date, presenter name,
   title and photo.
2. **Program schedule.** Slate panel on the left ("Pilot Program Schedule" + month). On the right, every session
   with its icon and date. Past sessions are greyed out; today's session has a green rounded outline and "UP
   NEXT" in green. Shown near the start of every session; the outline moves each time.
3. **Lesson objectives.** Slate, "Learning objectives for today", one icon on the left, the session name in
   bold, then the module's **main** learning objectives (the list before "These break down into"), copied
   word for word from its overview page (`0N/00 § Learning objectives`). This is the only place in the deck the
   objectives appear: overview slides don't repeat them. Sessions 3–5 each show their lesson's version of the
   Module 3 objectives (the other two products removed), written out in the topic list.
4. **Content.** White, title top-left (or white title on a slate header bar), at most 6 bullets or about 40
   words, one figure or screenshot where the lesson has one.
5. **Statement.** Black or slate background, one or two sentences in white, centred. Used to open a section or
   make one point land.
6. **Section divider.** Solid slate (or green/blue for a change of pace) with a large bold white title. A small
   recurring graphic (like the reproducibility pyramid) may come back on each divider of a series.
7. **Activity.** Slate, "Activity #N" large and bold, then the task with its time ("Take ~7 minutes to …"),
   numbered or bulleted steps, and a screenshot if learners need to find something.
8. **Live coding.** Slate, like an activity: "Live coding: <what>", the notebook file name, the sections to run,
   2–3 things to point out, and "Back to slides at <clock time>".
9. **Code.** One code block of at most 12 lines, terminal style (section 3). Arrows or brackets in accent
    colours can connect parts of the code to what they produce.
10. **Before → after.** The problem on the left in dark red, an arrow, the fix on the right in dark green.
    Works for file names, column layouts and code.
11. **Further reading and questions.** A content slide (type 4) titled "Further reading" with the lessons'
    external links. The speaker opens the floor for questions while it's up; there is no separate questions
    slide.

**How a session ends:** recap, what's due, further reading and questions, then (only when there is one) the
"before the next session" slide as the very last slide, so it's what learners leave with.

## 5. Emphasis: one device at a time

Use one of these per slide, and only to point at something the speaker is talking about:

- the green swoosh underline under one key word of a title;
- **bold** key phrases inside a sentence;
- a hand-drawn-style outline (ellipse or rounded rectangle, no fill, 2–3 pt line, orange, red or green) around
  part of a screenshot, table or figure;
- a single arrow pointing at something;
- greying out everything except the item being discussed.

## 6. "Animation" is a sequence of slides

- **No PowerPoint animations and no slide transitions.**
- To build up an idea, duplicate the slide and change one thing on each copy, keeping the title and everything
  else in exactly the same place. Patterns from Lindsay's decks:
  - **Reveal:** add one bullet, one code example or one panel per slide (the "Key takeaways" sequence in the
    cohort deck: same title and takeaways, one more example each slide).
  - **Overlay:** put a sticky note or label on top of an earlier slide to add a second layer of meaning
    ("Human readable" over Findable/Accessible).
  - **Spotlight:** the same image, first plain, then with one region highlighted, then darkened with a title
    over it.
  - **Move the outline:** the same table or schedule with the highlight moved to the next item.
  - **Grow a figure:** a definition first, then the same slide with the figure that extends it ("Reproducibility"
    → "Reproducibility v2.0" → with the continuum pyramid).
- A build sequence counts as one idea for pacing (section 8), however many slides it takes.

## 7. Visuals

- Prefer **real** visuals: the course figures in `images/`, screenshots of the tools and portals (Earthdata
  Search, HydroShare, the WDFN pages), and credited illustrations (for example The Turing Way's Scriberia
  illustrations, CC-BY).
- Insert a figure as one picture at its own aspect ratio; never stretch or crop away axes or credits.
- Every borrowed image gets a credit line (small grey text, bottom of the slide) and alt text.
- Simple diagrams are fine when Lindsay's decks use the same kind: a few labelled boxes with arrows, a
  four-panel grid, a pyramid. If a slide needs a diagram the lessons don't provide and it can't be drawn that
  simply, put a placeholder on the slide ("FIGURE NEEDED: …") and list it in the build report.

## 8. Pacing and density

From Lindsay's decks:

- Talks run at about **one slide a minute** (18–22 slides for a 15–20 minute talk); the cohort sessions, which
  mix teaching with activities and demos, run at about **2–3 minutes a slide**.
- Median words per slide: about 20–35 in talks, about 40 in the cohort sessions. Keep most slides under 40 words
  and no slide over 70, except activity instructions.
- Two-thirds or more of slides carry a picture.
- Each block of new concepts ends in something learners do: an activity, a live-coding switch or a question.
- The minutes in the topic list are the budget. A topic with 3 minutes gets about 1–2 ideas, so 1–4 slides
  counting builds.

## 9. Speaker notes

- Every slide has notes: 2–5 bullets of points to make, not a script.
- A slide whose notes start with `KEEP` is a human edit to preserve: updates never change, move or remove it.
- Add "Expect:" with a likely question where there is one, and "If short on time:" where a slide or build can be
  skipped.
- On live-coding and activity slides, put the clock time to come back.

## 10. Never

These are the habits that make a deck look machine-made. Don't:

- build a visual by layering shapes (cards behind text, circles behind icons, overlapping translucent panels);
- use rows of icon-plus-caption "cards", or icons as decoration (an icon is fine only where a template layout
  has one, like the schedule and objectives slides);
- add gradients, drop shadows, glows, 3-D effects or rounded "pill" labels that only decorate;
- put emoji anywhere;
- add "key stat" call-outs with giant numbers, unless the number is the point of the lesson section;
- fill empty space for its own sake: white space is fine;
- add a summary box or "Key takeaway" banner to every slide (a takeaway is its own slide, or the recap);
- make up content, numbers, quotes or figures that aren't in the lesson pages.

## Where these rules came from

Looked at in October 2026 (local copies, not in the repo):

- Cohort teaching decks: `260518_lplatt&kwong_DataPubCohort.pptx` (79 slides) and the November 2025 pilot PDFs
  (`251110_…FileUpload`, `251112_…READMEs`, `251120_…FinishingStrong`). Source of the session structure, slide
  types 1–3 and 7, the slate/green palette and the build sequences.
- Talks: `260624_lplatt_TBEP_PracticalOpenScience.pdf`, `250313_lplatt_NMC_reproducibility_slides.pptx`,
  `250329_…ASLO…`, `241212_…AGU_opensci.pptx`, `240624_…WaterSciCon24…`, `250605_…UCOWR_DataBestPractices.pdf`,
  `250930_…WhatIsTargets.pptx` and others. Source of the statement slides, swoosh underline, outline highlights,
  code slides, before → after and the pacing figures.
- Measured with `python-pptx`: words per slide, share of slides with pictures, fonts, colours, and runs of
  same-titled slides (the builds).
