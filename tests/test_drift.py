"""Drift detection unit tests."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

from product_builders.lifecycle.drift import run_drift_check
from product_builders.models.profile import ProductMetadata, ProductProfile


def _init_git_repo_with_commit(path: Path) -> str:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "test"],
        cwd=path,
        check=True,
        capture_output=True,
    )
    (path / "tracked.txt").write_text("hello", encoding="utf-8")
    subprocess.run(["git", "add", "tracked.txt"], cwd=path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=path,
        check=True,
        capture_output=True,
    )
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


def test_drift_no_git_repo_profile_without_sha(tmp_path: Path) -> None:
    """Non-git path + profile without SHA: no git drift; flags for CLI coloring."""
    meta = ProductMetadata(name="t", last_commit_sha=None)
    profile = ProductProfile(metadata=meta)
    r = run_drift_check(profile, tmp_path, full=False)
    assert r.full_drift is None
    assert not r.git_drift
    assert r.no_git_sha_in_profile is True
    assert r.git_head_unreadable is True
    assert r.profile_sha is None
    assert r.current_sha is None


def test_drift_git_head_matches_profile_sha(tmp_path: Path) -> None:
    """When HEAD equals stored profile SHA, no git drift."""
    head = _init_git_repo_with_commit(tmp_path)
    meta = ProductMetadata(name="t", last_commit_sha=head)
    profile = ProductProfile(metadata=meta)
    r = run_drift_check(profile, tmp_path, full=False)
    assert not r.git_drift
    assert r.current_sha == head
    assert r.profile_sha == head
    assert not r.no_git_sha_in_profile
    assert not r.git_head_unreadable
    assert "matches" in r.git_message.lower()


def test_drift_git_head_differs_from_profile_sha(tmp_path: Path) -> None:
    """When HEAD differs from profile, report git drift."""
    _init_git_repo_with_commit(tmp_path)
    wrong_sha = "b" * 40
    meta = ProductMetadata(name="t", last_commit_sha=wrong_sha)
    profile = ProductProfile(metadata=meta)
    r = run_drift_check(profile, tmp_path, full=False)
    assert r.git_drift
    assert "drift" in r.git_message.lower()


def test_drift_readable_git_no_sha_in_profile_yet(tmp_path: Path) -> None:
    """Git works but profile never recorded SHA — not drift, prompt to analyze."""
    _init_git_repo_with_commit(tmp_path)
    meta = ProductMetadata(name="t", last_commit_sha=None)
    profile = ProductProfile(metadata=meta)
    r = run_drift_check(profile, tmp_path, full=False)
    assert not r.git_drift
    assert r.no_git_sha_in_profile
    assert not r.git_head_unreadable
    assert r.current_sha is not None


@patch("product_builders.lifecycle.drift._fresh_heuristic_digest")
def test_full_check_analyzer_failure_is_not_fingerprint_drift(
    mock_fresh: object,
    tmp_path: Path,
) -> None:
    """When ``--full`` path raises, report failure — do not treat as heuristic drift."""
    head = _init_git_repo_with_commit(tmp_path)
    meta = ProductMetadata(name="t", last_commit_sha=head)
    profile = ProductProfile(metadata=meta)
    mock_fresh.side_effect = RuntimeError("simulated analyzer failure")

    r = run_drift_check(profile, tmp_path, full=True)

    assert r.full_check_failed is True
    assert r.full_drift is None
    assert r.heuristic_fingerprint is None
    assert r.full_message is not None
    assert "Full heuristic check failed" in r.full_message
    assert "simulated analyzer failure" in r.full_message
