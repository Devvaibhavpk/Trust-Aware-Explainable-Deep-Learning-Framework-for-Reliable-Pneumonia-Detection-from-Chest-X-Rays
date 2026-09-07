"""
CLI entry point for single-image chest X-ray inference.
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import DEFAULT_MC_SAMPLES, MODEL_SAVE_DIR
from inference.inference import run_pipeline


def main() -> None:
    """Run uncertainty-aware inference on a single chest X-ray image."""
    parser = argparse.ArgumentParser(
        description="Uncertainty-aware chest X-ray screening with Grad-CAM and MC Dropout."
    )
    parser.add_argument("image_path", type=str, help="Path to chest X-ray image")
    parser.add_argument("--save_dir", type=str, default=str(MODEL_SAVE_DIR))
    parser.add_argument("--output", type=str, default=None, help="Output PNG path")
    parser.add_argument(
        "--n_samples",
        type=int,
        default=DEFAULT_MC_SAMPLES,
        help="MC Dropout samples (default: 30)",
    )
    parser.add_argument(
        "--densenet_dir",
        type=str,
        default=None,
        help="Checkpoint directory for DenseNet121 ensemble member (optional).",
    )
    parser.add_argument(
        "--efficientnet_dir",
        type=str,
        default=None,
        help="Checkpoint directory for EfficientNet-B0 ensemble member (optional).",
    )
    args = parser.parse_args()

    run_pipeline(
        args.image_path,
        args.save_dir,
        args.output,
        n_mc_samples=args.n_samples,
        densenet_dir=args.densenet_dir,
        efficientnet_dir=args.efficientnet_dir,
    )


if __name__ == "__main__":
    main()
