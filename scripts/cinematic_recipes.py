"""Reusable viral-Shorts camera & staging recipes for ANY new blocky-3d-story-video project.

Import in projects/<name>/make_story.py:
    from cinematic_recipes import (
        cam_punch_in, cam_ots, cam_low_hero, cam_insert_prop,
        cam_track_run, cam_birds_eye, cam_whip_cut, cam_impact_hit
    )
"""


def cam_punch_in(tx, tz, y=4.65, dist_start=11.0, dist_end=7.4, fov=45, shake=None):
    """Fast easeOutCubic zoom onto eyes/face for shocking reveals & dialogue punchlines."""
    c = {
        "fov": fov,
        "keys": [
            {"u": 0, "pos": [tx, y + 0.15, tz + dist_start], "target": [tx, y, tz]},
            {"u": 0.35, "pos": [tx, y + 0.05, tz + dist_end], "target": [tx, y, tz], "ease": "easeOutCubic"},
            {"u": 1, "pos": [tx, y + 0.05, tz + dist_end * 0.94], "target": [tx, y, tz], "ease": "linear"},
        ],
    }
    if shake:
        c["shake"] = shake
    return c


def cam_ots(speaker_x, speaker_z, listener_x, listener_z, side=1, fov=43):
    """Clean over-the-shoulder dialogue shot (never crowd 4 people behind the hero)."""
    cam_x = round(listener_x + side * 2.4, 2)
    cam_z = round(listener_z + 4.8, 2)
    return {
        "fov": fov,
        "keys": [
            {"u": 0, "pos": [cam_x, 4.5, cam_z], "target": [speaker_x, 4.4, speaker_z]},
            {"u": 1, "pos": [round(cam_x - side * 0.4, 2), 4.5, round(cam_z - 0.9, 2)], "target": [speaker_x, 4.4, speaker_z], "ease": "linear"},
        ],
    }


def cam_low_hero(tx, tz, dist=9.5, fov=48):
    """Low-angle upward power shot for bullies, villains, or heroic climax moments."""
    return {
        "fov": fov,
        "keys": [
            {"u": 0, "pos": [tx + 1.2, 2.2, tz + dist], "target": [tx, 4.5, tz]},
            {"u": 1, "pos": [tx + 0.6, 2.0, tz + dist * 0.82], "target": [tx, 4.6, tz], "ease": "easeOutQuad"},
        ],
    }


def cam_insert_prop(px, py, pz, dist=5.2, fov=40):
    """Tight object cutaway (clocks, chains, doors, jars, glowing chests, feet)."""
    return {
        "fov": fov,
        "keys": [
            {"u": 0, "pos": [px + 0.6, py + 0.4, pz + dist], "target": [px, py, pz]},
            {"u": 1, "pos": [px + 0.2, py + 0.3, pz + dist * 0.82], "target": [px, py, pz], "ease": "easeOutCubic"},
        ],
    }


def cam_track_run(x0, z0, x1, z1, lead_x=2.8, lead_z=8.5, fov=48):
    """Dynamic camera racing ahead of a running/walking character."""
    return {
        "fov": fov,
        "keys": [
            {"u": 0, "pos": [x0 + lead_x, 4.0, z0 + lead_z], "target": [x0, 4.1, z0]},
            {"u": 1, "pos": [x1 + lead_x * 0.7, 3.8, z1 + lead_z * 0.85], "target": [x1, 4.1, z1], "ease": "linear"},
        ],
        "shake": [{"f0": 0, "f1": 90, "ampDeg": [0.08, 0.14], "mode": "random"}],
    }


def cam_birds_eye(tx, tz, height=26.0, dist=18.0, fov=50):
    """High top-down establishing / town-wide disaster shot."""
    return {
        "fov": fov,
        "keys": [
            {"u": 0, "pos": [tx, height, tz + dist], "target": [tx, 2.0, tz]},
            {"u": 1, "pos": [tx, height * 0.84, tz + dist * 0.82], "target": [tx, 2.0, tz], "ease": "linear"},
        ],
    }


def cam_whip_cut(tx, tz, side=1, dist=10.5, y=4.3, fov=47):
    """Fast whip-pan arrival + smooth creep-in (matches viral Shorts energy)."""
    p0 = [tx, y + 0.15, tz + dist]
    p1 = [tx, y + 0.1, tz + dist * 0.86]
    return {
        "fov": fov,
        "keys": [
            {"f": -1, "pos": p0, "target": [tx + side * 8.5, y, tz]},
            {"f": 4, "pos": p0, "target": [tx, y, tz], "ease": "easeOutCubic"},
            {"u": 1, "pos": p1, "target": [tx, y, tz], "ease": "linear"},
        ],
    }


def cam_impact_hit(tx, tz, dist=9.0, y=4.4, fov=47):
    """Hard impact zoom + damped shake for explosions, slams, and sound-word beats."""
    return cam_punch_in(
        tx, tz, y=y, dist_start=dist * 1.25, dist_end=dist * 0.85, fov=fov,
        shake=[{"f0": 0, "f1": 12, "ampDeg": [0.55, 0.55], "mode": "alt", "decay": 0.74}],
    )
