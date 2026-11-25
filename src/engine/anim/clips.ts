// Upgraded Roblox Story Animation Clips (30 fps, seekable) — inspired by viral Roblox Shorts pacing.
// Adds natural walk/run bounce, talkBounce, panicFlail, armsCrossed, shockJump, shoveForward, lookAround, sitIdle, fallSpin, etc.
import { evalTrack, Key } from "../core/ease";
import { Registry } from "../core/registry";

export type Pose = Record<string, number>;
export type Clip = { loop?: boolean; period?: number; tracks: Record<string, Key[]> };

export const clips = new Registry<Clip>("clip");
const both = (name: string, keys: Key[]) => ({ ["L." + name]: keys, ["R." + name]: keys });

// --- Core clips (upgraded with subtle life & bounce) ---
clips.add("rest", {
  loop: true, period: 48,
  tracks: {
    rootY: [{ f: 0, v: 0 }, { f: 24, v: 0.04, ease: "sine" }, { f: 48, v: 0, ease: "sine" }],
    ...both("shoulderRoll", [{ f: 0, v: 3 }, { f: 24, v: 5, ease: "sine" }, { f: 48, v: 3, ease: "sine" }]),
  },
});

clips.add("shrugOut", {
  tracks: {
    ...both("shoulderRoll", [{ f: 0, v: 3 }, { f: 3, v: 46, ease: "backOut" }, { f: 16, v: 36, ease: "settle" }]),
    ...both("shoulderPitch", [{ f: 0, v: 0 }, { f: 3, v: 24, ease: "snap" }, { f: 16, v: 18, ease: "settle" }]),
    headRoll: [{ f: 0, v: 0 }, { f: 4, v: 8, ease: "backOut" }, { f: 16, v: 5, ease: "settle" }],
  },
});

clips.add("wave", {
  tracks: {
    "R.shoulderPitch": [{ f: 0, v: 0 }, { f: 3, v: 165, ease: "snap" }, { f: 26, v: 165 }, { f: 28, v: 0, ease: "snap" }],
    "R.shoulderRoll": [{ f: 0, v: 0 }, { f: 3, v: 72, ease: "snap" }, { f: 8.75, v: 24, ease: "sine" }, { f: 14.5, v: 72, ease: "sine" }, { f: 20.25, v: 24, ease: "sine" }, { f: 26, v: 72, ease: "sine" }, { f: 28, v: 0, ease: "snap" }],
    headRoll: [{ f: 0, v: 0 }, { f: 4, v: -6, ease: "sine" }, { f: 26, v: -6 }, { f: 28, v: 0, ease: "sine" }],
  },
});

clips.add("handUpQuick", {
  tracks: {
    "R.shoulderPitch": [{ f: 0, v: 0 }, { f: 2, v: 122, ease: "backOut" }],
    "R.shoulderRoll": [{ f: 0, v: 0 }, { f: 2, v: 18, ease: "snap" }],
    torsoPitch: [{ f: 0, v: 0 }, { f: 3, v: 5, ease: "snap" }],
  },
});

clips.add("pointUp", {
  tracks: {
    "R.shoulderPitch": [{ f: 0, v: 0 }, { f: 2, v: 138, ease: "snap" }, { f: 3, v: 148, ease: "backOut" }, { f: 5, v: 140 }, { f: 18, v: 140 }, { f: 20, v: 0, ease: "snap" }],
    "R.shoulderRoll": [{ f: 0, v: 0 }, { f: 3, v: 20, ease: "snap" }, { f: 18, v: 20 }, { f: 20, v: 0, ease: "snap" }],
    headPitch: [{ f: 0, v: 0 }, { f: 3, v: -8, ease: "snap" }, { f: 18, v: -8 }, { f: 20, v: 0, ease: "snap" }],
  },
});

clips.add("armsUp", {
  tracks: {
    ...both("shoulderPitch", [{ f: 0, v: 0 }, { f: 2, v: 162, ease: "backOut" }]),
    ...both("shoulderRoll", [{ f: 0, v: 0 }, { f: 2, v: 24, ease: "snap" }]),
    rootY: [{ f: 0, v: 0 }, { f: 3, v: 0.14, ease: "backOut" }, { f: 7, v: 0, ease: "settle" }],
  },
});

clips.add("castForward", {
  tracks: {
    "R.shoulderPitch": [{ f: 0, v: 0 }, { f: 6, v: 100, ease: "backOut" }, { f: 9, v: 92 }],
    torsoPitch: [{ f: 0, v: 0 }, { f: 4, v: 8, ease: "snap" }, { f: 10, v: -8, ease: "snap" }],
  },
});

clips.add("castUpBoth", {
  tracks: {
    ...both("shoulderPitch", [{ f: 0, v: 0 }, { f: 4, v: 152, ease: "backOut" }]),
    ...both("shoulderRoll", [{ f: 0, v: 0 }, { f: 4, v: 26, ease: "snap" }]),
    torsoPitch: [{ f: 0, v: 0 }, { f: 4, v: -8, ease: "snap" }],
  },
});

clips.add("reachForward", {
  tracks: {
    "R.shoulderPitch": [{ f: 0, v: 0 }, { f: 3, v: 68, ease: "snap" }],
    torsoPitch: [{ f: 0, v: 0 }, { f: 4, v: 8, ease: "smooth" }],
  },
});

clips.add("presentPlate", {
  tracks: {
    "R.shoulderPitch": [{ f: 0, v: 0 }, { f: 10, v: 82, ease: "smooth" }],
    "L.shoulderPitch": [{ f: 0, v: 0 }, { f: 10, v: 25, ease: "smooth" }],
  },
});

clips.add("cheerLoop", {
  loop: true, period: 12,
  tracks: {
    "L.shoulderPitch": [{ f: 0, v: 148 }, { f: 6, v: 176, ease: "sine" }, { f: 12, v: 148, ease: "sine" }],
    "R.shoulderPitch": [{ f: 0, v: 176 }, { f: 6, v: 148, ease: "sine" }, { f: 12, v: 176, ease: "sine" }],
    ...both("shoulderRoll", [{ f: 0, v: 22 }]),
    rootY: [{ f: 0, v: 0 }, { f: 3, v: 0.22, ease: "sine" }, { f: 6, v: 0, ease: "sine" }, { f: 9, v: 0.22, ease: "sine" }, { f: 12, v: 0, ease: "sine" }],
  },
});

// Upgraded walk with snappy vertical step bounce + slight torso forward lean
clips.add("walk", {
  loop: true, period: 18,
  tracks: {
    torsoPitch: [{ f: 0, v: 6 }],
    rootY: [{ f: 0, v: 0 }, { f: 4.5, v: 0.14, ease: "sine" }, { f: 9, v: 0, ease: "sine" }, { f: 13.5, v: 0.14, ease: "sine" }, { f: 18, v: 0, ease: "sine" }],
    "L.shoulderPitch": [{ f: 0, v: -34 }, { f: 9, v: 34, ease: "sine" }, { f: 18, v: -34, ease: "sine" }],
    "R.shoulderPitch": [{ f: 0, v: 34 }, { f: 9, v: -34, ease: "sine" }, { f: 18, v: 34, ease: "sine" }],
    "L.hipPitch": [{ f: 0, v: 40 }, { f: 9, v: -40, ease: "sine" }, { f: 18, v: 40, ease: "sine" }],
    "R.hipPitch": [{ f: 0, v: -40 }, { f: 9, v: 40, ease: "sine" }, { f: 18, v: -40, ease: "sine" }],
  },
});

// Upgraded run with energetic arm pump + high step bounce (like Love Chains / Say Day chase shots)
clips.add("runLeaning", {
  loop: true, period: 12,
  tracks: {
    torsoPitch: [{ f: 0, v: 22 }],
    headPitch: [{ f: 0, v: -16 }],
    rootY: [{ f: 0, v: 0 }, { f: 3, v: 0.26, ease: "sine" }, { f: 6, v: 0, ease: "sine" }, { f: 9, v: 0.26, ease: "sine" }, { f: 12, v: 0, ease: "sine" }],
    "L.shoulderPitch": [{ f: 0, v: -55 }, { f: 6, v: 65, ease: "sine" }, { f: 12, v: -55, ease: "sine" }],
    "R.shoulderPitch": [{ f: 0, v: 65 }, { f: 6, v: -55, ease: "sine" }, { f: 12, v: 65, ease: "sine" }],
    ...both("shoulderRoll", [{ f: 0, v: 12 }]),
    "L.hipPitch": [{ f: 0, v: 60 }, { f: 6, v: -60, ease: "sine" }, { f: 12, v: 60, ease: "sine" }],
    "R.hipPitch": [{ f: 0, v: -60 }, { f: 6, v: 60, ease: "sine" }, { f: 12, v: -60, ease: "sine" }],
  },
});

// --- NEW Viral Story Animation Clips ---

/** Energetic storytelling idle while speaking (prevents stiff mannequin look) */
clips.add("talkBounce", {
  loop: true, period: 16,
  tracks: {
    rootY: [{ f: 0, v: 0 }, { f: 4, v: 0.08, ease: "sine" }, { f: 8, v: 0, ease: "sine" }, { f: 12, v: 0.06, ease: "sine" }, { f: 16, v: 0, ease: "sine" }],
    headPitch: [{ f: 0, v: 0 }, { f: 4, v: 5, ease: "sine" }, { f: 8, v: -2, ease: "sine" }, { f: 12, v: 4, ease: "sine" }, { f: 16, v: 0, ease: "sine" }],
    headRoll: [{ f: 0, v: -3 }, { f: 8, v: 3, ease: "sine" }, { f: 16, v: -3, ease: "sine" }],
    "R.shoulderPitch": [{ f: 0, v: 18 }, { f: 8, v: 38, ease: "sine" }, { f: 16, v: 18, ease: "sine" }],
    "L.shoulderPitch": [{ f: 0, v: 10 }, { f: 8, v: 22, ease: "sine" }, { f: 16, v: 10, ease: "sine" }],
    ...both("shoulderRoll", [{ f: 0, v: 8 }, { f: 8, v: 14, ease: "sine" }, { f: 16, v: 8, ease: "sine" }]),
  },
});

/** Frantic screaming/panicking arms waving (for disaster & crowd reaction beats) */
clips.add("panicFlail", {
  loop: true, period: 10,
  tracks: {
    "L.shoulderPitch": [{ f: 0, v: 135 }, { f: 5, v: 175, ease: "sine" }, { f: 10, v: 135, ease: "sine" }],
    "R.shoulderPitch": [{ f: 0, v: 175 }, { f: 5, v: 135, ease: "sine" }, { f: 10, v: 175, ease: "sine" }],
    ...both("shoulderRoll", [{ f: 0, v: 26 }, { f: 5, v: 42, ease: "sine" }, { f: 10, v: 26, ease: "sine" }]),
    headYaw: [{ f: 0, v: -12 }, { f: 5, v: 12, ease: "sine" }, { f: 10, v: -12, ease: "sine" }],
    rootY: [{ f: 0, v: 0 }, { f: 2.5, v: 0.14, ease: "sine" }, { f: 5, v: 0, ease: "sine" }, { f: 7.5, v: 0.14, ease: "sine" }, { f: 10, v: 0, ease: "sine" }],
  },
});

/** Instant surprise jump (great on reveal cuts and sound-word impacts) */
clips.add("shockJump", {
  tracks: {
    rootY: [{ f: 0, v: 0 }, { f: 3, v: 0.55, ease: "backOut" }, { f: 8, v: 0, ease: "settle" }],
    ...both("shoulderPitch", [{ f: 0, v: 0 }, { f: 3, v: 115, ease: "snap" }, { f: 12, v: 85, ease: "settle" }]),
    ...both("shoulderRoll", [{ f: 0, v: 0 }, { f: 3, v: 48, ease: "backOut" }, { f: 12, v: 32, ease: "settle" }]),
    torsoPitch: [{ f: 0, v: 0 }, { f: 3, v: -10, ease: "snap" }, { f: 10, v: 0, ease: "settle" }],
  },
});

/** Defiant crossed/folded stance with smug head tilt */
clips.add("armsCrossed", {
  tracks: {
    ...both("shoulderPitch", [{ f: 0, v: 48 }]),
    ...both("shoulderRoll", [{ f: 0, v: -14 }]),
    headYaw: [{ f: 0, v: -10 }],
    headRoll: [{ f: 0, v: 6 }],
  },
});

/** Dramatic villain/hero accusatory point (lean forward + locked arm) */
clips.add("dramaticPoint", {
  tracks: {
    "R.shoulderPitch": [{ f: 0, v: 0 }, { f: 3, v: 105, ease: "backOut" }],
    "R.shoulderRoll": [{ f: 0, v: 0 }, { f: 3, v: 10, ease: "snap" }],
    "L.shoulderPitch": [{ f: 0, v: 0 }, { f: 3, v: -15, ease: "snap" }],
    torsoPitch: [{ f: 0, v: 0 }, { f: 3, v: 12, ease: "snap" }],
    headPitch: [{ f: 0, v: 0 }, { f: 3, v: -8, ease: "snap" }],
  },
});

/** Two-handed shove / push interaction */
clips.add("shoveForward", {
  tracks: {
    ...both("shoulderPitch", [{ f: 0, v: 20 }, { f: 4, v: 108, ease: "backOut" }, { f: 12, v: 75, ease: "settle" }]),
    torsoPitch: [{ f: 0, v: -6 }, { f: 4, v: 16, ease: "snap" }, { f: 12, v: 6, ease: "settle" }],
  },
});

/** Nervous left-right head scan */
clips.add("lookAround", {
  loop: true, period: 32,
  tracks: {
    headYaw: [{ f: 0, v: 0 }, { f: 8, v: 28, ease: "smooth" }, { f: 16, v: 0, ease: "smooth" }, { f: 24, v: -28, ease: "smooth" }, { f: 32, v: 0, ease: "smooth" }],
    ...both("shoulderRoll", [{ f: 0, v: 10 }]),
  },
});

/** Emphatic head shake ("no!") */
clips.add("headShake", {
  tracks: {
    headYaw: [{ f: 0, v: 0 }, { f: 3, v: -24, ease: "snap" }, { f: 6, v: 24, ease: "snap" }, { f: 9, v: -18, ease: "snap" }, { f: 12, v: 0, ease: "settle" }],
  },
});

/** Agreement nod ("yes") */
clips.add("nodYes", {
  tracks: {
    headPitch: [{ f: 0, v: 0 }, { f: 4, v: 18, ease: "snap" }, { f: 8, v: -4, ease: "snap" }, { f: 12, v: 14, ease: "snap" }, { f: 16, v: 0, ease: "settle" }],
  },
});

/** Crying / trembling emotional beat */
clips.add("cryShake", {
  loop: true, period: 8,
  tracks: {
    torsoPitch: [{ f: 0, v: 12 }],
    headPitch: [{ f: 0, v: 14 }, { f: 4, v: 18, ease: "sine" }, { f: 8, v: 14, ease: "sine" }],
    headRoll: [{ f: 0, v: -4 }, { f: 4, v: 4, ease: "sine" }, { f: 8, v: -4, ease: "sine" }],
    ...both("shoulderPitch", [{ f: 0, v: 80 }, { f: 4, v: 88, ease: "sine" }, { f: 8, v: 80, ease: "sine" }]),
    ...both("shoulderRoll", [{ f: 0, v: -8 }]),
  },
});

/** Seated pose for kitchen table, benches, or chairs */
clips.add("sitIdle", {
  loop: true, period: 40,
  tracks: {
    rootY: [{ f: 0, v: -0.75 }],
    ...both("hipPitch", [{ f: 0, v: 84 }]),
    ...both("shoulderPitch", [{ f: 0, v: 22 }, { f: 20, v: 26, ease: "sine" }, { f: 40, v: 22, ease: "sine" }]),
    headPitch: [{ f: 0, v: 0 }, { f: 20, v: 4, ease: "sine" }, { f: 40, v: 0, ease: "sine" }],
  },
});

/** Mid-air dramatic fall / leap flail */
clips.add("fallSpin", {
  loop: true, period: 10,
  tracks: {
    torsoPitch: [{ f: 0, v: -18 }],
    "L.shoulderPitch": [{ f: 0, v: 145 }, { f: 5, v: 175, ease: "sine" }, { f: 10, v: 145, ease: "sine" }],
    "R.shoulderPitch": [{ f: 0, v: 175 }, { f: 5, v: 145, ease: "sine" }, { f: 10, v: 175, ease: "sine" }],
    "L.hipPitch": [{ f: 0, v: 35 }, { f: 5, v: -35, ease: "sine" }, { f: 10, v: 35, ease: "sine" }],
    "R.hipPitch": [{ f: 0, v: -35 }, { f: 5, v: 35, ease: "sine" }, { f: 10, v: -35, ease: "sine" }],
  },
});

/** pose of a clip at local frame f (frames since the clip started). Pure and seekable. */
export const evalClip = (id: string, f: number): Pose => {
  const c = clips.get(id);
  const lf = c.loop && c.period ? ((f % c.period) + c.period) % c.period : f;
  const pose: Pose = {};
  for (const [name, keys] of Object.entries(c.tracks)) pose[name] = evalTrack(keys, lf);
  return pose;
};
