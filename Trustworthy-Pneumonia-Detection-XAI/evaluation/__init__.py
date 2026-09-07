"""Evaluation module for metrics, calibration, and reliability analysis."""
from evaluation.calibration import TemperatureScaling, fit_temperature
from evaluation.confusion_matrix import plot_confusion_matrix
from evaluation.metrics import compute_classification_metrics, compute_confusion_matrix
from evaluation.reliability import compute_ece, reliability_diagram

__all__ = [
    "TemperatureScaling",
    "fit_temperature",
    "plot_confusion_matrix",
    "compute_classification_metrics",
    "compute_confusion_matrix",
    "compute_ece",
    "reliability_diagram",
]
