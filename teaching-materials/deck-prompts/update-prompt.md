# Prompt: update an existing deck

Use this instead of `deck-prompt.md` when you already have a deck for the session and want it brought up to
date, not rebuilt: a deck you made by hand, an earlier course's deck, or a committed deck whose lessons changed.
Copy everything below the line into Claude, replacing `{N}` with the session number. In Claude Code,
`/build-slides N update` does the same thing.

---

You are updating the slide deck for **Session {N}** of *Reproducible Workflows with Open Water Data: NASA,
NOAA, USGS River Data Access*, a CUAHSI course for researchers and graduate students who know some Python but
are new to federal water data APIs. The deck already exists and the instructor likes it. Change only what needs
changing, and leave everything else exactly as it is.

## Inputs

1. **The deck to update:** the `.pptx` for this session in `teaching-materials/deck-prompts/decks-to-update/`.
   If there's none there, the committed deck in `teaching-materials/slides/` (the file name in the topic list
   header).
2. **Topic list:** `teaching-materials/deck-prompts/topics/session-0{N}.md`: what the deck should cover, in what
   order, and for how many minutes.
3. **Lesson pages:** the learner copies of the pages the topic list names. They are the only source of content.
4. **Figures:** the files in `images/` that the topic list and the pages name.
5. **Design rules:** `teaching-materials/deck-prompts/design-rules.md`, for slides you add or change.
6. **Template:** `teaching-materials/deck-prompts/reference-decks/template.pptx`, only for a new slide whose type
   the deck doesn't already have.

## Rules

- **Slides whose speaker notes start with `KEEP` are never changed, moved or removed.** Report them as kept.
- The content rules in `deck-prompt.md` apply to everything you add or change: only lesson content, the course's
  exact name, objectives exactly as the topic list gives them, no internal links or internal notes, NASA → NOAA →
  USGS, "WDFN" not "NWIS".
- Don't restyle slides you aren't otherwise changing, even if they break a design rule; list those in the report
  instead.

## Steps

### 1. Inventory the deck (no changes yet)

List every slide: number, title, slide type (design rules §4, or "other"), which topic-list row it covers (or
"none"), and whether it's marked `KEEP`.

### 2. Compare and plan, then stop

For each slide, decide:

- **keep:** matches the topic list and the lessons;
- **update:** right topic, but its content differs from the lesson (changed numbers, names, code, figures,
  dates), or the course name, session dates or schedule are out of date;
- **move:** right content, wrong place in the topic list's order;
- **remove:** covers a topic that isn't a `deck` row any more.

Then list the `deck` rows with no slide (**add**), and compare each row's slides with its minutes.

Show me the plan as a table: slide number, title, action, and for updates what changes and why (quote the lesson
line it now follows). Wait for my go-ahead before changing anything. I may keep slides you'd remove.

### 3. Make the changes

Work on a copy of the deck:

- **Update** text in the existing text boxes and placeholders, and swap pictures in place. Keep every position,
  size, font and colour.
- **Add** a slide by copying a slide of the same type from this deck, or from the template if the deck has none,
  then replace its content.
- **Remove** and **move** slides as planned.
- Update the speaker notes on every slide you changed or added, and leave the others' notes alone.
- Save under the file name in the topic list header, in `teaching-materials/slides/`. Never overwrite the file in
  `decks-to-update/`.

### 4. Check

Render the deck to images and look at every slide you changed or added, and at its neighbours: nothing
overflows, new slides match the deck's existing style, builds still line up, no PowerPoint animations or
transitions were added.

### 5. Report

A change log: one line per slide (kept, updated, added, removed or moved, and why), then the same items as the
deck prompt's report (minutes per row, placeholders, hard-to-present content, design rules the deck doesn't
follow).
