from __future__ import annotations

import argparse
import json
import sys
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import asdict, dataclass
from pathlib import Path

from copilot_cli import stream_events
from skill_io import load_skill, render_skill

# Reading the skill file directly counts as triggering; anything else means the
# agent decided to handle the query itself, so the run can be abandoned early.
NEUTRAL_TOOLS = frozenset({"view", "glob", "grep"})


@dataclass(slots=True, frozen=True)
class EvalCase:
    query: str
    should_trigger: bool


@dataclass(slots=True, frozen=True)
class QueryResult:
    query: str
    should_trigger: bool
    triggers: int
    runs: int
    trigger_rate: float
    passed: bool


def load_eval_set(path: Path) -> list[EvalCase]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    cases = raw["cases"] if isinstance(raw, dict) else raw
    return [EvalCase(query=c["query"], should_trigger=bool(c["should_trigger"])) for c in cases]


def build_probe(root: Path, probe_name: str, description: str, body: str) -> None:
    skill_dir = root / ".github" / "skills" / probe_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        render_skill(probe_name, description, body), encoding="utf-8"
    )


def mentions_probe(event: dict, probe_name: str) -> bool:
    if event.get("type") != "tool.execution_start":
        return False
    data = event.get("data", {})
    if data.get("toolName") != "skill":
        return False
    return probe_name in str(data.get("arguments", {}).get("skill", ""))


def is_decisive_miss(event: dict) -> bool:
    if event.get("type") != "tool.execution_start":
        return False
    tool = event.get("data", {}).get("toolName", "")
    return tool != "skill" and tool not in NEUTRAL_TOOLS


def detect_trigger(events, probe_name: str) -> bool:
    for event in events:
        if mentions_probe(event, probe_name):
            return True
        if is_decisive_miss(event):
            return False
        if event.get("type") == "result":
            return False
    return False


def run_query(case: EvalCase, skill_name: str, description: str, body: str, opts) -> bool:
    probe_name = f"{skill_name}-{uuid.uuid4().hex[:8]}"
    with tempfile.TemporaryDirectory(prefix="skill-eval-") as tmp:
        root = Path(tmp)
        build_probe(root, probe_name, description, body)
        try:
            with closing(stream_events(case.query, root, opts.model, opts.timeout)) as events:
                return detect_trigger(events, probe_name)
        except Exception as error:
            print(f"warning: query failed ({error})", file=sys.stderr)
            return False


def score(case: EvalCase, outcomes: list[bool], threshold: float) -> QueryResult:
    rate = sum(outcomes) / len(outcomes)
    passed = rate >= threshold if case.should_trigger else rate < threshold
    return QueryResult(
        query=case.query,
        should_trigger=case.should_trigger,
        triggers=sum(outcomes),
        runs=len(outcomes),
        trigger_rate=rate,
        passed=passed,
    )


def run_eval(cases: list[EvalCase], skill_name: str, description: str, body: str, opts) -> dict:
    jobs = [(case, run_index) for case in cases for run_index in range(opts.runs_per_query)]
    with ThreadPoolExecutor(max_workers=opts.workers) as pool:
        outcomes = list(
            pool.map(lambda job: run_query(job[0], skill_name, description, body, opts), jobs)
        )

    by_query: dict[str, list[bool]] = {case.query: [] for case in cases}
    for (case, _), triggered in zip(jobs, outcomes):
        by_query[case.query].append(triggered)

    results = [score(case, by_query[case.query], opts.trigger_threshold) for case in cases]
    passed = sum(1 for r in results if r.passed)
    return {
        "skill_name": skill_name,
        "description": description,
        "results": [asdict(r) for r in results],
        "summary": {"total": len(results), "passed": passed, "failed": len(results) - passed},
    }


def report(output: dict) -> None:
    summary = output["summary"]
    print(f"{summary['passed']}/{summary['total']} passed", file=sys.stderr)
    for item in output["results"]:
        status = "PASS" if item["passed"] else "FAIL"
        rate = f"{item['triggers']}/{item['runs']}"
        expected = "trigger" if item["should_trigger"] else "no-trigger"
        print(f"  [{status}] {rate} expected={expected}: {item['query'][:70]}", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure how reliably a skill triggers")
    parser.add_argument("--skill-path", required=True, type=Path)
    parser.add_argument("--eval-set", required=True, type=Path)
    parser.add_argument("--description", default=None, help="Test this description instead")
    parser.add_argument("--runs-per-query", type=int, default=3)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--model", default=None)
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def main() -> None:
    opts = parse_args()
    skill = load_skill(opts.skill_path)
    cases = load_eval_set(opts.eval_set)
    output = run_eval(cases, skill.name, opts.description or skill.description, skill.body, opts)
    if not opts.quiet:
        report(output)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
