# Adaptive Interactive Brainstorming

Status: Accepted

## Context

Static idea lists either stay too shallow or commit too early to the first
interesting branch. Purely Socratic brainstorming has the opposite problem: it
keeps asking questions without contributing enough answers to expose useful new
questions.

The desired workflow resembles a mental A* search. It scans broadly, descends
where interest or uncertainty is high, and backtracks when a branch is a
blunder. Its heuristic is "learn more, faster."

## Decision

Use an explicit, user-steered search tree:

1. Represent every node as a question, not merely a category.
2. Show a compact path and depth on every turn.
3. At each frontier, present orthogonal questions with short provisional
   answers.
4. Deepen the question the user selects, answer it concretely, and derive the
   next frontier from that answer.
5. Prefer branches with high information value over branches that merely invite
   more detail.
6. Preserve the user's perspective unless another perspective is made an
   explicit branch.
7. Backtrack freely and retain useful conclusions from abandoned branches.

The skill may use Essence, Motivation, Business, Physics, Execution, and
Alternatives as a lens palette, but these are prompts rather than a fixed
taxonomy.

## Trigger boundary

Load for explicit brainstorming, mind mapping, and topic exploration, and for
broad, open-ended ideas or decisions. Do not take over narrow factual questions,
routine implementation work, or concrete either-or decisions that call for a
direct recommendation.

## Consequences

The interaction takes more turns than a one-shot idea dump, but each turn
produces both useful content and a better-informed choice of where to think
next. Visible state makes depth and backtracking legible. Provisional answers
must clearly distinguish facts, estimates, and hypotheses so that breadth does
not create false confidence.
