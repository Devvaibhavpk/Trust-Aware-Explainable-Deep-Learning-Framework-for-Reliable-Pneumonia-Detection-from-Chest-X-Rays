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
   python scripts/prepare_dataset.py path/to/chest_xray --val_ratio 0.15
   ```

   This copies a disjoint train/val split into `data/train` and `data/val`, and copies the Kaggle test set into `data/test`.

## Notes

- Supported formats: `.jpg`, `.jpeg`, `.png`
- Images are resized to 224×224 and normalized with ImageNet statistics
- Dataset files are excluded from version control via `.gitignore`
