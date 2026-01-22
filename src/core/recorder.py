from pynput import mouse


class Recorder:
    def __init__(self):
        self.recording = False
        self.points = []
        self.listener = None
        self.on_point_added = None
        self.on_status_change = None

    def _on_click(self, x, y, button, pressed):
        if pressed and self.recording:
            # Convertir le bouton en string
            button_map = {
                mouse.Button.left: "left",
                mouse.Button.right: "right",
                mouse.Button.middle: "middle"
            }
            button_str = button_map.get(button, "left")
            point = {"x": int(x), "y": int(y), "button": button_str}
            self.points.append(point)
            if self.on_point_added:
                self.on_point_added(point)

    def start(self):
        if self.recording:
            return
        self.recording = True
        self.listener = mouse.Listener(on_click=self._on_click)
        self.listener.start()
        if self.on_status_change:
            self.on_status_change(True)

    def stop(self):
        self.recording = False
        if self.listener:
            self.listener.stop()
            self.listener = None
        if self.on_status_change:
            self.on_status_change(False)

    def toggle(self):
        if self.recording:
            self.stop()
        else:
            self.start()

    def clear(self):
        self.points = []

    def get_points(self) -> list:
        return self.points.copy()

    def is_recording(self) -> bool:
        return self.recording
