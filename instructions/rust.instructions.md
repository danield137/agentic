---
name: Rust Performance Guidance
description: Personal Rust priorities and performance optimization guidance.
applyTo: '**/*.rs'
---

# Rust Performance Guidance

When writing or editing Rust code, prioritize concerns in this strict order:

1. Correctness
2. Performance
3. Extensibility
4. Readability

## Optimization

- Never dismiss an optimization as a micro-optimization or premature optimization. Point out every optimization opportunity you identify.
- Consider every relevant optimization, including SIMD, OS-specific, task-specific, and constraint-specific approaches.
- Always prefer zero-copy designs and avoid unnecessary allocations or data movement.
- Type-specialize hot paths instead of relying on generics.
