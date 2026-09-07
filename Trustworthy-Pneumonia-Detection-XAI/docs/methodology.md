# Methodology

## Classification

- **Task:** Binary chest X-ray classification (NORMAL vs PNEUMONIA)
- **Input:** 224×224 RGB images with ImageNet normalization
- **Output:** Single logit → sigmoid probability P(PNEUMONIA)
- **Loss:** Binary cross-entropy with logits (BCEWithLogitsLoss)
- **Optimizer:** Adam (lr = 1e-4)

## Probability Calibration

Post-hoc **Temperature Scaling** fits a scalar temperature T on the validation set:

```
p_calibrated = sigmoid(logit / T)
```

T is optimized to minimize negative log-likelihood. This improves **Expected Calibration Error (ECE)** without changing predicted classes.

## Explainability

**Grad-CAM** produces class-discriminative heatmaps from the last convolutional layer gradients. Heatmaps are overlaid on the original X-ray for visual inspection.

**FocusScore** measures overlap between high-activation Grad-CAM regions and a lung segmentation mask (U-Net when available, geometric prior otherwise):

```
FocusScore = Area(GradCAM ∩ Lung) / Area(GradCAM)
```

## Uncertainty Estimation

**Monte Carlo Dropout** runs N stochastic forward passes with dropout enabled at test time. The variance of predicted probabilities serves as an uncertainty score (Gal & Ghahramani, 2016).

## Trust Scoring

The **TrustEngine** combines four signals:

```
TrustScore = Confidence × FocusScore × (1 − Uncertainty) × AgreementScore
```

Trust levels (High / Medium / Low) are assigned using rule-based thresholds on calibrated confidence, uncertainty, and focus score.

## Evaluation Metrics

| Category | Metrics |
|----------|---------|
| Classification | Accuracy, Precision, Recall, F1, Confusion Matrix |
| Calibration | ECE, Reliability Diagram |
| Trust | FocusScore, TrustScore, OOD flag |
