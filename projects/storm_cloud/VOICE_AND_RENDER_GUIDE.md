# Never Bottle A Storm Cloud — Voice-Over & Antigravity Render Guide

## 1. Drop into your Antigravity studio
Copy this `storm_cloud/` folder into `<your-studio>/projects/storm_cloud/`.

## 2. Record or generate the voice-over (Stage 3)
Read `script.txt` and save the audio as `projects/storm_cloud/audio/narration.wav`.

**Target voice prompt (if using TTS):**
> A teenage boy, around 14 to 16, with a light, clear, slightly high voice. Fast, energetic storytelling pace (~188 wpm), like a kid excitedly telling a friend an unbelievable story. Deadpan and matter-of-fact on ordinary lines, then suddenly dramatic on big moments. Crisp, punchy delivery with very short pauses between sentences (~0.36 s). Bright, clean, close-microphone studio sound with no echo and no background noise. Not a cartoon voice and not a small child.

## 3. Run in Antigravity (from your studio root)
Replace `<venv-python>` with `.venv/Scripts/python` (Windows) or `.venv/bin/python` (macOS/Linux).

```bash
# Stage 3: Align and check voice-over
<venv-python> scripts/align.py projects/storm_cloud/audio/narration.wav projects/storm_cloud/script.txt projects/storm_cloud/words.json
<venv-python> scripts/voice_check.py projects/storm_cloud/audio/narration.wav projects/storm_cloud/words.json

# (Optional if pauses are > 0.42s)
<venv-python> scripts/tighten_pauses.py projects/storm_cloud/audio/narration.wav projects/storm_cloud/words.json projects/storm_cloud/audio/narration_tight.wav

# Regenerate story.json with exact word-aligned VFX timings
<venv-python> projects/storm_cloud/make_story.py

# Stage 4: Render character sheets
npx tsx scripts/sheet-props.ts projects/storm_cloud sheet.cast
npx remotion still src/index.ts CastSheet out/storm_cloud_cast.png --props=projects/storm_cloud/sheet.json --gl=angle

# Stage 5: Build video + storyboard check
npx tsx scripts/build-video.ts projects/storm_cloud
npx tsx scripts/storyboard.ts projects/storm_cloud

# Stage 6: Mix narration + SFX (copy extra-sounds/*.wav into sfx/ first for rain_light, rain_heavy, thunder, splash, drip)
<venv-python> scripts/mix_audio.py projects/storm_cloud/audio/narration.wav projects/storm_cloud/words.json public/audio/storm_cloud.wav --sounds projects/storm_cloud/sounds.json --sfx-dir sfx

# Stage 7: Render final MP4
npx remotion render src/index.ts Final out/storm_cloud.mp4 --props=projects/storm_cloud/final.json --gl=angle --crf=16 --concurrency=2 --timeout=180000

# Stage 8: Verify & score
<venv-python> scripts/verify_final.py out/storm_cloud.mp4 projects/storm_cloud/final.json
```
