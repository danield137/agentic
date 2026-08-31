---
name: Design and Architecture Principles
description: Personal guidance for design and architecture work before implementation.
applyTo: '**'
---

# Design and Architecture Principles

Design and architecture work is subtle. Do not jump directly into implementation when the task changes structure, contracts, data flow, APIs, storage, deployment behavior, or cross-component boundaries.

## Writing style and depth

- Use accessible language. Assume the reader is capable, but not already deep in this component.
- Avoid technically heavy wording unless the term has real significance, such as a data structure name, known design pattern, protocol, specific technology, or existing code concept that must be named precisely.
- Put the right depth in the right place: start with the goal, example use cases, high-level flow, and component responsibilities before diving into storage layout, algorithms, benchmarks, tradeoffs, decisions, and open questions.
- Prefer concrete examples and plain explanations before abstractions. Use precise technical detail where it changes the decision, contract, performance, correctness, or implementation risk.
- For larger design docs, a good shape is: goal, example use cases, high-level system flow, components, current state/layout, constraints and tradeoffs, benchmark or validation contract, design decisions, and open questions.

## Required workflow

1. **Gather enough context before proposing a solution.** Search for existing implementations, similar concepts, prior art, codebase conventions, adjacent abstractions, and relevant tests. Prefer reusing or extending existing patterns over inventing a new one. Ground analysis in the actual code: read the relevant code before recommending or claiming, rather than assuming, and verify claims — including PR-review comments — against the code before asserting them.
2. **Restate the problem in your own words.** Explain the understood goal, constraints, relevant context, and non-goals, then ask the user to confirm before continuing.
3. **Make a high-level pass first.** Sketch the algorithm, data flow, component responsibilities, or pseudocode before writing production code. Keep this implementation-independent enough to expose design tradeoffs early.
4. **Validate the call-site shape.** Before finalizing the design, assume the implementation already exists and show what client code would look like when using it. Confirm that the resulting API, ergonomics, naming, and integration points make sense before implementing.
5. **Structure larger changes into phases.** Always consider user compatibility and blast radius. If a change is risky, propose an initial phase made only of safe, preparatory changes before the final risky switch.
6. **Write an ADR before implementation.** Once the direction is clear, create an Architecture Decision Record in the root folder of the relevant code area. For example, for a storage-module change, place it under `docs/adr/storage/{change-title}.md`.

## Decision standard

A design is not ready for implementation until the context is grounded in the existing codebase, the problem statement is confirmed, the high-level approach is reviewed, the client-facing shape is acceptable, compatibility and blast radius are addressed, and the ADR records the chosen direction.
