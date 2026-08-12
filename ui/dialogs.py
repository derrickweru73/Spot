"""Reusable dialogs."""

import tkinter as tk
from theme import COLORS, FONTS
from components import RoundedButton


class ConfirmDialog(tk.Toplevel):
    def __init__(self, parent, title="Confirm", message="Are you sure?",
                 confirm_text="Yes", cancel_text="No", on_confirm=None):
        super().__init__(parent)
        self.on_confirm = on_confirm
        self.result = False
        self.title(title)
        self.geometry("380x180")
        self.configure(bg=COLORS["bg"])
        self.transient(parent)
        self.grab_set()
        self._build(message, confirm_text, cancel_text)
        self._center()

    def _build(self, message, confirm_text, cancel_text):
        tk.Label(self, text=message, bg=COLORS["bg"], fg=COLORS["text"],
                 font=FONTS["body"], wraplength=320, justify="center").pack(pady=(24, 16))
        buttons = tk.Frame(self, bg=COLORS["bg"])
        buttons.pack(pady=8)
        RoundedButton(buttons, text=cancel_text, command=self.destroy,
                      bg=COLORS["text_muted"], width=90, height=32).pack(side="left", padx=4)
        RoundedButton(buttons, text=confirm_text, command=self._confirm,
                      bg=COLORS["danger"], width=90, height=32).pack(side="left", padx=4)

    def _confirm(self):
        self.result = True
        if self.on_confirm:
            self.on_confirm()
        self.destroy()

    def _center(self):
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - 190
        y = self.winfo_screenheight() // 2 - 90
        self.geometry(f"+{x}+{y}")


class InputDialog(tk.Toplevel):
    def __init__(self, parent, title="Input", prompt="Enter value:", default=""):
        super().__init__(parent)
        self.result = None
        self.title(title)
        self.geometry("360x160")
        self.configure(bg=COLORS["bg"])
        self.transient(parent)
        self.grab_set()
        self._build(prompt, default)
        self._center()

    def _build(self, prompt, default):
        tk.Label(self, text=prompt, bg=COLORS["bg"], fg=COLORS["text"],
                 font=FONTS["body_bold"]).pack(anchor="w", padx=24, pady=(20, 6))
        self.entry = tk.Entry(self, font=FONTS["body"], bg=COLORS["input_bg"],
                              fg=COLORS["text"], insertbackground=COLORS["text"],
                              relief="flat", highlightthickness=1,
                              highlightcolor=COLORS["primary"],
                              highlightbackground=COLORS["border"])
        self.entry.pack(fill="x", padx=24, ipady=6)
        self.entry.insert(0, default)
        self.entry.select_range(0, "end")
        self.entry.focus_set()

        buttons = tk.Frame(self, bg=COLORS["bg"])
        buttons.pack(pady=16)
        RoundedButton(buttons, text="Cancel", command=self.destroy,
                      bg=COLORS["text_muted"], width=80, height=30).pack(side="left", padx=4)
        RoundedButton(buttons, text="OK", command=self._ok,
                      bg=COLORS["primary"], width=80, height=30).pack(side="left", padx=4)
        self.bind("<Return>", lambda e: self._ok())

    def _ok(self):
        self.result = self.entry.get().strip()
        self.destroy()

    def _center(self):
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - 180
        y = self.winfo_screenheight() // 2 - 80
        self.geometry(f"+{x}+{y}")