# Results

Example outputs are saved under `outputs/` after running the pipeline.

## Training

![Training curves](../outputs/training_curves.png)

Loss and accuracy curves for training and validation over 15 epochs (ResNet18).

## Calibration

![Reliability diagrams](../outputs/reliability_diagrams.png)

Reliability diagrams comparing uncalibrated and temperature-scaled predictions on the validation set. ECE decreases after calibration while accuracy remains unchanged.

## Evaluation

![Evaluation results](../outputs/evaluation_results.png)

Test-set confusion matrix and calibrated reliability diagram.

## Explainability

![Grad-CAM example](../outputs/IM-0001-0001_uncertainty_gradcam.png)

Four-panel inference figure: original X-ray, Grad-CAM overlay, MC Dropout histogram, and summary metrics including TrustScore.

## TrustScore Distribution

![TrustScore distribution](../outputs/trustscore_distribution.png)

Histogram of TrustScore values across the test set (requires `--trust_eval` flag during evaluation).

## Reproducing Results

```bash
python -m training.train --model_type resnet18 --epochs 15
python -m evaluation.calibrate
python -m evaluation.evaluate --trust_eval
python -m inference.predict data/test/NORMAL/IM-0001-0001.jpeg
```
