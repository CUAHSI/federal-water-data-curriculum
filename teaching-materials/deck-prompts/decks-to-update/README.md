# decks-to-update/: existing decks to edit, not rebuild

Everything in this folder except this README is git-ignored.

Put a session deck here when you want it **updated** rather than built from scratch: a deck you made by hand,
or one from an earlier run of the course. Name it after the session's deck (the file name in its topic list
header, e.g. `session-03_module-03_lesson-01_retrieve-nasa-swot-data.pptx`), so the prompt can find it.

Then run `update-prompt.md` (in Claude Code: `/build-slides N update`). It inventories the deck, shows you a
slide-by-slide plan (keep, update, move, remove, add), and after your go-ahead saves the updated deck in
`teaching-materials/slides/`. The file here is never overwritten.

To protect a slide from any change, start its speaker notes with `KEEP`.

If this folder has no deck for the session, the update prompt works on your local deck in
`teaching-materials/slides/` instead (decks are git-ignored). That's the usual way to bring a deck up to date after a lesson changes.
