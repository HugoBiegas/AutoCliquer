import json
import os
import sys


def get_config_dir():
    """Retourne le dossier de config (a cote de l'exe ou dans le dossier courant)"""
    if getattr(sys, 'frozen', False):
        # Mode exe
        return os.path.dirname(sys.executable)
    else:
        # Mode script
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Config:
    def __init__(self):
        self.config_dir = get_config_dir()
        self.config_file = os.path.join(self.config_dir, "autoclicker_config.json")
        self.autosave_file = os.path.join(self.config_dir, "autoclicker_autosave.json")

        self.default_config = {
            "hotkeys": {
                "clicker": "f6",
                "record": "f7",
                "playback": "f8"
            }
        }

        self.data = self.load()

    def load(self):
        """Charge la config depuis le fichier"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return self.default_config.copy()

    def save(self):
        """Sauvegarde la config dans le fichier"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def get_hotkeys(self):
        """Retourne les raccourcis"""
        return self.data.get("hotkeys", self.default_config["hotkeys"]).copy()

    def set_hotkeys(self, hotkeys):
        """Definit les raccourcis et sauvegarde"""
        self.data["hotkeys"] = hotkeys
        self.save()

    def save_autosave_script(self, points, delay):
        """Sauvegarde automatique du script"""
        if not points:
            return
        try:
            data = {
                "delay_ms": delay,
                "points": points
            }
            with open(self.autosave_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def load_autosave_script(self):
        """Charge le script sauvegarde automatiquement"""
        try:
            if os.path.exists(self.autosave_file):
                with open(self.autosave_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return {
                    "points": data.get("points", []),
                    "delay": data.get("delay_ms", 1000)
                }
        except (json.JSONDecodeError, IOError):
            pass
        return None

    def delete_autosave_script(self):
        """Supprime le script sauvegarde automatiquement"""
        try:
            if os.path.exists(self.autosave_file):
                os.remove(self.autosave_file)
        except IOError:
            pass
