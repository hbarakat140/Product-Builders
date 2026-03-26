"""Ingest Cursor-produced deep-analysis.yaml into a ProductProfile.

Loads the YAML, strips evidence fields (used only for validation), and
shallow-merges the deep sections into the existing profile — following the
same pattern as ``profiles.overrides.merge_overrides``.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

from product_builders.deep_analysis.schema import DeepAnalysisYAML, is_evidence_key
from product_builders.models.profile import ProductProfile

logger = logging.getLogger(__name__)

DEEP_SECTIONS = ("architecture_deep", "domain_model_deep", "implicit_conventions_deep")


def load_deep_yaml(path: Path) -> dict:
    """Load deep-analysis.yaml, returning an empty dict on failure."""
    if not path.exists():
        raise FileNotFoundError(f"Deep analysis file not found: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception as exc:
        logger.error("Failed to load deep analysis YAML %s: %s", path, exc)
        raise


def strip_evidence(data: Any) -> Any:
    """Recursively remove evidence keys from nested data.

    Evidence fields are used only for validation; they are stripped before
    merging into the profile to keep it focused on derived insights.
    """
    if isinstance(data, dict):
        return {
            k: strip_evidence(v)
            for k, v in data.items()
            if not is_evidence_key(k)
        }
    elif isinstance(data, list):
        return [strip_evidence(item) for item in data]
    return data


def ingest_deep_analysis(
    profile: ProductProfile,
    deep: DeepAnalysisYAML,
) -> ProductProfile:
    """Return a new profile with deep analysis sections merged in.

    Evidence fields are stripped before merging — they are used only during
    validation and are not stored in the profile.
    """
    profile_data = profile.model_dump()

    deep_data = deep.model_dump(by_alias=True)
    for section in DEEP_SECTIONS:
        section_data = deep_data.get(section)
        if section_data is None:
            continue
        cleaned = strip_evidence(section_data)
        if isinstance(cleaned, dict) and isinstance(profile_data.get(section), dict):
            profile_data[section].update(cleaned)
        else:
            profile_data[section] = cleaned

    return ProductProfile.model_validate(profile_data)
