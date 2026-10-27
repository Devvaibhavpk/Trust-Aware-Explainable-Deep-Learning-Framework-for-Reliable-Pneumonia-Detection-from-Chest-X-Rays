"use client";

import React, { useState } from "react";
import { useTheme } from "../context/ThemeContext";

export default function AnatomyViewer({
  activeCase,
  selectedLobe,
  setSelectedLobe,
  currentView = "anatomy",
  setCurrentView,
  onUploadClick,
}) {
  const { isDark } = useTheme();
  const [hoveredLobe, setHoveredLobe] = useState(null);
  const [isInverted, setIsInverted] = useState(false);

  const isPneumonia = activeCase?.predicted_class?.toLowerCase().includes("pneumonia");

  // Anatomical lobe paths for SVG rendering (viewBox 0 0 500 480)
  const LOBES = [
    {
      id: "RUL",
      name: "Right Upper Lobe (RUL)",
      path: "M 195,85 C 160,85 125,120 115,175 C 150,185 190,185 225,170 C 228,135 220,95 195,85 Z",
      focal: false,
    },
    {
      id: "RML",
      name: "Right Middle Lobe (RML)",
      path: "M 115,185 C 105,230 110,265 120,290 C 155,275 195,275 225,270 C 228,230 226,190 225,175 C 185,185 145,185 115,185 Z",
      focal: false,
    },
    {
      id: "RLL",
      name: "Right Lower Lobe (RLL)",
      path: "M 122,295 C 128,350 145,405 175,418 C 210,412 225,370 228,275 C 190,280 155,280 122,295 Z",
      focal: isPneumonia, // Primary consolidation site
    },
    {
      id: "LUL",
      name: "Left Upper Lobe (LUL)",
      path: "M 305,85 C 335,85 375,120 385,175 C 388,230 365,275 340,300 C 315,280 285,250 275,170 C 275,135 285,95 305,85 Z",
      focal: false,
    },
    {
      id: "LLL",
      name: "Left Lower Lobe (LLL)",
      path: "M 342,305 C 365,280 385,245 385,185 C 392,250 385,350 350,418 C 315,412 285,380 278,310 C 295,315 320,315 342,305 Z",
      focal: false,
    },
  ];

  const activeLobeId = hoveredLobe || selectedLobe;
  const activeLobeData = activeCase?.anatomical_lobes?.[activeLobeId] || null;

  // Normalize view string
  const activeMode = currentView === "cxr" ? "cxr" : (currentView === "gradcam" ? "gradcam" : "anatomy");

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      width: "100%",
    }}>
      {/* Central Interactive Display Area (NO background box - completely transparent) */}
      <div style={{
        position: "relative",
        width: "100%",
        maxWidth: activeMode === "gradcam" ? "450px" : "410px",
        height: "380px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "transparent",
      }}>
        {activeMode === "anatomy" ? (
          /* Subtle, Transparent Anatomical Vector Lungs */
          <div
            className="animate-breathe"
            style={{
              position: "relative",
              width: "100%",
              height: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <svg
              viewBox="0 0 500 480"
              style={{
                width: "100%",
                height: "100%",
                overflow: "visible",
                filter: "drop-shadow(0 10px 30px rgba(0, 0, 0, 0.4))",
              }}
            >
              <defs>
                {/* Healthy Aeration Gradient */}
                <linearGradient id="healthyLungGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#0284c7" stopOpacity="0.25" />
                  <stop offset="100%" stopColor="#0ea5e9" stopOpacity="0.10" />
                </linearGradient>

                {/* Pneumonia Consolidation Lesion Gradient */}
                <radialGradient id="pneumoniaConsolidationGrad" cx="45%" cy="50%" r="55%">
                  <stop offset="0%" stopColor="#ef4444" stopOpacity="0.65" />
                  <stop offset="60%" stopColor="#dc2626" stopOpacity="0.35" />
                  <stop offset="100%" stopColor="#991b1b" stopOpacity="0.15" />
                </radialGradient>

                {/* Subtle Cardiac Silhouette */}
                <radialGradient id="cardiacShadow" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#0f172a" stopOpacity="0.5" />
                  <stop offset="100%" stopColor="#0f172a" stopOpacity="0.0" />
                </radialGradient>
              </defs>

              {/* Translucent Cardiac Silhouette behind lungs */}
              <ellipse cx="260" cy="275" rx="42" ry="58" fill="url(#cardiacShadow)" opacity="0.6" />

              {/* Trachea and Carina Bifurcation */}
              <path
                d="M 243,30 L 257,30 L 257,110 C 257,125 243,125 243,110 Z"
                fill="none"
                stroke="#38bdf8"
                strokeWidth="3.5"
                strokeOpacity="0.45"
                strokeLinecap="round"
              />
              {/* Tracheal rings */}
              {[45, 60, 75, 90, 105].map((y) => (
                <line
                  key={y}
                  x1="243"
                  y1={y}
                  x2="257"
                  y2={y}
                  stroke="#38bdf8"
                  strokeWidth="1.2"
                  strokeOpacity="0.35"
                />
              ))}

              {/* Main Bronchi Branches */}
              <path
                d="M 250,115 C 235,130 205,150 175,165"
                fill="none"
                stroke="#38bdf8"
                strokeWidth="2.5"
                strokeOpacity="0.4"
                strokeDasharray="4 3"
              />
              <path
                d="M 250,115 C 265,130 295,150 325,165"
                fill="none"
                stroke="#38bdf8"
                strokeWidth="2.5"
                strokeOpacity="0.4"
                strokeDasharray="4 3"
              />

              {/* Bronchioles Arborization */}
              <path
                d="M 175,165 C 150,185 135,220 130,260"
                fill="none"
                stroke="rgba(56, 189, 248, 0.25)"
                strokeWidth="1.5"
              />
              <path
                d="M 175,165 C 190,210 185,270 175,340"
                fill="none"
                stroke="rgba(56, 189, 248, 0.25)"
                strokeWidth="1.5"
              />
              <path
                d="M 325,165 C 345,185 365,220 370,260"
                fill="none"
                stroke="rgba(56, 189, 248, 0.25)"
                strokeWidth="1.5"
              />
              <path
                d="M 325,165 C 315,210 320,270 330,340"
                fill="none"
                stroke="rgba(56, 189, 248, 0.25)"
                strokeWidth="1.5"
              />

              {/* Anatomical Lobes */}
              {LOBES.map((lobe) => {
                const isSelected = selectedLobe === lobe.id;
                const isHovered = hoveredLobe === lobe.id;
                const isConsolidated = lobe.focal;

                let fillStyle = "url(#healthyLungGrad)";
                let strokeStyle = "rgba(56, 189, 248, 0.35)";
                let strokeWidth = 1.4;

                if (isConsolidated) {
                  fillStyle = "url(#pneumoniaConsolidationGrad)";
                  strokeStyle = isSelected || isHovered ? "#ef4444" : "rgba(239, 68, 68, 0.75)";
                  strokeWidth = isSelected || isHovered ? 2.5 : 2;
                } else if (isSelected || isHovered) {
                  fillStyle = "rgba(14, 165, 233, 0.25)";
                  strokeStyle = "#38bdf8";
                  strokeWidth = 2;
                }

                return (
                  <g key={lobe.id}>
                    <path
                      d={lobe.path}
                      fill={fillStyle}
                      stroke={strokeStyle}
                      strokeWidth={strokeWidth}
                      style={{
                        cursor: "pointer",
                        transition: "all 0.3s cubic-bezier(0.16, 1, 0.3, 1)",
                        filter: isConsolidated
                          ? "drop-shadow(0 0 16px rgba(239, 68, 68, 0.45))"
                          : (isHovered || isSelected ? "drop-shadow(0 0 12px rgba(56, 189, 248, 0.4))" : "none"),
                      }}
                      onMouseEnter={() => setHoveredLobe(lobe.id)}
                      onMouseLeave={() => setHoveredLobe(null)}
                      onClick={() => setSelectedLobe(selectedLobe === lobe.id ? null : lobe.id)}
                    />
                  </g>
                );
              })}

              {/* Clear Pneumonia Focal Target Pin & Callout on Right Lower Lobe */}
              {isPneumonia && (
                <g style={{ pointerEvents: "none" }}>
                  <circle cx="175" cy="330" r="24" fill="none" stroke="#ef4444" strokeWidth="1.2" strokeDasharray="3 3" opacity="0.75" />
                  <circle cx="175" cy="330" r="14" fill="rgba(239, 68, 68, 0.25)" stroke="#ef4444" strokeWidth="1.8" />
                  <circle cx="175" cy="330" r="4" fill="#ffffff" />

                  <line x1="175" y1="330" x2="80" y2="330" stroke="#ef4444" strokeWidth="1.2" strokeDasharray="2 2" />
                  <circle cx="80" cy="330" r="2.5" fill="#ef4444" />
                </g>
              )}
            </svg>

            {/* Pneumonia Lesion Floating Minimal Badge */}
            {isPneumonia ? (
              <div style={{
                position: "absolute",
                bottom: "65px",
                left: "0px",
                backgroundColor: "rgba(15, 23, 42, 0.85)",
                backdropFilter: "blur(8px)",
                border: "1px solid rgba(239, 68, 68, 0.4)",
                padding: "0.35rem 0.65rem",
                borderRadius: "8px",
                fontFamily: "var(--font-mono)",
                fontSize: "0.68rem",
                color: "#f87171",
                boxShadow: "0 4px 14px rgba(0, 0, 0, 0.4)",
                display: "flex",
                alignItems: "center",
                gap: "0.4rem",
              }}>
                <span style={{ width: "6px", height: "6px", borderRadius: "50%", backgroundColor: "#ef4444" }} />
                <span>Pneumonia Focus · RLL Consolidation</span>
              </div>
            ) : (
              <div style={{
                position: "absolute",
                bottom: "65px",
                left: "20px",
                backgroundColor: "rgba(15, 23, 42, 0.85)",
                backdropFilter: "blur(8px)",
                border: "1px solid rgba(16, 185, 129, 0.35)",
                padding: "0.35rem 0.65rem",
                borderRadius: "8px",
                fontFamily: "var(--font-mono)",
                fontSize: "0.68rem",
                color: "#34d399",
                boxShadow: "0 4px 14px rgba(0, 0, 0, 0.4)",
                display: "flex",
                alignItems: "center",
                gap: "0.4rem",
              }}>
                <span style={{ width: "6px", height: "6px", borderRadius: "50%", backgroundColor: "#10b981" }} />
                <span>Clear Bilateral Aeration</span>
              </div>
            )}

            {/* Interactive Lobe Detail Hover Pill */}
            {activeLobeId && activeLobeData && (
              <div style={{
                position: "absolute",
                top: "15px",
                right: "10px",
                backgroundColor: isDark ? "rgba(15, 23, 42, 0.9)" : "rgba(255, 255, 255, 0.95)",
                backdropFilter: "blur(10px)",
                border: isDark ? "1px solid rgba(255, 255, 255, 0.12)" : "1px solid rgba(15, 23, 42, 0.12)",
                padding: "0.5rem 0.8rem",
                borderRadius: "10px",
                fontSize: "0.72rem",
                fontFamily: "var(--font-mono)",
                color: isDark ? "#f8fafc" : "#0f172a",
                boxShadow: isDark ? "0 8px 24px rgba(0, 0, 0, 0.5)" : "0 4px 16px rgba(0, 0, 0, 0.08)",
              }}>
                <div style={{ fontWeight: "700", color: isDark ? "#38bdf8" : "#0284c7", marginBottom: "3px" }}>
                  {LOBES.find(l => l.id === activeLobeId)?.name}
                </div>
                <div style={{ color: activeLobeData.active ? (isDark ? "#f87171" : "#dc2626") : (isDark ? "#94a3b8" : "#64748b") }}>
                  Status: <strong style={{ color: activeLobeData.active ? (isDark ? "#f87171" : "#dc2626") : (isDark ? "#34d399" : "#059669") }}>{activeLobeData.status}</strong>
                </div>
                <div style={{ color: "#64748b", marginTop: "2px" }}>
                  Attention: <strong style={{ color: isDark ? "#38bdf8" : "#0284c7" }}>{Math.round(activeLobeData.attention * 100)}%</strong>
                </div>
              </div>
            )}
          </div>
        ) : activeMode === "gradcam" ? (
          /* Separate Clean Grad-CAM Display: Original X-Ray + Grad-CAM Heatmap Overlay (Zero baked graphs/tables) */
          <div style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "0.85rem",
            width: "100%",
            height: "100%",
          }}>
            {/* 1. Original X-Ray */}
            <div style={{
              position: "relative",
              width: "205px",
              height: "270px",
              borderRadius: "14px",
              overflow: "hidden",
              border: "1px solid rgba(255, 255, 255, 0.1)",
              backgroundColor: "#030712",
              boxShadow: "0 10px 25px rgba(0, 0, 0, 0.6)",
            }}>
              <img
                src={activeCase?.cxrView || "/assets/cxr_bacterial.jpg"}
                alt="Original Radiograph"
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  filter: isInverted ? "invert(100%) contrast(1.15)" : "none",
                }}
              />
              <div style={{
                position: "absolute",
                top: "8px",
                left: "10px",
                fontSize: "0.6rem",
                fontFamily: "var(--font-mono)",
                color: "#94a3b8",
                backgroundColor: "rgba(0, 0, 0, 0.7)",
                padding: "2px 6px",
                borderRadius: "4px",
                border: "1px solid rgba(255, 255, 255, 0.1)",
              }}>
                ORIGINAL X-RAY
              </div>
            </div>

            {/* 2. Standalone Grad-CAM Saliency Overlay */}
            <div style={{
              position: "relative",
              width: "205px",
              height: "270px",
              borderRadius: "14px",
              overflow: "hidden",
              border: "1px solid rgba(239, 68, 68, 0.35)",
              backgroundColor: "#030712",
              boxShadow: "0 10px 25px rgba(0, 0, 0, 0.6)",
            }}>
              <img
                src={activeCase?.gradcamView || "/assets/gradcam_overlay_bacterial.png"}
                alt="Grad-CAM Saliency Overlay"
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  filter: isInverted ? "invert(100%) contrast(1.15)" : "none",
                }}
              />
              <div style={{
                position: "absolute",
                top: "8px",
                left: "10px",
                fontSize: "0.6rem",
                fontFamily: "var(--font-mono)",
                color: "#f87171",
                backgroundColor: "rgba(0, 0, 0, 0.7)",
                padding: "2px 6px",
                borderRadius: "4px",
                border: "1px solid rgba(239, 68, 68, 0.3)",
              }}>
                GRAD-CAM OVERLAY
              </div>
              <div style={{
                position: "absolute",
                bottom: "8px",
                right: "10px",
                fontSize: "0.58rem",
                fontFamily: "var(--font-mono)",
                color: "#38bdf8",
                backgroundColor: "rgba(0, 0, 0, 0.7)",
                padding: "2px 6px",
                borderRadius: "4px",
              }}>
                Focus: {activeCase?.lung_focus_percent || "96%"}
              </div>
            </div>
          </div>
        ) : (
          /* Single PA Radiograph Mode */
          <div style={{
            position: "relative",
            width: "320px",
            height: "320px",
            borderRadius: "16px",
            overflow: "hidden",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            backgroundColor: "#030712",
            boxShadow: "0 10px 30px rgba(0, 0, 0, 0.6)",
          }}>
            <img
              src={activeCase?.cxrView || "/assets/cxr_bacterial.jpg"}
              alt="Patient CXR"
              style={{
                width: "100%",
                height: "100%",
                objectFit: "contain",
                filter: isInverted ? "invert(100%) contrast(1.15)" : "none",
                transition: "filter 0.3s ease",
              }}
            />

            <div style={{
              position: "absolute",
              top: "10px",
              left: "12px",
              fontSize: "0.64rem",
              fontFamily: "var(--font-mono)",
              color: "#38bdf8",
              backgroundColor: "rgba(0, 0, 0, 0.6)",
              padding: "2px 6px",
              borderRadius: "4px",
            }}>
              CHEST PA RADIOGRAPH
            </div>
          </div>
        )}
      </div>

      {/* Sleek Minimal View Switcher (Replaces the 6 boxy thumbnails) */}
      <div style={{
        display: "flex",
        alignItems: "center",
        gap: "0.5rem",
        marginTop: "0.6rem",
        backgroundColor: isDark ? "rgba(11, 17, 32, 0.8)" : "rgba(255, 255, 255, 0.92)",
        backdropFilter: "blur(12px)",
        padding: "0.35rem 0.45rem",
        borderRadius: "9999px",
        border: isDark ? "1px solid rgba(255, 255, 255, 0.08)" : "1px solid rgba(15, 23, 42, 0.12)",
        boxShadow: isDark ? "0 4px 16px rgba(0, 0, 0, 0.3)" : "0 4px 16px rgba(15, 23, 42, 0.08)",
      }}>
        {/* Tab 1: Lung Anatomy */}
        <button
          onClick={() => setCurrentView("anatomy")}
          style={{
            padding: "0.45rem 0.9rem",
            borderRadius: "9999px",
            fontSize: "0.72rem",
            fontWeight: activeMode === "anatomy" ? "700" : "500",
            fontFamily: "var(--font-mono)",
            backgroundColor: activeMode === "anatomy" ? (isDark ? "rgba(56, 189, 248, 0.2)" : "rgba(2, 132, 199, 0.15)") : "transparent",
            color: activeMode === "anatomy" ? (isDark ? "#38bdf8" : "#0284c7") : (isDark ? "#94a3b8" : "#64748b"),
            border: activeMode === "anatomy" ? (isDark ? "1px solid rgba(56, 189, 248, 0.4)" : "1px solid rgba(2, 132, 199, 0.3)") : "1px solid transparent",
            display: "flex",
            alignItems: "center",
            gap: "0.35rem",
            transition: "all 0.2s ease",
          }}
        >
          <span>Anatomy</span>
        </button>

        {/* Tab 2: Radiograph (CXR) */}
        <button
          onClick={() => setCurrentView("cxr")}
          style={{
            padding: "0.45rem 0.9rem",
            borderRadius: "9999px",
            fontSize: "0.72rem",
            fontWeight: activeMode === "cxr" ? "700" : "500",
            fontFamily: "var(--font-mono)",
            backgroundColor: activeMode === "cxr" ? (isDark ? "rgba(56, 189, 248, 0.2)" : "rgba(2, 132, 199, 0.15)") : "transparent",
            color: activeMode === "cxr" ? (isDark ? "#38bdf8" : "#0284c7") : (isDark ? "#94a3b8" : "#64748b"),
            border: activeMode === "cxr" ? (isDark ? "1px solid rgba(56, 189, 248, 0.4)" : "1px solid rgba(2, 132, 199, 0.3)") : "1px solid transparent",
            display: "flex",
            alignItems: "center",
            gap: "0.35rem",
            transition: "all 0.2s ease",
          }}
        >
          <span>Radiograph</span>
        </button>

        {/* Tab 3: Grad-CAM Heatmap */}
        <button
          onClick={() => setCurrentView("gradcam")}
          style={{
            padding: "0.45rem 0.9rem",
            borderRadius: "9999px",
            fontSize: "0.72rem",
            fontWeight: activeMode === "gradcam" ? "700" : "500",
            fontFamily: "var(--font-mono)",
            backgroundColor: activeMode === "gradcam" ? (isDark ? "rgba(239, 68, 68, 0.2)" : "rgba(220, 38, 38, 0.15)") : "transparent",
            color: activeMode === "gradcam" ? (isDark ? "#f87171" : "#dc2626") : (isDark ? "#94a3b8" : "#64748b"),
            border: activeMode === "gradcam" ? (isDark ? "1px solid rgba(239, 68, 68, 0.4)" : "1px solid rgba(220, 38, 38, 0.3)") : "1px solid transparent",
            display: "flex",
            alignItems: "center",
            gap: "0.35rem",
            transition: "all 0.2s ease",
          }}
        >
          <span>Grad-CAM</span>
        </button>

        <span style={{ width: "1px", height: "16px", backgroundColor: isDark ? "rgba(255, 255, 255, 0.12)" : "rgba(15, 23, 42, 0.12)", margin: "0 0.15rem" }} />

        {/* Invert contrast button */}
        <button
          onClick={() => setIsInverted(!isInverted)}
          title="Invert Image Contrast"
          style={{
            padding: "0.45rem 0.75rem",
            borderRadius: "9999px",
            fontSize: "0.7rem",
            fontWeight: "500",
            fontFamily: "var(--font-mono)",
            backgroundColor: isInverted ? (isDark ? "rgba(255, 255, 255, 0.15)" : "rgba(15, 23, 42, 0.12)") : "transparent",
            color: isInverted ? (isDark ? "#ffffff" : "#0f172a") : (isDark ? "#94a3b8" : "#64748b"),
            display: "flex",
            alignItems: "center",
            gap: "0.3rem",
            transition: "all 0.2s ease",
          }}
        >
          <span>Invert</span>
        </button>
      </div>
    </div>
  );
}
