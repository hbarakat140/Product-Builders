"""Data loading for catalog and docs (profiles dir + packaged markdown)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from product_builders.config import validate_product_name

_CONTENT_DIR = Path(__file__).resolve().parent / "content" / "docs"

# Matches onboarding-{role}.md role segment (ContributorRole values)
_ONBOARDING_ROLE_RE = re.compile(r"^onboarding-([a-z_]+)\.md$")


@dataclass
class ProductSummary:
    name: str
    description: str
    analysis_timestamp: str | None
    primary_language: str | None
    has_analysis: bool


def profiles_dir_resolved(explicit: Path | None = None) -> Path:
    from product_builders.config import PROFILES_DIR

    base = explicit or PROFILES_DIR
    return Path(base).resolve()


def get_product_summary(profiles_root: Path, product_name: str) -> ProductSummary | None:
    """Return a single product summary or ``None`` if missing / invalid."""
    try:
        product_dir = safe_product_dir(profiles_root, product_name)
    except (ValueError, FileNotFoundError):
        return None
    analysis_path = product_dir / "analysis.json"
    if not analysis_path.is_file():
        return ProductSummary(
            name=product_name,
            description="",
            analysis_timestamp=None,
            primary_language=None,
            has_analysis=False,
        )
    meta = _read_analysis_metadata(analysis_path)
    return ProductSummary(
        name=product_name,
        description=(meta.get("description") or "")[:500],
        analysis_timestamp=meta.get("analysis_timestamp"),
        primary_language=meta.get("primary_language"),
        has_analysis=True,
    )


def list_products(profiles_root: Path) -> list[ProductSummary]:
    """Scan ``profiles_root`` for subdirectories containing ``analysis.json``."""
    if not profiles_root.is_dir():
        return []

    items: list[ProductSummary] = []
    for child in sorted(profiles_root.iterdir()):
        if not child.is_dir():
            continue
        name = child.name
        try:
            validate_product_name(name)
        except ValueError:
            continue
        analysis_path = child / "analysis.json"
        if not analysis_path.is_file():
            items.append(
                ProductSummary(
                    name=name,
                    description="",
                    analysis_timestamp=None,
                    primary_language=None,
                    has_analysis=False,
                )
            )
            continue
        meta = _read_analysis_metadata(analysis_path)
        items.append(
            ProductSummary(
                name=name,
                description=(meta.get("description") or "")[:500],
                analysis_timestamp=meta.get("analysis_timestamp"),
                primary_language=meta.get("primary_language"),
                has_analysis=True,
            )
        )
    return items


def _read_analysis_metadata(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    meta = data.get("metadata") or {}
    ts = meta.get("analysis_timestamp")
    if ts is not None and not isinstance(ts, str):
        ts = str(ts)
    tech = data.get("tech_stack") or {}
    primary = tech.get("primary_language")
    if primary is not None and not isinstance(primary, str):
        primary = str(primary)
    return {
        "description": meta.get("description") or "",
        "analysis_timestamp": ts,
        "primary_language": primary,
        "repo_path": meta.get("repo_path"),
    }


def safe_product_dir(profiles_root: Path, product_name: str) -> Path:
    """Return resolved product profile directory or raise ``ValueError``."""
    validate_product_name(product_name)
    resolved = (profiles_root / product_name).resolve()
    if not resolved.is_relative_to(profiles_root):
        raise ValueError("Invalid product path")
    if not resolved.is_dir():
        raise FileNotFoundError(product_name)
    return resolved


def list_onboarding_roles(product_dir: Path) -> list[tuple[str, str]]:
    """Return [(role_slug, label), ...] from ``docs/onboarding-*.md``."""
    docs = product_dir / "docs"
    if not docs.is_dir():
        return []
    roles: list[tuple[str, str]] = []
    for f in sorted(docs.glob("onboarding-*.md")):
        m = _ONBOARDING_ROLE_RE.match(f.name)
        if not m:
            continue
        role = m.group(1)
        roles.append((role, role.replace("_", " ").title()))
    return roles


def read_onboarding_markdown(profiles_root: Path, product_name: str, role: str) -> str:
    """Read ``docs/onboarding-{role}.md`` after validating paths."""
    if not re.match(r"^[a-z_]+$", role):
        raise ValueError("Invalid role")
    product_dir = safe_product_dir(profiles_root, product_name)
    path = product_dir / "docs" / f"onboarding-{role}.md"
    if not path.is_file():
        raise FileNotFoundError(str(path))
    return path.read_text(encoding="utf-8")


def packaged_doc_slugs() -> list[str]:
    """Slugs for markdown files shipped under ``webapp/content/docs/``."""
    if not _CONTENT_DIR.is_dir():
        return []
    return sorted(p.stem for p in _CONTENT_DIR.glob("*.md"))


def read_packaged_doc(slug: str) -> str:
    if not re.match(r"^[a-z0-9_-]+$", slug):
        raise ValueError("Invalid doc slug")
    path = _CONTENT_DIR / f"{slug}.md"
    if not path.is_file():
        raise FileNotFoundError(slug)
    return path.read_text(encoding="utf-8")


def render_markdown_to_html(text: str) -> str:
    import markdown

    return markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "nl2br"],
    )
