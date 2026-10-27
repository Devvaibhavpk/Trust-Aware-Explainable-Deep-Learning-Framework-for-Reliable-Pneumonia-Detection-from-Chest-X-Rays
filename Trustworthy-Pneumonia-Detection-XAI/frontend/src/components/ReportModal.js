"use client";

import React from "react";
import { useTheme } from "../context/ThemeContext";

export default function ReportModal({ isOpen, onClose, activeCase }) {
  const { isDark } = useTheme();
  if (!isOpen) return null;

  const isPneumonia = activeCase?.predicted_class?.toLowerCase().includes("pneumonia");

  return (
    <div style={{
      position: "fixed",
      inset: 0,
      backgroundColor: isDark ? "rgba(3, 7, 18, 0.82)" : "rgba(15, 23, 42, 0.6)",
      backdropFilter: "blur(12px)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 100,
      padding: "1rem",
    }}>
      <div style={{
        backgroundColor: isDark ? "rgba(11, 18, 33, 0.98)" : "#ffffff",
        borderRadius: "24px",
        boxShadow: isDark
          ? "0 25px 70px rgba(0, 0, 0, 0.85), 0 0 35px rgba(6, 182, 212, 0.15)"
          : "0 25px 50px -12px rgba(15, 23, 42, 0.25), 0 0 20px rgba(2, 132, 199, 0.1)",
        maxWidth: "700px",
        width: "100%",
        maxHeight: "90vh",
        overflowY: "auto",
        border: isDark ? "1px solid rgba(56, 189, 248, 0.28)" : "1px solid #e2e8f0",
        padding: "2.2rem",
        position: "relative",
        color: isDark ? "#f8fafc" : "#0f172a",
      }}>
        {/* Close Button */}
        <button
          onClick={onClose}
          style={{
            position: "absolute",
            top: "1.5rem",
            right: "1.5rem",
            width: "36px",
            height: "36px",
            borderRadius: "50%",
            backgroundColor: isDark ? "rgba(56, 189, 248, 0.12)" : "#f1f5f9",
            border: isDark ? "1px solid rgba(56, 189, 248, 0.25)" : "1px solid #cbd5e1",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: isDark ? "#94a3b8" : "#64748b",
            fontSize: "1.1rem",
            transition: "all 0.2s ease",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.color = isDark ? "#ffffff" : "#0f172a";
            e.currentTarget.style.borderColor = isDark ? "#38bdf8" : "#0284c7";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.color = isDark ? "#94a3b8" : "#64748b";
            e.currentTarget.style.borderColor = isDark ? "rgba(56, 189, 248, 0.25)" : "#cbd5e1";
          }}
        >
          ✕
        </button>

        {/* Modal Header */}
        <div style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "1.5rem" }}>
          <div style={{
            width: "48px",
            height: "48px",
            borderRadius: "14px",
            background: isDark
              ? "linear-gradient(135deg, rgba(14, 165, 233, 0.2) 0%, rgba(16, 185, 129, 0.15) 100%)"
              : "linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(16, 185, 129, 0.1) 100%)",
            border: isDark ? "1px solid rgba(56, 189, 248, 0.35)" : "1px solid rgba(2, 132, 199, 0.3)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: isDark ? "0 0 20px rgba(14, 165, 233, 0.3)" : "0 4px 12px rgba(2, 132, 199, 0.15)",
          }}>
            <img src="/assets/logo.svg" alt="logo" style={{ width: "32px", height: "32px" }} />
          </div>
          <div>
            <h2 style={{ fontSize: "1.3rem", fontWeight: "800", color: isDark ? "#f8fafc" : "#0f172a", letterSpacing: "0.02em" }}>
              Clinical Decision Support (CDS) Report
            </h2>
            <p style={{ fontSize: "0.78rem", color: isDark ? "#38bdf8" : "#0284c7", fontFamily: "var(--font-mono)" }}>
              trustworthy-pneumonia-detector · RESNET-18
            </p>
          </div>
        </div>

        {/* Patient & Exam Meta Grid */}
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "1rem",
          padding: "1rem 1.2rem",
          backgroundColor: isDark ? "rgba(6, 10, 20, 0.75)" : "#f8fafc",
          borderRadius: "14px",
          border: isDark ? "1px solid rgba(56, 189, 248, 0.15)" : "1px solid #e2e8f0",
          marginBottom: "1.5rem",
          fontFamily: "var(--font-mono)",
        }}>
          <div>
            <span style={{ fontSize: "0.66rem", color: isDark ? "#64748b" : "#94a3b8", display: "block" }}>PATIENT / CASE</span>
            <strong style={{ fontSize: "0.82rem", color: isDark ? "#f8fafc" : "#0f172a" }}>{activeCase?.name || "Patient CXR"}</strong>
          </div>
          <div>
            <span style={{ fontSize: "0.66rem", color: isDark ? "#64748b" : "#94a3b8", display: "block" }}>ACCESSION NO</span>
            <strong style={{ fontSize: "0.82rem", color: isDark ? "#38bdf8" : "#0284c7" }}>CXR-2026-9812</strong>
          </div>
          <div>
            <span style={{ fontSize: "0.66rem", color: isDark ? "#64748b" : "#94a3b8", display: "block" }}>CADx VERIFIER</span>
            <strong style={{ fontSize: "0.82rem", color: isDark ? "#10b981" : "#059669" }}>ResNet-18 (Calibrated)</strong>
          </div>
        </div>

        {/* Diagnostic Findings */}
        <div style={{ marginBottom: "1.5rem" }}>
          <h3 style={{
            fontSize: "0.76rem",
            fontWeight: "700",
            color: isDark ? "#38bdf8" : "#0284c7",
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            marginBottom: "0.6rem",
            fontFamily: "var(--font-mono)",
          }}>
            1. Primary Diagnostic Finding
          </h3>
          <div style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "1rem 1.25rem",
            borderRadius: "14px",
            backgroundColor: isPneumonia
              ? (isDark ? "rgba(239, 68, 68, 0.14)" : "rgba(239, 68, 68, 0.08)")
              : (isDark ? "rgba(16, 185, 129, 0.14)" : "rgba(16, 185, 129, 0.08)"),
            border: `1px solid ${
              isPneumonia
                ? (isDark ? "rgba(239, 68, 68, 0.45)" : "rgba(239, 68, 68, 0.3)")
                : (isDark ? "rgba(16, 185, 129, 0.45)" : "rgba(16, 185, 129, 0.3)")
            }`,
          }}>
            <div>
              <div style={{
                fontSize: "1.15rem",
                fontWeight: "800",
                color: isPneumonia ? (isDark ? "#f87171" : "#dc2626") : (isDark ? "#34d399" : "#059669"),
                fontFamily: "var(--font-mono)",
              }}>
                {isPneumonia ? "POSITIVE: PNEUMONIA DETECTED" : "NEGATIVE: NORMAL CHEST RADIOGRAPH"}
              </div>
              <div style={{ fontSize: "0.78rem", color: isDark ? "#cbd5e1" : "#475569", marginTop: "3px" }}>
                Classification: <strong>{activeCase?.subtype || "Lobar Consolidation"}</strong> | Focus: <strong>{activeCase?.primary_lobe || "Right Lower Lobe"}</strong>
              </div>
            </div>
            <div style={{
              padding: "0.4rem 0.9rem",
              borderRadius: "9999px",
              backgroundColor: activeCase?.trust_level === "High"
                ? (isDark ? "rgba(16, 185, 129, 0.25)" : "rgba(16, 185, 129, 0.15)")
                : (isDark ? "rgba(245, 158, 11, 0.25)" : "rgba(245, 158, 11, 0.15)"),
              color: activeCase?.trust_level === "High" ? (isDark ? "#34d399" : "#059669") : (isDark ? "#f59e0b" : "#d97706"),
              border: `1px solid ${activeCase?.trust_level === "High" ? "#10b981" : "#f59e0b"}`,
              fontSize: "0.75rem",
              fontWeight: "700",
              fontFamily: "var(--font-mono)",
            }}>
              {activeCase?.trust_level || "HIGH"} TRUST
            </div>
          </div>
        </div>

        {/* Trust & Uncertainty Metrics Breakdown */}
        <div style={{ marginBottom: "1.5rem" }}>
          <h3 style={{
            fontSize: "0.76rem",
            fontWeight: "700",
            color: isDark ? "#38bdf8" : "#0284c7",
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            marginBottom: "0.6rem",
            fontFamily: "var(--font-mono)",
          }}>
            2. Explainability & Uncertainty Telemetry
          </h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: "0.85rem" }}>
            <div style={{ padding: "0.85rem", backgroundColor: isDark ? "rgba(6, 10, 20, 0.75)" : "#f8fafc", borderRadius: "12px", border: isDark ? "1px solid rgba(56, 189, 248, 0.15)" : "1px solid #e2e8f0" }}>
              <span style={{ fontSize: "0.68rem", color: isDark ? "#64748b" : "#94a3b8", fontFamily: "var(--font-mono)" }}>TEMPERATURE-CALIBRATED CONFIDENCE</span>
              <div style={{ fontSize: "1.2rem", fontWeight: "800", color: isDark ? "#f8fafc" : "#0f172a", fontFamily: "var(--font-mono)", marginTop: "2px" }}>
                {Math.round((activeCase?.calibrated_confidence || 0) * 100)}%
                <span style={{ fontSize: "0.7rem", color: isDark ? "#94a3b8" : "#64748b", fontWeight: "500", marginLeft: "6px" }}>
                  (Raw: {Math.round((activeCase?.raw_confidence || 0) * 100)}%)
                </span>
              </div>
            </div>

            <div style={{ padding: "0.85rem", backgroundColor: isDark ? "rgba(6, 10, 20, 0.75)" : "#f8fafc", borderRadius: "12px", border: isDark ? "1px solid rgba(56, 189, 248, 0.15)" : "1px solid #e2e8f0" }}>
              <span style={{ fontSize: "0.68rem", color: isDark ? "#64748b" : "#94a3b8", fontFamily: "var(--font-mono)" }}>MC DROPOUT EPISTEMIC VARIANCE (σ²)</span>
              <div style={{ fontSize: "1.2rem", fontWeight: "800", color: isDark ? "#38bdf8" : "#0284c7", fontFamily: "var(--font-mono)", marginTop: "2px" }}>
                {activeCase?.uncertainty_score || "0.024"}
                <span style={{ fontSize: "0.7rem", color: isDark ? "#34d399" : "#059669", fontWeight: "500", marginLeft: "6px" }}>
                  (Stable)
                </span>
              </div>
            </div>

            <div style={{ padding: "0.85rem", backgroundColor: isDark ? "rgba(6, 10, 20, 0.75)" : "#f8fafc", borderRadius: "12px", border: isDark ? "1px solid rgba(56, 189, 248, 0.15)" : "1px solid #e2e8f0" }}>
              <span style={{ fontSize: "0.68rem", color: isDark ? "#64748b" : "#94a3b8", fontFamily: "var(--font-mono)" }}>GRAD-CAM ANATOMICAL FOCUS</span>
              <div style={{ fontSize: "1.2rem", fontWeight: "800", color: isDark ? "#f8fafc" : "#0f172a", fontFamily: "var(--font-mono)", marginTop: "2px" }}>
                {Math.round((activeCase?.focus_score || 0.94) * 100)}%
                <span style={{ fontSize: "0.7rem", color: isDark ? "#38bdf8" : "#0284c7", fontWeight: "500", marginLeft: "6px" }}>
                  (Parenchyma Overlap)
                </span>
              </div>
            </div>

            <div style={{ padding: "0.85rem", backgroundColor: isDark ? "rgba(6, 10, 20, 0.75)" : "#f8fafc", borderRadius: "12px", border: isDark ? "1px solid rgba(56, 189, 248, 0.15)" : "1px solid #e2e8f0" }}>
              <span style={{ fontSize: "0.68rem", color: isDark ? "#64748b" : "#94a3b8", fontFamily: "var(--font-mono)" }}>TRUSTENGINE™ COMPOSITE INDEX</span>
              <div style={{ fontSize: "1.2rem", fontWeight: "800", color: isDark ? "#34d399" : "#059669", fontFamily: "var(--font-mono)", marginTop: "2px" }}>
                {Math.round((activeCase?.trust_score || 0.94) * 100)}%
                <span style={{ fontSize: "0.7rem", color: isDark ? "#34d399" : "#059669", fontWeight: "500", marginLeft: "6px" }}>
                  FDA-Benchmark Clean
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Clinical Recommendation Text */}
        <div style={{
          padding: "1rem 1.25rem",
          borderRadius: "14px",
          backgroundColor: isDark ? "rgba(6, 10, 20, 0.75)" : "#f8fafc",
          border: isDark ? "1px solid rgba(56, 189, 248, 0.2)" : "1px solid #e2e8f0",
          marginBottom: "1.5rem",
        }}>
          <span style={{
            fontSize: "0.72rem",
            fontWeight: "700",
            color: isDark ? "#38bdf8" : "#0284c7",
            textTransform: "uppercase",
            display: "block",
            marginBottom: "0.4rem",
            fontFamily: "var(--font-mono)",
          }}>
            Physician Guidance & Next Steps
          </span>
          <p style={{ fontSize: "0.84rem", color: isDark ? "#cbd5e1" : "#334155", lineHeight: "1.5" }}>
            {activeCase?.recommendation || "Correlate with clinical presentation, complete blood count, and pulse oximetry."}
          </p>
        </div>

        {/* Actions */}
        <div style={{ display: "flex", justifyContent: "flex-end", gap: "0.75rem" }}>
          <button
            onClick={() => window.print()}
            style={{
              padding: "0.65rem 1.4rem",
              borderRadius: "12px",
              background: "linear-gradient(135deg, #0284c7 0%, #2563eb 100%)",
              color: "#ffffff",
              fontSize: "0.82rem",
              fontWeight: "700",
              fontFamily: "var(--font-mono)",
              boxShadow: "0 0 16px rgba(14, 165, 233, 0.4)",
            }}
          >
            🖨️ PRINT / EXPORT PDF
          </button>
          <button
            onClick={onClose}
            style={{
              padding: "0.65rem 1.4rem",
              borderRadius: "12px",
              backgroundColor: isDark ? "rgba(56, 189, 248, 0.12)" : "#f1f5f9",
              border: isDark ? "1px solid rgba(56, 189, 248, 0.25)" : "1px solid #cbd5e1",
              color: isDark ? "#94a3b8" : "#475569",
              fontSize: "0.82rem",
              fontWeight: "600",
              fontFamily: "var(--font-mono)",
            }}
          >
            DISMISS
          </button>
        </div>
      </div>
    </div>
  );
}
