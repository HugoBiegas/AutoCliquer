import threading
import time
import pyautogui

pyautogui.FAILSAFE = True


class Clicker:
    def __init__(self):
        self.running = False
        self.thread = None
        self.interval = 100  # ms
        self.click_type = "left"  # left, right, middle
        self.infinite = True
        self.click_count = 10
        self.use_fixed_position = False
        self.fixed_x = 0
        self.fixed_y = 0
        self.clicks_done = 0
        self.on_status_change = None

    def set_interval(self, ms: int):
        self.interval = max(10, ms)

    def set_click_type(self, click_type: str):
        if click_type in ("left", "right", "middle"):
            self.click_type = click_type

    def set_infinite(self, infinite: bool):
        self.infinite = infinite

    def set_click_count(self, count: int):
        self.click_count = max(1, count)

    def set_fixed_position(self, use_fixed: bool, x: int = 0, y: int = 0):
        self.use_fixed_position = use_fixed
        self.fixed_x = x
        self.fixed_y = y

    def _click_loop(self):
        self.clicks_done = 0
        while self.running:
            if not self.infinite and self.clicks_done >= self.click_count:
                self.running = False
                break

            try:
                if self.use_fixed_position:
                    pyautogui.click(self.fixed_x, self.fixed_y, button=self.click_type)
                else:
                    pyautogui.click(button=self.click_type)
                self.clicks_done += 1
            except pyautogui.FailSafeException:
                self.running = False
                break

            time.sleep(self.interval / 1000.0)

        if self.on_status_change:
            self.on_status_change(False)

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._click_loop, daemon=True)
        self.thread.start()
        if self.on_status_change:
            self.on_status_change(True)

    def stop(self):
        self.running = False
        if self.on_status_change:
            self.on_status_change(False)

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def is_running(self) -> bool:
        return self.running


class ScriptPlayer:
    def __init__(self):
        self.running = False
        self.thread = None
        self.points = []  # Liste de (x, y)
        self.delay = 1000  # ms entre chaque clic
        self.infinite = True
        self.loop_count = 1
        self.current_loop = 0
        self.current_point = 0
        self.on_status_change = None
        self.on_progress_change = None

    def set_points(self, points: list):
        self.points = points.copy()

    def set_delay(self, ms: int):
        self.delay = max(10, ms)

    def set_infinite(self, infinite: bool):
        self.infinite = infinite

    def set_loop_count(self, count: int):
        self.loop_count = max(1, count)

    def _play_loop(self):
        self.current_loop = 0
        while self.running:
            if not self.infinite and self.current_loop >= self.loop_count:
                self.running = False
                break

            for i, point in enumerate(self.points):
                if not self.running:
                    break
                self.current_point = i
                if self.on_progress_change:
                    self.on_progress_change(self.current_loop, i)

                try:
                    x, y = point["x"], point["y"]
                    button = point.get("button", "left")
                    pyautogui.click(x, y, button=button)
                except pyautogui.FailSafeException:
                    self.running = False
                    break

                time.sleep(self.delay / 1000.0)

            self.current_loop += 1

        if self.on_status_change:
            self.on_status_change(False)

    def start(self):
        if self.running or not self.points:
            return
        self.running = True
        self.thread = threading.Thread(target=self._play_loop, daemon=True)
        self.thread.start()
        if self.on_status_change:
            self.on_status_change(True)

    def stop(self):
        self.running = False
        if self.on_status_change:
            self.on_status_change(False)

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def is_running(self) -> bool:
        return self.running
