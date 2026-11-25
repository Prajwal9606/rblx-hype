// 3D Sculpted Roblox Hair & Neon Headphones builder (aligned cleanly above brows on 0.62-radius, 1.2-tall head).
import * as THREE from "three";

export type HairStyle =
  | "sidePart" | "bob" | "long" | "ponytail" | "tufts" | "bun"
  | "curly" | "spikyTop" | "hypeSpiky" | "bald" | "beanie" | "rainHat";

const cap = (r: number, h: number, seg = 14) => {
  const g = new THREE.SphereGeometry(r, seg, 6, 0, Math.PI * 2, 0, Math.PI / 2);
  g.scale(1, h / r, 1);
  return g;
};

const add = (
  grp: THREE.Group,
  geo: THREE.BufferGeometry,
  mat: THREE.Material,
  p: [number, number, number],
  rot: [number, number, number] = [0, 0, 0],
  s: [number, number, number] = [1, 1, 1]
) => {
  const m = new THREE.Mesh(geo, mat);
  m.position.set(...p);
  m.rotation.set(...rot);
  m.scale.set(...s);
  m.castShadow = true;
  m.receiveShadow = true;
  grp.add(m);
  return m;
};

/** 3D RBLX HYPE Over-Ear Neon Headphones (dark frame + glowing purple/cyan earcup rings) */
export const buildNeonHeadphones = () => {
  const grp = new THREE.Group();
  const frameMat = new THREE.MeshStandardMaterial({ color: "#191c28", roughness: 0.42, metalness: 0.25 });
  const purpleGlow = new THREE.MeshStandardMaterial({ color: "#9b4dff", emissive: "#7c3aed", emissiveIntensity: 0.9, roughness: 0.25 });
  const cyanGlow = new THREE.MeshStandardMaterial({ color: "#38e8ff", emissive: "#06b6d4", emissiveIntensity: 0.85, roughness: 0.25 });

  // Headband arc sitting cleanly over the hair crown
  const band = new THREE.Mesh(new THREE.TorusGeometry(0.69, 0.062, 10, 28, Math.PI), frameMat);
  band.position.set(0, 0.64, -0.02);
  band.castShadow = true;
  grp.add(band);

  // Subtle purple accent strip along top of headband
  const bandTrim = new THREE.Mesh(new THREE.TorusGeometry(0.71, 0.022, 8, 24, Math.PI * 0.72), purpleGlow);
  bandTrim.position.set(0, 0.64, -0.02);
  bandTrim.rotation.z = Math.PI * 0.14;
  grp.add(bandTrim);

  // Left and right earcups with outer purple & inner cyan neon rings
  for (const sx of [-1, 1]) {
    const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.16, 20), frameMat);
    cup.rotation.z = Math.PI / 2;
    cup.position.set(sx * 0.67, 0.60, -0.02);
    cup.castShadow = true;
    grp.add(cup);

    const outerRing = new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.032, 10, 20), purpleGlow);
    outerRing.rotation.y = Math.PI / 2;
    outerRing.position.set(sx * 0.755, 0.60, -0.02);
    grp.add(outerRing);

    const innerDot = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.085, 0.03, 16), cyanGlow);
    innerDot.rotation.z = Math.PI / 2;
    innerDot.position.set(sx * 0.76, 0.60, -0.02);
    grp.add(innerDot);
  }
  return grp;
};

/** 3D Layered Anime Spiky Hair sculpted to match the RBLX HYPE mascot */
const buildHypeSpiky = (grp: THREE.Group, color: string) => {
  const mat = new THREE.MeshStandardMaterial({ color, roughness: 0.68, metalness: 0.05 });
  const R = 0.68;
  // Smooth fitted crown cap raised above brow line
  add(grp, cap(R, 0.42, 16), mat, [0, 0.96, -0.03], [-0.08, 0, 0], [1.03, 1, 1.05]);
  // Full 3D back hair volume so side/rear shots look solid
  add(grp, new THREE.SphereGeometry(0.64, 14, 10), mat, [0, 0.74, -0.26], [0, 0, 0], [1.04, 0.78, 0.72]);

  // Layered spiky crown tufts (angled outward like the RBLX HYPE artwork)
  const lock = new THREE.ConeGeometry(0.19, 0.62, 5);
  const crownSpecs: [[number, number, number], [number, number, number], [number, number, number]][] = [
    [[0.0, 1.48, -0.02], [-0.15, 0.2, 0.12], [1.15, 1.15, 1.0]],
    [[-0.28, 1.40, 0.06], [0.05, 0.5, 0.58], [1.0, 1.05, 0.9]],
    [[0.30, 1.40, 0.04], [-0.05, -0.4, -0.62], [1.0, 1.08, 0.9]],
    [[-0.46, 1.24, -0.08], [-0.15, 0.8, 0.95], [0.9, 0.95, 0.85]],
    [[0.46, 1.24, -0.10], [-0.15, -0.8, -0.95], [0.9, 0.95, 0.85]],
    [[0.0, 1.32, -0.38], [-0.75, 0, 0], [1.1, 1.0, 0.95]],
    [[-0.28, 1.18, -0.42], [-0.85, 0.3, 0.4], [0.95, 0.92, 0.85]],
    [[0.28, 1.18, -0.42], [-0.85, -0.3, -0.4], [0.95, 0.92, 0.85]],
  ];
  for (const [p, r, s] of crownSpecs) add(grp, lock, mat, p, r, s);

  // Swept anime front bangs (pointing down & sideways cleanly ABOVE the eyes)
  const bang = new THREE.ConeGeometry(0.13, 0.42, 4);
  add(grp, bang, mat, [-0.26, 1.02, 0.54], [2.55, 0, 0.35], [1.0, 0.9, 0.75]);
  add(grp, bang, mat, [0.02, 1.04, 0.58], [2.62, 0, -0.18], [1.05, 0.95, 0.75]);
  add(grp, bang, mat, [0.28, 1.01, 0.52], [2.50, 0, -0.42], [0.95, 0.85, 0.75]);

  // Angled sideburns framing the face
  for (const sx of [-1, 1]) {
    add(grp, bang, mat, [sx * 0.58, 0.80, 0.22], [Math.PI, 0, sx * 0.14], [0.65, 0.85, 0.85]);
  }
};

export const buildHair = (style: HairStyle, color: string) => {
  const grp = new THREE.Group();
  if (style === "bald") return grp;
  if (style === "hypeSpiky" || style === "spikyTop") {
    buildHypeSpiky(grp, color);
    return grp;
  }

  const mat = new THREE.MeshStandardMaterial({ color, roughness: 0.72, flatShading: true });
  const smooth = new THREE.MeshStandardMaterial({ color, roughness: 0.72 });
  const R = 0.675;
  const spike = new THREE.ConeGeometry(0.16, 0.44, 5);
  const box = new THREE.BoxGeometry(1, 1, 1);

  switch (style) {
    case "sidePart": {
      const dome = new THREE.SphereGeometry(0.72, 16, 8, 0, Math.PI * 2, 0, Math.PI * 0.52);
      add(grp, dome, smooth, [0, 0.92, -0.05], [-0.26, 0, -0.14], [1, 0.84, 1.04]);
      add(grp, new THREE.SphereGeometry(0.32, 12, 8), smooth, [0.22, 1.12, 0.34], [0, 0, -0.3], [1.28, 0.5, 1]);
      add(grp, new THREE.SphereGeometry(0.62, 12, 8), smooth, [0, 0.76, -0.26], [0, 0, 0], [1.02, 0.72, 0.68]);
      for (const sx of [-1, 1]) add(grp, spike, smooth, [sx * 0.6, 0.82, 0.1], [Math.PI, 0, 0], [0.35, 0.55, 0.8]);
      break;
    }
    case "bob":
      add(grp, cap(R, 0.4, 14), smooth, [0, 1.0, 0]);
      add(grp, box, smooth, [0, 0.48, -0.35], [0, 0, 0], [1.38, 1.05, 0.66]);
      for (const sx of [-1, 1]) add(grp, box, smooth, [sx * 0.62, 0.52, 0], [0, 0, 0], [0.18, 1.0, 0.9]);
      add(grp, box, smooth, [0, 1.06, 0.53], [0, 0, 0], [1.14, 0.18, 0.16]);
      break;
    case "long":
      add(grp, cap(R + 0.04, 0.46, 14), smooth, [0, 1.0, 0]);
      add(grp, box, smooth, [0, 0.16, -0.41], [0.08, 0, 0], [1.44, 1.9, 0.62]);
      add(grp, box, smooth, [0.64, 0.06, 0.2], [0, 0, 0.08], [0.34, 1.8, 0.4]);
      add(grp, box, smooth, [-0.64, 0.52, 0.05], [0, 0, 0], [0.18, 1.0, 0.8]);
      add(grp, spike, smooth, [0.2, 1.08, 0.52], [1.75, 0, 0.9], [1.1, 1.05, 0.6]);
      break;
    case "ponytail":
      add(grp, cap(R + 0.02, 0.44, 14), smooth, [0, 1.0, 0]);
      add(grp, box, smooth, [0, 0.72, -0.32], [0, 0, 0], [1.32, 0.6, 0.7]);
      add(grp, new THREE.CylinderGeometry(0.18, 0.28, 1.55, 10), smooth, [0.0, 0.15, -0.72], [0.25, 0, 0]);
      break;
    case "tufts":
      add(grp, cap(R, 0.38, 12), mat, [0, 1.02, 0]);
      add(grp, new THREE.SphereGeometry(0.6, 10, 8), mat, [0, 0.78, -0.24], [0, 0, 0], [1.0, 0.68, 0.64]);
      for (let i = 0; i < 6; i++) {
        add(grp, spike, mat, [Math.cos(i * 1.05) * 0.36, 1.32, Math.sin(i * 1.05) * 0.36], [Math.sin(i) * 0.5, 0, Math.cos(i * 2) * 0.5], [0.85, 0.75, 0.85]);
      }
      break;
    case "bun":
      add(grp, cap(R, 0.38, 14), smooth, [0, 1.02, 0]);
      add(grp, new THREE.SphereGeometry(0.28, 12, 10), smooth, [0, 1.50, -0.14]);
      break;
    case "curly":
      for (let i = 0; i < 11; i++) {
        const rad = i < 9 ? 0.44 : 0.18;
        add(grp, new THREE.SphereGeometry(0.29, 10, 8), smooth, [Math.cos(i * 0.72) * rad, 1.06 + (i % 3) * 0.12, Math.sin(i * 0.72) * rad - 0.06]);
      }
      break;
    case "rainHat":
      add(grp, cap(R + 0.04, 0.56, 20), smooth, [0, 0.95, 0]);
      add(grp, new THREE.CylinderGeometry(R + 0.42, R + 0.5, 0.09, 24), smooth, [0, 0.97, -0.06], [-0.12, 0, 0]);
      break;
    case "beanie":
      add(grp, cap(R + 0.03, 0.56, 20), smooth, [0, 0.94, 0]);
      add(grp, new THREE.CylinderGeometry(R + 0.06, R + 0.06, 0.18, 20), smooth, [0, 0.98, 0]);
      break;
  }
  return grp;
};
