"""
DataLoader factory for train/validation/test splits.
"""

from pathlib import Path
from typing import Tuple

from torch.utils.data import DataLoader

from datasets.dataset import ChestXRayDataset
from datasets.transforms import get_transforms


def get_dataloaders(
    data_dir: str = "data",
    image_size: int = 224,
    batch_size: int = 32,
    num_workers: int = 0,
    use_imagenet_norm: bool = True,
    pin_memory: bool = True,
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

    if len(train_ds) == 0:
        raise ValueError(
            "No training data found. Expected directory structure:\n"
            f"  {data_path / 'train'}/NORMAL/  and  {data_path / 'train'}/PNEUMONIA/\n"
            "with .jpg, .jpeg, or .png images. Download the Chest X-Ray Pneumonia dataset "
            "from Kaggle and place train/val/test folders under the data/ directory."
        )

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
