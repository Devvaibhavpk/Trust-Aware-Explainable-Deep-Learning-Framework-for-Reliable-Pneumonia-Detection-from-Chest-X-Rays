"""
Train/validation split utilities for the Chest X-Ray Pneumonia dataset.
"""

import random
import shutil
from pathlib import Path


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
CLASS_NAMES = ["NORMAL", "PNEUMONIA"]


def _class_dir(root: Path, class_name: str) -> Path | None:
    for candidate in (root / class_name, root / class_name.lower()):
        if candidate.exists():
            return candidate
    return None


def _list_images(class_dir: Path) -> list[Path]:
    return [
        path
        for path in class_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    ]


def _copy_files(files: list[Path], dest_dir: Path) -> int:
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for src in files:
        dest = dest_dir / src.name
        shutil.copy2(src, dest)
        copied += 1
    return copied


def split_kaggle_dataset(
    source_root: Path,
    dest_root: Path,
    val_ratio: float = 0.15,
    seed: int = 42,
) -> None:
    """
    Copy the Kaggle chest-xray layout into dest_root without train/val leakage.

    Accepts either:
      - the Kaggle root (contains train/, test/, optional val/)
      - the Kaggle train folder (contains NORMAL/ and PNEUMONIA/)
    """
    source_root = source_root.resolve()
    dest_root = dest_root.resolve()
    random.seed(seed)

    train_src = source_root / "train"
    if _class_dir(source_root, "NORMAL") is not None:
        train_src = source_root
        test_src = source_root.parent / "test"
    else:
        test_src = source_root / "test"

    if _class_dir(train_src, "NORMAL") is None and _class_dir(train_src, "PNEUMONIA") is None:
        raise FileNotFoundError(
            f"Could not find NORMAL/PNEUMONIA folders under {train_src}. "
            "Pass the Kaggle chest_xray directory or its train folder."
        )

    train_dest = dest_root / "train"
    val_dest = dest_root / "val"
    test_dest = dest_root / "test"

    for class_name in CLASS_NAMES:
        class_dir = _class_dir(train_src, class_name)
        if class_dir is None:
            print(f"Skip (not found): {class_name}")
            continue

        images = _list_images(class_dir)
        random.shuffle(images)
        n_val = max(1, int(len(images) * val_ratio)) if images else 0
        val_files = images[:n_val]
        train_files = images[n_val:]

        n_train = _copy_files(train_files, train_dest / class_name)
        n_copied_val = _copy_files(val_files, val_dest / class_name)
        print(f"{class_name}: train={n_train}, val={n_copied_val}")

        test_class = _class_dir(test_src, class_name) if test_src.exists() else None
        if test_class is not None:
            n_test = _copy_files(_list_images(test_class), test_dest / class_name)
            print(f"{class_name}: test={n_test}")

    print(f"Dataset prepared at {dest_root}")


def split_folder(
    src_dir: Path,
    train_ratio: float = 0.85,
    val_ratio: float = 0.15,
    seed: int = 42,
    dest_root: Path | None = None,
) -> None:
    """Backward-compatible wrapper around split_kaggle_dataset()."""
    del train_ratio
    project_data = Path(__file__).resolve().parent.parent / "data"
    split_kaggle_dataset(src_dir, dest_root or project_data, val_ratio=val_ratio, seed=seed)
