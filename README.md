# agentic

Personal GitHub Copilot CLI customizations — instructions and skills — shared across every machine.

## Layout

Each top-level directory mirrors a directory of the same name inside the Copilot
CLI home directory (`~/.copilot`, or `$COPILOT_HOME` if set).

```
instructions/              *.instructions.md   always-on personal guidance
skills/                    <name>/SKILL.md     on-demand specialized capabilities
install.sh                                     symlinks everything into ~/.copilot
install_instructions.sh                        symlinks only instructions/
```

`agents/`, `hooks/`, and `mcp-config.json` are also recognized by `install.sh`;
create them here when needed and re-run the script.

## Install on a new machine

```bash
git clone https://github.com/<owner>/agentic.git ~/Source/repos/agentic
cd ~/Source/repos/agentic
./install.sh
```

For instructions only, without the skills:

```bash
./install_instructions.sh
```

Both scripts symlink into `~/.copilot`. Anything already at a target path is
moved to `~/.copilot/.agentic-backup/<timestamp>/` first. Use `--dry-run` to
preview and `--force` to skip the confirmation prompt. `install.sh` also accepts
an explicit component list, for example `./install.sh instructions skills`.

Because the entries are symlinks, editing a file here takes effect immediately —
no re-install after a `git pull`.

> The repo is deliberately cloned **outside** `~/.copilot`. That directory also
> holds credentials (`config.json`), logs, and session databases, which must
> never be committed.

## Skills

| Skill | Description |
| --- | --- |
| `adr-skill` | Create and maintain Architecture Decision Records using the MADR bare template. |
| `backlog` | Create and maintain lean, milestone-based planning backlogs. |
| `code-polish` | Review code for smells, dead code, duplication, SRP violations, extensibility problems, and bugs, reported as a ranked table. |
| `ppt-master` | Create, edit, redesign, and validate editable PowerPoint decks with a Copilot-adapted core workflow. |
| `skill-creator` | Create, review, and improve Copilot CLI skills, including measuring how reliably a skill triggers. |
| `ui-ux-pro-max` | Search and apply local UI/UX design intelligence across web, mobile, and desktop stacks. |

`skill-creator` ships three stdlib-only Python scripts under
`skills/skill-creator/scripts/`:

- `validate_skill.py` — structure, naming, and frontmatter checks. No quota cost.
- `run_eval.py` — sends eval queries through `copilot -p` and watches the JSON
  event stream to see whether the skill loaded.
- `optimize_description.py` — proposes better descriptions from eval failures and
  keeps the one that scores best on held-out queries.

The eval scripts spawn real `copilot -p` runs, so they consume Copilot quota.
`validate_skill.py` does not.

## Adding an instruction file

Instructions are loaded into every session, so keep them short and broadly
applicable. Create `instructions/<topic>.instructions.md`:

```markdown
---
name: Short Title
description: What this guidance covers.
applyTo: '**'
---

# Short Title

- Guidance goes here.
```

`applyTo` is a glob matched against the files in play — use `'**'` for
always-on guidance, or something like `'**/*.py'` to scope it to a language.

## Adding a skill

Skills are loaded only when Copilot judges them relevant, so they are the right
home for longer, task-specific procedures. The easiest way to write one is to
ask Copilot to use the `skill-creator` skill:

```
Use the /skill-creator skill to create a skill for <task>.
```

Written by hand, a skill is `skills/<skill-name>/SKILL.md` with a lowercase,
hyphenated directory name:

```markdown
---
name: skill-name
description: What the skill does, and when Copilot should use it.
---

Step-by-step instructions for the task.
```

Add any scripts or reference files alongside `SKILL.md`; Copilot discovers every
file in the skill directory and you can reference them from the instructions.

To pre-approve tools the skill needs, add an `allowed-tools` frontmatter field.
Only list `shell` or `bash` for skills whose scripts you have read and trust,
since doing so removes the per-command confirmation prompt.

After adding a skill, run `/skills reload` in an active session, or start a new
one. Verify with `copilot skill list`.

## Instructions vs. skills

Use **instructions** for guidance that applies to nearly every task, and
**skills** for detailed procedures that should only be loaded when relevant.
