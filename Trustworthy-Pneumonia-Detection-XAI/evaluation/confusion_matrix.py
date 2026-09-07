"""
Confusion matrix visualization utilities.
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_confusion_matrix(
    cm: np.ndarray,
    class_names: list[str],
    ax: plt.Axes | None = None,
    title: str = "Confusion Matrix",
) -> plt.Axes:
    """
    Plot a heatmap confusion matrix.

    Args:
        cm: Confusion matrix array.
        class_names: Class label names for axes.
        ax: Optional matplotlib axes.
        title: Plot title.

    Returns:
        Matplotlib axes with the plotted heatmap.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(5, 4))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        ax=ax,
    )
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.set_title(title)
    return ax
