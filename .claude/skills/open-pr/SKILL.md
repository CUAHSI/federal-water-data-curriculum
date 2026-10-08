---
name: open-pr
description: Commit, push a feature branch to upstream and open a DRAFT pull request against dev — no approval needed; Lindsay reviews and merges. Use when a roadmap task is finished and has passed content-reviewer and learner-reviewer.
---

# Commit, push, open a draft PR

Preconditions — stop if any fail:
- Current branch is not `main`, `master` or `dev` (`git branch --show-current`).
- `content-reviewer` returned PASS and `learner-reviewer` reports no Blockers (or Lindsay waived them).
- `myst build --html` succeeds.

## Step 1 — commit (no approval needed on a feature branch)
Commit with a descriptive message, e.g.
  ```
  content(04-synthesis): add USGS observations for the Skagit flood

  Pattern adapted from collect-usgs-streamflow.ipynb (CUAHSI notebooks).
  Roadmap: P3.1
  ```
`git add <files>` (name files; never add scratch/spike files) then `git commit`.

## Step 2 — push (no approval needed)
`git push -u upstream <branch>`. Always name the remote and branch; never push to `origin` (Lindsay's fork).
Branch names must be `<type>/<topic>` (content, chore, env, fix, docs); the guard blocks anything else.

## Step 3 — draft PR (no approval needed)
Write the body to a temp file, then:
`gh pr create --repo CUAHSI/federal-water-data-curriculum --draft --base dev --head <branch> --title "..." --body-file <tmpfile>`
Later pushes to the same branch update the PR; use `gh pr edit` only to refresh the description.

Body template:
```
## Roadmap
Roadmap task: P?.? — <name>

## What changed
- ...

## Sources adapted
- <notebook title> — <author/org>, <url>, <license>

## Open callouts added
- TODO (dev team): ...
- Partner review (AGENCY): ...

## Verification
- Build: ok
- Links: <checked/broken/unverified>
- content-reviewer: <summary line>   learner-reviewer: <summary line>
- Code executed: <list>   Reviewed only: <list>

## Open questions for review
- ...
```
**If `gh` isn't installed or authenticated** (`gh auth status` fails): don't install or log in yourself. After
the push, save the title/body to `~/fwdc-spike/pr-<branch>.md` and give Lindsay this link to open the
PR in her browser, with "Create draft pull request" selected:
`https://github.com/CUAHSI/federal-water-data-curriculum/compare/dev...<branch>?expand=1`

Then report the PR URL in your lane report. **Do not merge, approve, mark ready, enable auto-merge, or change the base.**
Lindsay reviews and merges into dev; only Lindsay updates main.
