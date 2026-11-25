#!/usr/bin/env python3
"""1-command Google Gemini TTS 'Iapetus' (Male) generator + automatic pause tightening + exact caption sync.

Usage (from your Antigravity studio root, with GEMINI_API_KEY set):
    .venv/Scripts/python scripts/generate_iapetus_voice.py projects/hype_short_45s
"""
import os
import shutil
import subprocess
import sys
import wave
from pathlib import Path

from google import genai
from google.genai import types

proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("projects/hype_short_45s")
script_path = proj / "script.txt"
audio_dir = proj / "audio"
audio_dir.mkdir(parents=True, exist_ok=True)
raw_wav = audio_dir / "narration_raw.wav"
final_wav = audio_dir / "narration.wav"
words_json = proj / "words.json"

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: Set GEMINI_API_KEY in your environment first.")
    sys.exit(1)

script_text = script_path.read_text(encoding="utf-8").strip()
prompt = (
    "Speak as a crisp, high-energy teenage male storyteller at a fast 190 words per minute YouTube Shorts pace. "
    "Keep pauses between sentences very short (~0.30s). Stay deadpan on setup lines and punch hard on dramatic words. "
    "Read every word verbatim:\n\n" + script_text
)

print("Generating Google Gemini TTS voice: Iapetus (Male)...")
client = genai.Client(api_key=api_key, http_options={"api_version": "v1beta"})
interaction = client.interactions.create(
    model="gemini-3.8-flash-tts",
    input=prompt,
    response_modalities=["audio"],
    generation_config={"speech_config": [{"voice": "Iapetus"}]},
)

audio_out = getattr(interaction, "output_audio", None)
if audio_out is None and getattr(interaction, "outputs", None):
    for item in interaction.outputs:
        if getattr(item, "type", None) == "audio":
            audio_out = item
            break

if audio_out is None:
    raise RuntimeError(f"No audio output in interaction: {interaction}")

raw = audio_out.data
if isinstance(raw, str):
    import base64
    raw = base64.b64decode(raw)

mime = getattr(audio_out, "mime_type", "") or ""
if raw[:4] == b"RIFF" or "wav" in mime.lower():
    raw_wav.write_bytes(raw)
else:
    with wave.open(str(raw_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(raw)

py = sys.executable
# 1. Initial alignment
subprocess.run([py, "scripts/align.py", str(raw_wav), str(script_path), str(words_json)], check=True)

# 2. Automatically tighten pauses for punchy 185-195 WPM Shorts pacing
tight_script = Path("scripts/tighten_pauses.py")
if tight_script.exists():
    subprocess.run([py, str(tight_script), str(raw_wav), str(words_json), str(final_wav)], check=True)
    subprocess.run([py, "scripts/align.py", str(final_wav), str(script_path), str(words_json)], check=True)
else:
    shutil.copyfile(raw_wav, final_wav)

subprocess.run([py, "scripts/voice_check.py", str(final_wav), str(words_json)], check=True)

# 3. Rebuild story.json (1:1 synced to words.json), final.json, and mixed SFX audio
if (proj / "make_story.py").exists():
    subprocess.run([py, str(proj / "make_story.py")], check=True)
subprocess.run(["npx.cmd", "tsx", "scripts/build-video.ts", str(proj)], check=True, shell=True)
subprocess.run(
    [py, "scripts/mix_audio.py", str(final_wav), str(words_json), f"public/audio/{proj.name}.wav",
     "--sounds", str(proj / "sounds.json"), "--sfx-dir", "sfx"],
    check=True,
)
print(f"Done! Tightened Iapetus narration + 1:1 captions + final.json ready in {proj}")
