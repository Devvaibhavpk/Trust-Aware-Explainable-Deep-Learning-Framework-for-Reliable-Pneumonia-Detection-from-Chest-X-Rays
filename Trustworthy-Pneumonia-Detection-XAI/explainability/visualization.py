"""
Visualization helpers for uncertainty-aware Grad-CAM inference figures.
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

TRUST_COLORS = {
    "High": "#2ecc71",
    "Medium": "#f39c12",
    "Low": "#e74c3c",
}


def plot_mc_histogram(ax, samples: np.ndarray, mean: float, std: float) -> None:
    """Plot MC Dropout probability distribution on the given axes."""
    ax.hist(
        samples,
        bins=15,
        range=(0, 1),
        color="#3498db",
        edgecolor="white",
        alpha=0.85,
    )
    ax.axvline(mean, color="#e74c3c", linewidth=2.0, linestyle="--", label=f"Mean: {mean:.3f}")
    ax.fill_betweenx(
        [0, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 1],
        max(0, mean - std),
        min(1, mean + std),
        alpha=0.18,
        color="#e74c3c",
        label=f"±1 std: {std:.3f}",
    )
    ax.set_xlim(0, 1)
    ax.set_xlabel("P(Pneumonia)", fontsize=9)
    ax.set_ylabel("Frequency", fontsize=9)
    ax.set_title("MC Dropout Sample Distribution", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.3)


def plot_summary_panel(ax, result: dict) -> None:
    """Render a formatted inference summary panel."""
    ax.axis("off")
    trust_level = result["trust_level"]
    trust_color = TRUST_COLORS.get(trust_level, "#95a5a6")

    lines = [
        ("INFERENCE SUMMARY", None, 13, "bold"),
        ("─" * 34, None, 9, "normal"),
        (f"Predicted class:       {result['predicted_class']}", None, 10, "normal"),
        (f"Raw confidence:        {result['raw_confidence']:.4f}", None, 10, "normal"),
        (f"Calibrated confidence: {result['calibrated_confidence']:.4f}", None, 10, "normal"),
        (f"Uncertainty (variance):{result['uncertainty_score']:.6f}", None, 10, "normal"),
        (f"Focus score:           {result['focus_score']:.4f}", None, 10, "normal"),
        (f"Trust score:           {result['trust_score']:.4f}", None, 10, "normal"),
        ("─" * 34, None, 9, "normal"),
        (f"Trust level: {trust_level}", trust_color, 12, "bold"),
    ]

    y = 0.97
    for text, color, size, weight in lines:
        ax.text(
            0.05,
            y,
            text,
            transform=ax.transAxes,
            fontsize=size,
            fontweight=weight,
            color=color or "#2c3e50",
            va="top",
            family="monospace",
        )
        y -= 0.10

    badge = mpatches.FancyBboxPatch(
        (0.05, 0.06),
        0.90,
        0.08,
        boxstyle="round,pad=0.01",
        facecolor=trust_color,
        edgecolor="none",
        alpha=0.20,
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(badge)


def build_inference_figure(
    img_np: np.ndarray,
    overlay: np.ndarray,
    samples: np.ndarray,
    mean_pred: float,
    std_pred: float,
    result: dict,
) -> plt.Figure:
    """Compose the 2×2 uncertainty-aware inference figure."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor("#1a1a2e")

    panel_titles = ["Original X-ray", "Grad-CAM Overlay"]
    images_np = [img_np, overlay]

    for col, (title, img) in enumerate(zip(panel_titles, images_np)):
        ax = axes[0][col]
        ax.imshow(img)
        ax.axis("off")
        ax.set_title(title, color="white", fontsize=11, fontweight="bold", pad=6)
        ax.set_facecolor("#1a1a2e")

    ax_hist = axes[1][0]
    ax_hist.set_facecolor("#0f3460")
    plot_mc_histogram(ax_hist, samples, mean_pred, std_pred)
    ax_hist.tick_params(colors="white")
    ax_hist.xaxis.label.set_color("white")
    ax_hist.yaxis.label.set_color("white")
    ax_hist.title.set_color("white")
    for spine in ax_hist.spines.values():
        spine.set_edgecolor("#34495e")

    ax_sum = axes[1][1]
    ax_sum.set_facecolor("#0f3460")
    plot_summary_panel(ax_sum, result)

    trust_level = result["trust_level"]
    trust_color = TRUST_COLORS.get(trust_level, "#95a5a6")
    fig.suptitle(
        f"Chest X-ray Screening  ·  {result['predicted_class']}  ·  Trust: {trust_level}",
        color=trust_color,
        fontsize=14,
        fontweight="bold",
        y=1.01,
    )
    plt.tight_layout()
    return fig
