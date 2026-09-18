---
name: change-review
description: >
  Runs a five-headed first-pass review of a pull request, branch diff, commit range, or local
  changes. Use when the user asks to "review this PR", "review my changes", "review my diff",
  perform a "change review" or "first-pass review", identify what they should flag, help review a
  change, or draft review comments. Launches five independent concern-specific reviewers, then
  verifies, merges, and deduplicates their findings without autonomously posting anything.
---

# Change Review

Act as a first-pass review helper. The user reads the proposed review, edits it, and decides what
actually gets said.

## Permission gate

Never submit, post, edit, resolve, approve, reject, or reply to a review comment without the user's
explicit approval. Produce the review as a proposal only. After the user approves specific
comments, post only those comments and only through the tool they approve.

## Required five-headed workflow

Always use this workflow for a code-change review.

1. **Resolve one exact review scope.**
   - Identify the pull request, comparison base, commit range, or staged/unstaged diff.
   - Include all changed production code, tests, configuration, and documentation in that scope.
   - If the target or base is ambiguous, ask the user before reviewing.

2. **Understand the change before judging it.**
   - The orchestrator reads the complete change once without critiquing it.
   - Capture the purpose, selected approach, important design choices, and blast radius.
   - Produce a short internal executive summary and give the same summary and exact review scope to
     every reviewer.

3. **Launch exactly five independent `code-review` subagents in parallel.**
   - Use one subagent for each review head below; do not add a sixth general reviewer.
   - Every subagent reads the complete scoped change but reports only its assigned concern.
   - Give every subagent the repository instructions, comparison base, changed-file scope, purpose
     summary, and the shared reviewer contract below.
   - Subagents are read-only. They must not edit files, post comments, or spawn more reviewers.
   - If five independent reviewers are unavailable, say so rather than faking five-head coverage.

4. **Verify the reports.**
   - Collect all five reports before synthesizing.
   - The orchestrator checks every reported file/line, call path, and failure scenario against the
     code. Discard unsupported or out-of-scope findings.
   - The orchestrator synthesizes; it does not perform a separate sixth review or invent findings
     that no specialist reported.

5. **Merge and deduplicate.**
   - Treat findings as duplicates when they describe the same root cause and affected behavior,
     even if they use different wording or point at different symptoms.
   - Keep one merged finding with all relevant concern tags and affected locations.
   - Preserve the strongest concrete evidence, the highest justified severity, and the clearest
     smallest fix. Do not raise severity merely because another reviewer used a stronger label.
   - Keep findings separate when similar symptoms have different root causes.
   - Call out meaningful cross-domain overlap without repeating the comment.

6. **Escalate genuine conflicts and tricky solutions.**
   - If reviewers recommend incompatible fixes, first check whether code evidence resolves the
     disagreement.
   - If a real tradeoff remains, do not silently choose. Surface the alternatives, consequences,
     compatibility and blast-radius implications, and the decision the user needs to make.
   - Treat a fix as tricky when it changes ownership or lifetime, layering, a public contract,
     persisted state, deployment ordering, rollback/roll-forward behavior, or requires broad churn
     for a local symptom.
   - Use `ask_user` for one decision at a time before implementing, posting, or presenting one
     alternative as settled.

7. **Present one ranked review, not five raw reports.**
   - Sort by severity, then confidence, then blast radius.
   - Show compact coverage results for all five heads so the user can see that each ran.
   - If a head found nothing significant, say so in the coverage line; do not manufacture a finding.

## The five review heads

### 1. Codebase consistency

Review only consistency with established codebase style and its existing design tradeoffs.

Look for:
- nearby prior art that the change should reuse or deliberately diverge from;
- established layering, ownership, async, error-handling, logging, instrumentation, testing, and
  resource-lifetime patterns;
- framework or repository helpers that make the new code fit the surrounding system;
- unexplained deviations from local conventions or decisions.

Do not report generic SOLID advice, standalone correctness bugs, compatibility concerns, or naming
preferences unless the issue is specifically an inconsistency with demonstrated repository
practice. Cite the existing comparison point.

### 2. SOLID and Clean Architecture

Review only general-purpose design quality and extensibility.

Look for:
- mixed responsibilities and misplaced logic;
- incorrect ownership or lifetime boundaries;
- dependency direction, inversion, interface shape, and testability;
- open/closed extensibility, hidden type checks, duplicated policy, and leaky abstractions;
- coupling that makes the next implementation or execution substrate require special cases.

Do not report codebase style, naming polish, or compatibility by itself. Explain the concrete change
or extension that the design makes unsafe or unnecessarily difficult.

### 3. Correctness and edge cases

Review only whether the change behaves correctly.

Look for:
- invalid state transitions, broken invariants, data loss/corruption, and incorrect results;
- null, empty, boundary, overflow, ordering, concurrency, retry, timeout, cancellation, and partial
  failure behavior;
- cleanup and resource leaks, stale state, race conditions, and error classification;
- tests that assert a proxy rather than the actual required behavior.

Every finding must include a concrete failure scenario or reproducible path. Do not report pure
design taste or readability.

### 4. Compatibility and evolution

Review only compatibility across time and versions.

Look for:
- source, binary, behavioral, API, CLI, config, protocol, and persisted-data compatibility;
- existing callers, wrappers, test doubles, automation, and default behavior;
- safe rollback after the new code has run and safe roll-forward from older state;
- mixed-version deployment, migration sequencing, feature gating, and future extension contracts.

Do not report generic architecture concerns unless they create a specific compatibility,
rollback, or roll-forward failure. State which old/new combination breaks.

### 5. Naming, logical flow, and readability

Review only whether an external developer can understand and safely modify the code.

Look for:
- names that obscure intent, use mixed vocabulary, or combine responsibilities;
- control flow that hides the happy path, important state transitions, or failure behavior;
- APIs whose call-site shape is surprising or difficult to use correctly;
- unnecessary indirection, cognitive load, comments that restate code, or missing explanation for
  non-obvious policy.

Apply this naming priority: codebase consistency > contextual consistency > standardization >
readability. Do not re-report correctness or architecture findings merely because they also make the
code harder to read.

## Shared reviewer contract

Each specialist must:

- inspect the full scoped change and enough adjacent code/tests to verify claims;
- stay inside its assigned concern and explicitly return `No significant findings` when appropriate;
- report only actionable findings with confidence **7/10 or higher**;
- avoid hypothetical concerns without a concrete caller, scenario, extension, or repository
  comparison point;
- prefer the smallest sound fix and identify when that fix is not actually small;
- use these severities:
  - **BLOCKING** - concrete bug, data/safety risk, build break, or contract break that must be fixed;
  - **WARNING** - meaningful risk or design problem that should be addressed;
  - **SUGGESTION** - worthwhile non-blocking improvement;
  - **NIT** - very small polish point; use sparingly.

Use this report shape for each finding:

```text
Severity:
Confidence: N/10
File and lines:
Title:
Evidence or failure scenario:
Smallest sound fix:
Proposed review comment:
Possible overlap: <head name or none>
```

## Review voice

The final proposed comments should be:

- **Terse and specific:** short comments pinned to exact lines.
- **Socratic:** prefer a focused question that makes the author justify the choice.
- **Calibrated:** use `nit:` for trivia and reserve firmness for concrete problems.
- **Warm and humble:** use plain informal language and acknowledge real uncertainty.
- **Grounded:** reference an existing mechanism, caller, failure path, or convention.
- **Actionable:** include a small alternative when one is clear.

## Final output

Present the merged review in this shape:

```text
* Executive summary: <purpose, approach, blast radius>
* Opinion: <one-line readiness assessment>
* Coverage: codebase consistency N; SOLID/architecture N; correctness N; compatibility N;
  naming/readability N
* Merged comments:
  1. [SEVERITY] [Concern tag(s)] file:line - <proposed comment>
     Evidence: <concrete scenario>
     Smallest fix: <fix>
     Confidence: N/10
* Decisions needed:
  1. <only genuine conflict/tricky tradeoff; omit section when empty>
```

Do not include the five raw reports unless the user asks for them. If there are no significant
findings, say so directly after the coverage line.

After presenting the review, ask which comments, if any, the user wants to post. Post nothing until
they explicitly approve the specific comments.
