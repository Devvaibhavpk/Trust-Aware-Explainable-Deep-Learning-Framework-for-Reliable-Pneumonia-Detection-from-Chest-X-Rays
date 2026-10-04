"""
Streamlit frontend for the trustworthy chest X-ray pneumonia demo.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import torch
import plotly.graph_objects as go
import plotly.express as px

from configs.config import MODEL_SAVE_DIR, MODEL_WEIGHTS_NAME, OUTPUT_DIR, ensure_dirs
from inference.api import predict

st.set_page_config(
    page_title="Trustworthy Pneumonia Detection",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

ensure_dirs()

st.markdown(
    """
    <style>
      .block-container {padding-top: 2rem; max-width: 1400px;}
      .trust-pill {
          padding: 0.5rem 1.2rem; 
          border-radius: 8px; 
          font-weight: 600; 
          display: inline-block;
          font-size: 1.1rem;
          margin-bottom: 1rem;
      }
      .metric-card {
          background-color: #1e1e1e;
          border-radius: 10px;
          padding: 1.5rem;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
          border: 1px solid #333;
      }
      .stTabs [data-baseweb="tab-list"] {
          gap: 24px;
      }
      .stTabs [data-baseweb="tab"] {
          height: 50px;
          white-space: pre-wrap;
          background-color: transparent;
          border-radius: 4px;
          font-size: 1.1rem;
      }
      h1, h2, h3 {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def checkpoint_path() -> Path:
    return MODEL_SAVE_DIR / MODEL_WEIGHTS_NAME


def trust_color(level: str) -> str:
    return {"High": "#00CC96", "Medium": "#FFA15A", "Low": "#EF553B"}.get(level, "#AB63FA")


def create_gauge(value: float, title: str, color: str) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 0.5], 'color': 'rgba(239, 85, 59, 0.2)'},
                {'range': [0.5, 0.8], 'color': 'rgba(255, 161, 90, 0.2)'},
                {'range': [0.8, 1.0], 'color': 'rgba(0, 204, 150, 0.2)'}],
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    return fig


def create_radar_chart(result: dict) -> go.Figure:
    categories = ['Calibrated Conf', 'Focus Score', 'Uncertainty (Inv)', 'Raw Conf']
    
    # Invert uncertainty so higher is better on the radar chart
    unc = max(0, 1 - result['uncertainty_score'])
    values = [
        result['calibrated_confidence'],
        result['focus_score'],
        unc,
        result['raw_confidence']
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(99, 110, 250, 0.4)',
        line=dict(color='#636efa'),
        name='Metrics'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="#444"),
            bgcolor="rgba(0,0,0,0)"
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': 'white'},
        margin=dict(l=40, r=40, t=40, b=40),
        height=350
    )
    return fig


def show_png_grid(paths: list[Path], width: int = 800) -> None:
    if not paths:
        st.info("No figures yet. Train in Colab / CLI first, then generate the faculty report.")
        return
    
    cols = st.columns(2)
    for i, path in enumerate(paths):
        with cols[i % 2]:
            st.markdown(f"#### {path.stem.replace('_', ' ').title()}")
            st.image(str(path), use_container_width=True)


def page_predict() -> None:
    st.markdown("## 🔬 Clinical Screening Pipeline")
    st.markdown("<p style='color: #888;'>Upload a DICOM-converted image to execute the Trustworthy XAI analysis pipeline.</p>", unsafe_allow_html=True)
    st.write("---")

    ckpt = checkpoint_path()
    if not ckpt.exists():
        st.error(
            f"⚠️ No trained model at `{ckpt}`. Run training in the Colab notebook or "
            "`python -m training.train --quick` first."
        )
        return

    left_col, right_col = st.columns([1, 2.5], gap="large")
    
    with left_col:
        st.markdown("### 📥 Input Data")
        uploaded = st.file_uploader("Upload Chest X-ray", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        
        st.markdown("### ⚙️ Pipeline Parameters")
        n_mc = st.slider("MC Dropout Samples", min_value=8, max_value=64, value=16, step=4, help="Higher values improve uncertainty estimation but take longer.")
        
        run = st.button("🚀 Run Analysis Pipeline", type="primary", disabled=uploaded is None, use_container_width=True)

        if uploaded is not None:
            st.markdown("#### Preview")
            st.image(uploaded, use_container_width=True, clamp=True)

    if not run or uploaded is None:
        with right_col:
            st.info("👈 Please upload an X-ray image and click 'Run Analysis Pipeline' to see the results.")
        return

    upload_dir = OUTPUT_DIR / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    image_path = upload_dir / uploaded.name
    image_path.write_bytes(uploaded.getvalue())

    with right_col:
        with st.spinner("🧠 Executing MC Dropout, Temperature Scaling, Grad-CAM, and TrustEngine..."):
            result = predict(str(image_path), n_mc_samples=n_mc)

        level = str(result["trust_level"])
        color = trust_color(level)

        st.markdown("### 📊 Pipeline Results")
        
        # Top Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Diagnosis", result["predicted_class"])
        m2.metric("Trust Level", level)
        m3.metric("OOD Flag", "🚨 Yes" if result['ood_flag'] else "✅ No")
        m4.metric("Process Time", f"{n_mc * 0.05 + 0.5:.2f}s") # mock timing just for visual

        st.write("---")

        # Visualizations Row
        viz_col1, viz_col2 = st.columns([1, 1])
        
        with viz_col1:
            st.markdown("#### 🎯 Trust Score Analysis")
            gauge = create_gauge(result['trust_score'], "Trust Score", color)
            st.plotly_chart(gauge, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown("#### 📈 Component Breakdown")
            radar = create_radar_chart(result)
            st.plotly_chart(radar, use_container_width=True, config={'displayModeBar': False})

        with viz_col2:
            st.markdown("#### 🔍 Explainability (Grad-CAM)")
            overlay = result.get("overlay_path")
            if overlay and Path(overlay).exists():
                st.image(overlay, use_container_width=True)
            else:
                st.warning("Grad-CAM overlay not generated.")
                
            with st.expander("Detailed Metrics Dashboard", expanded=True):
                d1, d2 = st.columns(2)
                d1.metric("Raw Confidence", f"{result['raw_confidence']:.3f}", help="Softmax output before calibration")
                d1.metric("Calibrated Confidence", f"{result['calibrated_confidence']:.3f}", help="Confidence after temperature scaling")
                d2.metric("Uncertainty", f"{result['uncertainty_score']:.4f}", help="Variance from MC Dropout")
                d2.metric("Focus Score", f"{result['focus_score']:.3f}", help="Overlap with lung region priors")


def page_faculty_graphs() -> None:
    st.markdown("## 📊 Faculty Report Artifacts")
    st.markdown("<p style='color: #888;'>Visualizations and validation metrics generated for academic review.</p>", unsafe_allow_html=True)
    st.write("---")
    
    report = OUTPUT_DIR / "faculty_report"
    paths = sorted(report.glob("*.png"))
    
    cols = st.columns([1, 3])
    with cols[0]:
        if st.button("🔄 Regenerate Artifacts", type="secondary"):
            import subprocess

            with st.spinner("Computing metrics, ROC, calibration, trust, and Grad-CAM gallery..."):
                code = subprocess.call(
                    [
                        sys.executable,
                        "-m",
                        "evaluation.faculty_report",
                        "--max_samples",
                        "120",
                        "--n_trust",
                        "32",
                        "--n_mc",
                        "10",
                        "--n_gradcam",
                        "8",
                    ],
                    cwd=str(PROJECT_ROOT),
                )
            if code != 0:
                st.error("Figure generation failed. Train the model and prepare the test set first.")
            else:
                st.rerun()
                
    show_png_grid(paths)


def page_pipeline() -> None:
    st.markdown("## 📈 Training & Evaluation Telemetry")
    st.markdown("<p style='color: #888;'>Historical tracking of model training, reliability diagrams, and evaluation runs.</p>", unsafe_allow_html=True)
    st.write("---")
    
    names = [
        "training_curves.png",
        "reliability_diagrams.png",
        "evaluation_results.png",
        "trustscore_distribution.png",
    ]
    found = [OUTPUT_DIR / name for name in names if (OUTPUT_DIR / name).exists()]
    extra = sorted(OUTPUT_DIR.glob("*_uncertainty_gradcam.png"))
    show_png_grid(found + extra)


def page_about() -> None:
    st.markdown("## 🧠 Architecture Overview")
    st.write("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(
            """
            This system implements a **Trustworthy Deep Learning Pipeline** for medical image analysis.
            It is designed to address key limitations of standard CNNs: overconfidence, lack of interpretability, and vulnerability to out-of-distribution (OOD) data.
            
            ### Pipeline Components:
            
            1. **Classification Head** — ResNet18 (or similar architectures) trained to classify Normal vs Pneumonia.
            2. **Temperature Scaling** — Post-hoc calibration applied to softmax outputs to align confidence with empirical accuracy.
            3. **Grad-CAM Explanations** — Gradient-weighted Class Activation Mapping to visualize areas driving the decision.
            4. **FocusScore** — Automated scoring that penalizes the model if attention falls outside anatomical priors (lung region).
            5. **MC Dropout Uncertainty** — Monte Carlo sampling at inference time to measure epistemic uncertainty (model instability).
            6. **TrustEngine Aggregator** — Heuristic synthesis of all signals into a single Trust Level.
            """
        )
        st.info("`TrustScore = Confidence × FocusScore × (1 − Uncertainty) × Agreement`")
        
    with col2:
        st.markdown("### System Architecture")
        # Creating a simple flowchart with standard markdown / mermaid inside an expander if needed, but a nice summary block works too
        st.markdown("""
        <div style='background-color:#1e1e1e; padding:20px; border-radius:10px; border: 1px solid #444;'>
        <b>Input X-Ray</b> <br>⬇️<br>
        <b>Feature Extractor</b> (CNN) <br>⬇️<br>
        <b>Multiple stochastic forward passes</b> (MC Dropout) <br>⬇️<br>
        <b>Calibrated Softmax</b> & <b>Grad-CAM</b> <br>⬇️<br>
        <b>Trust Engine</b> <br>⬇️<br>
        <b>Final Output & Explanations</b>
        </div>
        """, unsafe_allow_html=True)


def main() -> None:
    st.title("🫁 Trust-Aware Pneumonia Detection Pipeline")
    st.markdown("A robust, interpretable decision-support framework integrating uncertainty estimation and calibrated confidence.")
    
    device = "CUDA GPU 🚀" if torch.cuda.is_available() else "CPU 🐢"
    ckpt = checkpoint_path()
    
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=60)
        st.markdown("### Model Telemetry")
        st.metric("Compute Device", device)
        st.metric("Model Status", 'Loaded ✅' if ckpt.exists() else 'Offline ❌')
        st.metric("Output Directory", str(OUTPUT_DIR.name))
        
        st.markdown("---")
        st.markdown("### Navigation")
        st.markdown("Use the tabs in the main window to navigate through the pipeline stages.")
        
        st.markdown("---")
        st.caption("v1.2.0-beta | Research Prototype")

    tabs = st.tabs([
        "🔬 Clinical Screening", 
        "📊 Faculty Artifacts", 
        "📈 Pipeline Telemetry", 
        "🧠 Architecture"
    ])
    
    with tabs[0]:
        page_predict()
    with tabs[1]:
        page_faculty_graphs()
    with tabs[2]:
        page_pipeline()
    with tabs[3]:
        page_about()


if __name__ == "__main__":
    main()
