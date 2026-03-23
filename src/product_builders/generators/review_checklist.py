"""Review Checklist Generator — generates review-checklist.md for AI review integration.

The review checklist serves double duty:
  - Custom instructions for AI review tools (CodeRabbit, Copilot, etc.)
  - Human-readable PR review checklist for developer reviewers
"""

from __future__ import annotations

import logging
from pathlib import Path

from product_builders.generators.base import BaseGenerator
from product_builders.generators.registry import register
from product_builders.models.profile import ProductProfile
from product_builders.models.scopes import ContributorRole

logger = logging.getLogger(__name__)


class ReviewChecklistGenerator(BaseGenerator):
    @property
    def name(self) -> str:
        return "Review Checklist Generator"

    def generate(
        self,
        profile: ProductProfile,
        output_dir: Path,
        *,
        role: ContributorRole | None = None,
    ) -> list[Path]:
        context = {"profile": profile}
        content = self.render_template("review-checklist.md.j2", **context)
        path = self.write_file(output_dir / "review-checklist.md", content)
        return [path]


register(ReviewChecklistGenerator())
