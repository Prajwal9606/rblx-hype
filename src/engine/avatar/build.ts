// Roblox Starter Rig 3D Avatar Builder: beveled limbs, 7 starter presets, 3D hair, auto neon headphones for Hype, and HD Roblox faces.
import * as THREE from "three";
import type { BodyType, CharacterDef } from "../../schema/cast";
import type { Pose } from "../anim/clips";
import { faceKey, type FaceOpts } from "./faces";
import { buildHair, buildNeonHeadphones } from "./hair";
import { armSide, headTexture, legSide, torsoFront, torsoSide } from "./outfits";

type RigDims = {
  torso: [number, number, number];
  arm: [number, number, number];
  leg: [number, number, number];
  bevel: number;
  armGap: number;
  legGap: number;
  restRollDeg: number;
  headScale: number;
};

const RIG_PRESETS: Record<BodyType, RigDims> = {
  blocky:    { torso: [1.94, 1.98, 0.98], arm: [0.92, 1.96, 0.94], leg: [0.93, 1.98, 0.96], bevel: 0.085, armGap: 0.04, legGap: 0.04, restRollDeg: 2.5, headScale: 1.06 },
  boy:       { torso: [1.80, 1.94, 0.92], arm: [0.80, 1.92, 0.84], leg: [0.84, 1.96, 0.88], bevel: 0.13,  armGap: 0.05, legGap: 0.05, restRollDeg: 3.5, headScale: 1.08 },
  girl:      { torso: [1.66, 1.92, 0.86], arm: [0.74, 1.90, 0.78], leg: [0.78, 1.96, 0.82], bevel: 0.15,  armGap: 0.05, legGap: 0.05, restRollDeg: 4.0, headScale: 1.08 },
  man:       { torso: [2.04, 2.02, 1.02], arm: [0.88, 2.00, 0.92], leg: [0.92, 2.00, 0.94], bevel: 0.14,  armGap: 0.05, legGap: 0.05, restRollDeg: 3.0, headScale: 1.04 },
  woman:     { torso: [1.62, 1.96, 0.84], arm: [0.72, 1.92, 0.76], leg: [0.78, 1.98, 0.82], bevel: 0.16,  armGap: 0.05, legGap: 0.05, restRollDeg: 4.0, headScale: 1.06 },
  r20:       { torso: [1.88, 1.98, 0.96], arm: [0.84, 1.96, 0.88], leg: [0.88, 1.98, 0.92], bevel: 0.16,  armGap: 0.05, legGap: 0.05, restRollDeg: 3.0, headScale: 1.06 },
  superhero: { torso: [2.14, 2.04, 1.06], arm: [0.94, 2.00, 0.96], leg: [0.94, 2.02, 0.96], bevel: 0.15,  armGap: 0.05, legGap: 0.05, restRollDeg: 3.5, headScale: 1.04 },
};

const geoCache = new Map<string, THREE.BufferGeometry>();
const robloxBox = (w: number, h: number, d: number, bevel: number): THREE.BufferGeometry => {
  const key = `${w}_${h}_${d}_${bevel}`;
  const cached = geoCache.get(key);
  if (cached) return cached;
  const r = Math.min(bevel, w * 0.45, h * 0.45, d * 0.45);
  const geo = new THREE.BoxGeometry(w, h, d, 6, 6, 6);
  const pos = geo.getAttribute("position");
  const hx = w / 2 - r;
  const hy = h / 2 - r;
  const hz = d / 2 - r;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i);
    const cx = Math.max(-hx, Math.min(hx, x));
    const cy = Math.max(-hy, Math.min(hy, y));
    const cz = Math.max(-hz, Math.min(hz, z));
    const dx = x - cx, dy = y - cy, dz = z - cz;
    const len = Math.hypot(dx, dy, dz);
    if (len > 1e-6) pos.setXYZ(i, cx + (dx / len) * r, cy + (dy / len) * r, cz + (dz / len) * r);
  }
  geo.computeVertexNormals();
  geoCache.set(key, geo);
  return geo;
};

const HEAD_PROFILE: [number, number][] = [
  [0, 0], [0.38, 0], [0.54, 0.07], [0.61, 0.19], [0.62, 0.32],
  [0.62, 0.90], [0.59, 1.05], [0.49, 1.16], [0.34, 1.2], [0, 1.2],
];
let HEAD: THREE.BufferGeometry | null = null;
export const headGeometry = () => {
  if (HEAD) return HEAD;
  HEAD = new THREE.LatheGeometry(HEAD_PROFILE.map(([r, y]) => new THREE.Vector2(r, y)), 40, -Math.PI, Math.PI * 2);
  const pos = HEAD.getAttribute("position"), uv = HEAD.getAttribute("uv");
  for (let i = 0; i < uv.count; i++) uv.setY(i, pos.getY(i) / 1.2);
  HEAD.computeVertexNormals();
  return HEAD;
};

const NECK = new THREE.CylinderGeometry(0.28, 0.32, 0.22, 16);
const ROUGH = 0.76;
const mat = (o: THREE.MeshStandardMaterialParameters) => new THREE.MeshStandardMaterial({ roughness: ROUGH, metalness: 0.03, ...o });
const d2r = Math.PI / 180;

export class Avatar {
  readonly root = new THREE.Group();
  private lean = new THREE.Group();
  private head = new THREE.Group();
  private shoulder: Record<"L" | "R", THREE.Group> = { L: new THREE.Group(), R: new THREE.Group() };
  private hip: Record<"L" | "R", THREE.Group> = { L: new THREE.Group(), R: new THREE.Group() };
  private headMat: THREE.MeshStandardMaterial;
  private expression = "";
  private dims: RigDims;

  constructor(readonly def: CharacterDef, expression = "neutralTalk") {
    const { skin, outfit } = def;
    this.dims = RIG_PRESETS[def.body ?? "boy"];
    const { torso: [tw, th, td], arm: [aw, ah, ad], leg: [lw, lh, ld], bevel, armGap, legGap, headScale } = this.dims;

    this.root.add(this.lean);
    const shadow = (m: THREE.Mesh) => { m.castShadow = true; m.receiveShadow = true; return m; };

    const hipY = lh;
    const shoulderY = hipY + th;

    const side = mat({ map: torsoSide(outfit.torso) });
    const top = mat({ color: outfit.torso.color });
    const torso = shadow(new THREE.Mesh(robloxBox(tw, th, td, bevel), [side, side, top, top, mat({ map: torsoFront(outfit.torso) }), side]));
    torso.position.y = hipY + th / 2;
    this.lean.add(torso);

    const neck = shadow(new THREE.Mesh(NECK, mat({ color: skin })));
    neck.position.y = shoulderY + 0.05;
    this.lean.add(neck);

    const armM = mat({ map: armSide(outfit, skin) });
    const armTop = mat({ color: outfit.sleeves?.color ?? outfit.torso.color });
    const hand = mat({ color: skin });
    const legM = mat({ map: legSide(outfit, skin) });
    const legTop = mat({ color: outfit.legs.color });
    const sole = mat({ color: outfit.legs.shoes ?? "#0c0a0e" });

    const armGeo = robloxBox(aw, ah, ad, bevel * 0.9);
    const legGeo = robloxBox(lw, lh, ld, bevel * 0.85);

    for (const s of ["L", "R"] as const) {
      const sx = s === "L" ? 1 : -1;
      this.shoulder[s].position.set(sx * (tw / 2 + armGap), shoulderY, 0);
      this.shoulder[s].rotation.order = "ZXY";
      const arm = shadow(new THREE.Mesh(armGeo, [armM, armM, armTop, hand, armM, armM]));
      arm.position.set(sx * (aw / 2), -ah / 2, 0);
      this.shoulder[s].add(arm);
      this.lean.add(this.shoulder[s]);

      this.hip[s].position.set(sx * (lw / 2 + legGap / 2), hipY, 0);
      const leg = shadow(new THREE.Mesh(legGeo, [legM, legM, legTop, sole, legM, legM]));
      leg.position.y = -lh / 2;
      this.hip[s].add(leg);
      this.lean.add(this.hip[s]);
    }

    this.head.position.set(0, shoulderY + 0.06, 0);
    this.head.scale.setScalar(headScale);
    this.headMat = mat({ roughness: 0.65 });
    this.head.add(shadow(new THREE.Mesh(headGeometry(), this.headMat)));
    this.head.add(buildHair(def.hair.style, def.hair.color));

    // Auto-add RBLX HYPE neon headphones whenever headphones: true OR purple-trimmed Hype hero is detected
    const hasPurpleTrim =
      ("trim" in outfit.torso && outfit.torso.trim?.toLowerCase() === "#9b4dff") ||
      outfit.sleeves?.cuff?.toLowerCase() === "#9b4dff";
    if (def.headphones === true || (def.headphones !== false && hasPurpleTrim)) {
      this.head.add(buildNeonHeadphones());
    }

    this.lean.add(this.head);
    this.setPose({});
    this.setExpression(expression);
  }

  showOnlyHead() {
    for (const c of this.lean.children) c.visible = c === this.head;
  }

  setExpression(name: string, opts?: FaceOpts) {
    const key = faceKey(name, opts) + (this.def.faceStyle ?? "roblox");
    if (key === this.expression) return;
    this.expression = key;
    this.headMat.map = headTexture(this.def.skin, name, opts, this.def.faceStyle ?? "roblox");
    this.headMat.needsUpdate = true;
  }

  setPose(p: Pose) {
    const v = (k: string) => p[k] ?? 0;
    const baseRoll = this.dims.restRollDeg;
    for (const s of ["L", "R"] as const) {
      const sx = s === "L" ? 1 : -1;
      const pitch = v(`${s}.shoulderPitch`);
      const roll = v(`${s}.shoulderRoll`) || baseRoll;
      this.shoulder[s].rotation.set(-pitch * d2r, 0, sx * roll * d2r * (Math.cos(pitch * d2r) >= 0 ? 1 : -1));
      this.hip[s].rotation.set(-v(`${s}.hipPitch`) * d2r, 0, 0);
    }
    this.head.rotation.set(v("headPitch") * d2r, v("headYaw") * d2r, v("headRoll") * d2r, "YXZ");
    this.lean.rotation.x = v("torsoPitch") * d2r;
    this.lean.position.y = v("rootY");
  }

  handAnchor(s: "L" | "R") {
    const a = new THREE.Object3D();
    const { arm: [aw, ah] } = this.dims;
    a.position.set((s === "L" ? 1 : -1) * (aw / 2), -ah, 0);
    this.shoulder[s].add(a);
    return a;
  }
}
