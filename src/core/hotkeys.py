import keyboard


class HotkeyManager:
    def __init__(self):
        self.callbacks = {}
        self.registered = False

    def register(self, on_f6=None, on_f7=None, on_f8=None, on_escape=None):
        if self.registered:
            return

        if on_f6:
            self.callbacks["f6"] = on_f6
            keyboard.on_press_key("f6", lambda _: on_f6())

        if on_f7:
            self.callbacks["f7"] = on_f7
            keyboard.on_press_key("f7", lambda _: on_f7())

        if on_f8:
            self.callbacks["f8"] = on_f8
            keyboard.on_press_key("f8", lambda _: on_f8())

        if on_escape:
            self.callbacks["escape"] = on_escape
            keyboard.on_press_key("escape", lambda _: on_escape())

        self.registered = True

    def register_custom(self, keys, on_clicker=None, on_record=None, on_playback=None, on_escape=None):
        if self.registered:
            return

        if on_clicker and keys.get("clicker"):
            self.callbacks["clicker"] = on_clicker
            keyboard.on_press_key(keys["clicker"], lambda _: on_clicker())

        if on_record and keys.get("record"):
            self.callbacks["record"] = on_record
            keyboard.on_press_key(keys["record"], lambda _: on_record())

        if on_playback and keys.get("playback"):
            self.callbacks["playback"] = on_playback
            keyboard.on_press_key(keys["playback"], lambda _: on_playback())

        if on_escape:
            self.callbacks["escape"] = on_escape
            keyboard.on_press_key("escape", lambda _: on_escape())

        self.registered = True

    def unregister(self):
        if not self.registered:
            return
        keyboard.unhook_all()
        self.callbacks = {}
        self.registered = False
