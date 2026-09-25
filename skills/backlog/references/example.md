# Backlog

Simple planning for improving a repeatable workflow. Start with the relevant design context.

## Mandatory instructions

- Follow the Quality gate below.
- Complete dependent tasks in listed order; later work waits for the evidence produced by earlier tasks.
- Record required review and integration evidence before a milestone is complete.

## Quality gate

Use **BRCGBC** for every item: **Benchmark -> Red test -> Change/Fix -> Green test -> Benchmark -> Conformance**. Required evidence is a baseline and comparable follow-up measurement, a check that fails before and passes after the change, the change itself, and a conformance result against the stated requirements.

If a required step cannot run, keep the item open and record the blocker or approved replacement under that item. No replacement gate is currently approved; any future replacement must be named here with its required evidence and explicit benchmark and conformance substitutes.

---

* (current) [ ] **M1:** Stabilize the core workflow
  * [ ] **M1T1:** Reduce avoidable variation in the primary outcome
    * Note: Use the same representative case and conditions for both benchmarks.
  * [ ] **M1T2:** Prevent incomplete input from being accepted
  * [ ] **M1T3:** Restore the expected outcome after interrupted work

* (next) [ ] **M2:** Improve efficiency without weakening requirements
  * [ ] **M2T1:** Reduce effort for the common path
  * [ ] **M2T2:** Preserve required checks under the improved path
    * Note: Conformance evidence must cover normal and boundary cases.
  * [ ] **M2T3:** Reduce delay in boundary cases

* (future) [ ] **M3:** Broaden conformance
  * [ ] **M3T1:** Support additional representative scenarios
  * [ ] **M3T2:** Resolve the remaining conformance gaps

---

## Archive

Finished milestones whose items satisfied the Quality gate are appended here, newest last.
