# ADR Review Checklist

Use this as a prompt list before finalizing a bare-template ADR.

## Required

- [ ] `status`, `date`, and `decision-makers` are filled in.
- [ ] `consulted` and `informed` are filled in or intentionally left blank.
- [ ] The title states the decision, not just the topic.
- [ ] The context explains why the decision exists now.
- [ ] The scope and important constraints are clear.
- [ ] Decision drivers capture the criteria, constraints, or forces that matter.
- [ ] Considered options are real alternatives.
- [ ] Decision outcome names the chosen option.
- [ ] The justification explains why this option best satisfies the decision drivers.
- [ ] Consequences include at least one cost, risk, or tradeoff.
- [ ] Confirmation explains how the decision will be validated or considered complete.
- [ ] Pros and cons cover each meaningful option without straw-manning rejected options.
- [ ] Related ADRs, issues, PRs, or docs are linked when relevant.

## Common Fixes

| Problem | Fix |
| --- | --- |
| Context pitches the solution | Move solution language to Decision Outcome. |
| Decision drivers are vague | Rewrite them as criteria or constraints that affect the choice. |
| Only one option is listed | Ask what was rejected and why. |
| All consequences are positive | Ask what becomes harder or riskier. |
| Pros/cons straw-man a rejected option | Add the real reason someone would choose it. |
| Confirmation is empty | Add a concrete signal, approval, rollout state, or validation result. |
