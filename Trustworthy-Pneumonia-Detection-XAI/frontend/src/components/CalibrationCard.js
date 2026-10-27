"use client";

import React from "react";
import { useTheme } from "../context/ThemeContext";

export default function CalibrationCard({ activeCase }) {
  const { isDark } = useTheme();
  const calibrated = activeCase?.calibrated_confidence ? Math.round(activeCase.calibrated_confidence * 100) : 91;
  const raw = activeCase?.raw_confidence ? Math.round(activeCase.raw_confidence * 100) : 98;
  const temp = activeCase?.temperature_scaling?.temperature || 1.42;
  const ece = activeCase?.temperature_scaling?.ece_after || 0.016;

  return (
    <div className="pacs-placard" style={{
      width: "100%",
      height: "100%",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
    }}>
      {/* Title */}
      <div>
        <div className="pacs-placard-title">
          <span style={{ color: "#38bdf8" }}>◈</span>
          TEMPERATURE-SCALED CALIBRATION
        </div>

        <div style={{
          fontSize: "1.35rem",
          fontWeight: "800",
          fontFamily: "var(--font-mono)",
          color: isDark ? "#ffffff" : "#0f172a",
          display: "flex",
          alignItems: "baseline",
          gap: "6px",
          marginTop: "0.25rem",
        }}>
          <span>{calibrated}%</span>
          <span style={{ fontSize: "0.72rem", fontWeight: "600", color: "#38bdf8" }}>CALIBRATED</span>
        </div>
      </div>

      {/* Smooth Wavy Calibration Reliability Curve */}
      <div style={{ position: "relative", width: "100%", height: "60px", margin: "0.3rem 0" }}>
        <svg viewBox="0 0 200 60" style={{ width: "100%", height: "100%", overflow: "visible" }}>
          {/* Subtle baseline */}
          <line x1="0" y1="30" x2="200" y2="30" stroke="rgba(56, 189, 248, 0.2)" strokeWidth="1" strokeDasharray="3,3" />

          {/* Smooth neon probability alignment curve */}
          <path
            d="M 0,34 C 40,34 50,14 100,26 C 150,38 160,18 200,28"
            fill="none"
            stroke="#38bdf8"
            strokeWidth="2.5"
            strokeLinecap="round"
            style={{ filter: "drop-shadow(0 0 8px rgba(56, 189, 248, 0.6))" }}
          />

          {/* Glowing Slider / Marker Knob */}
          <circle
            cx="100"
            cy="26"
            r="7"
            fill="#060911"
            stroke="#22d3ee"
            strokeWidth="3"
            style={{
              filter: "drop-shadow(0 0 8px #22d3ee)",
              cursor: "pointer",
            }}
          />
        </svg>

        {/* Lower label: Scaling parameter */}
        <div style={{
          position: "absolute",
          bottom: "-4px",
          left: "50%",
          transform: "translateX(-50%)",
          fontSize: "0.68rem",
          fontFamily: "var(--font-mono)",
          color: "#94a3b8",
          fontWeight: "600",
        }}>
          T = {temp} (Optimized)
        </div>
      </div>

      {/* Footer comparison */}
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        paddingTop: "0.45rem",
        borderTop: isDark ? "1px solid rgba(56, 189, 248, 0.12)" : "1px solid rgba(15, 23, 42, 0.08)",
        fontFamily: "var(--font-mono)",
      }}>
        <span style={{ fontSize: "0.68rem", color: isDark ? "#64748b" : "#94a3b8" }}>Raw Softmax: {raw}%</span>
        <span style={{ fontSize: "0.68rem", color: isDark ? "#34d399" : "#059669", fontWeight: "700" }}>
          ECE: {ece}
        </span>
      </div>
    </div>
  );
}
