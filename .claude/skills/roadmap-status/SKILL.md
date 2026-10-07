---
name: roadmap-status
description: Summarize progress on ROADMAP.md — milestones done/in progress/next, open PRs and branches, and remaining TODO placeholders per module. Use at the start of a session or when asked "where are we?".
---

# Roadmap status

1. Read `ROADMAP.md`. Count checked vs. unchecked tasks per milestone.
2. `git fetch upstream --quiet` then `git branch -r --no-merged upstream/dev` for in-flight branches,
   and `gh pr list --repo CUAHSI/federal-water-data-curriculum --state open` (skip quietly if `gh` isn't installed or authenticated; list pushed branches instead).
3. `rg -c "\[TODO|\[describe|\[add |\[details|\[PARTNER REVIEW" --glob "0[234]*/**/*.md"` for placeholders per page.
4. Report in at most ~10 lines:
   - Overall: X of Y tasks done; where we are against the ROADMAP schedule table.
   - Per milestone: ✅ done / 🔄 in progress (branch/PR) / ⏳ not started.
   - Recommended next task and why (dependencies, target date).
   - Anything waiting at a 🚦 gate or on a roadmap open question.
Do not edit files.
