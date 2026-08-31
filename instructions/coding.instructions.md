---
name: General Coding Guidance
description: Personal language-agnostic coding conventions for readable, maintainable implementation work.
applyTo: '**/*.cs,**/*.py,**/*.ts,**/*.tsx,**/*.js,**/*.jsx,**/*.go,**/*.rs,**/*.java,**/*.kt,**/*.cpp,**/*.c,**/*.h,**/*.hpp'
---

# General Coding Guidance

Follow these conventions whenever writing or editing code.

- Prefer simple synchronous code over async code unless async is explicitly requested or clearly required by an existing interface.
- Prefer short-circuiting and early returns over nested control flow. Reducing nesting is important.
- Prefer minimizing the diff when applying a requested change. Avoid renaming things, moving lines, or reshaping nearby code unless there is a clear correctness, readability, or maintainability need.
- If it is not broken, do not touch it. Do not simplify, extract, generalize, maintain, or otherwise improve unrelated working code unless the user explicitly asks for that change. If you notice a worthwhile improvement, mention it as a proposal during design or implementation planning instead of making it silently.
- Do not lay groundwork for isolated small features. Avoid overdesigning abstractions, extension points, frameworks, or future-proofing until the feature actually needs them. Build the smallest sound solution that solves the current problem and keeps the blast radius low: anyone can build a bridge, but a good engineer builds one that just barely holds.
- Keep functions short and readable; avoid going over roughly 20 lines of code. Split longer logic into clear workflow steps such as `load_input()`, `validate()`, `do_something()`, and `do_next_thing()`.
- When naming things (functions, variables, types, etc.), resolve naming choices by this priority, highest first:
  1. **Codebase consistency**: match how similar existing code names the concept (e.g., if the codebase refers to the API server as "Frontend", align to that).
  2. **Contextual consistency**: keep names internally consistent within the change.
  3. **Standardization**: prefer names that are standard in the industry (design patterns, known architectural components like gateway, HTTP server, API, SDK).
  4. **Readability**: prefer names that are easy to reason about (e.g., `IsUserAuthorized` over `RequestHasAuthPropertyMatchingUser`; `check_that_user_is_permitted` over `user_permission_validation`).
  On collision between these, always rank strictly by this order.
- After a coding pass, make another pass to verify names and code are globally coherent, not just locally correct: a name that made sense in isolation may not fit once the whole feature is in place. Reconcile such names before finishing.
- When finishing feature work, run a small targeted subset of tests. Find code paths affected by the change, pick 2-5 relevant test classes and 1-5 tests in each class, and run them directly (for example, use the repository's existing test selector). Do not run full suites unless the user explicitly asks.
