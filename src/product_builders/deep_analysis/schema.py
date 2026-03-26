"""Schema validation for deep-analysis.yaml produced by Cursor.

Validates structure against expected models and checks that evidence
file citations actually exist in the target repository.
"""

from __future__ import annotations

import logging
from pathlib import Path

from pydantic import BaseModel, ValidationError

from product_builders.models.analysis import (
    ArchitectureDeepResult,
    DomainModelDeepResult,
    ImplicitConventionsDeepResult,
)

logger = logging.getLogger(__name__)


class DeepAnalysisYAML(BaseModel):
    """Expected top-level structure of deep-analysis.yaml."""

    architecture_deep: ArchitectureDeepResult | None = None
    domain_model_deep: DomainModelDeepResult | None = None
    implicit_conventions_deep: ImplicitConventionsDeepResult | None = None

    @property
    def section_count(self) -> int:
        """Number of non-None deep analysis sections (out of 3)."""
        return sum(
            1
            for s in ("architecture_deep", "domain_model_deep", "implicit_conventions_deep")
            if getattr(self, s) is not None
        )


def is_evidence_key(key: str) -> bool:
    """Return True if *key* is an evidence field name."""
    return key == "evidence" or key.endswith("_evidence")


def _collect_evidence_fields(data: object, path: str = "") -> list[tuple[str, str]]:
    """Walk a nested structure and collect all (dotted_path, value) pairs for evidence fields."""
    results: list[tuple[str, str]] = []
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{path}.{key}" if path else key
            if is_evidence_key(key):
                if isinstance(value, str) and value:
                    results.append((full_key, value))
            else:
                results.extend(_collect_evidence_fields(value, full_key))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            results.extend(_collect_evidence_fields(item, f"{path}[{i}]"))
    return results


def validate_deep_yaml(
    data: dict,
    repo_path: Path,
) -> tuple[DeepAnalysisYAML, list[str]]:
    """Parse and validate deep analysis YAML data.

    Returns the validated model and a list of warning strings.
    Raises ``ValueError`` if the YAML structure is fundamentally invalid.
    """
    warnings: list[str] = []

    try:
        parsed = DeepAnalysisYAML.model_validate(data)
    except ValidationError as exc:
        messages = []
        for err in exc.errors():
            loc = " → ".join(str(p) for p in err["loc"])
            messages.append(f"  {loc}: {err['msg']}")
        raise ValueError(
            "Invalid deep-analysis.yaml structure:\n" + "\n".join(messages)
        ) from exc

    # Validate evidence file paths exist in the repo
    dumped = parsed.model_dump(by_alias=True)
    evidence_pairs = _collect_evidence_fields(dumped)
    for field_path, cited_path in evidence_pairs:
        # Evidence may be a description rather than a strict file path —
        # only warn when it looks like a path (contains / or \).
        if "/" in cited_path or "\\" in cited_path:
            candidate = repo_path / cited_path
            if not candidate.exists():
                warnings.append(f"{field_path}: file not found: {cited_path}")

    return parsed, warnings
