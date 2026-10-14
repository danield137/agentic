# ADR Conventions

## Directory

If the repo already has an ADR directory, keep it.

If no ADR directory exists, create the ADR in the root folder of the relevant code area. For example, for a storage-module change, use `docs/adr/storage/`. The scripts don't detect per-area folders, so pass the folder with `--dir`.

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

Number the headings as the template does: `## 1. Context and Problem Statement` through `## 6. More Information`. `Before and After`, `Consequences`, and `Confirmation` are subsections `4.1` to `4.3` of `Decision Outcome`, and each option under `Pros and Cons of the Options` is numbered `5.1`, `5.2`, and so on. The front matter is not numbered, so these numbers differ from the list above.

Every new or substantively updated ADR must also contain a `Before and After` subsection under `Decision Outcome`, with directly comparable Mermaid diagrams. This extends the bare template without changing its top-level MADR sections. Existing ADRs do not need retrofitting for status-only lifecycle updates, link corrections, or appended learnings.

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
