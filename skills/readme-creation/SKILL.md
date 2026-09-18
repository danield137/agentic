---
name: readme-creation
description: Create, write, rewrite, simplify, restructure, audit, and improve repository README files so they are approachable, accurate, and useful. Use for substantial README work, documenting a project or tool, or adding usage, setup, architecture, limitations, or known issues. Do not use for typo-only edits unless the user asks to apply this skill or its template.
---

# README Creation

Create or substantially restructure an entry README around the reader's fastest
path to value. Prefer concise, verified guidance over exhaustive technical
detail or historical narrative.

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

## Default Skeleton

Specific README templates may be added to this skill later. When the target
repository has a repository-specific template, it takes precedence over this
generic default.

````markdown
# <Project or tool name>

<One or two sentences explaining what it is, who it helps, and the value it
provides.>

## Usage Example

```<shell-or-language>
<Verified common, runnable example>
```

<Expected result or what the reader should notice.>

## Setup Instructions

<Prerequisites and verified setup steps.>

## Architecture Overview

1. <First verified step in the main flow.>
2. <How the owning component processes or routes it.>
3. <What result or side effect completes the flow.>

## Limitations / Known Issues

- <Verified unsupported behavior, constraint, or known issue.>
````

Use the skeleton as a starting point, not a requirement to manufacture content.
