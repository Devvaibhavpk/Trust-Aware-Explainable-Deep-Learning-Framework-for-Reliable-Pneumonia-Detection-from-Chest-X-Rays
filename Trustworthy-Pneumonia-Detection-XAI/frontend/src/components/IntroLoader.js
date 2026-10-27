"use client";

import React, { useState, useEffect } from "react";

export default function IntroLoader({ onComplete }) {
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState("INITIALIZING BIO-PULMONARY SENSORS...");
  const [isFadingOut, setIsFadingOut] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setStatusText("PULMONARY SYSTEM ONLINE. READY.");
          setTimeout(() => {
            setIsFadingOut(true);
            setTimeout(() => {
              onComplete();
            }, 600);
          }, 400);
          return 100;
        }

        const nextVal = prev + Math.floor(Math.random() * 4) + 2;
        const clamped = Math.min(nextVal, 100);

        if (clamped < 25) {
          setStatusText("INITIALIZING BIO-PULMONARY SENSORS...");
        } else if (clamped < 50) {
          setStatusText("LOADING RESNET18 CONVOLUTIONAL WEIGHTS...");
        } else if (clamped < 75) {
          setStatusText("CALIBRATING TEMPERATURE SCALING MATRIX...");
        } else if (clamped < 95) {
          setStatusText("SYNCHRONIZING ANATOMICAL LUNG PRIORS...");
        } else {
          setStatusText("FINALIZING TRUST ENGINE CALIBRATION...");
        }

        return clamped;
      });
    }, 45);

    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <div style={{
      position: "fixed",
      inset: 0,
      backgroundColor: "#070d18",
      backgroundImage: "radial-gradient(circle at 50% 50%, #0d1b2e 0%, #050912 100%)",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 9999,
      opacity: isFadingOut ? 0 : 1,
      transition: "opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1)",
      pointerEvents: isFadingOut ? "none" : "all",
    }}>
      {/* Background Holographic Coordinate Rings */}
      <div style={{
        position: "absolute",
        width: "560px",
        height: "560px",
        borderRadius: "50%",
        border: "1px dashed rgba(6, 182, 212, 0.2)",
        pointerEvents: "none",
      }} className="animate-radar" />

      <div style={{
        position: "absolute",
        width: "480px",
        height: "480px",
        borderRadius: "50%",
        border: "1px solid rgba(6, 182, 212, 0.15)",
        pointerEvents: "none",
      }} />

      {/* Central Lung Structure Graphic */}
      <div style={{
        position: "relative",
        width: "280px",
        height: "280px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        marginBottom: "2rem",
      }}>
        {/* Soft Radial Backlight */}
        <div style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(circle, rgba(6, 182, 212, 0.3) 0%, transparent 70%)",
          filter: "blur(20px)",
        }} />

        {/* Pure Transparent Holographic SVG Lungs Structure (Zero white card / JPG box) */}
        <div style={{
          position: "relative",
          width: "260px",
          height: "260px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}>
          {/* Base faint ghost structure */}
          <div style={{ position: "absolute", inset: 0, opacity: 0.2 }}>
            <svg viewBox="0 0 300 300" style={{ width: "100%", height: "100%" }}>
              <path d="M 145,20 L 155,20 L 155,85 L 145,85 Z" fill="none" stroke="#38bdf8" strokeWidth="2" />
              <line x1="145" y1="35" x2="155" y2="35" stroke="#38bdf8" strokeWidth="1.2" />
              <line x1="145" y1="50" x2="155" y2="50" stroke="#38bdf8" strokeWidth="1.2" />
              <line x1="145" y1="65" x2="155" y2="65" stroke="#38bdf8" strokeWidth="1.2" />
              <path d="M 145,85 C 135,110 110,130 85,150" fill="none" stroke="#38bdf8" strokeWidth="2" />
              <path d="M 155,85 C 165,110 190,130 215,150" fill="none" stroke="#38bdf8" strokeWidth="2" />
              <path d="M 115,120 C 90,110 65,125 50,140" fill="none" stroke="#38bdf8" strokeWidth="1.5" strokeDasharray="3,2" />
              <path d="M 95,140 C 75,160 65,195 60,225" fill="none" stroke="#38bdf8" strokeWidth="1.5" />
              <path d="M 185,120 C 210,110 235,125 250,140" fill="none" stroke="#38bdf8" strokeWidth="1.5" strokeDasharray="3,2" />
              <path d="M 205,140 C 225,160 235,195 240,225" fill="none" stroke="#38bdf8" strokeWidth="1.5" />
              <path
                d="M 140,88 C 120,40 60,65 45,130 C 35,180 40,230 55,265 C 75,280 115,275 135,245 C 145,210 145,150 140,88 Z"
                fill="none"
                stroke="#38bdf8"
                strokeWidth="2"
              />
              <path d="M 45,160 C 75,170 110,165 140,180" fill="none" stroke="#38bdf8" strokeWidth="1.2" strokeDasharray="4,3" />
              <path d="M 50,210 C 80,225 110,215 135,240" fill="none" stroke="#38bdf8" strokeWidth="1.2" strokeDasharray="4,3" />
              <path
                d="M 160,88 C 180,40 240,65 255,130 C 265,180 260,230 245,265 C 225,280 185,275 170,235 C 155,200 155,150 160,88 Z"
                fill="none"
                stroke="#38bdf8"
                strokeWidth="2"
              />
              <path d="M 255,160 C 225,185 195,205 170,230" fill="none" stroke="#38bdf8" strokeWidth="1.2" strokeDasharray="4,3" />
            </svg>
          </div>

          {/* Active fill loaded from 0% to 100% */}
          <div style={{
            position: "absolute",
            inset: 0,
            overflow: "hidden",
            clipPath: `inset(${100 - progress}% 0 0 0)`,
            transition: "clip-path 0.08s ease-out",
          }}>
            <svg viewBox="0 0 300 300" style={{
              width: "100%",
              height: "100%",
              filter: "drop-shadow(0 0 15px #10b981) drop-shadow(0 0 25px #06b6d4)",
            }}>
              <path d="M 145,20 L 155,20 L 155,85 L 145,85 Z" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="2.5" />
              <line x1="145" y1="35" x2="155" y2="35" stroke="#10b981" strokeWidth="1.5" />
              <line x1="145" y1="50" x2="155" y2="50" stroke="#10b981" strokeWidth="1.5" />
              <line x1="145" y1="65" x2="155" y2="65" stroke="#10b981" strokeWidth="1.5" />
              <path d="M 145,85 C 135,110 110,130 85,150" fill="none" stroke="#10b981" strokeWidth="2.5" />
              <path d="M 155,85 C 165,110 190,130 215,150" fill="none" stroke="#10b981" strokeWidth="2.5" />
              <path d="M 115,120 C 90,110 65,125 50,140" fill="none" stroke="#00ff88" strokeWidth="1.8" />
              <path d="M 95,140 C 75,160 65,195 60,225" fill="none" stroke="#00ff88" strokeWidth="1.8" />
              <path d="M 185,120 C 210,110 235,125 250,140" fill="none" stroke="#00ff88" strokeWidth="1.8" />
              <path d="M 205,140 C 225,160 235,195 240,225" fill="none" stroke="#00ff88" strokeWidth="1.8" />
              <path
                d="M 140,88 C 120,40 60,65 45,130 C 35,180 40,230 55,265 C 75,280 115,275 135,245 C 145,210 145,150 140,88 Z"
                fill="rgba(16, 185, 129, 0.12)"
                stroke="#10b981"
                strokeWidth="2.5"
              />
              <path d="M 45,160 C 75,170 110,165 140,180" fill="none" stroke="#38bdf8" strokeWidth="1.5" strokeDasharray="4,3" />
              <path d="M 50,210 C 80,225 110,215 135,240" fill="none" stroke="#38bdf8" strokeWidth="1.5" strokeDasharray="4,3" />
              <path
                d="M 160,88 C 180,40 240,65 255,130 C 265,180 260,230 245,265 C 225,280 185,275 170,235 C 155,200 155,150 160,88 Z"
                fill="rgba(16, 185, 129, 0.12)"
                stroke="#10b981"
                strokeWidth="2.5"
              />
              <path d="M 255,160 C 225,185 195,205 170,230" fill="none" stroke="#38bdf8" strokeWidth="1.5" strokeDasharray="4,3" />
              <circle cx="55" cy="140" r="3.5" fill="#00ff88" />
              <circle cx="70" cy="190" r="3.5" fill="#00ff88" />
              <circle cx="95" cy="245" r="3.5" fill="#00ff88" />
              <circle cx="245" cy="140" r="3.5" fill="#00ff88" />
              <circle cx="230" cy="190" r="3.5" fill="#00ff88" />
              <circle cx="205" cy="245" r="3.5" fill="#00ff88" />
            </svg>
          </div>

          {/* Glowing laser scan line at the load boundary */}
          <div style={{
            position: "absolute",
            top: `${100 - progress}%`,
            left: "5%",
            right: "5%",
            height: "2px",
            background: "linear-gradient(90deg, transparent 0%, #00ff88 50%, transparent 100%)",
            boxShadow: "0 0 16px #00ff88, 0 0 30px #10b981",
            transition: "top 0.08s ease-out",
            opacity: progress > 0 && progress < 100 ? 1 : 0,
          }} />
        </div>
      </div>

      {/* Numerical Counter: 0% to 100% */}
      <div style={{
        fontSize: "3.5rem",
        fontWeight: "800",
        fontFamily: "var(--font-mono)",
        color: "#ffffff",
        letterSpacing: "0.04em",
        textShadow: "0 0 24px rgba(6, 182, 212, 0.6)",
        marginBottom: "0.5rem",
      }}>
        {progress}%
      </div>

      {/* Progress Track */}
      <div style={{
        width: "320px",
        height: "4px",
        backgroundColor: "rgba(255, 255, 255, 0.1)",
        borderRadius: "9999px",
        overflow: "hidden",
        position: "relative",
        marginBottom: "1.2rem",
      }}>
        <div style={{
          height: "100%",
          width: `${progress}%`,
          background: "linear-gradient(90deg, #2563eb 0%, #06b6d4 100%)",
          boxShadow: "0 0 12px #06b6d4",
          transition: "width 0.08s ease-out",
          borderRadius: "9999px",
        }} />
      </div>

      {/* Status Subtext */}
      <div style={{
        fontSize: "0.74rem",
        fontWeight: "600",
        fontFamily: "var(--font-mono)",
        color: "#94a3b8",
        letterSpacing: "0.12em",
        textTransform: "uppercase",
        textAlign: "center",
      }}>
        {statusText}
      </div>
    </div>
  );
}
