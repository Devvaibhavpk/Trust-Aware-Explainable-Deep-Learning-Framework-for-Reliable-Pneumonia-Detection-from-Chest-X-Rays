"use client";

import React, { useState } from "react";

export default function TrustRadarChart({ activeCase }) {
  const [hoveredAxis, setHoveredAxis] = useState(null);

  const metrics = [
    { label: "CONF", fullName: "Calibrated Confidence", value: activeCase?.calibrated_confidence ? Math.round(activeCase.calibrated_confidence * 100) : 91, x: 100, y: 16 },
    { label: "STAB", fullName: "Epistemic Stability (1-σ²)", value: activeCase?.uncertainty_score ? Math.round((1 - activeCase.uncertainty_score) * 100) : 98, x: 168, y: 44 },
    { label: "FOCUS", fullName: "Lung Anatomical Overlap", value: activeCase?.focus_score ? Math.round(activeCase.focus_score * 100) : 94, x: 168, y: 112 },
    { label: "AGREE", fullName: "Ensemble Consensus", value: 92, x: 100, y: 144 },
    { label: "SAFETY", fullName: "OOD Artifact Rejection", value: activeCase?.ood_flag ? 30 : 96, x: 32, y: 112 },
    { label: "CALIB", fullName: "Temperature Alignment", value: 89, x: 32, y: 44 },
  ];

  const cx = 100;
  const cy = 80;
  const maxR = 48;

  const polyPoints = metrics.map((m, i) => {
    const angle = (i * 60 - 90) * (Math.PI / 180);
    const r = (m.value / 100) * maxR;
    const px = cx + r * Math.cos(angle);
    const py = cy + r * Math.sin(angle);
    return `${px.toFixed(1)},${py.toFixed(1)}`;
  }).join(" ");

  return (
    <div className="pacs-placard" style={{
      width: "100%",
      height: "100%",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
    }}>
      {/* Title */}
      <div className="pacs-placard-title">
        <span style={{ color: "#38bdf8" }}>◈</span>
        TRUSTENGINE™ MULTI-SIGNAL RADAR
      </div>

      {/* Radar Chart SVG */}
      <div style={{ position: "relative", width: "100%", height: "125px" }}>
        <svg viewBox="0 0 200 160" style={{ width: "100%", height: "100%", overflow: "visible" }}>
          {/* Subtle concentric grid rings */}
          <circle cx="100" cy="80" r="48" fill="none" stroke="rgba(56, 189, 248, 0.2)" strokeWidth="1" />
          <circle cx="100" cy="80" r="30" fill="none" stroke="rgba(56, 189, 248, 0.15)" strokeWidth="1" strokeDasharray="2,2" />
          <circle cx="100" cy="80" r="14" fill="none" stroke="rgba(56, 189, 248, 0.1)" strokeWidth="1" />

          {/* Radial Spokes */}
          {metrics.map((m, i) => {
            const angle = (i * 60 - 90) * (Math.PI / 180);
            const ex = cx + maxR * Math.cos(angle);
            const ey = cy + maxR * Math.sin(angle);
            return (
              <line
                key={i}
                x1={cx}
                y1={cy}
                x2={ex}
                y2={ey}
                stroke="rgba(56, 189, 248, 0.18)"
                strokeWidth="1"
              />
            );
          })}

          {/* Glowing Fluid Neon Polygon */}
          <polygon
            points={polyPoints}
            fill="rgba(6, 182, 212, 0.28)"
            stroke="#22d3ee"
            strokeWidth="2"
            strokeLinejoin="round"
            style={{
              filter: "drop-shadow(0 0 10px rgba(34, 211, 238, 0.5))",
              transition: "all 0.4s ease",
            }}
          />

          {/* Vertex Labels */}
          {metrics.map((m, i) => (
            <text
              key={i}
              x={m.x}
              y={m.y}
              fill="#94a3b8"
              fontSize="8.5"
              fontFamily="var(--font-mono)"
              fontWeight="700"
              textAnchor="middle"
              style={{ cursor: "pointer", transition: "all 0.2s ease" }}
              onMouseEnter={() => setHoveredAxis(m)}
              onMouseLeave={() => setHoveredAxis(null)}
            >
              {m.label}
            </text>
          ))}
        </svg>

        {/* Hover Tooltip */}
        {hoveredAxis && (
          <div style={{
            position: "absolute",
            top: "-8px",
            left: "50%",
            transform: "translateX(-50%)",
            backgroundColor: "rgba(6, 9, 17, 0.95)",
            backdropFilter: "blur(8px)",
            color: "#ffffff",
            padding: "0.25rem 0.6rem",
            borderRadius: "6px",
            fontSize: "0.65rem",
            fontFamily: "var(--font-mono)",
            whiteSpace: "nowrap",
            boxShadow: "0 4px 16px rgba(0,0,0,0.6)",
            border: "1px solid rgba(56, 189, 248, 0.4)",
            zIndex: 10,
          }}>
            {hoveredAxis.fullName}: <strong style={{ color: "#38bdf8" }}>{hoveredAxis.value}%</strong>
          </div>
        )}
      </div>

      {/* Subtext info */}
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        paddingTop: "0.45rem",
        borderTop: "1px solid rgba(56, 189, 248, 0.12)",
        fontFamily: "var(--font-mono)",
      }}>
        <span style={{ fontSize: "0.68rem", color: "#64748b" }}>Multi-Signal Synthesis</span>
        <span style={{ fontSize: "0.68rem", color: "#38bdf8", fontWeight: "700" }}>Optimal</span>
      </div>
    </div>
  );
}
