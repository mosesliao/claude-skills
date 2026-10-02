# Applying Clean Code across languages

The book's examples are Java. The principles are mostly universal; some specific prescriptions are not. Rule of thumb: **keep the intent, use the language's idiom, and let the project's own conventions win.**

## Contents
- Universal vs. Java-specific advice
- Where tests live (test separation)
- Splitting large files
- Python
- JavaScript / TypeScript
- Go
- Rust
- C# / Kotlin / modern Java
- C / C++
- Functional languages (Haskell, Elixir, Clojure, F#, Scala FP style)
- SQL
- Shell (bash/sh)
- Infrastructure as Code (Terraform/HCL, CloudFormation, Helm/YAML)
- Notebooks and scripts

## Universal vs. Java-specific

Universal: intention-revealing names, small focused functions, one level of abstraction, no flag args, no dead or commented-out code, DRY, honest comments, explicit error context, Law of Demeter, SRP/cohesion, wrapping third-party boundaries, clean fast tests, incremental refactoring.

Adapt per language:
- "Prefer exceptions to error codes": in languages where errors are values (Go, Rust, functional Result types), the *intent* is "don't let error plumbing obscure the happy path and never ignore errors." Use idiomatic error values, not exceptions.
- "Prefer polymorphism to switch": in languages with sum types and exhaustive pattern matching (Rust, Kotlin sealed classes, TypeScript discriminated unions, Scala, Haskell, F#), a single exhaustive `match` is often the clean choice. The smell is the *same switch duplicated* in many places.
- "Classes should be small / SRP": applies to modules, packages and files in languages without classes.
- "Don't return null": use the language's Option/Maybe/nullable-type features.
- Wildcard imports (J1): most modern style guides (PEP 8, Go, Rust, TS lint rules) prefer explicit imports. Follow the language and project.
- Function-length targets: follow readability, not a line count. Idiomatic Go and C, for example, tolerate longer linear functions.

## Where tests live (test separation)

Tests go in separate files from production code, following each language's convention:

| Language | Conventional test location |
|---|---|
| Python | `tests/` directory (pytest) or `test_*.py` beside the module; never `if __name__ == "__main__":` test blocks or test classes inside production modules |
| JS / TS | `*.test.ts` / `*.spec.ts` beside the source, or `__tests__/` |
| Go | `*_test.go` in the same package (or `package foo_test` for black-box tests) |
| Rust | Small `#[cfg(test)] mod tests` inline is idiomatic. When it bloats the file, move it to `foo/tests.rs` via `#[cfg(test)] mod tests;`; integration tests go in `tests/` |
| Java / Kotlin | `src/test/java` / `src/test/kotlin` mirroring the main package |
| C# | Separate test project (`*.Tests.csproj`) |
| C / C++ | `tests/` with the project's framework (GoogleTest, Catch2, Unity…) |
| Swift | Separate test target (`Tests/<Module>Tests`) |
| Shell | `tests/*.bats` or similar |
| Terraform | `tests/*.tftest.hcl` (or Terratest in a separate Go module) |

When moving tests, check the test runner still discovers them (config globs, `testpaths`, `jest` roots, package names) and that test-only dependencies don't leak into production imports.

## Splitting large files (soft ~1,000 line limit)

Keep the public import path stable while splitting:
- Python: turn `big.py` into a `big/` package and re-export the public names from `big/__init__.py`.
- JS/TS: create a folder with an `index.ts` that re-exports.
- Go: split into several files in the same package. No import changes are needed, so this is the easiest case.
- Rust: `mod` submodules plus `pub use` re-exports.
- Java/Kotlin/C#: one public type per file is already the norm; large files usually mean a class doing too much, so split the class.

## Python
- Follow PEP 8 naming (`snake_case`, `PascalCase` classes, `UPPER_CASE` constants); ruff/black/flake8 configs win.
- Replace flag arguments with separate functions or keyword-only args + clear names; avoid mutable default arguments.
- Use `dataclasses`/`NamedTuple`/`TypedDict`/pydantic for data structures instead of loose dicts passed everywhere (G8, boundaries).
- Type hints make intent explicit (G27); `Optional[X]` / `X | None` makes nullability visible.
- Prefer specific exceptions with context; never bare `except:`; use context managers for cleanup.
- Comprehensions are fine but don't nest them past readability (G16).
- Docstrings for public APIs; no redundant docstrings restating the signature (C3).

## JavaScript / TypeScript
- Follow ESLint/Prettier configs. `camelCase` functions/vars, `PascalCase` types/components.
- Replace boolean option params with options objects or separate functions.
- TypeScript: use discriminated unions + exhaustive `switch` (with a `never` check) rather than stringly-typed branching; avoid `any`.
- Prefer `async/await` with try/catch scoped tightly over deeply nested promise chains/callbacks.
- Avoid optional-chaining train wrecks (`a?.b?.c?.d`) as a design; they often signal Law of Demeter issues.
- React: components are functions, so apply SRP (split UI from data fetching via hooks), keep props few, extract custom hooks for reused logic.

## Go
- `gofmt`/`go vet`/`golangci-lint` conventions; short names for short scopes are idiomatic (`r` for a reader in a 5-line func). N5 still applies to wide scopes.
- Errors are values: wrap with context (`fmt.Errorf("loading config %s: %w", path, err)`); never discard errors (G4). Early-return on error to keep the happy path left-aligned.
- Small interfaces defined by the consumer ("accept interfaces, return structs") is Go's dependency inversion.
- Don't introduce class-like hierarchies; use composition and small packages.
- Exported names are capitalized; package names short and non-stuttering (`config.Load`, not `config.ConfigLoad`).

## Rust
- `rustfmt` + `clippy` conventions.
- `Result`/`?` for errors with context (e.g. `anyhow::Context`, `thiserror` types designed for the caller); avoid `unwrap()`/`expect()` in non-test code paths unless an invariant is documented.
- `Option` instead of sentinel values; enums + exhaustive `match` are idiomatic.
- Use newtypes to make intent precise (G26, G27).
- Respect ownership: refactors that move code between functions may need borrow changes, so keep steps small and compile often.

## C# / Kotlin / modern Java
- Closest to the book; most advice applies directly.
- Use records/data classes for DTOs; sealed types + pattern matching where appropriate.
- Kotlin: nullable types replace "don't return null" with "make nullability explicit"; prefer scope functions only where they aid clarity.
- Use DI containers per framework conventions (Spring, .NET DI) for construction/use separation.

## C / C++
- C: no exceptions, so use consistent error return conventions with clear names, single cleanup path (`goto cleanup` is an accepted idiom). Make ownership explicit in names/comments.
- C++: RAII for resource handling, `std::optional`/`std::expected` for absent values/errors, avoid raw owning pointers.
- Macros: replace with `constexpr`/inline functions/enums where possible (G25, G16).

## Functional languages
- Pure functions already satisfy "no side effects"; push effects to the edges.
- Small composable functions and pipelines are the idiom; avoid point-free chains so dense they obscure intent (G16).
- Pattern matching over nested conditionals; sum types for states.
- "Classes" maps to modules; SRP applies to modules.

## SQL
- Meaningful aliases (not `a`, `b`, `t1`); consistent casing conventions.
- Break long queries into CTEs with intention-revealing names (the SQL equivalent of extract function).
- Avoid magic literals; parameterize. Avoid `SELECT *` in production queries.
- Refactoring SQL must preserve result sets exactly; compare outputs before/after on representative data.

## Shell (bash/sh)
- `set -euo pipefail` (where appropriate), quote variables, use functions with descriptive names, `local` variables.
- Extract repeated pipelines into functions; name magic paths/values at the top (G35).
- Use `shellcheck`. If a script grows past a few hundred lines of logic, suggest moving to a real language.

## Infrastructure as Code
- Terraform: meaningful resource and variable names, `description` on variables/outputs, extract repeated blocks into modules, use `locals` for derived values (explanatory variables), keep configurable data in variables at the top level (G35), `terraform fmt`/`tflint`.
- Refactoring Terraform can **destroy and recreate real resources**. Renames/moves need `moved {}` blocks (or `terraform state mv`), and every change must be verified with `terraform plan` showing no unintended destroy/replace. Treat a plan with replacements as a failed refactor.
- CloudFormation/Helm/K8s YAML: reduce duplication via templates/anchors/helpers carefully; render and diff the output before/after.

## Notebooks and scripts
- Move reusable logic out of cells into functions/modules; name intermediate results; delete dead cells.
- Don't over-engineer one-off scripts. Apply proportionate cleanup.
