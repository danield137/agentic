from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from skill_io import load_skill

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KNOWN_FIELDS = frozenset({"name", "description", "license", "allowed-tools", "version"})
RISKY_TOOLS = frozenset({"shell", "bash"})
MAX_BODY_BYTES = 20_000
MIN_DESCRIPTION_CHARS = 40


def check_name(skill, errors: list[str], warnings: list[str]) -> None:
    if not NAME_PATTERN.match(skill.name):
        errors.append(f"name '{skill.name}' must be lowercase words separated by hyphens")
    if skill.name != skill.path.name:
        warnings.append(f"name '{skill.name}' does not match directory '{skill.path.name}'")


def check_description(skill, errors: list[str], warnings: list[str]) -> None:
    description = skill.description
    if len(description) < MIN_DESCRIPTION_CHARS:
        errors.append("description is too short to trigger reliably")
        return
    lowered = description.lower()
    if "use " not in lowered and "when " not in lowered:
        warnings.append("description does not say when to use the skill, which weakens triggering")


def check_frontmatter(skill, warnings: list[str]) -> None:
    for field in sorted(set(skill.frontmatter) - KNOWN_FIELDS):
        warnings.append(f"unrecognized frontmatter field '{field}'")
    allowed = skill.frontmatter.get("allowed-tools", "")
    granted = {tool.strip() for tool in allowed.split(",")} & RISKY_TOOLS
    if granted:
        warnings.append(f"allowed-tools pre-approves {', '.join(sorted(granted))} without prompting")


def check_body(skill, warnings: list[str]) -> None:
    if not skill.body.strip():
        warnings.append("body is empty, so the skill adds no instructions once loaded")
    size = len(skill.body.encode("utf-8"))
    if size > MAX_BODY_BYTES:
        warnings.append(f"body is {size} bytes; move detail into reference files it can link to")


def check_references(skill, warnings: list[str]) -> None:
    present = {path.name for path in skill.path.rglob("*") if path.is_file()}
    for target in re.findall(r"`([\w./-]+\.(?:md|py|sh|json|html))`", skill.body):
        if (skill.path / target).exists() or Path(target).name in present:
            continue
        warnings.append(f"body references '{target}', which is not in the skill directory")


def validate(skill_dir: Path) -> tuple[list[str], list[str]]:
    skill_dir = skill_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    try:
        skill = load_skill(skill_dir)
    except (OSError, ValueError) as error:
        return [str(error)], []

    check_name(skill, errors, warnings)
    check_description(skill, errors, warnings)
    check_frontmatter(skill, warnings)
    check_body(skill, warnings)
    check_references(skill, warnings)
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a skill directory for structural problems")
    parser.add_argument("skill_path", type=Path)
    opts = parser.parse_args()

    errors, warnings = validate(opts.skill_path)
    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")

    if errors:
        sys.exit(1)
    print(f"{opts.skill_path} looks valid")


if __name__ == "__main__":
    main()
