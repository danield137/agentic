---
name: General Personal Guidance
description: Personal always-on guidance for the user's agent sessions, including change decisions and the BRCGBC change protocol.
applyTo: '**'
---

# General Personal Guidance

## Change decision principles

- Before proceeding with any change, ask the user what backward- and forward-compatibility guarantees are required. Never infer or assume the compatibility contract.
- Judge a proposed change against the system's primary requirements and the larger design, not only the local symptom. For example, do not add retries to mask failures when performance is a primary requirement. If a change may conflict with a broader requirement or priority, identify the tension and ask the user before proceeding.
- For any user-facing addition, fix, change, or removal, including library behavior, UI, and APIs, ask: "Can I explain this change in 10 words or fewer?" If not, treat that as evidence that the design may be complicated rather than merely complex: simplify it or ask the user before proceeding. Prefer simple over complex, and complex over complicated.

## The BRCGBC protocol

Follow this only when I explicitly invoke `BRCGBC` or `RCG`. Run the steps in order and report the outcome of each one as you go.

`BRCGBC` is the full loop:

1. **Benchmark** — measure the affected path before changing anything, and record the baseline.
2. **Red test** — write a test that fails for exactly the reason being fixed, and confirm it actually fails.
3. **Change/Fix** — make the smallest change that addresses that failure.
4. **Green test** — confirm the red test now passes, and that related tests still pass.
5. **Benchmark** — re-measure the same path and compare against the step 1 baseline.
6. **Conformance** — run the project's existing conformance or compatibility suite (spec, API contract, cross-implementation) to confirm the contract still holds.

`RCG` is the minimal variant: steps 2, 3, and 4 only. Use it when benchmarking the change makes little sense and the project has no conformance tests.

Rules for both variants:

- Never skip the red step. A test that already passes before the fix proves nothing.
- Use the same command, input, and environment for both benchmarks. A comparison against a differently measured baseline is not a result.
- The conformance step runs tests that already exist. Do not write a new conformance suite as part of the loop.
- If a step cannot run — no benchmark harness, no conformance suite, no way to reproduce the failure as a test — say so and ask how to proceed instead of quietly dropping it.
