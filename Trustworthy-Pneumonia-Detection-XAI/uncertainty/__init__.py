"""Backward-compatible re-export. Prefer: from explainability.uncertainty import ..."""
from explainability.uncertainty import (
    MCDropoutPredictor,
    enable_dropout,
    mc_dropout_uncertainty,
    ood_flag_from_confidence_uncertainty,
    predict_with_uncertainty,
)

__all__ = [
    "predict_with_uncertainty",
    "enable_dropout",
    "MCDropoutPredictor",
    "mc_dropout_uncertainty",
    "ood_flag_from_confidence_uncertainty",
]
