"use client";

import React, { useState, useRef } from "react";
import { useTheme } from "../context/ThemeContext";

export default function UploadView({
  selectedFile,
  setSelectedFile,
  previewUrl,
  setPreviewUrl,
  onAnalyzeAndTransition,
  onSelectSample,
  activeCaseId,
}) {
  const { isDark } = useTheme();
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      processFile(file);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      processFile(file);
    }
  };

  const processFile = (file) => {
    setSelectedFile(file);
    const reader = new FileReader();
    reader.onload = (event) => {
      setPreviewUrl(event.target.result);
    };
    reader.readAsDataURL(file);
  };

  const SAMPLES = [
    {
      id: "bacterial",
      label: "Sample A: Bacterial Lobar Pneumonia",
      code: "CASE A",
      badge: "Consolidation (Positive)",
      badgeColor: "#ef4444",
      desc: "Dense right lower lobe alveolar consolidation with air bronchograms",
    },
    {
      id: "normal",
      label: "Sample B: Normal Healthy Lungs",
      code: "CASE B",
      badge: "Clear Aeration (Negative)",
      badgeColor: "#10b981",
      desc: "Bilateral clear lung fields, sharp costophrenic angles, normal vasculature",
    },
    {
      id: "viral",
      label: "Sample C: Viral Infiltrate",
      code: "CASE C",
      badge: "Interstitial (Positive)",
      badgeColor: "#f59e0b",
      desc: "Diffuse bilateral perihilar reticulonodular interstitial opacities",
    },
    {
      id: "borderline",
      label: "Sample D: Equivocal Borderline",
      code: "CASE D",
      badge: "High Uncertainty (Audit)",
      badgeColor: "#f97316",
      desc: "Retrocardiac shadow with high epistemic variance (σ² = 0.28)",
    },
  ];

  return (
    <div style={{
      position: "relative",
      zIndex: 10,
      width: "100%",
      maxWidth: "920px",
      margin: "0 auto",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: "1.8rem",
      padding: "2rem 1.2rem",
    }}>
      {/* Title & Badge */}
      <div style={{ textAlign: "center" }}>
        <div style={{
          display: "inline-flex",
          alignItems: "center",
          gap: "0.55rem",
          padding: "0.4rem 1.1rem",
          borderRadius: "9999px",
          backgroundColor: "rgba(56, 189, 248, 0.1)",
          border: "1px solid rgba(56, 189, 248, 0.3)",
          color: "#38bdf8",
          fontSize: "0.74rem",
          fontWeight: "700",
          fontFamily: "var(--font-mono)",
          letterSpacing: "0.1em",
          textTransform: "uppercase",
          marginBottom: "1rem",
          boxShadow: "0 0 15px rgba(56, 189, 248, 0.15)",
        }}>
          <span style={{
            width: "7px",
            height: "7px",
            backgroundColor: "#38bdf8",
            borderRadius: "50%",
            boxShadow: "0 0 8px #38bdf8",
          }} />
          CLINICAL PACS CADx RADIOLOGY PORTAL
        </div>

        <h1 style={{
          fontSize: "2.3rem",
          fontWeight: "800",
          color: isDark ? "#f8fafc" : "#0f172a",
          letterSpacing: "-0.02em",
          lineHeight: "1.2",
          textTransform: "uppercase",
        }}>
          Upload Chest Radiograph
        </h1>
        <p style={{
          fontSize: "0.92rem",
          color: isDark ? "#94a3b8" : "#475569",
          marginTop: "0.5rem",
          maxWidth: "620px",
          lineHeight: "1.5",
        }}>
          Submit a posteroanterior (PA) chest radiograph to execute calibrated ResNet-18 inference, 
          Monte Carlo Dropout epistemic variance distribution, and Grad-CAM anatomical saliency mapping.
        </p>
      </div>

      {/* Main Upload Dropzone Container */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        style={{
          width: "100%",
          minHeight: "270px",
          borderRadius: "24px",
          backgroundColor: isDragging 
            ? (isDark ? "rgba(14, 165, 233, 0.15)" : "rgba(14, 165, 233, 0.12)") 
            : (isDark ? "rgba(13, 20, 36, 0.8)" : "rgba(255, 255, 255, 0.9)"),
          backdropFilter: "blur(24px)",
          border: isDragging 
            ? "2px dashed #38bdf8" 
            : (isDark ? "2px dashed rgba(56, 189, 248, 0.3)" : "2px dashed rgba(2, 132, 199, 0.35)"),
          boxShadow: isDragging
            ? "0 0 35px rgba(56, 189, 248, 0.35), 0 20px 40px rgba(0,0,0,0.6)"
            : (isDark ? "0 20px 50px rgba(0, 0, 0, 0.6), inset 0 0 30px rgba(6, 182, 212, 0.05)" : "0 10px 30px rgba(0, 0, 0, 0.06), inset 0 0 30px rgba(14, 165, 233, 0.04)"),
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "2.2rem",
          cursor: "pointer",
          transition: "all 0.25s ease",
          position: "relative",
          overflow: "hidden",
        }}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="image/*"
          style={{ display: "none" }}
        />

        {selectedFile && previewUrl ? (
          /* User Uploaded Image Preview */
          <div style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "1.1rem",
            width: "100%",
          }}>
            <div style={{
              position: "relative",
              width: "190px",
              height: "190px",
              borderRadius: "16px",
              overflow: "hidden",
              border: "2px solid #38bdf8",
              boxShadow: "0 0 30px rgba(56, 189, 248, 0.4)",
              backgroundColor: "#000000",
            }}>
              <img
                src={previewUrl}
                alt="Radiograph Preview"
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
              <div style={{
                position: "absolute",
                top: "6px",
                left: "8px",
                color: "#38bdf8",
                fontSize: "0.62rem",
                fontFamily: "var(--font-mono)",
                fontWeight: "700",
                textShadow: "0 1px 3px rgba(0,0,0,0.9)",
              }}>
                R · PA CHEST
              </div>
              <div style={{
                position: "absolute",
                bottom: 0,
                left: 0,
                right: 0,
                backgroundColor: "rgba(6, 10, 20, 0.88)",
                borderTop: "1px solid rgba(56, 189, 248, 0.3)",
                color: "#38bdf8",
                fontSize: "0.68rem",
                padding: "0.35rem",
                textAlign: "center",
                fontWeight: "700",
                fontFamily: "var(--font-mono)",
                letterSpacing: "0.06em",
              }}>
                ● READY FOR PIPELINE
              </div>
            </div>

            <div style={{ textAlign: "center" }}>
              <strong style={{ fontSize: "0.92rem", color: "#f8fafc", fontFamily: "var(--font-mono)" }}>
                {selectedFile?.name || "Uploaded Radiograph"}
              </strong>
              <div style={{ fontSize: "0.76rem", color: "#94a3b8", marginTop: "4px" }}>
                Click to replace image or drag a new radiograph here
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedFile(null);
                  setPreviewUrl(null);
                }}
                style={{
                  marginTop: "0.6rem",
                  padding: "0.35rem 0.9rem",
                  borderRadius: "8px",
                  backgroundColor: "rgba(239, 68, 68, 0.15)",
                  border: "1px solid rgba(239, 68, 68, 0.35)",
                  color: "#f87171",
                  fontSize: "0.72rem",
                  fontFamily: "var(--font-mono)",
                  fontWeight: "600",
                  cursor: "pointer",
                }}
              >
                ✕ Remove Uploaded File
              </button>
            </div>
          </div>
        ) : (
          /* Clean Upload Placeholder State (No Picture of Lungs) */
          <div style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "1rem",
            textAlign: "center",
          }}>
            <div style={{
              width: "72px",
              height: "72px",
              borderRadius: "22px",
              backgroundColor: "rgba(56, 189, 248, 0.12)",
              border: "1px solid rgba(56, 189, 248, 0.3)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0 0 25px rgba(56, 189, 248, 0.25)",
            }}>
              <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
            </div>

            <div>
              <div style={{ fontSize: "1.1rem", fontWeight: "700", color: "#f8fafc" }}>
                Drag and drop your Chest X-Ray radiograph here
              </div>
              <div style={{ fontSize: "0.8rem", color: "#94a3b8", marginTop: "6px", fontFamily: "var(--font-mono)" }}>
                Standard DICOM / PNG / JPEG / WEBP (Auto-normalized to 224×224)
              </div>
              {activeCaseId && (
                <div style={{
                  display: "inline-block",
                  marginTop: "0.85rem",
                  padding: "0.35rem 0.9rem",
                  borderRadius: "9999px",
                  backgroundColor: "rgba(56, 189, 248, 0.12)",
                  border: "1px solid rgba(56, 189, 248, 0.3)",
                  color: "#38bdf8",
                  fontSize: "0.72rem",
                  fontFamily: "var(--font-mono)",
                  fontWeight: "700",
                }}>
                  ● Selected Benchmark: {SAMPLES.find(s => s.id === activeCaseId)?.label}
                </div>
              )}
            </div>

            <button style={{
              marginTop: "0.4rem",
              padding: "0.65rem 1.6rem",
              borderRadius: "12px",
              backgroundColor: "rgba(56, 189, 248, 0.15)",
              border: "1px solid rgba(56, 189, 248, 0.4)",
              color: "#38bdf8",
              fontSize: "0.84rem",
              fontWeight: "700",
              fontFamily: "var(--font-mono)",
              boxShadow: "0 0 15px rgba(56, 189, 248, 0.2)",
              transition: "all 0.2s ease",
            }}>
              Browse Local Files
            </button>
          </div>
        )}
      </div>

      {/* Or Select Curated Clinical Samples */}
      <div style={{ width: "100%" }}>
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: "0.9rem",
        }}>
          <span style={{
            fontSize: "0.74rem",
            fontWeight: "700",
            color: "#94a3b8",
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            fontFamily: "var(--font-mono)",
          }}>
            Or Select Clinical Benchmark Reference Case:
          </span>
          <span style={{ fontSize: "0.68rem", color: "#38bdf8", fontFamily: "var(--font-mono)" }}>
            ResNet-18 Trained Checkpoint Suite
          </span>
        </div>

        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(2, 1fr)",
          gap: "0.9rem",
        }}>
          {SAMPLES.map((sample) => {
            const isSelected = activeCaseId === sample.id && !selectedFile;
            return (
              <button
                key={sample.id}
                onClick={(e) => {
                  e.stopPropagation();
                  onSelectSample(sample.id);
                }}
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "0.45rem",
                  padding: "0.9rem 1.1rem",
                  borderRadius: "16px",
                  backgroundColor: isSelected 
                    ? (isDark ? "rgba(14, 165, 233, 0.16)" : "rgba(14, 165, 233, 0.12)") 
                    : (isDark ? "rgba(13, 20, 36, 0.75)" : "rgba(255, 255, 255, 0.9)"),
                  backdropFilter: "blur(14px)",
                  border: isSelected 
                    ? "2px solid #38bdf8" 
                    : (isDark ? "1px solid rgba(56, 189, 248, 0.15)" : "1px solid rgba(15, 23, 42, 0.1)"),
                  boxShadow: isSelected 
                    ? "0 0 20px rgba(56, 189, 248, 0.3)" 
                    : (isDark ? "none" : "0 4px 14px rgba(0, 0, 0, 0.04)"),
                  textAlign: "left",
                  transition: "all 0.2s ease",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "0.6rem" }}>
                    <span style={{
                      fontSize: "0.68rem",
                      fontWeight: "800",
                      fontFamily: "var(--font-mono)",
                      color: isDark ? "#38bdf8" : "#0284c7",
                      backgroundColor: isDark ? "rgba(56, 189, 248, 0.15)" : "rgba(2, 132, 199, 0.1)",
                      border: `1px solid ${isDark ? "rgba(56, 189, 248, 0.3)" : "rgba(2, 132, 199, 0.25)"}`,
                      padding: "0.2rem 0.5rem",
                      borderRadius: "6px",
                    }}>
                      {sample.code}
                    </span>
                    <span style={{ fontSize: "0.82rem", fontWeight: "700", color: isDark ? "#f8fafc" : "#0f172a" }}>
                      {sample.label}
                    </span>
                  </div>
                  <span style={{
                    fontSize: "0.65rem",
                    fontWeight: "700",
                    fontFamily: "var(--font-mono)",
                    padding: "0.2rem 0.55rem",
                    borderRadius: "6px",
                    backgroundColor: `${sample.badgeColor}22`,
                    color: sample.badgeColor,
                    border: `1px solid ${sample.badgeColor}55`,
                  }}>
                    {sample.badge}
                  </span>
                </div>
                <p style={{
                  fontSize: "0.72rem",
                  color: isDark ? "#94a3b8" : "#475569",
                  margin: 0,
                  lineHeight: "1.4",
                }}>
                  {sample.desc}
                </p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Primary Action Button: Triggers Blood Flow Transition to Results */}
      <button
        onClick={onAnalyzeAndTransition}
        style={{
          width: "100%",
          padding: "1.05rem 2rem",
          borderRadius: "16px",
          background: "linear-gradient(135deg, #0284c7 0%, #2563eb 50%, #06b6d4 100%)",
          color: "#ffffff",
          fontSize: "0.95rem",
          fontWeight: "800",
          fontFamily: "var(--font-mono)",
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          boxShadow: "0 0 25px rgba(14, 165, 233, 0.45)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "0.75rem",
          cursor: "pointer",
          transition: "transform 0.2s ease, box-shadow 0.2s ease",
          marginTop: "0.5rem",
          border: "1px solid rgba(56, 189, 248, 0.5)",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = "translateY(-2px)";
          e.currentTarget.style.boxShadow = "0 0 35px rgba(14, 165, 233, 0.65)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = "translateY(0px)";
          e.currentTarget.style.boxShadow = "0 0 25px rgba(14, 165, 233, 0.45)";
        }}
      >
        <span>EXECUTE INFERENCE & RUN TRUST ENGINE</span>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <line x1="5" y1="12" x2="19" y2="12"></line>
          <polyline points="12 5 19 12 12 19"></polyline>
        </svg>
      </button>
    </div>
  );
}
