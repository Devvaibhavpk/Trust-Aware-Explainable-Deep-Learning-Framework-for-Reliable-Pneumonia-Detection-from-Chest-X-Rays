"""
Prepare Chest X-Ray Pneumonia dataset into train/val/test structure.

Kaggle dataset: https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import DATA_DIR
from datasets.split_dataset import split_kaggle_dataset


def main() -> None:
    """Split a Kaggle chest_xray folder into the project's data/ directory."""
    parser = argparse.ArgumentParser(
        description="Copy Kaggle chest X-ray data into data/train, data/val, and data/test"
    )
    parser.add_argument(
        "source",
        type=str,
        help="Path to the Kaggle chest_xray root or its train folder",
    )
    parser.add_argument("--val_ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--dest", type=str, default=str(DATA_DIR))
    args = parser.parse_args()

    src = Path(args.source)
    if not src.exists():
        print(f"Folder not found: {src}")
        sys.exit(1)

    split_kaggle_dataset(
        source_root=src,
        dest_root=Path(args.dest),
        val_ratio=args.val_ratio,
        seed=args.seed,
    )
    print("Done. Train and val images are disjoint. Test images were copied from Kaggle test/ if present.")


if __name__ == "__main__":
    main()
