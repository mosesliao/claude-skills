# Clean Code principles: working reference

Paraphrased summary of the principles in Robert C. Martin's *Clean Code* (2008), organized for refactoring work. Codes (C1, G5, N1…) follow the book's "Smells and Heuristics" chapter so findings can be cross-referenced. This is a summary for applying the ideas, not a substitute for the book.

## Contents
1. Core attitude
2. Names
3. Functions
4. Comments
5. Formatting
6. Objects and data structures
7. Error handling
8. Boundaries (third-party code)
9. Unit tests
10. Classes
11. Systems
12. Emergent design (simple design rules)
13. Concurrency
14. How to refactor (incrementalism)
15. Smell catalog (C, E, F, G, N, T)

---

## 1. Core attitude
- Messy code slows teams down over time; productivity drops as the mess grows. Cleaning continuously is cheaper than a big rewrite later.
- **Boy Scout Rule:** leave each piece of code a little cleaner than you found it. Small, frequent improvements compound.
- Code is read far more often than it is written, so optimize for the reader.
- Clean code reads like well-written prose: it does what the reader expects, with nothing surprising.

## 2. Names
- Names should reveal intent: why it exists, what it does, how it's used. If a name needs a comment, rename it.
- Avoid disinformation: don't call something a `list` if it isn't one; avoid names that differ only slightly.
- Make distinctions meaningful: no `data1`/`data2`, no noise words like `Info`, `Data`, `Manager` that add nothing.
- Use pronounceable and searchable names. Single letters only for tiny local scopes (loop counters).
- Avoid encodings: no Hungarian notation, no `m_` member prefixes, no type in the name.
- Classes/types: nouns. Functions/methods: verbs or verb phrases.
- One word per concept: don't mix `fetch`, `get`, `retrieve` for the same idea. Don't pun (using one word for two different ideas).
- Use solution-domain terms (patterns, algorithms) for technical concepts and problem-domain terms for business concepts.
- Add context through enclosing structure (class, module, namespace) rather than prefixes; don't add gratuitous context.
- Name length should scale with scope (N5): longer, more descriptive names for wider scopes.
- Names should mention side effects (N7): `getOrCreateSession`, not `getSession` if it creates.

## 3. Functions
- **Small**, then smaller. Blocks inside `if`/`while` ideally a single call. Deep nesting is a smell.
- **Do one thing.** A function does one thing if you can't meaningfully extract another function from it with a name that isn't just a restatement.
- **One level of abstraction per function.** Don't mix high-level policy with low-level detail.
- **Stepdown rule:** code reads top-down, each function followed by those at the next level of abstraction.
- **Switch/type dispatch:** bury it once (e.g. in a factory) and use polymorphism or dispatch elsewhere rather than repeating the switch.
- **Descriptive names**: a long descriptive name beats a short cryptic one plus a comment.
- **Arguments:** zero is best, one or two fine, three needs justification, more needs a very good reason. Group related args into an object/struct.
- **No flag (boolean) arguments**: they announce the function does two things; split it.
- **No output arguments**: return values instead of mutating inputs.
- **No hidden side effects**: a function shouldn't secretly change state its name doesn't promise (creates temporal coupling).
- **Command-query separation:** a function either changes state or answers a question, not both.
- **Prefer exceptions (or the language's idiomatic error mechanism) to returned error codes** that force immediate nested checks.
- **Extract try/catch bodies** into their own functions; error handling is "one thing."
- **DRY:** duplication is a root of much evil; extract it.
- Write it messy first, then refine with tests in place. Nobody writes clean functions in one pass.

## 4. Comments
- Comments don't make up for bad code. Prefer expressing intent in code (a well-named function or variable).
- **Acceptable comments:** legal headers, informative notes (e.g. what a regex matches), explanation of intent/why, clarification of unchangeable APIs, warnings of consequences, TODOs (sparingly), amplifying something non-obvious, docs for public APIs.
- **Bad comments:** mumbling, redundant restatement of code, misleading, mandated boilerplate docs, journal/changelog comments, noise, position markers/banners, closing-brace comments, attributions/bylines, **commented-out code** (delete it, since version control remembers), HTML in comments, nonlocal information, too much history, inobvious connection to the code, docs on non-public code that add nothing.

## 5. Formatting
- Formatting is communication. Follow team rules and use automated formatters.
- **Newspaper metaphor:** high-level summary at top, details lower down.
- Blank lines separate concepts; related lines stay tight together.
- Keep related things vertically close: variables near use, callers above callees, related functions together.
- Keep lines reasonably short; use horizontal whitespace to show precedence and grouping; don't hand-align columns.
- Never collapse scopes to save lines; indentation shows structure.

## 6. Objects and data structures
- Objects hide data behind behavior; data structures expose data and have no meaningful behavior. Pick one; **hybrids** (half object, half struct) get the worst of both.
- Procedural code makes adding functions easy; OO makes adding types easy. Choose based on which will change more.
- **Law of Demeter:** a method should talk to its immediate collaborators, not reach through chains (`a.getB().getC().doThing()`, a "train wreck"). Ask the object to do the work instead (tell, don't ask).
- DTOs/records are fine as plain data carriers; don't put business rules in them.

## 7. Error handling
- Use exceptions (or the language's idiomatic error type) rather than return codes, so the happy path stays readable.
- Write the try/catch/finally structure first when code can fail, defining a scope that leaves things consistent.
- Give errors context: what operation failed and why.
- Define error types by how callers need to handle them; wrap third-party errors behind your own.
- **Special case pattern:** define the normal flow so callers don't need special-case handling (e.g. return an empty collection or null object).
- **Don't return null; don't pass null.** Use empty collections, Option/Maybe types, or explicit errors.

## 8. Boundaries
- Wrap third-party APIs behind your own interface so changes in them touch one place and your code expresses your domain.
- Don't pass broad third-party types (e.g. raw maps/collections from a library) around your system.
- **Learning tests:** write tests against the third-party API to learn it and to detect breaking upgrades.
- For not-yet-existing APIs, define the interface you wish you had and adapt later.

## 9. Unit tests
- Three laws of TDD (summary): write a failing test before production code; write only enough test to fail; write only enough code to pass.
- Test code deserves the same care as production code; dirty tests become a liability and get abandoned.
- Readability is the main quality of a test: build-operate-check structure, domain-specific test helpers.
- Tests may use a relaxed standard for efficiency, but never for clarity.
- Aim for a single concept per test (one assert per test is a guideline, not a law).
- **F.I.R.S.T.:** Fast, Independent, Repeatable, Self-validating, Timely.

## 10. Classes
- Order: constants, variables (public then private), then public functions with their private helpers nearby.
- **Small**, measured by responsibilities, not lines. If you can't describe the class in ~25 words without "and/or/but," it does too much.
- **Single Responsibility Principle:** one reason to change.
- **Cohesion:** methods should use most of the instance variables. Low cohesion suggests a split.
- Splitting big functions often reveals new classes, so many small classes is the expected result.
- **Open/Closed:** organize so new behavior is added by adding code, not modifying existing classes.
- **Dependency Inversion:** depend on abstractions to isolate from change and enable testing.

## 11. Systems
- Separate construction (wiring objects together) from use. Keep startup/wiring in `main`, factories, or dependency injection.
- Handle cross-cutting concerns (logging, transactions, security) in a separate layer rather than scattered through business logic.
- Grow the architecture incrementally; postpone decisions until you have enough information.
- Use standards when they add demonstrable value; use domain-specific language to keep code close to the domain.

## 12. Emergent design: Kent Beck's simple design rules, in priority order
1. Runs all the tests.
2. Contains no duplication.
3. Expresses the programmer's intent.
4. Minimizes the number of classes and methods.

Rule 4 is lowest priority and counterbalances over-splitting: don't create classes and functions dogmatically.

## 13. Concurrency
- Keep concurrency code separate from other code (SRP).
- Limit the scope of shared data; prefer copies and independent threads.
- Know your library's thread-safe primitives and execution models (producer-consumer, readers-writers, dining philosophers).
- Keep synchronized/locked sections small; beware dependencies between synchronized methods.
- Get non-threaded code working first; make threaded code pluggable and tunable; treat spurious failures as possible threading bugs.
- When refactoring concurrent code, be extra conservative: structural moves can change interleavings.

## 14. How to refactor: incrementalism
- Don't make massive structural changes in one go. Make many tiny changes, running tests after each.
- First make it work, then make it right. Stop adding features when the code gets messy and clean up.
- Keep the system working at every step.

---

## 15. Smell catalog

### Comments
- **C1 Inappropriate information**: metadata (authors, change history, ticket numbers) that belongs in VCS/issue tracker.
- **C2 Obsolete comment**: outdated or wrong; fix or delete.
- **C3 Redundant comment**: says what the code already says.
- **C4 Poorly written comment**: if worth writing, write it well and briefly.
- **C5 Commented-out code**: delete it.

### Environment
- **E1 Build requires more than one step**: should be one simple command.
- **E2 Tests require more than one step**: should be one simple command.

### Functions
- **F1 Too many arguments.**
- **F2 Output arguments.**
- **F3 Flag arguments.**
- **F4 Dead function**: never called; delete.

### General
- **G1 Multiple languages in one source file**: minimize mixing (e.g. large HTML/SQL strings in code).
- **G2 Obvious behavior is unimplemented**: violates least surprise.
- **G3 Incorrect behavior at the boundaries**: edge cases unchecked.
- **G4 Overridden safeties**: disabled warnings, skipped tests, swallowed errors.
- **G5 Duplication**: copy-paste, repeated switch/if chains, similar algorithms.
- **G6 Code at wrong level of abstraction**: low-level details in high-level abstractions or vice versa.
- **G7 Base classes depending on their derivatives.**
- **G8 Too much information**: wide interfaces, too many exposed members.
- **G9 Dead code**: unreachable or unused; delete.
- **G10 Vertical separation**: declarations far from use.
- **G11 Inconsistency**: similar things done differently.
- **G12 Clutter**: unused variables, empty constructors, pointless code.
- **G13 Artificial coupling**: unrelated things bound together for convenience.
- **G14 Feature envy**: a method more interested in another object's data than its own.
- **G15 Selector arguments**: args that pick behavior (booleans, enums); split into functions.
- **G16 Obscured intent**: dense, cryptic expressions, magic values.
- **G17 Misplaced responsibility**: code where a reader wouldn't look for it.
- **G18 Inappropriate static**: should be polymorphic/instance behavior.
- **G19 Use explanatory variables**: name intermediate results.
- **G20 Function names should say what they do.**
- **G21 Understand the algorithm**: don't just fiddle until tests pass.
- **G22 Make logical dependencies physical**: depend explicitly rather than assuming.
- **G23 Prefer polymorphism to if/else or switch/case** (where repeated).
- **G24 Follow standard conventions.**
- **G25 Replace magic numbers with named constants.**
- **G26 Be precise**: e.g. correct types for money, handle nulls/concurrency deliberately.
- **G27 Structure over convention**: enforce design via structure (types, interfaces), not naming conventions.
- **G28 Encapsulate conditionals**: `if shouldBeDeleted(timer)` over a raw compound expression.
- **G29 Avoid negative conditionals**: `if buffer.shouldCompact()` over `if !buffer.shouldNotCompact()`.
- **G30 Functions should do one thing.**
- **G31 Hidden temporal couplings**: make call-order requirements explicit (e.g. pass results along).
- **G32 Don't be arbitrary**: structure should have a reason; make it communicate.
- **G33 Encapsulate boundary conditions**: compute `+1`/`-1` adjustments once, in a named variable.
- **G34 Functions should descend only one level of abstraction.**
- **G35 Keep configurable data at high levels**: defaults/constants up top, passed down.
- **G36 Avoid transitive navigation**: Law of Demeter, no train wrecks.

### Java-specific (generalize carefully, see language-adaptation.md)
- **J1** avoid long import lists (language-dependent; many modern style guides prefer explicit imports).
- **J2** don't inherit constants (use explicit imports/namespacing).
- **J3** prefer enums to integer/string constants.

### Names
- **N1 Choose descriptive names.**
- **N2 Names at the appropriate level of abstraction**: describe what, not how.
- **N3 Use standard nomenclature** (pattern names, domain terms).
- **N4 Unambiguous names.**
- **N5 Long names for long scopes.**
- **N6 Avoid encodings.**
- **N7 Names should describe side effects.**

### Tests
- **T1 Insufficient tests**: test everything that could break.
- **T2 Use a coverage tool.**
- **T3 Don't skip trivial tests.**
- **T4 An ignored test is a question about an ambiguity**: surface it.
- **T5 Test boundary conditions.**
- **T6 Exhaustively test near bugs**: bugs cluster.
- **T7 Patterns of failure are revealing.**
- **T8 Coverage patterns can be revealing.**
- **T9 Tests should be fast.**
