"""
Reliability metrics and calibration diagrams (ECE, reliability plots).
"""

from typing import Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")


def compute_ece(
    probs: np.ndarray,
    labels: np.ndarray,
    n_bins: int = 10,
) -> float:
    """
    Expected Calibration Error (ECE).

    Args:
        probs: Predicted probability for positive class, shape (N,).
        labels: Ground-truth binary labels, shape (N,).
        n_bins: Number of confidence bins.

    Returns:
        Scalar ECE value.
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        low, high = bin_boundaries[i], bin_boundaries[i + 1]
        in_bin = (probs > low) & (probs <= high)
        prop = np.mean(in_bin)
        if prop > 0:
            avg_confidence = np.mean(probs[in_bin])
            avg_accuracy = np.mean(labels[in_bin])
            ece += prop * np.abs(avg_accuracy - avg_confidence)
    return float(ece)


def reliability_diagram(
    probs: np.ndarray,
    labels: np.ndarray,
    n_bins: int = 10,
    title: str = "Reliability Diagram",
    path: Optional[str] = None,
    ax: Optional[plt.Axes] = None,
) -> Tuple[float, np.ndarray, np.ndarray]:
    """
    Plot reliability diagram: predicted confidence vs accuracy per bin.

    Returns:
        Tuple of (ECE, bin accuracies, bin confidences).
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_accs = []
    bin_confs = []
    for i in range(n_bins):
        low, high = bin_boundaries[i], bin_boundaries[i + 1]
        in_bin = (probs > low) & (probs <= high)
        if np.sum(in_bin) > 0:
            bin_accs.append(np.mean(labels[in_bin]))
            bin_confs.append(np.mean(probs[in_bin]))
        else:
            bin_accs.append(np.nan)
            bin_confs.append(np.nan)

    bin_accs_arr = np.array(bin_accs)
    bin_confs_arr = np.array(bin_confs)
    ece = compute_ece(probs, labels, n_bins)

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    else:
        fig = ax.figure if hasattr(ax, "figure") else None

    bin_centers = (bin_boundaries[:-1] + bin_boundaries[1:]) / 2
    ax.bar(
        bin_centers,
        bin_accs_arr,
        width=0.9 / n_bins,
        align="center",
        label="Accuracy",
        color="steelblue",
        alpha=0.8,
    )
    ax.plot(bin_centers, bin_confs_arr, "o-", color="darkred", linewidth=2, markersize=8, label="Confidence")
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Perfect calibration")
    ax.set_xlabel("Confidence")
    ax.set_ylabel("Accuracy")
    ax.set_title(f"{title}\nECE = {ece:.4f}")
    ax.legend(loc="lower right")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    plt.tight_layout()

    if path:
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
    elif fig is not None:
        plt.close(fig)

    return ece, bin_accs_arr, bin_confs_arr
