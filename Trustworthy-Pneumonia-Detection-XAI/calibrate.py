"""Backward-compatible entry point. Prefer: python -m evaluation.calibrate"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluation.calibrate import main

if __name__ == "__main__":
    main()
