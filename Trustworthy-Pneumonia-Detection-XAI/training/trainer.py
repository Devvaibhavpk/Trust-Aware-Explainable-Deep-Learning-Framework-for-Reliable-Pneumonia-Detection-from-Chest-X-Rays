"""
Training loop utilities for chest X-ray classification.
"""

import torch
import torch.nn as nn


def train_one_epoch(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> tuple[float, float]:
    """Run one training epoch and return average loss and accuracy."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    if len(loader) == 0:
        return 0.0, 0.0

    for images, labels, _ in loader:
        images = images.to(device)
        labels = labels.to(device).float().unsqueeze(1)

        optimizer.zero_grad()
        logits = model(images)

        if logits.size(-1) == 1:
            logits = logits.squeeze(-1)

        loss = criterion(logits, labels.squeeze(-1))
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        probs = torch.sigmoid(logits).detach()
        preds = (probs >= 0.5).long().squeeze()

        total += labels.size(0)
        correct += (preds == labels.squeeze().long()).sum().item()

    return running_loss / len(loader), correct / total


@torch.no_grad()
def evaluate_epoch(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> tuple[float, float]:
    """Run validation/test evaluation and return average loss and accuracy."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    if len(loader) == 0:
        return 0.0, 0.0

    for images, labels, _ in loader:
        images = images.to(device)
        labels = labels.to(device).float().unsqueeze(1)

        logits = model(images)

        if logits.size(-1) == 1:
            logits = logits.squeeze(-1)

        loss = criterion(logits, labels.squeeze(-1))
        running_loss += loss.item()

        probs = torch.sigmoid(logits)
        preds = (probs >= 0.5).long().squeeze()

        total += labels.size(0)
        correct += (preds == labels.squeeze().long()).sum().item()

    return running_loss / len(loader), correct / total
