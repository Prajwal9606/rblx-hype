# RBLX HYPE Master Upgrade Pack

1. Unzip this archive directly into your Antigravity studio root folder (overwrites `build.ts`, `hair.ts`, `outfits.ts`, `cast.ts`, `clips.ts`, `Captions.tsx`, `data/cast.json`, and adds `public/faces/` + `projects/hype_short_45s/`).
2. Generate tightened **Iapetus (Male)** voice + 1:1 captions + `final.json` for the new 43-second Short (or any existing project):
   ```bash
   .venv/Scripts/python scripts/generate_iapetus_voice.py projects/hype_short_45s
   ```
3. Render the 43-second MP4:
   ```bash
   npx remotion render src/index.ts Final out/hype_short_45s.mp4 --props=projects/hype_short_45s/final.json --gl=angle --crf=16 --concurrency=2 --timeout=180000
   ```
