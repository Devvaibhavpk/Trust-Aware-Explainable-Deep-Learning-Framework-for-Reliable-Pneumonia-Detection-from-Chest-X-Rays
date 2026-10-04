"""
Faculty demo helper: check the environment, then run the next useful step.
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import DATA_DIR, MODEL_SAVE_DIR, MODEL_WEIGHTS_NAME, OUTPUT_DIR
from datasets.dataset import ChestXRayDataset


def _run(cmd: list[str]) -> int:
    print("\n>", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(PROJECT_ROOT))


def _first_test_image() -> Path | None:
    test_root = DATA_DIR / "test"
    dataset = ChestXRayDataset(root=str(test_root), transform=None)
    if len(dataset) == 0:
        return None
    return Path(dataset.samples[0][0])


def main() -> None:
    parser = argparse.ArgumentParser(description="Check setup and run a faculty demo")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Train a 2-epoch subset model if no checkpoint exists (CPU-friendly).",
    )
    parser.add_argument(
        "--skip_train",
        action="store_true",
        help="Only run inference if a checkpoint already exists.",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Trustworthy Pneumonia Detection — faculty demo check")
    print("=" * 60)
    print(f"Project: {PROJECT_ROOT}")
    print(f"Python:  {sys.executable}")

    try:
        import torch

        print(f"PyTorch: {torch.__version__}")
        print(f"CUDA:    {torch.cuda.is_available()}")
    except ImportError:
        print("PyTorch is not installed. Run: pip install -r requirements.txt")
        sys.exit(1)

    train_n = len(ChestXRayDataset(root=str(DATA_DIR / "train")))
    val_n = len(ChestXRayDataset(root=str(DATA_DIR / "val")))
    test_n = len(ChestXRayDataset(root=str(DATA_DIR / "test")))
    print(f"Dataset: train={train_n}, val={val_n}, test={test_n}")

    if train_n == 0:
        print("\nNo images found under data/train.")
        print("Download the Kaggle Chest X-Ray Pneumonia dataset, then run:")
        print('  python scripts/prepare_dataset.py "C:\\path\\to\\chest_xray"')
        sys.exit(1)

    ckpt = MODEL_SAVE_DIR / MODEL_WEIGHTS_NAME
    if not ckpt.exists() and not args.skip_train:
        print(f"\nNo checkpoint at {ckpt}")
        train_cmd = [sys.executable, "-m", "training.train"]
        if args.quick:
            train_cmd.append("--quick")
            print("Starting a quick 2-epoch demo training run...")
        else:
            print("Starting full training (this can take a long time on CPU)...")
        code = _run(train_cmd)
        if code != 0:
            sys.exit(code)
        code = _run([sys.executable, "-m", "evaluation.calibrate"])
        if code != 0:
            sys.exit(code)
        code = _run([sys.executable, "-m", "evaluation.evaluate"])
        if code != 0:
            sys.exit(code)
    elif not ckpt.exists():
        print(f"No checkpoint at {ckpt}. Re-run without --skip_train.")
        sys.exit(1)
    else:
        print(f"Found checkpoint: {ckpt}")

    image = _first_test_image()
    if image is None:
        print("No test images found under data/test. Copy the Kaggle test set there.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    code = _run([sys.executable, "-m", "inference.predict", str(image)])
    if code != 0:
        sys.exit(code)

    print("\nDemo complete. Show faculty:")
    print(f"  - inference figure in {OUTPUT_DIR}")
    print("  - training_curves.png, reliability_diagrams.png, evaluation_results.png if generated")
    print("  - Presentation.md for slide talking points")


if __name__ == "__main__":
    main()
