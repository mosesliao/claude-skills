# Scheduled (recurring) refactoring

## Contents
- How scheduling works
- The schedule config (`.refactor-schedule.yml`)
- How a scheduled run behaves
- Setting up the trigger: Cowork, Claude Code + cron, GitHub Actions
- Helping the user set it up

## How scheduling works

The skill doesn't contain a timer. It defines what a scheduled run does; something outside the skill wakes Claude up and asks it to run. Options:

| Where Claude runs | How to schedule |
|---|---|
| Claude Cowork (desktop) | Built-in scheduled tasks: create a monthly task whose prompt invokes this skill |
| Claude Code (CLI) | OS scheduler (cron, launchd, Windows Task Scheduler) running Claude Code in headless/print mode in the repo |
| GitHub repo | GitHub Actions `schedule:` cron trigger running Claude Code via Anthropic's GitHub Action (see `assets/github-workflow-monthly-refactor.yml`) |
| Plain claude.ai chat | Cannot self-trigger. Tell the user plainly and offer one of the above, or suggest a calendar reminder to start a chat with "run my monthly refactor" |

Scheduling features and CLI flags change over time, so check current docs for exact syntax before finalizing a setup.

## The schedule config

Keep a `.refactor-schedule.yml` in the repo root (template: `assets/refactor-schedule.example.yml`). It's the human's standing instructions for unattended runs, so it replaces the interactive questions:

- `targets`: list of paths/globs, each with `areas` (same choices as the interactive question) and an optional `frequency` / `priority`.
- `rotation`: whether each run takes the next target in turn or all targets.
- `max_files_per_run` / `max_changes_per_run`: keeps PRs reviewable.
- `exclude`: generated code, vendored code, migrations, anything risky.
- `test_command`: default verification command; each target can override it with its own `test_command` (different stacks need different checks, e.g. a service's unit tests vs `terraform validate`).
- `file_rules`: the soft `max_file_lines` limit (default 1000), `separate_tests`, and `allow_large_files` exceptions.
- `branch_prefix`, `log_file`: where output goes.

If the config is missing in a scheduled run, don't guess a scope. Write a short note (PR description or log entry) saying no config was found, attach the example template, and stop.

## How a scheduled run behaves

Scheduled runs have no human present, so they're more conservative than interactive ones:

1. **Never ask questions.** Take scope and areas from the config. If something is ambiguous, choose the safer option and note it in the report.
2. **Read the log** (`log_file`) to see what previous runs did, what was deliberately left alone, and which target is next in rotation. Don't relitigate decisions recorded as "left alone" unless the code changed.
3. **Baseline tests** with the target's `test_command` (or the default). If they fail before you start, don't refactor. Report the failing baseline and stop.
4. **Apply file rules first.** If `separate_tests` is on and a target has tests inside production files, moving them out is a good first batch. Files over `max_file_lines` (and not in `allow_large_files`) get split by responsibility, at most one file per run, since splits produce big diffs that need careful review.
5. **Humanizing in unattended runs**: if `humanize` is in a target's areas, do the low-risk parts (A1–A4, A12, and A5/A7 only where types or tests prove the guard is unreachable). Never change error-handling behavior (A6) or swap in library replacements (A10) unattended; list them under "Suggested next steps" in the PR for a human to decide.
6. **Pick a small batch**: highest value, lowest risk items within the caps. Prefer Phase 2/3 changes (names, extraction, dead code, comments) over structural moves; only do structural changes if the config's `areas` explicitly include them and tests cover the code well.
7. **Refactor in small steps**, running tests after each. If a step breaks tests and the fix isn't obvious, revert that step and record it as "attempted, reverted."
8. **Output on a branch** named `<branch_prefix>/<YYYY-MM>-<target-slug>`, never commit to the default branch, and open a PR (or leave the branch plus a summary if PRs aren't available). The PR body uses the Refactor summary format from SKILL.md and lists smell codes.
9. **Append to the log** using `assets/refactor-log-template.md`: date, target, changes, left alone, next target.
10. If nothing worth changing was found, say so in the log and open no PR. Clean code staying clean is a fine outcome.

## Trigger setups

### Claude Cowork
Create a scheduled task (monthly), pointed at the project folder, with a prompt like:

> Run the clean-code-refactor skill in scheduled mode using .refactor-schedule.yml in this folder. Work on a new branch, don't touch main, and append to the refactor log.

### Claude Code + cron (Linux/macOS)
Example crontab entry for 09:00 on the 1st of every month (adjust path and CLI flags to the current Claude Code docs):

```
0 9 1 * * cd /path/to/repo && claude -p "Run the clean-code-refactor skill in scheduled mode using .refactor-schedule.yml. Create a branch, open a PR, append to the refactor log." >> ~/.refactor-cron.log 2>&1
```

The skill must be installed where Claude Code can find it (e.g. the project's or user's skills directory), and the environment needs credentials (API key or login) and `gh` for PRs.

### GitHub Actions
Copy `assets/github-workflow-monthly-refactor.yml` to `.github/workflows/`. Requires an `ANTHROPIC_API_KEY` repository secret, the skill committed under the project's skills directory (e.g. `.claude/skills/clean-code-refactor/`), and permission for the workflow to create branches/PRs. Check the action's current README for input names, since they evolve.

## Helping the user set it up

When the user asks for scheduling:
1. Ask (or infer) where they run Claude: Cowork, Claude Code, GitHub.
2. Draft their `.refactor-schedule.yml` from the template using the paths and areas they name.
3. Provide the matching trigger (task prompt, crontab line, or workflow file).
4. Remind them that each run produces a PR for human review. Scheduled refactors should never merge themselves.
