"""Backward-compatible re-export. Prefer: from explainability.trustscore import ..."""
from explainability.trustscore import (
    TrustAnalyzer,
    TrustEngine,
    TrustEngineConfig,
    compute_trust_score,
    get_trust_level,
)

__all__ = [
    "TrustAnalyzer",
    "TrustEngine",
    "TrustEngineConfig",
    "compute_trust_score",
    "get_trust_level",
]
