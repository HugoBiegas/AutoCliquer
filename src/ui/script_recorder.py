import customtkinter as ctk
from tkinter import filedialog


class ScriptRecorderTab:
    def __init__(self, parent, recorder, script_player, file_manager, config,
                 record_hotkey, playback_hotkey,
                 bg_color, accent_color, secondary_color, text_color):
        self.parent = parent
        self.recorder = recorder
        self.script_player = script_player
        self.file_manager = file_manager
        self.config = config
        self.record_hotkey = record_hotkey
        self.playback_hotkey = playback_hotkey
        self.bg_color = bg_color
        self.accent_color = accent_color
        self.secondary_color = secondary_color
        self.text_color = text_color

        self.recorder.on_point_added = lambda p: self.parent.after(0, lambda: self._add_point_to_list(p))
        self.recorder.on_status_change = lambda r: self.parent.after(0, self.update_status)
        self.script_player.on_status_change = lambda r: self.parent.after(0, self.update_status)

        self._create_widgets()

    def _create_widgets(self):
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Boutons d'enregistrement (centres)
        rec_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        rec_frame.pack(fill="x", pady=(0, 10))

        rec_inner = ctk.CTkFrame(rec_frame, fg_color="transparent")
        rec_inner.pack(expand=True)

        self.record_button = ctk.CTkButton(
            rec_inner,
            text=f"Enregistrer ({self.record_hotkey.upper()})",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#c73e54",
            hover_color="#a82e44",
            width=150,
            command=self.toggle_recording
        )
        self.record_button.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            rec_inner,
            text="Effacer",
            font=ctk.CTkFont(size=14),
            fg_color=self.secondary_color,
            hover_color="#1a4a7a",
            width=100,
            command=self._clear_points
        ).pack(side="left")

        # Liste des points
        self._create_section_label(main_frame, "Points enregistres")
        list_frame = ctk.CTkFrame(main_frame, fg_color=self.secondary_color, corner_radius=8)
        list_frame.pack(fill="both", expand=True, pady=(0, 15))

        self.points_textbox = ctk.CTkTextbox(
            list_frame,
            fg_color=self.bg_color,
            text_color=self.text_color,
            font=ctk.CTkFont(family="Consolas", size=12),
            height=120
        )
        self.points_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.points_textbox.configure(state="disabled")

        # Delai
        self._create_section_label(main_frame, "Delai entre clics")
        delay_frame = ctk.CTkFrame(main_frame, fg_color=self.secondary_color, corner_radius=8)
        delay_frame.pack(fill="x", pady=(0, 15))

        delay_inner = ctk.CTkFrame(delay_frame, fg_color="transparent")
        delay_inner.pack(expand=True, pady=10)

        self.delay_entry = ctk.CTkEntry(
            delay_inner,
            width=100,
            placeholder_text="1000",
            fg_color=self.bg_color,
            text_color=self.text_color,
            border_color=self.accent_color
        )
        self.delay_entry.pack(side="left", padx=(0, 10))
        self.delay_entry.insert(0, "1000")

        ctk.CTkLabel(
            delay_inner,
            text="millisecondes",
            text_color=self.text_color
        ).pack(side="left")

        # Repetitions
        rep_frame = ctk.CTkFrame(main_frame, fg_color=self.secondary_color, corner_radius=8)
        rep_frame.pack(fill="x", pady=(0, 15))

        rep_inner = ctk.CTkFrame(rep_frame, fg_color="transparent")
        rep_inner.pack(expand=True, pady=10)

        self.infinite_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            rep_inner,
            text="Boucle infinie",
            variable=self.infinite_var,
            fg_color=self.accent_color,
            hover_color="#c73e54",
            text_color=self.text_color,
            command=self._toggle_loop_entry
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(rep_inner, text="ou", text_color=self.text_color).pack(side="left", padx=5)

        self.loop_entry = ctk.CTkEntry(
            rep_inner,
            width=80,
            placeholder_text="1",
            fg_color=self.bg_color,
            text_color=self.text_color,
            border_color=self.accent_color,
            state="disabled"
        )
        self.loop_entry.pack(side="left", padx=5)
        self.loop_entry.insert(0, "1")

        ctk.CTkLabel(rep_inner, text="boucles", text_color=self.text_color).pack(side="left", padx=(5, 0))

        # Boutons sauvegarde/chargement (centres)
        file_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        file_frame.pack(fill="x", pady=(0, 10))

        file_inner = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_inner.pack(expand=True)

        ctk.CTkButton(
            file_inner,
            text="Sauvegarder",
            font=ctk.CTkFont(size=14),
            fg_color=self.secondary_color,
            hover_color="#1a4a7a",
            width=120,
            command=self._save_script
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            file_inner,
            text="Charger",
            font=ctk.CTkFont(size=14),
            fg_color=self.secondary_color,
            hover_color="#1a4a7a",
            width=120,
            command=self._load_script
        ).pack(side="left")

        # Bouton principal
        self.play_button = ctk.CTkButton(
            main_frame,
            text=f"LANCER ({self.playback_hotkey.upper()})",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.accent_color,
            hover_color="#c73e54",
            height=50,
            command=self.toggle_playback
        )
        self.play_button.pack(fill="x", pady=(10, 0))

    def _create_section_label(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.text_color,
            anchor="w"
        ).pack(fill="x", pady=(5, 5))

    def _toggle_loop_entry(self):
        if self.infinite_var.get():
            self.loop_entry.configure(state="disabled")
        else:
            self.loop_entry.configure(state="normal")

    def _add_point_to_list(self, point):
        self.points_textbox.configure(state="normal")
        count = len(self.recorder.get_points())
        button = point.get("button", "left")
        button_display = {"left": "Gauche", "right": "Droit", "middle": "Molette"}.get(button, "Gauche")
        self.points_textbox.insert("end", f"{count}. X: {point['x']}  Y: {point['y']}  [{button_display}]\n")
        self.points_textbox.configure(state="disabled")
        self.points_textbox.see("end")

    def _clear_points(self):
        self.recorder.clear()
        self.points_textbox.configure(state="normal")
        self.points_textbox.delete("1.0", "end")
        self.points_textbox.configure(state="disabled")
        # Supprimer la sauvegarde automatique
        self.config.delete_autosave_script()

    def _refresh_points_display(self, points):
        self.points_textbox.configure(state="normal")
        self.points_textbox.delete("1.0", "end")
        for i, point in enumerate(points, 1):
            button = point.get("button", "left")
            button_display = {"left": "Gauche", "right": "Droit", "middle": "Molette"}.get(button, "Gauche")
            self.points_textbox.insert("end", f"{i}. X: {point['x']}  Y: {point['y']}  [{button_display}]\n")
        self.points_textbox.configure(state="disabled")

    def toggle_recording(self):
        if self.recorder.is_recording():
            self.recorder.stop()
            # Sauvegarde automatique quand on arrete l'enregistrement
            points = self.recorder.get_points()
            if points:
                try:
                    delay = int(self.delay_entry.get())
                except ValueError:
                    delay = 1000
                self.config.save_autosave_script(points, delay)
        else:
            self.recorder.start()
        self.update_status()

    def toggle_playback(self):
        if self.script_player.is_running():
            self.script_player.stop()
        else:
            self._apply_settings()
            points = self.recorder.get_points()
            if points:
                self.script_player.set_points(points)
                self.script_player.start()
        self.update_status()

    def _apply_settings(self):
        try:
            delay = int(self.delay_entry.get())
        except ValueError:
            delay = 1000
        self.script_player.set_delay(delay)

        self.script_player.set_infinite(self.infinite_var.get())

        if not self.infinite_var.get():
            try:
                loops = int(self.loop_entry.get())
            except ValueError:
                loops = 1
            self.script_player.set_loop_count(loops)

    def _save_script(self):
        points = self.recorder.get_points()
        if not points:
            return

        try:
            delay = int(self.delay_entry.get())
        except ValueError:
            delay = 1000

        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialdir="scripts"
        )
        if filepath:
            self.file_manager.save_script(points, delay, filepath)

    def _load_script(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            initialdir="scripts"
        )
        if filepath:
            try:
                data = self.file_manager.load_script(filepath)
                self.recorder.clear()
                self.recorder.points = data["points"]
                self._refresh_points_display(data["points"])
                self.delay_entry.delete(0, "end")
                self.delay_entry.insert(0, str(data["delay"]))
            except (IOError, KeyError):
                pass

    def set_hotkeys(self, record_hotkey, playback_hotkey):
        self.record_hotkey = record_hotkey
        self.playback_hotkey = playback_hotkey
        self.update_status()

    def update_status(self):
        rec_key = self.record_hotkey.upper()
        play_key = self.playback_hotkey.upper()
        if self.recorder.is_recording():
            self.record_button.configure(text=f"Arreter ({rec_key})", fg_color="#a82e44")
            self.play_button.configure(state="disabled")
        elif self.script_player.is_running():
            self.play_button.configure(text=f"ARRETER ({play_key})", fg_color="#c73e54")
            self.record_button.configure(state="disabled")
        else:
            self.record_button.configure(text=f"Enregistrer ({rec_key})", fg_color="#c73e54")
            self.record_button.configure(state="normal")
            self.play_button.configure(text=f"LANCER ({play_key})", fg_color=self.accent_color)
            self.play_button.configure(state="normal")
