import React from "react";
import { Img, staticFile, useVideoConfig } from "remotion";

/**
 * Top-right channel watermark (logo + "RBLX HYPE" text) rendered over all Final videos.
 * Scales proportionally with video height (baseline 960 px).
 */
export const Watermark: React.FC = () => {
  const { height } = useVideoConfig();
  const k = height / 960;

  return (
    <div
      style={{
        position: "absolute",
        top: 22 * k,
        right: 22 * k,
        display: "flex",
        alignItems: "center",
        gap: 10 * k,
        padding: `${6 * k}px ${12 * k}px ${6 * k}px ${6 * k}px`,
        borderRadius: 14 * k,
        background: "rgba(10, 12, 22, 0.48)",
        border: `${1.5 * k}px solid rgba(255, 255, 255, 0.18)`,
        boxShadow: `0 ${4 * k}px ${14 * k}px rgba(0, 0, 0, 0.45)`,
        opacity: 0.9,
        pointerEvents: "none",
      }}
    >
      <Img
        src={staticFile("watermark-logo.jpg")}
        style={{
          width: 40 * k,
          height: 40 * k,
          borderRadius: 9 * k,
          objectFit: "cover",
          display: "block",
        }}
      />
      <span
        style={{
          fontFamily: '"CaptionFont", "Poppins", system-ui, sans-serif',
          fontWeight: 700,
          fontSize: 18 * k,
          letterSpacing: 0.6 * k,
          color: "#FCFCFC",
          textShadow: `0 ${2 * k}px ${4 * k}px rgba(0, 0, 0, 0.85)`,
          whiteSpace: "nowrap",
          lineHeight: 1,
        }}
      >
        RBLX HYPE
      </span>
    </div>
  );
};
