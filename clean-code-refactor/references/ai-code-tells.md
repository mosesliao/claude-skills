# Humanizing code: AI-generated code tells

Code written by AI assistants and agents tends to carry recognizable patterns that add volume without adding meaning. "Humanizing" code means removing them so a reader understands the code quickly and can change it safely. The goal is not to make code *look* hand-written. It is to stop boilerplate from hiding intent, whoever wrote it.

Codes A1–A12 extend the book's smell catalog so findings can be cited the same way (e.g. "A3, G4").

## Contents
- A1–A4: comments and documentation
- A5–A7: error handling and defensive code
- A8–A10: structure and abstraction
- A11–A12: consistency and leftovers
- Safety rules for humanizing
- Not a tell (leave alone)

## Comments and documentation

**A1 Narrating comments.** Comments that walk through the code step by step (`# Step 1: initialize the list`, `# Loop through items`, `# Return the result`). Delete them. If a block needs a label, extract it into a well-named function instead. Related: C3.

**A2 Signature-restating docstrings.** Docstrings or doc blocks on every function that repeat the parameter names and types already in the signature, with no information about behavior, edge cases or intent. Remove them on private helpers; on public APIs, rewrite to say what the signature can't (units, side effects, errors raised, invariants).

**A3 Chatty or conversational text in code.** Comments or log messages addressed to someone ("Now we handle the edge case!", "This ensures robust handling…"), marketing words (robust, seamless, comprehensive, elegant), and emoji in logs or comments. Rewrite plainly or delete.

**A4 Change-history comments from the session.** "Updated to fix the bug", "Changed from X to Y", "New implementation", "Added per request". This belongs in commit messages, not code. Related: C1.

## Error handling and defensive code

**A5 Defensive padding.** try/except (or the language's equivalent) around code that can't fail, repeated `None`/null checks on values that are guaranteed by the caller or the type system, `isinstance` checks against typed parameters. These make the real failure points hard to find. Remove them only after confirming the guarantee (types, callers, tests). Related: G4.

**A6 Swallowed errors.** Catch-all handlers that log and carry on, return a default, or `pass`. They turn crashes into silent wrong answers. Narrow the exception type, let it propagate, or handle it deliberately. **This changes behavior on failure**, so treat it as a behavior change, flag it to the user, and don't do it silently in a "pure refactor."

**A7 Impossible fallbacks.** Branches for cases that can't happen ("in case the list is somehow a string"), default values for required config, retry loops around deterministic local operations. Delete once confirmed impossible; if unsure, replace with an assertion or explicit error so the assumption is visible.

## Structure and abstraction

**A8 Speculative abstraction.** Interfaces or abstract base classes with a single implementation, factories that build one class, strategy patterns with one strategy, config flags nobody uses, "for future extensibility" layers. Inline them until a second real use appears. This is the book's fourth simple-design rule (minimal classes and methods).

**A9 Generic names at scale.** `data`, `result`, `response`, `item`, `obj`, `handler`, `manager`, `processor`, `helper`, and dumping-ground modules like `utils.py`, `helpers.ts`, `common/`. Rename to what the thing actually is and move functions to the module that owns the concept. If the domain meaning isn't clear, ask (non-negotiable 6). Related: N1, G17.

**A10 Reinventing the standard library or the project's own helpers.** Hand-written retry loops, date parsing, path joining, deep-copy, argument parsing, HTTP clients, or a second version of a helper the project already has. Replace with the standard or existing one. Check the behavior matches first (edge cases, error types). Related: G5.

## Consistency and leftovers

**A11 Cross-session inconsistency.** The same problem solved differently in different files because each was generated in a separate session: several config loaders, multiple logging setups, mixed error-handling styles, different naming conventions for the same concept. Pick the project's dominant (or best) pattern and converge on it, one usage at a time. Related: G11.

**A12 Scaffolding left behind.** Unused parameters and imports, debug prints, commented-out alternatives, TODOs the agent wrote to itself, placeholder values, example/main blocks in library files, and files appended to past any sensible size because "that's where the conversation was" (see File organization rules). Related: G9, G12, C5.

## Safety rules for humanizing

- Deleting comments, docstrings and dead code is low risk; do these first.
- Removing defensive code (A5, A7) needs evidence the guarded case can't happen: types, callers, tests. If the evidence is thin, keep the guard or replace it with an explicit assertion.
- Changing error handling (A6) changes behavior on failure. Report it separately and get the user's agreement.
- Replacing hand-rolled code with a library (A10) can change edge-case behavior; add or check tests around it first.
- Never strip comments that explain *why* (a workaround, a regulatory requirement, a non-obvious constraint), however chatty they sound. Rewrite them plainly instead.

## Not a tell (leave alone)
- Docstrings on public APIs that carry real information.
- Defensive checks at real trust boundaries: user input, network responses, file contents, third-party APIs.
- Comments explaining intent, constraints, workarounds or links to tickets/specs.
- Patterns required by the framework or the project's style guide.
