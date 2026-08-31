# Fix Workflow

Use this workflow only after the user selects finding IDs.

## Prepare the execution set

1. Confirm the referenced findings table is available and still maps each ID to
   code. Otherwise ask for the table or repeat the review.
2. Resolve lists and ranges such as `1, 2, 5-8`, then echo the IDs back.
3. Recheck `git status`. Never modify or stage unrelated user work. An
   overlapping dirty file or any pre-existing staged change is a readiness
   question; do not unstage it. If this is not a Git repository, ask before
   proceeding and never initialize one implicitly.
4. For each item, re-read its code, callers, tests, and contracts. Identify:
   - The behavior to change or preserve
   - The red test or equivalent proof
   - The smallest fix and its regression surface
   - Dependencies, overlaps, and unresolved choices
5. Order prerequisites before dependents, then correctness before descending
   severity. If one fix resolves several rows, implement it once and mark the
   others `resolved by #N`.

If an item needs input, handle those items one at a time before implementation.
Show the current snippet, why it is wrong, the proposed fix snippet, its risk or
ambiguity, and the exact questions. Stay on that item until it is ready or the
user skips it.

Classify factual failures accurately:

- `not reproduced` — the evidence does not support the original finding.
- `blocked` — required tools, dependencies, or an existing failure prevent
  safe work.
- `skipped during preparation` — the user chooses not to resolve a readiness
  question.

These are not design postponements. State the final execution set, then run it
to completion without checking in between items.

## Fix one item at a time

Before each item, relocate its symbol and confirm it still exists; earlier
fixes may have moved or resolved it.

1. **Red.** For a behavioral bug, add or run a test that fails for the expected
   reason. Record unrelated baseline failures.
2. **Fix.** Change only this item.
3. **Green.** Run the new test and existing tests around it.
4. **Commit.** Stage only this item's files or hunks, inspect
   `git diff --cached`, then make one commit. Never push.

For dead code, prove there are no callers, including registries, string lookup,
and reflection; the existing suite is the green step. For behavior-preserving
refactors, establish passing characterization coverage before editing. If a
factual finding cannot be demonstrated, mark it `not reproduced`; do not turn
it into a design question.

## Handle bugs found along the way

Ask: **can this be fixed correctly without asking the user?**

The answer is Yes only when a test, contract, or caller proves one mechanical
correction. Wrong argument order, inverted conditions, null dereferences,
off-by-one bounds, or wrong constants are examples, not automatic permission.
Ambiguous behavior is always No.

- **Yes:** queue it as `A1`, `A2`, and so on. Finish or revert the current item
  first, then give the bug its own red/fix/green/commit loop. If it blocks the
  current item, revert that item, fix the blocker cleanly, then retry.
- **No:** do not edit it. Queue it as `N1`, `N2`, and so on for the Newly found
  bugs table.

## Postpone only after implementation starts

Postpone an item only when new evidence changes a ready estimate: its fix
regresses another area, conflicts with a contract, or exposes a larger design
decision. Revert the partial item, record the conflict and question, and move
on. Environment or tooling failures are `blocked`, not postponed.

## Run the integration gate

After all item commits, run the broader relevant tests and build once against
the combined result. If this fails, identify the responsible commit or
interaction. Fix a mechanical regression under its own loop; otherwise revert
the responsible item and mark it postponed. Do not report completion while the
combined result is red.

## Report completion

Open with selected, fixed, skipped, blocked, not-reproduced, postponed, tests
added, and commits made. Count only tests genuinely added.

| # | Location | Outcome | Tests added | Commit |
| --- | --- | --- | --- | --- |
| 1 | src/api/orders.py:142 | fixed | 2 | a1b2c3d |
| 2 | src/api/orders.py:88 | resolved by #1 | 0 | a1b2c3d |
| 3 | src/api/retry.py:54 | postponed after start — contract conflict | 1 | — |
| A1 | src/api/client.py:73 | auto-fixed — reversed arguments | 1 | 9f8e7d6 |

Then include, when nonempty:

1. **Open questions** — only questions exposed after implementation started.
2. **Newly found bugs** — unfixed `N#` rows using the findings-table columns.
3. **Not yet addressed** — unselected original IDs and their current locations.

End with the integration-gate result and say plainly that nothing was pushed.
