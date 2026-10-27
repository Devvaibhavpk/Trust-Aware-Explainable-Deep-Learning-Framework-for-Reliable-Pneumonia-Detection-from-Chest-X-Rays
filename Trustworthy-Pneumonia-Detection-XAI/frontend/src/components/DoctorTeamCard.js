"use client";

import React from "react";

export default function DoctorTeamCard({ onExportReport }) {
  const doctors = [
    {
      id: "theresa",
      name: "Dr. Theresa Webb, MD",
      specialty: "CHIEF PULMONOLOGIST",
      sub: "Thoracic Critical Care",
      status: "Available for Triage",
      statusColor: "#10b981",
    },
    {
      id: "devon",
      name: "Dr. Devon Lane, MD",
      specialty: "LEAD THORACIC RADIOLOGIST",
      sub: "Chest X-Ray / CT Review",
      status: "In Case Review",
      statusColor: "#38bdf8",
    },
    {
      id: "kathryn",
      name: "Dr. Kathryn Murphy, MD",
      specialty: "INFECTIOUS DISEASE SPECIALIST",
      sub: "Bacterial vs Viral Protocol",
      status: "On Station",
      statusColor: "#10b981",
    },
  ];

  return (
    <div className="pacs-placard" style={{
      width: "100%",
      display: "flex",
      flexDirection: "column",
      gap: "0.85rem",
      padding: "1.25rem 1.4rem",
    }}>
      {/* Title */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div className="pacs-placard-title">
          <span style={{ color: "#38bdf8" }}>◈</span>
          RADIOLOGY CONSULTATION & CLINICAL OVER-READ
        </div>

        <button
          onClick={onExportReport}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.45rem",
            fontSize: "0.72rem",
            fontFamily: "var(--font-mono)",
            fontWeight: "700",
            color: "#38bdf8",
            backgroundColor: "rgba(56, 189, 248, 0.12)",
            border: "1px solid rgba(56, 189, 248, 0.3)",
            padding: "0.35rem 0.8rem",
            borderRadius: "6px",
            boxShadow: "0 0 10px rgba(56, 189, 248, 0.2)",
            transition: "all 0.2s ease",
          }}
        >
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          EXPORT CDS REPORT (PDF)
        </button>
      </div>

      {/* Doctor Rows in Dark Theme */}
      <div style={{ display: "flex", flexDirection: "column", gap: "0.6rem" }}>
        {doctors.map((doc) => (
          <div
            key={doc.id}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              padding: "0.55rem 0.85rem",
              borderRadius: "10px",
              backgroundColor: "rgba(6, 9, 17, 0.6)",
              border: "1px solid rgba(56, 189, 248, 0.15)",
              transition: "all 0.2s ease",
              cursor: "pointer",
            }}
          >
            {/* Left Info */}
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
              <div style={{
                width: "32px",
                height: "32px",
                borderRadius: "8px",
                backgroundColor: "rgba(56, 189, 248, 0.15)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "1rem",
                border: "1px solid rgba(56, 189, 248, 0.3)",
              }}>
                👨‍⚕️
              </div>
              <div style={{ display: "flex", flexDirection: "column" }}>
                <span style={{ fontSize: "0.82rem", fontWeight: "700", color: "#f8fafc" }}>
                  {doc.name}
                </span>
                <span style={{ fontSize: "0.65rem", color: "#94a3b8", fontFamily: "var(--font-mono)" }}>
                  {doc.specialty} · {doc.sub}
                </span>
              </div>
            </div>

            {/* Right Status */}
            <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
                <span style={{
                  width: "6px",
                  height: "6px",
                  borderRadius: "50%",
                  backgroundColor: doc.statusColor,
                  boxShadow: `0 0 6px ${doc.statusColor}`,
                }} />
                <span style={{ fontSize: "0.72rem", color: "#cbd5e1", fontFamily: "var(--font-mono)" }}>
                  {doc.status}
                </span>
              </div>

              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
