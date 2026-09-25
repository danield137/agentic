# Backlog

Simple, time-ordered planning. Keep **at most 3-4 milestones** and only plan as far as
we will realistically reach. Milestones carry the timing; tasks carry the work.

Design docs carry why. This backlog carries what/when. Current-status docs carry what exists now.

## Mandatory instructions

- Follow the Quality gate below.
- {Concise completion-affecting instruction or mandatory authoritative link. Include reference status, ordering, validation, review, compatibility, rollout, or environment constraints when relevant. Write "None beyond the Quality gate" when none applies.}

## Task areas

| Area | Covers |
| --- | --- |
| `{AREA}` | {What this area covers, in plain words} |
| `{OTHER_AREA}` | {What this area covers, in plain words} |

## Quality gate

Use **BRCGBC** for every item: **Benchmark -> Red test -> Change/Fix -> Green test -> Benchmark -> Conformance**. An item is complete only with evidence for each required step.

If a required step cannot run, record the blocker or approved replacement in this backlog. A replacement gate must be named here, state its required completion evidence, and explicitly say what replaces any benchmark or conformance step.

---

* (current) [ ] **M1:** {current milestone outcome}
  * [ ] **{AREA}001:** Finalize {work item}
    * Note: {One non-obvious constraint, decision boundary, blocker, reference caveat, or acceptance criterion.}
  * [ ] **{AREA}002:** Validate {work item}
  * [ ] **{OTHER_AREA}003:** Benchmark {work item}

* (next) [ ] **M2:** {next milestone outcome}
  * [ ] **{OTHER_AREA}004:** Decide {work item}
    * Note: {Optional one high-signal note.}
  * [ ] **{AREA}003:** Build {work item}

* (future) [ ] **M3:** {future milestone outcome}
  * [ ] **{AREA}004:** Build {future work item}
  * [ ] **{OTHER_AREA}005:** Document {future work item}

* (future) [ ] **M4:** {user-facing exposure milestone}
  * [ ] **{AREA}005:** Expose {public profile, policy, or user-facing surface}
    * Note: Public surfaces belong late because users can discover and depend on them.

---

## Archive

Finished milestones whose items satisfied the Quality gate are appended here, newest last.

* (done) [x] **M0:** {finished milestone outcome}
  * [x] **{OTHER_AREA}001:** {Completed task}
    * Note: {Optional one-line result or evidence reference if useful.}
  * [-] **{OTHER_AREA}002:** {Skipped task}
    * Note: {Why this is not happening.}
