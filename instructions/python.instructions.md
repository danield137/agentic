---
name: Python Guidance
description: Personal Python coding conventions, typing preferences, and tooling expectations.
applyTo: '**/*.py'
---

# Python Guidance

Follow these conventions whenever writing or editing Python code.

## Code shape

- Do not write module-level docstrings or module-level documentation blocks. Prefer clear names and small functions; add focused function or class docstrings only when they explain non-obvious behavior.
- Do not use leading underscores for private module-level functions. If a helper is module-scoped, give it a normal name. Leading underscores are allowed for private class methods only.
- Keep imports at the top of the file. Only place imports inside functions or branches when the import is intentionally optional, expensive, or platform-specific.

## Typing and data modeling

- Always use `from __future__ import annotations`; do not quote type annotations just to handle forward references.
- Prefer typed dataclasses over arbitrary dictionaries for structured data.
- Prefer dataclasses with `slots=True` and `frozen=True` unless mutability, inheritance, or framework constraints require otherwise.

## Tooling

- Use a virtual environment for Python work.
- Use `uv` to manage packages and environments.
- Use `ty` for type checking and `ruff` for linting/formatting when the project does not already mandate different tools.
- For complex multi-package work, use Python workspaces rather than ad-hoc package wiring.
