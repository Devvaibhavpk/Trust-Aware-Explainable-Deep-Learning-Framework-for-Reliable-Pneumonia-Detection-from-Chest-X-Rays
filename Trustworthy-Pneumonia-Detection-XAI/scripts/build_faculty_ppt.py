"""Build a self-explanatory faculty PowerPoint for the XAI pneumonia project."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import nsmap
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Emu, Inches, Pt

NAVY = RGBColor(0, 32, 96)       # Darker, bolder navy
TEAL = RGBColor(0, 128, 128)     # Standard high-contrast teal
GOLD = RGBColor(255, 192, 0)     # Brighter gold
WHITE = RGBColor(255, 255, 255)
OFF = RGBColor(240, 240, 240)    # Slightly more contrast for off-white
INK = RGBColor(0, 0, 0)          # True black for highest text contrast
MUTED = RGBColor(64, 64, 64)     # Darker gray for better readability
RED = RGBColor(192, 0, 0)        # Sharper red

OUT = Path(__file__).resolve().parent.parent / "docs" / "Trustworthy_Pneumonia_XAI_Faculty_Presentation_v2.pptx"


def _set_run(run, text, size, bold=False, color=INK, font="Calibri"):
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def _fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def _rect(slide, l, t, w, h, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    _fill(shape, color)
    return shape


def _textbox(slide, l, t, w, h, text, size, bold=False, color=INK, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    _set_run(p.add_run() if p.runs else _ensure_run(p), text, size, bold, color)
    # python-pptx: paragraphs start with empty run sometimes
    if p.runs:
        _set_run(p.runs[0], text, size, bold, color)
        # remove extra if we added
        if len(p.runs) > 1:
            p.runs[0].text = text
    return box


def _ensure_run(p):
    if p.runs:
        return p.runs[0]
    return p.add_run()


def add_footer(slide, page, total):
    _rect(slide, Inches(0), Inches(7.28), Inches(13.333), Inches(0.22), NAVY)
    box = slide.shapes.add_textbox(Inches(0.4), Inches(7.28), Inches(10.5), Inches(0.22))
    p = box.text_frame.paragraphs[0]
    _set_run(_ensure_run(p), "Health care Data Analytics  ·  Trustworthy Pneumonia Detection using XAI", 10, False, WHITE)
    num = slide.shapes.add_textbox(Inches(11.6), Inches(7.28), Inches(1.4), Inches(0.22))
    p = num.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    _set_run(_ensure_run(p), f"{page}  /  {total}", 10, False, WHITE)


def header_bar(slide, title):
    _rect(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.05), NAVY)
    _rect(slide, Inches(0), Inches(1.05), Inches(13.333), Inches(0.08), GOLD)
    box = slide.shapes.add_textbox(Inches(0.45), Inches(0.22), Inches(12.4), Inches(0.7))
    p = box.text_frame.paragraphs[0]
    _set_run(_ensure_run(p), title, 26, True, WHITE)


def bullets(slide, items, top=1.35, left=0.5, width=12.3, size=16, spacing=True):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5.7))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(10 if spacing else 6)
        if isinstance(item, tuple):
            head, body = item
            run = _ensure_run(p)
            _set_run(run, head + "  ", size, True, TEAL)
            run2 = p.add_run()
            _set_run(run2, body, size, False, INK)
        else:
            _set_run(_ensure_run(p), item, size, False, INK)
    return box


def card(slide, l, t, w, h, title, body, accent=TEAL):
    shape = _rect(slide, Inches(l), Inches(t), Inches(w), Inches(h), WHITE)
    shape.line.fill.solid()
    shape.line.color.rgb = RGBColor(220, 226, 232)
    _rect(slide, Inches(l), Inches(t), Inches(0.1), Inches(h), accent)
    tb = slide.shapes.add_textbox(Inches(l + 0.25), Inches(t + 0.12), Inches(w - 0.4), Inches(0.4))
    _set_run(_ensure_run(tb.text_frame.paragraphs[0]), title, 16, True, NAVY)
    bb = slide.shapes.add_textbox(Inches(l + 0.25), Inches(t + 0.5), Inches(w - 0.4), Inches(h - 0.62))
    bb.text_frame.word_wrap = True
    _set_run(_ensure_run(bb.text_frame.paragraphs[0]), body, 13, False, MUTED)


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    slides_spec = []

    # We add slides then stamp footers with total
    def new():
        return prs.slides.add_slide(blank)

    # 1 Title
    s = new()
    _rect(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), NAVY)
    _rect(s, Inches(0), Inches(0), Inches(0.18), Inches(7.5), GOLD)
    box = s.shapes.add_textbox(Inches(0.7), Inches(1.15), Inches(12), Inches(0.4))
    _set_run(_ensure_run(box.text_frame.paragraphs[0]), "COURSE PROJECT  ·  HEALTH CARE DATA ANALYTICS", 14, True, GOLD)
    box = s.shapes.add_textbox(Inches(0.7), Inches(1.7), Inches(12), Inches(1.8))
    tf = box.text_frame
    tf.word_wrap = True
    _set_run(_ensure_run(tf.paragraphs[0]), "Trustworthy Deep Learning System for", 32, True, WHITE)
    p = tf.add_paragraph()
    _set_run(_ensure_run(p), "Chest X-Ray Pneumonia Detection", 32, True, WHITE)
    p = tf.add_paragraph()
    _set_run(_ensure_run(p), "A calibrated and explainable AI (XAI) framework", 18, False, RGBColor(186, 210, 220))
    box = s.shapes.add_textbox(Inches(0.7), Inches(4.3), Inches(12), Inches(2.2))
    tf = box.text_frame
    tf.word_wrap = True
    _set_run(_ensure_run(tf.paragraphs[0]), "Team Members", 13, True, GOLD)
    p = tf.add_paragraph()
    _set_run(_ensure_run(p), "Goutham Kumar   ·   Adhithiyan C   ·   Vaibhav Pk   ·   Yadarth Sangem", 20, True, WHITE)
    p = tf.add_paragraph()
    _set_run(_ensure_run(p), "This presentation is written to be readable on its own: each slide explains the concept, why it matters in healthcare, and how we implemented it.", 14, False, RGBColor(176, 190, 204))

    # 2 Agenda
    s = new()
    header_bar(s, "What this presentation covers")
    bullets(
        s,
        [
            ("The clinical problem. ", "Pneumonia screening from chest X-rays, and why a raw CNN score is not enough for healthcare."),
            ("Accuracy is not trust. ", "Overconfidence, silent failures, and black-box decisions."),
            ("The four safety layers. ", "Classification, calibration, explainability, and trust assessment."),
            ("Core methods, explained. ", "ResNet18, temperature scaling, Grad-CAM, FocusScore, MC Dropout, ensemble agreement, TrustEngine, OOD flags."),
            ("How we evaluate and demo. ", "Metrics, reliability diagrams, Colab pipeline, and a Streamlit interface."),
            ("Limits and next steps. ", "This is a research prototype, not a licensed clinical device."),
        ],
    )

    # 3 Problem
    s = new()
    header_bar(s, "Clinical problem: pneumonia on chest X-rays")
    bullets(
        s,
        [
            ("What pneumonia is. ", "An infection that fills air sacs with fluid or pus. Chest radiographs are a first-line, widely available screening tool."),
            ("What the model does. ", "Binary classification: NORMAL vs PNEUMONIA from a single frontal chest X-ray."),
            ("Why deep learning is used. ", "CNNs can learn texture and opacity patterns that correlate with consolidation, but they do not automatically know anatomy or uncertainty."),
            ("The healthcare requirement. ", "A clinician needs more than a label. They need: How sure is the model? Where did it look? Should this output be trusted or reviewed?"),
            ("Dataset used. ", "Public Kaggle Chest X-Ray Pneumonia dataset (pediatric CXRs, NORMAL / PNEUMONIA folders, train–val–test split with no train/val leakage)."),
        ],
    )

    # 4 Why accuracy fails
    s = new()
    header_bar(s, "Why “high accuracy” is not the same as trustworthy AI")
    card(s, 0.45, 1.4, 4.0, 5.4, "1. Black box", "A CNN maps pixels to a probability, but does not say which pixels mattered. In medicine, a right answer for the wrong reason (text markers, tubes, laterality letters) is dangerous.", RED)
    card(s, 4.65, 1.4, 4.0, 5.4, "2. Overconfidence", "Modern networks often output 0.99 even when they are guessing. Uncalibrated confidence misleads triage: people treat 99% as certainty. We measure this with Expected Calibration Error (ECE).", GOLD)
    card(s, 8.85, 1.4, 4.0, 5.4, "3. Silent failure", "On damaged images, non-chest photos, or domain shift, a vanilla model still prints a class. Safe systems must flag Out-of-Distribution (OOD) cases as UNRELIABLE instead of guessing.", TEAL)

    # 5 Goal
    s = new()
    header_bar(s, "Project goal")
    bullets(
        s,
        [
            ("Not only detect pneumonia. ", "Build a decision-support pipeline that returns a diagnosis plus evidence and a safety score."),
            ("Four outputs for every image. ", "(1) Predicted class, (2) calibrated confidence, (3) visual explanation (Grad-CAM), (4) TrustScore / trust level / OOD flag."),
            ("Design principle. ", "If any safety signal is weak — low focus on lungs, high uncertainty, or low confidence — the system should downgrade trust instead of looking certain."),
            ("Intended use. ", "Academic demonstration of trustworthy ML for Health care Data Analytics. Not for real patient care or regulatory deployment."),
        ],
    )

    # 6 Architecture
    s = new()
    header_bar(s, "System architecture — four layers")
    card(s, 0.4, 1.35, 3.05, 5.5, "Classification", "CNN backbone (default ResNet18). Input 224×224 ImageNet-normalized X-ray. Output: one logit → sigmoid → P(Pneumonia). Loss: BCE with logits. Optimizer: Adam, learning rate 1e-4.", TEAL)
    card(s, 3.55, 1.35, 3.05, 5.5, "Calibration", "Post-hoc Temperature Scaling on the validation set. p_cal = sigmoid(logit / T). Accuracy stays the same; probabilities become honest. We track ECE and reliability diagrams.", GOLD)
    card(s, 6.7, 1.35, 3.05, 5.5, "Explainability", "Grad-CAM heatmap from the last convolutional layer. FocusScore = area(CAM ∩ lung prior) / area(CAM). Penalizes attention on collars, text, or corners.", RGBColor(49, 92, 160))
    card(s, 9.85, 1.35, 3.05, 5.5, "Trust", "MC Dropout variance + optional ensemble agreement. TrustEngine multiplies the signals and can raise an OOD / UNRELIABLE flag.", RED)

    # 7 CNN
    s = new()
    header_bar(s, "Layer 1 — CNN classifier (ResNet18 by default)")
    bullets(
        s,
        [
            ("Task. ", "One image in → one probability out. If P(Pneumonia) ≥ 0.5 we predict PNEUMONIA, else NORMAL."),
            ("Why ResNet18. ", "A residual network pretrained on ImageNet. Transfer learning reuses generic visual filters, then we replace the last layer with a single logit and dropout. Dropout is required so Monte Carlo uncertainty is not always zero."),
            ("Other backbones supported. ", "Custom CNN, VGG16, DenseNet121, EfficientNet-B0 — same training and Grad-CAM interface."),
            ("Training hygiene. ", "Best checkpoint is saved from validation accuracy. Train and validation images are disjoint. Test images are held out until evaluation."),
            ("What this layer cannot do. ", "It does not know if the probability is calibrated, if the model looked at lungs, or if the input is even a chest X-ray. Those jobs belong to later layers."),
        ],
    )

    # 8 Calibration
    s = new()
    header_bar(s, "Layer 2 — Probability calibration (temperature scaling)")
    bullets(
        s,
        [
            ("The idea in one sentence. ", "If the model says 80% pneumonia, then among all cases scored ~80%, about 80% should actually be pneumonia."),
            ("Method. ", "We keep the trained CNN frozen. We learn one scalar temperature T on the validation set by minimizing negative log-likelihood (cross-entropy on probabilities)."),
            ("Formula. ", "p_calibrated = sigmoid(logit / T). T > 1 softens overconfident logits; T < 1 would sharpen them. Ranking of cases does not change, so accuracy is unchanged."),
            ("ECE (Expected Calibration Error). ", "Split predictions into confidence bins. In each bin, compare average confidence with actual accuracy. ECE is the weighted average of those gaps. Lower is better."),
            ("Reliability diagram. ", "A plot of confidence vs accuracy. A trustworthy model hugs the diagonal. After temperature scaling this curve typically moves closer to the diagonal."),
        ],
    )

    # 9 Grad-CAM
    s = new()
    header_bar(s, "Layer 3a — Grad-CAM: where did the network look?")
    bullets(
        s,
        [
            ("Name. ", "Gradient-weighted Class Activation Mapping (Selvaraju et al.)."),
            ("How it is computed. ", "Forward pass to the last conv layer (activations). Backward pass of the target class logit (gradients). Channel weights = global-average of gradients. Weighted sum of activation maps → ReLU → upsample to 224×224 → overlay on the X-ray."),
            ("How to read the heatmap. ", "Warm colors = regions that most increased the predicted class score. A pneumonia call should light up lung fields / consolidation, not the ‘R’ marker or the image border."),
            ("Clinical value. ", "Lets a human audit the reason. If Grad-CAM highlights a pacemaker or a tube, the prediction is a shortcut, not pathology."),
            ("Limitation. ", "A pretty heatmap is still qualitative. We therefore convert it into a number: FocusScore."),
        ],
    )

    # 10 Focus
    s = new()
    header_bar(s, "Layer 3b — FocusScore: is the explanation on the lungs?")
    bullets(
        s,
        [
            ("Why we added it. ", "Grad-CAM alone does not fail the model when the blob is in the wrong place. FocusScore makes anatomy a hard constraint."),
            ("Lung mask. ", "If a trained lung U-Net is available we use it. Otherwise we use a geometric prior: a central rectangle that roughly covers the lung fields on a frontal CXR. The demo uses this prior so the pipeline always runs."),
            ("Formula. ", "FocusScore = Area(high-activation Grad-CAM ∩ lung mask) / Area(high-activation Grad-CAM). Values near 1 mean the explanation is inside lungs; near 0 means it is mostly outside."),
            ("Threshold. ", "Grad-CAM is binarised at 0.4 before overlap is computed, so faint noise is ignored."),
            ("Effect on trust. ", "Low FocusScore pulls TrustScore down and can force a Low trust level, even if confidence is high."),
        ],
    )

    # 11 MC Dropout
    s = new()
    header_bar(s, "Layer 4a — Uncertainty with Monte Carlo Dropout")
    bullets(
        s,
        [
            ("Reference. ", "Gal & Ghahramani (2016): dropout at test time is a cheap Bayesian approximation."),
            ("Procedure. ", "Keep BatchNorm in eval mode, but turn Dropout layers ON. Run N stochastic forward passes (default 30 in full inference). Each pass gives a slightly different P(Pneumonia)."),
            ("Statistics. ", "Mean of the N probabilities = raw confidence. Variance of the N probabilities = uncertainty score. High variance means the model’s answer is unstable."),
            ("How to interpret. ", "Low variance: the network is consistently sure (still may be consistently wrong). High variance: the network ‘does not know’ — hard case or OOD input."),
            ("Implementation note. ", "Stock ResNet18 has no dropout in the head. We add Dropout(0.5) before the final linear layer so this uncertainty signal actually exists."),
        ],
    )

    # 12 Ensemble
    s = new()
    header_bar(s, "Layer 4b — Ensemble agreement")
    bullets(
        s,
        [
            ("Idea. ", "One architecture can be biased. If ResNet18 and DenseNet121 disagree on the same X-ray, that disagreement is a warning."),
            ("AgreementScore. ", "Each model votes NORMAL or PNEUMONIA. Agreement = (number of models in the majority) / (total models). Range is [0, 1]."),
            ("In a single-model demo. ", "Only one vote exists, so agreement is 1.0 by definition. The code still accepts extra checkpoints (--densenet_dir, --efficientnet_dir) for a true ensemble."),
            ("Role in TrustScore. ", "Agreement is a multiplier. Disagreement cannot be hidden by high confidence from a single net."),
        ],
    )

    # 13 TrustEngine
    s = new()
    header_bar(s, "TrustEngine — one number, three levels")
    bullets(
        s,
        [
            ("Formula. ", "TrustScore = Confidence_calibrated × FocusScore × (1 − Uncertainty) × AgreementScore. Each term is clipped to [0, 1]. Confidence uses max(p, 1−p) so a confident NORMAL is not punished."),
            ("Why multiply, not add. ", "A single failed safety check should collapse trust. Addition would let a 0.99 confidence hide a 0.1 focus score."),
            ("High trust. ", "Calibrated confidence > 0.8 and uncertainty < 0.1 (and focus not critically low). Suitable to display as a stable screening suggestion."),
            ("Medium trust. ", "Borderline confidence or moderate uncertainty. Show the heatmap and ask for review."),
            ("Low trust. ", "Uncertainty > 0.3 or FocusScore < 0.35. Do not treat the class label as reliable."),
        ],
    )

    # 14 OOD
    s = new()
    header_bar(s, "Out-of-distribution (OOD) / UNRELIABLE flag")
    bullets(
        s,
        [
            ("Safe failure. ", "In clinic, refusing to answer can be better than a confident wrong answer on a blurry photo or an abdominal film."),
            ("Hard rule in this project. ", "Flag UNRELIABLE if calibrated confidence < 0.6 AND MC variance > 0.03."),
            ("What this catches. ", "Low confidence plus unstable dropout samples — typical of inputs the CNN never saw in training."),
            ("What this is not. ", "It is not a full OOD detector (no dedicated outlier model). It is a conservative gate using signals we already compute."),
            ("How it is shown. ", "The Streamlit app and the 4-panel inference figure print OOD flag = True/False next to the trust level."),
        ],
    )

    # 15 Inference
    s = new()
    header_bar(s, "End-to-end inference (one image)")
    bullets(
        s,
        [
            ("Step 1. ", "Load X-ray, resize to 224×224, ImageNet-normalize."),
            ("Step 2. ", "MC Dropout → mean P(Pneumonia) and variance."),
            ("Step 3. ", "Single deterministic forward pass → logit → temperature scaling → calibrated confidence."),
            ("Step 4. ", "Grad-CAM on the last conv layer → overlay; lung prior → FocusScore."),
            ("Step 5. ", "Optional extra models → AgreementScore."),
            ("Step 6. ", "TrustEngine → TrustScore, trust level, OOD flag."),
            ("Human-facing output. ", "A four-panel figure: original X-ray, Grad-CAM overlay, MC histogram, and a metrics/trust summary. Also exposed as a Streamlit web app and a Colab notebook."),
        ],
        size=15,
    )

    # 16 Metrics
    s = new()
    header_bar(s, "How we evaluate the system")
    card(s, 0.45, 1.4, 4.0, 5.4, "Discrimination", "Accuracy, Precision, Recall, F1-score, confusion matrix, ROC-AUC, and precision–recall. These answer: does the class label match the test set?", TEAL)
    card(s, 4.65, 1.4, 4.0, 5.4, "Calibration", "ECE before vs after temperature scaling; reliability diagrams; confidence histograms. These answer: is 80% actually 80%?", GOLD)
    card(s, 8.85, 1.4, 4.0, 5.4, "Trust & XAI", "FocusScore distribution, TrustScore histogram, trust-level counts, uncertainty vs confidence (correct vs wrong), Grad-CAM gallery. These answer: should a person believe this case?", RED)

    # 17 Demo
    s = new()
    header_bar(s, "Demonstration for faculty")
    bullets(
        s,
        [
            ("Google Colab + GPU. ", "Download Kaggle data, train, calibrate, evaluate, then generate a 12-plot faculty figure pack."),
            ("Upload an X-ray. ", "The notebook / Streamlit UI accepts a jpg/png and prints class, confidence, uncertainty, focus, and trust."),
            ("Streamlit app (app.py). ", "Browser frontend with tabs: Screen an X-ray, Faculty graphs, Pipeline results, How it works."),
            ("What to say in 30 seconds. ", "We do not stop at accuracy. Every prediction is calibrated, visually explained, uncertainty-aware, and assigned a trust level."),
        ],
        top=1.35, left=0.5, width=6.0, size=14
    )
    # Add screenshot image to demo slide if it exists
    project_root = Path(__file__).resolve().parent.parent
    potential_image = project_root / "Screenshot 2026-09-23 095826.png"
    if potential_image.exists():
        s.shapes.add_picture(str(potential_image), Inches(6.8), Inches(1.35), width=Inches(6.0))
    elif (project_root / "outputs").exists() and list((project_root / "outputs").glob("*.png")):
        s.shapes.add_picture(str(list((project_root / "outputs").glob("*.png"))[0]), Inches(6.8), Inches(1.35), width=Inches(6.0))

    # 18 Limits
    s = new()
    header_bar(s, "Honest limitations (important for healthcare AI)")
    bullets(
        s,
        [
            ("Not a medical device. ", "No clinical trial, no radiologist reader study, no FDA/CE pathway. Classroom / research demo only."),
            ("Dataset bias. ", "Kaggle CXR pneumonia is a known, relatively easy pediatric set. Hospital data will look different (devices, views, adult pathology, COVID, TB)."),
            ("Lung mask is a prior unless a U-Net is provided. ", "FocusScore is still useful, but it is not a radiologist-grade segmentation."),
            ("Single-model agreement is 1.0. ", "A true ensemble needs extra trained checkpoints."),
            ("Shortcuts still possible. ", "Grad-CAM helps us see them; it does not automatically remove dataset leakage."),
        ],
    )

    # 19 Future + conclusion
    s = new()
    header_bar(s, "Conclusion and future work")
    bullets(
        s,
        [
            ("What we built. ", "A full trustworthy pipeline: CNN + temperature scaling + Grad-CAM + FocusScore + MC Dropout + TrustEngine + OOD flag + evaluation plots + Streamlit UI."),
            ("What we showed conceptually. ", "Trustworthy medical AI is a stack of complementary checks, not a single accuracy number."),
            ("Next technical steps. ", "DICOM/PACS integration; multi-class pulmonary disease; a real lung segmentation network; human-in-the-loop reader studies."),
            ("Take-home line. ", "If the model is unsure, unfocused, or uncalibrated, it should say so — that is the difference between a black box and a decision-support system."),
        ],
    )

    # 20 Thanks
    s = new()
    _rect(s, Inches(0), Inches(0), Inches(13.333), Inches(7.5), NAVY)
    _rect(s, Inches(0), Inches(0), Inches(0.18), Inches(7.5), GOLD)
    box = s.shapes.add_textbox(Inches(0.7), Inches(2.0), Inches(12), Inches(1))
    _set_run(_ensure_run(box.text_frame.paragraphs[0]), "Thank you", 44, True, WHITE)
    box = s.shapes.add_textbox(Inches(0.7), Inches(3.1), Inches(12), Inches(2.4))
    tf = box.text_frame
    tf.word_wrap = True
    _set_run(_ensure_run(tf.paragraphs[0]), "Questions from faculty are welcome — especially on calibration, Grad-CAM, and why trust is multiplicative.", 16, False, RGBColor(186, 210, 220))
    p = tf.add_paragraph()
    _set_run(_ensure_run(p), "", 12, False, WHITE)
    p = tf.add_paragraph()
    _set_run(_ensure_run(p), "Team: Goutham Kumar  ·  Adhithiyan C  ·  Vaibhav Pk  ·  Yadarth Sangem", 16, True, GOLD)
    p = tf.add_paragraph()
    _set_run(_ensure_run(p), "Course: Health care Data Analytics", 16, False, WHITE)

    total = len(prs.slides)
    # skip footer on dark title/thanks
    for idx, slide in enumerate(prs.slides, start=1):
        if idx in (1, total):
            continue
        add_footer(slide, idx, total)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT))
    print(f"Wrote {OUT} ({total} slides)")


if __name__ == "__main__":
    build()
