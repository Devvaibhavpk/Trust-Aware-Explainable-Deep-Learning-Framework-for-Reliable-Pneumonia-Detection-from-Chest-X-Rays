# Faculty Demo Guide

This is the shortest path to show the project to faculty on Windows.

## What to say in one minute

This is a **trustworthy** chest X-ray pneumonia detector, not only an accuracy model. For each image it reports:

1. **Prediction** — Normal vs Pneumonia  
2. **Calibrated confidence** — temperature scaling so 80% confidence means it is right about 80% of the time  
3. **Grad-CAM heatmap** — where the CNN looked  
4. **MC Dropout uncertainty** — whether the model is unstable  
5. **Trust score / OOD flag** — whether the result is safe to show a clinician  

Use `Presentation.md` for the slide talking points.

## Google Colab (recommended for faculty day)

You do **not** need a local GPU. Use the notebook in this repo:

1. Zip this project folder (include the code, not the Kaggle images).
2. Open [Google Colab](https://colab.research.google.com/).
3. `Runtime` → `Change runtime type` → **T4 GPU**.
4. Upload `notebooks/colab_faculty_demo.ipynb` (`File` → `Upload notebook`) **or** open it from Drive.
5. Upload the project zip when the notebook asks, then upload your Kaggle `kaggle.json`.
6. Run all cells. Keep `QUICK = True` for a live demo; set it to `False` if you can wait for a full 15-epoch train.

The last cells show training curves, reliability diagrams, and the 4-panel Grad-CAM / TrustScore figure.

To show the same thing in a browser UI after training:

```powershell
pip install streamlit
python -m streamlit run app.py
```

Then open the local URL (usually `http://localhost:8501`).

## Local setup (once)

In PowerShell:

```powershell
cd "C:\Users\revku\Documents\projects\Health-care Project\Trustworthy-Pneumonia-Detection-XAI"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Download [Chest X-Ray Pneumonia (Kaggle)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia), unzip it, then:

```powershell
python scripts/prepare_dataset.py "C:\path\to\chest_xray"
```

That copies images into `data/train`, `data/val`, and `data/test` **without putting validation images back into train**.

## What to run on demo day

### Option A — quick live demo (CPU, a few minutes)

Accuracy will not be paper-grade. The UI and pipeline still work.

```powershell
python scripts/demo.py --quick
```

This trains a small ResNet18, calibrates it, evaluates, then opens a 4-panel inference figure on a test X-ray.

### Option B — full research run (GPU preferred)

```powershell
python -m training.train --model_type resnet18 --epochs 15
python -m evaluation.calibrate
python -m evaluation.evaluate --trust_eval
python -m inference.predict path\to\one\test\xray.jpeg
```

Or:

```powershell
python scripts/run_pipeline.py
```

then run inference on one image.

## What to show on screen

| File | What it proves |
|------|----------------|
| `outputs/*_uncertainty_gradcam.png` | Live diagnosis + heatmap + trust panel |
| `outputs/training_curves.png` | The model actually trained |
| `outputs/reliability_diagrams.png` | Calibration improved ECE |
| `outputs/evaluation_results.png` | Test accuracy / confusion matrix |
| `outputs/trustscore_distribution.png` | Trust metrics on the test set (`--trust_eval`) |

## If something is missing

| Symptom | Fix |
|---------|-----|
| `No training data found` | Run `scripts/prepare_dataset.py` on the unzipped Kaggle folder |
| `FileNotFoundError: chestxray_best.pt` | Train first (`python -m training.train` or `scripts/demo.py --quick`) |
| Training is extremely slow | Use `--quick` for the live show; full 15 epochs needs a GPU |
| Uncertainty is always ~0 on an old checkpoint | Retrain; ResNet18 now has dropout so MC Dropout can vary |

Do **not** claim clinical deployment. This is a research decision-support prototype on a public Kaggle dataset.
