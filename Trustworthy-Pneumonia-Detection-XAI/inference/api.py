"""
Programmatic API for chest X-ray pneumonia screening.
"""

from inference.inference import run_pipeline

__all__ = ["run_pipeline", "predict"]


def predict(
    image_path: str,
    save_dir: str | None = None,
    output_path: str | None = None,
    n_mc_samples: int = 30,
    densenet_dir: str | None = None,
    efficientnet_dir: str | None = None,
) -> dict:
    """
    Run the full trustworthy inference pipeline on a single image.

    Args:
        image_path: Path to the chest X-ray image.
        save_dir: Directory containing model checkpoints.
        output_path: Optional path for the visualization PNG.
        n_mc_samples: Number of MC Dropout forward passes.
        densenet_dir: Optional DenseNet121 ensemble checkpoint directory.
        efficientnet_dir: Optional EfficientNet-B0 ensemble checkpoint directory.

    Returns:
        Dictionary with prediction, confidence, uncertainty, and trust metrics.
    """
    from configs.config import MODEL_SAVE_DIR

    return run_pipeline(
        image_path=image_path,
        save_dir=save_dir or str(MODEL_SAVE_DIR),
        output_path=output_path,
        n_mc_samples=n_mc_samples,
        densenet_dir=densenet_dir,
        efficientnet_dir=efficientnet_dir,
    )
