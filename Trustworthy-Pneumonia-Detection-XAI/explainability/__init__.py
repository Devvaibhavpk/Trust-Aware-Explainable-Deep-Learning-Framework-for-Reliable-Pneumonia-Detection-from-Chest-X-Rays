"""Explainability modules: Grad-CAM, uncertainty, trust scoring, and visualization."""
from explainability.attention_maps import (
    LungSegmenter,
    SimpleUNet,
    focus_overlap_score,
    tensor_mask_to_numpy,
)
from explainability.gradcam import GradCAM, generate_gradcam_heatmap, overlay_heatmap
from explainability.trustscore import (
    TrustAnalyzer,
    TrustEngine,
    TrustEngineConfig,
    compute_trust_score,
    get_trust_level,
    heatmap_focus_score,
)
from explainability.uncertainty import (
    MCDropoutPredictor,
    enable_dropout,
    mc_dropout_uncertainty,
    ood_flag_from_confidence_uncertainty,
    predict_with_uncertainty,
)

__all__ = [
    "GradCAM",
    "generate_gradcam_heatmap",
    "overlay_heatmap",
    "predict_with_uncertainty",
    "MCDropoutPredictor",
    "enable_dropout",
    "mc_dropout_uncertainty",
    "ood_flag_from_confidence_uncertainty",
    "TrustAnalyzer",
    "TrustEngine",
    "TrustEngineConfig",
    "compute_trust_score",
    "get_trust_level",
    "heatmap_focus_score",
    "LungSegmenter",
    "SimpleUNet",
    "focus_overlap_score",
    "tensor_mask_to_numpy",
]
