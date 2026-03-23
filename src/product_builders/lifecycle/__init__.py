"""Rule lifecycle management — drift detection, feedback, versioning."""

from product_builders.lifecycle.drift import DriftReport, run_drift_check

__all__ = ["DriftReport", "run_drift_check"]
