import json
import os
from datetime import datetime
from .config import get_config_dir


class FileManager:
    def __init__(self):
        # Utiliser le dossier AppData pour les scripts
        config_dir = get_config_dir()
        self.scripts_dir = os.path.join(config_dir, "scripts")
        os.makedirs(self.scripts_dir, exist_ok=True)

    def save_script(self, points: list, delay: int, filename: str = None) -> str:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"script_{timestamp}.json"

        if not filename.endswith(".json"):
            filename += ".json"

        filepath = os.path.join(self.scripts_dir, filename)

        data = {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "delay_ms": delay,
            "points": points
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filepath

    def load_script(self, filepath: str) -> dict:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "points": data.get("points", []),
            "delay": data.get("delay_ms", 1000)
        }

    def list_scripts(self) -> list:
        scripts = []
        for filename in os.listdir(self.scripts_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.scripts_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    scripts.append({
                        "filename": filename,
                        "filepath": filepath,
                        "points_count": len(data.get("points", [])),
                        "created": data.get("created", "")
                    })
                except (json.JSONDecodeError, IOError):
                    continue
        return sorted(scripts, key=lambda x: x["created"], reverse=True)

    def delete_script(self, filepath: str) -> bool:
        try:
            os.remove(filepath)
            return True
        except OSError:
            return False
