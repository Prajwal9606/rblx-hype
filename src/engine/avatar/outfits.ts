// Clothing (including RBLX HYPE neon purple circuit hoodie) & Roblox HD Face textures.
import * as THREE from "three";
import { drawFace, EXPRESSIONS, faceKey, type FaceOpts } from "./faces";

export type TorsoPrint =
  | { kind: "plain"; color: string }
  | { kind: "varsity"; color: string; strip: string; trim?: string }
  | { kind: "cyberHoodie"; color: string; trim: string; accent?: string }
  | { kind: "stripes"; color: string; color2: string; bands?: number }
  | { kind: "plaid"; color: string; color2: string }
  | { kind: "coat"; color: string; trim: string };

export type Outfit = {
  torso: TorsoPrint;
  sleeves?: { color: string; length?: number; cuff?: string };
  legs: { color: string; length?: number; shoes?: string };
};

const cache = new Map<string, THREE.Texture>();
const tex = (key: string, w: number, h: number, draw: (g: CanvasRenderingContext2D) => void) => {
  let t = cache.get(key);
  if (!t) {
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    draw(c.getContext("2d")!);
    t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = 8;
    cache.set(key, t);
  }
  return t;
};

const hdFaceImages = new Map<string, HTMLImageElement | "failed">();
const hdFaceListeners = new Map<string, (() => void)[]>();

const getRobloxFaceImage = (expression: string, onLoad?: () => void): HTMLImageElement | null => {
  const existing = hdFaceImages.get(expression);
  if (existing === "failed") return null;
  if (existing && existing.complete && existing.naturalWidth > 0) return existing;
  if (onLoad) {
    const list = hdFaceListeners.get(expression) ?? [];
    list.push(onLoad);
    hdFaceListeners.set(expression, list);
  }
  if (!existing && typeof Image !== "undefined") {
    const img = new Image();
    img.crossOrigin = "anonymous";
    hdFaceImages.set(expression, img);
    img.onload = () => {
      const cbs = hdFaceListeners.get(expression) ?? [];
      hdFaceListeners.delete(expression);
      cbs.forEach((fn) => fn());
    };
    img.onerror = () => {
      hdFaceImages.set(expression, "failed");
      hdFaceListeners.delete(expression);
    };
    img.src = `/faces/${expression}.png`;
  }
  return null;
};

const hem = (g: CanvasRenderingContext2D, S: number, trim: string, u0 = 0, u1 = 1) => {
  g.fillStyle = trim;
  g.fillRect(u0 * S, 0.91 * S, (u1 - u0) * S, 0.08 * S);
  g.fillStyle = "rgba(0,0,0,0.28)";
  for (let x = u0 * S; x < u1 * S; x += S * 0.04) g.fillRect(x, 0.91 * S, 3, 0.08 * S);
};

const drawCyberHoodieFront = (g: CanvasRenderingContext2D, S: number, baseCol: string, trim: string, accent = "#38e8ff") => {
  g.fillStyle = baseCol;
  g.fillRect(0, 0, S, S);
  // Hoodie collar & kangaroo pocket
  g.fillStyle = "rgba(0,0,0,0.34)";
  g.fillRect(0.22 * S, 0.64 * S, 0.56 * S, 0.25 * S);
  g.strokeStyle = trim;
  g.lineWidth = 0.022 * S;
  g.lineCap = "round";
  g.lineJoin = "round";
  // Drawstrings
  for (const u of [0.42, 0.58]) {
    g.beginPath(); g.moveTo(u * S, 0.06 * S); g.lineTo(u * S, 0.34 * S); g.stroke();
  }
  // Neon purple geometric circuit lines matching RBLX HYPE art
  const lines: [number, number][][] = [
    [[0.14, 0.12], [0.30, 0.26], [0.22, 0.48], [0.32, 0.62]],
    [[0.86, 0.12], [0.70, 0.26], [0.78, 0.48], [0.68, 0.62]],
    [[0.10, 0.50], [0.20, 0.56], [0.20, 0.84]],
    [[0.90, 0.50], [0.80, 0.56], [0.80, 0.84]],
  ];
  for (const pts of lines) {
    g.beginPath();
    pts.forEach(([x, y], i) => (i ? g.lineTo(x * S, y * S) : g.moveTo(x * S, y * S)));
    g.stroke();
  }
  // Subtle cyan node dots
  g.fillStyle = accent;
  for (const [x, y] of [[0.30, 0.26], [0.70, 0.26], [0.32, 0.62], [0.68, 0.62]]) {
    g.beginPath(); g.arc(x * S, y * S, 0.018 * S, 0, Math.PI * 2); g.fill();
  }
  hem(g, S, trim, 0, 1);
};

const body = (g: CanvasRenderingContext2D, S: number, p: TorsoPrint) => {
  g.fillStyle = p.color; g.fillRect(0, 0, S, S);
  if (p.kind === "stripes") {
    const n = p.bands ?? 7; g.fillStyle = p.color2;
    for (let i = 0; i < n; i++) g.fillRect(0, ((i * 2 + 1) / (n * 2)) * S, S, S / (n * 2));
  }
  if (p.kind === "plaid") {
    g.fillStyle = p.color2; g.globalAlpha = 0.55;
    for (let i = 0; i < 4; i++) { g.fillRect(((i * 2 + 1) / 8) * S, 0, S / 8, S); g.fillRect(0, ((i * 2 + 1) / 8) * S, S, S / 8); }
    g.globalAlpha = 1;
  }
};

export const torsoFront = (p: TorsoPrint) =>
  tex("tf" + JSON.stringify(p), 512, 512, (g) => {
    const S = 512;
    if (p.kind === "cyberHoodie" || (p.kind === "varsity" && p.trim?.toLowerCase() === "#9b4dff")) {
      drawCyberHoodieFront(g, S, p.color, p.trim ?? "#9b4dff", p.kind === "cyberHoodie" ? p.accent : "#38e8ff");
      return;
    }
    body(g, S, p);
    if (p.kind === "varsity") {
      const trim = p.trim ?? "#f2efec";
      g.fillStyle = p.strip; g.fillRect(0.38 * S, 0, 0.205 * S, S);
      g.fillStyle = trim;
      for (const v of [0.09, 0.27, 0.45, 0.62, 0.79, 0.96]) { g.beginPath(); g.arc(0.36 * S, v * S, 0.015 * S, 0, Math.PI * 2); g.fill(); }
      hem(g, S, trim, 0, 0.33); hem(g, S, trim, 0.64, 1);
    }
    if (p.kind === "coat") {
      const dark = "rgba(0,0,0,0.28)", light = "rgba(255,255,255,0.16)";
      g.fillStyle = light; g.beginPath(); g.moveTo(0.5 * S, 0.3 * S); g.lineTo(0.2 * S, 0); g.lineTo(0.5 * S, 0); g.closePath(); g.fill();
      g.beginPath(); g.moveTo(0.5 * S, 0.3 * S); g.lineTo(0.8 * S, 0); g.lineTo(0.5 * S, 0); g.closePath(); g.fill();
      g.strokeStyle = dark; g.lineWidth = 0.014 * S; g.beginPath(); g.moveTo(0.2 * S, 0); g.lineTo(0.5 * S, 0.3 * S); g.lineTo(0.8 * S, 0); g.stroke();
      g.beginPath(); g.moveTo(0.5 * S, 0.3 * S); g.lineTo(0.5 * S, S); g.stroke();
      g.fillStyle = p.trim; for (const v of [0.4, 0.52, 0.76, 0.88]) { g.beginPath(); g.arc(0.56 * S, v * S, 0.024 * S, 0, Math.PI * 2); g.fill(); }
      g.fillStyle = dark; g.fillRect(0, 0.6 * S, S, 0.085 * S);
      g.fillStyle = p.trim; g.fillRect(0.44 * S, 0.59 * S, 0.12 * S, 0.105 * S);
    }
  });

export const torsoSide = (p: TorsoPrint) =>
  tex("ts" + JSON.stringify(p), 256, 256, (g) => {
    body(g, 256, p);
    if (p.kind === "cyberHoodie" || p.kind === "varsity") hem(g, 256, p.trim ?? "#f2efec");
    if (p.kind === "coat") { g.fillStyle = "rgba(0,0,0,0.28)"; g.fillRect(0, 0.6 * 256, 256, 0.085 * 256); }
  });

export const armSide = (o: Outfit, skin: string) => {
  const s = o.sleeves ?? { color: o.torso.color };
  return tex("as" + JSON.stringify(s) + skin, 128, 256, (g) => {
    const len = s.length ?? 1;
    g.fillStyle = skin; g.fillRect(0, 0, 128, 256);
    g.fillStyle = s.color; g.fillRect(0, 0, 128, 256 * len);
    if (s.cuff) {
      g.fillStyle = s.cuff; g.fillRect(0, 256 * 0.85, 128, 256 * 0.14);
      g.fillStyle = s.color; g.fillRect(0, 256 * 0.895, 128, 4); g.fillRect(0, 256 * 0.945, 128, 4);
      // Neon lightning stripe down Hype's sleeve
      if (s.cuff.toLowerCase() === "#9b4dff") {
        g.strokeStyle = s.cuff; g.lineWidth = 6;
        g.beginPath(); g.moveTo(64, 18); g.lineTo(44, 110); g.lineTo(78, 175); g.lineTo(64, 215); g.stroke();
      }
    }
  });
};

export const legSide = (o: Outfit, skin: string) =>
  tex("ls" + JSON.stringify(o.legs) + skin, 128, 256, (g) => {
    const len = o.legs.length ?? 1;
    g.fillStyle = skin; g.fillRect(0, 0, 128, 256);
    g.fillStyle = o.legs.color; g.fillRect(0, 0, 128, 256 * len);
    g.fillStyle = o.legs.shoes ?? "#0c0a0e"; g.fillRect(0, 256 * 0.89, 128, 256 * 0.11);
  });

const paintHeadCanvas = (g: CanvasRenderingContext2D, skin: string, expression: string, opts: FaceOpts | undefined, hdImg: HTMLImageElement | null) => {
  const spec = EXPRESSIONS[expression];
  if (!spec) throw new Error(`unknown expression "${expression}"`);
  g.fillStyle = skin; g.fillRect(0, 0, 1024, 512);
  for (let x = 0; x < 1024; x += 4) {
    const ang = Math.abs((x / 1024 - 0.5) * Math.PI * 2), k = Math.min(1, Math.max(0, (ang - 0.75) / 1.3));
    g.fillStyle = `rgba(70,30,22,${(0.28 * k * k).toFixed(3)})`; g.fillRect(x, 0, 4, 512);
  }
  const top = g.createLinearGradient(0, 0, 0, 140); top.addColorStop(0, "rgba(60,25,18,0.3)"); top.addColorStop(1, "rgba(60,25,18,0)");
  g.fillStyle = top; g.fillRect(0, 0, 1024, 140);
  const chin = g.createLinearGradient(0, 430, 0, 512); chin.addColorStop(0, "rgba(60,25,18,0)"); chin.addColorStop(1, "rgba(60,25,18,0.32)");
  g.fillStyle = chin; g.fillRect(0, 430, 1024, 82);

  const F = 512, face = document.createElement("canvas");
  face.width = face.height = F;
  const fg = face.getContext("2d")!;
  if (hdImg && !opts?.blink) {
    const pad = F * 0.10, size = F - pad * 2;
    fg.drawImage(hdImg, pad, pad + F * 0.03, size, size);
  } else {
    drawFace(fg, F, spec, opts);
  }
  for (let x = 0; x < 1024; x++) {
    const ang = (x / 1024 - 0.5) * Math.PI * 2;
    if (Math.abs(ang) > 1.4) continue;
    const sx = (0.5 + Math.sin(ang) / 2) * F;
    g.drawImage(face, sx, 0, 1, F, x, 0, 1, 512);
  }
};

export const headTexture = (skin: string, expression: string, opts?: FaceOpts, faceStyle: "roblox" | "drawn" = "roblox") => {
  const key = "hd" + faceStyle + skin + faceKey(expression, opts);
  let t = cache.get(key);
  if (!t) {
    const c = document.createElement("canvas");
    c.width = 1024; c.height = 512;
    const g = c.getContext("2d")!;
    t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = 8;
    cache.set(key, t);
    const redraw = () => {
      const loaded = getRobloxFaceImage(expression);
      if (loaded) { paintHeadCanvas(g, skin, expression, opts, loaded); t!.needsUpdate = true; }
    };
    const hdImg = faceStyle === "roblox" ? getRobloxFaceImage(expression, redraw) : null;
    paintHeadCanvas(g, skin, expression, opts, hdImg);
  }
  return t;
};
