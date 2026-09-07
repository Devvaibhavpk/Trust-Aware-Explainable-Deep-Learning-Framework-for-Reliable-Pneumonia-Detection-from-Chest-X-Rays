"""
Run full pipeline: train -> calibrate -> evaluate.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    """Execute training, calibration, and evaluation sequentially."""
    steps = [
        ("Training", [sys.executable, "-m", "training.train"]),
        ("Calibration", [sys.executable, "-m", "evaluation.calibrate"]),
        ("Evaluation", [sys.executable, "-m", "evaluation.evaluate"]),
    ]
    for name, cmd in steps:
        print(f"\n{'=' * 60}\n{name}\n{'=' * 60}")
        ret = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
        if ret.returncode != 0:
            print(f"{name} failed with exit code {ret.returncode}")
            sys.exit(ret.returncode)
    print("\nPipeline completed. Run: python -m inference.predict path/to/xray.jpg")


if __name__ == "__main__":
    main()
