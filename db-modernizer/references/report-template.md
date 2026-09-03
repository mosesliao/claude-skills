# Audit Report Template

Use this exact structure for `audit-report.md`. Every issue must carry evidence (a count,
a query, or example values) and a severity.

```markdown
# Database Audit: [database name]

**Engine:** [engine + version]  ·  **Tables:** [n]  ·  **Total rows:** [~n]  ·  **Date:** [date]

## Executive Summary
[3–6 sentences: overall health, the worst offenders, and whether the data is trustworthy
enough for business insights as-is. State the headline recommendation.]

## Inventory
| Table | Rows | Has PK | FKs | Notable issues |
|-------|-----:|:------:|:---:|----------------|

## Findings
Group by severity. For each finding:

### [SEVERITY] Short title
- **Where:** table.column(s)
- **Problem:** what's wrong
- **Evidence:** count / sample values / query
- **Impact:** why it hurts data quality or the redesign
- **Fix direction:** how Phase 2/3 will address it

Severities: **Critical** (blocks trustworthy insights / migration), **High**, **Medium**, **Low**.

## Normalization Assessment
[Which tables violate 2NF/3NF, the repeating groups / transitive dependencies found, and
the decomposition proposed.]

## Data-Quality Scorecard
| Dimension | Status | Notes |
|-----------|:------:|-------|
| Completeness (nulls) | | |
| Consistency (enums/formats) | | |
| Uniqueness (dupes) | | |
| Referential integrity (orphans) | | |
| Validity (types/ranges) | | |

## Risks & Open Questions
[Ambiguities that need the user's business knowledge before redesign — e.g. "is status
'X' still meaningful?", "can we drop rows with no customer?"]

## Recommended Next Steps
[What Phase 2 will produce, pending sign-off.]
```
