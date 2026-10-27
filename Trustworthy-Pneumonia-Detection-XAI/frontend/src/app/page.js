"use client";

import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import IntroLoader from "../components/IntroLoader";
import BiopulmonaryBackground from "../components/BiopulmonaryBackground";
import UploadView from "../components/UploadView";
import VeinTransition from "../components/VeinTransition";
import ResultsDashboard from "../components/ResultsDashboard";
import { useTheme } from "../context/ThemeContext";

export default function Home() {
  const { theme, isDark } = useTheme();
  // Navigation stage: "intro" -> "upload" -> "transitioning" -> "results"
  const [stage, setStage] = useState("intro");
  const [activeTab, setActiveTab] = useState("systems");
  const [activeCaseId, setActiveCaseId] = useState("bacterial");
  const [activeCase, setActiveCase] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  // Load initial case data on mount
  useEffect(() => {
    async function fetchCase(id) {
      try {
        const res = await fetch(`/api/predict?case=${id}`);
        if (res.ok) {
          const data = await res.json();
          setActiveCase(data);
        }
      } catch (err) {
        console.error("Failed to load initial case:", err);
      }
    }
    fetchCase(activeCaseId);
  }, [activeCaseId]);

  // Handle switching sample case in upload view
  const handleSelectSample = async (id) => {
    setActiveCaseId(id);
    setSelectedFile(null);
    setPreviewUrl(null);
    try {
      const res = await fetch(`/api/predict?case=${id}`);
      if (res.ok) {
        const data = await res.json();
        setActiveCase(data);
      }
    } catch (err) {
      console.error("Failed to select sample case:", err);
    }
  };

  // Trigger blood vein flow transition to results
  const handleAnalyzeAndTransition = async () => {
    // Start vein transition
    setStage("transitioning");

    // If a custom image was selected, execute live model inference
    if (selectedFile && previewUrl) {
      try {
        const res = await fetch("/api/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            fileName: selectedFile.name,
            imageData: previewUrl,
          }),
        });
        if (res.ok) {
          const liveData = await res.json();
          setActiveCase(liveData);
        }
      } catch (err) {
        console.warn("Live model analysis fallback:", err);
      }
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      backgroundColor: isDark ? "#060911" : "#f1f5f9",
      backgroundImage: isDark
        ? "radial-gradient(circle at 50% 20%, rgba(14, 165, 233, 0.12) 0%, rgba(6, 9, 17, 0.98) 80%)"
        : "radial-gradient(circle at 50% 20%, rgba(14, 165, 233, 0.08) 0%, rgba(241, 245, 249, 0.98) 80%)",
      color: isDark ? "#f8fafc" : "#0f172a",
      position: "relative",
      overflowX: "hidden",
      transition: "background-color 0.25s ease, color 0.25s ease",
    }}>
      {/* 1. Stage: Initial Loading Screen (0% to 100% Lung Structure) */}
      {stage === "intro" && (
        <IntroLoader onComplete={() => setStage("upload")} />
      )}

      {/* 2. Top Header Navigation */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* 3. Subtle Translucent Breathing Lungs Background with Blood Flow in Veins & Air Exchange */}
      <BiopulmonaryBackground />

      {/* 4. Stage: Blood Rushing Through Veins Transition */}
      {stage === "transitioning" && (
        <VeinTransition onComplete={() => setStage("results")} />
      )}

      {/* 5. Stage: Upload Page */}
      {stage === "upload" && (
        <UploadView
          selectedFile={selectedFile}
          setSelectedFile={setSelectedFile}
          previewUrl={previewUrl}
          setPreviewUrl={setPreviewUrl}
          onAnalyzeAndTransition={handleAnalyzeAndTransition}
          onSelectSample={handleSelectSample}
          activeCaseId={activeCaseId}
        />
      )}

      {/* 6. Stage: Dedicated Results Page */}
      {stage === "results" && (
        <ResultsDashboard
          activeCase={activeCase}
          selectedFile={selectedFile}
          previewUrl={previewUrl}
          onBackToUpload={() => setStage("upload")}
        />
      )}
    </div>
  );
}
