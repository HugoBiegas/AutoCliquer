import customtkinter as ctk
import os
import sys
from .simple_clicker import SimpleClickerTab
from .script_recorder import ScriptRecorderTab
from ..core.clicker import Clicker, ScriptPlayer
from ..core.recorder import Recorder
from ..core.hotkeys import HotkeyManager
from ..utils.file_manager import FileManager
from ..utils.config import Config


def get_icon_path():
    """Retourne le chemin vers l'icone"""
    if getattr(sys, 'frozen', False):
        # Executable PyInstaller
        base_path = sys._MEIPASS
    else:
        # Mode developpement
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, "assets", "icon.ico")


class App(ctk.CTk):
    # Couleurs du theme sombre
    BG_COLOR = "#1a1a2e"
    CARD_COLOR = "#16213e"
    ACCENT_COLOR = "#e94560"
    SECONDARY_COLOR = "#0f3460"
    TEXT_COLOR = "#ffffff"
    TEXT_SECONDARY = "#a0a0a0"
    DISABLED_COLOR = "#0d0d1a"

    def __init__(self):
        super().__init__()

        # Configuration fenetre (taille fixe)
        self.title("Auto-Clicker")
        self.geometry("450x640")
        self.resizable(False, False)
        self.configure(fg_color=self.BG_COLOR)

        # Definir l'icone
        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # Initialisation des composants
        self.config = Config()
        self.clicker = Clicker()
        self.script_player = ScriptPlayer()
        self.recorder = Recorder()
        self.hotkey_manager = HotkeyManager()
        self.file_manager = FileManager()

        # Charger les raccourcis depuis la config
        self.hotkeys = self.config.get_hotkeys()

        # Overlay pour griser la fenetre
        self.overlay = None
        self.settings_window = None

        # Creation de l'interface
        self._create_header()
        self._create_tabs()
        self._setup_hotkeys()

        # Charger le script sauvegarde automatiquement
        self._load_autosave()

        # Gestion fermeture
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_header(self):
        header = ctk.CTkFrame(self, fg_color=self.CARD_COLOR, corner_radius=0, height=60)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="Auto-Clicker",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.TEXT_COLOR
        )
        title.pack(side="left", padx=20, pady=15)

        # Bouton Settings (roue crantee)
        self.settings_btn = ctk.CTkButton(
            header,
            text="\u2699",
            font=ctk.CTkFont(size=22),
            fg_color="transparent",
            hover_color=self.SECONDARY_COLOR,
            text_color=self.TEXT_COLOR,
            width=40,
            height=40,
            command=self._open_settings
        )
        self.settings_btn.pack(side="right", padx=15, pady=10)

    def _create_tabs(self):
        # Conteneur des onglets
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=self.CARD_COLOR,
            segmented_button_fg_color=self.SECONDARY_COLOR,
            segmented_button_selected_color=self.ACCENT_COLOR,
            segmented_button_selected_hover_color="#c73e54",
            segmented_button_unselected_color=self.SECONDARY_COLOR,
            segmented_button_unselected_hover_color="#1a4a7a",
            text_color=self.TEXT_COLOR
        )
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)

        # Onglet Clic Simple
        tab1 = self.tabview.add("Clic Simple")
        self.simple_tab = SimpleClickerTab(
            tab1,
            self.clicker,
            self.config,
            hotkey=self.hotkeys["clicker"],
            bg_color=self.CARD_COLOR,
            accent_color=self.ACCENT_COLOR,
            secondary_color=self.SECONDARY_COLOR,
            text_color=self.TEXT_COLOR
        )

        # Onglet Script/Macro
        tab2 = self.tabview.add("Script/Macro")
        self.script_tab = ScriptRecorderTab(
            tab2,
            self.recorder,
            self.script_player,
            self.file_manager,
            self.config,
            record_hotkey=self.hotkeys["record"],
            playback_hotkey=self.hotkeys["playback"],
            bg_color=self.CARD_COLOR,
            accent_color=self.ACCENT_COLOR,
            secondary_color=self.SECONDARY_COLOR,
            text_color=self.TEXT_COLOR
        )

        # Configurer les callbacks pour le verrouillage
        self.clicker.on_status_change = lambda running: self.after(0, lambda: self._on_clicker_status(running))
        self.recorder.on_status_change = lambda recording: self.after(0, lambda: self._on_recorder_status(recording))
        self.script_player.on_status_change = lambda running: self.after(0, lambda: self._on_player_status(running))

    def _setup_hotkeys(self):
        self.hotkey_manager.register_custom(
            keys=self.hotkeys,
            on_clicker=self._on_f6,
            on_record=self._on_f7,
            on_playback=self._on_f8,
            on_escape=self._on_escape
        )

    def _update_button_texts(self):
        self.simple_tab.set_hotkey(self.hotkeys["clicker"])
        self.script_tab.set_hotkeys(self.hotkeys["record"], self.hotkeys["playback"])

    def _on_clicker_status(self, running):
        """Callback quand le clicker demarre/arrete"""
        self.simple_tab.update_status()
        if running:
            # Verrouiller tout sauf le bouton d'arret
            self.simple_tab.set_locked(True, keep_button=True)
            self.script_tab.set_locked(True)
            self.settings_btn.configure(state="disabled")
            self.tabview.configure(state="disabled")
        else:
            # Deverrouiller tout
            self.simple_tab.set_locked(False)
            self.script_tab.set_locked(False)
            self.settings_btn.configure(state="normal")
            self.tabview.configure(state="normal")

    def _on_recorder_status(self, recording):
        """Callback quand l'enregistrement demarre/arrete"""
        self.script_tab.update_status()
        if recording:
            # Verrouiller tout sauf le bouton d'arret
            self.simple_tab.set_locked(True)
            self.script_tab.set_locked(True, active_button="record")
            self.settings_btn.configure(state="disabled")
            self.tabview.configure(state="disabled")
        else:
            # Deverrouiller tout
            self.simple_tab.set_locked(False)
            self.script_tab.set_locked(False)
            self.settings_btn.configure(state="normal")
            self.tabview.configure(state="normal")

    def _on_player_status(self, running):
        """Callback quand la lecture demarre/arrete"""
        self.script_tab.update_status()
        if running:
            # Verrouiller tout sauf le bouton d'arret
            self.simple_tab.set_locked(True)
            self.script_tab.set_locked(True, active_button="play")
            self.settings_btn.configure(state="disabled")
            self.tabview.configure(state="disabled")
        else:
            # Deverrouiller tout
            self.simple_tab.set_locked(False)
            self.script_tab.set_locked(False)
            self.settings_btn.configure(state="normal")
            self.tabview.configure(state="normal")

    def _load_autosave(self):
        """Charge le script sauvegarde automatiquement"""
        data = self.config.load_autosave_script()
        if data and data["points"]:
            self.recorder.points = data["points"]
            self.script_tab._refresh_points_display(data["points"])
            self.script_tab.delay_entry.delete(0, "end")
            self.script_tab.delay_entry.insert(0, str(data["delay"]))

    def _on_f6(self):
        # Autoriser seulement si clicker actif (pour arreter) ou aucune action en cours
        if self.clicker.is_running() or not (self.recorder.is_recording() or self.script_player.is_running()):
            self.after(0, self.simple_tab.toggle_clicker)

    def _on_f7(self):
        # Autoriser seulement si enregistrement actif (pour arreter) ou aucune action en cours
        if self.recorder.is_recording() or not (self.clicker.is_running() or self.script_player.is_running()):
            self.after(0, self.script_tab.toggle_recording)

    def _on_f8(self):
        # Autoriser seulement si lecture active (pour arreter) ou aucune action en cours
        if self.script_player.is_running() or not (self.clicker.is_running() or self.recorder.is_recording()):
            self.after(0, self.script_tab.toggle_playback)

    def _on_escape(self):
        self.after(0, self._stop_all)

    def _stop_all(self):
        self.clicker.stop()
        self.recorder.stop()
        self.script_player.stop()
        # Deverrouiller tout
        self.simple_tab.set_locked(False)
        self.script_tab.set_locked(False)
        self.settings_btn.configure(state="normal")
        self.tabview.configure(state="normal")
        self.simple_tab.update_status()
        self.script_tab.update_status()

    def _on_close(self):
        self._stop_all()
        self.hotkey_manager.unregister()
        self.destroy()

    def _show_overlay(self):
        """Affiche un overlay grise sur la fenetre principale"""
        if self.overlay:
            return
        self.overlay = ctk.CTkFrame(
            self,
            fg_color="#000000",
            corner_radius=0
        )
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.configure(fg_color=("gray50", "gray20"))
        # Rendre semi-transparent en utilisant une couleur sombre
        self.overlay.bind("<Button-1>", lambda e: self._focus_settings())

    def _hide_overlay(self):
        """Cache l'overlay"""
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None

    def _focus_settings(self):
        """Met la fenetre des parametres au premier plan"""
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            self.settings_window.focus_force()

    def _open_settings(self):
        self._show_overlay()
        self.settings_window = SettingsWindow(
            self,
            self.hotkeys,
            self._apply_new_hotkeys,
            self._on_settings_close
        )

    def _on_settings_close(self):
        """Callback quand les parametres se ferment"""
        self._hide_overlay()
        self.settings_window = None

    def _apply_new_hotkeys(self, new_hotkeys):
        self.hotkeys = new_hotkeys
        self.config.set_hotkeys(new_hotkeys)
        self.hotkey_manager.unregister()
        self.hotkey_manager.register_custom(
            keys=self.hotkeys,
            on_clicker=self._on_f6,
            on_record=self._on_f7,
            on_playback=self._on_f8,
            on_escape=self._on_escape
        )
        self._update_button_texts()


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, current_hotkeys, on_save, on_close):
        super().__init__(parent)
        self.parent_app = parent
        self.on_save = on_save
        self.on_close_callback = on_close
        self.current_hotkeys = current_hotkeys.copy()
        self.listening_button = None

        self.title("Parametres")
        self.resizable(False, False)
        self.configure(fg_color=App.BG_COLOR)

        # Centrer sur la fenetre parente
        self.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        win_w, win_h = 350, 280
        x = parent_x + (parent_w - win_w) // 2
        y = parent_y + (parent_h - win_h) // 2
        self.geometry(f"{win_w}x{win_h}+{x}+{y}")

        # Forcer au premier plan
        self.transient(parent)
        self.grab_set()
        self.focus_force()

        # Gestion fermeture
        self.protocol("WM_DELETE_WINDOW", self._close)

        self._create_widgets()

    def _create_widgets(self):
        # Titre
        ctk.CTkLabel(
            self,
            text="Raccourcis clavier",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=App.TEXT_COLOR
        ).pack(pady=(20, 20))

        # Frame pour les raccourcis
        frame = ctk.CTkFrame(self, fg_color=App.CARD_COLOR, corner_radius=10)
        frame.pack(fill="x", padx=20, pady=(0, 20))

        # Clic simple
        self._create_hotkey_row(frame, "Clic simple:", "clicker")
        # Enregistrement
        self._create_hotkey_row(frame, "Enregistrer:", "record")
        # Lecture script
        self._create_hotkey_row(frame, "Lancer script:", "playback")

        # Boutons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20)

        ctk.CTkButton(
            btn_frame,
            text="Annuler",
            fg_color=App.SECONDARY_COLOR,
            hover_color="#1a4a7a",
            width=100,
            command=self._close
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_frame,
            text="Sauvegarder",
            fg_color=App.ACCENT_COLOR,
            hover_color="#c73e54",
            width=100,
            command=self._save
        ).pack(side="right")

    def _create_hotkey_row(self, parent, label, key):
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            row_frame,
            text=label,
            text_color=App.TEXT_COLOR,
            width=120,
            anchor="w"
        ).pack(side="left")

        btn = ctk.CTkButton(
            row_frame,
            text=self.current_hotkeys[key].upper(),
            fg_color=App.BG_COLOR,
            hover_color=App.SECONDARY_COLOR,
            text_color=App.TEXT_COLOR,
            border_color=App.ACCENT_COLOR,
            border_width=2,
            width=100,
            command=lambda k=key: self._start_listening(k)
        )
        btn.pack(side="right")
        setattr(self, f"btn_{key}", btn)

    def _start_listening(self, key):
        if self.listening_button:
            return

        self.listening_button = key
        btn = getattr(self, f"btn_{key}")
        btn.configure(text="Appuyez...", fg_color=App.ACCENT_COLOR)

        # Ecouter le clavier
        import keyboard
        keyboard.unhook_all()

        def on_key(event):
            self.after(0, lambda: self._on_key_captured(key, event.name))
            return False

        keyboard.on_press(on_key)

    def _on_key_captured(self, key, key_name):
        import keyboard
        keyboard.unhook_all()

        self.current_hotkeys[key] = key_name
        btn = getattr(self, f"btn_{key}")
        btn.configure(text=key_name.upper(), fg_color=App.BG_COLOR)
        self.listening_button = None

        # Re-enregistrer les hotkeys de l'app principale avec les touches actuelles
        self.parent_app.hotkey_manager.register_custom(
            keys=self.parent_app.hotkeys,
            on_clicker=self.parent_app._on_f6,
            on_record=self.parent_app._on_f7,
            on_playback=self.parent_app._on_f8,
            on_escape=self.parent_app._on_escape
        )

    def _close(self):
        self.on_close_callback()
        self.destroy()

    def _save(self):
        self.on_save(self.current_hotkeys)
        self._close()
