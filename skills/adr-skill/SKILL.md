---
name: adr-skill
description: Create and maintain Architecture Decision Records (ADRs) using the MADR bare template. Use when you need to propose, write, update, accept/reject, deprecate, or supersede an ADR; bootstrap an ADR folder and index; consult existing ADRs before implementation; or enforce MADR bare conventions.
metadata:
  internal: true
---

# ADR Skill

Use the MADR bare template as the only ADR format. Do not offer alternate ADR formats unless the target repo already has an incompatible ADR convention.

## ADR Shape

```markdown
---
status:
date:
decision-makers:
consulted:
informed:
---

# <!-- short title, representative of solved problem and found solution -->

## Context and Problem Statement

## Decision Drivers

* <!-- decision driver -->

## Considered Options

* <!-- option -->

## Decision Outcome

Chosen option: "", because

### Consequences

* Good, because
* Bad, because

### Confirmation

## Pros and Cons of the Options

### <!-- title of option -->

* Good, because
* Neutral, because
* Bad, because

## More Information
```

Fill every section with real content or remove entries that do not apply. Keep ADRs concise, but preserve the rationale: decision drivers, outcome justification, and option pros/cons explain why the chosen option won.

## When to Write an ADR

Write an ADR when a decision:

- Changes how the system is built or operated.
- Is hard to reverse once code depends on it.
- Affects future contributors or agents.
- Has real alternatives worth recording.

Do not write an ADR for routine implementation details, bug fixes, style preferences, or decisions already captured in an existing ADR.

## Workflow

### 1. Scan the Repo

Before drafting:

1. Look for existing ADRs in `contributing/decisions/`, `docs/decisions/`, `adr/`, `docs/adr/`, `docs/adrs/`, or `decisions/`.
2. Preserve the repo's existing directory and filename convention.
3. Read related ADRs so the new decision does not conflict with accepted decisions.
4. Check related code/docs enough to understand the decision context.

### 2. Capture Intent

Ask questions one at a time. Stop when you can fill the bare template without inventing content.

Core questions:

1. What decision are we recording?
2. Why does it need to be decided now?
3. What drivers, constraints, or forces matter?
4. What options were considered?
5. Which option is chosen, and why does it best satisfy those drivers?
6. What are the good, neutral, and bad consequences?
7. How will we confirm the decision is valid or complete?
8. Are there related ADRs, issues, PRs, or docs to link?

Before drafting, summarize the captured intent and ask the human to confirm or correct it.

### 3. Draft the ADR

Use `assets/templates/adr-bare.md`.

Preferred:

```bash
node /path/to/adr-skill/scripts/new_adr.js --title "Choose database"
```

Then replace every placeholder with real content. Keep the ADR self-contained and focused on the decision.

### 4. Review

Use `references/review-checklist.md` as a prompt list:

- Metadata follows repo convention.
- Context explains why the decision exists now.
- Decision drivers explain what mattered.
- Options are real alternatives.
- Outcome names the chosen option and gives the reason.
- Consequences and option pros/cons include tradeoffs, not just positives.
- Confirmation says how the decision will be validated or considered complete.

Surface only meaningful gaps.

## Consulting Existing ADRs

Before implementing architecture-sensitive changes, read relevant ADRs:

1. Find the ADR directory and index.
2. Scan titles and read related ADRs fully.
3. Treat accepted decisions as constraints.
4. If the code conflicts with an accepted ADR, flag it before changing direction.

## Updating Existing ADRs

- **Accept/reject**: update the `status` field.
- **Deprecate**: set `status: deprecated` and explain replacement path in `More Information`.
- **Supersede**: prefer creating a new ADR and linking old and new records.
- **Add learnings**: append dated notes instead of rewriting history.

Use `scripts/set_adr_status.js` for status changes.

## Bootstrap

When introducing ADRs to a repo with no ADR directory:

```bash
node /path/to/adr-skill/scripts/bootstrap_adr.js --dir adr
```

This creates an index and a first bare-template ADR for adopting ADRs.

## Resources

- `assets/templates/adr-bare.md` - the only ADR template.
- `assets/templates/adr-readme.md` - ADR directory index scaffold.
- `references/examples.md` - filled-out bare ADR example.
- `references/adr-conventions.md` - directory, naming, status, and lifecycle conventions.
- `references/review-checklist.md` - bare-template review prompts.
- `scripts/new_adr.js` - creates a new ADR using the bare template.
- `scripts/bootstrap_adr.js` - creates an ADR directory, index, and first ADR.
- `scripts/set_adr_status.js` - updates ADR status in-place.
