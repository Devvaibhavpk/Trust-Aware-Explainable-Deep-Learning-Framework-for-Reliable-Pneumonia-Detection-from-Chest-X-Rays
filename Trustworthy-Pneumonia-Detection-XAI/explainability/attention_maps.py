"""
Lung segmentation and Grad-CAM explanation validation.

This module provides:
  - LungSegmenter: wraps a (pretrained) U-Net–style model for binary lung masks
  - focus_overlap_score: quantitative Grad-CAM × lung-overlap FocusScore

Design goals:
  - Optional: if no pretrained weights are provided, falls back to a
    geometric lung prior (central region mask) so the pipeline still runs.
  - GPU-friendly: all heavy computation is in PyTorch; only the final
    FocusScore uses NumPy for convenience.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleUNet(nn.Module):
    """
    Lightweight U-Net–like architecture for 224×224 inputs.

    This is provided so users can easily plug in pretrained lung
    segmentation weights (e.g. trained on JSRT/Montgomery or NIH CXR).
    The exact architecture is not critical for the trust pipeline as
    long as the forward signature matches:
        input:  (N, 1 or 3, H, W)
        output: (N, 1, H, W) logits
    """

    def __init__(self, in_channels: int = 1, base_channels: int = 32):
        super().__init__()
        self.enc1 = self._block(in_channels, base_channels)
        self.enc2 = self._block(base_channels, base_channels * 2)
        self.enc3 = self._block(base_channels * 2, base_channels * 4)

        self.pool = nn.MaxPool2d(2)

        self.bottleneck = self._block(base_channels * 4, base_channels * 8)

        self.up3 = nn.ConvTranspose2d(base_channels * 8, base_channels * 4, 2, stride=2)
        self.dec3 = self._block(base_channels * 8, base_channels * 4)
        self.up2 = nn.ConvTranspose2d(base_channels * 4, base_channels * 2, 2, stride=2)
        self.dec2 = self._block(base_channels * 4, base_channels * 2)
        self.up1 = nn.ConvTranspose2d(base_channels * 2, base_channels, 2, stride=2)
        self.dec1 = self._block(base_channels * 2, base_channels)

        self.out_conv = nn.Conv2d(base_channels, 1, kernel_size=1)

    @staticmethod
    def _block(in_ch: int, out_ch: int) -> nn.Sequential:
        return nn.Sequential(
            nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))

        b = self.bottleneck(self.pool(e3))

        d3 = self.up3(b)
        d3 = torch.cat([d3, e3], dim=1)
        d3 = self.dec3(d3)

        d2 = self.up2(d3)
        d2 = torch.cat([d2, e2], dim=1)
        d2 = self.dec2(d2)

        d1 = self.up1(d2)
        d1 = torch.cat([d1, e1], dim=1)
        d1 = self.dec1(d1)

        return self.out_conv(d1)


@dataclass
class LungSegmenter:
    """
    Wrapper around a lung segmentation model.

    Usage
    -----
    segmenter = LungSegmenter.from_checkpoint("lung_unet.pt", device)
    lung_mask = segmenter.segment(image_tensor)  # (1, H, W) float in {0,1}

    If no checkpoint is provided or loading fails, a geometric fallback mask
    (central lung prior) is used to keep the pipeline robust.
    """

    model: Optional[nn.Module]
    device: torch.device
    threshold: float = 0.5

    @classmethod
    def from_checkpoint(
        cls,
        checkpoint_path: Optional[str] = None,
        device: Optional[torch.device] = None,
        in_channels: int = 1,
    ) -> "LungSegmenter":
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model: Optional[nn.Module] = None
        if checkpoint_path is not None:
            ckpt_path = Path(checkpoint_path)
            if ckpt_path.exists():
                model = SimpleUNet(in_channels=in_channels)
                state = torch.load(ckpt_path, map_location=device)
                # Allow either raw state_dict or dict wrapper
                if isinstance(state, dict) and "model_state_dict" in state:
                    state = state["model_state_dict"]
                model.load_state_dict(state, strict=True)
                model.to(device)
                model.eval()

        return cls(model=model, device=device)

    def _geometric_prior_mask(self, h: int, w: int) -> torch.Tensor:
        """
        Fallback: central lung prior.
        Approximates the lung fields by a central rectangular region.
        """
        y = torch.linspace(0.0, 1.0, steps=h, device=self.device)
        x = torch.linspace(0.0, 1.0, steps=w, device=self.device)
        # Lungs occupy roughly central 70–80 % horizontally and 50–80 % vertically.
        y_low, y_high = 0.15, 0.90
        x_low, x_high = 0.10, 0.90
        yy = (y >= y_low) & (y <= y_high)
        xx = (x >= x_low) & (x <= x_high)
        mask = torch.outer(yy.float(), xx.float())
        return mask.unsqueeze(0)  # (1, H, W)

    @torch.no_grad()
    def segment(self, image_tensor: torch.Tensor) -> torch.Tensor:
        """
        Produce a binary lung mask for a single image.

        Parameters
        ----------
        image_tensor : (1, C, H, W) or (C, H, W), already on the correct device.

        Returns
        -------
        mask : torch.Tensor of shape (1, H, W) with values in {0, 1}.
        """
        if image_tensor.dim() == 3:
            image_tensor = image_tensor.unsqueeze(0)

        _, _, h, w = image_tensor.shape

        if self.model is None:
            return self._geometric_prior_mask(h, w)

        x = image_tensor.to(self.device)
        # If model expects single-channel input, convert RGB to grayscale
        if x.size(1) == 3 and isinstance(self.model, SimpleUNet) and self.model.enc1[0].in_channels == 1:
            x = x.mean(dim=1, keepdim=True)

        logits = self.model(x)
        probs = torch.sigmoid(logits)
        mask = (probs >= self.threshold).float()

        # Ensure shape (1, H, W)
        return mask.squeeze(0)


def focus_overlap_score(
    heatmap: np.ndarray,
    lung_mask: np.ndarray,
    heatmap_threshold: float = 0.4,
) -> float:
    """
    Compute Grad-CAM × lung overlap FocusScore.

    FocusScore = Area(GradCAM ∩ LungRegion) / Area(GradCAM)

    Parameters
    ----------
    heatmap : np.ndarray
        Grad-CAM heatmap (H, W) in [0, 1].
    lung_mask : np.ndarray
        Binary lung mask (H, W) in {0, 1}.
    heatmap_threshold : float
        Threshold to binarise Grad-CAM importance (default: 0.4).
    """
    if heatmap.ndim != 2:
        raise ValueError("heatmap must be 2D (H, W)")
    if lung_mask.ndim != 2:
        raise ValueError("lung_mask must be 2D (H, W)")

    hm_binary = (heatmap >= heatmap_threshold).astype(np.float32)
    if hm_binary.sum() == 0.0:
        return 0.0

    lung_binary = (lung_mask > 0.5).astype(np.float32)
    overlap = (hm_binary * lung_binary).sum()
    focus = float(overlap / hm_binary.sum())
    return float(np.clip(focus, 0.0, 1.0))


def tensor_mask_to_numpy(mask: torch.Tensor) -> np.ndarray:
    """
    Utility: convert (1, H, W) or (H, W) torch mask to numpy (H, W).
    """
    if mask.dim() == 3:
        mask = mask.squeeze(0)
    return mask.detach().cpu().numpy().astype(np.float32)

