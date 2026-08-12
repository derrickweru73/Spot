"""Toast notifications."""

import tkinter as tk
from theme import COLORS, FONTS
from config import TOAST_DURATION


class ToastManager:
    def __init__(self, parent):
        self.parent = parent
        self.toasts = []
        self.max_toasts = 4

    def show(self, message, toast_type="info", duration=None):
        if duration is None:
            duration = TOAST_DURATION
        while len(self.toasts) >= self.max_toasts:
            old = self.toasts.pop(0)
            old.destroy()
        toast = Toast(self.parent, message, toast_type, duration)
        toast.manager = self
        self.toasts.append(toast)
        self._reposition()

    def _reposition(self):
        x = self.parent.winfo_width() - 20
        y = 60
        for toast in self.toasts:
            if toast.winfo_exists():
                toast.place(x=x - toast.winfo_reqwidth(), y=y)
                y += toast.winfo_reqheight() + 8

    def remove(self, toast):
        if toast in self.toasts:
            self.toasts.remove(toast)
        self._reposition()


class Toast(tk.Frame):
    TYPE_COLORS = {
        "info": ("#00A3FF", "i"),
        "success": ("#2EB872", "✓"),
        "warning": ("#FF7A00", "!"),
        "error": ("#E53935", "✕"),
    }

    def __init__(self, parent, message, toast_type="info", duration=3000):
        super().__init__(parent, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1)
        self.manager = None
        self.duration = duration
        color, icon = self.TYPE_COLORS.get(toast_type, self.TYPE_COLORS["info"])

        icon_label = tk.Label(self, text=icon, bg=color, fg="white",
                              font=("Segoe UI", 10, "bold"), width=3)
        icon_label.pack(side="left", fill="y")

        msg = tk.Label(self, text=message, bg=COLORS["card"], fg=COLORS["text"],
                       font=FONTS["small"], wraplength=280, justify="left", padx=10, pady=8)
        msg.pack(side="left", fill="both", expand=True)

        close = tk.Label(self, text="✕", bg=COLORS["card"], fg=COLORS["text_muted"],
                         font=("Segoe UI", 10), cursor="hand2", padx=8)
        close.pack(side="right", fill="y")
        close.bind("<Button-1>", lambda e: self.dismiss())

        self.after(duration, self.dismiss)
        self.place(x=parent.winfo_width(), y=60)
        self.update_idletasks()

    def dismiss(self):
        if self.winfo_exists():
            self.destroy()
            if self.manager:
                self.manager.remove(self)