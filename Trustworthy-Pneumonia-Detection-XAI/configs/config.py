"""
Central configuration for model type, paths, and training hyperparameters.

Change MODEL_TYPE to 'custom', 'resnet18', 'vgg16', 'densenet121', or 'efficientnet_b0'.
"""

from pathlib import Path

# Model architecture
MODEL_TYPE = "resnet18"

# Paths — project root is parent of configs/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODEL_SAVE_DIR = PROJECT_ROOT / "checkpoints"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
LOGS_DIR = OUTPUT_DIR / "logs"
PREDICTIONS_DIR = OUTPUT_DIR / "predictions"
REPORTS_DIR = OUTPUT_DIR / "reports"

# Training
IMAGE_SIZE = 224
BATCH_SIZE = 32
NUM_EPOCHS = 15
LEARNING_RATE = 1e-4
NUM_WORKERS = 0

# Filenames
MODEL_WEIGHTS_NAME = "chestxray_best.pt"
CALIBRATOR_NAME = "temperature_scaling.pt"
MODEL_CONFIG_NAME = "model_config.txt"

# Trust / uncertainty defaults
DEFAULT_MC_SAMPLES = 30
DEFAULT_ECE_BINS = 10
HEATMAP_THRESHOLD = 0.4


def ensure_dirs() -> None:
    """Create output and checkpoint directories if they do not exist."""
    MODEL_SAVE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
