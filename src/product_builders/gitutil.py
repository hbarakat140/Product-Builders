"""Git helpers for drift detection (optional — repo may not be a git worktree)."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def get_git_head_sha(repo_path: Path) -> str | None:
    """Return 40-char hex SHA of ``HEAD``, or ``None`` if not a git repo / git missing."""
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        logger.debug("git rev-parse failed: %s", e)
        return None
    if proc.returncode != 0:
        return None
    sha = proc.stdout.strip()
    if len(sha) >= 7 and all(c in "0123456789abcdef" for c in sha.lower()):
        return sha
    return None
