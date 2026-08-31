# ADR Conventions

## Directory

If the repo already has an ADR directory, keep it.

If no ADR directory exists, prefer:

- `docs/decisions/` when the repo already has a docs structure.
- `adr/` for smaller repos.

The scripts detect: `contributing/decisions/`, `docs/decisions/`, `adr/`, `docs/adr/`, `docs/adrs/`, then `decisions/`.

## Filenames

Prefer date-prefixed filenames:

`YYYY-MM-DD-short-title.md`

Examples:

- `2026-06-25-choose-database.md`
- `2026-06-25-adopt-adrs.md`

If the repo already uses slug-only filenames, follow that convention.

## Required Sections

Every ADR should use the bare template sections:

1. Metadata front matter
2. Context and Problem Statement
3. Decision Drivers
4. Considered Options
5. Decision Outcome
6. Consequences
7. Confirmation
8. Pros and Cons of the Options
9. More Information

## Status Values

Use the `status` field in front matter:

- `proposed`
- `accepted`
- `rejected`
- `deprecated`
- `superseded by [title](link)`

## Lifecycle

- Create a bare-template ADR when a meaningful architecture decision is being made.
- If the decision changes, prefer a new ADR that supersedes the old one.
- Link related ADRs both ways when superseding.
- Append dated notes for important follow-up learnings instead of rewriting history.
