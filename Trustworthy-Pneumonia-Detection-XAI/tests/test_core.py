"""
Unit tests for core trust, calibration, model, and dataset-split behavior.
"""

import sys
from pathlib import Path

import numpy as np
import torch.nn as nn
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_resnet_includes_dropout_for_mc_uncertainty() -> None:
    from models.cnn_model import build_model

    model = build_model(model_type="resnet18", pretrained=False, num_classes=1)
    dropouts = [module for module in model.modules() if isinstance(module, nn.Dropout)]
    assert dropouts, "ResNet18 needs dropout so Monte Carlo Dropout can produce uncertainty"


def test_vgg_gradcam_target_is_conv2d() -> None:
    from models.cnn_model import build_model, get_last_conv_layer_for_model

    model = build_model(model_type="vgg16", pretrained=False, num_classes=1)
    layer = get_last_conv_layer_for_model(model, "vgg16")
    assert isinstance(layer, nn.Conv2d)


def test_reliability_diagram_does_not_close_parent_figure() -> None:
    import matplotlib.pyplot as plt
    from evaluation.reliability import reliability_diagram

    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    probs = np.array([0.1, 0.2, 0.8, 0.9])
    labels = np.array([0, 0, 1, 1])
    reliability_diagram(probs, labels, n_bins=4, title="Calibrated", ax=axes[1])
    assert plt.fignum_exists(fig.number)
    plt.close(fig)


def test_trust_score_is_bounded() -> None:
    from explainability.trustscore import TrustEngine

    engine = TrustEngine()
    score = engine.compute_trust_score(
        calibrated_confidence=0.9,
        focus_score=0.8,
        uncertainty=0.05,
        agreement_score=1.0,
    )
    assert 0.0 <= score <= 1.0


def test_kaggle_split_has_no_train_val_overlap(tmp_path: Path) -> None:
    from datasets.split_dataset import split_kaggle_dataset

    src = tmp_path / "chest_xray"
    for split in ("train", "test"):
        for class_name in ("NORMAL", "PNEUMONIA"):
            class_dir = src / split / class_name
            class_dir.mkdir(parents=True)
            count = 10 if split == "train" else 4
            for index in range(count):
                Image.new("RGB", (8, 8), color=index).save(class_dir / f"{class_name}_{index}.jpeg")

    dest = tmp_path / "data"
    split_kaggle_dataset(src, dest, val_ratio=0.2, seed=0)

    train_names = {path.name for path in (dest / "train" / "NORMAL").iterdir()}
    val_names = {path.name for path in (dest / "val" / "NORMAL").iterdir()}
    assert train_names
    assert val_names
    assert train_names.isdisjoint(val_names)
    assert (dest / "test" / "PNEUMONIA").exists()
