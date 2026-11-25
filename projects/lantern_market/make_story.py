"""Writes story.json for 'Midnight Lantern Market'.
Usage: .venv/Scripts/python projects/lantern_market/make_story.py (run from studio root)
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, "words.json"), encoding="utf-8"))["words"]
fr = lambda i: round(W[i]["t"] * 30)
shots = []

# ---------------------------------------------------------------- scenes & looks
BLUE_SKY = {
    "top": "#4f86d8", "horizon": "#b4d2f4", "gradientHeight": 0.5,
    "haze": "#e2edf9", "hazeHeight": 0.06,
    "cloudLight": "#ffffff", "cloudDark": "#aebcd8", "cloudCover": 0.36, "cloudScale": 1.3, "cloudSeed": 5,
}
FOG = {
    "sky": BLUE_SKY,
    "fog": {"color": "#cfdcf2", "density": 0.0026},
    "lights": {
        "hemi": {"sky": "#dfe6ff", "ground": "#9a948c", "intensity": 0.95},
        "key": {"color": "#fff0d8", "intensity": 3.2, "from": [0.55, 0.62, 0.6], "shadow": True},
    },
}
DUSK = {
    "sky": {
        "top": "#6d528a", "horizon": "#e8a0a0", "gradientHeight": 0.55,
        "haze": "#eab0a8", "hazeHeight": 0.06,
        "cloudLight": "#f6c8c0", "cloudDark": "#8f6488", "cloudCover": 0.5, "cloudScale": 1.2, "cloudSeed": 4,
    },
    "lights": {
        "hemi": {"sky": "#c79ab4", "ground": "#4a2a30", "intensity": 1.0},
        "key": {"color": "#ffc4a4", "intensity": 2.2, "from": [0.4, 0.5, 0.8], "shadow": True},
    },
}
LATE_POST = {
    "toneMapping": "none", "exposure": 0.84,
    "bloom": {"strength": 0.25, "radius": 0.6, "threshold": 0.95},
    "ao": {"radius": 1.2, "intensity": 1.0},
    "grade": {"saturation": 1.05, "contrast": 1.0, "lift": [0, 0, 0], "gain": [1.03, 0.99, 0.94], "gamma": 1, "vignette": 0},
}
LATE = {
    "sky": BLUE_SKY,
    "fog": {"color": "#d8ceb8", "density": 0.0024},
    "lights": {
        "hemi": {"sky": "#e8cdb8", "ground": "#8a6a58", "intensity": 0.85},
        "key": {"color": "#ffe2c0", "intensity": 2.4, "from": [0.5, 0.45, 0.7], "shadow": True},
    },
    "post": LATE_POST,
}
NIGHT_POST = {
    "toneMapping": "none", "exposure": 1.0,
    "bloom": {"strength": 0.34, "radius": 0.8, "threshold": 0.92},
    "ao": {"radius": 1.5, "intensity": 1.0},
    "grade": {"saturation": 1.05, "contrast": 1.0, "lift": [0, 0, 0], "gain": [1.04, 0.97, 0.92], "gamma": 1, "vignette": 0},
}
NIGHT_L = {
    "post": NIGHT_POST,
    "lights": {
        "hemi": {"sky": "#8a6674", "ground": "#2e1c22", "intensity": 1.45},
        "key": {"color": "#ffe4d4", "intensity": 2.7, "from": [0.35, 0.6, 0.8], "shadow": True},
    },
}
BLACKOUT_L = {
    "post": {**NIGHT_POST, "exposure": 0.72, "bloom": {"strength": 0.22, "radius": 0.6, "threshold": 0.95}},
    "lights": {
        "hemi": {"sky": "#2a2e48", "ground": "#141622", "intensity": 1.15},
        "key": {"color": "#a8b8e0", "intensity": 1.6, "from": [0.35, 0.6, 0.8], "shadow": True},
    },
}
KITCH_L = {
    "lights": {
        "hemi": {"sky": "#e6ddd2", "ground": "#8a7a6a", "intensity": 1.65},
        "key": {"color": "#ffe6c0", "intensity": 2.4, "from": [-0.55, 0.6, 0.65], "shadow": True},
    },
}
SIGN_AWAY = {"sign": {"x": -9.55, "y": -80, "z": -18, "w": 4, "h": 7, "panel": "#786a92", "trim": "#847690", "glyph": "#8f8068", "yaw": 0}}

SCENES = {
    "plazaN": dict(set="tabletPlaza", setParams=SIGN_AWAY, look="NIGHT_EMBER", lookOverrides=NIGHT_L, shadow={"focus": [0, 0, -4], "extent": 34}),
    "plazaDark": dict(set="tabletPlaza", setParams=SIGN_AWAY, look="NIGHT_EMBER", lookOverrides=BLACKOUT_L, shadow={"focus": [0, 0, -4], "extent": 34}),
    "plaza": dict(set="tabletPlaza", setParams=SIGN_AWAY, look="DAY_COOL", lookOverrides=FOG, shadow={"focus": [0, 0, -4], "extent": 30}),
    "street": dict(set="fireStreet", setParams={"bowls": None}, look="DAY_SUN", lookOverrides=FOG, shadow={"focus": [0, 0, -8], "extent": 44}),
    "dusk": dict(set="fireStreet", setParams={"houses": {"lit": 0.5}}, look="DUSK_MAGENTA", lookOverrides=DUSK, shadow={"focus": [0, 0, -8], "extent": 44}),
    "night": dict(set="fireStreet", setParams={"houses": {"lit": 0.75}, "flames": False}, look="NIGHT_EMBER", lookOverrides=NIGHT_L, shadow={"focus": [0, 0, -8], "extent": 44}),
    "nightDark": dict(set="fireStreet", setParams={"houses": {"lit": 0.0}, "flames": False}, look="NIGHT_EMBER", lookOverrides=BLACKOUT_L, shadow={"focus": [0, 0, -8], "extent": 44}),
    "river": dict(set="waterStreet", setParams={"ground": {"stone": "#cdb98e", "stoneDark": "#a8946c", "gap": "#8a7858"}}, look="DAY_SUN", lookOverrides=FOG, shadow={"focus": [6, 0, -14], "extent": 50}),
    "courtyard": dict(set="waterCourtyard", setParams={"torches": False}, look="DAY_COOL", lookOverrides=FOG, shadow={"focus": [0, 0, -8], "extent": 50}),
    "kitchen": dict(set="kitchen", setParams={"chairs": [], "table": None}, look="INTERIOR_NEUTRAL", lookOverrides=KITCH_L, shadow={"focus": [-4, 3, -3], "extent": 26}),
    "late": dict(set="fireStreet", setParams={"bowls": None}, look="DAY_SUN", lookOverrides=LATE, shadow={"focus": [0, 0, -8], "extent": 44}),
}

# ---------------------------------------------------------------- helpers
TALKERS = {"neutralTalk", "bigHappy", "smug", "angryTalk", "dotSmile", "worried", "deadpan", "happyArcs", "angryFrown", "nervous", "laugh", "eyesClosedTalk"}
PAIR = {
    "neutralTalk": "eyesClosedTalk", "bigHappy": "laugh", "laugh": "bigHappy",
    "worried": "nervous", "nervous": "worried", "blank": "worried", "deadpan": "blank",
    "smug": "happyArcs", "dotSmile": "happyArcs", "happyArcs": "dotSmile",
    "angryFrown": "angryTalk", "angryTalk": "angryFrown", "hollowShock": "blank",
    "scream": "hollowShock", "grittedAngry": "angryTalk", "disgust": "deadpan",
}
HELD = lambda clip: (clip, -990)


def A(ch, x, z, yaw=0, face="neutralTalk", faces=(), clips=(), **kw):
    a = {"character": ch, "pos": [x, z], **({} if yaw is None else {"yaw": yaw}), "faces": [{"f": 0, "v": face}] + [{"word": w, "v": v} for w, v in faces]}
    if clips:
        a["clips"] = [({"clip": c, "word": w} if isinstance(w, int) and w >= 0 else {"clip": c, "at": -w - 1000}) for c, w in clips]
    a.update(kw)
    return a


def cam(target, frm, push=0.2, whip=None, out=None, shake=None, fov=47, rise=0, pan=None, to=None):
    t = list(target)
    p0 = list(frm)
    near = math.dist(p0, t) < 9.5
    p1 = list(to) if to else [p0[i] + (t[i] - p0[i]) * (min(push, 0.05) if near else push * 1.3) for i in range(3)]
    p1[1] += rise
    if not to:
        p1[0] += 0.9 * (1 if p0[0] >= t[0] else -1) * (-1 if len(shots) % 2 else 1)
    keys = []
    if whip:
        keys += [{"f": -1, "pos": p0, "target": [t[0] + whip, t[1], t[2]]}, {"f": 4, "pos": p0, "target": t, "ease": "easeOutCubic"}]
    else:
        keys += [{"u": 0, "pos": p0, "target": t}]
    t1 = pan if pan else t
    if out:
        keys += [{"u": 0.9, "pos": p1, "target": t1, "ease": "linear"}, {"u": 1.07, "pos": p1, "target": [t1[0] + out, t1[1], t1[2]], "ease": "easeInQuart"}]
    else:
        keys += [{"u": 1, "pos": p1, "target": t1, "ease": "linear"}]
    c = {"fov": fov, "keys": keys}
    if shake:
        c["shake"] = shake
    return c


def med(x, z, side=3.0, dist=11.5, h=4.4, ty=3.9, **kw):
    return cam([x, ty, z], [x + side, h, z + dist], **kw)


def close(x, z, side=1.6, dist=8.0, h=4.8, ty=4.7, **kw):
    return cam([x, ty, z], [x + side, h, z + dist], **kw)


def wide(x, z, side=7, dist=30, h=8, ty=5, **kw):
    return cam([x, ty, z], [x + side, h, z + dist], **kw)


def track(target, frm, delta, push=0.0, shake=None):
    t1 = [target[i] + delta[i] for i in range(3)]
    p1 = [frm[i] + delta[i] + (t1[i] - frm[i] - delta[i]) * push for i in range(3)]
    c = {"fov": 47, "keys": [{"u": 0, "pos": list(frm), "target": list(target)}, {"u": 1, "pos": p1, "target": t1, "ease": "linear"}]}
    if shake:
        c["shake"] = shake
    return c


IMPACT = lambda f=0: [{"f0": f, "f1": f + 10, "ampDeg": [0.5, 0.5], "mode": "alt", "decay": 0.75}]
RUMBLE = lambda f=0, n=50: [{"f0": f, "f1": f + n, "ampDeg": [0.04, 0.5], "mode": "alt", "bursts": 2}]

# ---------------------------------------------------------------- props & effects
def LANTERN(x, y, z, scale=1.0, lit=True, glow=0.65):
    col = "#ffb84d" if lit else "#252630"
    trim = "#6a3a22" if lit else "#14161e"
    g = glow if lit else 0.0
    return [
        dict(shape="box", pos=[x, y, z], size=[1.3 * scale, 1.7 * scale, 1.3 * scale], color=col, glow=g),
        dict(shape="box", pos=[x, y + 0.95 * scale, z], size=[1.5 * scale, 0.22 * scale, 1.5 * scale], color=trim),
        dict(shape="box", pos=[x, y - 0.95 * scale, z], size=[1.5 * scale, 0.22 * scale, 1.5 * scale], color=trim),
    ]


def KING_LANTERN(x, z, lit=True, flame_sz=1.8):
    items = LANTERN(x, 4.6, z, scale=2.2, lit=lit, glow=0.5) + [
        dict(shape="box", pos=[x, 1.1, z], size=[3.0, 2.2, 3.0], color="#3e3c48"),
        dict(shape="box", pos=[x, 2.3, z], size=[3.4, 0.3, 3.4], color="#585466"),
    ]
    v = [props(*items)]
    if lit:
        v.append({"type": "flame", "pos": [x, 4.4, z], "size": min(flame_sz, 2.0), "light": 8})
    else:
        v.append({"type": "steam", "pos": [x, 6.2, z], "count": 10, "spread": 3, "rise": 10, "size": 5, "color": "#26242c", "opacity": 0.45})
    return v


MARKET_LANTERNS = (
    LANTERN(-7, 6.2, -6, 0.85) + LANTERN(6.5, 6.8, -8, 0.9) +
    LANTERN(-4, 7.6, -15, 0.8) + LANTERN(4.5, 7.2, -16, 0.85) +
    LANTERN(0, 8.8, -22, 1.0)
)
DARK_LANTERNS = (
    LANTERN(-7, 6.2, -6, 0.85, lit=False) + LANTERN(6.5, 6.8, -8, 0.9, lit=False) +
    LANTERN(-4, 7.6, -15, 0.8, lit=False) + LANTERN(4.5, 7.2, -16, 0.85, lit=False)
)

BIKE = lambda x, z: [
    dict(shape="cyl", pos=[x - 1.1, 0.7, z], size=[0.7, 0.22], color="#22242c", rotX=90),
    dict(shape="cyl", pos=[x + 1.1, 0.7, z], size=[0.7, 0.22], color="#22242c", rotX=90),
    dict(shape="box", pos=[x, 1.25, z], size=[2.0, 0.22, 0.22], color="#28804a"),
    dict(shape="box", pos=[x + 0.8, 1.8, z], size=[0.2, 1.0, 0.2], color="#c8ccd4"),
]
GOLD_BAG = lambda x, y, z: [
    dict(shape="cyl", pos=[x, y, z], size=[0.55, 0.85], color="#d8a830"),
    dict(shape="cyl", pos=[x, y + 0.45, z], size=[0.35, 0.2], color="#b88420"),
]
TROPHY = lambda x, y, z: [
    dict(shape="box", pos=[x, y, z], size=[0.6, 0.3, 0.6], color="#4a3020"),
    dict(shape="cyl", pos=[x, y + 0.55, z], size=[0.42, 0.75], color="#f2c438", glow=0.4),
]
LUNCHBOX = lambda x, y, z: [
    dict(shape="box", pos=[x, y, z], size=[0.85, 0.6, 0.5], color="#d84038"),
    dict(shape="box", pos=[x, y + 0.36, z], size=[0.36, 0.14, 0.14], color="#22242c"),
]

EMBERS = lambda c=(0, 10, -10), n=260, size=0.16: {"type": "embers", "count": n, "box": [50, 24, 50], "centre": list(c), "size": size}
RAIN = lambda c=(0, 13, -4), n=2200: {"type": "rain", "count": n, "box": [44, 30, 34], "centre": list(c)}
STEAM = lambda pos, n=10, size=5, color="#e6e2de", op=0.35: {"type": "steam", "pos": list(pos), "count": n, "spread": 6, "rise": 8, "size": size, "color": color, "opacity": op}
def props(*items): return {"type": "props", "items": [dict(i) for i in items]}
def crowd(area, n, pal="water", facing=0, cheer=0.0, seed=1, **kw): return {"palette": pal, "count": n, "area": list(area), "facing": facing, "cheer": cheer, "seed": seed, **kw}

def TOWN(seed=1, cheer=0.0, z0=-70, z1=-14, mood="calm", walk=0.4, run=False):
    w = dict(mood=mood, walk=walk, walkDir=0, bothWays=True, run=run)
    return [
        crowd([-8, z0, 12, z1], 28, "water", 0, cheer, seed, **w),
        crowd([-8, z0, 12, z1], 22, "fire", 0, cheer, seed + 7, **w),
        crowd([-8, z0 - 60, 14, z0 - 4], 20, "water", 0, cheer, seed + 3, **w),
        crowd([7, z1 + 1, 13, z1 + 9], 5, "fire", -40, cheer, seed + 5, mood=mood),
    ]

def SIDES(seed=1, mood="calm", walk=0.5, run=False, z0=-80, z1=-4):
    w = dict(mood=mood, walk=walk, walkDir=0, bothWays=True, run=run)
    return [crowd([-8, z0, -2.5, z1], 20, "water", 60, 0, seed, **w), crowd([6.5, z0, 13, z1], 20, "fire", -60, 0, seed + 4, **w)]

def stall(x, z, col, rot=0):
    return [
        dict(shape="box", pos=[x, 1.3, z], size=[4.2, 2.6, 2.2], color="#7a5a3c", rotY=rot),
        dict(shape="box", pos=[x, 2.75, z], size=[4.4, 0.3, 2.4], color="#c9a878", rotY=rot),
        dict(shape="box", pos=[x - 2, 3.6, z - 1], size=[0.25, 7.2, 0.25], color="#5a4030"),
        dict(shape="box", pos=[x + 2, 3.6, z - 1], size=[0.25, 7.2, 0.25], color="#5a4030"),
        dict(shape="box", pos=[x, 7.3, z - 0.2], size=[5.2, 0.35, 3.4], color=col, rotX=14, rotY=rot),
    ]
def barrel(x, z): return [dict(shape="cyl", pos=[x, 0.9, z], size=[0.75, 1.8, 0.65], color="#6a4a30"), dict(shape="cyl", pos=[x, 1.5, z], size=[0.78, 0.14], color="#2a2420")]
def banner(x, z, col): return [dict(shape="cyl", pos=[x, 5, z], size=[0.14, 10], color="#4a3a30"), dict(shape="box", pos=[x + 0.9, 8.2, z], size=[1.7, 3.2, 0.08], color=col)]

STREET_DRESS = stall(-6.6, -24, "#c8382c", 8) + stall(7.5, -32, "#2f8f83", -10) + barrel(-8.4, -3) + barrel(9, -15) + banner(-8.8, -12, "#c8382c") + banner(11, -24, "#e8b83a")
PLAZA_DRESS = stall(-11, -16, "#c8382c", 20) + stall(11, -18, "#2f8f83", -20) + barrel(-6.5, -22) + barrel(8, -24) + banner(-13.5, -24, "#e8b83a") + banner(13.5, -24, "#c8382c")
KITCHEN_DRESS = [
    dict(shape="box", pos=[-10.5, 3.2, -10], size=[5, 6.4, 1.4], color="#8a5a3a"),
    dict(shape="box", pos=[3, 1.6, -9.8], size=[3.4, 3.2, 2], color="#3a3a40"),
    dict(shape="cyl", pos=[2.4, 3.55, -9.8], size=[0.6, 0.7], color="#b0b4ba"),
    dict(shape="box", pos=[-3, 7.2, -10.8], size=[2.6, 2, 0.15], color="#e8d8a8"),
    dict(shape="box", pos=[-2, 0.03, -4], size=[11, 0.06, 7], color="#9a3a34"),
    dict(shape="box", pos=[-2, 0.045, -4], size=[9.6, 0.06, 5.6], color="#c8a46a"),
    dict(shape="box", pos=[8.5, 4.6, -10.6], size=[4.2, 0.2, 0.9], color="#6a4a30"),
    dict(shape="cyl", pos=[7.4, 5.1, -10.6], size=[0.4, 0.8], color="#4a7a9a"),
]
DRESS = {
    "street": STREET_DRESS, "dusk": STREET_DRESS, "night": STREET_DRESS, "nightDark": STREET_DRESS, "late": STREET_DRESS,
    "plaza": PLAZA_DRESS, "plazaN": PLAZA_DRESS, "plazaDark": PLAZA_DRESS,
    "kitchen": KITCHEN_DRESS,
}

MANUAL_SFX = {}
CUE = [0]
NIGHT = [False]


def at(cue, night=False):
    CUE[0] = cue
    NIGHT[0] = night
    return cue


def S(id, cue, scene, actors, camera, vfx=(), crowds=(), sound=None, extra_sfx=(), **over):
    dress = over.pop("dress", True)
    vfx = list(vfx) + ([props(*DRESS[scene])] if scene in DRESS and dress else [])
    for i, a in enumerate(actors):
        if a.get("talk") is False:
            del a["talk"]
        elif "talk" not in a and i == 0 and a["faces"][0]["v"] in TALKERS:
            a["talk"] = True
    NIGHT[0] = False
    s = {"id": f"{len(shots) + 1:02d}_{id}", "cue": cue, **json.loads(json.dumps(SCENES[scene])), "actors": actors, "camera": camera}
    if vfx:
        s["vfx"] = list(vfx)
    if crowds:
        s["crowds"] = list(crowds)
    if sound:
        s["sound"] = sound
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(s.get(k), dict):
            s[k] = {**s[k], **v}
        else:
            s[k] = v

    sfx, layers = list(extra_sfx) + list(MANUAL_SFX.get(cue, [])), {}
    def layer(kind, gain, at_=0):
        layers[kind] = max(layers.get(kind, (-99, 0))[0], gain), min(layers.get(kind, (0, at_))[1], at_)

    for v in vfx:
        if v["type"] == "rain":
            layer("rain_light", -4)
        elif v["type"] == "flame":
            layer("fire", -4)
    sfx += [{"type": k, "at": at_, "dur": "shot", "gain": g} for k, (g, at_) in layers.items()]
    sfx = [x for x in sfx if os.path.exists(os.path.join(HERE, "..", "..", "sfx", x["type"] + ".wav"))]
    if sfx:
        s["sfx"] = sfx
    shots.append(s)


# ================================================================ 1. Premise & How it works (0..58)
S("market_open", at(0, True), "plazaN",
  [A("narrator", 0, -4, 10, "neutralTalk"), A("toby", -5, -7, 25, "happyArcs"), A("nora", 5, -7, -20, "dotSmile")],
  wide(0, -6, side=7, dist=30, h=8.5, whip=-9, push=0.22),
  vfx=[props(*MARKET_LANTERNS), EMBERS((0, 9, -10), 220)],
  crowds=TOWN(1, mood="calm", walk=0.35),
  sound="whoosh", extra_sfx=[{"type": "whoosh_air", "at": 0}, {"type": "bell_pop", "word": 6}])

S("wish_memory", at(12, True), "plazaN",
  [A("narrator", 0, -5, 10, "smug", faces=[(16, "neutralTalk")]), A("bram", -4, -7, 20, "happyArcs", talk=False)],
  med(0, -5, side=-2.8, dist=11.5, push=0.22),
  vfx=[props(*LANTERN(-3.6, 6.6, -7, 0.9), *LANTERN(4.2, 6.8, -8, 0.85)), EMBERS((0, 8, -7), 160)],
  crowds=TOWN(1, mood="calm", walk=0.35))

S("trade_line", at(20), "dusk",
  [A("narrator", -2, -5, 15, "neutralTalk", faces=[(24, "smug")]), A("bram", 3, -8, -10, "happyArcs"), A("nora", 6, -10, -15, "dotSmile")],
  med(0, -6, side=3.2, dist=12, push=0.2),
  vfx=[props(*LANTERN(-2, 6.2, -5, 0.9), *LANTERN(4, 6.8, -8, 0.9))],
  crowds=TOWN(2, mood="calm", walk=0.45),
  extra_sfx=[{"type": "transition", "at": 0}, {"type": "pop_soft_in", "word": 22}])

S("bram_knee", at(29), "street",
  [A("bram", 0, -6, 12, "worried", faces=[(31, "blank")], clips=[("handUpQuick", 30)])],
  med(0, -6, side=-2.8, dist=11, push=0.22),
  crowds=TOWN(3, mood="calm", walk=0.4),
  extra_sfx=[{"type": "pop_soft", "word": 30}])

S("bram_bike", at(34), "street",
  [A("bram", 0, -6, 15, "bigHappy", faces=[(36, "laugh")], clips=[("armsUp", 35)])],
  med(0, -6, side=2.8, dist=11, whip=6, push=0.2),
  vfx=[props(*BIKE(2.8, -5.5))],
  crowds=TOWN(3, mood="cheer", walk=0.3),
  sound="hit", extra_sfx=[{"type": "bell_pop", "at": 0}])

S("nora_rain", at(39), "river",
  [A("nora", -2, -10, 15, "worried", faces=[(41, "deadpan")], clips=[("shrugOut", 40)])],
  med(-2, -10, side=2.6, dist=11.5, push=0.2),
  vfx=[RAIN((-2, 12, -10), 1800)],
  crowds=SIDES(4, mood="calm", walk=0.5),
  extra_sfx=[{"type": "transition", "at": 0}])

S("nora_win", at(44), "river",
  [A("nora", 0, -18, None, "bigHappy", faces=[(46, "laugh")], clips=[("runLeaning", -1000)], to=[0, -7])],
  track([0, 4.0, -18], [3.6, 4.4, -7], [0, 0, 11]),
  crowds=SIDES(5, mood="cheer", walk=0.2, run=False),
  extra_sfx=[{"type": "whoosh_quick", "at": 0}])

S("toby_gold", at(49), "plazaN",
  [A("toby", 0, -5, 10, "smug", faces=[(54, "bigHappy")], clips=[("presentPlate", 55)])],
  med(0, -5, side=-2.6, dist=11.5, push=0.22),
  vfx=[props(*GOLD_BAG(1.8, 2.2, -4.6), *LANTERN(-3.8, 6.5, -7, 0.95)), EMBERS((0, 8, -6), 160)],
  crowds=TOWN(6, mood="calm", walk=0.3),
  sound="hit", extra_sfx=[{"type": "money", "word": 57}, {"type": "pop_b", "word": 50}])

# ================================================================ 2. Rule & Odd Detail (59..93)
S("one_rule", at(59), "courtyard",
  [A("narrator", 0, -6, 0, "angryTalk", clips=[("pointUp", 61)])],
  close(0, -6, side=1.5, dist=8.0, push=0.04),
  crowds=[crowd([-12, -18, -4, -8], 10, "water", 70, seed=10), crowd([4, -18, 12, -8], 10, "fire", -70, seed=11)],
  sound="hit", extra_sfx=[{"type": "click", "word": 62}])

S("let_go", at(64), "courtyard",
  [A("narrator", 0, -6, 8, "angryTalk", faces=[(67, "worried")], clips=[("shrugOut", 65)])],
  med(0, -6, side=2.8, dist=11.5, push=0.2),
  vfx=[props(*LANTERN(-3.5, 6.4, -7.5, 0.9))],
  crowds=[crowd([-12, -18, -4, -8], 10, "water", 70, seed=10), crowd([4, -18, 12, -8], 10, "fire", -70, seed=11)])

S("takes_light", at(71), "plazaDark",
  [A("narrator", 0, -5, 0, "hollowShock", faces=[(75, "nervous")], look=[0, -0.05])],
  close(0, -5, side=-1.6, dist=8.2, push=0.04, shake=IMPACT(4)),
  vfx=[props(*DARK_LANTERNS)],
  crowds=TOWN(7, mood="worried", walk=0.2),
  sound="hit", extra_sfx=[{"type": "riser", "at": 0, "lead": 1.84}])

S("weird_part", at(79), "plazaN",
  [A("narrator", 0, -5, 10, "smug", faces=[(82, "deadpan")], look=[0.04, 0])],
  close(0, -5, side=1.6, dist=8.0, push=0.04),
  vfx=[props(*LANTERN(-3.4, 6.3, -7, 0.9))],
  extra_sfx=[{"type": "pop_c", "at": 0}])

S("empty_bright", at(84), "plazaN",
  [A("narrator", -2, -6, 18, "neutralTalk", faces=[(86, "smug")]), A("bram", 3, -8, -15, "blank")],
  med(0, -6, side=-3.2, dist=12, push=0.2),
  vfx=[props(*MARKET_LANTERNS), EMBERS((0, 9, -8), 200)],
  crowds=TOWN(8, mood="calm", walk=0.35),
  extra_sfx=[{"type": "loading_soft", "at": 0, "gain": -4}])

S("empty_inside", at(88), "plazaN",
  [A("narrator", 0, -5, 10, "deadpan", faces=[(91, "blank")])],
  close(0, -5, side=1.6, dist=8.0, push=0.04),
  vfx=[props(*LANTERN(3.6, 6.4, -7.5, 0.9))])

# ================================================================ 3. Narrator Hype, Cost, Keepsake (94..153)
S("hype_intro", at(94), "street",
  [A("narrator", 0, -6, 10, "deadpan", faces=[(98, "smug")], clips=[("shrugOut", 96)])],
  med(0, -6, side=2.6, dist=11.5, whip=-7, push=0.2),
  crowds=TOWN(9, mood="calm", walk=0.45),
  sound="whoosh", extra_sfx=[{"type": "transition", "at": 0}, {"type": "whoosh_short", "at": 0}])

S("left_shoe", at(103), "kitchen",
  [A("narrator", -3, -4, 15, "worried", faces=[(106, "blank")], look=[-0.04, 0.04], clips=[("shrugOut", 104)])],
  cam([-3, 3.8, -4], [2.5, 4.6, 5.5], push=0.18),
  extra_sfx=[{"type": "pop_soft_in", "word": 105}])

S("lunchbox_porch", at(110), "street",
  [A("narrator", -2, -5, 20, "deadpan", faces=[(113, "worried")], clips=[("handUpQuick", 112)])],
  med(-1, -5, side=3.0, dist=11.5, push=0.2),
  vfx=[props(*LUNCHBOX(-5.5, 0.4, -4.5))],
  crowds=TOWN(10, mood="calm", walk=0.35),
  extra_sfx=[{"type": "pop_soft", "word": 112}])

S("slippers_walk", at(117), "street",
  [A("narrator", 1.5, -24, None, "deadpan", faces=[(120, "nervous")], clips=[("walk", -1000)], to=[1.5, -14])],
  track([1.5, 4.0, -24], [4.5, 4.3, -12.5], [0, 0, 10]),
  crowds=SIDES(11, mood="calm", walk=0.5),
  extra_sfx=[{"type": "whoosh_quick", "at": 0}])

S("toby_laughs", at(124), "street",
  [A("toby", -1.5, -5, 25, "laugh", faces=[(127, "smug")], clips=[("pointUp", 125)]), A("narrator", 2.5, -5, -25, "deadpan", talk=False)],
  med(0, -5, side=2.6, dist=11, push=0.2),
  crowds=TOWN(12, mood="calm", walk=0.3),
  extra_sfx=[{"type": "pop_b", "word": 125}])

S("calls_blank", at(130), "street",
  [A("toby", 0, -5, 8, "smug", faces=[(132, "laugh")])],
  close(0, -5, side=-1.5, dist=8.0, push=0.04),
  sound="hit", extra_sfx=[{"type": "click", "word": 133}])

S("everyone_blank", at(134), "courtyard",
  [A("narrator", 0, -6, 0, "deadpan", faces=[(136, "worried")], look=[0.04, 0])],
  med(0, -6, side=2.8, dist=12, push=0.2),
  crowds=[crowd([-12, -18, -4, -8], 12, "water", 70, seed=13), crowd([4, -18, 12, -8], 12, "fire", -70, seed=14)],
  extra_sfx=[{"type": "pop_c", "at": 0}])

S("grandma_says", at(139), "kitchen",
  [A("grandma", -4, -5, 25, "dotSmile", faces=[(141, "happyArcs")], clips=[("presentPlate", 140)]), A("narrator", 0.5, -3.5, -30, "neutralTalk", talk=False)],
  cam([-2.2, 4.1, -4.5], [3.5, 4.6, 4.8], push=0.16),
  extra_sfx=[{"type": "transition", "at": 0}])

S("empty_cup", at(144), "kitchen",
  [A("grandma", -3, -5, 10, "dotSmile", faces=[(149, "happyArcs")], look=[0, 0])],
  close(-3, -5, side=1.6, dist=8.0, push=0.04),
  extra_sfx=[{"type": "bell_pop", "word": 146}])

# ================================================================ 4. The Turn & Blackout (154..208)
S("winter_night", at(154, True), "dusk",
  [A("narrator", 0, -6, 10, "worried", faces=[(157, "nervous")], look=[0, -0.04])],
  wide(0, -8, side=6, dist=28, h=8.5, whip=8, push=0.22),
  vfx=[props(*MARKET_LANTERNS), STEAM((0, 4, -8), 8, 5, "#dce4f4", 0.25)],
  crowds=TOWN(15, mood="worried", walk=0.3),
  sound="whoosh", extra_sfx=[{"type": "transition", "at": 0}, {"type": "whoosh_air", "at": 0}])

S("king_lantern", at(161, True), "plazaN",
  [A("toby", -4, -4, 30, "smug", faces=[(166, "bigHappy")], clips=[("walk", -1000)], to=[-2.5, -5.5])],
  wide(0, -8, side=5, dist=24, h=7.5, push=0.2),
  vfx=KING_LANTERN(2.5, -9, lit=True, flame_sz=2.6) + [EMBERS((2.5, 8, -9), 260)],
  crowds=TOWN(16, mood="calm", walk=0.2),
  extra_sfx=[{"type": "riser_fear", "at": 0, "lead": 2.0}])

S("toby_wish", at(172, True), "plazaN",
  [A("toby", -2, -5.5, 20, "bigHappy", faces=[(176, "smug")], clips=[("armsUp", 174)])],
  med(-1, -6, side=3.2, dist=11.5, push=0.22),
  vfx=KING_LANTERN(2.5, -9, lit=True, flame_sz=2.6),
  extra_sfx=[{"type": "money", "word": 177}])

S("brag_memory", at(179, True), "plazaN",
  [A("toby", -2, -5.5, 18, "smug", faces=[(184, "grittedAngry")], clips=[("castForward", 181)])],
  close(-2, -5.5, side=1.6, dist=8.2, push=0.05),
  vfx=KING_LANTERN(2.5, -9, lit=True, flame_sz=2.8),
  extra_sfx=[{"type": "riser_burst", "at": 0, "lead": 2.31}])

S("crack_black", at(191, True), "plazaDark",
  [A("toby", -2.5, -5.5, 20, "hollowShock", faces=[(194, "scream")], clips=[("armsUp", 192)])],
  med(0, -7, side=3.0, dist=13, push=0.18, shake=IMPACT(0)),
  vfx=KING_LANTERN(2.5, -9, lit=False),
  crowds=TOWN(17, mood="panic", walk=0.15),
  sound="hit", extra_sfx=[{"type": "click", "at": 0}])

S("lamps_out", at(198, True), "nightDark",
  [A("narrator", 0, -6, 12, "hollowShock", faces=[(201, "nervous")], look=[0, -0.05])],
  wide(0, -10, side=-6, dist=26, h=7.5, push=0.22, shake=RUMBLE(0, 30)),
  vfx=[props(*DARK_LANTERNS)],
  crowds=TOWN(18, mood="panic", walk=0.4, run=True),
  sound="hit", extra_sfx=[{"type": "crowd_panic", "at": 0, "dur": "shot", "gain": -2}])

S("darkness_square", at(204, True), "plazaDark",
  [A("narrator", -3, -5, 15, "nervous", faces=[(206, "hollowShock")]), A("toby", 3, -6, -15, "scream", talk=False)],
  wide(0, -8, side=4, dist=22, h=6.5, push=0.2),
  vfx=KING_LANTERN(0, -12, lit=False),
  crowds=TOWN(19, mood="panic", walk=0.25),
  extra_sfx=[{"type": "crowd_panic", "at": 0, "dur": "shot", "gain": -3}])

# ================================================================ 5. Everyone Fails (209..244)
S("bram_trophy", at(209, True), "plazaDark",
  [A("bram", -2, -5.5, 22, "angryTalk", faces=[(212, "grittedAngry")], clips=[("presentPlate", 210)])],
  med(-1, -6, side=-2.8, dist=11.5, push=0.2),
  vfx=KING_LANTERN(2.5, -9, lit=False) + [props(*TROPHY(-0.5, 2.5, -5.5))],
  extra_sfx=[{"type": "pop_soft_in", "word": 210}])

S("bram_fail", at(214, True), "plazaDark",
  [A("bram", -2, -5.5, 10, "hollowShock", faces=[(215, "blank")], clips=[("shrugOut", 214)])],
  close(-2, -5.5, side=1.5, dist=8.0, push=0.04, shake=IMPACT(0)),
  sound="hit", extra_sfx=[{"type": "pop_soft", "at": 0}])

S("nora_sprint", at(216, True), "plazaDark",
  [A("nora", -6, -6, None, "grittedAngry", faces=[(219, "nervous")], clips=[("runLeaning", -1000)], to=[0, -6])],
  track([-6, 4.2, -6], [-2, 4.5, 6], [6, 0, 0]),
  vfx=KING_LANTERN(3.5, -9, lit=False),
  extra_sfx=[{"type": "whoosh_quick", "at": 0}])

S("nora_fail", at(221, True), "plazaDark",
  [A("nora", 0, -6, 0, "hollowShock", faces=[(222, "worried")])],
  close(0, -6, side=-1.5, dist=8.0, push=0.04, shake=IMPACT(0)),
  sound="hit", extra_sfx=[{"type": "click", "at": 0}])

S("toby_throw", at(223, True), "plazaDark",
  [A("toby", -2, -5.5, 25, "grittedAngry", faces=[(228, "angryTalk")], clips=[("castForward", 225)])],
  med(-1, -6, side=3.0, dist=11.5, push=0.22),
  vfx=KING_LANTERN(2.5, -9, lit=False) + [props(*GOLD_BAG(0.5, 2.8, -6.8))],
  extra_sfx=[{"type": "money", "word": 227}, {"type": "whoosh_short", "word": 225}])

S("toby_fail", at(232, True), "plazaDark",
  [A("toby", -2, -5.5, 10, "scream", faces=[(233, "hollowShock")])],
  close(-2, -5.5, side=1.6, dist=8.0, push=0.04, shake=IMPACT(0)),
  sound="hit")

S("toby_yells", at(234, True), "plazaDark",
  [A("toby", 0, -5, 0, "scream", faces=[(236, "grittedAngry")], clips=[("armsUp", 234)])],
  close(0, -5, side=-1.5, dist=8.0, push=0.05),
  extra_sfx=[{"type": "crowd_panic", "at": 0, "dur": "shot", "gain": -4}])

S("shivering_dark", at(238, True), "nightDark",
  [A("narrator", -2, -5, 10, "nervous", faces=[(241, "worried")]), A("bram", 3, -7, -15, "worried", talk=False)],
  wide(0, -8, side=5, dist=24, h=7, push=0.2),
  crowds=TOWN(20, mood="worried", walk=0.1),
  extra_sfx=[{"type": "clock_tick", "at": 0, "gain": -4}])

# ================================================================ 6. Reframe & The Act (245..351)
S("understood", at(245, True), "plazaDark",
  [A("narrator", 0, -5, 0, "blank", faces=[(247, "smug")], look=[0, -0.04])],
  close(0, -5, side=1.5, dist=8.0, push=0.04),
  sound="hit", extra_sfx=[{"type": "bell_pop", "at": 0}])

S("holding_tight", at(249, True), "plazaDark",
  [A("narrator", -2, -5, 15, "neutralTalk", faces=[(253, "smug")]), A("toby", 3, -7, -20, "worried", talk=False)],
  med(0, -6, side=-3.0, dist=11.5, push=0.2),
  vfx=KING_LANTERN(3, -10, lit=False))

S("echo_grandma", at(257, True), "kitchen",
  [A("grandma", -3, -5, 10, "dotSmile", faces=[(261, "happyArcs")])],
  close(-3, -5, side=1.5, dist=8.0, push=0.04),
  extra_sfx=[{"type": "transition", "at": 0}])

S("echo_cup", at(263, True), "plazaDark",
  [A("narrator", 0, -5, 0, "smug", faces=[(268, "bigHappy")])],
  close(0, -5, side=-1.5, dist=8.0, push=0.04),
  extra_sfx=[{"type": "loading_soft", "at": 0, "gain": -3}])

S("walk_lantern", at(273, True), "plazaDark",
  [A("narrator", -4, -3, None, "neutralTalk", faces=[(277, "smug")], clips=[("walk", -1000)], to=[0, -6.5])],
  track([-4, 4.0, -3], [-0.5, 4.4, 8], [4, 0, -3.5]),
  vfx=KING_LANTERN(3, -9.5, lit=False),
  crowds=SIDES(21, mood="stunned", walk=0.0),
  extra_sfx=[{"type": "whoosh_air", "at": 0}])

S("give_lunchbox", at(281, True), "plazaDark",
  [A("narrator", 0, -6.5, 25, "neutralTalk", faces=[(284, "smug")])],
  close(0, -6.5, side=-1.5, dist=8.0, push=0.04),
  vfx=KING_LANTERN(3.5, -9.5, lit=False))

S("lunchbox_toss", at(286, True), "plazaDark",
  [A("narrator", 0, -6.5, 25, "smug", faces=[(289, "bigHappy")], clips=[("castForward", 287)])],
  med(1, -7, side=3.0, dist=11.5, push=0.22),
  vfx=KING_LANTERN(3.5, -9.5, lit=False) + [props(*LUNCHBOX(1.8, 3.0, -7.8))],
  extra_sfx=[{"type": "pop_b", "word": 288}])

S("flicker", at(292, True), "plazaN",
  [A("narrator", 0, -6.5, 25, "bigHappy")],
  med(1.5, -7.5, side=-2.8, dist=12, push=0.18, shake=IMPACT(0)),
  vfx=KING_LANTERN(3.5, -9.5, lit=True, flame_sz=1.2) + [EMBERS((3.5, 5, -9.5), 140)],
  sound="hit", extra_sfx=[{"type": "bell_pop", "at": 0}])

S("tiny_spark", at(293, True), "plazaN",
  [A("narrator", 0, -6.5, 25, "bigHappy", faces=[(297, "laugh")])],
  med(1.5, -7.5, side=-2.8, dist=11, push=0.22),
  vfx=KING_LANTERN(3.5, -9.5, lit=True, flame_sz=1.6) + [EMBERS((3.5, 5.5, -9.5), 180)])

S("give_shoe", at(302, True), "plazaN",
  [A("narrator", 0, -6.5, 25, "smug", faces=[(306, "bigHappy")], clips=[("castForward", 304)])],
  med(1.5, -7.5, side=2.8, dist=11, push=0.22),
  vfx=KING_LANTERN(3.5, -9.5, lit=True, flame_sz=2.0) + [EMBERS((3.5, 6, -9.5), 220)],
  extra_sfx=[{"type": "pop_c", "word": 304}])

S("glow_spark", at(310, True), "plazaN",
  [A("narrator", 0, -6.5, 20, "bigHappy", clips=[("castUpBoth", 310)])],
  close(0, -6.5, side=1.5, dist=8.0, push=0.04, shake=IMPACT(0)),
  vfx=KING_LANTERN(3.5, -9.5, lit=True, flame_sz=2.3) + [EMBERS((3.5, 6.5, -9.5), 260)],
  sound="hit")

S("give_slippers", at(311, True), "plazaN",
  [A("narrator", 0, -6.5, 22, "bigHappy", faces=[(314, "laugh")], clips=[("castForward", 312)])],
  med(1.5, -7.5, side=-2.8, dist=11.5, push=0.22),
  vfx=KING_LANTERN(3.5, -9.5, lit=True, flame_sz=2.4) + [EMBERS((3.5, 7, -9.5), 300)],
  extra_sfx=[{"type": "pop_soft_in", "word": 313}])

S("give_homework", at(316, True), "plazaN",
  [A("narrator", 0, -6.5, 20, "smug", faces=[(318, "bigHappy")], clips=[("handUpQuick", 316)])],
  close(0, -6.5, side=-1.6, dist=8.0, push=0.05),
  vfx=KING_LANTERN(3.5, -9.5, lit=True, flame_sz=2.5) + [EMBERS((3.5, 7, -9.5), 320)],
  extra_sfx=[{"type": "pop_b", "word": 317}])

S("give_tuesday", at(319, True), "plazaN",
  [A("narrator", 0, -6.5, 18, "bigHappy", faces=[(323, "laugh")], clips=[("castUpBoth", 320)])],
  med(1.5, -7.5, side=3.0, dist=12, push=0.24),
  vfx=KING_LANTERN(3.5, -9.5, lit=True, flame_sz=2.0) + [EMBERS((3.5, 8, -9.5), 340)],
  extra_sfx=[{"type": "riser_burst", "word": 321, "lead": 2.31}])

S("couldnt_remember", at(322, True), "plazaN",
  [A("narrator", 0, -6.5, 16, "smug", faces=[(325, "bigHappy")], clips=[("shrugOut", 322)])],
  close(0, -6.5, side=-1.5, dist=8.0, push=0.05),
  vfx=KING_LANTERN(3.5, -9.5, lit=True, flame_sz=2.0) + [EMBERS((3.5, 8, -9.5), 340)])

S("up_up_up", at(327, True), "plazaN",
  [A("narrator", 0, -6.5, 15, "bigHappy", clips=[("armsUp", 327)])],
  med(2, -8, side=3.2, dist=12.5, push=0.22, shake=IMPACT(0)),
  vfx=KING_LANTERN(3.5, -9.5, lit=True, flame_sz=2.8) + [EMBERS((3.5, 9, -9.5), 400)],
  sound="whoosh", extra_sfx=[{"type": "whoosh_air", "at": 0}])

S("sky_flame", at(330, True), "plazaN",
  [A("narrator", 0, -6.5, 15, "laugh", faces=[(333, "bigHappy")], clips=[HELD("armsUp")])],
  wide(2, -8, side=-6, dist=24, h=7.5, push=0.25, shake=RUMBLE(0, 30)),
  vfx=KING_LANTERN(3.5, -9.5, lit=True, flame_sz=2.8) + [props(*MARKET_LANTERNS), EMBERS((0, 10, -10), 420)],
  crowds=TOWN(22, mood="cheer", cheer=0.6, walk=0.0))

S("whoosh_on", at(336, True), "night",
  [A("narrator", 0, -6, 10, "bigHappy", clips=[("cheerLoop", 336)])],
  wide(0, -10, side=-7, dist=28, h=8.5, whip=-9, push=0.22),
  vfx=[props(*MARKET_LANTERNS), EMBERS((0, 11, -12), 360)],
  crowds=TOWN(23, mood="cheer", cheer=0.8, walk=0.2),
  sound="whoosh", extra_sfx=[{"type": "whoosh_short", "at": 0}])

S("town_lit", at(337, True), "night",
  [A("narrator", 0, -6, 10, "laugh", faces=[(341, "bigHappy")], clips=[HELD("cheerLoop")])],
  med(0, -6, side=3.0, dist=12, push=0.22),
  vfx=[props(*MARKET_LANTERNS), EMBERS((0, 10, -10), 300)],
  crowds=TOWN(23, mood="cheer", cheer=0.8, walk=0.2),
  sound="hit", extra_sfx=[{"type": "crowd_cheer", "at": 0, "dur": "shot", "gain": 2}])

S("warm_glow", at(345, True), "plazaN",
  [A("narrator", -2, -5, 15, "bigHappy", faces=[(348, "dotSmile")]), A("bram", 3, -7, -15, "happyArcs", talk=False), A("nora", 6, -8, -20, "bigHappy", talk=False)],
  med(0, -6, side=3.0, dist=12.5, push=0.2),
  vfx=[props(*MARKET_LANTERNS), EMBERS((0, 9, -8), 220)],
  crowds=TOWN(24, mood="cheer", cheer=0.5, walk=0.1))

# ================================================================ 7. Coda (352..395)
S("toby_whisper", at(352, True), "plazaN",
  [A("toby", -2, -5, 20, "worried", faces=[(355, "dotSmile")]), A("narrator", 2.5, -5, -20, "smug", talk=False)],
  close(-2, -5, side=1.5, dist=8.0, push=0.04),
  extra_sfx=[{"type": "pop_soft_in", "at": 0}])

S("just_blank", at(357, True), "plazaN",
  [A("toby", -2, -5, 15, "dotSmile", faces=[(360, "happyArcs")]), A("narrator", 2.5, -5, -20, "bigHappy", talk=False)],
  med(0, -5, side=-2.6, dist=11, push=0.18),
  extra_sfx=[{"type": "click", "word": 360}])

S("nobody_blank", at(364), "late",
  [A("narrator", 0, -6, 10, "bigHappy", faces=[(366, "smug")], clips=[("wave", 365)])],
  med(0, -6, side=2.6, dist=11.5, push=0.2),
  crowds=TOWN(25, mood="calm", walk=0.4),
  extra_sfx=[{"type": "transition", "at": 0}])

S("find_shoe", at(369), "late",
  [A("toby", -2, -5, 25, "dotSmile", faces=[(373, "happyArcs")], clips=[("handUpQuick", 372)], talk=False), A("narrator", 2.2, -5, -20, "bigHappy", faces=[(374, "laugh")])],
  med(0, -5, side=-2.8, dist=11.5, push=0.2),
  crowds=TOWN(26, mood="calm", walk=0.35),
  extra_sfx=[{"type": "pop_soft", "word": 372}])

S("coda_lunchbox", at(379), "late",
  [A("narrator", 0, -5, 8, "deadpan", faces=[(384, "smug")], clips=[("shrugOut", 381)])],
  close(0, -5, side=1.6, dist=8.0, push=0.04),
  extra_sfx=[{"type": "pop_b", "word": 383}])

S("coda_end", at(388), "late",
  [A("narrator", 0, -5, 0, "smug", faces=[(392, "bigHappy")], look=[0.03, 0])],
  close(0, -5, side=-1.5, dist=8.0, push=0.04),
  extra_sfx=[{"type": "bell_pop", "word": 394}])

# ---------------------------------------------------------------- ensure live faces on every actor
for s in shots:
    for a in s["actors"]:
        if len(a["faces"]) == 1:
            v0 = a["faces"][0]["v"]
            v1 = PAIR.get(v0, "neutralTalk")
            idx = shots.index(s)
            next_cue = shots[idx + 1]["cue"] if idx + 1 < len(shots) else len(W)
            mid_w = (s["cue"] + next_cue) // 2
            if mid_w > s["cue"]:
                a["faces"].append({"word": mid_w, "v": v1})

story = {
    "audio": "audio/lantern_market.wav",
    "names": ["Bram", "Nora", "Toby", "Blank", "Grandma"],
    "sfx": ["Crack", "Flicker", "Glow", "Whoosh"],
    "endHoldFrames": 32,
    "shots": shots,
}
out_path = os.path.join(HERE, "story.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(story, f, indent=2)
print(f"Wrote {out_path} ({len(shots)} shots)")
