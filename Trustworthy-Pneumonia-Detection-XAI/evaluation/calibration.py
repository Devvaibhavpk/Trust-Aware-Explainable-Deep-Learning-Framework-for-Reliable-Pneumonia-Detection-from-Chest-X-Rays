"""
Post-hoc probability calibration via Temperature Scaling.
"""

from typing import List

import torch
import torch.nn as nn


class TemperatureScaling(nn.Module):
    """
    Post-hoc temperature scaling for binary classification.

    For sigmoid: p_calibrated = sigmoid(logit / T).
    T is learned on the validation set to minimize NLL.
    """

    def __init__(self, initial_t: float = 1.5) -> None:
        super().__init__()
        self.temperature = nn.Parameter(torch.tensor(initial_t, dtype=torch.float32))

    def forward(self, logits: torch.Tensor) -> torch.Tensor:
        """Scale logits by temperature; output has same shape as logits."""
        return logits / torch.clamp(self.temperature, min=1e-4)

    def calibrate_logits(self, logits: torch.Tensor) -> torch.Tensor:
        """Return temperature-scaled logits."""
        return self.forward(logits)

    def calibrate_probs(self, logits: torch.Tensor) -> torch.Tensor:
        """Return calibrated probability (sigmoid(logit/T)) for binary case."""
        scaled = self.calibrate_logits(logits)
        if scaled.dim() == 1 or scaled.size(-1) == 1:
            return torch.sigmoid(scaled.squeeze(-1))
        return torch.softmax(scaled, dim=-1)

    @property
    def T(self) -> float:
        return float(torch.clamp(self.temperature, min=1e-4).detach().cpu().item())


def fit_temperature(
    model: nn.Module,
    val_loader: torch.utils.data.DataLoader,
    device: torch.device,
    lr: float = 0.01,
    max_iter: int = 50,
    use_sigmoid: bool = True,
) -> TemperatureScaling:
    """
    Fit temperature scaling on the validation set (post-hoc).

    Args:
        model: Trained classifier outputting logits of shape (batch, 1) or (batch, 2).
        val_loader: Validation DataLoader.
        device: Torch device.
        lr: LBFGS learning rate.
        max_iter: Maximum LBFGS iterations.
        use_sigmoid: True for single-logit binary classification.

    Returns:
        Fitted TemperatureScaling module.
    """
    temperature = TemperatureScaling(initial_t=1.5).to(device)
    optimizer = torch.optim.LBFGS([temperature.temperature], lr=lr, max_iter=max_iter)

    logits_list: List[torch.Tensor] = []
    labels_list: List[torch.Tensor] = []
    model.eval()
    with torch.no_grad():
        for batch in val_loader:
            images = batch[0].to(device)
            labels = batch[1].to(device)
            out = model(images)
            logits_list.append(out.detach())
            labels_list.append(labels.detach())

    all_logits = torch.cat(logits_list, dim=0)
    all_labels = torch.cat(labels_list, dim=0)

    def eval_loss() -> torch.Tensor:
        optimizer.zero_grad()
        scaled = temperature(all_logits)
        if use_sigmoid and (scaled.size(-1) == 1 or all_logits.size(-1) == 1):
            probs = torch.sigmoid(scaled.squeeze(-1))
            loss = nn.functional.binary_cross_entropy(probs.float(), all_labels.float())
        else:
            probs = torch.softmax(scaled, dim=-1)
            loss = nn.functional.cross_entropy(probs, all_labels.long())
        loss.backward()
        return loss

    optimizer.step(eval_loss)
    return temperature
