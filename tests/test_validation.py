"""Structural validation tests."""

from __future__ import annotations

from pathlib import Path

from product_builders.validation import validate_product_profile_dir


def test_validate_empty_profile_dir_warns(tmp_path: Path) -> None:
    r = validate_product_profile_dir(tmp_path)
    assert r.ok  # warnings only
    assert any("analysis" in w.lower() or "rules" in w.lower() for w in r.warnings)


def test_validate_bad_mdc_frontmatter(tmp_path: Path) -> None:
    (tmp_path / "analysis.json").write_text("{}", encoding="utf-8")
    rules = tmp_path / ".cursor" / "rules"
    rules.mkdir(parents=True)
    (rules / "bad.mdc").write_text("Hello without yaml\n", encoding="utf-8")
    (tmp_path / ".cursor" / "hooks.json").write_text('{"hooks":[]}', encoding="utf-8")
    (tmp_path / ".cursor" / "cli.json").write_text('{"permissions":{}}', encoding="utf-8")
    r = validate_product_profile_dir(tmp_path)
    assert not r.ok
    assert any("bad.mdc" in e for e in r.errors)


def test_validate_good_mdc_and_json(tmp_path: Path) -> None:
    (tmp_path / "analysis.json").write_text('{"metadata":{"name":"x"}}', encoding="utf-8")
    rules = tmp_path / ".cursor" / "rules"
    rules.mkdir(parents=True)
    (rules / "test.mdc").write_text(
        '---\ndescription: "Test"\nalwaysApply: true\n---\n\n# Hi\n',
        encoding="utf-8",
    )
    (tmp_path / ".cursor" / "hooks.json").write_text(
        '{"hooks":[{"event":"preToolUse","action":"block","tools":["x"]}]}',
        encoding="utf-8",
    )
    (tmp_path / ".cursor" / "cli.json").write_text(
        '{"permissions":{"deny":{"write":["*.secret"]}}}',
        encoding="utf-8",
    )
    r = validate_product_profile_dir(tmp_path)
    assert r.ok
    assert not r.errors
