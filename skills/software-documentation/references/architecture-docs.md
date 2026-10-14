# Architecture docs

An architecture doc describes how a system is built today and why: its major
components, how they interact, where data lives, and the decisions and
tradeoffs that shaped them. It is the map that maintainers keep current and
read before changing the system.

## Profile

| Dimension | Architecture doc |
| --- | --- |
| Reader | Engineers who maintain or extend this system. |
| Question | How is it built, and why? |
| Language | Technical and precise. Use the real names of components, protocols, data stores, and patterns, matching the code. Define project-specific terms once. |
| Coverage | Broad and deep. Every major component, every interaction between components, data ownership, and the cross-cutting mechanisms: consistency, caching, concurrency, failure handling, and security. |
| Depth | Structural. Component responsibilities, interaction sequences, entities and their relationships, and the decisions and tradeoffs behind them, with diagrams. Not every field, parameter, or error code. |
| Intent | Justify the structure, so a maintainer can change it without breaking the reasons it exists. |
| Length | As long as the system needs, split into sections per component and per key flow that each make sense on their own. |
| Stop when | The next sentence would list every field, parameter, type, or error of an interface; link to the spec. Or it would argue a new decision in full; write or link an ADR. |

## Guidelines

- Describe the system as built. Mark planned changes as planned and link their
  design docs; never describe a proposal as current.
- Zoom in one level at a time, the way the C4 model does: the system in its
  context of users and external systems, then its deployable parts and
  components, then the key flows.
- Draw diagrams in Mermaid so they stay diffable, and introduce each with one
  sentence saying what it shows:
  - `flowchart` for components, boundaries, dependencies, and data flow.
  - `sequenceDiagram` for one request or process across components.
  - `erDiagram` for the main entities and their relationships.
  - `classDiagram` only for the few central types whose structure shapes the
    design, never for every helper.
- Use the same names in diagrams, prose, and code.
- For each component, state its responsibility, what it owns, what it depends
  on, and what calls it.
- Tie each structural choice to the requirement that drives it, and link the
  ADR that records the full decision.
- For each key flow, cover partial failure, retries, duplicates, and races.
- Link to specs for exact interfaces and to code for implementation.

## Good examples

**A decision tied to its driver, with a sequence diagram** (banking app):

> Transfers must move money between two accounts atomically, so the Ledger
> keeps balances in PostgreSQL and applies each transfer as one database
> transaction. The document store used by Profiles can't update two documents
> atomically, so it stays out of the money path (see the ADR "Use PostgreSQL
> for the ledger").
>
> The sequence below shows a transfer from request to notification. The
> notification is sent only after the commit.
>
> ```mermaid
> sequenceDiagram
>     participant API as Transfers API
>     participant Ledger
>     participant DB as Ledger DB
>     participant Notify as Notifications
>     API->>Ledger: Post transfer
>     Ledger->>DB: Debit, credit, and outbox row in one transaction
>     DB-->>Ledger: Committed
>     Ledger-->>API: Transfer ID
>     Ledger->>Notify: Transfer completed (sent from the outbox)
> ```

It works because it names the requirement, the choice, and the rejected
alternative, and the diagram shows the order of events and the commit boundary.

**Machinery with its reasons** (recipe app):

> Similar recipes are computed when a recipe is uploaded, not when one is
> viewed: views outnumber uploads about 1,000 to 1, and the recipe page must
> render in under 200 ms. The Similarity Indexer updates `recipe_links` for the
> new recipe and its neighbors; the Similar Recipes API only reads. Taste
> profiles are reduced to three numbers with PCA, so scoring a neighbor costs a
> few multiplications. Results are cached per recipe for 24 hours and cleared
> when the recipe or one of its neighbors changes.

It works because this is where PCA, caching, and latency belong: each mechanism
appears with the requirement it serves.

**A component entry:**

> **Ledger** (`services/ledger`). Owns account balances and the entry history.
> Only the Ledger writes balances; other services read them through its API.
> Depends on the Ledger DB. Called by the Transfers API and the Statements job.

It works because responsibility, ownership, dependencies, and callers fit in
four lines.

## Bad examples

**A handbook in disguise:**

> Transactions are important in banking because money must never be lost, so
> the system handles them carefully.

It fails because it names the concept but no component, mechanism, decision, or
tradeoff.

**A spec in disguise:**

> `POST /v1/transfers`: `fromAccountId` (string, required), `toAccountId`
> (string, required), `amount.value` (decimal string, greater than 0),
> `amount.currency` (ISO 4217 code), ...

It fails because field-by-field contracts belong in the spec. The architecture
doc says which component owns the endpoint and what it guarantees.

**A diagram without a story:**

> A class diagram with 40 boxes, one per class and helper, and no sentence
> saying what to look for.

It fails because it is too deep for this level, and the reader can't tell which
relationships matter.

## Template

Use `assets/templates/architecture-doc.md`.
