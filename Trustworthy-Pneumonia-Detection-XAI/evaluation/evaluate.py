"""
Full evaluation: classification metrics, calibration (ECE), and trust-aware analysis.
"""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import (
    BATCH_SIZE,
    DATA_DIR,
    IMAGE_SIZE,
    MODEL_SAVE_DIR,
    NUM_WORKERS,
    OUTPUT_DIR,
    ensure_dirs,
)
from datasets.dataset import CLASS_NAMES
from datasets.preprocessing import get_dataloaders
from evaluation.confusion_matrix import plot_confusion_matrix
from evaluation.metrics import compute_classification_metrics, compute_confusion_matrix
from evaluation.reliability import compute_ece, reliability_diagram
from explainability.attention_maps import (
    LungSegmenter,
    focus_overlap_score,
    tensor_mask_to_numpy,
)
from explainability.gradcam import GradCAM
from explainability.trustscore import TrustEngine
from explainability.uncertainty import predict_with_uncertainty
from models.cnn_model import get_last_conv_layer_for_model
from models.ensemble import agreement_from_probabilities
from utils.helpers import configure_matplotlib_backend, show_or_open_figure
from utils.io import load_model_and_calibrator

configure_matplotlib_backend(prefer_interactive=False)


def main() -> None:
    """Evaluate the trained model on the test set."""
    parser = argparse.ArgumentParser(description="Evaluate chest X-ray classifier")
    parser.add_argument("--data_dir", type=str, default=str(DATA_DIR))
    parser.add_argument("--save_dir", type=str, default=str(MODEL_SAVE_DIR))
    parser.add_argument("--n_bins", type=int, default=10)
    parser.add_argument(
        "--trust_eval",
        action="store_true",
        help="Compute research-grade trust metrics (MC Dropout, Grad-CAM × lungs, TrustScore, OOD).",
    )
    parser.add_argument(
        "--n_mc_samples",
        type=int,
        default=20,
        help="MC Dropout samples per test image when --trust_eval is enabled.",
    )
    args = parser.parse_args()

    ensure_dirs()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    _, _, test_loader = get_dataloaders(
        data_dir=args.data_dir,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        pin_memory=(device.type == "cuda"),
    )
    if len(test_loader.dataset) == 0:
        print("No test data. Add data/test/NORMAL and data/test/PNEUMONIA")
        return

    model, model_type, calibrator = load_model_and_calibrator(device, args.save_dir)
    target_layer = get_last_conv_layer_for_model(model, model_type)
    gradcam = GradCAM(model, target_layer) if args.trust_eval else None

    all_preds, all_labels, all_raw_probs, all_cal_probs = [], [], [], []
    focus_scores, trust_scores, ood_flags = [], [], []

    if args.trust_eval:
        segmenter = LungSegmenter.from_checkpoint(checkpoint_path=None, device=device)
        trust_engine = TrustEngine()

    for images, labels, _ in test_loader:
        images = images.to(device)
        labels_np_batch = labels.numpy()

        with torch.no_grad():
            logits = model(images).squeeze(-1)
            raw_probs_batch = torch.sigmoid(logits).cpu().numpy()

            if calibrator is not None:
                cal_probs_batch = (
                    calibrator.calibrate_probs(logits.unsqueeze(-1).to(device))
                    .squeeze(-1)
                    .cpu()
                    .numpy()
                )
            else:
                cal_probs_batch = raw_probs_batch

        preds_batch = (raw_probs_batch >= 0.5).astype(int)

        all_preds.extend(preds_batch.tolist())
        all_labels.extend(labels_np_batch.tolist())
        all_raw_probs.extend(raw_probs_batch.tolist())
        cal_list = cal_probs_batch.tolist()
        all_cal_probs.extend(cal_list)

        if args.trust_eval:
            for i in range(images.size(0)):
                img = images[i : i + 1]
                cal_prob = float(cal_list[i])

                mc_res = predict_with_uncertainty(
                    model, img, n_samples=args.n_mc_samples, device=device
                )
                mean_pred = mc_res["mean_prediction"]
                variance = mc_res["variance"]

                pred_class = int(preds_batch[i])
                heatmap = gradcam.generate(img, target_class=pred_class)

                lung_mask_tensor = segmenter.segment(img)
                lung_mask_np = tensor_mask_to_numpy(lung_mask_tensor)
                focus = focus_overlap_score(heatmap, lung_mask_np, heatmap_threshold=0.4)

                _, agreement_score = agreement_from_probabilities([mean_pred], threshold=0.5)

                trust_summary = trust_engine.summarize(
                    calibrated_confidence=cal_prob,
                    focus_score=focus,
                    uncertainty=variance,
                    agreement_score=agreement_score,
                )

                focus_scores.append(focus)
                trust_scores.append(trust_summary["trust_score"])
                ood_flags.append(trust_summary["ood_flag"])

    y_true = np.array(all_labels)
    y_pred = np.array(all_preds)
    raw_probs = np.array(all_raw_probs)
    cal_probs = np.array(all_cal_probs)

    metrics = compute_classification_metrics(y_true, y_pred)
    cm = compute_confusion_matrix(y_true, y_pred)

    print("=" * 50)
    print("DEEP LEARNING METRICS")
    print("=" * 50)
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1-score:  {metrics['f1']:.4f}")
    print("Confusion Matrix:")
    print(cm)
    print(f"  (rows: {CLASS_NAMES}, cols: predicted)")

    ece_raw = compute_ece(raw_probs, y_true, n_bins=args.n_bins)
    ece_cal = compute_ece(cal_probs, y_true, n_bins=args.n_bins)
    print("\n" + "=" * 50)
    print("CALIBRATION")
    print("=" * 50)
    print(f"ECE (raw):   {ece_raw:.4f}")
    print(f"ECE (cal):   {ece_cal:.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    plot_confusion_matrix(cm, CLASS_NAMES, ax=axes[0])
    reliability_diagram(cal_probs, y_true, n_bins=args.n_bins, title="Test Set - Calibrated", ax=axes[1])
    plt.tight_layout()
    output_file = OUTPUT_DIR / "evaluation_results.png"
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    print(f"\nPlots saved to {output_file}")

    show_or_open_figure(output_file)
    plt.close()

    print("\n" + "=" * 50)
    print("EXPLAINABILITY (Qualitative)")
    print("=" * 50)
    print("Fidelity: Grad-CAM highlights regions that the model used for the prediction;")
    print("  check that highlighted areas align with clinical relevance (lung fields).")
    print("Stability: For similar X-rays, heatmaps should be similar; run inference on")
    print("  multiple images to assess. Human-level interpretability: heatmaps allow")
    print("  clinicians to verify whether the model 'looks at' the right anatomy.")

    if args.trust_eval and len(focus_scores) > 0:
        focus_arr = np.array(focus_scores, dtype=np.float32)
        trust_arr = np.array(trust_scores, dtype=np.float32)
        ood_arr = np.array(ood_flags, dtype=bool)

        print("\n" + "=" * 50)
        print("TRUST METRICS (Research)")
        print("=" * 50)
        print(
            f"FocusScore: mean={focus_arr.mean():.4f}, std={focus_arr.std():.4f}, "
            f"min={focus_arr.min():.4f}, max={focus_arr.max():.4f}"
        )
        print(
            f"TrustScore: mean={trust_arr.mean():.4f}, std={trust_arr.std():.4f}, "
            f"min={trust_arr.min():.4f}, max={trust_arr.max():.4f}"
        )

        y_correct = y_true == y_pred
        ood_pred = ood_arr

        tp = int((~y_correct & ood_pred).sum())
        fp = int((y_correct & ood_pred).sum())
        tn = int((y_correct & ~ood_pred).sum())
        fn = int(((~y_correct) & ~ood_pred).sum())

        total = tp + fp + tn + fn
        if total > 0:
            ood_acc = (tp + tn) / total
            print(f"OOD detection accuracy (vs correctness proxy): {ood_acc:.4f}")
            print(f"  TP={tp}, FP={fp}, TN={tn}, FN={fn}")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(trust_arr, bins=20, range=(0, 1), color="#34495e", edgecolor="white", alpha=0.9)
        ax.set_xlabel("TrustScore")
        ax.set_ylabel("Count")
        ax.set_title("TrustScore Distribution (Test Set)")
        plt.tight_layout()
        trust_hist_path = OUTPUT_DIR / "trustscore_distribution.png"
        plt.savefig(trust_hist_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"TrustScore distribution saved to {trust_hist_path}")


if __name__ == "__main__":
    main()
