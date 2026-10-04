"""
Calibration script: fit Temperature Scaling on validation set (post-hoc).
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
    CALIBRATOR_NAME,
    DATA_DIR,
    IMAGE_SIZE,
    MODEL_SAVE_DIR,
    NUM_WORKERS,
    OUTPUT_DIR,
    ensure_dirs,
)
from datasets.preprocessing import get_dataloaders
from evaluation.calibration import fit_temperature
from evaluation.reliability import compute_ece, reliability_diagram
from utils.helpers import configure_matplotlib_backend, show_or_open_figure
from utils.io import load_model_and_calibrator

configure_matplotlib_backend(prefer_interactive=False)


def collect_logits_and_labels(
    model: torch.nn.Module,
    loader: torch.utils.data.DataLoader,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Collect model logits and labels from a DataLoader."""
    logits_list, labels_list = [], []
    with torch.no_grad():
        for images, labels, _ in loader:
            images = images.to(device)
            out = model(images)
            logits_list.append(out.squeeze(-1).cpu() if out.size(-1) == 1 else out.cpu())
            labels_list.append(labels.cpu())
    return torch.cat(logits_list, dim=0), torch.cat(labels_list, dim=0)


def main() -> None:
    """Fit temperature scaling on the validation set and save reliability diagrams."""
    parser = argparse.ArgumentParser(description="Calibrate model confidence with temperature scaling")
    parser.add_argument("--data_dir", type=str, default=str(DATA_DIR))
    parser.add_argument("--save_dir", type=str, default=str(MODEL_SAVE_DIR))
    parser.add_argument("--n_bins", type=int, default=10)
    args = parser.parse_args()

    ensure_dirs()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    _, val_loader, _ = get_dataloaders(
        data_dir=args.data_dir,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        pin_memory=(device.type == "cuda"),
    )
    if len(val_loader.dataset) == 0:
        print("No validation data. Run with data/val/NORMAL and data/val/PNEUMONIA")
        return

    model, _, _ = load_model_and_calibrator(device, args.save_dir)
    logits, labels = collect_logits_and_labels(model, val_loader, device)
    labels_np = labels.numpy()
    uncal_probs = torch.sigmoid(logits).numpy().flatten()

    temperature = fit_temperature(model, val_loader, device, use_sigmoid=True)
    print(f"Fitted temperature T = {temperature.T:.4f}")

    logits_batch = logits.unsqueeze(-1).to(device)
    cal_probs = temperature.calibrate_probs(logits_batch).squeeze(-1).detach().cpu().numpy()
    cal_probs = cal_probs.flatten()

    ece_uncal = compute_ece(uncal_probs, labels_np, n_bins=args.n_bins)
    ece_cal = compute_ece(cal_probs, labels_np, n_bins=args.n_bins)
    print(f"ECE (uncalibrated) = {ece_uncal:.4f}")
    print(f"ECE (calibrated)   = {ece_cal:.4f}")

    cal_path = Path(args.save_dir) / CALIBRATOR_NAME
    torch.save({"temperature": temperature.state_dict(), "T": temperature.T}, cal_path)
    print(f"Calibrator saved to {cal_path}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    reliability_diagram(uncal_probs, labels_np, n_bins=args.n_bins, title="Uncalibrated", ax=ax1)
    reliability_diagram(
        cal_probs,
        labels_np,
        n_bins=args.n_bins,
        title="Calibrated (Temperature Scaling)",
        ax=ax2,
    )
    plt.tight_layout()
    out_path = OUTPUT_DIR / "reliability_diagrams.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Reliability diagrams saved to {out_path}")

    show_or_open_figure(out_path)
    plt.close()

    print("\n--- Why calibration improves reliability but not accuracy ---")
    print("Accuracy depends only on the predicted class, unchanged by temperature scaling.")
    print("Calibration adjusts probability values so confidence matches empirical frequency.")
    print("So ECE decreases while accuracy stays the same.")


if __name__ == "__main__":
    main()
