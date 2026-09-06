---
name: interactive-brainstorm
description: Explores a topic as an adaptive question-and-answer search tree, giving provisional answers before opening sharper questions and following or backtracking between branches interactively. Use when the user says brainstorm, mindmap, topic exploration, explore an idea, think through an open-ended idea, or wants to investigate a broad opportunity, project, product, or life decision. Do not use for narrow factual questions, routine implementation, or concrete either-or choices that need a direct recommendation.
---

# Interactive Brainstorm

Explore the topic like a mental A* search: scan broadly, answer enough to learn,
descend where the user sees energy, and backtrack when a branch is a blunder.
Optimize for useful new distinctions per turn—"learn more, faster"—rather than
for reaching a solution quickly.

## Maintain the search state

Start with the topic as the root. Show the current path and depth compactly on
every turn:

```text
Path: Local coffee shop → Will it make a profit? (level 2)
```

Keep track of:

- the current question;
- the user's perspective and goal;
- conclusions and assumptions gathered along the path;
- unexplored sibling questions worth returning to.

Default to the user's perspective. Do not silently switch to the perspective of
a customer, player, employee, or other actor. Make that a visible branch when it
is useful.

## Expand one frontier at a time

At the root, surface five to eight genuinely different questions. On later
turns, surface the questions created by the current answer.

Every node must be a question worth answering, not a category disguised as a
node:

- Weak: `Business — pricing, margins, and competition`
- Strong: `Will it make a profit? — It may, but the early estimate suggests
  daily volume is the fragile assumption.`

For each question:

1. State the question in plain language.
2. Give a short best-current answer.
3. Mark consequential uncertainty as fact, estimate, assumption, or hypothesis.

The short answers let the user judge which branch deserves depth. After the
user chooses one, answer that question more substantially before presenting its
next frontier. Never produce a questions-only interrogation.

Use this lens palette to avoid blind spots, but do not force it into every
topic:

- **Essence:** What is this really?
- **Motivation:** Why does the user want it, and will that motive endure?
- **Business:** How can it create and capture value?
- **Physics:** What does objective reality permit or require?
- **Execution:** What path could make it real?
- **Alternatives:** What else could satisfy the same underlying goal?

Add, merge, or omit lenses when the topic demands it. Prefer a few fundamental
questions over a flat inventory of narrower subquestions.

## Choose high-information branches

Build the frontier from questions likely to:

- change whether the idea is attractive or viable;
- expose a hidden assumption, constraint, or contradiction;
- distinguish between meaningfully different versions of the idea;
- connect several previously separate observations;
- be answered cheaply enough to guide the next step.

Avoid synonymous branches, exhaustive checklists, and premature implementation
detail. Do not tunnel into the first interesting connection before scanning the
other major ways of viewing the topic.

When a useful answer requires current or niche facts, research them. When it
requires economics, scale, time, or feasibility, make a back-of-the-envelope
estimate with visible assumptions and sensitivity. When evidence is unavailable,
give a hypothesis and say what observation would test it.

## Let answers generate questions

Use this rhythm:

```text
question → provisional answer → sharper questions → user chooses → deeper answer
```

Derive the next questions from the answer just given. For example, an estimated
break-even point should produce questions about the few assumptions that most
affect it, not a generic business checklist.

End each turn with one focused branch-selection question. Prefer choices that
mirror the visible frontier, while allowing the user to redirect in their own
words. Do not descend more than one level per turn unless the user explicitly
asks for an autonomous pass.

## Navigate corrections and backtracking

Treat user corrections as updates to the search model:

- If the level is wrong, climb and rebuild the frontier at the requested depth.
- If the perspective drifted, restate it and regenerate the affected questions.
- If several branches all matter, connect them into a causal model instead of
  forcing an arbitrary choice.
- If a branch is a blunder or loses energy, return to the nearest useful
  frontier without discarding conclusions already earned.
- If the user redirects the topic, begin a fresh root scan using what their
  corrections revealed about how they think.

Do not defend the old framing or continue down a corrected branch.

## Converge only when requested

Continue exploring until the user asks to consolidate, decide, plan, or build.
Then summarize:

1. the strongest current answers;
2. material evidence and assumptions;
3. the causal connections discovered;
4. unresolved questions ranked by information value;
5. the cheapest next experiments or decisions.

If the user asks to implement something, leave brainstorming mode and follow the
normal implementation workflow rather than continuing to expand the tree.
