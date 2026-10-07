# Claude Code agent setup — federal-water-data-curriculum

## What's in this kit

```
CLAUDE.md                              instructions Claude Code loads every session (scope, conventions, git rules)
ROADMAP.md                             Module 4 → Module 3 plan to the 10/12 first cut, with 🚦 approval gates
.claude/settings.json                  starts sessions in auto mode; ASK only before commit, push, PR/issue
                                       actions, reset/rebase; DENY merges, force-push, push to main/dev,
                                       edits to Modules 1–2 and to the guardrail files
.claude/hooks/git_guard.py             blocks pushes/commits to main or dev, PR merges, force-push and
                                       branch deletes however they're spelled
.claude/agents/curriculum-developer.md writes lesson content from notebooks + agency resources
.claude/agents/content-reviewer.md     read-only reviewer: code documented + executed, links resolve, build ok
.claude/skills/port-notebook/          notebook → lesson section
.claude/skills/roadmap-status/         "where are we?"
.claude/skills/open-pr/                commit → push → draft PR to dev, asking at each step
.claude/scripts/check_links.py         link checker (stdlib only)
.github/workflows/pr-checks.yml        on PRs to dev/main: MyST build + link check of changed pages
.github/workflows/deploy-dev-preview.yml
                                       on push to dev: build and publish to GitHub Pages, titled
                                       "— DRAFT (dev)" with a draft banner on every page
.github/scripts/mark_draft.py          adds the draft title/banner in CI only (never committed)
```

## One-time setup (≈20 minutes)

1. **Bring the existing `dev` branch up to date with `main`** (it has nothing `main` lacks, so this is a
   fast-forward), then add the kit through a PR you merge:
   ```bash
   cd federal-water-data-curriculum
   git fetch upstream
   git switch dev 2>/dev/null || git switch -c dev upstream/dev
   git merge --ff-only upstream/main && git push upstream dev
   gh repo set-default CUAHSI/federal-water-data-curriculum   # gh commands target the CUAHSI repo, not your fork
   git switch -c chore/claude-agent-setup
   # unzip the kit into the repo root (keeps .claude/ and .github/), then:
   git add CLAUDE.md ROADMAP.md AGENT_SETUP.md .claude .github
   git commit -m "Add Claude Code agent configuration and dev preview workflows"
   git push -u upstream chore/claude-agent-setup
   gh pr create --repo CUAHSI/federal-water-data-curriculum --base dev --title "Claude Code agent setup" --body "Agent config, roadmap, CI"
   ```
   Merge it yourself.
2. **Branch protection on the CUAHSI repo** — essential now, because the agent pushes branches straight to
   `upstream` (Settings → Rules → Rulesets): for `main` *and* `dev` — require a pull
   request, block force pushes, restrict deletions, no bypass. This is the backstop behind the local rules.
3. **Pages preview:** Settings → Pages → Source: *GitHub Actions*. Settings → Environments →
   `github-pages` → Deployment branches: add `dev` (by default only `main` may deploy).
   The preview appears at `https://cuahsi.github.io/federal-water-data-curriculum/`.
4. **Local tools:** conda/mamba, Node + `npm install -g mystmd`, `gh auth login`.
5. **Credentials** in your shell profile (the agent reads them; they never go in the repo):
   `API_USGS_PAT`; Earthdata Login via `EARTHDATA_USERNAME`/`EARTHDATA_PASSWORD` or `~/.netrc`.
6. **Update Claude Code** (`claude update`) so auto mode is available.

## Fewer "Allow" prompts

The project settings start every session in **auto mode**: a background classifier reviews each action
instead of prompting you, so edits, installs, scripts, builds, downloads and **local commits on feature
branches** run without stopping. What still asks you:
- `git push`, `gh pr create/edit/comment`, `gh issue create/comment`, `git reset`, `git rebase`

What is refused outright in every mode: merges, force-push, committing or pushing to `main`/`dev`,
edits to Modules 1–2, edits to the guardrail files.

Switch modes any time with **Shift+Tab**. If auto mode isn't offered on your account or model, use
`acceptEdits` mode; the allow list covers the routine commands. To require approval for commits again,
move `"Bash(git commit:*)"` from `allow` back to `ask` in `.claude/settings.json`.

## Start the three lanes (parallel sessions)

From your clone, on an up-to-date `dev`, create one worktree per lane (separate folders, same repo):

```bash
git fetch upstream
mkdir -p ~/fwdc-spike
git worktree add ../fwdc-laneA -b content/03-nwm-access-routes upstream/dev
git worktree add ../fwdc-laneB -b content/04-synthesis upstream/dev
git worktree add ../fwdc-laneC -b content/03-swot-raster upstream/dev
```

Open three terminals and run `claude` in each folder, then paste the matching prompt.

**Lane A** (`../fwdc-laneA`):
> You are Lane A in ROADMAP.md. Rough-cut standard per CLAUDE.md. Do P1.3 (NWM access-route measurements; spike
> files in ~/fwdc-spike/nwm, report in ~/fwdc-spike/nwm/REPORT.md as soon as the numbers exist), create
> environments/nwm.yml, then P4.1 on this branch. Commit locally as you go; don't push. Post a short summary when
> the report is written and again when the page is drafted.

**Lane B** (`../fwdc-laneB`):
> You are Lane B in ROADMAP.md. Rough-cut standard per CLAUDE.md. Do P1.1 and P1.2 (spike files in
> ~/fwdc-spike/usgs and ~/fwdc-spike/swot), create environments/synthesis.yml, then draft P3.1 (04/02) on this
> branch. Write the NWM section last using ~/fwdc-spike/nwm/REPORT.md; if it isn't there yet, leave a marked stub
> and tell me. Commit locally as you go; don't push. Post a summary when done.

**Lane C** (`../fwdc-laneC`):
> You are Lane C in ROADMAP.md. Rough-cut standard per CLAUDE.md. On this branch do P4.2 (03/01 SWOT incl. Raster
> water area; create environments/swot.yml). Then for each of P4.3, P3.2 and P3.3 create its branch from
> upstream/dev in this worktree (`git switch -c <branch> upstream/dev`), committing before you switch. For P3.2 data
> provider recommendations, mark each with [PARTNER REVIEW: ...]. Finally draft the P4.4 Module 2 issue text as a
> file in ~/fwdc-spike/. Commit locally as you go; don't push. Post a summary after each page.

Stay near your laptop if you can: each lane posts questions and summaries as it goes, and quick answers speed
things up. When a lane says a branch is ready, you can approve its push and draft PR right away.
Afterwards, `git worktree remove ../fwdc-laneA` (etc.) cleans up; branches stay.

## Testing the guard

```bash
echo '{"tool_name":"Bash","cwd":".","tool_input":{"command":"gh pr merge 1"}}' \
  | python3 .claude/hooks/git_guard.py; echo "exit=$?"   # expect exit=2 and a BLOCKED message
```
