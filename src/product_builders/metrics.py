"""Append-only metrics log (JSON Lines) per product profile."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def record_event(product_dir: Path, event: str, **payload: Any) -> None:
    """Append one JSON line to ``metrics.jsonl`` under the product directory."""
    line = {
        "ts": datetime.now(tz=timezone.utc).isoformat(),
        "event": event,
        **payload,
    }
    path = product_dir / "metrics.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line, default=str) + "\n")


def read_recent_events(product_dir: Path, limit: int = 100) -> list[dict[str, Any]]:
    """Parse up to ``limit`` trailing lines from ``metrics.jsonl``."""
    path = product_dir / "metrics.jsonl"
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[dict[str, Any]] = []
    for raw in lines[-limit:]:
        try:
            out.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return out
