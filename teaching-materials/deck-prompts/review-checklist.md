# Review checklist for a generated deck

Go through this before a deck is used. It takes about 20 minutes per deck.

## Content
- [ ] Every `deck` row in the topic list is on a slide, in order, and nothing else is.
- [ ] Every claim, number, date and code line matches the lesson page. Spot-check at least five.
- [ ] No `CONTENT NEEDED` or `FIGURE NEEDED` placeholder is left (or each one has an owner).
- [ ] No internal course links, no dev-team or partner-review notes.
- [ ] The course name is exactly *Reproducible Workflows with Open Water Data: NASA, NOAA, USGS River Data
      Access* everywhere it appears; dates on the title and schedule slides are right.
- [ ] The objectives slide shows only the main objectives, as the topic list gives them.
- [ ] Agency order NASA → NOAA → USGS; "WDFN", not "NWIS" (except the legacy contrast).
- [ ] Live-coding slides name the right notebook file and sections, and give the time to come back.

## Updates (decks made with `update-prompt.md`)
- [ ] The change log matches what you see: flick through every slide it says changed, was added or moved.
- [ ] Slides marked `KEEP`, and slides the log says were kept, are exactly as they were.

## Look
- [ ] Flip through at full screen: it looks like your other decks, not like a different designer's.
- [ ] No layered shapes, decorative icons, cards, gradients, shadows or emoji (design rules §10).
- [ ] One emphasis device per slide, and it points at what you'll talk about.
- [ ] No text below 16 pt except credit lines; nothing overflows or overlaps.
- [ ] Builds line up: flick back and forth, and only the one change should move.
- [ ] No PowerPoint animations or transitions (Transitions and Animations tabs are empty).
- [ ] Every borrowed image has a credit line and alt text.

## Pacing
- [ ] Rehearse, or at least click through with a timer: each block lands near its minutes in the topic list.
- [ ] Every slide's notes start with SAY (the points to get across, as you'd say them to learners) and end with
      COURSE CONTENT (where the material is in the lessons); answer slides repeat their activity prompt.
- [ ] "IF SHORT ON TIME" marks what you can skip.

## Save it
- [ ] Save the deck under the name in the topic list header, in `teaching-materials/slides/`. Decks are
      git-ignored: never commit them. Share them through Canvas.
- [ ] Its document properties' Comments say which commit it was built from.
- [ ] Commit any topic-list
      edits together.
- [ ] If you fixed content on a slide, fix the lesson page too, or the next build undoes it.
