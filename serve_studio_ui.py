import os
import sys
import json
import subprocess
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = 5050
BASE_DIR = Path(__file__).resolve().parent

class StudioHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            ui_path = BASE_DIR / "public" / "studio_ui.html"
            self.wfile.write(ui_path.read_bytes())
            return
        elif self.path.startswith("/out/"):
            file_name = self.path[len("/out/"):]
            file_path = BASE_DIR / "out" / file_name
            if file_path.exists():
                self.send_response(200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Content-Length", str(file_path.stat().st_size))
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return
        elif self.path.startswith("/models/"):
            file_name = self.path[len("/models/"):]
            file_path = BASE_DIR / "public" / "models" / file_name
            if file_path.exists():
                content_type = "application/octet-stream"
                if file_name.endswith(".obj") or file_name.endswith(".mtl"):
                    content_type = "text/plain"
                elif file_name.endswith(".glb"):
                    content_type = "model/gltf-binary"
                elif file_name.endswith(".gltf"):
                    content_type = "model/gltf+json"
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(file_path.stat().st_size))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return
        
        super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        data = json.loads(body) if body else {}

        if self.path == "/api/run":
            slug = data.get("slug", "town_shadows_45s")
            mode = data.get("mode", "full")
            voice = data.get("voice", "iapetus")

            no_render_flag = " --no-render" if mode == "quick" else ""
            cmd = f'.venv\\Scripts\\python run_studio_pipeline.py {slug} --voice {voice}{no_render_flag}'
            
            print(f"[UI TRIGGER] {cmd}")
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=str(BASE_DIR))
            
            output = proc.stdout + "\n" + proc.stderr
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": proc.returncode == 0, "output": output}).encode("utf-8"))
            return

        elif self.path == "/api/save_character":
            char_id = data.get("charId")
            cfg = data.get("config", {})
            print(f"[SAVE CHARACTER] Updating character '{char_id}' with configs: {cfg}")

            # Update cast.json across projects
            for p in (BASE_DIR / "projects").glob("*/cast.json"):
                try:
                    cast_data = json.loads(p.read_text(encoding="utf-8"))
                    if char_id not in cast_data:
                        cast_data[char_id] = {
                            "skin": cfg.get("skin", "#e6b38a"),
                            "body": cfg.get("body", "boy"),
                            "faceStyle": "roblox",
                            "hair": {
                                "style": cfg.get("hairStyle", "spikyTop"),
                                "color": cfg.get("hairColor", "#1c1e26")
                            },
                            "outfit": {
                                "torso": {
                                    "kind": "cyberHoodie" if cfg.get("headphones") else "plain",
                                    "color": cfg.get("torsoColor", "#202330"),
                                    "trim": "#9b4dff"
                                },
                                "legs": {
                                    "color": cfg.get("legsColor", "#2b2e3a"),
                                    "length": 1,
                                    "shoes": "#6f38c5"
                                }
                            },
                            "headphones": cfg.get("headphones", False)
                        }
                    else:
                        c = cast_data[char_id]
                        c["skin"] = cfg.get("skin", c.get("skin"))
                        c["body"] = cfg.get("body", c.get("body", "boy"))
                        if "hair" in c:
                            c["hair"]["style"] = cfg.get("hairStyle", c["hair"].get("style"))
                            c["hair"]["color"] = cfg.get("hairColor", c["hair"].get("color"))
                        if "headphones" in cfg:
                            c["headphones"] = cfg["headphones"]
                        if "outfit" in c and "torso" in c["outfit"]:
                            c["outfit"]["torso"]["color"] = cfg.get("torsoColor", c["outfit"]["torso"].get("color"))
                        if "outfit" in c and "legs" in c["outfit"]:
                            c["outfit"]["legs"]["color"] = cfg.get("legsColor", c["outfit"]["legs"].get("color"))

                    p.write_text(json.dumps(cast_data, indent=2), encoding="utf-8")
                except Exception as e:
                    print(f"Error updating {p}: {e}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": f"Character '{char_id}' synced and saved to cast.json!"}).encode("utf-8"))
            return

        elif self.path == "/api/create":
            slug = data.get("slug")
            script = data.get("script")

            proj_dir = BASE_DIR / "projects" / slug
            proj_dir.mkdir(parents=True, exist_ok=True)
            (proj_dir / "audio").mkdir(parents=True, exist_ok=True)
            (proj_dir / "script.txt").write_text(script, encoding="utf-8")

            example_dir = BASE_DIR / "projects" / "hype_short_45s"
            if example_dir.exists():
                for f in ["cast.json", "sounds.json", "story.json"]:
                    src_f = example_dir / f
                    dst_f = proj_dir / f
                    if src_f.exists() and not dst_f.exists():
                        dst_f.write_text(src_f.read_text(encoding="utf-8"), encoding="utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": f"Project '{slug}' created successfully!"}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    os.chdir(str(BASE_DIR))
    server = ThreadingHTTPServer(("localhost", PORT), StudioHandler)
    print(f"🚀 RBLX Hype Studio UI running at: http://localhost:{PORT}")
    server.serve_forever()
