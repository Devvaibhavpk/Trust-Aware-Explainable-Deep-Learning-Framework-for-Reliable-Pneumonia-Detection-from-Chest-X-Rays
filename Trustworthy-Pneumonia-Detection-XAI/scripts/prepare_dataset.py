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

from datasets.split_dataset import split_folder


def main() -> None:
    """Split a Kaggle train folder into train and validation sets."""
    parser = argparse.ArgumentParser(
        description="Prepare train/val from Kaggle chest x-ray train folder"
    )
    parser.add_argument(
        "train_folder",
        type=str,
        help="Path to folder containing NORMAL and PNEUMONIA subdirs",
    )
    parser.add_argument("--val_ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    src = Path(args.train_folder)
    if not src.exists():
        print(f"Folder not found: {src}")
        return

    split_folder(src, train_ratio=1 - args.val_ratio, val_ratio=args.val_ratio, seed=args.seed)
    print(
        "Done. Ensure test set is in data/test/NORMAL and data/test/PNEUMONIA "
        "(copy from Kaggle test)."
    )


if __name__ == "__main__":
    main()
