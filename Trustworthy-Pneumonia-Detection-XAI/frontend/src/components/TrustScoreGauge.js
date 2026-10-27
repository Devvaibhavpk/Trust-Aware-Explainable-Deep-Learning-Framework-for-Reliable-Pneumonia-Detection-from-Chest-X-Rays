"use client";

import React from "react";

export default function TrustScoreGauge({ activeCase }) {
  const trustScore = activeCase?.trust_score ? Math.round(activeCase.trust_score * 100) : 94;
  const isHighTrust = trustScore >= 75;

  const radius = 38;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (trustScore / 100) * circumference;

  return (
    <div className="pacs-placard" style={{
      width: "100%",
      height: "100%",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      textAlign: "center",
      padding: "1.2rem 1rem",
    }}>
      {/* Circular Radial Gauge */}
      <div style={{ position: "relative", width: "96px", height: "96px", marginBottom: "0.65rem" }}>
        <svg viewBox="0 0 100 100" style={{ width: "100%", height: "100%", transform: "rotate(-90deg)" }}>
          {/* Background circle track */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="rgba(56, 189, 248, 0.15)"
            strokeWidth="5.5"
          />

          {/* Active Glowing Progress Ring */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke={isHighTrust ? "#22d3ee" : "#f59e0b"}
            strokeWidth="6"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            style={{
              transition: "stroke-dashoffset 0.8s cubic-bezier(0.16, 1, 0.3, 1)",
              filter: isHighTrust ? "drop-shadow(0 0 8px rgba(34, 211, 238, 0.8))" : "drop-shadow(0 0 8px rgba(245, 158, 11, 0.8))",
            }}
          />
        </svg>

        {/* Center Percentage Display */}
        <div style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "1.35rem",
          fontWeight: "800",
          fontFamily: "var(--font-mono)",
          color: "#ffffff",
          textShadow: "0 0 12px rgba(34, 211, 238, 0.6)",
        }}>
          {trustScore}%
        </div>
      </div>

      {/* Label */}
      <div style={{
        fontSize: "0.72rem",
        fontWeight: "800",
        fontFamily: "var(--font-mono)",
        letterSpacing: "0.1em",
        color: "#ffffff",
        textTransform: "uppercase",
        marginBottom: "0.3rem",
      }}>
        COMPOSITE TRUST INDEX
      </div>

      {/* Status Badge */}
      <span style={{
        fontSize: "0.66rem",
        fontWeight: "700",
        fontFamily: "var(--font-mono)",
        color: isHighTrust ? "#34d399" : "#fbbf24",
        backgroundColor: isHighTrust ? "rgba(16, 185, 129, 0.12)" : "rgba(245, 158, 11, 0.12)",
        padding: "0.2rem 0.55rem",
        borderRadius: "4px",
        border: `1px solid ${isHighTrust ? "rgba(16, 185, 129, 0.3)" : "rgba(245, 158, 11, 0.3)"}`,
      }}>
        {isHighTrust ? "GRADE A · CLINICAL SAFE" : "OVER-READ REQUIRED"}
      </span>
    </div>
  );
}
