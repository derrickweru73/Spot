"""PIN lock screen."""

import tkinter as tk
from theme import COLORS, FONTS
from config import PIN_LENGTH, PIN_MAX_ATTEMPTS


class PinLockScreen(tk.Toplevel):
    def __init__(self, parent, on_unlock=None):
        super().__init__(parent)
        self.on_unlock = on_unlock
        self.attempts = 0
        self.pin = ""
        self.stored_pin = self._load_pin()

        self.title("Spot - Locked")
        self.geometry("340x420")
        self.configure(bg=COLORS["bg"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        if not self.stored_pin:
            self.destroy()
            if self.on_unlock:
                self.on_unlock()
            return

        self._build()
        self._center()

    def _build(self):
        tk.Label(self, text="SPOT", bg=COLORS["bg"], fg=COLORS["primary"],
                 font=("Segoe UI", 28, "bold")).pack(pady=(30, 5))
        tk.Label(self, text="Enter PIN to unlock", bg=COLORS["bg"],
                 fg=COLORS["text_muted"], font=FONTS["body"]).pack()

        self.dots_frame = tk.Frame(self, bg=COLORS["bg"])
        self.dots_frame.pack(pady=20)

        self.dots = []
        for _ in range(PIN_LENGTH):
            dot = tk.Label(self.dots_frame, text="○", bg=COLORS["bg"],
                           fg=COLORS["text_muted"], font=("Segoe UI", 20))
            dot.pack(side="left", padx=8)
            self.dots.append(dot)

        self.error_label = tk.Label(self, text="", bg=COLORS["bg"],
                                    fg=COLORS["danger"], font=FONTS["small"])
        self.error_label.pack()

        keypad = tk.Frame(self, bg=COLORS["bg"])
        keypad.pack(pady=10)

        buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "C", "0", "⌫"]
        for i, char in enumerate(buttons):
            btn = tk.Button(keypad, text=char, font=("Segoe UI", 14, "bold"),
                            bg=COLORS["card"], fg=COLORS["text"],
                            activebackground=COLORS["card_hover"],
                            activeforeground=COLORS["text"],
                            relief="flat", borderwidth=0, cursor="hand2",
                            width=4, height=2,
                            command=lambda c=char: self._keypress(c))
            btn.grid(row=i // 3, column=i % 3, padx=4, pady=4)

        self.bind("<Key>", self._on_key)

    def _keypress(self, char):
        if char == "C":
            self.pin = ""
        elif char == "⌫":
            self.pin = self.pin[:-1]
        else:
            if len(self.pin) < PIN_LENGTH:
                self.pin += char
        self._update_dots()
        if len(self.pin) == PIN_LENGTH:
            self._check_pin()

    def _on_key(self, event):
        if event.char.isdigit():
            self._keypress(event.char)
        elif event.keysym == "BackSpace":
            self._keypress("⌫")
        elif event.keysym == "Escape":
            self._keypress("C")

    def _update_dots(self):
        for i, dot in enumerate(self.dots):
            dot.config(text="●" if i < len(self.pin) else "○",
                       fg=COLORS["primary"] if i < len(self.pin) else COLORS["text_muted"])

    def _check_pin(self):
        if self.pin == self.stored_pin:
            self.destroy()
            if self.on_unlock:
                self.on_unlock()
        else:
            self.attempts += 1
            remaining = PIN_MAX_ATTEMPTS - self.attempts
            self.error_label.config(text=f"Incorrect PIN. {remaining} attempts remaining.")
            self.pin = ""
            self._update_dots()
            if self.attempts >= PIN_MAX_ATTEMPTS:
                self.error_label.config(text="Too many attempts. Exiting.")
                self.after(1500, self.master.quit)

    def _load_pin(self):
        from config import CONFIG_FILE
        import os
        if not os.path.exists(CONFIG_FILE):
            return None
        try:
            with open(CONFIG_FILE, "r") as f:
                for line in f:
                    if line.startswith("pin="):
                        return line.strip()[4:]
        except Exception:
            pass
        return None

    def _save_pin(self, pin):
        from config import CONFIG_FILE
        import os
        lines = []
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                lines = f.readlines()
        lines = [l for l in lines if not l.startswith("pin=")]
        lines.append(f"pin={pin}\n")
        with open(CONFIG_FILE, "w") as f:
            f.writelines(lines)

    def _center(self):
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - 170
        y = self.winfo_screenheight() // 2 - 210
        self.geometry(f"+{x}+{y}")


def change_pin_dialog(parent):
    from ui.dialogs import InputDialog
    current = PinLockScreen._load_pin(PinLockScreen, None) or ""
    dialog = InputDialog(parent, "Change PIN", "Enter new 4-digit PIN:", current)
    parent.wait_window(dialog)
    if dialog.result and len(dialog.result) == 4 and dialog.result.isdigit():
        PinLockScreen._save_pin(PinLockScreen, None, dialog.result)
        return True
    return False