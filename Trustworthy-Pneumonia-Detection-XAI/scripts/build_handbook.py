"""
Generate a professionally formatted, comprehensive PDF handbook for the
Trustworthy Pneumonia Detection XAI project.
Uses TTF fonts for full Unicode support.
"""

from pathlib import Path
from fpdf import FPDF, XPos, YPos

# Windows system fonts with full Unicode support
FONT_DIR  = Path("C:/Windows/Fonts")
F_REG     = str(FONT_DIR / "arial.ttf")
F_BOLD    = str(FONT_DIR / "arialbd.ttf")
F_ITALIC  = str(FONT_DIR / "ariali.ttf")
F_MONO    = str(FONT_DIR / "cour.ttf")
F_MONO_B  = str(FONT_DIR / "courbd.ttf")

# -- colour palette -----------------------------------------------------------
NAVY      = (0,  32,  96)
TEAL      = (0, 128, 128)
GOLD      = (196, 149,  46)
WHITE     = (255, 255, 255)
LIGHT_BG  = (245, 247, 250)
DARK_TEXT = (20,  20,  40)
MID_TEXT  = (60,  60,  80)
CODE_BG   = (30,  30,  50)
CODE_FG   = (200, 220, 255)
WARN_BG   = (255, 243, 205)
WARN_FG   = (120,  80,   0)
RED       = (192,   0,   0)

OUT = Path(__file__).resolve().parent.parent / "docs" / "Project_Handbook_v2.pdf"


# =============================================================================
class HandbookPDF(FPDF):

    def _reg_fonts(self):
        self.add_font("AR",  style="",  fname=F_REG)
        self.add_font("AR",  style="B", fname=F_BOLD)
        self.add_font("AR",  style="I", fname=F_ITALIC)
        self.add_font("CR",  style="",  fname=F_MONO)
        self.add_font("CR",  style="B", fname=F_MONO_B)

    # -------------------------------------------------------------------------
    # Header / Footer
    # -------------------------------------------------------------------------
    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 10, "F")
        self.set_font("AR", "B", 8)
        self.set_text_color(*WHITE)
        self.set_xy(10, 1.5)
        self.cell(0, 6, "Trustworthy Pneumonia Detection XAI  |  Technical Handbook",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*DARK_TEXT)
        self.ln(4)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_fill_color(*NAVY)
        self.rect(0, 285, 210, 12, "F")
        self.set_font("AR", "", 8)
        self.set_text_color(*WHITE)
        self.cell(0, 8, f"Page {self.page_no() - 1}", align="C",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # -------------------------------------------------------------------------
    # Cover page
    # -------------------------------------------------------------------------
    def cover(self):
        self.add_page()
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 297, "F")
        self.set_fill_color(*GOLD)
        self.rect(0, 0, 6, 297, "F")

        self.set_font("AR", "B", 11)
        self.set_text_color(*GOLD)
        self.set_xy(20, 50)
        self.cell(0, 8, "COURSE PROJECT  --  HEALTH CARE DATA ANALYTICS",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("AR", "B", 27)
        self.set_text_color(*WHITE)
        self.set_xy(20, 68)
        self.multi_cell(170, 12, "Trustworthy Deep Learning System\nfor Pneumonia Detection")

        self.set_font("AR", "", 14)
        self.set_text_color(180, 210, 230)
        self.set_xy(20, 110)
        self.multi_cell(170, 7,
            "A calibrated, explainable, and uncertainty-aware AI framework\n"
            "for reliable chest X-ray screening")

        self.set_draw_color(*GOLD)
        self.set_line_width(0.8)
        self.line(20, 135, 190, 135)

        self.set_font("AR", "B", 12)
        self.set_text_color(*GOLD)
        self.set_xy(20, 142)
        self.cell(0, 8, "COMPREHENSIVE TECHNICAL HANDBOOK",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("AR", "", 11)
        self.set_text_color(200, 215, 230)
        self.set_xy(20, 152)
        self.multi_cell(170, 6,
            "This document provides an end-to-end technical reference covering\n"
            "every module, class, function, training procedure, evaluation metric,\n"
            "and system architecture of the XAI pneumonia detection pipeline.")

        self.set_font("AR", "B", 11)
        self.set_text_color(*GOLD)
        self.set_xy(20, 200)
        self.cell(0, 7, "Team Members", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("AR", "B", 13)
        self.set_text_color(*WHITE)
        self.set_xy(20, 209)
        self.cell(0, 8,
                  "Goutham Kumar   .   Adhithiyan C   .   Vaibhav Pk   .   Yadarth Sangem",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font("AR", "I", 10)
        self.set_text_color(150, 175, 200)
        self.set_xy(20, 220)
        self.multi_cell(170, 5,
            "Research prototype for academic purposes only.\n"
            "Not intended for clinical deployment without formal validation.")

        self.set_text_color(*DARK_TEXT)

    # -------------------------------------------------------------------------
    # TOC entry
    # -------------------------------------------------------------------------
    def toc_entry(self, num, title):
        self.set_font("AR", "B", 11)
        self.set_text_color(*TEAL)
        self.cell(12, 7, str(num) + ".", new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.set_text_color(*DARK_TEXT)
        self.set_font("AR", "", 11)
        self.cell(0, 7, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # -------------------------------------------------------------------------
    # Section heading  (starts a new page)
    # -------------------------------------------------------------------------
    def section_heading(self, num, title):
        self.add_page()
        self.set_fill_color(*NAVY)
        self.rect(0, 14, 210, 20, "F")
        self.set_font("AR", "B", 16)
        self.set_text_color(*WHITE)
        self.set_xy(10, 16)
        self.cell(0, 16, f"  {num}.  {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_fill_color(*GOLD)
        self.rect(0, 34, 210, 2, "F")
        self.set_text_color(*DARK_TEXT)
        self.ln(6)

    # -------------------------------------------------------------------------
    # Sub-section heading
    # -------------------------------------------------------------------------
    def sub_heading(self, title, level=2):
        self.ln(3)
        if level == 2:
            self.set_font("AR", "B", 12)
            self.set_text_color(*TEAL)
            self.set_fill_color(*LIGHT_BG)
            self.set_x(10)
            self.cell(190, 8, "   " + title, fill=True,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_fill_color(*TEAL)
            self.rect(10, self.get_y() - 8, 2, 8, "F")
        elif level == 3:
            self.set_font("AR", "B", 11)
            self.set_text_color(*NAVY)
            self.set_x(15)
            self.cell(0, 7, "  >> " + title,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*DARK_TEXT)
        self.ln(1)

    # -------------------------------------------------------------------------
    # Body text
    # -------------------------------------------------------------------------
    def body(self, text, size=10):
        self.set_font("AR", "", size)
        self.set_text_color(*DARK_TEXT)
        self.set_x(15)
        self.multi_cell(180, 5.5, text)
        self.ln(2)

    # -------------------------------------------------------------------------
    # Bullet point
    # -------------------------------------------------------------------------
    def bullet(self, bold_label, text, indent=15):
        self.set_x(indent)
        self.set_fill_color(*TEAL)
        cy = self.get_y() + 2.5
        self.ellipse(indent, cy, 1.8, 1.8, "F")
        self.set_x(indent + 5)
        self.set_font("AR", "B", 10)
        self.set_text_color(*NAVY)
        self.write(5.5, bold_label + "  ")
        self.set_font("AR", "", 10)
        self.set_text_color(*DARK_TEXT)
        self.write(5.5, text)
        self.ln(6)

    # -------------------------------------------------------------------------
    # Code block (dark themed)
    # -------------------------------------------------------------------------
    def code_block(self, code_text, caption=""):
        if caption:
            self.set_font("AR", "I", 8.5)
            self.set_text_color(*MID_TEXT)
            self.set_x(15)
            self.cell(0, 5, "  " + caption, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_fill_color(*CODE_BG)
        x0, y0 = 15, self.get_y()
        lines = code_text.split("\n")
        h_line = 4.5
        total_h = len(lines) * h_line + 6
        self.rect(x0, y0, 180, total_h, "F")
        self.set_fill_color(*TEAL)
        self.rect(x0, y0, 2.5, total_h, "F")
        self.set_font("CR", "", 8)
        self.set_text_color(*CODE_FG)
        self.set_xy(x0 + 6, y0 + 2.5)
        for line in lines:
            self.set_x(x0 + 6)
            self.cell(170, h_line, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*DARK_TEXT)
        self.ln(4)

    # -------------------------------------------------------------------------
    # Info / warning box
    # -------------------------------------------------------------------------
    def info_box(self, text, kind="info"):
        bg  = LIGHT_BG  if kind == "info" else WARN_BG
        fg  = TEAL       if kind == "info" else WARN_FG
        icon = "INFO"   if kind == "info" else "NOTE"
        x0, y0 = 15, self.get_y()
        lines = text.split("\n")
        total_h = max(len(lines) * 5.5, 12) + 8
        self.set_fill_color(*bg)
        self.rect(x0, y0, 180, total_h, "F")
        self.set_fill_color(*fg)
        self.rect(x0, y0, 3.5, total_h, "F")
        self.set_font("AR", "B", 8)
        self.set_text_color(*fg)
        self.set_xy(x0 + 7, y0 + 3)
        self.cell(18, 5, icon + ":", new_x=XPos.RIGHT, new_y=YPos.LAST)
        self.set_font("AR", "", 9.5)
        self.set_text_color(*DARK_TEXT)
        self.set_x(x0 + 26)
        self.multi_cell(150, 5.5, text)
        self.ln(4)

    # -------------------------------------------------------------------------
    # Two-column metric card
    # -------------------------------------------------------------------------
    def metric_card(self, left_label, left_val, right_label, right_val):
        x0 = 15
        y0 = self.get_y()
        w  = 87
        for label, val, dx in [(left_label, left_val, 0), (right_label, right_val, 93)]:
            self.set_fill_color(*LIGHT_BG)
            self.rect(x0 + dx, y0, w, 18, "F")
            self.set_fill_color(*TEAL)
            self.rect(x0 + dx, y0, 2.5, 18, "F")
            self.set_font("AR", "B", 9)
            self.set_text_color(*TEAL)
            self.set_xy(x0 + dx + 6, y0 + 3)
            self.cell(w - 9, 5, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_font("AR", "", 10)
            self.set_text_color(*DARK_TEXT)
            self.set_xy(x0 + dx + 6, y0 + 9)
            self.cell(w - 9, 5, val, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(x0, y0 + 22)
        self.set_text_color(*DARK_TEXT)

    # -------------------------------------------------------------------------
    # Divider
    # -------------------------------------------------------------------------
    def divider(self):
        self.set_draw_color(*TEAL)
        self.set_line_width(0.3)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(3)


# =============================================================================
def build():
    pdf = HandbookPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(10, 14, 10)
    pdf._reg_fonts()

    # == COVER =================================================================
    pdf.cover()

    # == TABLE OF CONTENTS =====================================================
    pdf.add_page()
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 14, 210, 16, "F")
    pdf.set_font("AR", "B", 15)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(10, 16)
    pdf.cell(0, 12, "  TABLE OF CONTENTS",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_fill_color(*GOLD)
    pdf.rect(0, 30, 210, 2, "F")
    pdf.ln(8)

    toc = [
        (1,  "Project Overview & Clinical Motivation"),
        (2,  "System Architecture -- Four Safety Layers"),
        (3,  "Configuration & Hyperparameters  (configs/config.py)"),
        (4,  "Dataset & Data Pipeline  (datasets/)"),
        (5,  "Model Architecture  (models/)"),
        (6,  "Training Pipeline  (training/)"),
        (7,  "Calibration -- Temperature Scaling  (evaluation/)"),
        (8,  "Explainability -- Grad-CAM & FocusScore  (explainability/)"),
        (9,  "Uncertainty -- Monte Carlo Dropout  (explainability/)"),
        (10, "TrustEngine -- Safety Scoring  (explainability/)"),
        (11, "End-to-End Inference Pipeline  (inference/)"),
        (12, "Evaluation Suite  (evaluation/)"),
        (13, "Project Structure & Module Reference"),
        (14, "Limitations & Future Work"),
    ]
    for num, title in toc:
        pdf.toc_entry(num, title)
        pdf.ln(1)

    # == 1. PROJECT OVERVIEW ===================================================
    pdf.section_heading(1, "Project Overview & Clinical Motivation")
    pdf.body(
        "Pneumonia is a life-threatening infection that fills the air sacs of the lungs with "
        "fluid or pus. Chest radiographs (X-rays) remain the most accessible first-line "
        "screening tool globally. Deep learning models have demonstrated radiologist-level "
        "accuracy on this task, but raw accuracy alone is insufficient for safe clinical use."
    )
    pdf.info_box(
        "The core thesis: A model that is accurate but uninterpretable, "
        "overconfident, and cannot detect its own failures is NOT safe for healthcare. "
        "We add four verifiable safety layers on top of the base classifier.",
        kind="note"
    )
    pdf.body(
        "For every chest X-ray, the system produces FOUR outputs instead of just a label:"
    )
    pdf.bullet("Predicted class:", "NORMAL or PNEUMONIA.")
    pdf.bullet("Calibrated confidence:", "An honest probability reflecting real-world accuracy.")
    pdf.bullet("Visual explanation:", "A Grad-CAM heatmap showing WHERE the model looked.")
    pdf.bullet("Trust assessment:",
               "A numerical TrustScore, trust level (High/Medium/Low), and an OOD flag.")

    pdf.sub_heading("Dataset")
    pdf.body(
        "Kaggle Chest X-Ray Pneumonia dataset (Guangzhou Women and Children's Medical Center). "
        "5,863 paediatric frontal chest X-rays in two classes: NORMAL and PNEUMONIA. "
        "Split into train/val/test with zero leakage by prepare_dataset.py."
    )
    pdf.metric_card(
        "Training Split", "~5,216 images",
        "Test Split", "~624 images"
    )

    # == 2. SYSTEM ARCHITECTURE ================================================
    pdf.section_heading(2, "System Architecture -- Four Safety Layers")
    pdf.body(
        "The pipeline is structured as a stack of four independently verifiable safety layers. "
        "They are combined by the TrustEngine using a MULTIPLICATIVE formula, so a failure "
        "in any single layer collapses the trust score."
    )
    pdf.sub_heading("Layer 1: Classification")
    pdf.body("CNN backbone (default: ResNet18) maps a 224x224 RGB X-ray to a single logit -> sigmoid -> P(Pneumonia). Decision threshold: 0.5.")
    pdf.sub_heading("Layer 2: Calibration (Probability Honesty)")
    pdf.body("Temperature Scaling post-processes the logit so 80% confidence means ~80% of such cases are truly positive.")
    pdf.sub_heading("Layer 3: Explainability (Grad-CAM + FocusScore)")
    pdf.body("Grad-CAM produces a spatial heatmap. FocusScore measures whether attention falls inside the lungs.")
    pdf.sub_heading("Layer 4: Uncertainty (Monte Carlo Dropout)")
    pdf.body("30 stochastic forward passes with Dropout ON. High variance = model is guessing or image is out-of-distribution.")
    pdf.code_block(
        "TrustScore = Calibrated_Confidence\n"
        "           x FocusScore\n"
        "           x (1 - Uncertainty)\n"
        "           x AgreementScore\n\n"
        "All terms clipped to [0, 1]. A single failed check collapses TrustScore.",
        caption="The Multiplicative Trust Formula:"
    )

    # == 3. CONFIGURATION ======================================================
    pdf.section_heading(3, "Configuration & Hyperparameters (configs/config.py)")
    pdf.body(
        "All paths, model choices, and training hyperparameters are declared in one central "
        "file. Changing a value here propagates automatically to every module in the pipeline."
    )
    pdf.code_block(
        "MODEL_TYPE         = 'resnet18'    # backbone: custom/resnet18/vgg16/densenet121/efficientnet_b0\n"
        "IMAGE_SIZE         = 224           # input px (width = height)\n"
        "BATCH_SIZE         = 32\n"
        "NUM_EPOCHS         = 15\n"
        "LEARNING_RATE      = 1e-4          # Adam optimizer lr\n"
        "NUM_WORKERS        = 0             # DataLoader workers\n"
        "DEFAULT_MC_SAMPLES = 30            # MC Dropout stochastic passes\n"
        "DEFAULT_ECE_BINS   = 10            # calibration histogram bins\n"
        "HEATMAP_THRESHOLD  = 0.4           # Grad-CAM binarisation threshold\n"
        "MODEL_WEIGHTS_NAME = 'chestxray_best.pt'\n"
        "CALIBRATOR_NAME    = 'temperature_scaling.pt'",
        caption="configs/config.py -- key constants"
    )
    pdf.sub_heading("ensure_dirs()")
    pdf.body(
        "Called at every script entry-point. Creates MODEL_SAVE_DIR, OUTPUT_DIR, FIGURES_DIR, "
        "LOGS_DIR, PREDICTIONS_DIR, and REPORTS_DIR with mkdir(parents=True, exist_ok=True)."
    )

    # == 4. DATASET ============================================================
    pdf.section_heading(4, "Dataset & Data Pipeline (datasets/)")
    pdf.sub_heading("ChestXRayDataset  (datasets/dataset.py)")
    pdf.body(
        "Subclasses torch.utils.data.Dataset. Walks data/train, data/val, or data/test "
        "looking for NORMAL/ and PNEUMONIA/ subdirectories. Stores (path, label) tuples."
    )
    pdf.code_block(
        "CLASS_NAMES  = ['NORMAL', 'PNEUMONIA']   labels: 0, 1\n"
        "\n__init__(root, transform, extension=('.jpg','.jpeg','.png'))\n"
        "  _load_samples()  -- walks class folders, appends (path, int_label)\n"
        "  __len__()        -- len(self.samples)\n"
        "  __getitem__(i)   -- opens PIL image, applies transform, returns (tensor, label, path)",
        caption="ChestXRayDataset interface"
    )
    pdf.sub_heading("get_transforms()  (datasets/transforms.py)")
    pdf.body("Returns torchvision transform pipelines per split:")
    pdf.bullet("Training:", "RandomHorizontalFlip + RandomRotation(10deg) + Resize(224) + ToTensor + Normalize(ImageNet)")
    pdf.bullet("Val/Test:", "Resize(224) + CenterCrop(224) + ToTensor + Normalize(ImageNet)")
    pdf.body("ImageNet mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]")

    pdf.sub_heading("get_dataloaders()  (datasets/preprocessing.py)")
    pdf.body(
        "Factory wrapping ChestXRayDataset in DataLoader objects. Training: shuffle=True. "
        "Val/Test: shuffle=False. Optional max_samples truncates splits for quick demos."
    )
    pdf.sub_heading("split_kaggle_dataset()  (datasets/split_dataset.py)")
    pdf.body(
        "Copies raw Kaggle images into train/val/test at a 70-15-15 stratified split. "
        "Seeded (default 42) for reproducibility. Prevents train/val leakage."
    )

    # == 5. MODEL ARCHITECTURE =================================================
    pdf.section_heading(5, "Model Architecture (models/)")
    pdf.body(
        "Five backbone architectures, all sharing the same interface: single logit output, "
        "sigmoid activation, Dropout(0.5) before the classification head (required for MC Dropout)."
    )

    pdf.sub_heading("5.1  ChestXRayCNN -- Custom CNN  (models/cnn_model.py)")
    pdf.code_block(
        "Input:  (B, 3, 224, 224)\n"
        "Block1: Conv(3->32, 3x3) + BN + ReLU + MaxPool2d  -> (B, 32, 112, 112)\n"
        "Block2: Conv(32->64)     + BN + ReLU + MaxPool2d  -> (B, 64, 56, 56)\n"
        "Block3: Conv(64->128)    + BN + ReLU + MaxPool2d  -> (B, 128, 28, 28)\n"
        "Block4: Conv(128->256)   + BN + ReLU + MaxPool2d  -> (B, 256, 14, 14)\n"
        "Block5: Conv(256->512)   + BN + ReLU + MaxPool2d  -> (B, 512, 7, 7)\n"
        "AdaptiveAvgPool2d(1,1)                            -> (B, 512, 1, 1)\n"
        "Head:  Flatten -> Linear(512,256) -> ReLU -> Dropout(0.5) -> Linear(256,1)\n"
        "Output: (B,1) logit  [sigmoid -> P(Pneumonia)]",
        caption="ChestXRayCNN forward pass"
    )

    pdf.sub_heading("5.2  ResNet18 (DEFAULT)  -- get_resnet18()")
    pdf.body(
        "Pre-trained ImageNet weights (IMAGENET1K_V1). Original fc(512->1000) replaced with "
        "Dropout(0.5) -> Linear(512, 1). Grad-CAM target: model.layer4[-1].conv2."
    )
    pdf.code_block(
        "model.fc = nn.Sequential(\n"
        "    nn.Dropout(p=0.5),\n"
        "    nn.Linear(512, 1)\n"
        ")   # num_classes=1 -> sigmoid for binary",
        caption="ResNet18 head replacement"
    )

    pdf.sub_heading("5.3  VGG16  -- get_vgg16()")
    pdf.body("Pre-trained. classifier[6] replaced: Linear(4096,1000) -> Linear(4096,1). "
             "Grad-CAM target: last Conv2d in model.features.")

    pdf.sub_heading("5.4  DenseNet121  -- get_densenet121()")
    pdf.body("Pre-trained. classifier replaced: Dropout(0.5) -> Linear(1024,1). "
             "Grad-CAM target: model.features.denseblock4.denselayer16.conv2.")

    pdf.sub_heading("5.5  EfficientNet-B0  -- get_efficientnet_b0()")
    pdf.body("Pre-trained. classifier[1] replaced: Linear(1280,1). "
             "Grad-CAM target: model.features[-1][0].")

    pdf.sub_heading("5.6  build_model()  -- Factory function")
    pdf.body(
        "Accepts model_type string, pretrained bool, num_classes int. "
        "Returns the correct nn.Module. All models output a single logit for binary classification."
    )

    pdf.sub_heading("5.7  get_last_conv_layer_for_model()")
    pdf.body(
        "Given a model + model_type, returns the exact nn.Module for Grad-CAM hook registration. "
        "Each architecture has a different layer path to the final spatial convolutional layer."
    )

    pdf.sub_heading("5.8  Ensemble Agreement  (models/ensemble.py)")
    pdf.code_block(
        "majority_vote(class_indices) -> (majority_class, agreement_score)\n"
        "  agreement_score = majority_count / total_models\n"
        "  Range: [0.5, 1.0] for binary. 1.0 means unanimous agreement.\n\n"
        "agreement_from_probabilities(probs, threshold=0.5) -> (class, score)\n"
        "  Threshold each P(Pneumonia) -> binary vote -> calls majority_vote()",
        caption="models/ensemble.py interface"
    )

    # == 6. TRAINING ===========================================================
    pdf.section_heading(6, "Training Pipeline (training/)")

    pdf.sub_heading("Loss Function")
    pdf.body(
        "nn.BCEWithLogitsLoss (Binary Cross-Entropy with Logits). Combines sigmoid + BCE in "
        "one numerically stable operation. Raw logit in, no sigmoid applied DURING training."
    )
    pdf.code_block(
        "Loss = -[ y*log(sigmoid(z)) + (1-y)*log(1-sigmoid(z)) ]\n"
        "where z = logit, y in {0=NORMAL, 1=PNEUMONIA}",
        caption="BCE with Logits formula"
    )

    pdf.sub_heading("Optimiser")
    pdf.body(
        "Adam with lr=1e-4, beta1=0.9, beta2=0.999, eps=1e-8. Chosen for fast convergence "
        "on medical imaging and robustness to sparse gradients."
    )

    pdf.sub_heading("train_one_epoch()  (training/trainer.py)")
    pdf.code_block(
        "model.train()   # enables BN updates + Dropout\n"
        "for images, labels, _ in loader:\n"
        "    optimizer.zero_grad()\n"
        "    logits = model(images).squeeze(-1)\n"
        "    loss = BCEWithLogitsLoss(logits, labels.float())\n"
        "    loss.backward()\n"
        "    optimizer.step()\n"
        "    probs = sigmoid(logits.detach())\n"
        "    preds = (probs >= 0.5).long()\n"
        "    accumulate loss + correct count\n"
        "return avg_loss, accuracy",
        caption="train_one_epoch() pseudocode"
    )

    pdf.sub_heading("evaluate_epoch()  (training/trainer.py)")
    pdf.body(
        "Identical loop with model.eval() and @torch.no_grad(). No weight updates. "
        "Returns avg_loss, accuracy on validation set."
    )

    pdf.sub_heading("main()  (training/train.py) -- Full Training Orchestration")
    pdf.bullet("1. Parse CLI args:", "--model_type, --epochs, --batch_size, --lr, --seed, --quick.")
    pdf.bullet("2. set_seed(42):", "Seeds Python random, NumPy, PyTorch, and CUDA for reproducibility.")
    pdf.bullet("3. Build DataLoaders:", "get_dataloaders() for train/val splits.")
    pdf.bullet("4. Build model:", "build_model(model_type, pretrained=True, num_classes=1).")
    pdf.bullet("5. Training loop:", "train_one_epoch -> evaluate_epoch -> save if val_acc improves.")
    pdf.bullet("6. Best checkpoint:", "Saved as checkpoints/chestxray_best.pt with model_state_dict + model_type.")
    pdf.bullet("7. model_config.txt:", "Records model_type for inference-time backbone selection.")
    pdf.bullet("8. Plots:", "training_curves.png (loss + accuracy vs epoch) saved to outputs/.")

    pdf.info_box(
        "--quick flag: sets epochs=2 and max_samples=128 per split. CPU-friendly demo "
        "that completes in under a minute. Full training (15 epochs) recommended on GPU.",
        kind="note"
    )

    # == 7. CALIBRATION ========================================================
    pdf.section_heading(7, "Calibration -- Temperature Scaling (evaluation/calibration.py)")
    pdf.body(
        "Standard neural networks are overconfident: they output 0.97 confidence even when "
        "essentially guessing. Temperature Scaling is a post-hoc method that aligns predicted "
        "confidence with empirical accuracy WITHOUT changing the class ranking or re-training."
    )

    pdf.sub_heading("The Formula")
    pdf.code_block(
        "p_calibrated = sigmoid(logit / T)\n\n"
        "T > 1 : softens overconfident predictions  (flattens sigmoid curve)\n"
        "T < 1 : sharpens underconfident predictions (steepens sigmoid curve)\n"
        "T = 1 : no change\n\n"
        "Accuracy unchanged because relative ranking of logits is preserved.",
        caption="Temperature Scaling formula"
    )

    pdf.sub_heading("TemperatureScaling class")
    pdf.code_block(
        "temperature = nn.Parameter(torch.tensor(1.5))  # initial T, learnable\n\n"
        "forward(logits)        -> logits / clamp(T, min=1e-4)\n"
        "calibrate_logits()     -> same as forward\n"
        "calibrate_probs(logits)-> sigmoid(logits / T)   # for binary\n"
        "property T             -> float value of current temperature",
        caption="TemperatureScaling class interface"
    )

    pdf.sub_heading("fit_temperature() -- How T is Learned")
    pdf.body("The CNN is completely FROZEN. Only the scalar T is optimised.")
    pdf.bullet("Step 1:", "Run entire validation set through frozen model, collect all logits + labels.")
    pdf.bullet("Step 2:", "optimizer = L-BFGS([temperature.temperature], lr=0.01, max_iter=50).")
    pdf.bullet("Step 3:", "Closure: loss = BCELoss(sigmoid(logits/T), labels). Call optimizer.step(closure).")
    pdf.bullet("Returns:", "Fitted TemperatureScaling module saved to checkpoints/temperature_scaling.pt.")
    pdf.body("L-BFGS is chosen because this is a 1-parameter problem and converges in very few iterations.")

    pdf.sub_heading("Expected Calibration Error (ECE)")
    pdf.code_block(
        "ECE = sum over bins b:\n"
        "    |b| / N  *  |mean_confidence(b) - mean_accuracy(b)|\n\n"
        "n_bins = 10 (equal-width bins from 0 to 1)\n"
        "Lower is better. ECE = 0 means perfect calibration.\n"
        "We report ECE before and after temperature scaling to demonstrate improvement.",
        caption="ECE formula (evaluation/reliability.py: compute_ece)"
    )

    # == 8. EXPLAINABILITY =====================================================
    pdf.section_heading(8, "Explainability -- Grad-CAM & FocusScore (explainability/)")

    pdf.sub_heading("8.1  Grad-CAM Algorithm  (explainability/gradcam.py)")
    pdf.body("Gradient-weighted Class Activation Mapping (Selvaraju et al., 2017). Produces a "
             "coarse spatial heatmap showing which regions drove the predicted class score.")
    pdf.code_block(
        "Step 1: Forward pass through model\n"
        "        Hook captures activation maps A^k at target_layer  (C x H' x W')\n\n"
        "Step 2: Backward pass of class score\n"
        "        Hook captures gradients dY/dA^k at target_layer\n\n"
        "Step 3: Channel weights (global average pooled gradients):\n"
        "        alpha^k = (1/H'W') * sum_{i,j}  dY/dA^k_{ij}\n\n"
        "Step 4: Weighted sum + ReLU (only positive contributions):\n"
        "        CAM = ReLU( sum_k  alpha^k * A^k )\n\n"
        "Step 5: cv2.resize to 224x224,  min-max normalise to [0, 1]\n"
        "        Returns np.float32 array (H, W)",
        caption="Grad-CAM computation -- GradCAM.generate()"
    )

    pdf.sub_heading("GradCAM class methods", level=3)
    pdf.code_block(
        "__init__(model, target_layer)     -- stores refs, initialises hook list\n"
        "_save_activation(module,in,out)  -- forward hook: saves output.detach()\n"
        "_save_gradient(module,gi,go)     -- backward hook: saves go[0].detach()\n"
        "_register_hooks()                -- attaches forward + full_backward hooks\n"
        "_remove_hooks()                  -- removes all hooks after generation\n"
        "generate(input_tensor, target_class=None) -> np.ndarray (H,W) in [0,1]\n\n"
        "generate_gradcam_heatmap()       -- functional (stateless) API wrapper\n"
        "overlay_heatmap(heatmap, img)    -- cv2 jet colormap blend, alpha=0.5",
        caption="GradCAM class full interface"
    )

    pdf.sub_heading("Binary vs. Multi-class Grad-CAM", level=3)
    pdf.body(
        "Binary (single logit): target_class=1 -> backward on output.sum(). "
        "target_class=0 -> backward on (-output).sum(). "
        "Multi-class (2 outputs): one-hot mask selects the target class score before backprop."
    )

    pdf.sub_heading("8.2  FocusScore  (explainability/attention_maps.py)")
    pdf.body(
        "Turns the qualitative heatmap into a quantifiable constraint. A model can produce "
        "a visually plausible heatmap that focuses on the wrong anatomy. FocusScore penalises this."
    )
    pdf.code_block(
        "FocusScore = Area(GradCAM_binary AND LungMask) / Area(GradCAM_binary)\n\n"
        "GradCAM_binary = (heatmap >= HEATMAP_THRESHOLD)   [HEATMAP_THRESHOLD=0.4]\n"
        "LungMask       = binary mask of lung region\n\n"
        "Range [0, 1]:\n"
        "  ~ 1.0  -> attention fully inside lungs  (good)\n"
        "  ~ 0.0  -> attention almost entirely outside lungs  (dangerous shortcut)",
        caption="focus_overlap_score() formula"
    )

    pdf.sub_heading("Lung Mask Sources", level=3)
    pdf.bullet("Geometric Prior (default):",
               "Central rectangle y=[15%,90%], x=[10%,90%] of image. "
               "Approximates typical frontal CXR lung field position.")
    pdf.bullet("SimpleUNet (optional):",
               "Lightweight 3-encoder/3-decoder U-Net. Can be loaded from a pretrained "
               "checkpoint (e.g. trained on JSRT/Montgomery). Falls back to geometric prior "
               "automatically if no checkpoint is supplied.")

    pdf.sub_heading("SimpleUNet Architecture", level=3)
    pdf.code_block(
        "Encoder:    enc1(in->32) -> pool -> enc2(32->64) -> pool -> enc3(64->128) -> pool\n"
        "Bottleneck: (128->256)\n"
        "Decoder:    up3 + concat(enc3) -> dec3(256->128)\n"
        "            up2 + concat(enc2) -> dec2(128->64)\n"
        "            up1 + concat(enc1) -> dec1(64->32)\n"
        "Output:     Conv2d(32->1, kernel=1) -> sigmoid -> threshold @ 0.5\n"
        "Each block: Conv(3x3)+BN+ReLU repeated twice",
        caption="SimpleUNet architecture (attention_maps.py)"
    )

    # == 9. UNCERTAINTY ========================================================
    pdf.section_heading(9, "Uncertainty -- Monte Carlo Dropout (explainability/uncertainty.py)")
    pdf.body(
        "Reference: Gal & Ghahramani (2016), 'Dropout as a Bayesian Approximation' "
        "(arXiv:1506.02142). Dropout at inference time approximates sampling from a "
        "posterior distribution over model weights. Variance of samples is a proxy for "
        "epistemic (model) uncertainty."
    )

    pdf.sub_heading("enable_dropout()  /  disable_dropout()")
    pdf.body(
        "enable_dropout(): iterates model.modules(), calls .train() on every nn.Dropout "
        "and nn.Dropout2d -- re-enables stochasticity while leaving BatchNorm in eval mode "
        "(preserving running statistics). Call AFTER model.eval()."
    )
    pdf.body("disable_dropout(): calls .eval() on Dropout layers -- fully deterministic mode.")

    pdf.sub_heading("predict_with_uncertainty()  -- Core Function")
    pdf.code_block(
        "predict_with_uncertainty(model, image_tensor, n_samples=30, device):\n\n"
        "  1. model.eval()          # freeze BN, base dropout state\n"
        "  2. enable_dropout(model) # re-enable ONLY dropout layers\n"
        "  3. with torch.no_grad(): # no gradient computation needed\n"
        "         for _ in range(n_samples):\n"
        "             logits = model(image_tensor)\n"
        "             prob   = sigmoid(logits).item()\n"
        "             probabilities.append(prob)\n"
        "  4. model.eval()          # fully disable dropout\n"
        "  5. samples = np.array(probabilities)\n"
        "     return {\n"
        "       'mean_prediction': mean(samples),   # raw confidence\n"
        "       'variance':        var(samples),    # THE uncertainty score\n"
        "       'std':             std(samples),\n"
        "       'samples':         samples           # (n_samples,) array\n"
        "     }",
        caption="predict_with_uncertainty() -- exact procedure"
    )

    pdf.sub_heading("Interpreting Variance")
    pdf.bullet("variance < 0.01  (Low):",
               "Consistent predictions. Model is confident and stable.")
    pdf.bullet("0.01 <= variance < 0.05  (Medium):",
               "Some variation. Case may be ambiguous. Human review recommended.")
    pdf.bullet("variance >= 0.05  (High):",
               "Model is essentially guessing. Output must NOT be trusted. OOD highly likely.")

    pdf.sub_heading("MCDropoutPredictor class")
    pdf.body(
        "Stateful wrapper: stores model, n_samples, and device. "
        "predict(image_tensor) delegates to predict_with_uncertainty(). "
        "uncertainty_level(variance) returns 'low', 'medium', or 'high' label."
    )
    pdf.sub_heading("ood_flag_from_confidence_uncertainty()")
    pdf.body("Delegates to TrustEngine.detect_ood(). "
             "Returns True (UNRELIABLE) if calibrated_confidence < 0.6 AND variance > 0.03.")

    # == 10. TRUST ENGINE ======================================================
    pdf.section_heading(10, "TrustEngine -- Safety Scoring (explainability/trustscore.py)")
    pdf.body(
        "The TrustEngine is the unifying safety arbiter. It combines all signals into a single "
        "scalar TrustScore and produces a human-readable trust level."
    )

    pdf.sub_heading("compute_trust_score_with_uncertainty()  -- Current Formula")
    pdf.code_block(
        "confidence_component = max(p, 1-p)  # reward confidence in EITHER class\n"
        "trust = confidence_component\n"
        "      * clip(focus_score, 0, 1)\n"
        "      * (1 - clip(uncertainty, 0, 1))\n"
        "return clip(trust, 0, 1)\n\n"
        "Why multiplicative: a single failed check (focus=0.1 or uncertainty=0.9)\n"
        "collapses the score. Addition would let high confidence hide bad focus.",
        caption="compute_trust_score_with_uncertainty()"
    )

    pdf.sub_heading("TrustEngine.compute_trust_score()  -- Full Formula")
    pdf.code_block(
        "trust = max(p, 1-p)\n"
        "      * clip(focus_score, 0, 1)\n"
        "      * (1 - clip(uncertainty, 0, 1))\n"
        "      * clip(agreement_score, 0, 1)   # adds ensemble signal\n"
        "return clip(trust, 0, 1)",
        caption="TrustEngine.compute_trust_score() -- adds AgreementScore"
    )

    pdf.sub_heading("get_trust_level()  -- Decision Logic")
    pdf.code_block(
        "if uncertainty > 0.3 or focus_score < 0.35:   return 'low'\n"
        "if confidence > 0.8 and uncertainty < 0.1:    return 'high'\n"
        "if 0.6 <= confidence <= 0.8\n"
        "   or 0.1 <= uncertainty <= 0.3:              return 'medium'\n"
        "else:                                          return 'medium'",
        caption="Trust level decision tree"
    )

    pdf.sub_heading("TrustEngine.detect_ood()  -- OOD / UNRELIABLE Flag")
    pdf.code_block(
        "TrustEngineConfig: confidence_threshold=0.6, uncertainty_threshold=0.03\n\n"
        "detect_ood(calibrated_confidence, uncertainty):\n"
        "    return (calibrated_confidence < 0.6) AND (uncertainty > 0.03)",
        caption="OOD detection rule"
    )
    pdf.body(
        "This is a conservative heuristic gate, not a learned OOD model. "
        "It catches low-confidence + high-variance cases -- typical of inputs the CNN "
        "has never seen in training (blurry scans, non-CXR images, extreme noise)."
    )

    pdf.sub_heading("summarize()  -- All-in-one Convenience")
    pdf.code_block(
        "engine.summarize(calibrated_confidence, focus_score, uncertainty, agreement_score)\n"
        "    -> {'trust_score': float, 'ood_flag': bool}",
        caption="TrustEngine.summarize()"
    )

    # == 11. INFERENCE =========================================================
    pdf.section_heading(11, "End-to-End Inference Pipeline (inference/)")
    pdf.body(
        "run_pipeline() is the master integration function. It sequentially applies "
        "all four safety layers and returns a rich output dictionary plus a 4-panel figure."
    )

    pdf.sub_heading("load_and_transform_image()")
    pdf.code_block(
        "load_and_transform_image(image_path, device):\n"
        "    img_pil = Image.open(path).convert('RGB')\n"
        "    transform = Resize(224) + ToTensor + Normalize(ImageNet_mean, ImageNet_std)\n"
        "    img_tensor = transform(img_pil).unsqueeze(0).to(device)  # (1,3,224,224)\n"
        "    img_np = denormalize(tensor) * 255  # uint8 RGB for visualisation\n"
        "    return img_tensor, img_np",
        caption="Image loading and normalisation"
    )

    pdf.sub_heading("run_pipeline()  -- Step-by-Step")
    pdf.bullet("Step 1 -- Setup:",
               "ensure_dirs(). Detect CUDA/CPU. load_model_and_calibrator() from checkpoints/. "
               "get_last_conv_layer_for_model() for Grad-CAM target.")
    pdf.bullet("Step 2 -- Load image:",
               "load_and_transform_image() -> img_tensor (1,3,224,224) + img_np (RGB uint8).")
    pdf.bullet("Step 3 -- MC Dropout:",
               "predict_with_uncertainty(model, img_tensor, n_samples=30). "
               "Returns mean_prediction, variance, std, samples array.")
    pdf.bullet("Step 4 -- Calibrated confidence:",
               "Deterministic forward pass (model.eval(), no_grad). "
               "calibrator.calibrate_probs(logits) -> calibrated_prob.")
    pdf.bullet("Step 5 -- Grad-CAM:",
               "GradCAM(model, target_layer).generate(img_tensor, target_class). "
               "overlay_heatmap(heatmap, img_np, alpha=0.5) -> RGB overlay.")
    pdf.bullet("Step 6 -- FocusScore:",
               "LungSegmenter.segment(img_tensor) -> lung_mask. "
               "focus_overlap_score(heatmap, lung_mask, threshold=0.4) -> focus_score.")
    pdf.bullet("Step 7 -- Ensemble:",
               "If auxiliary DenseNet/EfficientNet checkpoints are supplied, run inference, "
               "append to ensemble_probs. agreement_from_probabilities() -> agreement_score.")
    pdf.bullet("Step 8 -- TrustEngine:",
               "engine.summarize(calibrated_prob, focus_score, variance, agreement_score). "
               "get_trust_level() -> 'High', 'Medium', or 'Low'.")
    pdf.bullet("Step 9 -- Output:",
               "Returns dict with all metrics. build_inference_figure() creates a 4-panel plot "
               "(original X-ray | Grad-CAM overlay | MC histogram | metrics summary). "
               "Saved to outputs/<name>_uncertainty_gradcam.png.")

    pdf.sub_heading("Output Dictionary Keys")
    pdf.code_block(
        "{\n"
        "  'predicted_class':        'NORMAL' or 'PNEUMONIA',\n"
        "  'raw_confidence':          float  (MC Dropout mean),\n"
        "  'calibrated_confidence':   float  (temperature-scaled),\n"
        "  'uncertainty_score':       float  (MC Dropout variance),\n"
        "  'focus_score':             float  (Grad-CAM x lung overlap),\n"
        "  'agreement_score':         float  (ensemble majority fraction),\n"
        "  'trust_score':             float  [0,1],\n"
        "  'trust_level':             'High' / 'Medium' / 'Low',\n"
        "  'ood_flag':                bool   (True = UNRELIABLE),\n"
        "  'overlay_path':            str    (path to saved figure)\n"
        "}",
        caption="run_pipeline() return dictionary"
    )

    # == 12. EVALUATION ========================================================
    pdf.section_heading(12, "Evaluation Suite (evaluation/)")

    pdf.sub_heading("12.1  Classification Metrics  (evaluation/metrics.py)")
    pdf.bullet("Accuracy:", "Fraction of correct predictions = (TP+TN) / N.")
    pdf.bullet("Precision:", "TP / (TP+FP). Fraction of predicted-positive that are true-positive.")
    pdf.bullet("Recall (Sensitivity):", "TP / (TP+FN). Fraction of true-positive cases detected.")
    pdf.bullet("F1-Score:", "2 * Precision * Recall / (Precision + Recall). Handles class imbalance.")
    pdf.bullet("Confusion Matrix:", "2x2 [[TN,FP],[FN,TP]] via sklearn.")

    pdf.sub_heading("12.2  Calibration Metrics  (evaluation/reliability.py)")
    pdf.bullet("compute_ece(probs, labels, n_bins=10):",
               "Expected Calibration Error. Reported before and after temperature scaling.")
    pdf.bullet("reliability_diagram():",
               "Bar chart of accuracy (blue bars) vs confidence (red line) per bin. "
               "A well-calibrated model hugs the diagonal. Returns (ECE, bin_accs, bin_confs).")

    pdf.sub_heading("12.3  Full Evaluation  (evaluation/evaluate.py)")
    pdf.bullet("Standard pass:", "Accuracy, Precision, Recall, F1, confusion matrix on test set.")
    pdf.bullet("Calibration:", "ECE raw vs calibrated. Plots reliability diagram.")
    pdf.bullet("--trust_eval flag:",
               "Per-image MC Dropout (20 samples), Grad-CAM, FocusScore, TrustEngine. "
               "Reports mean/std FocusScore, mean/std TrustScore, and OOD detection accuracy.")
    pdf.bullet("Outputs:", "evaluation_results.png (CM + reliability), trustscore_distribution.png.")

    pdf.sub_heading("12.4  Faculty Report  (evaluation/faculty_report.py)")
    pdf.body(
        "Generates a 12-panel figure pack including: training curves, confusion matrix, "
        "reliability diagrams (before/after calibration), Grad-CAM gallery, FocusScore "
        "distribution, TrustScore distribution, uncertainty histogram, and MC sample traces."
    )

    # == 13. PROJECT STRUCTURE =================================================
    pdf.section_heading(13, "Project Structure & Module Reference")
    pdf.code_block(
        "project_root/\n"
        "+-- configs/\n"
        "|   +-- config.py               Central hyperparameters and paths\n"
        "+-- datasets/\n"
        "|   +-- dataset.py              ChestXRayDataset (PyTorch Dataset)\n"
        "|   +-- preprocessing.py        get_dataloaders() factory\n"
        "|   +-- transforms.py           get_transforms() with augmentation\n"
        "|   +-- split_dataset.py        Train/val/test splitting utilities\n"
        "+-- models/\n"
        "|   +-- cnn_model.py            All 5 backbones + build_model() factory\n"
        "|   +-- ensemble.py             majority_vote() + agreement_from_probabilities()\n"
        "+-- training/\n"
        "|   +-- train.py                Training CLI entry point\n"
        "|   +-- trainer.py              train_one_epoch() + evaluate_epoch()\n"
        "+-- evaluation/\n"
        "|   +-- calibrate.py            Fit temperature scalar (CLI)\n"
        "|   +-- calibration.py          TemperatureScaling class + fit_temperature()\n"
        "|   +-- evaluate.py             Full test evaluation (CLI)\n"
        "|   +-- metrics.py              Accuracy/Precision/Recall/F1\n"
        "|   +-- reliability.py          compute_ece() + reliability_diagram()\n"
        "|   +-- confusion_matrix.py     plot_confusion_matrix()\n"
        "|   +-- faculty_report.py       12-panel figure pack\n"
        "+-- explainability/\n"
        "|   +-- gradcam.py              GradCAM class + overlay_heatmap()\n"
        "|   +-- attention_maps.py       LungSegmenter + focus_overlap_score()\n"
        "|   +-- uncertainty.py          predict_with_uncertainty() + MCDropoutPredictor\n"
        "|   +-- trustscore.py           TrustEngine + TrustAnalyzer + get_trust_level()\n"
        "|   +-- visualization.py        build_inference_figure() 4-panel plot\n"
        "+-- inference/\n"
        "|   +-- inference.py            run_pipeline() master function\n"
        "|   +-- predict.py              CLI entry point\n"
        "|   +-- api.py                  Programmatic API wrapper\n"
        "+-- scripts/\n"
        "|   +-- build_faculty_ppt.py    PowerPoint generator\n"
        "|   +-- build_handbook.py       This PDF handbook generator\n"
        "|   +-- demo.py                 Faculty demo environment checker\n"
        "|   +-- run_pipeline.py         Full pipeline runner\n"
        "+-- utils/\n"
        "|   +-- io.py                   load_model_and_calibrator()\n"
        "|   +-- helpers.py              matplotlib backend utils\n"
        "|   +-- seed.py                 set_seed()\n"
        "|   +-- logger.py              get_logger()\n"
        "+-- tests/\n"
        "|   +-- test_core.py            Unit tests (ResNet dropout, trust bounds)\n"
        "|   +-- test_imports.py         Smoke tests for all imports\n"
        "+-- notebooks/\n"
        "|   +-- colab_faculty_demo.ipynb\n"
        "+-- checkpoints/\n"
        "|   +-- chestxray_best.pt       Best model weights\n"
        "|   +-- temperature_scaling.pt  Fitted calibrator\n"
        "+-- outputs/                    All generated figures and plots\n"
        "+-- docs/                       Presentations and handbooks",
        caption="Complete project directory structure"
    )

    # == 14. LIMITATIONS =======================================================
    pdf.section_heading(14, "Limitations & Future Work")
    pdf.info_box(
        "IMPORTANT: This is a research prototype for academic purposes ONLY. "
        "It has not undergone clinical validation, reader studies, or regulatory review. "
        "It must NOT be used for real patient care decisions.",
        kind="note"
    )

    pdf.sub_heading("Known Limitations")
    pdf.bullet("Dataset bias:",
               "Kaggle CXR is paediatric-only. Adult pathology, COVID-19, TB, and "
               "non-standard equipment will degrade performance significantly.")
    pdf.bullet("Geometric lung prior:",
               "FocusScore uses a static rectangular mask unless a U-Net is provided. "
               "Not radiologist-grade segmentation.")
    pdf.bullet("OOD detection is a heuristic:",
               "The (confidence<0.6 AND variance>0.03) rule can miss subtle OOD cases. "
               "Not a learned density estimator.")
    pdf.bullet("Single-model ensemble:",
               "Without extra checkpoints, AgreementScore is always 1.0 -- no signal.")
    pdf.bullet("JPEG/PNG only:",
               "Clinical systems use DICOM. No pydicom integration currently.")
    pdf.bullet("Shortcut learning:",
               "Grad-CAM reveals shortcuts but does NOT prevent them during training.")

    pdf.sub_heading("Future Work")
    pdf.bullet("Real lung segmentation:", "Train SimpleUNet on JSRT/Montgomery datasets.")
    pdf.bullet("DICOM/PACS integration:", "Add pydicom support for clinical workflows.")
    pdf.bullet("Multi-class disease:", "Extend to 14-class NIH ChestX-ray14.")
    pdf.bullet("Reader study:", "Validate TrustScore utility with radiologists.")
    pdf.bullet("Dedicated OOD detector:", "Replace heuristic with learned anomaly detection.")
    pdf.bullet("Larger ensembles:", "Train 3-5 diverse architectures for meaningful agreement.")

    # == SAVE ==================================================================
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    print(f"\nHandbook written -> {OUT}  ({pdf.page_no()-1} pages)")


if __name__ == "__main__":
    build()
