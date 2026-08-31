---
name: backlog
description: Create and maintain lean, milestone-based backlog documents for planning work. Use when asked to create a backlog, update backlog items, organize planned work into current/next/future milestones, turn discussion or TODOs into backlog tasks, renumber backlog ids, or keep planning separate from design docs, current-status docs, ADRs, and code review.
---

# Backlog Skill

Create simple planning backlogs in the format defined by `assets/templates/backlog.md`.

Backlog docs carry **what/when**. Design docs carry **why**. Current-status docs carry **what exists now**. ADRs record committed decisions. Code review comments belong in PRs.

## Core Rules

- Milestones are enough structure. Use top-level milestone checkbox lines, not heavy section headings with prose.
- Keep **at most 3-4 milestones**.
- Always include at least `(current)` and `(next)`. Put work that does not realistically fit in next under `(future)`.
- Use milestone ids `M1`, `M2`, etc. Use task ids `M1T1`, `M1T2`, `M2T1`, etc.
- Every milestone and task starts with a checkbox: `[ ]` planned, `[x]` done, `[-]` skipped/not happening.
- Milestone line shape: `* (current) [ ] **M1:** Stabilize the vector foundation`.
- Task line shape: `  * [ ] **M1T1:** Finalize a stable storage format`.
- Bold only the milestone/task id, not the full text.
- Tasks should be one-line checkboxes. Do not add `Outline`, `Context`, `Implementation hints`, `Commits`, or `Skipped because` sub-sections.
- Add at most one high-signal note per task. The note should capture a non-obvious constraint, decision boundary, blocker, reference/prototype caveat, or acceptance criterion.
- Avoid implementation walkthroughs. Backlog is not design, not status, and not code review.
- Prefer simple verbs: `Finalize`, `Build`, `Validate`, `Benchmark`, `Decide`, `Document`.
- Keep reference/prototype status explicit. A prototype PR can be reference material without being the implementation baseline.
- Separate immediate work from user-facing exposure. Public profiles, public policies, and public UX usually belong in the last/future milestone.
- Fold TODOs into work items, but do not copy TODO.md. Convert TODOs into clear tasks that are useful from `dev`.
- When a milestone finishes, move the whole milestone to the bottom under `---` / `## Archive`.

## Item Shape

Every planned item uses this structure:

```markdown
* (current) [ ] **M1:** Short milestone outcome
  * [ ] **M1T1:** Finalize the first task
    * Note: One non-obvious constraint, boundary, blocker, or acceptance criterion.
  * [ ] **M1T2:** Validate the second task
```

Ids are monotonic within each milestone. If moving items between milestones, renumber them.

## Workflow

### 1. Find or Create the Backlog

Look for an existing backlog before creating one:

1. `Backlog.md`
2. `BACKLOG.md`
3. `docs/backlog.md`
4. `docs/Backlog.md`

If none exists, create one from `assets/templates/backlog.md`.

### 2. Capture Planning Intent

Ask only what is needed to fill the backlog without inventing content:

1. What is the current milestone trying to achieve?
2. What belongs next?
3. What should be deferred to future work?
4. Which user-facing/public exposure belongs last?
5. Is any PR, branch, or prototype only reference material?
6. Are there TODOs to fold into clear tasks?
7. For each task, is there one non-obvious note worth preserving?

Do not over-plan. If the user gives too many items, keep Current and Next focused and move the rest to Future work.

### 3. Write or Update Items

For each item:

- Milestone line: `* (current|next|future) [ ] **M{n}:** Outcome`.
- Task line: `  * [ ] **M{n}T{n}:** Simple-verb task`.
- Optional note: `    * Note: One high-signal note.`
- Keep notes rare. If every task has multiple notes, the backlog is becoming a design doc.
- Prefer repo-relative links only when they materially clarify reference/prototype status or an acceptance criterion.

Smell test: if a line reads like "how to implement this", move it to a design doc or omit it.

### 4. Review

Before finalizing:

- Current and next both exist.
- There are no more than 3-4 milestones.
- Milestones are top-level checkbox bullets, not prose-heavy sections.
- Every task begins with `[ ]`, `[x]`, or `[-]`.
- Task lines are one-line checkboxes.
- Bold applies only to ids (`**M1:**`, `**M1T1:**`), not the full text.
- Each task has at most one note.
- Ids are monotonic after any move.
- Immediate work is separated from public/user-facing exposure.
- Reference/prototype status is explicit when relevant.
- TODOs are converted into useful tasks, not copied.
- Design rationale and implementation walkthroughs are absent.
- Finished milestones are appended under the bottom `---` / `## Archive` section only when every task in the milestone is `[x]` or `[-]`.

## Resources

- `assets/templates/backlog.md` - canonical backlog file template.
- `references/example.md` - filled example that demonstrates the expected style and level of detail.
