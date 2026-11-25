# GSD State - RBLX Hype Blocky Studio Installation

## Current Objectives
- Install the Blocky Studio template from `blocky-3d-story-video` into `C:\Users\Admin\Videos\RBLX Hype` without overwriting existing `projects/storm_cloud`, `scripts/`, or `src/` files.
- Install Node.js (`npm install`) and Python (`.venv` + `requirements.txt`) dependencies.
- Verify the studio installation with typecheck and Remotion/Python checks.

## Milestones
- [x] M1: Inspect template and copy missing studio files into `C:\Users\Admin\Videos\RBLX Hype` (91 files copied; `src\engine\anim\clips.ts` preserved).
- [x] M2: Install Node.js dependencies (`npm install`) and Python `.venv` dependencies (Python 3.12 + `requirements.txt`).
- [x] M3: Verify TypeScript (`tsc --noEmit`) and Python/Remotion tooling.

## Architecture Decisions
- Configured `.venv` with Python 3.12 (`py -3.12 -m venv .venv`) for pre-compiled binary wheels (`av`, `onnxruntime`, `ctranslate2`, `faster-whisper`, `opencv-python-headless`).
- Preserved existing workspace files (`projects/storm_cloud`, `scripts/cinematic_recipes.py`, `scripts/generate_iapetus_voice.py`, `src/engine/anim/clips.ts`) during template copy.
