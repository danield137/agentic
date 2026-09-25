---
name: backlog
description: Create and maintain lean, milestone-based backlog documents for planning work. Use when asked to create a backlog, update backlog items, organize planned work into current/next/future milestones, turn discussion or informal task lists into backlog tasks, assign stable area-based task IDs or migrate older backlogs to them, or keep planning separate from design docs, current-status docs, decision records, and review feedback.
---

# Backlog Skill

Create simple planning backlogs in the format defined by `assets/templates/backlog.md`.

Backlog docs carry **what/when** and the mandatory instructions needed to complete the work. Design docs carry **why** and implementation detail. Current-status docs carry **what exists now**. Decision records capture committed choices. Review feedback stays in its review context.

## Mandatory instructions

The backlog is the primary entry point for agents taking on work. Before the active milestones, persist every durable instruction that affects how work is selected, implemented, validated, reviewed, integrated, deployed, released, or considered complete. State the instruction concisely in the backlog or provide a mandatory link to its authoritative details.

Do not copy full design docs, process manuals, decision records, or status reports into the backlog. Persist only the directive and authoritative link needed to discover the requirement. Examples include the quality gate, validation or conformance requirements, compatibility or rollout gates, dependency or ordering constraints, review or integration prerequisites, and environment restrictions.

## Task areas

Every backlog persists a `## Task areas` section after `## Mandatory instructions` and before `## Quality gate`. It is a two-column `| Area | Covers |` table that lists each area code in use and says, in plain words, what the area covers. Keep rows for areas that appear only in the Archive. Add a new area to the table when a task first uses it.

## Quality gate

Every backlog persists a short `## Quality gate` section near the top, before active milestones. Use **BRCGBC** unless the backlog explicitly replaces it:

`Benchmark -> Red test -> Change/Fix -> Green test -> Benchmark -> Conformance`

An item or milestone is complete only when evidence exists for every required step. If a step cannot run, the backlog records the blocker or approved replacement. A replacement gate must be named, state the evidence required before completion, and explicitly identify what replaces any benchmark or conformance step.

## Core Rules

- Milestones are enough structure. Use top-level milestone checkbox lines, not heavy section headings with prose.
- Keep **at most 3-4 milestones**.
- Always include at least `(current)` and `(next)`. Put work that does not realistically fit in next under `(future)`.
- Use milestone IDs `M1`, `M2`, etc. They describe timing and order, not identity.
- Task IDs are an area code plus a three-digit number, such as `REMINDERS001`, `SYNC002`, or `SHARING001`.
- Area codes are uppercase, with words separated by underscores, as in `TASK_LIST`. They must be understandable to someone who doesn't know the backlog: prefer a plain word, such as `REMINDERS`, over a cryptic abbreviation, such as `RMDR`. Abbreviate only when the result stays obvious, as in `AUTH` for authentication.
- Task IDs are stable. An ID never changes when its task moves between milestones, and numbers are never reused. A new task takes the next free number in its area.
- In notes and other docs, refer to a task by its ID in backticks, such as `SYNC001`.
- Every milestone and task starts with a checkbox: `[ ]` planned, `[x]` done, `[-]` skipped/not happening.
- Milestone line shape: `* (current) [ ] **M1:** Stabilize the core workflow`.
- Task line shape: `  * [ ] **REMINDERS001:** Finalize the completion criteria`.
- Bold only the milestone/task ID, not the full text.
- Tasks should be one-line checkboxes. Do not add `Outline`, `Context`, `Implementation hints`, `Change records`, or `Skipped because` sub-sections.
- Add at most one high-signal note per task. The note should capture a non-obvious constraint, decision boundary, blocker, reference/prototype caveat, or acceptance criterion.
- Avoid implementation walkthroughs. Backlog is not design, not status, and not a review record.
- Prefer simple verbs: `Finalize`, `Build`, `Validate`, `Benchmark`, `Decide`, `Document`.
- Keep reference/prototype status explicit. A prototype can be reference material without being the implementation baseline.
- Separate immediate work from external or user-facing exposure, which usually belongs in the last/future milestone.
- Fold informal task lists into work items, but do not copy them verbatim. Convert them into clear tasks that remain useful from the active work context.
- When a milestone finishes and its completed items satisfy the persisted quality gate, move the whole milestone to the bottom under `---` / `## Archive`.

## Item Shape

Every planned item uses this structure:

```markdown
* (current) [ ] **M1:** Short milestone outcome
  * [ ] **REMINDERS001:** Finalize the first task
    * Note: One non-obvious constraint, boundary, blocker, or acceptance criterion.
  * [ ] **SYNC001:** Validate the second task
```

A task ID comes from the task's area, not its milestone, so the ID stays the same when the task moves between milestones.

## Workflow

### 1. Find or Create the Backlog

Look for an existing backlog before creating one:

1. `Backlog.md`
2. `BACKLOG.md`
3. `docs/backlog.md`
4. `docs/Backlog.md`

If none exists, create one from `assets/templates/backlog.md`.

When updating an existing backlog, add `## Mandatory instructions`, `## Task areas`, and `## Quality gate` before the active milestones if any is missing. Preserve explicitly named requirements and replacement gates; otherwise use BRCGBC.

If the backlog still uses `M{n}T{n}` task IDs, migrate it once: map each task to an area ID, add the `## Task areas` table, and update references to the old IDs in notes and other docs. Record the ID rule in its Mandatory instructions, using one of the backlog's own IDs as the example:

```markdown
- Task IDs are an area code plus a three-digit number, such as `REMINDERS001`. An ID never changes when its task moves between milestones, and numbers aren't reused. The area codes are listed in Task areas; add new areas there in the same style. This replaces the `M1T1` style for tasks; milestones keep `M1`, `M2`, and so on.
```

### 2. Capture Planning Intent

Ask only what is needed to fill the backlog without inventing content:

1. What is the current milestone trying to achieve?
2. What belongs next?
3. What should be deferred to future work?
4. Which user-facing/public exposure belongs last?
5. Is any draft, reference, or prototype only supporting material?
6. Are there informal task lists to fold into clear tasks?
7. For each task, is there one non-obvious note worth preserving?

Identify any durable requirement that affects selection, implementation, validation, review, integration, deployment, release, or completion. When details live elsewhere, capture a concise directive and mandatory authoritative link rather than copying the source.

Use BRCGBC by default without asking. Ask about a replacement only when a required step does not fit or the backlog already names another gate. Capture the replacement name, its required completion evidence, and the explicit substitute for any benchmark or conformance step.

Do not over-plan. If the user gives too many items, keep Current and Next focused and move the rest to Future work.

### 3. Write or Update Items

For each item:

- Persist `## Mandatory instructions` before the Quality gate and active milestones. Include each completion-affecting requirement directly or through a mandatory authoritative link.
- Persist `## Task areas` between Mandatory instructions and the Quality gate. Add an area there the first time a task uses it.
- Persist `## Quality gate` before the active milestones; chat guidance alone is not sufficient.
- Follow the persisted gate for item and milestone work. Mark an item `[x]` only after its required evidence exists.
- Record a gate-wide replacement in the Quality gate section. Record an item-specific blocker or approved replacement in that item's optional note.
- Milestone line: `* (current|next|future) [ ] **M{n}:** Outcome`.
- Task line: `  * [ ] **AREA001:** Simple-verb task`, where `AREA` is a code listed in Task areas and `001` is the next free number in that area.
- Optional note: `    * Note: One high-signal note.`
- Keep notes rare. If every task has multiple notes, the backlog is becoming a design doc.
- Prefer local links only when they materially clarify reference/prototype status, a mandatory instruction, or an acceptance criterion.

Smell test: if a line reads like "how to implement this", move it to a design doc or omit it.

### 4. Review

Before finalizing:

- `## Mandatory instructions` appears before the Quality gate and active milestones.
- Every durable requirement affecting selection, implementation, validation, review, integration, deployment, release, or completion is stated there or discoverable through a mandatory authoritative link.
- Linked details are summarized as concise directives; full design docs, process manuals, decision records, and status reports are not duplicated.
- `## Task areas` appears after Mandatory instructions and before the Quality gate, and its `| Area | Covers |` table lists every area code in use.
- `## Quality gate` appears before the active milestones.
- BRCGBC is present as `Benchmark -> Red test -> Change/Fix -> Green test -> Benchmark -> Conformance`, unless the backlog explicitly names a replacement.
- A replacement gate states the evidence required before completion and what replaces any benchmark or conformance step.
- Completed items and milestones have satisfied the persisted gate; blocked steps or approved replacements are recorded in the backlog.
- Current and next both exist.
- There are no more than 3-4 milestones.
- Milestones are top-level checkbox bullets, not prose-heavy sections.
- Every task begins with `[ ]`, `[x]`, or `[-]`.
- Task lines are one-line checkboxes.
- Bold applies only to IDs (`**M1:**`, `**REMINDERS001:**`), not the full text.
- Each task has at most one note.
- Task IDs are unique, use an area code listed in Task areas, never change when a task moves, and numbers aren't reused.
- Area codes are uppercase, separate words with underscores, and are clear to someone who doesn't know the backlog.
- No task still uses an `M{n}T{n}` ID; a migrated backlog records the ID rule in Mandatory instructions, and references use the new IDs.
- Immediate work is separated from public/user-facing exposure.
- Reference/prototype status is explicit when relevant.
- Informal task lists are converted into useful tasks, not copied.
- Design rationale and implementation walkthroughs are absent.
- Finished milestones are appended under the bottom `---` / `## Archive` section only when every task in the milestone is `[x]` or `[-]` and every completed task satisfies the persisted quality gate.

## Resources

- `assets/templates/backlog.md` - canonical backlog file template.
- `references/example.md` - filled example that demonstrates the expected style and level of detail.
