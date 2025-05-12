import tkinter as tk

class KonamiCodeDetector:
    KONAMI_CODE = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]  # Up, Up, Down, Down, Left, Right, Left, Right, B, A

    def __init__(self, root: tk.Tk, callback):
        self.root = root
        self.callback = callback
        self.konami_index = 0  # Track position in the Konami sequence
        self.root.bind("<KeyPress>", self._detect_konami_code)

    def _detect_konami_code(self, event):
        # Check if the pressed key matches the next code key
        if event.keycode == self.KONAMI_CODE[self.konami_index]:
            self.konami_index += 1
            if self.konami_index == len(self.KONAMI_CODE):  # Full sequence matched
                self.callback()  # Trigger callback
                self.konami_index = 0
        else:
            self.konami_index = 0  # Reset on incorrect input