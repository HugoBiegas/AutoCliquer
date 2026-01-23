import json
import os


def get_config_dir():
    """Retourne le dossier de config dans AppData (Windows)"""
    # Utiliser AppData/Roaming sur Windows
    appdata = os.environ.get("APPDATA")
    if appdata:
        config_dir = os.path.join(appdata, "AutoClicker")
    else:
        # Fallback: dossier home de l'utilisateur
        config_dir = os.path.join(os.path.expanduser("~"), ".autoclicker")

    # Creer le dossier s'il n'existe pas
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    return config_dir


class Config:
    def __init__(self):
        self.config_dir = get_config_dir()
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.autosave_file = os.path.join(self.config_dir, "autosave.json")

        self.default_config = {
            "hotkeys": {
                "clicker": "f6",
                "record": "f7",
                "playback": "f8"
            },
            "simple_clicker": {
                "interval": 100,
                "click_type": "left",
                "infinite": True,
                "click_count": 10,
                "follow_cursor": True,
                "fixed_x": 0,
                "fixed_y": 0
            },
            "macro": {
                "delay": 1000,
                "infinite": True,
                "loop_count": 1
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

    def get_simple_clicker_settings(self):
        """Retourne les parametres du clic simple"""
        default = self.default_config["simple_clicker"]
        return self.data.get("simple_clicker", default).copy()

    def set_simple_clicker_settings(self, settings):
        """Definit les parametres du clic simple et sauvegarde"""
        self.data["simple_clicker"] = settings
        self.save()

    def get_macro_settings(self):
        """Retourne les parametres macro"""
        default = self.default_config["macro"]
        return self.data.get("macro", default).copy()

    def set_macro_settings(self, settings):
        """Definit les parametres macro et sauvegarde"""
        self.data["macro"] = settings
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
