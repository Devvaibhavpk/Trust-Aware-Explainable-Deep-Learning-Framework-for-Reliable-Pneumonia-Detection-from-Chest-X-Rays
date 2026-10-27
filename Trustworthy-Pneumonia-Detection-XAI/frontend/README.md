# trustworthy-pneumonia-detector · Frontend

A clinical-grade Next.js web application for the **Trust-Aware Explainable Deep Learning Framework for Reliable Pneumonia Detection from Chest X-Rays**.

## Tech Stack
- **Framework**: Next.js 16 (App Router)
- **UI**: React 19, Vanilla CSS
- **Charts**: Recharts 3
- **Backend bridge**: Next.js API Route → Python inference pipeline

## Features

| Feature | Description |
|---|---|
| 🫁 Animated Loader | Full-screen lung structure loading animation (0 → 100%) |
| 🩺 Upload & Classify | Drag-and-drop CXR upload with live ResNet-18 inference |
| 🔬 Grad-CAM Viewer | Side-by-side Original / Radiograph / Grad-CAM overlay tabs |
| 📊 MC Dropout Chart | 30-pass epistemic uncertainty histogram (Recharts) |
| 🧠 Trust Score | Composite TrustEngine™ score with reliability badge |
| 📋 CDS Report Modal | Exportable Clinical Decision Support report (print-ready) |
| 🌗 Dark / Light Mode | Toggle between PACS workstation dark and clinical light themes |
| 💉 Vein Transition | Blood-flow animation on navigation to results |

## Run Locally

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

## Architecture

```
frontend/
├── src/
│   ├── app/
│   │   ├── api/predict/route.js   # Next.js API → Python inference bridge
│   │   ├── globals.css            # CSS design system (dark/light variables)
│   │   ├── layout.js              # Root layout + ThemeProvider
│   │   └── page.js                # Stage state machine (intro→upload→results)
│   ├── components/
│   │   ├── IntroLoader.js         # Lung loading animation
│   │   ├── BiopulmonaryBackground.js  # Animated canvas background
│   │   ├── Header.js              # Logo + dark/light mode toggle
│   │   ├── UploadView.js          # Drag-and-drop upload + sample selection
│   │   ├── VeinTransition.js      # Blood-vein transition animation
│   │   ├── ResultsDashboard.js    # Main results layout
│   │   ├── AnatomyViewer.js       # Anatomy / Radiograph / Grad-CAM viewer
│   │   ├── TrustUncertaintyChart.js  # MC Dropout histogram + inference summary
│   │   └── ReportModal.js         # CDS clinical report modal
│   └── context/
│       └── ThemeContext.js        # Theme state + localStorage persistence
└── public/assets/                 # Static assets (logo, CXR images, Grad-CAM maps)
```

## Theme System

The app supports full **Dark Mode** (PACS workstation) and **Light Mode** (clinical workstation) via:
- CSS custom properties in `[data-theme="dark"]` / `[data-theme="light"]`
- `useTheme()` hook from `ThemeContext.js`
- Toggle button in the header; preference persisted to `localStorage`
