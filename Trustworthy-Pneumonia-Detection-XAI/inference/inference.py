"""
Single-image uncertainty-aware inference pipeline for chest X-ray classification.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from configs.config import (
    DEFAULT_MC_SAMPLES,
    HEATMAP_THRESHOLD,
    IMAGE_SIZE,
    MODEL_SAVE_DIR,
    OUTPUT_DIR,
    ensure_dirs,
)
from datasets.dataset import CLASS_NAMES
from datasets.transforms import IMAGENET_MEAN, IMAGENET_STD
from explainability.attention_maps import (
    LungSegmenter,
    focus_overlap_score,
    tensor_mask_to_numpy,
)
from explainability.gradcam import GradCAM, overlay_heatmap
from explainability.trustscore import TrustEngine, get_trust_level
from explainability.uncertainty import predict_with_uncertainty
from explainability.visualization import build_inference_figure, plot_mc_histogram, plot_summary_panel
from models.cnn_model import get_last_conv_layer_for_model
from models.ensemble import agreement_from_probabilities
from utils.helpers import configure_matplotlib_backend, show_or_open_figure
from utils.io import load_aux_model, load_model_and_calibrator

configure_matplotlib_backend(prefer_interactive=False)


def load_and_transform_image(
    image_path: str,
    device: torch.device,
) -> tuple[torch.Tensor, np.ndarray]:
    """Load an image and return a normalized tensor and denormalized RGB array."""
    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])
    img_pil = Image.open(image_path).convert("RGB")
    img_tensor = transform(img_pil).unsqueeze(0).to(device)
    img_np = img_tensor.squeeze(0).cpu().numpy().transpose(1, 2, 0)
    img_np = (img_np * np.array(IMAGENET_STD) + np.array(IMAGENET_MEAN)) * 255
    img_np = np.clip(img_np, 0, 255).astype(np.uint8)
    return img_tensor, img_np


def run_pipeline(
    image_path: str,
    save_dir: str = str(MODEL_SAVE_DIR),
    output_path: str | None = None,
    n_mc_samples: int = DEFAULT_MC_SAMPLES,
    densenet_dir: str | None = None,
    efficientnet_dir: str | None = None,
) -> dict:
    """
    Full uncertainty-aware inference pipeline for a single chest X-ray.

    Returns:
        Dictionary with predicted class, confidences, uncertainty, trust metrics,
        and path to the saved visualization.
    """
    ensure_dirs()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    model, model_type, calibrator = load_model_and_calibrator(device, save_dir)
    target_layer = get_last_conv_layer_for_model(model, model_type)
    img_tensor, img_np = load_and_transform_image(image_path, device)

    densenet_model = None
    efficientnet_model = None
    if densenet_dir is not None:
        densenet_model = load_aux_model(device, Path(densenet_dir), "densenet121")
    if efficientnet_dir is not None:
        efficientnet_model = load_aux_model(device, Path(efficientnet_dir), "efficientnet_b0")

    print(f"Running MC Dropout inference ({n_mc_samples} samples)...")
    mc_result = predict_with_uncertainty(model, img_tensor, n_samples=n_mc_samples, device=device)

    mean_prediction = mc_result["mean_prediction"]
    variance = mc_result["variance"]
    std_pred = mc_result["std"]
    mc_samples = mc_result["samples"]

    pred_class = 1 if mean_prediction >= 0.5 else 0
    pred_label = CLASS_NAMES[pred_class]

    model.eval()
    with torch.no_grad():
        logits = model(img_tensor).squeeze(-1)

    if calibrator is not None:
        calibrated_prob = calibrator.calibrate_probs(
            logits.unsqueeze(0).unsqueeze(-1)
        ).squeeze().item()
    else:
        calibrated_prob = mean_prediction

    gradcam = GradCAM(model, target_layer)
    heatmap = gradcam.generate(img_tensor, target_class=pred_class)
    overlay = overlay_heatmap(heatmap, img_np, alpha=0.5)

    segmenter = LungSegmenter.from_checkpoint(checkpoint_path=None, device=device)
    lung_mask_tensor = segmenter.segment(img_tensor)
    lung_mask_np = tensor_mask_to_numpy(lung_mask_tensor)
    focus_score = focus_overlap_score(heatmap, lung_mask_np, heatmap_threshold=HEATMAP_THRESHOLD)

    ensemble_probs = [mean_prediction]

    if densenet_model is not None:
        with torch.no_grad():
            dn_logits = densenet_model(img_tensor).squeeze(-1)
            ensemble_probs.append(torch.sigmoid(dn_logits).item())

    if efficientnet_model is not None:
        with torch.no_grad():
            ef_logits = efficientnet_model(img_tensor).squeeze(-1)
            ensemble_probs.append(torch.sigmoid(ef_logits).item())

    _, agreement_score = agreement_from_probabilities(ensemble_probs, threshold=0.5)

    engine = TrustEngine()
    trust_outputs = engine.summarize(
        calibrated_confidence=calibrated_prob,
        focus_score=focus_score,
        uncertainty=variance,
        agreement_score=agreement_score,
    )
    trust_score = trust_outputs["trust_score"]
    ood_flag = trust_outputs["ood_flag"]

    trust_level = get_trust_level(
        trust_score=trust_score,
        calibrated_confidence=calibrated_prob,
        focus_score=focus_score,
        uncertainty=variance,
    ).capitalize()

    print("=" * 60)
    print("CHEST X-RAY SCREENING RESULT  (Uncertainty-Aware)")
    print("=" * 60)
    print(f"Image:                   {image_path}")
    print(f"Predicted class:         {pred_label}")
    print(f"Raw confidence           (MC mean):        {mean_prediction:.4f}")
    print(f"Calibrated confidence    (temperature):    {calibrated_prob:.4f}")
    print(f"Uncertainty score        (MC variance):    {variance:.6f}")
    print(f"Uncertainty std          :                 {std_pred:.4f}")
    print(f"Focus score              (Grad-CAM × lungs): {focus_score:.4f}")
    print(f"Agreement score          (ensemble):       {agreement_score:.4f}")
    print(f"Trust score              :                 {trust_score:.4f}")
    print(f"Trust level              :                 {trust_level}")
    print(f"OOD / UNRELIABLE flag    :                 {ood_flag}")
    print("=" * 60)

    output_result = {
        "predicted_class": pred_label,
        "raw_confidence": mean_prediction,
        "calibrated_confidence": calibrated_prob,
        "uncertainty_score": variance,
        "focus_score": focus_score,
        "agreement_score": agreement_score,
        "trust_score": trust_score,
        "trust_level": trust_level,
        "ood_flag": ood_flag,
    }

    if output_path is None:
        output_path = OUTPUT_DIR / (Path(image_path).stem + "_uncertainty_gradcam.png")
    else:
        output_path = Path(output_path)

    # Save standalone high-resolution Grad-CAM overlay image (no embedded graphs/tables)
    pure_overlay_path = OUTPUT_DIR / (Path(image_path).stem + "_overlay.png")
    Image.fromarray(overlay).save(pure_overlay_path)
    output_result["pure_overlay_path"] = str(pure_overlay_path)

    # Save standalone MC Dropout sample distribution histogram (generated by chestxray_best.pt)
    fig_hist, ax_hist = plt.subplots(figsize=(6, 4))
    plot_mc_histogram(ax_hist, mc_samples, mean_prediction, std_pred)
    hist_path = OUTPUT_DIR / (Path(image_path).stem + "_histogram.png")
    fig_hist.savefig(hist_path, dpi=150, bbox_inches="tight", facecolor=fig_hist.get_facecolor())
    plt.close(fig_hist)
    output_result["histogram_path"] = str(hist_path)

    # Save standalone dual-panel figure (Histogram + Inference Summary) as requested
    fig_dual, axes_dual = plt.subplots(1, 2, figsize=(14, 5))
    fig_dual.patch.set_facecolor("#1a1a2e")
    ax_h = axes_dual[0]
    ax_h.set_facecolor("#0f3460")
    plot_mc_histogram(ax_h, mc_samples, mean_prediction, std_pred)
    ax_h.tick_params(colors="white")
    ax_h.xaxis.label.set_color("white")
    ax_h.yaxis.label.set_color("white")
    ax_h.title.set_color("white")
    for spine in ax_h.spines.values():
        spine.set_edgecolor("#34495e")

    ax_s = axes_dual[1]
    ax_s.set_facecolor("#1a1a2e")
    plot_summary_panel(ax_s, output_result)

    dual_path = OUTPUT_DIR / (Path(image_path).stem + "_dual_summary.png")
    fig_dual.savefig(dual_path, dpi=150, bbox_inches="tight", facecolor=fig_dual.get_facecolor())
    plt.close(fig_dual)
    output_result["dual_summary_path"] = str(dual_path)

    fig = build_inference_figure(img_np, overlay, mc_samples, mean_prediction, std_pred, output_result)
    fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Standalone overlay saved to: {pure_overlay_path}")
    print(f"Standalone histogram saved to: {hist_path}")
    print(f"Standalone dual summary saved to: {dual_path}")
    print(f"4-panel figure saved to: {output_path}")
    output_result["overlay_path"] = str(output_path)

    show_or_open_figure(output_path)
    plt.close(fig)
    return output_result
