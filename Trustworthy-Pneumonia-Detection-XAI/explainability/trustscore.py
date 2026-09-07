"""
Trust scoring, trust levels, and the unified TrustEngine.

Combines trust analysis from the original trust_analysis module with
the research-grade TrustEngine (ensemble agreement + OOD detection).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional, Tuple

import numpy as np

TrustLevel = Literal["high", "medium", "low"]


# ---------------------------------------------------------------------------
# Heatmap utilities
# ---------------------------------------------------------------------------

def _central_region_mask(height: int, width: int, center_ratio: float = 0.5) -> np.ndarray:
    """Binary mask for central region (approximate lung area in chest X-ray)."""
    y = np.linspace(0, 1, height)
    x = np.linspace(0, 1, width)
    low = (1 - center_ratio) / 2
    high = 1 - low
    in_y = (y >= low) & (y <= high)
    in_x = (x >= low) & (x <= high)
    return np.outer(in_y, in_x).astype(np.float32)


def heatmap_focus_score(heatmap: np.ndarray, center_ratio: float = 0.5) -> float:
    """Fraction of Grad-CAM activation mass inside the central lung region."""
    h, w = heatmap.shape
    mask = _central_region_mask(h, w, center_ratio)
    total_mass = np.sum(heatmap) + 1e-10
    central_mass = np.sum(heatmap * mask)
    return float(central_mass / total_mass)


def compute_trust_score(
    calibrated_confidence: float,
    heatmap: np.ndarray,
    center_ratio: float = 0.5,
    w_confidence: float = 0.5,
    w_focus: float = 0.5,
) -> Tuple[float, float]:
    """Legacy trust score without uncertainty (weighted sum)."""
    focus_score = heatmap_focus_score(heatmap, center_ratio)
    confidence_component = max(calibrated_confidence, 1.0 - calibrated_confidence)
    trust_score = w_confidence * confidence_component + w_focus * focus_score
    return float(np.clip(trust_score, 0, 1)), focus_score


def compute_trust_score_with_uncertainty(
    calibrated_confidence: float,
    heatmap: np.ndarray,
    uncertainty: float,
    center_ratio: float = 0.5,
) -> Tuple[float, float]:
    """Uncertainty-aware trust score: Confidence × Focus × (1 − Uncertainty)."""
    focus_score = heatmap_focus_score(heatmap, center_ratio)
    confidence_component = max(calibrated_confidence, 1.0 - calibrated_confidence)
    uncertainty_clamped = float(np.clip(uncertainty, 0.0, 1.0))
    trust_score = confidence_component * focus_score * (1.0 - uncertainty_clamped)
    return float(np.clip(trust_score, 0, 1)), focus_score


def compute_trust_score_with_uncertainty(
    calibrated_confidence: float,
    heatmap: np.ndarray,
    uncertainty: float,
    center_ratio: float = 0.5,
) -> Tuple[float, float]:
    """Uncertainty-aware trust score: Confidence × Focus × (1 − Uncertainty)."""
    focus_score = heatmap_focus_score(heatmap, center_ratio)
    confidence_component = max(calibrated_confidence, 1.0 - calibrated_confidence)
    uncertainty_clamped = float(np.clip(uncertainty, 0.0, 1.0))
    trust_score = confidence_component * focus_score * (1.0 - uncertainty_clamped)
    return float(np.clip(trust_score, 0, 1)), focus_score


def get_trust_level(
    trust_score: float,
    calibrated_confidence: float,
    focus_score: float,
    uncertainty: Optional[float] = None,
    high_threshold: float = 0.7,
    low_threshold: float = 0.4,
) -> TrustLevel:
    """Assign High / Medium / Low trust level from confidence, focus, and uncertainty."""
    if uncertainty is not None:
        if uncertainty > 0.3 or focus_score < 0.35:
            return "low"
        if calibrated_confidence > 0.8 and uncertainty < 0.1:
            return "high"
        if (0.6 <= calibrated_confidence <= 0.8) or (0.1 <= uncertainty <= 0.3):
            return "medium"
        return "medium"

    if trust_score >= high_threshold:
        return "high"
    if trust_score <= low_threshold:
        return "low"
    return "medium"


class TrustAnalyzer:
    """Uncertainty-aware trust analyzer combining confidence, heatmap focus, and variance."""

    def __init__(
        self,
        center_ratio: float = 0.5,
        w_confidence: float = 0.5,
        w_focus: float = 0.5,
        high_threshold: float = 0.7,
        low_threshold: float = 0.4,
    ) -> None:
        self.center_ratio = center_ratio
        self.w_confidence = w_confidence
        self.w_focus = w_focus
        self.high_threshold = high_threshold
        self.low_threshold = low_threshold

    def analyze(
        self,
        calibrated_confidence: float,
        heatmap: np.ndarray,
        uncertainty: Optional[float] = None,
    ) -> dict:
        """Compute trust score and level from calibrated confidence and Grad-CAM heatmap."""
        if uncertainty is not None:
            trust_score, focus_score = compute_trust_score_with_uncertainty(
                calibrated_confidence,
                heatmap,
                uncertainty,
                center_ratio=self.center_ratio,
            )
        else:
            trust_score, focus_score = compute_trust_score(
                calibrated_confidence,
                heatmap,
                center_ratio=self.center_ratio,
                w_confidence=self.w_confidence,
                w_focus=self.w_focus,
            )

        trust_level = get_trust_level(
            trust_score,
            calibrated_confidence,
            focus_score,
            uncertainty=uncertainty,
            high_threshold=self.high_threshold,
            low_threshold=self.low_threshold,
        )

        return {
            "trust_score": trust_score,
            "focus_score": focus_score,
            "trust_level": trust_level,
            "uncertainty_score": uncertainty if uncertainty is not None else 0.0,
        }


# ---------------------------------------------------------------------------
# Unified TrustEngine (ensemble + OOD)
# ---------------------------------------------------------------------------

@dataclass
class TrustEngineConfig:
    """Hyperparameters for the trust engine and OOD rule."""

    confidence_threshold: float = 0.6
    uncertainty_threshold: float = 0.03


class TrustEngine:
    """
    Research-grade trust computation and OOD detection.

    TrustScore = Confidence × FocusScore × (1 − Uncertainty) × AgreementScore
    """

    def __init__(self, config: TrustEngineConfig | None = None) -> None:
        self.config = config or TrustEngineConfig()

    def compute_trust_score(
        self,
        calibrated_confidence: float,
        focus_score: float,
        uncertainty: float,
        agreement_score: float,
    ) -> float:
        """Compute scalar TrustScore in [0, 1]."""
        confidence_component = max(calibrated_confidence, 1.0 - calibrated_confidence)
        focus_clamped = float(np.clip(focus_score, 0.0, 1.0))
        agreement_clamped = float(np.clip(agreement_score, 0.0, 1.0))
        uncertainty_clamped = float(np.clip(uncertainty, 0.0, 1.0))

        trust = (
            confidence_component
            * focus_clamped
            * (1.0 - uncertainty_clamped)
            * agreement_clamped
        )
        return float(np.clip(trust, 0.0, 1.0))

    def detect_ood(self, calibrated_confidence: float, uncertainty: float) -> bool:
        """Mark sample as UNRELIABLE when confidence is low and uncertainty is high."""
        return bool(
            (calibrated_confidence < self.config.confidence_threshold)
            and (uncertainty > self.config.uncertainty_threshold)
        )

    def summarize(
        self,
        calibrated_confidence: float,
        focus_score: float,
        uncertainty: float,
        agreement_score: float,
    ) -> dict:
        """Return trust score and OOD flag in one dict."""
        trust_score = self.compute_trust_score(
            calibrated_confidence=calibrated_confidence,
            focus_score=focus_score,
            uncertainty=uncertainty,
            agreement_score=agreement_score,
        )
        ood_flag = self.detect_ood(
            calibrated_confidence=calibrated_confidence,
            uncertainty=uncertainty,
        )
        return {
            "trust_score": trust_score,
            "ood_flag": ood_flag,
        }
