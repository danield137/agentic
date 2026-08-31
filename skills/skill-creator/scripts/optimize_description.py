from __future__ import annotations

import argparse
import json
import random
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from copilot_cli import run_text
from run_eval import EvalCase, load_eval_set, run_eval
from skill_io import load_skill, replace_description

PROPOSAL_PATTERN = re.compile(r"<description>(.*?)</description>", re.DOTALL)
TRAIN_FRACTION = 0.6


@dataclass(slots=True, frozen=True)
class Attempt:
    description: str
    train_score: float
    test_score: float


def split_cases(cases: list[EvalCase], seed: int) -> tuple[list[EvalCase], list[EvalCase]]:
    shuffled = list(cases)
    random.Random(seed).shuffle(shuffled)
    cut = max(1, round(len(shuffled) * TRAIN_FRACTION))
    return shuffled[:cut], shuffled[cut:] or shuffled[cut - 1 :]


def score_of(output: dict) -> float:
    summary = output["summary"]
    return summary["passed"] / summary["total"] if summary["total"] else 0.0


def format_failures(output: dict) -> str:
    lines = []
    for item in output["results"]:
        if item["passed"]:
            continue
        expected = "should trigger" if item["should_trigger"] else "should NOT trigger"
        rate = f"{item['triggers']}/{item['runs']}"
        lines.append(f"- ({expected}, triggered {rate}) {item['query']}")
    return "\n".join(lines) or "- none"


def build_prompt(skill_name: str, body: str, description: str, output: dict) -> str:
    return (
        f"You are tuning the `description` field of a GitHub Copilot CLI skill so that the\n"
        f"agent loads it exactly when it should.\n\n"
        f"Skill name: {skill_name}\n\n"
        f"Current description:\n{description}\n\n"
        f"What the skill does once loaded:\n{body[:4000]}\n\n"
        f"These evaluation queries came out wrong:\n{format_failures(output)}\n\n"
        f"Write one improved description. State what the skill does and the situations that\n"
        f"should load it, using wording close to how a user would phrase those requests. Keep\n"
        f"it under 500 characters and do not widen it so far that unrelated queries match.\n"
        f"Reply with the description alone, wrapped in <description></description> tags."
    )


def propose_description(prompt: str, model: str | None, timeout: int) -> str | None:
    reply = run_text(prompt, model=model, timeout=timeout)
    match = PROPOSAL_PATTERN.search(reply)
    if not match:
        return None
    proposal = " ".join(match.group(1).split())
    return proposal or None


def evaluate(cases: list[EvalCase], skill, description: str, opts) -> dict:
    return run_eval(cases, skill.name, description, skill.body, opts)


def measure(train, test, skill, description: str, opts) -> tuple[Attempt, dict]:
    train_output = evaluate(train, skill, description, opts)
    test_output = evaluate(test, skill, description, opts)
    return Attempt(description, score_of(train_output), score_of(test_output)), train_output


def optimize(skill, cases: list[EvalCase], opts) -> list[Attempt]:
    train, test = split_cases(cases, opts.seed)
    attempt, train_output = measure(train, test, skill, skill.description, opts)
    attempts = [attempt]
    print(f"baseline train={attempt.train_score:.2f} test={attempt.test_score:.2f}", file=sys.stderr)

    for iteration in range(1, opts.iterations + 1):
        if attempts[-1].train_score >= 1.0:
            break
        prompt = build_prompt(skill.name, skill.body, attempts[-1].description, train_output)
        proposal = propose_description(prompt, opts.model, opts.propose_timeout)
        if not proposal:
            print("warning: no description proposed, stopping", file=sys.stderr)
            break
        attempt, train_output = measure(train, test, skill, proposal, opts)
        attempts.append(attempt)
        print(
            f"iteration {iteration} train={attempt.train_score:.2f} "
            f"test={attempt.test_score:.2f}",
            file=sys.stderr,
        )

    return attempts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Improve a skill description against an eval set")
    parser.add_argument("--skill-path", required=True, type=Path)
    parser.add_argument("--eval-set", required=True, type=Path)
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--runs-per-query", type=int, default=3)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--propose-timeout", type=int, default=300)
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--model", default=None)
    parser.add_argument("--apply", action="store_true", help="Write the winner back to SKILL.md")
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def main() -> None:
    opts = parse_args()
    skill = load_skill(opts.skill_path)
    cases = load_eval_set(opts.eval_set)
    attempts = optimize(skill, cases, opts)

    best = max(attempts, key=lambda a: (a.test_score, a.train_score))
    if opts.apply and best.description != skill.description:
        replace_description(opts.skill_path / "SKILL.md", best.description)
        print(f"applied best description to {opts.skill_path / 'SKILL.md'}", file=sys.stderr)

    print(
        json.dumps(
            {
                "skill_name": skill.name,
                "original_description": skill.description,
                "best_description": best.description,
                "best_train_score": best.train_score,
                "best_test_score": best.test_score,
                "attempts": [asdict(a) for a in attempts],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
