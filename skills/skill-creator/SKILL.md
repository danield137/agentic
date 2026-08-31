---
name: skill-creator
description: Create, review, and improve GitHub Copilot CLI skills. Use when the user wants to write a new skill, turn a repeated workflow or prompt into a skill, fix a skill that never loads or loads too often, review a SKILL.md, or measure and tune how reliably a skill triggers.
---

# Skill Creator

Build a skill for Copilot CLI, then check that it actually loads when it should.

A skill is a folder with a `SKILL.md` inside it. Copilot reads every skill's
`name` and `description` at startup, but only pulls the body into context when
it judges the skill relevant. So a skill has two separate jobs: the description
decides *whether* it loads, and the body decides *what happens* once it does.
Those fail independently, and you debug them differently.

## When a skill is the right answer

Use a skill for a procedure that matters occasionally: a release checklist, a
tricky migration, a house style for a specific kind of file.

Use custom instructions instead when the guidance applies to nearly every task,
since instructions are always in context. Reach for a skill when loading the
guidance every single time would be waste.

If the user is really describing a one-off task, say so rather than building a
skill around it.

## Workflow

Find out where the user already is and start there. If they have a draft, skip
to reviewing it. If they only have an idea, start at step 1.

1. **Pin down the trigger.** Ask what the user would be typing when they'd want
   this skill. Collect their actual phrasing. This is the raw material for both
   the description and the eval set, and it is the step most worth slowing down
   for.
2. **Write the draft.** Create the directory and `SKILL.md`.
3. **Validate.** Run `scripts/validate_skill.py` — it is free and instant.
4. **Try it live.** Reload and give it one of the real queries from step 1.
5. **Measure, if triggering is the problem.** Build an eval set and run
   `scripts/run_eval.py`.
6. **Tune the description.** Run `scripts/optimize_description.py`, or edit by
   hand using the failures as evidence.

Steps 5 and 6 each spawn real `copilot -p` runs and consume quota. Do not start
them without telling the user what it will cost, and do not start them at all
until the body is settled — otherwise you are tuning a moving target.

## Where skills live

| Location | Scope |
| --- | --- |
| `.github/skills/<name>/SKILL.md` | The current repository |
| `~/.copilot/skills/<name>/SKILL.md` | Every project, personal |

Project skills win over personal ones with the same name. In this repo, personal
skills are the `skills/` directory, symlinked into `~/.copilot/skills`.

Directory names are lowercase with hyphens, and should match the `name` field.

## Anatomy

```markdown
---
name: release-checklist
description: Walks through the pre-release checklist for this service. Use when the user is cutting a release, tagging a version, or asks what needs to happen before shipping.
---

# Release Checklist

1. Confirm the changelog covers every merged PR since the last tag.
2. ...
```

Frontmatter fields:

- `name` (required) — lowercase, hyphenated, matches the directory.
- `description` (required) — what it does and when to load it.
- `license` (optional).
- `allowed-tools` (optional) — comma-separated tools that skip the permission
  prompt. Listing `shell` or `bash` here means scripts in this skill run without
  asking. Only add them for skills the user has read and trusts, and say plainly
  that this is what the field does before adding it.

## Writing the description

The description is the whole triggering mechanism. Copilot sees only the name
and description when deciding, so anything about *when to use this* belongs
there and nowhere else. Guidance buried in the body cannot affect loading.

Cover both halves, always:

1. What the skill does.
2. The situations that should load it, in the user's words.

```
description: Converts SVG files to PNG. Use when the user asks to convert,
  rasterize, or export SVG images, or needs a PNG version of a vector asset.
```

Points worth knowing:

- **Mirror real phrasing.** Queries match the description on wording. If users
  say "rasterize", the word "rasterize" needs to appear.
- **Under-triggering is the common failure.** Skills tend not to load when they
  would have helped. If a skill is being missed, name more situations explicitly
  rather than making the summary grander.
- **Simple queries will not trigger anything.** Copilot handles one-step
  requests directly. A skill loads for work that is multi-step or specialized,
  so "read this file" is a poor test case no matter how good the description is.
- **Over-broad descriptions cost more than they look.** A skill that loads
  constantly is back to being an instruction file, and a worse one.

## Writing the body

The body is read only after the skill loads, so it can assume it is relevant.
Write it as instructions to an agent that has already committed to the task.

- Lead with the procedure. Steps, in order, concrete.
- Say what to do on the common failures.
- Keep it lean. Move long references into sibling files and link them, so they
  are read only when needed — `See references/schemas.md for the full schema.`
- Bundle scripts next to `SKILL.md` and describe when to run them. Every file in
  the skill directory is available once the skill loads.

## Building an eval set

An eval set is a JSON list of queries with the triggering you expect:

```json
[
  {"query": "convert logo.svg to a png at 2x", "should_trigger": true},
  {"query": "why is this svg blurry in safari?", "should_trigger": false}
]
```

Rules that make an eval set worth running:

- **Include negatives.** Without `should_trigger: false` cases you cannot detect
  a description that fires on everything, which is the easier failure to cause.
- **Write queries, not summaries.** Real ones: lowercase, typos, file names,
  half a sentence of backstory.
- **Aim at the boundary.** Obvious cases pass regardless. The useful cases are
  the ambiguous ones, and the user should confirm the intended answer on each.
- **Twelve or more, with a real negative share.** Below that the scores move
  around too much to act on.

## Running the scripts

Run them from the `scripts/` directory. They need Python 3.10+ and nothing else
— no third-party packages.

```bash
cd scripts

python3 validate_skill.py ../../my-skill

python3 run_eval.py --skill-path ../../my-skill --eval-set evals.json

python3 optimize_description.py --skill-path ../../my-skill \
    --eval-set evals.json --iterations 3 --apply
```

- `validate_skill.py` — structure, naming, and frontmatter. No quota.
- `run_eval.py` — installs the description as a throwaway project skill in a temp
  directory, sends each query through `copilot -p`, and watches the JSON event
  stream for the `skill` tool loading it. Prints a summary and emits JSON.
- `optimize_description.py` — splits the eval set into train and held-out test,
  proposes new descriptions from the failures, and keeps the one with the best
  test score. Selecting on held-out data is what stops it from overfitting to the
  queries it was shown. `--apply` writes the winner back.

Cost scales as queries × `--runs-per-query` (default 3) per evaluation, and the
optimizer evaluates once per iteration. Start with `--runs-per-query 1` while
checking the setup works, then raise it once you trust the numbers.

Note that the user's own installed skills are loaded during evals alongside the
one under test, which is realistic but means a similar existing skill can absorb
queries. If results look strange, check for an overlapping skill first.

## After it works

Reload with `/skills reload`, or start a new session. Confirm with
`copilot skill list`. Then have the user drive it once on a real task — a skill
that passes evals can still give bad instructions once loaded, and that only
shows up in use.
