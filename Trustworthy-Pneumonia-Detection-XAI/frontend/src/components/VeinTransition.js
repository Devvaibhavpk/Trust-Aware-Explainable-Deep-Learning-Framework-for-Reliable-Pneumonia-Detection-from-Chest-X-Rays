"use client";

import React, { useEffect } from "react";

export default function VeinTransition({ onComplete }) {
  useEffect(() => {
    // Complete the vascular transition after 1.5s
    const timer = setTimeout(() => {
      onComplete();
    }, 1500);

    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div style={{
      position: "fixed",
      inset: 0,
      zIndex: 9998,
      pointerEvents: "none",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      overflow: "hidden",
      backgroundColor: "rgba(10, 15, 29, 0.45)",
      backdropFilter: "blur(6px)",
    }}>
      {/* Vascular Arterial Sweep Animation */}
      <svg
        viewBox="0 0 1000 1000"
        className="animate-blood-surge"
        style={{
          width: "120vw",
          height: "120vh",
          maxWidth: "1800px",
          maxHeight: "1800px",
        }}
      >
        <defs>
          <filter id="bloodGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          <linearGradient id="surgeGradient1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#ef4444" stopOpacity="1" />
            <stop offset="60%" stopColor="#b91c1c" stopOpacity="0.85" />
            <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.9" />
          </linearGradient>

          <linearGradient id="surgeGradient2" x1="100%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.95" />
            <stop offset="50%" stopColor="#ef4444" stopOpacity="0.9" />
            <stop offset="100%" stopColor="#dc2626" stopOpacity="1" />
          </linearGradient>
        </defs>

        {/* Major Pulmonary Arteries Branching Outward */}
        <g filter="url(#bloodGlow)">
          {/* Main Central Trunk */}
          <path
            d="M 500,500 C 450,400 350,300 150,150 M 500,500 C 550,400 650,300 850,150 M 500,500 C 400,550 250,650 100,850 M 500,500 C 600,550 750,650 900,850"
            fill="none"
            stroke="url(#surgeGradient1)"
            strokeWidth="14"
            strokeLinecap="round"
          />

          {/* Secondary Arterial Bifurcations */}
          <path
            d="M 350,300 C 300,220 200,200 50,220 M 650,300 C 700,220 800,200 950,220 M 250,650 C 200,720 150,750 20,800 M 750,650 C 800,720 850,750 980,800"
            fill="none"
            stroke="url(#surgeGradient2)"
            strokeWidth="8"
            strokeLinecap="round"
          />

          {/* Tertiary Micro-Capillary Web */}
          <path
            d="M 150,150 C 100,100 80,40 10,10 M 850,150 C 900,100 920,40 990,10 M 500,500 C 500,320 480,200 500,20 M 500,500 C 500,680 480,800 500,980"
            fill="none"
            stroke="#ef4444"
            strokeWidth="4"
            strokeLinecap="round"
          />
        </g>

        {/* Central Heart/Vascular Node Pulmonic Ring */}
        <circle
          cx="500"
          cy="500"
          r="48"
          fill="#dc2626"
          filter="url(#bloodGlow)"
          opacity="0.9"
        />
        <circle
          cx="500"
          cy="500"
          r="80"
          fill="none"
          stroke="#ef4444"
          strokeWidth="6"
          opacity="0.8"
        />
      </svg>

      {/* Floating Center Badge during transition */}
      <div style={{
        position: "absolute",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "0.5rem",
        color: "#ffffff",
      }}>
        <div style={{
          padding: "0.5rem 1.4rem",
          backgroundColor: "rgba(15, 23, 42, 0.9)",
          backdropFilter: "blur(12px)",
          borderRadius: "9999px",
          border: "1.5px solid rgba(239, 68, 68, 0.7)",
          boxShadow: "0 0 30px rgba(220, 38, 38, 0.5)",
          fontSize: "0.85rem",
          fontWeight: "800",
          letterSpacing: "0.1em",
          textTransform: "uppercase",
          display: "flex",
          alignItems: "center",
          gap: "0.6rem",
        }}>
          <span style={{
            width: "8px",
            height: "8px",
            backgroundColor: "#ef4444",
            borderRadius: "50%",
            boxShadow: "0 0 10px #ef4444",
          }} />
          PULMONARY VASCULAR SURGE
        </div>
        <span style={{ fontSize: "0.72rem", color: "#cbd5e1", letterSpacing: "0.08em" }}>
          STREAMING TELEMETRY RESULTS...
        </span>
      </div>
    </div>
  );
}
