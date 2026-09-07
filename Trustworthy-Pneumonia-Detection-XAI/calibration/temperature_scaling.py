"""Backward-compatible re-export. Prefer: from evaluation import ..."""
from evaluation.calibration import TemperatureScaling, fit_temperature
from evaluation.reliability import compute_ece, reliability_diagram

__all__ = ["TemperatureScaling", "fit_temperature", "compute_ece", "reliability_diagram"]
