# READMEs

Create or substantially restructure an entry README around the reader's fastest
path to value. Prefer concise, verified guidance over exhaustive technical
detail or historical narrative.

## Profile

| Dimension | README |
| --- | --- |
| Reader | Someone who just found the repository or tool and wants to use it. |
| Question | How do I get started? |
| Language | Plain and direct. Explain repository-specific terms at first use; use standard industry terms without defining them. |
| Coverage | Narrow: what it is, the common use, setup, a short mental model, and limitations. |
| Depth | Shallow: one verified, runnable example of the common path, and the architecture as a short numbered flow. |
| Intent | Get the reader to a first success fast, then point them onward. |
| Length | Short. A reader reaches a first successful run within a few minutes. |
| Stop when | A section starts teaching concepts in depth (handbook), justifying the design (architecture doc), or listing the full interface (spec). Link to those instead. |

## Workflow

1. **Inspect repository guidance and documentation.**
   - Read repository instructions and the current README/document hierarchy.
   - Find contribution guides, owning component docs, ADRs, and any existing
     README template or convention.
   - Preserve useful current content while removing duplication and stale
     history.
2. **Define the reader and first success.**
   - Identify the primary audience, the job they came to do, and the most common
     first successful action.
   - Lead with the repository's purpose and user value, not implementation
     details.
3. **Inventory and classify real entry points.**
   - Inspect scripts, binaries, packages, services, configuration, examples,
     and other supported entry points.
   - Determine ownership and dependency boundaries so each instruction points
     to the component that actually owns the behavior.
   - For each component that could be misunderstood, distinguish what it is,
     why it exists, when to use it, and what it does not do.
4. **Draft the reader journey.**
   - Use the default order: intro, usage example, setup instructions,
     architecture overview, then limitations or known issues.
   - Put a verified, runnable example of the common path immediately after the
     intro. Explain setup only after showing the outcome or use.
   - Explain architecture with a short numbered flow or pseudo-algorithm by
     default. Use UML, Mermaid, or ASCII only when the user explicitly asks or a
     diagram is materially clearer.
   - Adapt section names or omit genuinely inapplicable sections, but preserve
     the journey: purpose -> first use -> setup -> mental model -> limitations.
     Never leave empty headings.
5. **Validate every concrete claim.**
   - Check commands, paths, options, configuration names and fields, links, and
     claimed behavior against current source, built-in help, or configuration.
   - Prefer examples already present in the repository. Never invent commands,
     configuration, output, or supported behavior.
   - Check local links and anchors, command syntax, Markdown fences and tables,
     terminology, unintended jargon, duplication, and repository documentation
     tests when they exist.
   - For README-only work, use focused link, command/help, schema, and Markdown
     checks instead of a broad build unless the repository's documentation
     tests require it.
6. **Report the documentation result.**
   - Summarize the changed docs and the validation actually performed.
   - Do not imply that a command, build, or runtime flow was tested when it was
     only inspected.

For an audit-only request, report prioritized gaps with supporting evidence and
do not rewrite the README unless the user also asks for edits.

## Writing Rules

- Use concise, approachable, direct language and consistent terminology.
- Avoid jargon. Explain repository-specific terms only when needed, at first
  use; do not define standard industry terms unnecessarily.
- Keep detailed implementation material in its owning docs or ADRs and link to
  it instead of duplicating it in the entry README.
- State unsupported behavior, constraints, and known issues plainly. Never
  present future work as implemented.
- Keep examples focused on the target repository and its common path.

When documenting tools, scripts, or configuration, use a concise table with
verified values:

| Name or path | Purpose | When to use | Side effects | Key inputs |
| --- | --- | --- | --- | --- |
| `<verified item>` | `<why it exists>` | `<appropriate context>` | `<files, state, services, or none>` | `<arguments, fields, environment, or prerequisites>` |

Verify the owning component and placement of every listed item. Shared or
generic tools must not hide product-specific defaults; document the coupling or
move the detail to the product's owning documentation.

## Good examples

The good and bad examples below come from an imaginary recipe app. Use them
only to calibrate the level of detail. Don't reuse their names, facts, or
wording; a real README describes the actual repository.

**Purpose and first use up front** (recipe app):

> **similar-recipes**
>
> Suggests recipes similar to the one a cook is viewing, based on shared
> ingredients, taste, and prep time.
>
> ```bash
> curl http://localhost:8080/v1/recipes/r42/similar
> ```
>
> Returns the three most similar recipes, best match first.

It works because the purpose fits in one sentence and a verified command shows
the result before any setup.

**The architecture as a short numbered flow:**

> 1. When a recipe is uploaded, its ingredients are categorized and it is
>    connected to recipes that share ingredients.
> 2. A request for similar recipes scores the connected recipes on
>    ingredients, taste, and prep time.
> 3. The three best matches are returned. The handbook's "Similar recipes"
>    topic explains more.

It works because three steps give a mental model and link onward instead of
explaining internals.

**Limitations stated plainly:**

> - Recipes with no ingredients get no suggestions.
> - A new recipe starts appearing in suggestions about a minute after upload,
>   not instantly.

It works because each constraint is a plain fact, without hedging or promises
of future work.

## Bad examples

**History before purpose:**

> This project started at a 2021 hackathon, when three of us wanted better
> dinner ideas. Over the years it grew into...

It fails because the reader came to use the tool. History delays the first
success and rarely belongs in a README.

**An unverified, hedged command:**

> Run `make all` (should work on most systems; if not, try the Docker setup,
> which may be out of date).

It fails because the command wasn't verified, and the hedging tells the reader
the README can't be trusted.

**An internals tour:**

> **Modules**
>
> - `indexer/`: `GraphBuilder`, `EdgeWeigher`, `PcaReducer`, ...
> - `api/`: `SimilarHandler`, `CacheMiddleware`, ...

It fails because a class-by-class inventory is architecture detail. The README
needs one short flow and a link.

## Template

When the target repository has its own README template or convention, it takes
precedence. Otherwise start from `assets/templates/repository-readme.md`, whose
sections follow the reader journey above. Use it as a starting point, not a
requirement to manufacture content.
