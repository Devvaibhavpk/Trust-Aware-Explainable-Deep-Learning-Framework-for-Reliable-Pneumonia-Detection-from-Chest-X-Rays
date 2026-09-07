"""
PyTorch Dataset for Chest X-Ray Pneumonia classification.
"""

from pathlib import Path
from typing import Optional, Tuple

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

CLASS_NAMES = ["NORMAL", "PNEUMONIA"]
CLASS_TO_IDX = {"NORMAL": 0, "PNEUMONIA": 1}
IDX_TO_CLASS = {0: "NORMAL", 1: "PNEUMONIA"}


class ChestXRayDataset(Dataset):
    """
    Dataset for chest X-ray images from directory-based layout.

    Root should contain subdirs NORMAL and PNEUMONIA (or lowercase equivalents).
    """

    def __init__(
        self,
        root: str,
        transform: Optional[transforms.Compose] = None,
        extension: Tuple[str, ...] = (".jpg", ".jpeg", ".png"),
    ) -> None:
        self.root = Path(root)
        self.transform = transform
        self.extension = extension
        self.samples: list[tuple[str, int]] = []
        self._load_samples()

    def _load_samples(self) -> None:
        """Collect image paths and labels from class subdirectories."""
        for class_name in CLASS_NAMES:
            class_dir = self.root / class_name
            if not class_dir.exists():
                class_dir = self.root / class_name.lower()
            if not class_dir.exists():
                continue
            idx = CLASS_TO_IDX[class_name]
            for path in class_dir.iterdir():
                if path.suffix.lower() in self.extension:
                    self.samples.append((str(path), idx))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int, str]:
        path, label = self.samples[index]
        image = Image.open(path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label, path
