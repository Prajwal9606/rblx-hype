// RBLX HYPE Neon + Comic Impact Tilt captions (Option 3 + Option 5 mix).
// Drop-in replacement for src/remotion/Captions.tsx — keeps full API compatibility with Final.tsx and build-video.ts.
import React, { useEffect, useState } from "react";
import { continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export type Caption = { w: string; f: number }; // text as displayed, first frame

const FONT = "CaptionFont";
const EM_PER_XHEIGHT = 1 / 0.548;
const ASCENT = 1.05;

export const CAPTION_TUNE = {
  xHeight: 40, // slightly punchier than 36 for comic impact
  baseline: 684, // at 960 px frame height (71% frame height, clear of faces)
  outline: 4.5,
  shadowX: 4,
  shadowY: 5,
};

export const useCaptionFont = () => {
  const [ready, setReady] = useState(false);
  useEffect(() => {
    const h = delayRender("caption font");
    const face = new FontFace(FONT, `url(${staticFile("fonts/Poppins-Bold.ttf")})`);
    face.load().then((f) => {
      (document.fonts as unknown as { add: (f: FontFace) => void }).add(f);
      setReady(true);
      continueRender(h);
    });
  }, []);
  return ready;
};

export const Captions: React.FC<{ captions: Caption[] }> = ({ captions }) => {
  const frame = useCurrentFrame();
  const { height, width } = useVideoConfig();
  const ready = useCaptionFont();

  let activeIdx = -1;
  for (let i = 0; i < captions.length; i++) {
    if (captions[i].f <= frame) activeIdx = i;
    else break;
  }
  if (!ready || activeIdx < 0) return null;

  const active = captions[activeIdx];
  const word = active.w;
  const age = Math.max(0, frame - active.f);

  // Detect SFX / ALL-CAPS punch words vs normal words
  const isPunch = word.length >= 2 && word === word.toUpperCase() && /[A-Z]/.test(word);
  // Detect capitalised character names (e.g. Bram, Grandpa, Puddle)
  const isName = !isPunch && word.length > 1 && word[0] === word[0].toUpperCase() && word[0] !== word[0].toLowerCase();

  const k = height / 960;
  const baseSize = CAPTION_TUNE.xHeight * EM_PER_XHEIGHT * k * (isPunch ? 1.22 : 1.0);

  // Snappy 3-frame comic pop-in scale
  const popScale = interpolate(age, [0, 2, 4], [0.84, 1.07, 1.0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Alternating comic tilt (-2.4 deg / +2.4 deg) and stronger -5 deg slam on punch words
  const tiltDeg = isPunch ? -5 : activeIdx % 2 === 0 ? -2.4 : 2.4;

  const sx = CAPTION_TUNE.shadowX * k * (isPunch ? 1.35 : 1.0);
  const sy = CAPTION_TUNE.shadowY * k * (isPunch ? 1.35 : 1.0);
  const strokePx = CAPTION_TUNE.outline * 2 * k * (isPunch ? 1.2 : 1.0);

  const fillColor = isPunch ? "#38E8FF" : isName ? "#7CEFFF" : "#FFFFFF";
  const glowColor = isPunch ? "rgba(56, 232, 255, 0.85)" : "rgba(155, 77, 255, 0.90)";
  const glowOuter = isPunch ? "rgba(155, 77, 255, 0.75)" : "rgba(56, 232, 255, 0.45)";

  const common: React.CSSProperties = {
    position: "absolute",
    left: 0,
    width,
    textAlign: "center",
    whiteSpace: "nowrap",
    top: CAPTION_TUNE.baseline * k - ASCENT * baseSize,
    fontFamily: FONT,
    fontSize: baseSize,
    lineHeight: 1.35,
    fontWeight: 700,
    letterSpacing: isPunch ? 1.5 * k : 0.4 * k,
    WebkitTextStroke: `${strokePx}px #0B0614`,
    paintOrder: "stroke fill",
    transformOrigin: "center center",
  };

  const transformMain = `scale(${popScale.toFixed(3)}) rotate(${tiltDeg}deg)`;
  const transformShadow = `translate(${sx.toFixed(1)}px, ${sy.toFixed(1)}px) scale(${popScale.toFixed(3)}) rotate(${tiltDeg}deg)`;

  return (
    <>
      {/* Heavy comic block shadow */}
      <div style={{ ...common, color: "#000000", WebkitTextStroke: `${strokePx}px #000000`, transform: transformShadow }}>
        {word}
      </div>
      {/* Neon purple/cyan RBLX HYPE glow + crisp fill */}
      <div
        style={{
          ...common,
          color: fillColor,
          transform: transformMain,
          textShadow: `0 0 ${14 * k}px ${glowColor}, 0 0 ${28 * k}px ${glowOuter}`,
        }}
      >
        {word}
      </div>
    </>
  );
};

/** Caption text rules: uppercase punch/SFX words, capitalised names & "I", clean punchy display. */
export const captionText = (spoken: string, names: string[] = [], sfx: string[] = []) => {
  const bare = spoken.replace(/[^\p{L}\p{N}'’-]/gu, "").replace(/’/g, "'");
  const low = bare.toLowerCase();
  if (sfx.some((x) => x.toLowerCase() === low)) return bare.toUpperCase() + "!";
  const name = names.find((x) => x.toLowerCase() === low);
  if (name) return name;
  if (low === "i" || low.startsWith("i'")) return "I" + low.slice(1);
  return low;
};
