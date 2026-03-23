"""Drift detection — profile vs current repo state."""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path

import pydantic

from product_builders.analyzers import registry as analyzer_registry
from product_builders.gitutil import get_git_head_sha
from product_builders.models.heuristic_dimensions import HEURISTIC_PROFILE_FIELDS
from product_builders.models.profile import ProductMetadata, ProductProfile

logger = logging.getLogger(__name__)


@dataclass
class DriftReport:
    git_drift: bool
    git_message: str
    profile_sha: str | None
    current_sha: str | None
    full_drift: bool | None
    full_message: str | None
    heuristic_fingerprint: str | None
    #: True if ``--full`` was requested but analyzers / hashing failed (not the same as fingerprint mismatch).
    full_check_failed: bool = False
    #: Profile has no ``last_commit_sha`` (informational until next ``analyze``).
    no_git_sha_in_profile: bool = False
    #: Could not run ``git rev-parse HEAD`` on the repo path.
    git_head_unreadable: bool = False


def run_drift_check(
    profile: ProductProfile,
    repo_path: Path,
    *,
    full: bool = False,
) -> DriftReport:
    """Compare stored profile to repo (git HEAD, optionally full heuristic re-run)."""
    current_sha = get_git_head_sha(repo_path)
    profile_sha = profile.metadata.last_commit_sha
    no_git_sha_in_profile = profile_sha is None
    git_head_unreadable = current_sha is None

    if current_sha is None:
        if profile_sha is None:
            git_msg = (
                "Could not read git HEAD — not a git repo or git unavailable. "
                "Run `analyze` inside a git checkout to record HEAD."
            )
            git_drift = False
        else:
            git_msg = "Cannot read current git HEAD but profile has a stored SHA (unusual)."
            git_drift = True
    elif profile_sha is None:
        git_msg = (
            "No commit SHA in profile yet — run `analyze` to record HEAD for git drift checks, "
            "or use `--full` to compare heuristic fingerprints."
        )
        git_drift = False
    elif current_sha != profile_sha:
        git_msg = f"Git drift: profile recorded {profile_sha[:12]}… but repo HEAD is {current_sha[:12]}…"
        git_drift = True
    else:
        git_msg = f"Git HEAD matches profile ({current_sha[:12]}…)."
        git_drift = False

    full_drift: bool | None = None
    full_msg: str | None = None
    fp: str | None = None
    full_check_failed = False

    if full:
        try:
            fresh_digest, detail = _fresh_heuristic_digest(repo_path, profile)
            fp = fresh_digest
            stored_digest, _ = _heuristic_payload_digest(profile)
            if fresh_digest != stored_digest:
                full_drift = True
                full_msg = (
                    f"Heuristic fingerprint differs (stored {stored_digest[:12]}… vs "
                    f"current {fresh_digest[:12]}…). {detail}"
                )
            else:
                full_drift = False
                full_msg = "Heuristic dimensions match cached profile fingerprint."
        except Exception as e:
            logger.exception("Full drift check failed")
            full_drift = None
            full_msg = f"Full heuristic check failed: {e}"
            full_check_failed = True

    return DriftReport(
        git_drift=git_drift,
        git_message=git_msg,
        profile_sha=profile_sha,
        current_sha=current_sha,
        full_drift=full_drift,
        full_message=full_msg,
        heuristic_fingerprint=fp,
        full_check_failed=full_check_failed,
        no_git_sha_in_profile=no_git_sha_in_profile,
        git_head_unreadable=git_head_unreadable,
    )


def _stable_json(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, default=_json_default)


def _json_default(o: object) -> object:
    if isinstance(o, pydantic.BaseModel):
        return o.model_dump(mode="json")
    raise TypeError


def _heuristic_payload_digest(profile: ProductProfile) -> tuple[str, int]:
    """SHA-256 hex digest and serialized payload size for heuristic dimensions only."""
    payload = {k: getattr(profile, k).model_dump(mode="json") for k in sorted(HEURISTIC_PROFILE_FIELDS)}
    raw = _stable_json(payload)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return digest, len(raw)


def _fresh_heuristic_digest(repo_path: Path, existing: ProductProfile) -> tuple[str, str]:
    """Re-run analyzers, return digest and a short detail string."""
    meta = ProductMetadata(
        name=existing.metadata.name,
        repo_path=str(repo_path),
        description=existing.metadata.description,
    )
    fresh = ProductProfile(metadata=meta)

    analyzers = analyzer_registry.get_all_analyzers()
    for analyzer in analyzers:
        if analyzer.dimension not in HEURISTIC_PROFILE_FIELDS:
            continue
        result = analyzer.safe_analyze(repo_path)
        setattr(fresh, analyzer.dimension, result)

    digest, raw_len = _heuristic_payload_digest(fresh)
    detail = f"({len(analyzers)} analyzers, {raw_len} bytes compared)"
    return digest, detail
