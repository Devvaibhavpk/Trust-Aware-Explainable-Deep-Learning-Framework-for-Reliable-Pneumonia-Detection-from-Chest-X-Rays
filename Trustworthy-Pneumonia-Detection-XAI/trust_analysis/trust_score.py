"""Backward-compatible re-export. Prefer: from explainability.trustscore import ..."""
from explainability.trustscore import (
    TrustAnalyzer,
    TrustEngine,
    TrustEngineConfig,
    compute_trust_score,
    compute_trust_score_with_uncertainty,
    get_trust_level,
    heatmap_focus_score,
)

__all__ = [
    "TrustAnalyzer",
    "TrustEngine",
    "TrustEngineConfig",
    "compute_trust_score",
    "compute_trust_score_with_uncertainty",
    "get_trust_level",
    "heatmap_focus_score",
]
