---
name: "clean-code-refactor"
description: Refactor code in any programming language using the principles from Robert C. Martin's "Clean Code" (meaningful names, small single-purpose functions, honest comments, clean error handling, cohesive classes, clean tests, and the book's catalog of code smells), plus "humanizing" code by removing AI-generated code tells (narrating comments, boilerplate docstrings, defensive padding, speculative abstractions, generic names). Use this skill whenever the user asks to refactor, clean up, tidy, simplify, untangle, or "make readable" some code, asks for a code-smell review or a refactoring plan, wants AI-generated or agent-written code made more human-readable or less sloppy, mentions Clean Code or Uncle Bob, or wants recurring/scheduled (e.g. monthly) refactoring of part of a repo — even if they don't name the book. Also use it when a scheduled task invokes a refactoring run against a refactor-schedule config file.
---

# Clean Code Refactor

Refactor code so it is easier to read and change, without changing what it does, guided by the principles of *Clean Code*. Code is read far more than it is written, so it should be written for the human reader. That includes **humanizing** code produced by AI assistants and agents, which tends to carry boilerplate that hides intent. Works for any language: apply the *intent* of each principle, expressed in that language's own idioms.

## Files in this skill

- `references/principles.md`: the Clean Code principles and smell catalog (C/E/F/G/N/T codes), paraphrased. Read it before producing a smell report or plan.
- `references/ai-code-tells.md`: AI-generated code tells (codes A1–A12) and the safety rules for removing them. Read it whenever the code was written by AI or agents, or the user picks the humanize area. If you can't tell who wrote it, skim it anyway, since these patterns are common now.
- `references/language-adaptation.md`: how to translate the book's Java-era advice into other languages (Python, JS/TS, Go, Rust, C#, Kotlin, functional languages, SQL, shell, Terraform/IaC). Read the section for the language you're touching.
- `references/scheduling.md`: how to run this skill on a schedule (monthly etc.) and how scheduled runs behave. Read it when the user asks for scheduling or when you're running non-interactively.
- `assets/refactor-schedule.example.yml`: config template for scheduled runs.
- `assets/github-workflow-monthly-refactor.yml`: example GitHub Actions workflow.
- `assets/refactor-log-template.md`: format for the running log of scheduled refactors.

## The non-negotiables

These hold in every mode, because a refactor that changes behavior is a bug with good intentions:

1. **Preserve behavior.** Refactoring changes structure, not behavior. Don't fix bugs, add features, or change public APIs in the same change. If you spot a bug, report it separately. This includes humanizing: tightening a catch-all error handler (A6) changes what happens on failure, so it's a behavior change that needs the user's agreement.
2. **Tests are the safety net.** Find and run the existing tests before and after. If the target has no meaningful tests, say so plainly and propose writing characterization tests (tests that pin current behavior, including oddities) *before* touching structure. If tests can't run in this environment, say that too, and keep changes smaller and more mechanical.
3. **Small, reversible steps.** One kind of change at a time (rename, extract, move, inline). Each step should leave the code working. Prefer a sequence of small commits over one big rewrite. The book's "grand redesign" warning applies.
4. **Respect the house style.** Project linters, formatters, naming conventions and established patterns beat the book's defaults. Consistency within a codebase is itself a Clean Code principle (G11, G24).
5. **Judgment over dogma.** The book's heuristics are guidelines from 2008-era Java. Applying one mechanically (say, splitting a clear 15-line function into five 3-line ones) can make code worse. Every change should make the code easier to understand for the next reader; if it doesn't, skip it.
6. **Don't invent domain meaning.** Renaming cryptic code often needs business knowledge you don't have (what "type 1" means, what a multiplier represents). If the meaning isn't clear from the code, docs or surrounding context, ask the user, or use a neutral descriptive name and flag it as provisional in the summary. A confident but wrong domain name is worse than a vague one.

## File organization rules

The user cares about these, so check them on every refactor, not only when "structure" is the chosen area:

- **Separate tests from production code.** Test code doesn't belong in the same file as the code it tests. Move tests into the language's conventional test location: `tests/` or `test_*.py` (Python), `*.test.ts` / `__tests__/` (JS/TS), `*_test.go` (Go), `src/test/...` (Java/Kotlin), a separate test project (C#). Rust is the exception, since inline `#[cfg(test)] mod tests` is idiomatic. There, keep small test modules inline, but once tests make a file large, move them to a sibling file (`mod tests;` → `foo/tests.rs`) or to `tests/` for integration tests. See `references/language-adaptation.md`. Shared fixtures and test helpers go in test-only modules too, never in production files.
- **Soft limit: about 1,000 lines per file.** A file over 1,000 lines is a finding to report (treat it as G8/SRP at file level). Propose a split along responsibilities, not at arbitrary line counts. Exceptions are fine when splitting would hurt: generated code, data/fixture tables, migrations, a single cohesive state machine or parser, or language constraints. Name the exception and the reason in "Deliberately left alone" rather than silently ignoring the file.
- **How to split a huge file safely:** (1) move tests out first, since that's lowest risk and usually shrinks the file a lot; (2) run the tests from their new location to confirm they're still discovered and passing; (3) split production code by responsibility into a module/package, one step at a time; (4) keep existing import paths working with re-exports (e.g. `__init__.py`, `index.ts`, `pub use`) so callers don't break; (5) re-run tests after each move. Mention that each move should be its own commit so git history and blame stay readable.

## Step 1: Work out the mode

Pick one from the request:

| Signal | Mode |
|---|---|
| User shares code / names files and says "refactor" without saying how | **Interactive** (default): ask scope first |
| "Review", "what smells", "audit", "how clean is this" | **Assess**: smell report only, no edits |
| "Plan", "roadmap", large codebase or many files | **Plan**: phased plan, then wait for approval |
| Clear, narrow instruction ("rename these", "extract the validation", "just fix the names") | **Direct**: do exactly that slice |
| Invoked by a scheduler / no human present / prompt references a schedule config | **Scheduled**: see `references/scheduling.md`; never ask questions |

## Step 2 (Interactive mode): Ask before changing

Before editing, ask the user two things. Use a tappable-options tool (e.g. `ask_user_input_v0`) if one is available, otherwise ask briefly in prose. Ask in one turn, not a series of messages.

**Question A: Which area?** (multi-select)
- Naming (variables, functions, classes)
- Functions (size, one job, arguments, side effects)
- Comments & formatting
- Error handling (exceptions vs codes, nulls)
- Classes & structure (responsibilities, coupling, Law of Demeter)
- File structure (separate tests from code, split files over ~1,000 lines)
- Humanize AI-generated code (narrating comments, boilerplate docs, defensive padding, over-abstraction)
- Duplication & dead code
- Tests
- Everything: let Claude prioritize

**Question B: How to proceed?**
- Show me a plan first, then I'll approve
- Go ahead and refactor
- Just report the smells, don't change anything

If the user already answered either question in their message, don't ask it again. If the code is tiny (under ~40 lines) and the request is clear, you can skip asking and go straight ahead, then say what you focused on.

## Step 3: Assess

1. **Get the actual code.** If the user names files you can't see, look for them first: uploads, the working directory, or a connected repository (e.g. a GitHub connector). If you still can't find them, say so and ask for the file. If a plan is requested anyway, label it **provisional** and keep it short. A generic plan presented as specific is not useful.
2. Identify the language, framework and any project conventions (lint configs, formatter, existing patterns). Read the matching section of `references/language-adaptation.md`.
3. Measure file sizes (e.g. `wc -l`) and check where tests live. Flag files over ~1,000 lines and any tests mixed into production files (see File organization rules).
4. Find the tests and how to run them. Run them if you can, and note the baseline result.
5. Read `references/principles.md` (and `references/ai-code-tells.md` when relevant) and scan the target for smells within the chosen areas.
6. Rank findings by **impact on readability/changeability × risk of the change**. High-value, low-risk items first (renames, extracting explanatory variables, deleting dead/commented-out code); risky structural moves later.

Report findings in this format:

```
## Smell report: <file or area>
Baseline: <tests found / run result, or "no tests found">

| # | Location | Smell (code) | Why it hurts | Proposed fix | Risk |
|---|----------|--------------|--------------|--------------|------|
| 1 | parse_order() L40-112 | Function does many things (G30), too many args (F1) | Hard to test pieces separately | Extract validate/price/persist steps | Med |
```

Keep "Why it hurts" concrete to this code, not a generic quote of the rule. Don't report a smell just because a rule matches; skip it if fixing it wouldn't help a reader.

## Step 4 (Plan mode, or when the user asked for a plan)

Group fixes into phases ordered safest-first. A typical shape:

1. **Safety net**: characterization tests for anything untested that later phases touch.
2. **Separate tests and split oversized files**: move inline tests to their conventional location, then split files over ~1,000 lines by responsibility (see File organization rules). Do this early, because smaller files make every later phase easier to review.
3. **Surface cleanup and humanizing**: names, magic numbers to named constants, explanatory variables, remove dead and commented-out code, fix misleading/redundant comments, strip narrating comments, boilerplate docstrings and leftover scaffolding (A1–A4, A12).
4. **Function-level**: remove defensive padding and impossible fallbacks where the guarantee is proven (A5, A7), extract functions to one level of abstraction, remove flag arguments, reduce argument counts, separate commands from queries, isolate try/catch bodies.
5. **Structure-level**: inline speculative abstractions (A8), converge cross-session inconsistencies and replace reinvented helpers (A10, A11), split classes by responsibility, fix feature envy / misplaced responsibility, replace type-switches with polymorphism or dispatch tables where it fits the language, isolate third-party boundaries.
6. **Tests**: clean up the tests themselves (readability, one concept per test, F.I.R.S.T.).

For each phase list: files touched, smells addressed (codes), estimated size, risk, and how it will be verified. End with a clear question asking which phases to run. Don't start editing until the user approves.

## Step 5: Refactor

- Work phase by phase, or item by item for small jobs. After each logical step, re-run tests where possible.
- Keep each change explainable in one sentence. If a step needs a paragraph to justify, it's probably too big or not worth it.
- Edit the user's actual files when you have them on disk or in a repo; otherwise return the full refactored code. For files over ~20 lines, write files rather than pasting giant inline blocks.
- Don't silently change formatting across a whole file (it buries the real diff); leave mass reformatting to the project's formatter, as a separate step.

## Step 6: Report

Close with a short summary:

```
## Refactor summary
Scope: <files / area>   Mode: <interactive/plan/direct/scheduled>
Tests: <before → after, or "not runnable here: please run X">

Changes
- <one line per change> (<smell codes>)

Deliberately left alone
- <thing> because <reason, e.g. public API, would need behavior change, low value>

Suggested next steps
- <next phase or follow-up, if any>
```

"Deliberately left alone" matters: it shows judgment and stops the next run from redoing the same debate.

## Scheduling

If the user wants a piece of code refactored on a schedule (e.g. "once a month"), read `references/scheduling.md`. In short: the skill defines how a scheduled run behaves (non-interactive, small scoped batch, branch + PR, never pushing to main, appending to a refactor log). The *timer* comes from whatever runs Claude: a scheduled task in Claude Cowork, a cron job running Claude Code headless, or a GitHub Actions workflow. Help the user set up a `.refactor-schedule.yml` from the template and the trigger that fits their setup. Plain claude.ai chat can't wake itself up on a timer, so say so honestly rather than implying it will.
