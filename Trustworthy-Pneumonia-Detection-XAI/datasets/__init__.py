"""Dataset loading and preprocessing for chest X-ray classification."""

_DATASET_EXPORTS = {
    "CLASS_NAMES",
    "CLASS_TO_IDX",
    "ChestXRayDataset",
    "IDX_TO_CLASS",
}
_PREPROCESS_EXPORTS = {"get_dataloaders"}
_TRANSFORM_EXPORTS = {"get_transforms", "IMAGENET_MEAN", "IMAGENET_STD"}

__all__ = [
    "CLASS_NAMES",
    "CLASS_TO_IDX",
    "IDX_TO_CLASS",
    "ChestXRayDataset",
    "get_dataloaders",
    "get_transforms",
    "IMAGENET_MEAN",
    "IMAGENET_STD",
]


def __getattr__(name: str):
    if name in _DATASET_EXPORTS:
        from datasets import dataset

        return getattr(dataset, name)
    if name in _PREPROCESS_EXPORTS:
        from datasets import preprocessing

        return getattr(preprocessing, name)
    if name in _TRANSFORM_EXPORTS:
        from datasets import transforms

        return getattr(transforms, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
