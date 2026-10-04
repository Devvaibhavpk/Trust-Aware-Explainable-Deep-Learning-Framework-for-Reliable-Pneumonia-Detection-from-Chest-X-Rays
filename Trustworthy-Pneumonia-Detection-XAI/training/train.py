"""
Training script for chest X-ray binary classification.

Trains CNN (custom / ResNet18 / VGG16 / DenseNet121 / EfficientNet-B0),
saves best weights, and plots loss and accuracy curves.
"""

import argparse
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import (
    BATCH_SIZE,
    DATA_DIR,
    IMAGE_SIZE,
    LEARNING_RATE,
    MODEL_CONFIG_NAME,
    MODEL_SAVE_DIR,
    MODEL_TYPE,
    MODEL_WEIGHTS_NAME,
    NUM_EPOCHS,
    NUM_WORKERS,
    OUTPUT_DIR,
    ensure_dirs,
)
from datasets.preprocessing import get_dataloaders
from models.cnn_model import build_model
from training.trainer import evaluate_epoch, train_one_epoch
from utils.seed import set_seed

matplotlib.use("Agg")


def main() -> None:
    """Train a chest X-ray classifier and save the best checkpoint."""
    parser = argparse.ArgumentParser(description="Train chest X-ray pneumonia classifier")
    parser.add_argument("--data_dir", type=str, default=str(DATA_DIR))
    parser.add_argument(
        "--model_type",
        type=str,
        default=MODEL_TYPE,
        choices=["custom", "resnet18", "vgg16", "densenet121", "efficientnet_b0"],
    )
    parser.add_argument("--epochs", type=int, default=NUM_EPOCHS)
    parser.add_argument("--batch_size", type=int, default=BATCH_SIZE)
    parser.add_argument("--lr", type=float, default=LEARNING_RATE)
    parser.add_argument("--save_dir", type=str, default=str(MODEL_SAVE_DIR))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--max_samples",
        type=int,
        default=None,
        help="Cap images per split for a quick demo (leave unset for the full dataset).",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Faculty-demo preset: 2 epochs and 128 images per split.",
    )
    args = parser.parse_args()

    if args.quick:
        if args.epochs == NUM_EPOCHS:
            args.epochs = 2
        if args.max_samples is None:
            args.max_samples = 128

    set_seed(args.seed)

    ensure_dirs()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    train_loader, val_loader, _ = get_dataloaders(
        data_dir=args.data_dir,
        image_size=IMAGE_SIZE,
        batch_size=args.batch_size,
        num_workers=NUM_WORKERS,
        pin_memory=(device.type == "cuda"),
        max_samples=args.max_samples,
        seed=args.seed,
    )

    if len(train_loader.dataset) == 0:
        print("No training data found. Place data in data/train/NORMAL and data/train/PNEUMONIA")
        return

    if len(val_loader.dataset) == 0:
        print("Warning: no validation images found. The best checkpoint will use training accuracy.")

    model = build_model(model_type=args.model_type, pretrained=True, num_classes=1)
    model = model.to(device)
    print("Model running on:", next(model.parameters()).device)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    best_val_acc = 0.0
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    save_dir_path = Path(args.save_dir)
    save_dir_path.mkdir(parents=True, exist_ok=True)

    for epoch in range(1, args.epochs + 1):
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate_epoch(model, val_loader, criterion, device)

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)

        print(
            f"Epoch {epoch}/{args.epochs} | "
            f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f} | "
            f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}"
        )

        if val_acc > best_val_acc or (len(val_loader.dataset) == 0 and train_acc > best_val_acc):
            best_val_acc = val_acc if len(val_loader.dataset) > 0 else train_acc
            save_path = save_dir_path / MODEL_WEIGHTS_NAME
            torch.save(
                {"model_state_dict": model.state_dict(), "model_type": args.model_type},
                save_path,
            )
            print(f"  -> Saved best model to {save_path}")

    config_path = save_dir_path / MODEL_CONFIG_NAME
    with open(config_path, "w", encoding="utf-8") as handle:
        handle.write(f"model_type={args.model_type}\n")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(history["train_loss"], label="Train Loss")
    ax1.plot(history["val_loss"], label="Val Loss")
    ax1.set_title("Loss")
    ax1.set_xlabel("Epoch")
    ax1.legend()

    ax2.plot(history["train_acc"], label="Train Acc")
    ax2.plot(history["val_acc"], label="Val Acc")
    ax2.set_title("Accuracy")
    ax2.set_xlabel("Epoch")
    ax2.legend()

    plt.tight_layout()
    plot_path = OUTPUT_DIR / "training_curves.png"
    plt.savefig(plot_path, dpi=150)
    plt.close()

    print(f"Training curves saved to {plot_path}")


if __name__ == "__main__":
    main()
