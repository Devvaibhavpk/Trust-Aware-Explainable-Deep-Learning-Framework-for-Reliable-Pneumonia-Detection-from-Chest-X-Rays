"""CNN models and ensemble agreement for chest X-ray classification."""
from models.ensemble import agreement_from_probabilities, majority_vote

_CNN_EXPORTS = (
    "ChestXRayCNN",
    "build_model",
    "get_resnet18",
    "get_vgg16",
    "get_densenet121",
    "get_efficientnet_b0",
    "get_last_conv_layer_for_model",
)

__all__ = [
    *_CNN_EXPORTS,
    "majority_vote",
    "agreement_from_probabilities",
]


def __getattr__(name: str):
    if name in _CNN_EXPORTS:
        from models import cnn_model

        return getattr(cnn_model, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
