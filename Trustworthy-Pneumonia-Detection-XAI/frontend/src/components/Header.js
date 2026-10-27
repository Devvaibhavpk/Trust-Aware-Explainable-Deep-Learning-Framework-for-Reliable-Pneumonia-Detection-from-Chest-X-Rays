"use client";

import React from "react";
import { useTheme } from "../context/ThemeContext";

export default function Header() {
  const { theme, isDark, toggleTheme } = useTheme();

  return (
    <header style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0.85rem 2.2rem",
      backgroundColor: isDark ? "rgba(6, 10, 20, 0.85)" : "rgba(255, 255, 255, 0.92)",
      backdropFilter: "blur(14px)",
      borderBottom: isDark ? "1px solid rgba(255, 255, 255, 0.08)" : "1px solid rgba(15, 23, 42, 0.08)",
      position: "relative",
      zIndex: 50,
      transition: "background-color 0.25s ease, border-color 0.25s ease",
    }}>
      {/* Brand Logo & Project Title */}
      <div style={{ display: "flex", alignItems: "center", gap: "0.85rem" }}>
        {/* Logo Emblem Icon */}
        <div style={{
          position: "relative",
          width: "36px",
          height: "36px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          borderRadius: "10px",
          background: isDark
            ? "linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(16, 185, 129, 0.1) 100%)"
            : "linear-gradient(135deg, rgba(2, 132, 199, 0.12) 0%, rgba(16, 185, 129, 0.08) 100%)",
          border: isDark ? "1px solid rgba(56, 189, 248, 0.3)" : "1px solid rgba(2, 132, 199, 0.25)",
          boxShadow: isDark ? "0 0 20px rgba(14, 165, 233, 0.25)" : "0 4px 12px rgba(2, 132, 199, 0.12)",
        }}>
          <img
            src="/assets/logo.svg"
            alt="trustworthy-pneumonia-detector logo"
            style={{
              width: "28px",
              height: "28px",
              objectFit: "contain",
            }}
          />
        </div>

        {/* Project Name & Subtext */}
        <div style={{ display: "flex", flexDirection: "column" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.45rem" }}>
            <span style={{
              fontSize: "1.05rem",
              fontWeight: "800",
              color: isDark ? "#f8fafc" : "#0f172a",
              letterSpacing: "-0.01em",
              fontFamily: "var(--font-mono)",
            }}>
              trustworthy<span style={{ color: isDark ? "#38bdf8" : "#0284c7" }}>-pneumonia-detector</span>
            </span>
            <span style={{
              fontSize: "0.58rem",
              fontFamily: "var(--font-mono)",
              color: isDark ? "#10b981" : "#059669",
              backgroundColor: isDark ? "rgba(16, 185, 129, 0.12)" : "rgba(16, 185, 129, 0.1)",
              border: `1px solid ${isDark ? "rgba(16, 185, 129, 0.25)" : "rgba(16, 185, 129, 0.3)"}`,
              padding: "1px 5px",
              borderRadius: "4px",
              fontWeight: "700",
            }}>
              XAI
            </span>
          </div>
          <span style={{
            fontSize: "0.64rem",
            color: isDark ? "#64748b" : "#64748b",
            fontFamily: "var(--font-mono)",
            letterSpacing: "0.04em",
          }}>
            Trust-Aware Deep Learning Framework · ResNet-18
          </span>
        </div>
      </div>

      {/* Right Controls: Dark/Light Mode Switcher & System Status */}
      <div style={{ display: "flex", alignItems: "center", gap: "0.85rem" }}>
        {/* Dark/Light Mode Toggle Button */}
        <button
          onClick={toggleTheme}
          title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
          aria-label={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.45rem",
            padding: "0.38rem 0.75rem",
            borderRadius: "10px",
            backgroundColor: isDark ? "rgba(15, 23, 42, 0.7)" : "rgba(241, 245, 249, 0.95)",
            border: isDark ? "1px solid rgba(255, 255, 255, 0.12)" : "1px solid rgba(15, 23, 42, 0.12)",
            color: isDark ? "#f8fafc" : "#0f172a",
            fontSize: "0.74rem",
            fontWeight: "600",
            fontFamily: "var(--font-mono)",
            cursor: "pointer",
            transition: "all 0.2s ease",
            boxShadow: isDark ? "none" : "0 2px 6px rgba(0, 0, 0, 0.05)",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = isDark ? "#38bdf8" : "#0284c7";
            e.currentTarget.style.transform = "scale(1.02)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = isDark ? "rgba(255, 255, 255, 0.12)" : "rgba(15, 23, 42, 0.12)";
            e.currentTarget.style.transform = "scale(1)";
          }}
        >
          {isDark ? (
            /* Sun Icon (for switching to Light mode) */
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="5"></circle>
              <line x1="12" y1="1" x2="12" y2="3"></line>
              <line x1="12" y1="21" x2="12" y2="23"></line>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
              <line x1="1" y1="12" x2="3" y2="12"></line>
              <line x1="21" y1="12" x2="23" y2="12"></line>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
          ) : (
            /* Moon Icon (for switching to Dark mode) */
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#0284c7" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
          )}
          <span>{isDark ? "Light Mode" : "Dark Mode"}</span>
        </button>

        {/* Clean System Status Indicator */}
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: "0.55rem",
          backgroundColor: isDark ? "rgba(15, 23, 42, 0.6)" : "rgba(241, 245, 249, 0.95)",
          padding: "0.38rem 0.75rem",
          borderRadius: "8px",
          border: isDark ? "1px solid rgba(255, 255, 255, 0.06)" : "1px solid rgba(15, 23, 42, 0.08)",
          boxShadow: isDark ? "none" : "0 2px 6px rgba(0, 0, 0, 0.04)",
        }}>
          <span style={{
            width: "7px",
            height: "7px",
            borderRadius: "50%",
            backgroundColor: "#10b981",
            boxShadow: "0 0 8px #10b981",
          }} />
          <span style={{
            fontSize: "0.72rem",
            color: isDark ? "#cbd5e1" : "#334155",
            fontFamily: "var(--font-mono)",
            fontWeight: "600",
          }}>
            PyTorch Inference Online
          </span>
        </div>
      </div>
    </header>
  );
}
