"""
Shared I/O utilities for model and calibrator loading.
"""

from pathlib import Path

import torch

from configs.config import CALIBRATOR_NAME, MODEL_CONFIG_NAME, MODEL_WEIGHTS_NAME
from evaluation.calibration import TemperatureScaling
from models.cnn_model import build_model


def load_model_and_calibrator(
    device: torch.device,
    save_dir: str | Path,
) -> tuple[torch.nn.Module, str, TemperatureScaling | None]:
    """
    Load trained classifier weights and optional temperature-scaling calibrator.

    Args:
        device: Torch device for loaded tensors.
        save_dir: Directory containing checkpoint and config files.

    Returns:
        Tuple of (model, model_type, calibrator or None).
    """
    save_path = Path(save_dir)
    config_path = save_path / MODEL_CONFIG_NAME
    model_type = "resnet18"

    if config_path.exists():
        with open(config_path, encoding="utf-8") as handle:
            for line in handle:
                if "model_type=" in line:
                    model_type = line.strip().split("=", 1)[1].strip()
                    break

    ckpt = torch.load(save_path / MODEL_WEIGHTS_NAME, map_location=device)
    if isinstance(ckpt, dict) and "model_type" in ckpt:
        model_type = ckpt["model_type"]

    model = build_model(model_type=model_type, pretrained=False, num_classes=1)
    state = (
        ckpt["model_state_dict"]
        if isinstance(ckpt, dict) and "model_state_dict" in ckpt
        else ckpt
    )
    model.load_state_dict(state, strict=True)
    model = model.to(device)
    model.eval()

    calibrator = None
    cal_path = save_path / CALIBRATOR_NAME
    if cal_path.exists():
        cal_ckpt = torch.load(cal_path, map_location=device)
        calibrator = TemperatureScaling()
        if "temperature" in cal_ckpt:
            calibrator.load_state_dict(cal_ckpt["temperature"], strict=True)
        calibrator = calibrator.to(device)

    return model, model_type, calibrator


def load_aux_model(
    device: torch.device,
    save_dir: Path,
    model_type: str,
) -> torch.nn.Module | None:
    """Load an auxiliary ensemble model checkpoint, if present."""
    ckpt_path = save_dir / MODEL_WEIGHTS_NAME
    if not ckpt_path.exists():
        return None

    ckpt = torch.load(ckpt_path, map_location=device)
    model = build_model(model_type=model_type, pretrained=False, num_classes=1)
    state = (
        ckpt["model_state_dict"]
        if isinstance(ckpt, dict) and "model_state_dict" in ckpt
        else ckpt
    )
    model.load_state_dict(state, strict=True)
    model = model.to(device)
    model.eval()
    return model
