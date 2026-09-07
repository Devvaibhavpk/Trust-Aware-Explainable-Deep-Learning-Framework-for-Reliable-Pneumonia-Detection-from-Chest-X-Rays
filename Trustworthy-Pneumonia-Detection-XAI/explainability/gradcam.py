"""
Grad-CAM: Gradient-weighted Class Activation Mapping for explaining CNN predictions.
Uses the last convolutional layer to produce class-specific heatmaps.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Optional, Tuple
import cv2


class GradCAM:
    """
    Grad-CAM for a given model and target layer.
    Registers forward hook to capture activations and backward hook for gradients.
    """

    def __init__(self, model: nn.Module, target_layer: nn.Module):
        self.model = model
        self.target_layer = target_layer
        self.activations: Optional[torch.Tensor] = None
        self.gradients: Optional[torch.Tensor] = None
        self._hooks = []

    def _save_activation(self, module: nn.Module, input: torch.Tensor, output: torch.Tensor) -> None:
        self.activations = output.detach()

    def _save_gradient(self, module: nn.Module, grad_input: torch.Tensor, grad_output: torch.Tensor) -> None:
        self.gradients = grad_output[0].detach()

    def _register_hooks(self) -> None:
        self._hooks.append(self.target_layer.register_forward_hook(self._save_activation))
        self._hooks.append(self.target_layer.register_full_backward_hook(self._save_gradient))

    def _remove_hooks(self) -> None:
        for h in self._hooks:
            h.remove()
        self._hooks = []

    def generate(
        self,
        input_tensor: torch.Tensor,
        target_class: Optional[int] = None,
        use_softmax: bool = False,
    ) -> np.ndarray:
        """
        Generate Grad-CAM heatmap for the given input.
        input_tensor: (1, C, H, W); must be on the same device as the model (caller's responsibility).
        target_class: for binary with sigmoid, 1 = pneumonia (positive). If None, use predicted class.
        use_softmax: if model has 2 outputs and uses softmax, set True.
        Returns heatmap (H', W') in range [0, 1] (spatial size of the target layer).
        """
        self.model.eval()
        self._register_hooks()
        self.activations = None
        self.gradients = None

        output = self.model(input_tensor)
        if target_class is None:
            if output.size(-1) == 1:
                target_class = 1 if output.item() >= 0.5 else 0
            else:
                target_class = output.argmax(dim=-1).item()

        if output.size(-1) == 1:
            # Binary sigmoid: gradient w.r.t. the single logit (positive class)
            self.model.zero_grad()
            if target_class == 1:
                output.sum().backward()
            else:
                (-output).sum().backward()
        else:
            self.model.zero_grad()
            one_hot = torch.zeros_like(output)
            one_hot[0, target_class] = 1
            (output * one_hot).sum().backward()

        self._remove_hooks()
        if self.activations is None or self.gradients is None:
            raise RuntimeError("Grad-CAM: activations or gradients not captured")

        # weights: mean of gradients over spatial dims (channel-wise importance)
        weights = self.gradients.mean(dim=(2, 3))
        # cam: weighted sum of activation maps
        cam = (weights.unsqueeze(-1).unsqueeze(-1) * self.activations).sum(dim=1, keepdim=True)
        cam = F.relu(cam)
        cam = cam.squeeze().cpu().numpy()
        # resize to input spatial size and normalize to [0, 1]
        cam = cv2.resize(cam, (input_tensor.size(3), input_tensor.size(2)))
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        return cam.astype(np.float32)


def generate_gradcam_heatmap(
    model: nn.Module,
    target_layer: nn.Module,
    input_tensor: torch.Tensor,
    target_class: Optional[int] = None,
    device: torch.device = torch.device("cpu"),
) -> np.ndarray:
    """
    Reusable function: generate Grad-CAM heatmap.
    input_tensor: (1, C, H, W).
    """
    gradcam = GradCAM(model, target_layer)
    return gradcam.generate(input_tensor.to(device), target_class=target_class)


def overlay_heatmap(
    heatmap: np.ndarray,
    original_image: np.ndarray,
    alpha: float = 0.5,
    colormap: int = cv2.COLORMAP_JET,
) -> np.ndarray:
    """
    Overlay heatmap on original image.
    heatmap: (H, W) in [0, 1].
    original_image: (H, W, 3) in [0, 255] or (H, W) grayscale.
    Returns RGB image (H, W, 3) in [0, 255].
    """
    if original_image.ndim == 2:
        original_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
    heatmap_uint8 = (heatmap * 255).astype(np.uint8)
    heatmap_colored = cv2.applyColorMap(heatmap_uint8, colormap)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    overlay = (alpha * heatmap_colored + (1 - alpha) * original_image).astype(np.uint8)
    return overlay
