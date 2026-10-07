---
name: open-pr
description: Commit locally, then push a feature branch and open a DRAFT pull request against dev — push and PR only after Lindsay explicitly approves. Use when a roadmap task is finished and reviewed.
---

# Commit, push, open a draft PR (approval before push and before PR)

Preconditions — stop if any fail:
- Current branch is not `main`, `master` or `dev` (`git branch --show-current`).
- `content-reviewer` returned PASS for this branch (or Lindsay waived it).
- `myst build --html` succeeds.

## Step 1 — commit (no approval needed on a feature branch)
Commit with a descriptive message, e.g.
  ```
  content(04-synthesis): add USGS observations for the Skagit flood

  Pattern adapted from collect-usgs-streamflow.ipynb (CUAHSI notebooks).
  Roadmap: P3.1
  ```
`git add <files>` (name files; never add scratch/spike files) then `git commit`.

## Step 2 — push (ask first)
Show `git log --oneline upstream/dev..HEAD` and a 3–6 line summary, then ask: "OK to push `<branch>` to upstream (CUAHSI)?" On yes: `git push -u upstream <branch>` (always name the remote and branch; never push to `origin`, Lindsay's fork).

## Step 3 — draft PR (ask first)
Draft the PR title/body and show it. On yes:
`gh pr create --repo CUAHSI/federal-water-data-curriculum --draft --base dev --head <branch> --title "..." --body-file <tmpfile>`

Body template:
```
## Roadmap
Roadmap task: P?.? — <name>

## What changed
- ...

## Sources adapted
- <notebook title> — <author/org>, <url>, <license>

## Partner review markers added
- [PARTNER REVIEW: ...] lines, if any

## Verification
- Build: ok
- Links: <checked/broken/unverified>
- Code executed: <list>   Reviewed only: <list>

## Open questions for review
- ...
```
**If `gh` isn't installed or authenticated** (`gh auth status` fails): don't install or log in yourself. After
the approved push, save the title/body to `~/fwdc-spike/pr-<branch>.md` and give Lindsay this link to open the
PR in her browser, with "Create draft pull request" selected:
`https://github.com/CUAHSI/federal-water-data-curriculum/compare/dev...<branch>?expand=1`

Then report the PR URL. **Do not merge, approve, enable auto-merge, or request merge.**
Lindsay reviews and merges into dev; only Lindsay updates main.
