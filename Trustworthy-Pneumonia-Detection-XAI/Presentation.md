# Trustworthy Deep Learning System for Chest X-ray Pneumonia Detection
## A Calibrated and Explainable XAI Framework

---

## Slide 1: Title & Introduction
**Title:** Trustworthy Deep Learning System for Chest X-ray Pneumonia Detection
**Subtitle:** A Calibrated and Explainable XAI Framework
**Author/Presenter:** [Your Name / Team]
**Core Theme:** Moving beyond "black-box" medical AI by integrating probability calibration, explainability, uncertainty estimation, and unified trust scoring.

---

## Slide 2: Problem Statement & Motivation
- **The Black Box Problem:** Deep learning models for medical imaging are highly accurate but lack inherent reliability guarantees and transparency.
- **Silent Failures:** Standard CNNs often fail silently on Out-of-Distribution (OOD) data, outputting arbitrary predictions.
- **Overconfidence:** Uncalibrated models produce misleading confidence scores (e.g., predicting 99% probability based on a textual artifact rather than pathology).
- **The Solution:** A transparent, trustworthy AI framework that provides not only a diagnosis but also visual explanations, uncertainty metrics, and a quantifiable "Trust Score".

---

## Slide 3: System Architecture Overview
The framework is built upon four core layers:
1. **Classification Layer:** CNN Backbone (e.g., ResNet18) for binary Normal vs. Pneumonia prediction.
2. **Calibration Layer:** Post-hoc Temperature Scaling on validation logits to ensure reliable confidence estimates.
3. **Explainability Layer:** Grad-CAM spatial heatmaps combined with lung-region focus validation.
4. **Trust Assessment Layer:** Monte Carlo (MC) Dropout variance, ensemble agreement, and the overarching TrustEngine.

*(Note: Present the Mermaid architecture diagram from the docs here)*

---

## Slide 4: Classification Backbone
- **Task:** Binary classification (NORMAL vs. PNEUMONIA).
- **Input:** $224 \times 224$ RGB ImageNet-normalized X-ray images.
- **Output:** A single logit passed through a sigmoid function to yield $P(Pneumonia)$.
- **Optimization:** Binary Cross Entropy with Logits (`BCEWithLogitsLoss`), optimized using Adam ($lr=1e^{-4}$).
- **Modularity:** Supports multiple architectures including a Custom CNN, ResNet18 (default), VGG16, DenseNet121, and EfficientNet-B0.

---

## Slide 5: Probability Calibration (Temperature Scaling)
- **The Issue:** Modern deep neural networks are notoriously overconfident in their predictions.
- **The Method:** We implement Post-hoc Temperature Scaling.
- **Mechanism:** A scalar temperature parameter $T$ is fitted on the validation set to minimize the negative log-likelihood.
- **Formula:** $p_{calibrated} = \sigma(logit / T)$
- **Impact:** Temperature scaling preserves the rank order of predictions (accuracy remains unchanged) while significantly reducing the Expected Calibration Error (ECE) and producing a reliable, diagonal reliability diagram.

---

## Slide 6: Explainability via Grad-CAM
- **What it is:** Gradient-weighted Class Activation Mapping (Grad-CAM).
- **How it works:** Extracts gradients from the final convolutional layer of the CNN during the backward pass.
- **Output:** Produces a coarse, spatial, class-discriminative heatmap highlighting the regions of the X-ray most influential to the model's decision.
- **Clinical Value:** Enables visual inspection by radiologists to ensure the model is basing its diagnosis on actual lung pathology rather than spurious correlations (e.g., pacemakers, tubes, or L/R text markers).

---

## Slide 7: Focus Score & Anatomical Validation
- **The Gap:** A heatmap alone does not mathematically quantify whether the model's explanation is anatomically valid.
- **Our Innovation:** The `FocusScore` metric.
- **Mechanism:** Computes the overlap between high-activation Grad-CAM regions and a predefined central lung segmentation mask (or geometric prior).
- **Formula:** $FocusScore = \frac{Area(GradCAM \cap LungMask)}{Area(GradCAM)}$
- **Result:** Directly penalizes the model if its attention mass strays outside the valid anatomical regions.

---

## Slide 8: Uncertainty Estimation (MC Dropout)
- **Concept:** Bayesian approximation of model uncertainty using Monte Carlo (MC) Dropout.
- **Execution:** Performs $N$ stochastic forward passes with dropout layers left enabled during inference.
- **Measurement:** Calculates the variance of the predicted probabilities across the $N$ stochastic passes.
- **Interpretation:** High variance indicates high epistemic uncertainty (the model "doesn't know"). This is crucial for distinguishing between hard clinical cases and completely out-of-distribution (OOD) samples.

---

## Slide 9: Ensemble Agreement
- **Structural Uncertainty:** Relying on a single architecture can introduce bias.
- **Method:** The framework supports evaluating consensus across diverse architectural backbones (e.g., ResNet18 + DenseNet121).
- **Metric:** `AgreementScore` $\in [0, 1]$ represents the level of consensus among the models.
- **Benefit:** A low agreement score acts as an early warning system for edge cases, domain shifts, or ambiguous pathologies where a single model might confidently guess wrong.

---

## Slide 10: The TrustEngine Framework
- **Core Innovation:** The unified `TrustEngine` aggregates multiple safety signals into a singular, actionable metric.
- **TrustScore Formula:** 
  $TrustScore = Confidence_{calib} \times FocusScore \times (1 - Uncertainty_{clamped}) \times AgreementScore$
- **Trust Levels:**
  - **High Trust:** High confidence ($>0.8$), low uncertainty ($<0.1$).
  - **Medium Trust:** Borderline metrics.
  - **Low Trust:** High uncertainty ($>0.3$) or low focus ($<0.35$).

---

## Slide 11: Out-of-Distribution (OOD) Detection
- **Safety First:** Safe failure is paramount in clinical settings.
- **Mechanism:** The TrustEngine implements a hard OOD flagging system based on strict thresholds.
  - *Confidence Threshold:* $0.6$
  - *Uncertainty Threshold:* $0.03$
- **Rule:** If $Confidence < 0.6$ AND $Uncertainty > 0.03$, the sample is flagged as **UNRELIABLE**.
- **Impact:** Prevents the system from rendering diagnoses on corrupted images, non-chest X-rays, or severe domain shifts.

---

## Slide 12: Training & Optimization Pipeline
- **Data Handling:** Automated end-to-end pipeline for processing the Kaggle Chest X-Ray dataset, including rigorous train/val/test splitting.
- **Monitoring:** Tracks training/validation loss and accuracy over epochs.
- **Checkpointing:** Automatically saves the best model weights (`best.pt`) based on validation performance to prevent overfitting.
- **Testing:** Strict evaluation on a held-out test set to ensure robust generalizability.

---

## Slide 13: Evaluation & Reliability Metrics
- **Classification:** Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
- **Calibration:** Expected Calibration Error (ECE) and before/after Reliability Diagrams.
- **Trust Metrics:** Analysis of the TrustScore distribution across the test set.
- **Actionability:** Allows hospital administrators to tune thresholds based on their specific clinical risk appetite (e.g., optimizing for zero false negatives).

---

## Slide 14: End-to-End Inference Pipeline
A fully automated programmatic API (`inference.predict`) processes single images through the entire trustworthy pipeline:
1. **MC Dropout Forward Passes:** Yields mean prediction & variance.
2. **Temperature Scaling:** Yields calibrated confidence.
3. **Grad-CAM:** Generates the spatial heatmap.
4. **Lung Segmentation:** Computes the Focus Score.
5. **TrustEngine:** Aggregates data to output Trust Level & OOD Flag.
- **Output:** A comprehensive four-panel visual report containing the original X-ray, Grad-CAM overlay, MC Dropout histogram, and summary metrics.

---

## Slide 15: Conclusion & Future Scope
- **Conclusion:** By providing probability calibration, visual explanations, explicit uncertainty boundaries, and a unified trust score, this framework successfully transitions deep learning from a "black box" to a verifiable, safe clinical decision support tool.
- **Impact:** Prevents silent failures and builds clinician trust through transparency.
- **Future Scope:** 
  - Integration with hospital PACS/DICOM systems.
  - Extending the framework to multi-class pulmonary diseases (e.g., COVID-19, Tuberculosis).
  - Enhancing the lung segmentation module with heavier foundational models.
