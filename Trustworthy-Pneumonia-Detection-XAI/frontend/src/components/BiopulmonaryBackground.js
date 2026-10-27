"use client";

import React, { useEffect, useRef } from "react";

export default function BiopulmonaryBackground() {
  const canvasRef = useRef(null);

  // Animated green wake shock waves, air exchange gas particles & circulating blood corpuscles
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let animationFrameId;

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", handleResize);

    const centerX = () => width / 2;
    const centerY = () => height / 2;

    // Green wake shockwaves radiating across the entire screen
    const shockwaves = [
      { r: 40, maxR: Math.max(width, height) * 0.9, speed: 2.2, alpha: 0.8 },
      { r: 240, maxR: Math.max(width, height) * 0.9, speed: 2.2, alpha: 0.5 },
      { r: 440, maxR: Math.max(width, height) * 0.9, speed: 2.2, alpha: 0.2 },
    ];

    // Air exchange & bio-energy particles
    const particles = [];
    const numAir = 45;
    const numBlood = 40;

    for (let i = 0; i < numAir; i++) {
      particles.push({
        type: "air",
        x: centerX() + (Math.random() - 0.5) * width * 0.8,
        y: centerY() + (Math.random() - 0.5) * height * 0.8,
        radius: Math.random() * 2.5 + 1.2,
        vx: (Math.random() - 0.5) * 0.5,
        vy: -Math.random() * 0.8 - 0.2, // drifting upward
        alpha: Math.random() * 0.6 + 0.2,
        color: Math.random() > 0.4 ? "rgba(16, 185, 129, " : "rgba(34, 211, 238, ",
      });
    }

    // Vascular branching coordinates
    const branches = [
      { start: [-10, -80], cp: [-120, -30], end: [-260, 80] },
      { start: [-20, -50], cp: [-100, 60], end: [-220, 160] },
      { start: [-15, -90], cp: [-110, -130], end: [-200, -170] },
      { start: [10, -80], cp: [120, -30], end: [260, 80] },
      { start: [20, -50], cp: [100, 60], end: [220, 160] },
      { start: [15, -90], cp: [110, -130], end: [200, -170] },
    ];

    for (let i = 0; i < numBlood; i++) {
      const branch = branches[Math.floor(Math.random() * branches.length)];
      particles.push({
        type: "blood",
        branch,
        t: Math.random(),
        speed: 0.003 + Math.random() * 0.004,
        radius: Math.random() * 2.5 + 1.4,
        isOxygenated: Math.random() > 0.5,
      });
    }

    const getBezierPoint = (t, p0, p1, p2) => {
      const oneMinusT = 1 - t;
      return oneMinusT * oneMinusT * p0 + 2 * oneMinusT * t * p1 + t * t * p2;
    };

    let step = 0;

    const render = () => {
      step += 0.02;
      ctx.clearRect(0, 0, width, height);

      const cx = centerX();
      const cy = centerY();

      // 1. Draw subtle ambient Green Wake Shockwaves (Gentle & Minimal)
      for (let sw of shockwaves) {
        sw.r += sw.speed * 0.7;
        sw.alpha = Math.max(0, 0.35 * (1 - sw.r / sw.maxR));

        if (sw.r >= sw.maxR) {
          sw.r = 20;
          sw.alpha = 0.35;
        }

        ctx.save();
        ctx.beginPath();
        ctx.arc(cx, cy, sw.r, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(16, 185, 129, ${sw.alpha * 0.25})`;
        ctx.lineWidth = 1;
        ctx.stroke();
        ctx.restore();
      }

      // 2. Render air exchange & bio particles
      for (let p of particles) {
        if (p.type === "air") {
          p.x += p.vx;
          p.y += p.vy;
          if (p.y < 0 || p.y > height || p.x < 0 || p.x > width) {
            p.x = cx + (Math.random() - 0.5) * width * 0.7;
            p.y = cy + (Math.random() - 0.2) * height * 0.6;
          }
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
          ctx.fillStyle = `${p.color}${p.alpha})`;
          ctx.shadowColor = "#10b981";
          ctx.shadowBlur = 8;
          ctx.fill();
        } else if (p.type === "blood") {
          p.t += p.speed;
          if (p.t > 1) p.t = 0;

          const b = p.branch;
          const px = cx + getBezierPoint(p.t, b.start[0], b.cp[0], b.end[0]);
          const py = cy + getBezierPoint(p.t, b.start[1], b.cp[1], b.end[1]);

          ctx.beginPath();
          ctx.arc(px, py, p.radius, 0, Math.PI * 2);
          if (p.isOxygenated) {
            ctx.fillStyle = "rgba(239, 68, 68, 0.85)";
            ctx.shadowColor = "rgba(239, 68, 68, 0.7)";
          } else {
            ctx.fillStyle = "rgba(34, 211, 238, 0.85)";
            ctx.shadowColor = "rgba(34, 211, 238, 0.7)";
          }
          ctx.shadowBlur = 8;
          ctx.fill();
        }
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div style={{
      position: "fixed",
      inset: 0,
      pointerEvents: "none",
      zIndex: 0,
      overflow: "hidden",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    }}>
      {/* 1. Full-Viewport Green Bio-Wake Shock Pulsars (CSS Animated expanding rings) */}
      <div
        className="animate-wake-shock-1"
        style={{
          position: "absolute",
          width: "420px",
          height: "420px",
          borderRadius: "50%",
          border: "1px solid rgba(16, 185, 129, 0.2)",
          pointerEvents: "none",
        }}
      />
      <div
        className="animate-wake-shock-2"
        style={{
          position: "absolute",
          width: "420px",
          height: "420px",
          borderRadius: "50%",
          border: "1px solid rgba(16, 185, 129, 0.2)",
          pointerEvents: "none",
        }}
      />
      <div
        className="animate-wake-shock-3"
        style={{
          position: "absolute",
          width: "420px",
          height: "420px",
          borderRadius: "50%",
          border: "1px solid rgba(16, 185, 129, 0.2)",
          pointerEvents: "none",
        }}
      />

      {/* 2. Soft Ambient Pulmonic Green Halo */}
      <div style={{
        position: "absolute",
        width: "700px",
        height: "700px",
        borderRadius: "50%",
        background: "radial-gradient(circle, rgba(16, 185, 129, 0.06) 0%, rgba(6, 182, 212, 0.02) 50%, transparent 70%)",
        filter: "blur(60px)",
      }} />

      {/* 3. Expansive Pure SVG Vascular Pulmonary Network (Minimal & Subtle) */}
      <svg
        viewBox="0 0 1000 1000"
        style={{
          position: "absolute",
          width: "800px",
          height: "800px",
          opacity: 0.12,
        }}
      >
        <defs>
          <linearGradient id="bioWakeGreenGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#10b981" stopOpacity="0.9" />
            <stop offset="50%" stopColor="#22d3ee" stopOpacity="0.6" />
            <stop offset="100%" stopColor="#059669" stopOpacity="0.9" />
          </linearGradient>
        </defs>

        {/* Trachea to Bronchial Tree */}
        <path
          d="M 500,200 L 500,380 C 500,430 400,490 300,580"
          fill="none"
          stroke="url(#bioWakeGreenGrad)"
          strokeWidth="3"
          strokeDasharray="10 8"
          className="animate-vein-flow"
        />
        <path
          d="M 500,380 C 500,430 600,490 700,580"
          fill="none"
          stroke="url(#bioWakeGreenGrad)"
          strokeWidth="3"
          strokeDasharray="10 8"
          className="animate-vein-flow"
          style={{ animationDelay: "1s" }}
        />

        {/* Branching secondary bronchioles */}
        <path
          d="M 400,490 C 340,540 270,510 220,600"
          fill="none"
          stroke="rgba(16, 185, 129, 0.7)"
          strokeWidth="2"
          strokeDasharray="8 6"
          className="animate-vein-flow"
          style={{ animationDelay: "0.5s" }}
        />
        <path
          d="M 600,490 C 660,540 730,510 780,600"
          fill="none"
          stroke="rgba(34, 211, 238, 0.7)"
          strokeWidth="2"
          strokeDasharray="8 6"
          className="animate-vein-flow"
          style={{ animationDelay: "1.5s" }}
        />
        <path
          d="M 500,350 C 450,320 380,300 310,360"
          fill="none"
          stroke="rgba(0, 255, 136, 0.6)"
          strokeWidth="1.8"
          strokeDasharray="6 6"
          className="animate-vein-flow"
          style={{ animationDelay: "2s" }}
        />
        <path
          d="M 500,350 C 550,320 620,300 690,360"
          fill="none"
          stroke="rgba(0, 255, 136, 0.6)"
          strokeWidth="1.8"
          strokeDasharray="6 6"
          className="animate-vein-flow"
          style={{ animationDelay: "2.5s" }}
        />
      </svg>

      {/* 4. Canvas for dynamic Green Wake shock pulses and circulating bio-particles */}
      <canvas
        ref={canvasRef}
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
        }}
      />
    </div>
  );
}
