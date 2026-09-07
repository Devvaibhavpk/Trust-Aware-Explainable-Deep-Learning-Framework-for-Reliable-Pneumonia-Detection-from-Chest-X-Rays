"""
Train/validation split utilities for the Chest X-Ray Pneumonia dataset.
"""

import random
import shutil
from pathlib import Path


def split_folder(
    src_dir: Path,
    train_ratio: float = 0.85,
    val_ratio: float = 0.15,
    seed: int = 42,
) -> None:
    """
    Split a folder with NORMAL/PNEUMONIA subdirs into train and val sets.

    Args:
        src_dir: Source directory containing class subfolders.
        train_ratio: Fraction of images assigned to training.
        val_ratio: Fraction of images assigned to validation.
        seed: Random seed for reproducible splits.
    """
    random.seed(seed)
    parent = src_dir.parent
    train_dir = parent / "train"
    val_dir = parent / "val"
    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)

    for class_name in ["NORMAL", "PNEUMONIA"]:
        class_dir = src_dir / class_name
        if not class_dir.exists():
            class_dir = src_dir / class_name.lower()
        if not class_dir.exists():
            print(f"Skip (not found): {class_dir}")
            continue

        images = [
            f for f in class_dir.glob("*.*")
            if f.suffix.lower() in (".jpg", ".jpeg", ".png")
        ]
        random.shuffle(images)
        n_val = max(1, int(len(images) * val_ratio))
        n_train = len(images) - n_val
        train_list = images[:n_train]
        val_list = images[n_train:]

        (train_dir / class_name).mkdir(parents=True, exist_ok=True)
        (val_dir / class_name).mkdir(parents=True, exist_ok=True)

        for f in train_list:
            dest = train_dir / class_name / f.name
            if not dest.exists() or dest.resolve() != f.resolve():
                try:
                    shutil.copy2(f, dest)
                except OSError as exc:
                    print(f"Copy failed {f} -> {dest}: {exc}")

        for f in val_list:
            dest = val_dir / class_name / f.name
            if not dest.exists() or dest.resolve() != f.resolve():
                try:
                    shutil.copy2(f, dest)
                except OSError as exc:
                    print(f"Copy failed {f} -> {dest}: {exc}")

        print(f"{class_name}: train={len(train_list)}, val={len(val_list)}")
