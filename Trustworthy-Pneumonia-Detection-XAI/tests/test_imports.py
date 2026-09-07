"""
Smoke tests for imports and configuration after repository reorganization.
"""

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_config_paths_exist() -> None:
    from configs.config import DATA_DIR, MODEL_SAVE_DIR, OUTPUT_DIR, PROJECT_ROOT

    assert PROJECT_ROOT.is_dir()
    assert DATA_DIR.name == "data"
    assert MODEL_SAVE_DIR.name == "checkpoints"
    assert OUTPUT_DIR.name == "outputs"


def test_model_build() -> None:
    from models.cnn_model import build_model

    model = build_model(model_type="resnet18", pretrained=False, num_classes=1)
    assert model is not None


def test_backward_compat_imports() -> None:
    from calibration.temperature_scaling import TemperatureScaling, compute_ece
    from explainability.gradcam import GradCAM
    from explainability.trustscore import TrustEngine, get_trust_level
    from explainability.uncertainty import predict_with_uncertainty
    from models.ensemble import agreement_from_probabilities
    from utils.preprocessing import get_dataloaders, CLASS_NAMES

    assert TemperatureScaling is not None
    assert GradCAM is not None
    assert TrustEngine is not None
    assert callable(predict_with_uncertainty)
    assert callable(get_dataloaders)
    assert CLASS_NAMES == ["NORMAL", "PNEUMONIA"]


def test_legacy_root_shims() -> None:
    import config
    import agreement
    import segmentation
    import trust_engine
    import uncertainty

    assert hasattr(config, "DATA_DIR")
    assert hasattr(agreement, "agreement_from_probabilities")
    assert hasattr(segmentation, "LungSegmenter")
    assert hasattr(trust_engine, "TrustEngine")
    assert hasattr(uncertainty, "predict_with_uncertainty")


@pytest.mark.skipif(
    not (PROJECT_ROOT / "checkpoints" / "chestxray_best.pt").exists(),
    reason="Checkpoint not available",
)
def test_load_checkpoint_if_present() -> None:
    import torch
    from utils.io import load_model_and_calibrator

    device = torch.device("cpu")
    model, model_type, calibrator = load_model_and_calibrator(device, PROJECT_ROOT / "checkpoints")
    assert model_type in {"resnet18", "custom", "vgg16", "densenet121", "efficientnet_b0"}
    assert model is not None
