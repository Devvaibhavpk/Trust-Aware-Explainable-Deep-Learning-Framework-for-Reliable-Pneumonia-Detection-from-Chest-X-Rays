"""
Faculty figure pack: classification, calibration, explainability, and trust plots.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
from sklearn.metrics import (
    average_precision_score,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import (
    BATCH_SIZE,
    DATA_DIR,
    HEATMAP_THRESHOLD,
    IMAGE_SIZE,
    MODEL_SAVE_DIR,
    NUM_WORKERS,
    OUTPUT_DIR,
    ensure_dirs,
)
from datasets.dataset import CLASS_NAMES
from datasets.preprocessing import get_dataloaders
from datasets.transforms import IMAGENET_MEAN, IMAGENET_STD
from evaluation.confusion_matrix import plot_confusion_matrix
from evaluation.metrics import compute_classification_metrics, compute_confusion_matrix
from evaluation.reliability import compute_ece, reliability_diagram
from explainability.attention_maps import (
    LungSegmenter,
    focus_overlap_score,
    tensor_mask_to_numpy,
)
from explainability.gradcam import GradCAM, overlay_heatmap
from explainability.trustscore import TrustEngine, get_trust_level
from explainability.uncertainty import predict_with_uncertainty
from models.cnn_model import get_last_conv_layer_for_model
from models.ensemble import agreement_from_probabilities
from utils.io import load_model_and_calibrator

sns.set_theme(style="whitegrid", context="talk")
PALETTE = {
    "normal": "#4C78A8",
    "pneumonia": "#E45756",
    "accent": "#54A24B",
    "trust": "#F58518",
}


def _save(fig: plt.Figure, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"saved {path}")
    return path


def _denormalize(image: torch.Tensor) -> np.ndarray:
    mean = torch.tensor(IMAGENET_MEAN, device=image.device).view(3, 1, 1)
    std = torch.tensor(IMAGENET_STD, device=image.device).view(3, 1, 1)
    rgb = (image * std + mean).clamp(0, 1).detach().cpu().numpy().transpose(1, 2, 0)
    return (rgb * 255).astype(np.uint8)


def collect_predictions(model, calibrator, loader, device) -> dict:
    labels, raw_probs, cal_probs, images, paths = [], [], [], [], []
    model.eval()
    with torch.no_grad():
        for batch in loader:
            imgs, y, img_paths = batch
            imgs = imgs.to(device)
            logits = model(imgs).squeeze(-1)
            raw = torch.sigmoid(logits).cpu().numpy()
            if calibrator is not None:
                cal = (
                    calibrator.calibrate_probs(logits.unsqueeze(-1))
                    .squeeze(-1)
                    .cpu()
                    .numpy()
                )
            else:
                cal = raw
            labels.extend(y.numpy().tolist())
            raw_probs.extend(np.atleast_1d(raw).tolist())
            cal_probs.extend(np.atleast_1d(cal).tolist())
            for i in range(imgs.size(0)):
                images.append(imgs[i].cpu())
                paths.append(img_paths[i])
    y_true = np.array(labels)
    raw_arr = np.array(raw_probs)
    cal_arr = np.array(cal_probs)
    y_pred = (raw_arr >= 0.5).astype(int)
    return {
        "y_true": y_true,
        "y_pred": y_pred,
        "raw": raw_arr,
        "cal": cal_arr,
        "images": images,
        "paths": paths,
    }


def collect_trust(model, model_type, preds: dict, device, n_trust: int, n_mc: int) -> dict:
    n = min(n_trust, len(preds["y_true"]))
    target_layer = get_last_conv_layer_for_model(model, model_type)
    gradcam = GradCAM(model, target_layer)
    segmenter = LungSegmenter.from_checkpoint(checkpoint_path=None, device=device)
    engine = TrustEngine()

    focus, trust, levels, uncert, ood = [], [], [], [], []
    for i in range(n):
        img = preds["images"][i].unsqueeze(0).to(device)
        cal = float(preds["cal"][i])
        mc = predict_with_uncertainty(model, img, n_samples=n_mc, device=device)
        heatmap = gradcam.generate(img, target_class=int(preds["y_pred"][i]))
        mask = tensor_mask_to_numpy(segmenter.segment(img))
        focus_i = focus_overlap_score(heatmap, mask, heatmap_threshold=HEATMAP_THRESHOLD)
        _, agree = agreement_from_probabilities([mc["mean_prediction"]])
        summary = engine.summarize(cal, focus_i, mc["variance"], agree)
        level = get_trust_level(summary["trust_score"], cal, focus_i, mc["variance"])
        focus.append(focus_i)
        trust.append(summary["trust_score"])
        levels.append(level.capitalize())
        uncert.append(mc["variance"])
        ood.append(summary["ood_flag"])
    return {
        "focus": np.array(focus),
        "trust": np.array(trust),
        "levels": levels,
        "uncertainty": np.array(uncert),
        "ood": np.array(ood),
        "n": n,
    }


def plot_pack(preds: dict, trust: dict, model, model_type, device, out_dir: Path, n_gradcam: int) -> list[Path]:
    saved: list[Path] = []
    y_true, y_pred, raw, cal = preds["y_true"], preds["y_pred"], preds["raw"], preds["cal"]
    metrics = compute_classification_metrics(y_true, y_pred)
    cm = compute_confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=(6.2, 5.4))
    plot_confusion_matrix(cm, CLASS_NAMES, ax=ax, title="Confusion Matrix (Test Sample)")
    saved.append(_save(fig, out_dir / "01_confusion_matrix.png"))

    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    names = ["Accuracy", "Precision", "Recall", "F1-score"]
    values = [metrics["accuracy"], metrics["precision"], metrics["recall"], metrics["f1"]]
    bars = ax.bar(names, values, color=["#4C78A8", "#72B7B2", "#54A24B", "#E45756"])
    ax.set_ylim(0, 1.05)
    ax.set_title("Classification Metrics")
    ax.set_ylabel("Score")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.02, f"{value:.3f}", ha="center", fontsize=12)
    saved.append(_save(fig, out_dir / "02_classification_metrics.png"))

    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    if len(np.unique(y_true)) == 2:
        fpr, tpr, _ = roc_curve(y_true, cal)
        auc = roc_auc_score(y_true, cal)
        ax.plot(fpr, tpr, color=PALETTE["pneumonia"], linewidth=2.5, label=f"AUC = {auc:.3f}")
        ax.plot([0, 1], [0, 1], "k--", linewidth=1)
        ax.legend(loc="lower right")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    saved.append(_save(fig, out_dir / "03_roc_curve.png"))

    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    if len(np.unique(y_true)) == 2:
        prec, rec, _ = precision_recall_curve(y_true, cal)
        ap = average_precision_score(y_true, cal)
        ax.plot(rec, prec, color=PALETTE["normal"], linewidth=2.5, label=f"AP = {ap:.3f}")
        ax.legend(loc="lower left")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision–Recall Curve")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    saved.append(_save(fig, out_dir / "04_precision_recall.png"))

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6))
    reliability_diagram(raw, y_true, n_bins=10, title="Uncalibrated", ax=axes[0])
    reliability_diagram(cal, y_true, n_bins=10, title="Temperature Scaled", ax=axes[1])
    fig.suptitle("Reliability Diagrams", y=1.02)
    saved.append(_save(fig, out_dir / "05_reliability_diagrams.png"))

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    ece_raw = compute_ece(raw, y_true)
    ece_cal = compute_ece(cal, y_true)
    bars = ax.bar(["Raw ECE", "Calibrated ECE"], [ece_raw, ece_cal], color=["#E45756", "#54A24B"])
    ax.set_ylabel("Expected Calibration Error (lower is better)")
    ax.set_title("Calibration Improves Confidence Honesty")
    for bar, value in zip(bars, [ece_raw, ece_cal]):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.002, f"{value:.4f}", ha="center")
    saved.append(_save(fig, out_dir / "06_ece_comparison.png"))

    fig, ax = plt.subplots(figsize=(8.2, 5.4))
    ax.hist(raw, bins=20, range=(0, 1), alpha=0.55, label="Raw confidence", color=PALETTE["pneumonia"])
    ax.hist(cal, bins=20, range=(0, 1), alpha=0.55, label="Calibrated confidence", color=PALETTE["normal"])
    ax.set_xlabel("P(Pneumonia)")
    ax.set_ylabel("Count")
    ax.set_title("Confidence Distribution Before vs After Calibration")
    ax.legend()
    saved.append(_save(fig, out_dir / "07_confidence_histograms.png"))

    fig, ax = plt.subplots(figsize=(8.0, 5.4))
    ax.hist(trust["trust"], bins=16, range=(0, 1), color="#4C78A8", edgecolor="white")
    ax.set_xlabel("TrustScore")
    ax.set_ylabel("Count")
    ax.set_title(f"TrustScore Distribution (n={trust['n']})")
    saved.append(_save(fig, out_dir / "08_trustscore_distribution.png"))

    fig, ax = plt.subplots(figsize=(6.8, 5.4))
    order = ["High", "Medium", "Low"]
    counts = [trust["levels"].count(name) for name in order]
    ax.bar(order, counts, color=["#54A24B", "#F58518", "#E45756"])
    ax.set_ylabel("Images")
    ax.set_title("Trust Levels on the Sampled Test Images")
    saved.append(_save(fig, out_dir / "09_trust_levels.png"))

    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    correct = (y_true[: trust["n"]] == y_pred[: trust["n"]])
    ax.scatter(
        preds["cal"][: trust["n"]][correct],
        trust["uncertainty"][correct],
        c="#54A24B",
        alpha=0.75,
        label="Correct",
    )
    ax.scatter(
        preds["cal"][: trust["n"]][~correct],
        trust["uncertainty"][~correct],
        c="#E45756",
        alpha=0.85,
        label="Incorrect",
    )
    ax.set_xlabel("Calibrated confidence")
    ax.set_ylabel("MC Dropout variance")
    ax.set_title("Uncertainty vs Confidence")
    ax.legend()
    saved.append(_save(fig, out_dir / "10_uncertainty_vs_confidence.png"))

    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    ax.hist(trust["focus"], bins=14, range=(0, 1), color="#72B7B2", edgecolor="white")
    ax.set_xlabel("FocusScore (Grad-CAM ∩ lung prior)")
    ax.set_ylabel("Count")
    ax.set_title("Does the explanation stay on the lungs?")
    saved.append(_save(fig, out_dir / "11_focus_score.png"))

    n_show = min(n_gradcam, len(preds["images"]))
    cols = 4
    rows = int(np.ceil(n_show / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3.2, rows * 3.3))
    axes = np.atleast_2d(axes)
    target_layer = get_last_conv_layer_for_model(model, model_type)
    gradcam = GradCAM(model, target_layer)
    for idx in range(rows * cols):
        ax = axes[idx // cols][idx % cols]
        ax.axis("off")
        if idx >= n_show:
            continue
        img = preds["images"][idx].unsqueeze(0).to(device)
        heatmap = gradcam.generate(img, target_class=int(y_pred[idx]))
        overlay = overlay_heatmap(heatmap, _denormalize(preds["images"][idx]))
        ax.imshow(overlay)
        truth = CLASS_NAMES[int(y_true[idx])]
        pred = CLASS_NAMES[int(y_pred[idx])]
        ax.set_title(f"true {truth}\npred {pred}", fontsize=10)
    fig.suptitle("Grad-CAM Explanations", fontsize=16)
    saved.append(_save(fig, out_dir / "12_gradcam_gallery.png"))
    return saved


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate faculty demo figure pack")
    parser.add_argument("--data_dir", type=str, default=str(DATA_DIR))
    parser.add_argument("--save_dir", type=str, default=str(MODEL_SAVE_DIR))
    parser.add_argument("--max_samples", type=int, default=160)
    parser.add_argument("--n_trust", type=int, default=48)
    parser.add_argument("--n_mc", type=int, default=12)
    parser.add_argument("--n_gradcam", type=int, default=8)
    args = parser.parse_args()

    ensure_dirs()
    out_dir = OUTPUT_DIR / "faculty_report"
    out_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    _, _, test_loader = get_dataloaders(
        data_dir=args.data_dir,
        image_size=IMAGE_SIZE,
        batch_size=min(BATCH_SIZE, 16),
        num_workers=NUM_WORKERS,
        pin_memory=(device.type == "cuda"),
        max_samples=args.max_samples,
        seed=42,
    )
    if len(test_loader.dataset) == 0:
        print("No test images. Prepare the dataset first.")
        return

    model, model_type, calibrator = load_model_and_calibrator(device, args.save_dir)
    preds = collect_predictions(model, calibrator, test_loader, device)
    trust = collect_trust(model, model_type, preds, device, n_trust=args.n_trust, n_mc=args.n_mc)
    paths = plot_pack(preds, trust, model, model_type, device, out_dir, n_gradcam=args.n_gradcam)
    print(f"\nGenerated {len(paths)} figures in {out_dir}")


if __name__ == "__main__":
    main()
