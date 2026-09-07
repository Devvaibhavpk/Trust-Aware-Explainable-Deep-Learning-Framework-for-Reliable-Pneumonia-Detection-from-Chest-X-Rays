"""
Monte Carlo Dropout Uncertainty Estimation.

Implements stochastic inference by enabling dropout at test time, running
multiple forward passes, and computing statistics over the resulting
probability distribution.

Key function:
    predict_with_uncertainty(model, image_tensor, n_samples, device)

Reference:
    Gal & Ghahramani (2016) "Dropout as a Bayesian Approximation"
    https://arxiv.org/abs/1506.02142
"""

from __future__ import annotations

import torch
import torch.nn as nn
import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def enable_dropout(model: nn.Module) -> None:
    """
    Set all Dropout / Dropout2d layers to training mode while leaving
    everything else in eval mode.  This is the canonical MC-Dropout trick:
    activating stochasticity without affecting BatchNorm running stats.

    Call model.eval() first, then call this function.
    """
    for module in model.modules():
        if isinstance(module, (nn.Dropout, nn.Dropout2d)):
            module.train()


def disable_dropout(model: nn.Module) -> None:
    """Restore all Dropout layers to eval mode (deterministic)."""
    for module in model.modules():
        if isinstance(module, (nn.Dropout, nn.Dropout2d)):
            module.eval()


# ---------------------------------------------------------------------------
# Core inference function
# ---------------------------------------------------------------------------

def predict_with_uncertainty(
    model: nn.Module,
    image_tensor: torch.Tensor,
    n_samples: int = 30,
    device: Optional[torch.device] = None,
) -> dict:
    """
    Run Monte Carlo Dropout inference and return prediction statistics.

    Steps
    -----
    1. Put model into eval mode (freezes BN, etc.)
    2. Re-enable dropout layers so each forward pass is stochastic.
    3. Run `n_samples` forward passes and collect sigmoid probabilities.
    4. Compute mean, variance, and std of the probability distribution.
    5. Restore model to fully deterministic eval mode.

    Parameters
    ----------
    model : nn.Module
        Any CNN with at least one Dropout layer.  Works out-of-the-box
        with ResNet18 (has Dropout in final classifier layer when trained
        with dropout) and ChestXRayCNN (explicit Dropout(0.5) in classifier).
    image_tensor : torch.Tensor
        Pre-processed input of shape (1, C, H, W).
    n_samples : int
        Number of stochastic forward passes (30 is a common default).
    device : torch.device or None
        If None, inferred from model parameters.

    Returns
    -------
    dict with:
        mean_prediction  (float)   — mean P(pneumonia) across all samples
        variance         (float)   — variance of P(pneumonia); high = uncertain
        std              (float)   — standard deviation of P(pneumonia)
        samples          (ndarray) — shape (n_samples,); all probabilities
    """
    if device is None:
        try:
            device = next(model.parameters()).device
        except StopIteration:
            device = torch.device("cpu")

    image_tensor = image_tensor.to(device)

    # 1. Set base eval mode (freezes BatchNorm etc.)
    model.eval()

    # 2. Activate dropout stochasticity
    enable_dropout(model)

    probabilities: list[float] = []

    # 3. Stochastic forward passes
    with torch.no_grad():
        for _ in range(n_samples):
            logits = model(image_tensor)
            # Binary sigmoid output (single logit)
            if logits.size(-1) == 1:
                prob = torch.sigmoid(logits).item()
            else:
                # Multi-class softmax — take P(class 1 = pneumonia)
                prob = torch.softmax(logits, dim=-1)[0, 1].item()
            probabilities.append(prob)

    # 4. Restore fully deterministic eval mode
    model.eval()  # this also calls .eval() on all sub-modules, disabling dropout

    # 5. Compute statistics
    samples_np = np.array(probabilities, dtype=np.float32)
    mean_pred = float(np.mean(samples_np))
    variance = float(np.var(samples_np))       # uncertainty score
    std = float(np.std(samples_np))

    return {
        "mean_prediction": mean_pred,
        "variance": variance,
        "std": std,
        "samples": samples_np,
    }


# ---------------------------------------------------------------------------
# Convenience class
# ---------------------------------------------------------------------------

class MCDropoutPredictor:
    """
    Stateful wrapper around predict_with_uncertainty.

    Usage
    -----
        predictor = MCDropoutPredictor(model, n_samples=30, device=device)
        result = predictor.predict(image_tensor)

    The predictor keeps a reference to the model and device so callers
    don't have to pass them repeatedly.
    """

    def __init__(
        self,
        model: nn.Module,
        n_samples: int = 30,
        device: Optional[torch.device] = None,
    ) -> None:
        self.model = model
        self.n_samples = n_samples
        if device is None:
            try:
                self.device = next(model.parameters()).device
            except StopIteration:
                self.device = torch.device("cpu")
        else:
            self.device = device

    def predict(self, image_tensor: torch.Tensor) -> dict:
        """
        Run MC Dropout inference.

        Parameters
        ----------
        image_tensor : torch.Tensor
            Pre-processed image of shape (1, C, H, W).

        Returns
        -------
        dict — same format as predict_with_uncertainty().
        """
        return predict_with_uncertainty(
            model=self.model,
            image_tensor=image_tensor,
            n_samples=self.n_samples,
            device=self.device,
        )

    def uncertainty_level(self, variance: float) -> str:
        """
        Convert raw variance into a human-readable level label.

        Thresholds
        ----------
        - Low uncertainty   : variance < 0.01
        - Medium uncertainty: 0.01 ≤ variance < 0.05
        - High uncertainty  : variance ≥ 0.05
        """
        if variance < 0.01:
            return "low"
        if variance < 0.05:
            return "medium"
        return "high"


# ---------------------------------------------------------------------------
# High-level wrappers (from legacy root uncertainty.py)
# ---------------------------------------------------------------------------

def mc_dropout_uncertainty(
    model,
    image_tensor,
    n_samples: int = 30,
    device=None,
) -> dict:
    """Thin wrapper around predict_with_uncertainty()."""
    return predict_with_uncertainty(
        model=model,
        image_tensor=image_tensor,
        n_samples=n_samples,
        device=device,
    )


def ood_flag_from_confidence_uncertainty(
    calibrated_confidence: float,
    uncertainty: float,
    config=None,
) -> bool:
    """Apply the OOD decision rule using TrustEngine."""
    from explainability.trustscore import TrustEngine, TrustEngineConfig

    engine = TrustEngine(config=config or TrustEngineConfig())
    return engine.detect_ood(
        calibrated_confidence=calibrated_confidence,
        uncertainty=uncertainty,
    )
