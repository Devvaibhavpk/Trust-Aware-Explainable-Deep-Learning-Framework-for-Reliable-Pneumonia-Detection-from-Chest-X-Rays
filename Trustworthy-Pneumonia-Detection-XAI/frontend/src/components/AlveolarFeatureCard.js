"use client";

import React from "react";

export default function AlveolarFeatureCard({ activeCase }) {
  const isPneumonia = activeCase?.predicted_class?.toLowerCase().includes("pneumonia");
  const focusPercent = activeCase?.focus_score ? Math.round(activeCase.focus_score * 100) : 94;

  return (
    <div className="pacs-placard" style={{
      width: "100%",
      height: "100%",
      padding: "0.5rem",
      display: "flex",
      flexDirection: "column",
      position: "relative",
      overflow: "hidden",
      borderRadius: "20px",
    }}>
      {/* Background Microscopic Tissue Scan */}
      <div style={{
        position: "relative",
        width: "100%",
        height: "100%",
        minHeight: "180px",
        borderRadius: "16px",
        overflow: "hidden",
      }}>
        <img
          src={activeCase?.tissueView || "/assets/alveolar_tissue.jpg"}
          alt="Alveolar Sac Infiltration"
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            filter: "brightness(0.9) contrast(1.1)",
          }}
        />

        {/* Floating Badge 1 (Top Left) */}
        <div style={{
          position: "absolute",
          top: "12px",
          left: "12px",
          backgroundColor: isPneumonia ? "rgba(220, 38, 38, 0.85)" : "rgba(16, 185, 129, 0.85)",
          backdropFilter: "blur(8px)",
          color: "#ffffff",
          fontSize: "0.68rem",
          fontWeight: "700",
          fontFamily: "var(--font-mono)",
          padding: "0.3rem 0.65rem",
          borderRadius: "9999px",
          boxShadow: "0 4px 14px rgba(0, 0, 0, 0.4)",
          display: "flex",
          alignItems: "center",
          gap: "5px",
        }}>
          <span style={{ width: "5px", height: "5px", borderRadius: "50%", backgroundColor: "#ffffff" }} />
          <span>{isPneumonia ? "FOCAL CONSOLIDATION" : "CLEAR AERATION"}</span>
        </div>

        {/* Floating Badge 2 (Top Right) */}
        <div style={{
          position: "absolute",
          top: "12px",
          right: "12px",
          backgroundColor: "rgba(15, 23, 42, 0.9)",
          backdropFilter: "blur(8px)",
          border: "1px solid rgba(56, 189, 248, 0.4)",
          color: "#38bdf8",
          fontSize: "0.68rem",
          fontWeight: "700",
          fontFamily: "var(--font-mono)",
          padding: "0.3rem 0.65rem",
          borderRadius: "9999px",
          boxShadow: "0 4px 12px rgba(0, 0, 0, 0.4)",
        }}>
          {focusPercent}% LUNG FOCUS
        </div>

        {/* Bottom Dark Gradient Label */}
        <div style={{
          position: "absolute",
          bottom: "0",
          left: "0",
          right: "0",
          padding: "0.6rem 0.85rem",
          background: "linear-gradient(to top, rgba(6, 9, 17, 0.95) 0%, transparent 100%)",
          color: "#ffffff",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontFamily: "var(--font-mono)",
        }}>
          <span style={{ fontSize: "0.68rem", fontWeight: "700", color: "#f8fafc" }}>
            ALVEOLAR PARENCHYMA
          </span>
          <span style={{ fontSize: "0.62rem", color: isPneumonia ? "#f87171" : "#34d399" }}>
            {isPneumonia ? "Active Infiltrate" : "Normal Capillaries"}
          </span>
        </div>
      </div>
    </div>
  );
}
