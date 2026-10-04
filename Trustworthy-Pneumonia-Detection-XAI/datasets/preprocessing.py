"""
DataLoader factory for train/validation/test splits.
"""

from pathlib import Path
from typing import Optional, Tuple

import torch
from torch.utils.data import DataLoader, Subset

from datasets.dataset import ChestXRayDataset
from datasets.transforms import get_transforms


def _maybe_subset(dataset, max_samples: Optional[int], seed: int = 42):
    """Optionally cap a dataset size for quick faculty demos."""
    if max_samples is None or max_samples <= 0 or len(dataset) <= max_samples:
        return dataset
    generator = torch.Generator()
    generator.manual_seed(seed)
    indices = torch.randperm(len(dataset), generator=generator)[:max_samples].tolist()
    return Subset(dataset, indices)


def get_dataloaders(
    data_dir: str = "data",
    image_size: int = 224,
    batch_size: int = 32,
    num_workers: int = 0,
    use_imagenet_norm: bool = True,
    pin_memory: bool = True,
    max_samples: Optional[int] = None,
    seed: int = 42,
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Build train, validation, and test DataLoaders.

    Args:
        data_dir: Root containing train/, val/, and test/ subdirectories.
        image_size: Target image size passed to transforms.
        batch_size: Batch size for all loaders.
        num_workers: DataLoader worker count.
        use_imagenet_norm: Use ImageNet normalization statistics.
        pin_memory: Enable pinned memory for GPU transfer.
        max_samples: Optional cap on images per split (useful for a quick demo).
        seed: RNG seed used when subsampling.

    Returns:
        Tuple of (train_loader, val_loader, test_loader).
    """
    data_path = Path(data_dir)
    train_ds = ChestXRayDataset(
        root=str(data_path / "train"),
        transform=get_transforms("train", image_size, use_imagenet_norm),
    )
    val_ds = ChestXRayDataset(
        root=str(data_path / "val"),
        transform=get_transforms("val", image_size, use_imagenet_norm),
    )
    test_ds = ChestXRayDataset(
        root=str(data_path / "test"),
        transform=get_transforms("test", image_size, use_imagenet_norm),
    )
    train_ds = _maybe_subset(train_ds, max_samples, seed)
    val_ds = _maybe_subset(val_ds, max_samples, seed)
    test_ds = _maybe_subset(test_ds, max_samples, seed)

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )
    test_loader = DataLoader(
        test_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )
    return train_loader, val_loader, test_loader
