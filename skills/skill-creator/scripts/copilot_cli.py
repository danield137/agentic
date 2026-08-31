from __future__ import annotations

import json
import queue
import subprocess
import threading
import time
from collections.abc import Iterator
from pathlib import Path

BASE_FLAGS = ("--allow-all-tools", "--allow-all-paths", "--no-color", "--log-level", "none")


class CopilotError(RuntimeError):
    pass


def build_command(prompt: str, model: str | None, output_format: str) -> list[str]:
    command = ["copilot", "-p", prompt, "--output-format", output_format, *BASE_FLAGS]
    if output_format == "text":
        command.append("--silent")
    if model:
        command.extend(["--model", model])
    return command


def run_text(prompt: str, model: str | None = None, timeout: int = 300) -> str:
    """Run a single non-interactive prompt and return the agent's text reply.

    The prompt is passed on argv because `copilot -p` does not read stdin.
    """
    command = build_command(prompt, model, "text")
    result = subprocess.run(
        command, capture_output=True, text=True, timeout=timeout, check=False
    )
    if result.returncode != 0:
        raise CopilotError(f"copilot exited {result.returncode}: {result.stderr.strip()}")
    return result.stdout.strip()


def stream_events(
    prompt: str,
    cwd: Path,
    model: str | None = None,
    timeout: int = 120,
) -> Iterator[dict]:
    """Yield JSONL events from a non-interactive run, killing it if abandoned.

    Breaking out of the loop terminates the underlying process, so callers can
    stop as soon as they have their answer instead of paying for a full run.
    """
    command = build_command(prompt, model, "json")
    process = subprocess.Popen(
        command,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )
    lines: queue.Queue[str | None] = queue.Queue()
    reader = threading.Thread(target=drain, args=(process, lines), daemon=True)
    reader.start()

    try:
        yield from read_events(lines, timeout)
    finally:
        terminate(process)


def drain(process: subprocess.Popen[str], lines: queue.Queue[str | None]) -> None:
    if process.stdout is not None:
        for line in process.stdout:
            lines.put(line)
    lines.put(None)


def read_events(lines: queue.Queue[str | None], timeout: int) -> Iterator[dict]:
    deadline = None if timeout <= 0 else time.monotonic() + timeout
    while True:
        remaining = None if deadline is None else deadline - time.monotonic()
        if remaining is not None and remaining <= 0:
            return
        try:
            line = lines.get(timeout=remaining)
        except queue.Empty:
            return
        if line is None:
            return
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def terminate(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
