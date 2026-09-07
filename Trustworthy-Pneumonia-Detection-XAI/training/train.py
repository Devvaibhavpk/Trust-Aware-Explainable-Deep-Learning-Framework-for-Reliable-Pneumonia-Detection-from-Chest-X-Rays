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
    args = parser.parse_args()

    ensure_dirs()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    train_loader, val_loader, _ = get_dataloaders(
        data_dir=args.data_dir,
        image_size=IMAGE_SIZE,
        batch_size=args.batch_size,
        num_workers=NUM_WORKERS,
        pin_memory=(device.type == "cuda"),
    )

    if len(train_loader.dataset) == 0:
        print("No training data found. Place data in data/train/NORMAL and data/train/PNEUMONIA")
        return

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

        if val_acc > best_val_acc:
            best_val_acc = val_acc
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
