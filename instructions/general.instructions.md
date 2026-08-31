---
name: General Personal Guidance
description: Personal always-on guidance for the user's agent sessions, including change decisions.
applyTo: '**'
---

# General Personal Guidance

## Change decision principles

- Before proceeding with any change, ask the user what backward- and forward-compatibility guarantees are required. Never infer or assume the compatibility contract.
- Judge a proposed change against the system's primary requirements and the larger design, not only the local symptom. For example, do not add retries to mask failures when performance is a primary requirement. If a change may conflict with a broader requirement or priority, identify the tension and ask the user before proceeding.
- For any user-facing addition, fix, change, or removal, including library behavior, UI, and APIs, ask: "Can I explain this change in 10 words or fewer?" If not, treat that as evidence that the design may be complicated rather than merely complex: simplify it or ask the user before proceeding. Prefer simple over complex, and complex over complicated.
