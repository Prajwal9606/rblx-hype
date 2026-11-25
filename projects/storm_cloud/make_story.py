#!/usr/bin/env python3
"""Upgraded beat-by-beat generator for projects/storm_cloud/ (Never Bottle A Storm Cloud).

Preserves the exact main script.txt and cast.json, fixes:
1. Exact words.json['words'] 1:1 caption/shot sync (fixes 'loaf-sized' 1-word drift).
2. Cinematic animation clips (talkBounce, shockJump, panicFlail, armsCrossed, dramaticPoint, sitIdle, cryShake).
3. Camera variety (cam_ots, cam_low_hero, cam_punch_in, cam_track_run, cam_birds_eye, cam_impact_hit) with tight whip-ins.
4. Staging fixes from storm_cloud_sheet.jpg (no cropped two-shots, no jar blocking Hype's face, rain cleared off faces).
"""
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
)

# Load exact tokens from words.json['words'] when present so shot cues match audio/captions 1:1
tokens = []
word_times = []
if WORDS_PATH.exists():
    wdata = json.loads(WORDS_PATH.read_text(encoding="utf-8"))
    wlist = wdata["words"] if isinstance(wdata, dict) and "words" in wdata else wdata
    tokens = [w["w"] for w in wlist]
    word_times = [float(w.get("t", i * 0.319)) for i, w in enumerate(wlist)]
else:
    raw_text = SCRIPT_PATH.read_text(encoding="utf-8").strip()
    tokens = raw_text.split()
    word_times = [round(i * 0.319, 3) for i in range(len(tokens))]


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9'-]", "", w.lower())


def find_word(phrase: str, start: int = 0) -> int:
    p_toks = [norm(t) for t in phrase.split() if norm(t)]
    t_low = [norm(t) for t in tokens]
    for i in range(start, len(t_low) - len(p_toks) + 1):
        if t_low[i : i + len(p_toks)] == p_toks:
            return i
    raise ValueError(f"Phrase not found from {start}: {phrase!r}")


def cam_tight_whip(tx, tz, side=1, dist=11.0, y=4.2, fov=47):
    """Tight 3.8-stud whip-in resolving by frame 3 (eliminates empty blurry wall frames)."""
    p0 = [tx, y + 0.15, tz + dist]
    p1 = [tx, y + 0.1, tz + dist * 0.87]
    return {
        "fov": fov,
        "keys": [
            {"f": -1, "pos": p0, "target": [tx + side * 3.8, y, tz]},
            {"f": 3, "pos": p0, "target": [tx, y, tz], "ease": "easeOutCubic"},
            {"u": 1, "pos": p1, "target": [tx, y, tz], "ease": "linear"},
        ],
    }


SCENES = {
    "aerial_day": {
        "set": "aerialKingdoms",
        "look": "DAY_SUN",
        "shadow": {"focus": [0, 0, -600], "extent": 700},
    },
    "street_day": {
        "set": "fireStreet",
        "setParams": {"flames": False, "bowls": None},
        "look": "DAY_SUN",
        "lookOverrides": {"fog": {"color": "#c4d2ec", "density": 0.0028}},
        "shadow": {"focus": [0, 2, -6], "extent": 36},
    },
    "plaza_day": {
        "set": "tabletPlaza",
        "look": "DAY_COOL",
        "shadow": {"focus": [0, 2, -6], "extent": 36},
    },
    "kitchen_day": {
        "set": "kitchen",
        "setParams": {"chairs": []},
        "look": "INTERIOR_NEUTRAL",
        "lookOverrides": {
            "lights": {
                "hemi": {"sky": "#e6ddd2", "ground": "#8a7a6a", "intensity": 1.9},
                "key": {"color": "#fff0dc", "intensity": 1.8, "from": [0.5, 0.8, 0.7], "shadow": True},
            }
        },
        "shadow": {"focus": [-4, 3, -3], "extent": 24},
    },
    "plaza_dusk": {
        "set": "tabletPlaza",
        "look": "DUSK_MAGENTA",
        "shadow": {"focus": [0, 2, -8], "extent": 44},
    },
    "plaza_storm": {
        "set": "tabletPlaza",
        "look": "NIGHT_EMBER",
        "lookOverrides": {"fog": {"color": "#1a2030", "density": 0.0040}},
        "shadow": {"focus": [0, 2, -10], "extent": 50},
    },
    "plaza_rain": {
        "set": "tabletPlaza",
        "look": "RAIN_OVERCAST",
        "shadow": {"focus": [0, 2, -8], "extent": 46},
    },
    "street_clear": {
        "set": "fireStreet",
        "setParams": {"flames": False, "bowls": None},
        "look": "DAY_SUN",
        "lookOverrides": {"fog": {"color": "#c8daf5", "density": 0.0022}},
        "shadow": {"focus": [0, 2, -6], "extent": 38},
    },
}


def actor(char, x, z, yaw=0, face="neutralTalk", faces=None, clips=None, talk=False, look=None, to=None):
    a = {"character": char, "pos": [x, z], "contactShadow": 0.7}
    if to is None:
        a["yaw"] = yaw
    else:
        a["to"] = to
    f_list = [{"f": 0, "v": face}]
    if faces:
        f_list.extend(faces)
    a["faces"] = f_list
    if clips:
        a["clips"] = clips
    if talk:
        a["talk"] = talk
    if look:
        a["look"] = look
    return a


def jar_prop(x, z, color="#8ad8ff", y=2.5, glow=0.35):
    return {
        "type": "props",
        "items": [
            {"shape": "cyl", "pos": [x, y, z], "size": [0.42, 0.90], "color": color, "glow": glow},
            {"shape": "cyl", "pos": [x, y + 0.52, z], "size": [0.34, 0.16], "color": "#b88940"},
        ],
    }


def personal_cloud(x, z, follow_idx=0, size=2.8, dark=0.45, rain=0.45, glow=0.0):
    return {
        "type": "cloud",
        "pos": [x, 7.3, z],
        "size": size,
        "dark": dark,
        "rain": rain,
        "follow": follow_idx,
        "lag": 7,
        "glow": glow,
    }


def clean_rain(cx, cz, opacity=0.28, count=1050):
    """Rain positioned slightly behind subject so character faces stay 100% sharp and readable."""
    return {"type": "rain", "count": count, "box": [26, 20, 14], "centre": [cx, 10, cz - 5], "length": 1.15, "opacity": opacity}


BEATS = [
    # Part 1: Premise
    ("01_open_world", "In this world", "aerial_day",
     [], [], [],
     {"fov": 47, "keys": [{"u": 0, "pos": [0, 175, 180], "target": [0, 0, -240]}, {"u": 1, "pos": [0, 145, 90], "target": [0, 0, -280], "ease": "linear"}]},
     None, [{"type": "whoosh_air", "at": 0}]),

    # Part 2: How it works
    ("02_chores_intro", "You see weather", "street_day",
     [actor("hero", 0, 0, 0, "neutralTalk", [{"f": 16, "v": "happyArcs"}], [{"clip": "talkBounce", "at": 0}], talk=True)],
     [{"palette": "water", "count": 16, "area": [-8, -45, 12, -14], "facing": 0, "mood": "calm", "walk": 0.45, "bothWays": True, "seed": 11}],
     [jar_prop(1.3, 0.7, "#b7e4ff")],
     cam_punch_in(0, 0, y=4.2, dist_start=12.5, dist_end=10.5), None, [{"type": "pop_soft_in", "at": 0}]),

    ("03_breeze_kids", "Breeze kids dry", "street_day",
     [actor("breeze_kid", -2, -4, 15, "bigHappy", [{"f": 14, "v": "happyArcs"}], [{"clip": "castForward", "at": 3}])],
     [],
     [jar_prop(-0.8, -3.3, "#9be3ff"), {"type": "steam", "pos": [0.8, 3.0, -3.0], "count": 40, "spread": 2.5, "rise": 1.2, "size": 0.4, "color": "#eef7ff", "opacity": 0.5}],
     cam_tight_whip(-2, -4, side=1, dist=10.8), None, [{"type": "whoosh_short", "at": 0}]),

    ("04_sun_kids", "Sun kids heat", "kitchen_day",
     [actor("bram", -3.5, -3, 25, "smug", [{"f": 14, "v": "bigHappy"}], [{"clip": "presentPlate", "at": 4}])],
     [],
     [jar_prop(-2.1, -2.5, "#ffd452", glow=0.5), {"type": "steam", "pos": [-1.8, 3.2, -2.5], "count": 30, "spread": 1.2, "rise": 1.5, "size": 0.35, "color": "#fff5d6", "opacity": 0.55}],
     cam_punch_in(-3.2, -3, y=4.1, dist_start=11.0, dist_end=9.2, fov=41), None, [{"type": "pop_b", "at": 0}]),

    ("05_mist_kids", "Mist kids water", "street_day",
     [actor("mist_kid", 2, -6, -15, "happyArcs", [{"f": 14, "v": "bigHappy"}], [{"clip": "wave", "at": 3}])],
     [],
     [jar_prop(0.9, -5.2, "#6ee7d8"), {"type": "cloud", "pos": [2.0, 7.2, -6.0], "size": 2.6, "dark": 0.1, "rain": 0.35}],
     cam_tight_whip(2, -6, side=-1, dist=10.8), None, [{"type": "pop_c", "at": 0}, {"type": "drip", "at": 10}]),

    # Part 3: Rule or limit
    ("06_one_rule", "And there's only", "plaza_day",
     [actor("hero", 0, -2, 0, "angryTalk", [{"f": 14, "v": "worried"}], [{"clip": "dramaticPoint", "at": 3}], talk=True)],
     [{"palette": "water", "count": 18, "area": [-18, -26, 18, -14], "facing": 0, "mood": "calm", "seed": 21}],
     [],
     cam_low_hero(0, -2, dist=10.0), "hit", None),

    ("07_never_bottle", "Never bottle a", "plaza_day",
     [actor("hero", 0, -2, 0, "hollowShock", [{"f": 14, "v": "worried"}], [{"clip": "headShake", "at": 2}], talk=True)],
     [],
     [{"type": "cloud", "pos": [0, 8.2, -5.0], "size": 4.2, "dark": 0.85, "rain": 0.45}],
     cam_punch_in(0, -2, y=4.65, dist_start=9.2, dist_end=7.5), None, [{"type": "riser", "at": 0, "lead": 1.2}]),

    ("08_tears_apart", "A trapped storm", "plaza_dusk",
     [actor("hero", 0, -2, 0, "worried", [{"f": 16, "v": "nervous"}], [{"clip": "lookAround", "at": 0}], talk=True)],
     [],
     [{"type": "cloud", "pos": [0, 9.5, -6.0], "size": 6.5, "dark": 0.95, "rain": 0.7}, {"type": "embers", "count": 110, "box": [24, 14, 24], "centre": [0, 6, -8], "size": 0.20}],
     cam_birds_eye(0, -4, height=14.0, dist=17.0), None, [{"type": "thunder", "at": 4}]),

    # Part 4: Odd detail
    ("09_weird_part", "But here's the", "street_day",
     [actor("hero", 0, 0, 10, "smug", [{"f": 14, "v": "neutralTalk"}], [{"clip": "talkBounce", "at": 0}], talk=True)],
     [],
     [jar_prop(1.2, 0.8, "#a8dcff")],
     cam_punch_in(0, 0, y=4.6, dist_start=9.2, dist_end=7.8), None, [{"type": "pop_soft", "at": 0}]),

    ("10_brass_vent", "Every jar has", "street_day",
     [actor("hero", 0, 0, 0, "neutralTalk", [{"f": 14, "v": "blank"}], [{"clip": "pointUp", "at": 4}], talk=True, look=[0.04, -0.02])],
     [],
     [jar_prop(1.2, 0.8, "#c2e8ff")],
     cam_punch_in(0.3, 0.2, y=4.4, dist_start=8.6, dist_end=7.4), None, [{"type": "click", "at": 6}]),

    ("11_nobody_knows", "Nobody knows why", "street_day",
     [actor("hero", 0, 0, 0, "deadpan", [{"f": 10, "v": "neutralTalk"}], [{"clip": "shrugOut", "at": 2}], talk=True)],
     [], [],
     cam_punch_in(0, 0, y=4.65, dist_start=8.2, dist_end=7.3), None, None),

    # Part 5: Narrator & flaw
    ("12_worst_jar", "And me I", "street_day",
     [actor("hero", -1, -2, 0, "worried", [{"f": 16, "v": "deadpan"}], [{"clip": "talkBounce", "at": 0}], talk=True)],
     [],
     [jar_prop(0.3, -1.3, "#7a8694", glow=0.05)],
     cam_tight_whip(-1, -2, side=-1, dist=11.0), "hit", None),

    ("13_cracked_lid", "My lid came", "street_day",
     [actor("hero", -1, -2, 5, "disgust", [{"f": 14, "v": "worried"}], [{"clip": "presentPlate", "at": 3}], talk=True)],
     [],
     [jar_prop(0.3, -1.2, "#6c7684", glow=0.0)],
     cam_punch_in(-0.8, -1.8, y=4.55, dist_start=8.8, dist_end=7.5), None, [{"type": "pop_b", "at": 4}]),

    ("14_tiny_cloud", "So it only", "street_day",
     [actor("hero", 0, -2, 0, "deadpan", [{"f": 14, "v": "worried"}], [{"clip": "rest", "at": 0}], talk=True, look=[0, -0.05])],
     [],
     [personal_cloud(0, -2, 0, size=2.6, dark=0.5, rain=0.4)],
     cam_punch_in(0, -2, y=4.3, dist_start=12.8, dist_end=11.0), None, [{"type": "pop_soft_in", "at": 6}, {"type": "rain_light", "dur": "shot", "gain": -10}]),

    ("15_loaf_sized", "Just loaf-sized", "street_day",
     [actor("hero", 0, -2, 0, "deadpan", [{"f": 10, "v": "blank"}], [{"clip": "shrugOut", "at": 2}], talk=True)],
     [],
     [personal_cloud(0, -2, 0, size=2.4, dark=0.5, rain=0.45)],
     cam_punch_in(0, -2, y=4.65, dist_start=9.2, dist_end=8.0), None, [{"type": "drip", "at": 4}]),

    ("16_leaks_walk", "It leaks a", "street_day",
     [actor("hero", -4, -4, 90, "worried", [{"f": 16, "v": "deadpan"}], [{"clip": "walk", "at": -100}], talk=True, to=[4, -4])],
     [{"palette": "water", "count": 14, "area": [-8, -30, 10, -14], "facing": 0, "mood": "calm", "walk": 0.5, "bothWays": True, "seed": 31}],
     [personal_cloud(-4, -4, 0, size=2.8, dark=0.55, rain=0.55)],
     cam_track_run(-4, -4, 4, -4, lead_x=0.5, lead_z=11.5),
     None, [{"type": "rain_light", "dur": "shot", "gain": -9}]),

    ("17_even_indoors", "Even indoors", "kitchen_day",
     [actor("hero", -3, -3, 15, "deadpan", [{"f": 10, "v": "worried"}], [{"clip": "sitIdle", "at": 0}], talk=True)],
     [],
     [personal_cloud(-3, -3, 0, size=2.6, dark=0.5, rain=0.55)],
     cam_punch_in(-3, -3, y=3.9, dist_start=11.2, dist_end=9.6, fov=40), None, [{"type": "drip", "at": 2}]),

    # Fixed staging: Hype & Mist Kid closer and facing each other (not clipped at screen edges!)
    ("18_steals_water", "Worse whenever my", "street_day",
     [
         actor("hero", -1.6, -3, 35, "worried", [{"f": 20, "v": "hollowShock"}], [{"clip": "walk", "at": -100}], talk=True, to=[-0.4, -3]),
         actor("mist_kid", 1.8, -3, -40, "blank", [{"f": 18, "v": "angryFrown"}], [{"clip": "shockJump", "at": 18}]),
     ],
     [],
     [personal_cloud(-1.6, -3, 0, size=3.3, dark=0.65, rain=0.85)],
     cam_punch_in(0.4, -3, y=4.2, dist_start=13.5, dist_end=11.5), None, [{"type": "splash", "at": 30}, {"type": "rain_light", "dur": "shot", "gain": -8}]),

    # Part 6: Cost & rival
    ("19_bram_intro", "Bram has the", "plaza_day",
     [actor("bram", 0, -3, 0, "smug", [{"f": 16, "v": "bigHappy"}], [{"clip": "armsCrossed", "at": 0}])],
     [{"palette": "fire", "count": 14, "area": [-16, -24, 16, -13], "facing": 0, "mood": "cheer", "cheer": 0.35, "seed": 41}],
     [jar_prop(1.4, -2.2, "#ffd94a", glow=0.7)],
     cam_low_hero(0, -3, dist=9.6), "hit", None),

    ("20_bram_laughed", "He laughed when", "plaza_day",
     [
         actor("bram", 1.6, -3, -35, "laugh", [{"f": 14, "v": "smug"}], [{"clip": "dramaticPoint", "at": 3}]),
         actor("hero", -1.6, -3, 35, "worried", [{"f": 14, "v": "deadpan"}], [{"clip": "headShake", "at": 4}]),
     ],
     [],
     [personal_cloud(-1.6, -3, 1, size=2.8, dark=0.55, rain=0.75)],
     cam_ots(1.6, -3, -1.6, -3, side=-1), None, [{"type": "splash", "at": 8}]),

    ("21_calls_puddle", "He calls me", "plaza_day",
     [actor("bram", 0, -3, 0, "smug", [{"f": 12, "v": "laugh"}], [{"clip": "dramaticPoint", "at": 3}], talk=True)],
     [], [],
     cam_punch_in(0, -3, y=4.65, dist_start=8.8, dist_end=7.4), None, [{"type": "pop_c", "at": 8}]),

    ("22_everyone_puddle", "Now everyone calls", "street_day",
     [actor("hero", 0, -3, 0, "deadpan", [{"f": 14, "v": "worried"}], [{"clip": "walk", "at": -100}], talk=True, to=[0, 1.0])],
     [{"palette": "water", "count": 22, "area": [-10, -28, 14, -12], "facing": 0, "mood": "cheer", "cheer": 0.25, "seed": 45}],
     [personal_cloud(0, -3, 0, size=2.7, dark=0.55, rain=0.45)],
     cam_track_run(0, -3, 0, 1.0, lead_x=1.2, lead_z=10.5), None, None),

    # Part 7: Keepsake (Grandpa — fixed over-the-shoulder framing, no cropped faces!)
    ("23_grandpa_says", "Grandpa always says", "kitchen_day",
     [
         actor("grandpa", -3.8, -3.5, 30, "dotSmile", [{"f": 16, "v": "neutralTalk"}], [{"clip": "sitIdle", "at": 0}, {"clip": "nodYes", "at": 8}]),
         actor("hero", -1.2, -2.5, -40, "neutralTalk", [{"f": 16, "v": "happyArcs"}], [{"clip": "sitIdle", "at": 0}]),
     ],
     [], [],
     cam_ots(-3.8, -3.5, -1.2, -2.5, side=1, fov=40), None, [{"type": "pop_soft", "at": 0}]),

    ("24_storm_heavy", "A storm isn't", "kitchen_day",
     [actor("grandpa", -3.8, -3.5, 20, "dotSmile", [{"f": 18, "v": "neutralTalk"}], [{"clip": "talkBounce", "at": 0}], talk=True)],
     [], [],
     cam_punch_in(-3.8, -3.5, y=4.5, dist_start=8.8, dist_end=7.4, fov=40), None, None),

    ("25_never_got_it", "I never got", "kitchen_day",
     [actor("hero", -1.2, -2.5, -20, "blank", [{"f": 12, "v": "deadpan"}], [{"clip": "shrugOut", "at": 3}], talk=True)],
     [], [],
     cam_punch_in(-1.2, -2.5, y=4.5, dist_start=8.6, dist_end=7.4, fov=40), None, None),

    # Part 8: The Turn
    ("26_summer_fair", "Then came the", "plaza_dusk",
     [actor("hero", 0, -2, 0, "worried", [{"f": 14, "v": "nervous"}], [{"clip": "lookAround", "at": 0}], talk=True)],
     [{"palette": "fire", "count": 36, "area": [-20, -26, 20, -12], "facing": 0, "mood": "cheer", "cheer": 0.3, "seed": 51}],
     [],
     cam_birds_eye(0, -6, height=17.0, dist=18.0), "hit", [{"type": "riser_burst", "at": 0, "lead": 1.6}]),

    ("27_bram_prove", "Bram wanted to", "plaza_dusk",
     [actor("bram", 0, -6, 0, "smug", [{"f": 16, "v": "bigHappy"}], [{"clip": "armsUp", "at": 4}])],
     [{"palette": "fire", "count": 26, "area": [-18, -24, 18, -14], "facing": 0, "mood": "cheer", "seed": 52}],
     [jar_prop(1.4, -5.2, "#ffd94a", glow=0.7)],
     cam_low_hero(0, -6, dist=9.8), None, None),

    ("28_climbed_wall", "He climbed the", "plaza_dusk",
     [actor("bram", 0, -14, 0, "grittedAngry", [{"f": 18, "v": "bigHappy"}], [{"clip": "castUpBoth", "at": 6}])],
     [],
     [
         jar_prop(1.3, -13.2, "#ffd94a", y=3.1, glow=0.8),
         {"type": "cloud", "pos": [0, 10.5, -14.0], "size": 9.0, "dark": 0.98, "rain": 0.7, "glow": 0.25},
     ],
     cam_low_hero(0, -14, dist=16.0), None, [{"type": "riser", "at": 0, "lead": 1.4}]),

    # Sound beat: Crack!
    ("29_crack", "Crack", "plaza_storm",
     [actor("bram", 0, -14, 0, "hollowShock", [{"f": 6, "v": "scream"}], [{"clip": "shockJump", "at": 0}])],
     [],
     [
         {"type": "cloud", "pos": [0, 11.0, -14.0], "size": 12.0, "dark": 1.0, "rain": 0.9, "glow": 0.35},
         {"type": "embers", "count": 180, "box": [26, 16, 20], "centre": [0, 7, -17], "size": 0.24, "gain": 2.1},
     ],
     cam_impact_hit(0, -14, dist=12.0, y=4.6), "hit", [{"type": "thunder", "at": 0}]),

    ("30_glass_split", "The glass split", "plaza_storm",
     [actor("hero", 0, 2, 180, "hollowShock", [{"f": 12, "v": "scream"}], [{"clip": "shockJump", "at": 3}])],
     [],
     [
         {"type": "cloud", "pos": [0, 12.0, -14.0], "size": 15.0, "dark": 1.0, "rain": 0.9, "glow": 0.3},
         clean_rain(0, -2, opacity=0.30, count=1100),
     ],
     cam_birds_eye(0, -8, height=14.0, dist=18.0),
     None, [{"type": "rain_heavy", "dur": "shot", "gain": -9}]),

    ("31_pitch_black", "Pitch black", "plaza_storm",
     [actor("hero", 0, 0, 0, "hollowShock", [{"f": 8, "v": "nervous"}], [{"clip": "lookAround", "at": 0}], look=[0, -0.05])],
     [],
     [clean_rain(0, -2, opacity=0.26, count=900)],
     cam_punch_in(0, 0, y=4.65, dist_start=9.2, dist_end=7.5), None, [{"type": "thunder", "at": 0}]),

    # Part 9: Everyone else fails (3 tries — faces crisp, tight whip-ins!)
    ("32_breeze_fail", "The breeze kids", "plaza_storm",
     [actor("breeze_kid", -3, -4, 180, "grittedAngry", [{"f": 18, "v": "hollowShock"}], [{"clip": "castForward", "at": 3}])],
     [{"palette": "water", "count": 22, "area": [-18, -24, 18, -14], "facing": 0, "mood": "panic", "run": True, "walk": 0.5, "seed": 61}],
     [
         {"type": "cloud", "pos": [0, 12.0, -14.0], "size": 15.0, "dark": 1.0, "rain": 0.9, "glow": 0.25},
         {"type": "steam", "pos": [-2, 4.0, -8.5], "count": 55, "spread": 3.5, "rise": 2.0, "size": 0.55, "color": "#cbd8e6", "opacity": 0.45},
     ],
     cam_tight_whip(-3, -4, side=1, dist=11.8), None, [{"type": "whoosh_air", "at": 4}, {"type": "rain_heavy", "dur": "shot", "gain": -10}]),

    ("33_sun_fail", "The sun kids", "plaza_storm",
     [actor("bram", 3, -5, 180, "grittedAngry", [{"f": 20, "v": "scream"}], [{"clip": "castForward", "at": 4}])],
     [],
     [
         {"type": "jet", "from": [3, 3.2, -5.8], "dir": [0, 0.35, -1], "length": 10, "start": 12},
         {"type": "steam", "pos": [2, 6.0, -12.0], "count": 75, "spread": 5.5, "rise": 2.2, "size": 0.8, "color": "#d8e0e8", "opacity": 0.65},
     ],
     cam_tight_whip(3, -5, side=-1, dist=11.8), "hit", [{"type": "hiss", "at": 14}, {"type": "rain_heavy", "dur": "shot", "gain": -10}]),

    ("34_guards_fail", "Even the guards", "plaza_storm",
     [actor("guard", 0, -4, 180, "angryTalk", [{"f": 18, "v": "hollowShock"}], [{"clip": "castUpBoth", "at": 4}])],
     [],
     [
         {"type": "cloud", "pos": [0, 12.0, -14.0], "size": 15.0, "dark": 1.0, "rain": 0.9, "glow": 0.35},
         {"type": "embers", "count": 160, "box": [22, 16, 18], "centre": [0, 7, -13], "size": 0.22, "gain": 2.1},
     ],
     cam_impact_hit(0, -4, dist=12.0, y=4.3), None, [{"type": "thunder", "at": 14}]),

    ("35_bram_trapped", "Bram fell behind", "plaza_storm",
     [actor("bram", -2, -10, 20, "scream", [{"f": 18, "v": "nervous"}], [{"clip": "cryShake", "at": 0}])],
     [],
     [
         {"type": "embers", "count": 140, "box": [16, 12, 14], "centre": [-2, 5, -14], "size": 0.20, "gain": 2.0},
         clean_rain(-2, -10, opacity=0.28, count=950),
     ],
     cam_punch_in(-2, -10, y=4.2, dist_start=10.8, dist_end=8.4), None, [{"type": "crowd_panic", "dur": "shot", "gain": -12}]),

    # Part 10: The Reframe
    ("36_understood", "That's when I", "plaza_storm",
     [actor("hero", 0, 2, 0, "blank", [{"f": 14, "v": "neutralTalk"}, {"f": 26, "v": "bigHappy"}], [{"clip": "nodYes", "at": 16}], talk=True)],
     [],
     [clean_rain(0, 2, opacity=0.22, count=750)],
     cam_punch_in(0, 2, y=4.65, dist_start=9.5, dist_end=7.3), "hit", [{"type": "riser_burst", "at": 0, "lead": 1.2}]),

    # Part 11: The Act
    ("37_sprint_in", "I sprinted into", "plaza_storm",
     [actor("hero", 0, 6, 180, "grittedAngry", [{"f": 20, "v": "angryTalk"}], [{"clip": "runLeaning", "at": -100}], talk=True, to=[0, -6])],
     [],
     [
         personal_cloud(0, 6, 0, size=3.0, dark=0.6, rain=0.55, glow=0.2),
         {"type": "cloud", "pos": [0, 12.0, -14.0], "size": 15.0, "dark": 1.0, "rain": 0.9, "glow": 0.3},
     ],
     cam_track_run(0, 6, 0, -6, lead_x=4.5, lead_z=8.5),
     None, [{"type": "whoosh_quick", "at": 0}, {"type": "rain_heavy", "dur": "shot", "gain": -9}]),

    ("38_first_try_fail", "The gale slammed", "plaza_storm",
     [actor("hero", 0, -6, 0, "scream", [{"f": 16, "v": "grittedAngry"}], [{"clip": "shockJump", "at": 2}, {"clip": "castUpBoth", "at": 12}], talk=True)],
     [],
     [
         personal_cloud(0, -6, 0, size=3.2, dark=0.65, rain=0.65, glow=0.22),
         clean_rain(0, -6, opacity=0.28, count=1000),
     ],
     cam_impact_hit(0, -6, dist=11.0, y=4.3), "hit", [{"type": "whoosh_air", "at": 4}]),

    # Fixed jar_prop position: held out to side at hand height (x=1.2, y=3.0) instead of blocking Hype's eyes!
    ("39_touch_belly", "My little cloud", "plaza_storm",
     [actor("hero", 0, -8, 0, "grittedAngry", [{"f": 14, "v": "hollowShock"}], [{"clip": "castUpBoth", "at": 0}], talk=True, look=[0, -0.05])],
     [],
     [
         {"type": "cloud", "pos": [0, 11.5, -10.0], "size": 14.0, "dark": 0.95, "rain": 0.85, "glow": 0.35},
         jar_prop(1.25, -7.4, "#9b4dff", y=3.1, glow=0.85),
     ],
     cam_low_hero(0, -8, dist=11.5), None, [{"type": "riser", "at": 0, "lead": 1.5}]),

    ("40_whoosh_drain", "Whoosh", "plaza_rain",
     [actor("hero", 0, -8, 0, "bigHappy", [{"f": 20, "v": "happyArcs"}], [{"clip": "armsUp", "at": 3}], talk=True)],
     [{"palette": "water", "count": 30, "area": [-18, -24, 18, -14], "facing": 0, "mood": "stunned", "seed": 71}],
     [
         {"type": "cloud", "pos": [0, 10.5, -9.0], "size": 8.0, "dark": 0.5, "rain": 0.95, "vanish": 65},
         clean_rain(0, -8, opacity=0.34, count=1300),
         {"type": "water", "pos": [0, 0.08, -6], "size": [18, 22]},
     ],
     cam_impact_hit(0, -8, dist=16.0, y=4.8), "whoosh", [{"type": "splash", "at": 0}, {"type": "rain_heavy", "dur": "shot", "gain": -8}]),

    ("41_sky_splits", "The thunder stopped", "plaza_day",
     [actor("hero", 0, -6, 0, "happyArcs", [{"f": 14, "v": "bigHappy"}], [{"clip": "rest", "at": 0}], talk=True)],
     [{"palette": "water", "count": 30, "area": [-18, -24, 18, -14], "facing": 0, "mood": "stunned", "seed": 71}],
     [],
     cam_birds_eye(0, -6, height=14.0, dist=16.0), None, [{"type": "bell_pop", "at": 4}]),

    ("42_town_froze", "The whole town", "street_clear",
     [
         actor("hero", -1.4, -4, 25, "neutralTalk", [{"f": 20, "v": "happyArcs"}], [{"clip": "rest", "at": 0}], talk=True),
         actor("bram", 2.8, -4, -35, "worried", [{"f": 20, "v": "dotSmile"}], [{"clip": "walk", "at": -100}, {"clip": "presentPlate", "at": 20}], to=[1.2, -4]),
     ],
     [{"palette": "water", "count": 24, "area": [-10, -28, 12, -14], "facing": 0, "mood": "stunned", "seed": 75}],
     [],
     cam_ots(-1.4, -4, 1.8, -4, side=1), None, [{"type": "crowd_cheer", "at": 20, "gain": -12}]),

    # Part 12: Coda + callback joke
    ("43_plaza_roof", "Now I work", "plaza_day",
     [actor("hero", 0, -2, 0, "smug", [{"f": 16, "v": "bigHappy"}], [{"clip": "wave", "at": 6}], talk=True)],
     [{"palette": "fire", "count": 18, "area": [-18, -24, 18, -13], "facing": 0, "mood": "cheer", "cheer": 0.4, "seed": 81}],
     [personal_cloud(0, -2, 0, size=2.4, dark=0.15, rain=0.0)],
     cam_low_hero(0, -2, dist=10.5), None, [{"type": "pop_soft_in", "at": 0}]),

    ("44_dry_socks", "Well except Bram", "street_clear",
     [
         actor("hero", -1.3, -2, 20, "laugh", [{"f": 16, "v": "bigHappy"}], [{"clip": "talkBounce", "at": 0}], talk=True),
         actor("bram", 1.5, -2, -25, "bigHappy", [{"f": 14, "v": "laugh"}], [{"clip": "presentPlate", "at": 4}]),
     ],
     [],
     [personal_cloud(-1.3, -2, 0, size=2.2, dark=0.1, rain=0.15)],
     cam_punch_in(0.1, -2, y=4.3, dist_start=11.5, dist_end=9.8), None, [{"type": "pop_b", "at": 10}]),
]

shots = []
beat_rows = []
cursor = 0
for idx, (sid, anchor, scene_key, actors_list, crowds_list, vfx_list, camera, sound, sfx_list) in enumerate(BEATS):
    cue = find_word(anchor, cursor)
    cursor = cue + 1
    sc = SCENES[scene_key]
    shot = {
        "id": sid,
        "cue": cue,
        "set": sc["set"],
        "look": sc["look"],
        "actors": actors_list,
        "camera": camera,
        "motionBlur": "auto",
    }
    if "setParams" in sc:
        shot["setParams"] = sc["setParams"]
    if "lookOverrides" in sc:
        shot["lookOverrides"] = sc["lookOverrides"]
    if "shadow" in sc:
        shot["shadow"] = sc["shadow"]
    if crowds_list:
        shot["crowds"] = crowds_list
    if vfx_list:
        shot["vfx"] = vfx_list
    if sound:
        shot["sound"] = sound
    if sfx_list:
        shot["sfx"] = sfx_list
    shots.append(shot)

for i, shot in enumerate(shots):
    w0 = shot["cue"]
    w1 = (shots[i + 1]["cue"] - 1) if i + 1 < len(shots) else (len(tokens) - 1)
    excerpt = " ".join(tokens[w0 : min(w0 + 10, w1 + 1)])
    if w1 - w0 >= 10:
        excerpt += " ..."
    vfx_names = ", ".join(v["type"] for v in shot.get("vfx", [])) or "-"
    sfx_names = ", ".join(s["type"] for s in shot.get("sfx", []))
    if shot.get("sound"):
        sfx_names = shot["sound"] + (", " + sfx_names if sfx_names else "")
    sfx_names = sfx_names or "-"
    beat_rows.append(
        f"| {i+1} | `{shot['id']}` | {w0}–{w1} | {excerpt} | `{shot['set']}` / `{shot['look']}` | {vfx_names} | {sfx_names} |"
    )

story = {
    "audio": "audio/storm_cloud.wav",
    "names": ["Bram", "Puddle", "Grandpa"],
    "sfx": ["CRACK", "WHOOSH"],
    "endHoldFrames": 32,
    "shots": shots,
}

OUT_STORY.write_text(json.dumps(story, indent=2), encoding="utf-8")
OUT_BEATS.write_text(
    "# Beat Table — Never Bottle A Storm Cloud (Upgraded Animation, Camera & Exact Caption Sync)\n\n"
    f"Total words: {len(tokens)} | Total shots: {len(shots)} | Estimated length: ~{round(word_times[-1])}s\n\n"
    "| # | Shot ID | Words | Line | Set / Look | VFX | Sound |\n"
    "|---|---|---|---|---|---|---|\n"
    + "\n".join(beat_rows)
    + "\n",
    encoding="utf-8",
)
print(f"Generated {OUT_STORY.name} ({len(shots)} shots, exact {len(tokens)}-word sync) and {OUT_BEATS.name}")
