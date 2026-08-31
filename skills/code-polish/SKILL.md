---
name: code-polish
description: Reviews code for smells, dead code, duplication, Single Responsibility violations, extensibility problems, and likely bugs, then fixes selected findings under a red/green test loop. Use for explicit cleanup, polish, tech-debt, or multi-finding code-quality requests, and to fix numbered findings from an earlier pass. Do not use for routine PR review, formatting-only work, or one known bug.
---

# Code Polish

Find what is worth fixing, rank it, and report it. Do not edit during review.

## 1. Agree on scope and exclusions

Ask which scope to review:

- Uncommitted changes
- The branch diff against its base
- A named file or directory
- The whole codebase

Never assume the whole codebase. Before reading code:

1. Load repository instructions, architecture guidance, and existing test/lint
   configuration.
2. Record `git status` so user changes are never mistaken for review work.
3. Enumerate eligible files. Skip generated, vendored, minified, lock, and
   binary files unless the user includes them explicitly.

For a large scope, state the file count and confirm it. Review independent
directories in passes, then run one cross-directory pass for duplication,
responsibility leaks, and boundary problems. Track eligible, reviewed, and
skipped counts.

## 2. Find and verify problems

Every finding must point at code read in this session. Trace enough callers,
tests, registries, configuration, and dynamic lookup paths to support it.

Report only `high` or `med` confidence:

- `high` — directly demonstrated by control/data flow, tests, or tooling.
- `med` — evidence is strong, but dynamic behavior prevents complete proof.
- `low` — speculative; do not report it.

Use one primary category per finding. Prefer the most specific category;
`smell` is the fallback. Merge copies of the same underlying problem.

| Category | What counts |
| --- | --- |
| `correctness` | Wrong results, unhandled failures, bad boundaries, races, leaks, ignored return values |
| `dead code` | Unreachable branches, unused functions/exports/flags, obsolete or commented-out code |
| `duplication` | Repeated logic, especially copies that have drifted |
| `SRP` | A unit has unrelated jobs or changes for unrelated reasons |
| `extensibility` | A plausible next change is blocked by hardcoded cases or assumptions |
| `smell` | Deep nesting, flag arguments, primitive obsession, feature envy, leaky abstractions |

Do not report formatting, style-only lint findings, missing tests/docs unless
asked, rewrites disguised as findings, or hypothetical extensibility needs.
A correctness problem remains reportable even if a configured analyzer also
finds it.

## 3. Rate impact and fix risk

Severity is the cost of leaving the problem; risk is the cost of the proposed
fix.

| Sev | Meaning |
| --- | --- |
| 5 | Data loss, security exposure, crash, or silently wrong results |
| 4 | Likely bug or blocker for an expected change |
| 3 | Real problem without urgency |
| 2 | Worth fixing while already in the area |
| 1 | Nit |

| Risk | Meaning |
| --- | --- |
| `low` | Local, behavior-preserving, and covered |
| `med` | Shared path or boundary behavior; tests need inspection |
| `high` | Cross-cutting, public contract, or hard to verify |

Rate risk for the fix actually proposed, not an ideal redesign.

## 4. Present findings

Open with coverage and category counts:

```text
34/41 eligible files reviewed; 7 generated/vendor files skipped —
correctness: 3, SRP: 2, duplication: 2, dead code: 1, smell: 1
```

Sort by severity descending, then confidence (`high` first), then risk
(`low` first). Keep the top 25 and state how many lower-ranked findings were
dropped.

| # | Location | Category | Sev | Risk | Conf | Problem | Fix |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | src/api/orders.py:142 | correctness | 5 | low | high | A retried call reads a response after it closes, returning a stale body. | Build and consume the response inside each attempt. |
| 2 | src/api/orders.py:88 | SRP | 4 | med | med | OrderService validates payloads and writes the ledger, coupling unrelated changes. | Move payload validation into an OrderValidator. |

Rules:

- IDs are sequential across the whole review, including multi-directory
  passes. Once shown, never renumber or reuse them.
- Locations are repo-relative `path:line` links. For duplication, list
  comma-separated locations in one row.
- Problem and Fix are each one concrete sentence, not a principle.

After the table, offer to fix rows by ID and wait. When the user selects rows,
read and follow `references/fix-workflow.md`.
