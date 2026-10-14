---
name: software-documentation
description: Write, restructure, review, and audit software documentation at the right level of detail for its reader - READMEs, onboarding handbooks, design docs, architecture docs, specs and API references, and architecture decision records (ADRs). Use when writing docs for a project, component, API, or decision; creating or substantially rewriting a README; writing a design doc or proposal, an architecture overview with diagrams, a handbook or onboarding guide, or an interface spec; proposing, writing, updating, accepting, deprecating, or superseding an ADR, bootstrapping an ADR folder, or consulting existing ADRs before architecture-sensitive changes; reorganizing or consolidating a docs folder; or judging whether a doc is too deep, too shallow, or the wrong type. Not for code comments or docstrings, changelogs or release notes, typo fixes, summarizing existing docs, or explaining code in chat.
---

# Software Documentation

Most documentation goes wrong at the level of detail, not the facts: jargon in
an onboarding page, a schema dump in an overview, rationale buried in a
contract, three levels of depth in one paragraph. Choose the document type
first. The type fixes the reader, the question the document answers, and how
deep it goes.

## Document types

| Type | Answers | Reader | Purpose | Guide |
| --- | --- | --- | --- | --- |
| Comment | Why is this code surprising? | Someone reading this code | Explain the local reason | [Comments](#comments) |
| README | How do I get started? | Someone new to the repository or tool | Reach a first success | `references/readmes.md` |
| Handbook | What should I understand? | An engineer new to the product or its domain | Build intuition | `references/handbooks.md` |
| Design doc | How should we build this change, and why? | Reviewers and implementers of the change | Reach a decision before building | `references/design-docs.md` |
| ADR | What did we decide, and why? | Future maintainers | Record one decision | `references/adrs.md` |
| Architecture doc | How is it built, and why? | Maintainers of the system | Justify the structure | `references/architecture-docs.md` |
| Spec | Exactly what is the contract? | Implementers and tools | Define, not explain | `references/specs.md` |

Pick the type whose question matches what the reader needs. When a request
mixes questions, split the content: each piece goes in the document whose
question it answers, and the documents link to each other. If the user asks for
content that belongs in a different type, such as a schema in a handbook, say
where it belongs and why, then follow the user's decision.

## Levels of detail

Think of the types as zoom levels on a map, from farthest to closest:

1. **README**: what it is and how to start using it.
2. **Handbook**: the concepts, rough step-by-step outlines, and where things
   live.
3. **Architecture doc**: components, interactions, data, and the decisions
   behind them.
4. **Spec**: every field, type, error, and limit.

Design docs and ADRs each cover one change or one decision. A design doc frames
the problem at handbook level and describes the proposal at architecture level.
An ADR records one decision at architecture level. A comment sits next to the
code and explains only the local reason.

The table below shows one feature, "find similar recipes" in an imaginary
recipe app, at each level. It only illustrates the levels of detail; don't
reuse its names, facts, or wording.

| Type | What it says |
| --- | --- |
| README | Suggests three recipes like the one you're viewing. Try it: `curl localhost:8080/v1/recipes/r42/similar`. |
| Handbook | Each ingredient gets a category and a taste profile. Recipes that share ingredients are connected. The recipes connected to the one you're viewing are scored on shared ingredients, taste, and prep time, and the top three are shown. Connections live in the `recipe_links` table. |
| Architecture doc | The Similarity Indexer precomputes connections when a recipe is uploaded, because views outnumber uploads about 1,000 to 1. Taste profiles are reduced to three numbers with PCA to make scoring cheap, and results are cached per recipe for 24 hours. |
| Spec | `GET /v1/recipes/{recipeId}/similar` takes `limit` (integer, 1 to 10, default 3) and returns `items` ordered by `score` descending, ties by `recipeId` ascending. An unknown recipe returns `404 recipe_not_found`. |
| Comment | `# Break ties by recipe ID so results don't reorder between cache refreshes.` |

## Shared rules

1. **Write for the type's reader.** Use the language level in the type's
   profile. Don't default to "simple" or to "technical".
2. **Step down one level at a time.** Start at the reader's level. Introduce a
   term only when stepping down, define it at first use, and signal the step,
   for example "In more detail:". Never jump more than one level in a
   paragraph.
3. **Concepts before machinery.** Say what happens and why before how it is
   implemented.
4. **One owner per fact.** Put each fact in the document whose question it
   answers. Elsewhere, name where it lives and link to it instead of copying
   it.
5. **Stop at the type's stopping rule.** When the next sentence needs the level
   below, link to the document at that level, or note that it is missing.
6. **Verify every concrete claim.** Check commands, paths, names,
   configuration, and behavior against the code, built-in help, or schemas.
   Never present planned work as built.
7. **Follow the repository first.** Its existing templates, folders, naming,
   and conventions win over this skill's defaults.

## Document structure

These rules apply to every document type except comments.

1. **Number the sections.** Leave the title unnumbered and number everything
   below it: `1.`, `1.1`, `1.1.1`, `1.1.1.1`. Renumber when you add, remove, or
   move a section.
2. **Nest at most four levels.** Four levels of numbered sections, `##` through
   `#####`, is the maximum. If the content needs a fifth, split the document or
   flatten the outline.
3. **Add a table of contents to longer documents.** When a document runs longer
   than about two screens, put an unnumbered `Contents` section after the title
   and any introduction, listing the numbered sections as nested links. Design
   docs, architecture docs, specs, and multi-topic handbooks usually need one;
   READMEs and ADRs usually don't. Keep it in sync with the headings.
4. **Keep the existing structure when editing.** Apply these rules to new
   documents and to documents you restructure. For a smaller edit to an
   existing document, follow its current numbering and layout.

For example, a handbook for an imaginary recipe app might nest four levels like
this. Copy the shape, not the names:

```markdown
## Contents

- [1. Systems](#1-systems)
  - [1.1 Recommendation system](#11-recommendation-system)
    - [1.1.1 UX](#111-ux)
      - [1.1.1.1 Recommended recipe carousel](#1111-recommended-recipe-carousel)

## 1. Systems

### 1.1 Recommendation system

#### 1.1.1 UX

##### 1.1.1.1 Recommended recipe carousel
```

## Workflow

1. **Choose the type.** Identify the reader and their question, and match them
   to the table above. For several questions, plan one document per question
   and the links between them.
2. **Read the guide.** Open the type's guide in `references/` and its template
   in `assets/templates/`. Each guide starts with a profile (reader, question,
   language, coverage, depth, intent, length, and stopping rule), followed by
   that type's rules and examples.
3. **Inspect the repository.** Find existing documents and conventions, and the
   code, configuration, and tests behind each claim. Gather facts at the
   type's level and no deeper.
4. **Draft.** Fill the template at the type's level. Omit sections that
   genuinely don't apply; never leave empty headings or placeholder text.
5. **Review.** Check the draft against the guide's profile, especially its
   stopping rule, and against its bad examples. Check numbering, nesting depth,
   the table of contents, links, anchors, commands, Markdown, and Mermaid
   syntax.
6. **Report.** Summarize what changed, where each kind of content went, and
   which checks actually ran. Don't imply a command was run when it was only
   read.

For an audit, classify each document by the question it actually answers,
compare it with that type's profile, and report misplaced or missing content
and where it belongs. Don't rewrite unless asked.

To reorganize or consolidate documentation, classify each section by type, move
it to the document that owns it, merge duplicates, remove content only after
confirming it is stale, and replace copies with links.

## Comments

Comments have no separate guide. Add one only where the code would surprise a
careful reader: a non-obvious reason, a constraint imposed from elsewhere, a
workaround, or an invariant. Say why, not what. If the explanation needs more
than a few lines, move it to the architecture doc or an ADR and link to it from
the comment.

## How the documents connect

- A README links to the handbook for concepts and to the spec for the full
  interface.
- A handbook links each topic to the architecture doc, specs, and code.
- An architecture doc links each structural decision to its ADR and each
  interface to its spec.
- A design doc proposes a change, and its decisions are recorded as ADRs. Once
  the change ships, the architecture doc and specs are updated to describe it,
  and the design doc is marked implemented.

## Resources

- One guide per type: `references/readmes.md`, `references/handbooks.md`,
  `references/design-docs.md`, `references/adrs.md`,
  `references/architecture-docs.md`, and `references/specs.md`.
- ADR details: `references/adr-conventions.md`, `references/adr-examples.md`,
  `references/adr-review-checklist.md`, and
  `references/adr-template-variants.md`.
- Templates in `assets/templates/`: `repository-readme.md`, `handbook.md`,
  `design-doc.md`, `adr-bare.md`, `adr-readme.md`, `architecture-doc.md`, and
  `spec.md`.
- ADR file helpers in `scripts/`: `new_adr.js`, `bootstrap_adr.js`, and
  `set_adr_status.js`. See `references/adrs.md` for usage.
