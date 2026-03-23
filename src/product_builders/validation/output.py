"""Validate generated artifacts under ``profiles/<name>/``."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL | re.MULTILINE)


@dataclass
class ValidationReport:
    """Result of validating a product profile output directory."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def validate_product_profile_dir(product_dir: Path) -> ValidationReport:
    """Check ``analysis.json``, ``.cursor/rules/*.mdc``, ``hooks.json``, ``cli.json``."""
    report = ValidationReport()
    if not product_dir.is_dir():
        report.errors.append(f"Not a directory: {product_dir}")
        return report

    analysis = product_dir / "analysis.json"
    if analysis.exists():
        try:
            json.loads(analysis.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            report.errors.append(f"analysis.json: invalid JSON ({e})")
    else:
        report.warnings.append("analysis.json: missing")

    cursor = product_dir / ".cursor"
    rules_dir = cursor / "rules"
    if rules_dir.is_dir():
        for mdc in sorted(rules_dir.glob("*.mdc")):
            _validate_mdc(mdc, report)
    elif cursor.is_dir():
        report.warnings.append(".cursor/rules/: missing or not a directory (no *.mdc to validate)")
    else:
        report.warnings.append(".cursor/: missing — no generated rules directory")

    hooks = cursor / "hooks.json"
    if hooks.exists():
        _validate_hooks_json(hooks, report)
    else:
        report.warnings.append(".cursor/hooks.json: missing")

    cli = cursor / "cli.json"
    if cli.exists():
        _validate_cli_json(cli, report)
    else:
        report.warnings.append(".cursor/cli.json: missing")

    return report


def _validate_mdc(path: Path, report: ValidationReport) -> None:
    rel = path.name
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        report.errors.append(f"{rel}: cannot read ({e})")
        return
    if not text.startswith("---"):
        report.errors.append(f"{rel}: expected YAML frontmatter starting with ---")
        return
    m = _FRONTMATTER_RE.match(text)
    if not m:
        report.errors.append(f"{rel}: missing closing --- after frontmatter")
        return
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        report.errors.append(f"{rel}: invalid YAML frontmatter ({e})")
        return
    if not isinstance(fm, dict):
        report.errors.append(f"{rel}: frontmatter must be a mapping")
        return
    if "description" not in fm:
        report.warnings.append(f"{rel}: frontmatter has no 'description'")
    if "alwaysApply" not in fm and "globs" not in fm:
        report.warnings.append(f"{rel}: neither alwaysApply nor globs set (may be intentional)")


def _validate_hooks_json(path: Path, report: ValidationReport) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        report.errors.append(f"hooks.json: invalid JSON ({e})")
        return
    hooks = data.get("hooks")
    if not isinstance(hooks, list):
        report.errors.append("hooks.json: 'hooks' must be a list")
        return
    known_events = frozenset({"preToolUse", "beforeShellExecution", "afterFileEdit"})
    known_actions = frozenset({"block", "warn", "allow", "deny"})
    for i, hook in enumerate(hooks):
        if not isinstance(hook, dict):
            report.errors.append(f"hooks.json: hooks[{i}] must be an object")
            continue
        ev = hook.get("event")
        if ev not in known_events:
            report.warnings.append(f"hooks.json: hooks[{i}].event={ev!r} (unexpected)")
        act = hook.get("action")
        if act is not None and act not in known_actions:
            report.warnings.append(f"hooks.json: hooks[{i}].action={act!r} (unexpected)")


def _validate_cli_json(path: Path, report: ValidationReport) -> None:
    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        report.errors.append(f"cli.json: invalid JSON ({e})")
        return
    if not isinstance(data, dict):
        report.errors.append("cli.json: root must be an object")
        return
    perms = data.get("permissions")
    if perms is not None and not isinstance(perms, dict):
        report.errors.append("cli.json: 'permissions' must be an object")
