from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

FRONTMATTER_FENCE = "---"


@dataclass(slots=True, frozen=True)
class Skill:
    path: Path
    name: str
    description: str
    body: str
    frontmatter: dict[str, str]


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return the raw frontmatter block and the body that follows it."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_FENCE:
        raise ValueError("SKILL.md must start with a '---' frontmatter fence")

    for index in range(1, len(lines)):
        if lines[index].strip() == FRONTMATTER_FENCE:
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])

    raise ValueError("SKILL.md frontmatter is missing its closing '---' fence")


def parse_frontmatter(block: str) -> dict[str, str]:
    """Parse the small YAML subset skill frontmatter is allowed to use.

    Supports `key: value` and `key: |` block scalars. Anything richer is
    rejected rather than silently misread.
    """
    fields: dict[str, str] = {}
    lines = block.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"cannot parse frontmatter line: {line!r}")

        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value in ("|", ">", "|-", ">-"):
            block_lines, index = read_block_scalar(lines, index)
            fields[key] = "\n".join(block_lines).strip()
            continue
        fields[key] = unquote(value)

    return fields


def read_block_scalar(lines: list[str], start: int) -> tuple[list[str], int]:
    collected: list[str] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if line.strip() and not line.startswith((" ", "\t")):
            break
        collected.append(line.strip())
        index += 1
    return collected, index


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        if value[0] == '"':
            return json.loads(value)
        return value[1:-1]
    return value


def load_skill(skill_dir: Path) -> Skill:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise FileNotFoundError(f"no SKILL.md in {skill_dir}")

    block, body = split_frontmatter(skill_file.read_text(encoding="utf-8"))
    fields = parse_frontmatter(block)
    missing = [key for key in ("name", "description") if not fields.get(key)]
    if missing:
        raise ValueError(f"SKILL.md frontmatter is missing: {', '.join(missing)}")

    return Skill(
        path=skill_dir,
        name=fields["name"],
        description=fields["description"],
        body=body,
        frontmatter=fields,
    )


def render_skill(name: str, description: str, body: str) -> str:
    """Render a SKILL.md. Values are JSON-encoded, which is valid YAML."""
    return (
        f"{FRONTMATTER_FENCE}\n"
        f"name: {json.dumps(name)}\n"
        f"description: {json.dumps(description)}\n"
        f"{FRONTMATTER_FENCE}\n\n"
        f"{body.strip()}\n"
    )


def replace_description(skill_file: Path, description: str) -> None:
    block, body = split_frontmatter(skill_file.read_text(encoding="utf-8"))
    updated: list[str] = []
    skipping = False

    for line in block.splitlines():
        if line.startswith("description:"):
            updated.append(f"description: {json.dumps(description)}")
            skipping = line.split(":", 1)[1].strip() in ("|", ">", "|-", ">-")
            continue
        if skipping:
            if line.strip() and not line.startswith((" ", "\t")):
                skipping = False
            else:
                continue
        updated.append(line)

    fence = FRONTMATTER_FENCE
    skill_file.write_text(
        f"{fence}\n" + "\n".join(updated) + f"\n{fence}\n{body}", encoding="utf-8"
    )
