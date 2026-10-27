import "./globals.css";
import { ThemeProvider } from "../context/ThemeContext";

export const metadata = {
  title: "trustworthy-pneumonia-detector | Trust-Aware Explainable Deep Learning",
  description: "Trustworthy Pneumonia Detection from Chest Radiographs with Monte Carlo Dropout uncertainty estimation, temperature-scaled calibration, and Grad-CAM explainability.",
  icons: {
    icon: "/assets/logo.svg",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" data-theme="dark">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="icon" href="/assets/logo.svg" type="image/svg+xml" />
      </head>
      <body>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
