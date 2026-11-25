#!/usr/bin/env python3
"""Generate 43-second acted Short: 'Don't Blink In The Plaza' (16 fast cuts, starring Hype)."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT_PATH = ROOT / "script.txt"
WORDS_PATH = ROOT / "words.json"
OUT_STORY = ROOT / "story.json"
OUT_BEATS = ROOT / "beats.md"

sys.path.insert(0, str(ROOT.parent.parent / "scripts"))
sys.path.insert(0, "/working_dir/c_2f4fcecea490e13d/cinematic_fix/scripts")
from cinematic_recipes import (
    cam_birds_eye,
    cam_impact_hit,
    cam_low_hero,
    cam_ots,
    cam_punch_in,
    cam_track_run,
    cam_whip_cut,
)

if WORDS_PATH.exists():
    wdata = json.loads(WORDS_PATH.read_text(encoding="utf-8"))
    wlist = wdata["words"] if isinstance(wdata, dict) and "words" in wdata else wdata
    tokens = [w["w"] for w in wlist]
else:
    tokens = SCRIPT_PATH.read_text(encoding="utf-8").strip().split()


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9'-]", "", w.lower())


def find_word(phrase: str, start: int = 0) -> int:
    p = [norm(t) for t in phrase.split() if norm(t)]
    t = [norm(x) for x in tokens]
    for i in range(start, len(t) - len(p) + 1):
        if t[i : i + len(p)] == p:
            return i
    raise ValueError(f"Not found from {start}: {phrase!r}")


SCENES = {
    "plaza_dusk": {"set": "tabletPlaza", "look": "DUSK_MAGENTA", "shadow": {"focus": [0, 2, -8], "extent": 40}},
    "plaza_day": {"set": "tabletPlaza", "look": "DAY_COOL", "shadow": {"focus": [0, 2, -6], "extent": 36}},
    "plaza_night": {"set": "tabletPlaza", "look": "NIGHT_EMBER", "lookOverrides": {"fog": {"color": "#141624", "density": 0.0040}}, "shadow": {"focus": [0, 2, -10], "extent": 48}},
    "kitchen": {"set": "kitchen", "setParams": {"chairs": []}, "look": "INTERIOR_NEUTRAL", "lookOverrides": {"lights": {"hemi": {"sky": "#e6ddd2", "ground": "#8a7a6a", "intensity": 1.9}, "key": {"color": "#fff0dc", "intensity": 1.8, "from": [0.5, 0.8, 0.7], "shadow": True}}}, "shadow": {"focus": [-4, 3, -3], "extent": 24}},
    "street_day": {"set": "fireStreet", "setParams": {"flames": False, "bowls": None}, "look": "DAY_SUN", "lookOverrides": {"fog": {"color": "#c4d2ec", "density": 0.0024}}, "shadow": {"focus": [0, 2, -6], "extent": 36}},
}


def A(char, x, z, yaw=0, face="neutralTalk", faces=None, clips=None, talk=False, to=None):
    a = {"character": char, "pos": [x, z], "contactShadow": 0.7}
    if to is None:
        a["yaw"] = yaw
    else:
        a["to"] = to
    a["faces"] = [{"f": 0, "v": face}] + (faces or [])
    if clips:
        a["clips"] = clips
    if talk:
        a["talk"] = talk
    return a


def statue_prop(x, z, tilt=0.0):
    return {
        "type": "props",
        "items": [
            {"shape": "box", "pos": [x, 0.6, z], "size": [2.8, 1.2, 2.8], "color": "#4f5563"},
            {"shape": "box", "pos": [x, 3.6, z], "size": [2.1, 4.8, 1.4], "color": "#7b8291", "rotX": tilt},
            {"shape": "box", "pos": [x, 6.7, z], "size": [1.35, 1.35, 1.35], "color": "#8b93a3", "rotX": tilt},
        ],
    }


BEATS = [
    ("01_hook", "In this town", "plaza_dusk", [A("hype", 0, -2, 0, "hollowShock", [{"f": 12, "v": "worried"}], [{"clip": "talkBounce", "at": 0}], talk=True)], [statue_prop(0, -10)], cam_punch_in(0, -2, y=4.5, dist_start=12.0, dist_end=9.2), "hit", [{"type": "whoosh_air", "at": 0}]),
    ("02_guards", "You see guards", "plaza_day", [A("rook", -1.5, -3, 15, "angryTalk", [{"f": 12, "v": "blank"}], [{"clip": "lookAround", "at": 0}]), A("clara", 1.8, -3, -20, "worried", [], [{"clip": "rest", "at": 0}])], [], cam_whip_cut(0, -3, side=1, dist=10.5), None, [{"type": "pop_soft_in", "at": 0}]),
    ("03_rule", "And there's only", "plaza_dusk", [A("hype", 0, -2, 0, "angryTalk", [{"f": 14, "v": "hollowShock"}], [{"clip": "dramaticPoint", "at": 3}], talk=True)], [statue_prop(2.8, -8)], cam_low_hero(0, -2, dist=9.5), "hit", [{"type": "riser", "at": 0, "lead": 1.0}]),
    ("04_hype_flaw", "My name is", "street_day", [A("hype", 0, -2, 0, "deadpan", [{"f": 10, "v": "eyesClosedTalk"}, {"f": 16, "v": "worried"}], [{"clip": "talkBounce", "at": 0}], talk=True)], [], cam_punch_in(0, -2, y=4.6, dist_start=9.5, dist_end=7.8), None, [{"type": "pop_b", "at": 6}]),
    ("05_dax_winky", "Dax calls me", "street_day", [A("dax", 1.6, -3, -35, "laugh", [{"f": 10, "v": "smug"}], [{"clip": "dramaticPoint", "at": 2}]), A("hype", -1.6, -3, 35, "worried", [], [{"clip": "headShake", "at": 4}])], [], cam_ots(1.6, -3, -1.6, -3, side=-1), None, [{"type": "pop_c", "at": 4}]),
    ("06_grandpa", "Grandpa Otis always", "kitchen", [A("otis", -3.8, -3.5, 30, "dotSmile", [{"f": 12, "v": "neutralTalk"}], [{"clip": "sitIdle", "at": 0}, {"clip": "nodYes", "at": 6}], talk=True), A("hype", -1.2, -2.5, -40, "blank", [], [{"clip": "sitIdle", "at": 0}])], [], cam_ots(-3.8, -3.5, -1.2, -2.5, side=1, fov=40), None, [{"type": "pop_soft", "at": 0}]),
    ("07_midnight", "Then came midnight", "plaza_night", [A("hype", 0, 1, 180, "hollowShock", [{"f": 10, "v": "nervous"}], [{"clip": "lookAround", "at": 0}], talk=True)], [statue_prop(0, -10)], cam_birds_eye(0, -5, height=15.0, dist=16.0), "hit", [{"type": "thunder", "at": 0}]),
    ("08_statue_moves", "A giant stone", "plaza_night", [A("dax", 0, -6, 180, "scream", [{"f": 12, "v": "hollowShock"}], [{"clip": "panicFlail", "at": 0}])], [statue_prop(0, -10.5, tilt=0.14)], cam_impact_hit(0, -8, dist=11.0, y=4.4), "hit", [{"type": "riser_burst", "at": 0, "lead": 1.1}]),
    ("09_dax_runs", "Dax ran It", "plaza_night", [A("dax", 0, -6, 0, "scream", [], [{"clip": "runLeaning", "at": -100}], to=[0, 2])], [statue_prop(0, -8.5, tilt=0.22)], cam_track_run(0, -6, 0, 2, lead_x=3.5, lead_z=8.5), None, [{"type": "whoosh_quick", "at": 0}]),
    ("10_understood", "That's when I", "plaza_night", [A("hype", 0, 3, 0, "blank", [{"f": 10, "v": "bigHappy"}], [{"clip": "nodYes", "at": 8}], talk=True)], [], cam_punch_in(0, 3, y=4.65, dist_start=9.2, dist_end=7.2), "hit", [{"type": "pop_soft_in", "at": 6}]),
    ("11_sprint_freeze", "I sprinted between", "plaza_night", [A("hype", -3.0, 2, 180, "grittedAngry", [{"f": 16, "v": "eyesClosedTalk"}], [{"clip": "runLeaning", "at": -100}, {"clip": "rest", "at": 16}], talk=True, to=[0, -3])], [statue_prop(0, -7.5, tilt=0.2)], cam_track_run(-3.0, 2, 0, -3, lead_x=3.5, lead_z=7.5), None, [{"type": "whoosh_air", "at": 0}]),
    ("12_thud", "Thud", "plaza_night", [A("hype", 0, -3, 0, "eyesClosedTalk", [{"f": 6, "v": "hollowShock"}], [{"clip": "rest", "at": 0}])], [statue_prop(0, -5.2, tilt=0.0)], cam_impact_hit(0, -3.8, dist=8.5, y=4.5), "hit", [{"type": "thunder", "at": 0}]),
    ("13_bowed", "The statue stopped", "plaza_night", [A("hype", 0, -3, 0, "blank", [{"f": 14, "v": "bigHappy"}], [{"clip": "rest", "at": 0}], talk=True)], [statue_prop(0, -6.0, tilt=0.35)], cam_low_hero(0, -4, dist=10.5), None, [{"type": "bell_pop", "at": 12}]),
    ("14_coda", "Now Dax brings", "street_day", [A("hype", -1.4, -2, 20, "laugh", [{"f": 14, "v": "bigHappy"}], [{"clip": "talkBounce", "at": 0}], talk=True), A("dax", 1.5, -2, -25, "bigHappy", [], [{"clip": "presentPlate", "at": 4}])], [{"type": "props", "items": [{"shape": "cyl", "pos": [0.4, 2.5, -1.5], "size": [0.22, 0.65], "color": "#38e8ff", "glow": 0.5}]}], cam_punch_in(0.1, -2, y=4.3, dist_start=11.0, dist_end=9.2), None, [{"type": "pop_b", "at": 6}]),
]

shots, rows = [], []
cursor = 0
for i, (sid, anchor, sc_key, actors, vfx, cam, sound, sfx) in enumerate(BEATS):
    cue = find_word(anchor, cursor)
    cursor = cue + 1
    sc = SCENES[sc_key]
    s = {"id": sid, "cue": cue, "set": sc["set"], "look": sc["look"], "actors": actors, "camera": cam, "motionBlur": "auto"}
    for k in ("setParams", "lookOverrides", "shadow"):
        if k in sc:
            s[k] = sc[k]
    if vfx:
        s["vfx"] = vfx
    if sound:
        s["sound"] = sound
    if sfx:
        s["sfx"] = sfx
    shots.append(s)
    rows.append(f"| {i+1} | `{sid}` | {cue} | `{sc['set']}` / `{sc['look']}` |")

story = {"audio": "audio/hype_short_45s.wav", "names": ["Hype", "Dax", "Winky", "Otis", "Grandpa"], "sfx": ["THUD"], "endHoldFrames": 24, "shots": shots}
OUT_STORY.write_text(json.dumps(story, indent=2), encoding="utf-8")
OUT_BEATS.write_text(f"# Don't Blink In The Plaza (43s Short — {len(tokens)} words, {len(shots)} shots)\n\n| # | Shot | Cue | Set / Look |\n|---|---|---|---|\n" + "\n".join(rows) + "\n", encoding="utf-8")
print(f"Generated {OUT_STORY.name} ({len(shots)} shots, {len(tokens)} words, ~{round(len(tokens)/188*60)}s)")
