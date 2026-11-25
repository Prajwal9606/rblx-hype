import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

"""
RBLX Hype Unified Studio Pipeline:
Combines:
  1. `blocky-shorts` (Fast data-driven 9:16 vertical storytelling, punch FX, camera push/crash)
  2. `roblox-story-kit` (First-person narrator rules, "In this world...", fast cuts, sound design)
  3. `blocky-3d-story-video` (Remotion + Three.js rendering, word-level audio alignment, watermark)
"""

BASE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = BASE_DIR / "scripts"
OUT_DIR = BASE_DIR / "out"
PUBLIC_DIR = BASE_DIR / "public"

def run_cmd(cmd, env=None, cwd=None):
    print(f"\n[RUNNING] {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, shell=True, env=env, cwd=cwd)
    if res.returncode != 0:
        print(f"[ERROR] Command failed with return code {res.returncode}")
        return False
    return True

def run_pipeline(slug, voice="iapetus", render=True):
    print(f"=== Starting Unified 1-Click Pipeline for [{slug}] ===")
    proj_dir = BASE_DIR / "projects" / slug
    if not proj_dir.exists():
        print(f"Project directory {proj_dir} not found!")
        return False

    script_path = proj_dir / "script.txt"
    wav_path = proj_dir / "audio" / "narration.wav"
    
    # Step 1: Voice Generation (Gemini TTS / Iapetus)
    if not wav_path.exists():
        print("--> Generating Voiceover with Google AI (Iapetus)...")
        gen_voice_script = SCRIPTS_DIR / "generate_iapetus_voice.py"
        if gen_voice_script.exists():
            run_cmd(f'.venv\\Scripts\\python scripts/generate_iapetus_voice.py projects/{slug}')

    # Step 2: Alignment (Faster-Whisper word-level timestamps)
    print("--> Aligning Speech to Words (Faster-Whisper)...")
    run_cmd(f'.venv\\Scripts\\python scripts/align.py projects/{slug}/audio/narration.wav projects/{slug}/script.txt projects/{slug}/words.json')

    # Step 3: Build Remotion Storyboard & Timeline Props
    print("--> Building Remotion Timeline & Props...")
    run_cmd(f'npx.cmd tsx scripts/build-video.ts projects/{slug}')

    # Step 4: Audio Mix & Sound Effects
    print("--> Mixing Audio, SFX and Ambience...")
    run_cmd(f'.venv\\Scripts\\python scripts/mix_audio.py projects/{slug}/audio/narration.wav projects/{slug}/words.json public/audio/{slug}.wav --sounds projects/{slug}/sounds.json --sfx-dir sfx')

    # Step 5: Render Final 9:16 MP4 with Watermark
    if render:
        print("--> Rendering Master 9:16 Video with Remotion...")
        out_mp4 = OUT_DIR / f"{slug}.mp4"
        run_cmd(f'npx.cmd remotion render src/index.ts Final out/{slug}.mp4 --props=projects/{slug}/final.json --gl=angle --crf=16 --concurrency=2 --timeout=180000')
        print(f"✅ Video Render Complete: {out_mp4}")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unified 1-Click RBLX Hype Studio Pipeline")
    parser.add_argument("slug", help="Project slug (e.g. hype_short_45s, town_shadows_45s)")
    parser.add_argument("--voice", default="iapetus", help="TTS voice choice")
    parser.add_argument("--no-render", action="store_true", help="Skip remotion render")
    args = parser.parse_args()
    
    run_pipeline(args.slug, voice=args.voice, render=not args.no_render)
