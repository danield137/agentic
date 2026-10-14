# Design docs

A design doc proposes a change before it is built: the problem, the proposed
design, the alternatives, and the risks. It lets reviewers agree on a direction
while changing it is still cheap. Once the change ships, the architecture doc
describes the result, and the design doc remains the record of the proposal.

## Profile

| Dimension | Design doc |
| --- | --- |
| Reader | Reviewers who approve the direction and engineers who will implement it. |
| Question | How should we build this change, and why? |
| Language | Accessible first, technical where it matters. Assume a capable reader who isn't deep in this component. Use precise terms where they change the decision: a data structure, a protocol, or an existing code concept. |
| Coverage | One change: its goal and non-goals, use cases, the current state, the proposed design, alternatives, compatibility, validation, decisions, and open questions. |
| Depth | Starts at handbook level for the problem and use cases, then goes to architecture level for the proposal. Implementation detail appears only where it changes the decision or its risk. |
| Intent | Reach a decision by making the tradeoffs reviewable before code exists. |
| Length | As short as still lets reviewers decide, usually a few pages. |
| Stop when | Reviewers can approve or reject the direction. Exact contracts go in the spec, each settled decision in an ADR, and the description of the shipped system in the architecture doc. |

## Guidelines

- Follow this order: goal, non-goals, example use cases, high-level flow,
  components, current state and layout, call-site example, constraints and
  tradeoffs, compatibility and phases, benchmark or validation contract, design
  decisions, and open questions. The template has a section for each.
- Ground the current state in the code. Read it; don't assume it.
- Show the call site: what client code looks like once the change exists, so
  reviewers can judge names and ergonomics before anything is built.
- State compatibility guarantees and blast radius. When a change is risky,
  propose a first phase of safe, preparatory changes before the risky switch.
- Name the benchmark, tests, or conformance checks that will show the change
  works.
- Present real alternatives with honest costs, and explain why the proposal
  wins.
- Keep a status in the front matter: draft, in review, accepted, implemented,
  or abandoned. Never describe a proposal in words that read as already built.
- Record each accepted decision as an ADR and link it. After the change ships,
  update the architecture doc and specs, and mark the design doc implemented.
- Keep open questions at the bottom and remove each one once it is answered.

## Good examples

The good and bad examples below come from an imaginary banking app. Use them
only to calibrate the level of detail. Don't reuse their names, facts, or
wording; a real design doc describes the actual change.

**Scope that reviewers can check** (banking app, "Scheduled transfers"):

> **Goal:** Let customers schedule a transfer for a future date.
>
> **Non-goals:** Recurring transfers, and transfers to other banks.
>
> **Use case:** Dana schedules a $1,200 rent payment for the 1st. At 06:00 on
> the 1st the transfer runs, or Dana is notified that funds are short.

It works because the scope fits in three lines and the use case grounds every
later decision.

**A call-site example:**

> ```python
> transfer = transfers.schedule(source, destination, Money("1200.00", "USD"), run_on=date(2026, 11, 1))
> transfers.cancel(transfer.id)  # allowed until the run starts
> ```

It works because reviewers can judge the API's names and shape before it
exists.

**Alternatives with real costs:**

> **Option A: a scheduler service that calls the Transfers API at run time.**
> The Ledger stays unchanged, but there is one more service to deploy and
> monitor.
>
> **Option B: store scheduled transfers in the Ledger and run them from a
> Ledger job.** No new service, but scheduling logic moves into the most
> sensitive component.
>
> **Proposal: Option A**, because the Ledger's guarantees stay easy to audit,
> and the scheduler can fail without touching balances.

It works because each option has a real cost and the choice follows from the
goals.

## Bad examples

**An implementation diary:**

> First I added `scheduler.py`, then a `run()` method that loops over pending
> transfers, and then I fixed a bug in the date parsing.

It fails because it narrates coding steps instead of proposing a design that
can be reviewed.

**A handbook chapter with no proposal:**

> Scheduling is useful because customers like to plan ahead. Many banks offer
> it.

It fails because it explains the concept but proposes nothing and decides
nothing.

**A proposal written as if it were built:**

> The scheduler runs every minute and posts due transfers to the Ledger.

It fails because, with no status and present-tense wording, readers mistake the
proposal for the running system.

## Template

Use `assets/templates/design-doc.md`.
