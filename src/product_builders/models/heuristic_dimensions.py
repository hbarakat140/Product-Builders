"""Single source of truth: which ``ProductProfile`` fields are heuristic (analyzers), not metadata/deep."""

from __future__ import annotations

from product_builders.models.profile import ProductProfile

HEURISTIC_PROFILE_FIELDS: frozenset[str] = frozenset(ProductProfile.model_fields.keys()) - {
    "metadata",
    "scopes",
    "architecture_deep",
    "domain_model_deep",
    "implicit_conventions_deep",
}
