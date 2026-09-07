# Chest X-Ray Pneumonia Dataset

## Source

[Chest X-Ray Pneumonia (Kaggle)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)

## Expected Layout

```
data/
├── train/
│   ├── NORMAL/
│   └── PNEUMONIA/
├── val/
│   ├── NORMAL/
│   └── PNEUMONIA/
└── test/
    ├── NORMAL/
    └── PNEUMONIA/
```

## Setup

1. Download and unzip the Kaggle dataset.
2. Split the original training folder into train/val:

   ```bash
   python scripts/prepare_dataset.py path/to/chest_xray/train --val_ratio 0.15
   ```

3. Copy or symlink the resulting folders into `data/train`, `data/val`, and copy the Kaggle test set to `data/test`.

## Notes

- Supported formats: `.jpg`, `.jpeg`, `.png`
- Images are resized to 224×224 and normalized with ImageNet statistics
- Dataset files are excluded from version control via `.gitignore`
