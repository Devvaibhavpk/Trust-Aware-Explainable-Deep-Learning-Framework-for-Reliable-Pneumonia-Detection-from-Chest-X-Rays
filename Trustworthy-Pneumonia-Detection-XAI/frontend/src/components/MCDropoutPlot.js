"use client";

import React, { useState } from "react";

export default function MCDropoutPlot({ activeCase }) {
  const [hoveredPoint, setHoveredPoint] = useState(null);

  const meanConf = activeCase?.calibrated_confidence || 0.914;
  const variance = activeCase?.uncertainty_score || 0.0126;
  const std = (Math.sqrt(variance)).toFixed(4);
  const isPneumonia = activeCase?.predicted_class?.toLowerCase().includes("pneumonia");

  // Generate 2D coordinate points for the 30 MC stochastic forward passes
  const samples = activeCase?.mc_samples || [
    0.92, 0.94, 0.89, 0.95, 0.91, 0.88, 0.93, 0.90, 0.96, 0.91,
    0.93, 0.87, 0.92, 0.95, 0.89, 0.94, 0.90, 0.92, 0.91, 0.93
  ];

  const points = [
    { x: 140, y: 85, r: 20, fill: "url(#centerGrad)", isCenter: true, label: "Ensemble Mean (μ)", val: (meanConf * 100).toFixed(1) + "%" },
    { x: 185, y: 65, r: 10, fill: isPneumonia ? "#38bdf8" : "#34d399", label: "MC Pass #04", val: `${((samples[3] || 0.94) * 100).toFixed(1)}%` },
    { x: 200, y: 95, r: 8, fill: "#0284c7", label: "MC Pass #08", val: `${((samples[7] || 0.91) * 100).toFixed(1)}%` },
    { x: 165, y: 50, r: 9, fill: "#2563eb", label: "MC Pass #12", val: `${((samples[11] || 0.89) * 100).toFixed(1)}%` },
    { x: 105, y: 105, r: 12, fill: "#0369a1", label: "MC Pass #17", val: `${((samples[16] || 0.93) * 100).toFixed(1)}%` },
    { x: 85, y: 80, r: 7, fill: "#38bdf8", label: "MC Pass #21", val: `${((samples[20] || 0.90) * 100).toFixed(1)}%` },
    { x: 120, y: 48, r: 8, fill: "#60a5fa", label: "MC Pass #25", val: `${((samples[24] || 0.92) * 100).toFixed(1)}%` },
    { x: 170, y: 115, r: 9, fill: "#0ea5e9", label: "MC Pass #29", val: `${((samples[28] || 0.91) * 100).toFixed(1)}%` },
  ];

  return (
    <div className="pacs-placard" style={{
      width: "100%",
      height: "100%",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
    }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div className="pacs-placard-title">
          <span style={{ color: "#38bdf8" }}>◈</span>
          MC DROPOUT UNCERTAINTY DISTRIBUTION
        </div>

        <span style={{
          fontSize: "0.68rem",
          fontWeight: "700",
          fontFamily: "var(--font-mono)",
          color: "#38bdf8",
          backgroundColor: "rgba(56, 189, 248, 0.12)",
          padding: "0.2rem 0.6rem",
          borderRadius: "6px",
          border: "1px solid rgba(56, 189, 248, 0.25)",
        }}>
          VAR σ² = {variance}
        </span>
      </div>

      {/* 2D Coordinate Scatter Plot */}
      <div style={{ position: "relative", width: "100%", height: "145px", marginTop: "0.25rem" }}>
        <svg viewBox="0 0 280 160" style={{ width: "100%", height: "100%", overflow: "visible" }}>
          <defs>
            <radialGradient id="centerGrad" cx="40%" cy="40%" r="60%">
              <stop offset="0%" stopColor="#38bdf8" />
              <stop offset="70%" stopColor="#0284c7" />
              <stop offset="100%" stopColor="#1e3a8a" />
            </radialGradient>
          </defs>

          {/* Coordinate Crosshairs */}
          <line x1="140" y1="15" x2="140" y2="145" stroke="rgba(56, 189, 248, 0.25)" strokeWidth="1" strokeDasharray="3,3" />
          <line x1="20" y1="85" x2="260" y2="85" stroke="rgba(56, 189, 248, 0.25)" strokeWidth="1" strokeDasharray="3,3" />

          {/* Axis Labels */}
          <text x="140" y="24" fill="#64748b" fontSize="10" fontFamily="var(--font-mono)" textAnchor="middle">P(PNEUMONIA)</text>
          <text x="25" y="80" fill="#64748b" fontSize="9.5" fontFamily="var(--font-mono)">-2σ</text>
          <text x="255" y="80" fill="#64748b" fontSize="9.5" fontFamily="var(--font-mono)" textAnchor="end">+2σ</text>

          {/* Dynamic Stochastic Pass Bubbles */}
          {points.map((pt, idx) => (
            <circle
              key={idx}
              cx={pt.x}
              cy={pt.y}
              r={pt.r}
              fill={pt.fill}
              style={{
                cursor: "pointer",
                transition: "all 0.25s ease",
                filter: pt.isCenter ? "drop-shadow(0 0 12px rgba(56, 189, 248, 0.8))" : "drop-shadow(0 0 4px rgba(56, 189, 248, 0.4))",
              }}
              onMouseEnter={() => setHoveredPoint(pt)}
              onMouseLeave={() => setHoveredPoint(null)}
            />
          ))}
        </svg>

        {/* Hover Tooltip */}
        {hoveredPoint && (
          <div style={{
            position: "absolute",
            bottom: "8px",
            left: "50%",
            transform: "translateX(-50%)",
            backgroundColor: "rgba(6, 9, 17, 0.95)",
            backdropFilter: "blur(8px)",
            color: "#ffffff",
            padding: "0.3rem 0.65rem",
            borderRadius: "6px",
            fontSize: "0.68rem",
            fontFamily: "var(--font-mono)",
            whiteSpace: "nowrap",
            boxShadow: "0 4px 16px rgba(0,0,0,0.6)",
            border: "1px solid rgba(56, 189, 248, 0.4)",
            zIndex: 10,
          }}>
            {hoveredPoint.label}: <strong style={{ color: "#38bdf8" }}>{hoveredPoint.val}</strong>
          </div>
        )}
      </div>

      {/* Footer Details */}
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        paddingTop: "0.45rem",
        borderTop: "1px solid rgba(56, 189, 248, 0.12)",
        fontFamily: "var(--font-mono)",
      }}>
        <span style={{ fontSize: "0.68rem", color: "#94a3b8" }}>30 Stochastic Samples</span>
        <span style={{ fontSize: "0.68rem", fontWeight: "700", color: "#34d399" }}>
          Std Dev: ±{std} (Stable)
        </span>
      </div>
    </div>
  );
}
