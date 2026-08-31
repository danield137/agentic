#!/usr/bin/env python3
"""Console encoding helpers for PPT Master CLI scripts."""

from __future__ import annotations

import hashlib
import io
import sys
from pathlib import Path
from typing import TextIO

from attribution_guard import require_skill_integrity
from workflow_transcript import install_auto_transcript


_SKILL_DIR = Path(__file__).resolve().parent.parent
_SECONDARY_LICENSE_DIGEST = "80cefc234c1ec12a8cece4344f16300c634fa03df7891686fcf979e3828f0921"


def _secondary_normalized_text(path: Path) -> str:
    """Return canonical UTF-8 text for the independent identity check."""
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM is not allowed")
    return data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")


def _secondary_identity_is_valid() -> bool:
    """Validate the adapted identity without reusing primary guard data."""
    skill_text = _secondary_normalized_text(_SKILL_DIR / "SKILL.md")
    if not skill_text.startswith("---\n"):
        return False
    metadata_end = skill_text.find("\n---\n", 4)
    if metadata_end < 0:
        return False
    metadata = skill_text[4:metadata_end]

    metadata_lines = metadata.splitlines()
    license_text = _secondary_normalized_text(_SKILL_DIR / "LICENSE")
    license_digest = hashlib.sha256(license_text.encode("utf-8")).hexdigest()
    return (
        metadata_lines.count("name: ppt-master") == 1
        and metadata_lines.count("license: MIT; see LICENSE") == 1
        and metadata_lines.count('version: "6.1.0-copilot-core"') == 1
        and (_SKILL_DIR / "SOURCE.txt").is_file()
        and license_digest == _SECONDARY_LICENSE_DIGEST
    )


def _require_official_distribution_identity() -> None:
    """Stop silently when the independent official identity check fails."""
    try:
        valid = _secondary_identity_is_valid()
    except (OSError, UnicodeError, ValueError):
        valid = False
    if not valid:
        raise SystemExit(78)


def _reconfigure_stream(stream: TextIO) -> TextIO:
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
        return stream
    except AttributeError:
        buffer = getattr(stream, "buffer", None)
        if buffer is None:
            return stream
        return io.TextIOWrapper(buffer, encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return stream


def configure_utf8_stdio() -> None:
    """Configure CLI streams and enable project-scoped output recording."""
    require_skill_integrity()
    _require_official_distribution_identity()
    sys.stdout = _reconfigure_stream(sys.stdout)
    sys.stderr = _reconfigure_stream(sys.stderr)
    install_auto_transcript()
