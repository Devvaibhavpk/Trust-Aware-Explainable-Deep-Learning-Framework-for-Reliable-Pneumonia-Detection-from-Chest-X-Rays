"""
Ensemble-based agreement scoring for CNN classifiers.

This module is intentionally model-agnostic: it operates purely on
per-model predictions or probabilities so it can be reused with
ResNet18, DenseNet121, EfficientNet-B0, or any future architecture.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable, List, Sequence, Tuple

import numpy as np


def majority_vote(
    class_indices: Sequence[int],
) -> Tuple[int, float]:
    """
    Compute majority class and agreement score from discrete predictions.

    AgreementScore = (# models with majority prediction) / total_models
    """
    if len(class_indices) == 0:
        raise ValueError("class_indices must be non-empty")

    counts = Counter(class_indices)
    majority_class, majority_count = counts.most_common(1)[0]
    agreement_score = float(majority_count / len(class_indices))
    return majority_class, agreement_score


def agreement_from_probabilities(
    probs: Sequence[float],
    threshold: float = 0.5,
) -> Tuple[int, float]:
    """
    Convenience wrapper: compute agreement from pneumonia probabilities.

    Each probability is thresholded at `threshold` to obtain a binary
    prediction (0 = NORMAL, 1 = PNEUMONIA), then majority_vote() is used.
    """
    class_indices = [int(p >= threshold) for p in probs]
    return majority_vote(class_indices)

