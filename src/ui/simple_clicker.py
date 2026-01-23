import customtkinter as ctk
from pynput import mouse


class SimpleClickerTab:
    def __init__(self, parent, clicker, config, hotkey, bg_color, accent_color, secondary_color, text_color):
        self.parent = parent
        self.clicker = clicker
        self.config = config
        self.hotkey = hotkey
        self.bg_color = bg_color
        self.accent_color = accent_color
        self.secondary_color = secondary_color
        self.text_color = text_color

        self.clicker.on_status_change = lambda running: self.parent.after(0, self.update_status)
        self.capture_listener = None
        self.is_capturing = False

        # Liste des widgets a desactiver
        self.controls = []

        # Charger les parametres sauvegardes
        self.saved_settings = self.config.get_simple_clicker_settings()

        self._create_widgets()
        self._load_settings()

    def _create_widgets(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame pour le contenu (scrollable si besoin)
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # Section Intervalle
        self._create_section_label(content_frame, "Intervalle entre clics")
        interval_frame = ctk.CTkFrame(content_frame, fg_color=self.secondary_color, corner_radius=8)
        interval_frame.pack(fill="x", pady=(0, 10))

        interval_inner = ctk.CTkFrame(interval_frame, fg_color="transparent")
        interval_inner.pack(expand=True, pady=10)

        self.interval_entry = ctk.CTkEntry(
            interval_inner,
            width=100,
            placeholder_text="100",
            fg_color=self.bg_color,
            text_color=self.text_color,
            border_color=self.accent_color
        )
        self.interval_entry.pack(side="left", padx=(0, 10))
        self.interval_entry.insert(0, "100")
        self.interval_entry.bind("<FocusOut>", lambda e: self._save_settings())
        self.interval_entry.bind("<Return>", lambda e: self._save_settings())
        self.controls.append(self.interval_entry)

        ctk.CTkLabel(
            interval_inner,
            text="millisecondes",
            text_color=self.text_color
        ).pack(side="left")

        # Section Type de clic
        self._create_section_label(content_frame, "Type de clic")
        click_type_frame = ctk.CTkFrame(content_frame, fg_color=self.secondary_color, corner_radius=8)
        click_type_frame.pack(fill="x", pady=(0, 10))

        click_type_inner = ctk.CTkFrame(click_type_frame, fg_color="transparent")
        click_type_inner.pack(expand=True, pady=10)

        self.click_type_var = ctk.StringVar(value="left")
        self.click_type_var.trace_add("write", lambda *args: self._save_settings())
        self.radio_buttons = []
        for text, value in [("Gauche", "left"), ("Droit", "right"), ("Molette", "middle")]:
            rb = ctk.CTkRadioButton(
                click_type_inner,
                text=text,
                variable=self.click_type_var,
                value=value,
                fg_color=self.accent_color,
                hover_color="#c73e54",
                text_color=self.text_color,
                width=20
            )
            rb.pack(side="left", padx=12)
            self.radio_buttons.append(rb)
            self.controls.append(rb)

        # Section Repetitions
        self._create_section_label(content_frame, "Repetitions")
        rep_frame = ctk.CTkFrame(content_frame, fg_color=self.secondary_color, corner_radius=8)
        rep_frame.pack(fill="x", pady=(0, 10))

        rep_inner = ctk.CTkFrame(rep_frame, fg_color="transparent")
        rep_inner.pack(expand=True, pady=10)

        self.infinite_var = ctk.BooleanVar(value=True)
        self.infinite_checkbox = ctk.CTkCheckBox(
            rep_inner,
            text="Infini",
            variable=self.infinite_var,
            fg_color=self.accent_color,
            hover_color="#c73e54",
            text_color=self.text_color,
            command=self._on_infinite_change
        )
        self.infinite_checkbox.pack(side="left", padx=(0, 10))
        self.controls.append(self.infinite_checkbox)

        ctk.CTkLabel(rep_inner, text="ou", text_color=self.text_color).pack(side="left", padx=5)

        self.count_entry = ctk.CTkEntry(
            rep_inner,
            width=80,
            placeholder_text="10",
            fg_color=self.bg_color,
            text_color=self.text_color,
            border_color=self.accent_color,
            state="disabled"
        )
        self.count_entry.pack(side="left", padx=5)
        self.count_entry.insert(0, "10")
        self.count_entry.bind("<FocusOut>", lambda e: self._save_settings())
        self.count_entry.bind("<Return>", lambda e: self._save_settings())
        self.controls.append(self.count_entry)

        ctk.CTkLabel(rep_inner, text="clics", text_color=self.text_color).pack(side="left", padx=(5, 0))

        # Section Position
        self._create_section_label(content_frame, "Position")
        pos_frame = ctk.CTkFrame(content_frame, fg_color=self.secondary_color, corner_radius=8)
        pos_frame.pack(fill="x", pady=(0, 5))

        pos_inner = ctk.CTkFrame(pos_frame, fg_color="transparent")
        pos_inner.pack(expand=True, pady=10)

        self.use_cursor_var = ctk.BooleanVar(value=True)
        self.cursor_checkbox = ctk.CTkCheckBox(
            pos_inner,
            text="Suivre le curseur",
            variable=self.use_cursor_var,
            fg_color=self.accent_color,
            hover_color="#c73e54",
            text_color=self.text_color,
            command=self._on_cursor_change
        )
        self.cursor_checkbox.pack()
        self.controls.append(self.cursor_checkbox)

        # Frame pour position fixe avec bouton capture
        pos_fixed_frame = ctk.CTkFrame(content_frame, fg_color=self.secondary_color, corner_radius=8)
        pos_fixed_frame.pack(fill="x", pady=(0, 5))

        pos_fixed_inner = ctk.CTkFrame(pos_fixed_frame, fg_color="transparent")
        pos_fixed_inner.pack(expand=True, pady=10)

        self.capture_button = ctk.CTkButton(
            pos_fixed_inner,
            text="Capturer position",
            font=ctk.CTkFont(size=12),
            fg_color="#0f3460",
            hover_color="#1a4a7a",
            width=130,
            command=self._start_capture,
            state="disabled"
        )
        self.capture_button.pack(side="left", padx=(0, 15))
        self.controls.append(self.capture_button)

        ctk.CTkLabel(pos_fixed_inner, text="X:", text_color=self.text_color).pack(side="left")
        self.x_entry = ctk.CTkEntry(
            pos_fixed_inner,
            width=55,
            fg_color=self.bg_color,
            text_color=self.text_color,
            border_color=self.accent_color,
            state="disabled"
        )
        self.x_entry.pack(side="left", padx=(5, 10))
        self.x_entry.insert(0, "0")
        self.x_entry.bind("<FocusOut>", lambda e: self._save_settings())
        self.x_entry.bind("<Return>", lambda e: self._save_settings())
        self.controls.append(self.x_entry)

        ctk.CTkLabel(pos_fixed_inner, text="Y:", text_color=self.text_color).pack(side="left")
        self.y_entry = ctk.CTkEntry(
            pos_fixed_inner,
            width=55,
            fg_color=self.bg_color,
            text_color=self.text_color,
            border_color=self.accent_color,
            state="disabled"
        )
        self.y_entry.pack(side="left", padx=5)
        self.y_entry.insert(0, "0")
        self.y_entry.bind("<FocusOut>", lambda e: self._save_settings())
        self.y_entry.bind("<Return>", lambda e: self._save_settings())
        self.controls.append(self.y_entry)

        # Bouton principal (dans main_frame, en bas)
        self.start_button = ctk.CTkButton(
            main_frame,
            text=f"DEMARRER ({self.hotkey.upper()})",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.accent_color,
            hover_color="#c73e54",
            height=50,
            corner_radius=8,
            command=self.toggle_clicker
        )
        self.start_button.pack(side="bottom", fill="x", pady=(10, 0))

    def _create_section_label(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.text_color,
            anchor="w"
        ).pack(fill="x", pady=(5, 5))

    def _toggle_count_entry(self):
        if self.infinite_var.get():
            self.count_entry.configure(state="disabled")
        else:
            self.count_entry.configure(state="normal")

    def _on_infinite_change(self):
        """Callback quand la case infini change"""
        self._toggle_count_entry()
        self._save_settings()

    def _toggle_position_entries(self):
        state = "disabled" if self.use_cursor_var.get() else "normal"
        self.x_entry.configure(state=state)
        self.y_entry.configure(state=state)
        self.capture_button.configure(state=state)

    def _on_cursor_change(self):
        """Callback quand la case suivre curseur change"""
        self._toggle_position_entries()
        self._save_settings()

    def _start_capture(self):
        if self.is_capturing:
            return
        self.is_capturing = True
        self.capture_button.configure(text="Cliquez...", fg_color="#e94560")

        def on_click(x, y, button, pressed):
            if pressed:
                self.parent.after(0, lambda: self._on_position_captured(int(x), int(y)))
                return False

        self.capture_listener = mouse.Listener(on_click=on_click)
        self.capture_listener.start()

    def _on_position_captured(self, x, y):
        self.is_capturing = False
        self.capture_button.configure(text="Capturer position", fg_color="#0f3460")

        self.x_entry.configure(state="normal")
        self.x_entry.delete(0, "end")
        self.x_entry.insert(0, str(x))

        self.y_entry.configure(state="normal")
        self.y_entry.delete(0, "end")
        self.y_entry.insert(0, str(y))

        if self.use_cursor_var.get():
            self.x_entry.configure(state="disabled")
            self.y_entry.configure(state="disabled")

        # Sauvegarder la position capturee
        self._save_settings()

    def toggle_clicker(self):
        if self.clicker.is_running():
            self.clicker.stop()
        else:
            self._apply_settings()
            self.clicker.start()
        self.update_status()

    def _load_settings(self):
        """Charge les parametres sauvegardes"""
        settings = self.saved_settings

        # Intervalle
        self.interval_entry.delete(0, "end")
        self.interval_entry.insert(0, str(settings.get("interval", 100)))

        # Type de clic
        self.click_type_var.set(settings.get("click_type", "left"))

        # Repetitions
        self.infinite_var.set(settings.get("infinite", True))
        self.count_entry.configure(state="normal")
        self.count_entry.delete(0, "end")
        self.count_entry.insert(0, str(settings.get("click_count", 10)))
        self._toggle_count_entry()

        # Position
        self.use_cursor_var.set(settings.get("follow_cursor", True))
        self.x_entry.configure(state="normal")
        self.x_entry.delete(0, "end")
        self.x_entry.insert(0, str(settings.get("fixed_x", 0)))
        self.y_entry.configure(state="normal")
        self.y_entry.delete(0, "end")
        self.y_entry.insert(0, str(settings.get("fixed_y", 0)))
        self._toggle_position_entries()

    def _save_settings(self):
        """Sauvegarde les parametres"""
        try:
            interval = int(self.interval_entry.get())
        except ValueError:
            interval = 100

        try:
            click_count = int(self.count_entry.get())
        except ValueError:
            click_count = 10

        try:
            fixed_x = int(self.x_entry.get())
            fixed_y = int(self.y_entry.get())
        except ValueError:
            fixed_x, fixed_y = 0, 0

        settings = {
            "interval": interval,
            "click_type": self.click_type_var.get(),
            "infinite": self.infinite_var.get(),
            "click_count": click_count,
            "follow_cursor": self.use_cursor_var.get(),
            "fixed_x": fixed_x,
            "fixed_y": fixed_y
        }
        self.config.set_simple_clicker_settings(settings)

    def _apply_settings(self):
        try:
            interval = int(self.interval_entry.get())
        except ValueError:
            interval = 100
        self.clicker.set_interval(interval)

        self.clicker.set_click_type(self.click_type_var.get())
        self.clicker.set_infinite(self.infinite_var.get())

        if not self.infinite_var.get():
            try:
                count = int(self.count_entry.get())
            except ValueError:
                count = 10
            self.clicker.set_click_count(count)

        use_cursor = self.use_cursor_var.get()
        if not use_cursor:
            try:
                x = int(self.x_entry.get())
                y = int(self.y_entry.get())
            except ValueError:
                x, y = 0, 0
            self.clicker.set_fixed_position(True, x, y)
        else:
            self.clicker.set_fixed_position(False)

        # Sauvegarder les parametres
        self._save_settings()

    def set_hotkey(self, hotkey):
        self.hotkey = hotkey
        self.update_status()

    def update_status(self):
        key = self.hotkey.upper()
        if self.clicker.is_running():
            self.start_button.configure(text=f"ARRETER ({key})", fg_color="#c73e54")
        else:
            self.start_button.configure(text=f"DEMARRER ({key})", fg_color=self.accent_color)

    def set_locked(self, locked, keep_button=False):
        """Verrouille ou deverrouille tous les controles"""
        state = "disabled" if locked else "normal"
        for control in self.controls:
            control.configure(state=state)

        if locked and not keep_button:
            self.start_button.configure(state="disabled")
        elif not locked:
            self.start_button.configure(state="normal")
            # Restaurer les etats speciaux
            self._toggle_count_entry()
            self._toggle_position_entries()
