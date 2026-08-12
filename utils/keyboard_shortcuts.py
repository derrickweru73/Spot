"""Keyboard shortcuts."""

import tkinter as tk

SHORTCUTS = {
    "Ctrl+n": "Add new item",
    "Ctrl+f": "Focus search",
    "Ctrl+e": "Export to CSV",
    "Ctrl+i": "Import from CSV",
    "Ctrl+b": "Create backup",
    "Ctrl+t": "Toggle theme",
    "Ctrl+1": "Dashboard",
    "Ctrl+2": "Inventory",
    "Ctrl+3": "Lent Out",
    "Ctrl+4": "Borrowed",
    "Ctrl+5": "Trash",
    "Ctrl+0": "Advanced Search",
    "Delete": "Move to trash",
    "F5": "Refresh current view",
    "Ctrl+q": "Quit application",
    "Ctrl+h": "Show shortcuts help",
}


def bind_shortcuts(app, controller):
    app.bind("<Control-n>", lambda e: controller.open_add())
    app.bind("<Control-N>", lambda e: controller.open_add())
    app.bind("<Control-f>", lambda e: _focus_search(controller))
    app.bind("<Control-F>", lambda e: _focus_search(controller))
    app.bind("<Control-e>", lambda e: controller.export_items())
    app.bind("<Control-E>", lambda e: controller.export_items())
    app.bind("<Control-i>", lambda e: controller.import_items())
    app.bind("<Control-I>", lambda e: controller.import_items())
    app.bind("<Control-b>", lambda e: controller.create_backup())
    app.bind("<Control-B>", lambda e: controller.create_backup())
    app.bind("<Control-t>", lambda e: controller.toggle_theme())
    app.bind("<Control-T>", lambda e: controller.toggle_theme())
    app.bind("<Control-Key-1>", lambda e: controller.show_view("dashboard"))
    app.bind("<Control-Key-2>", lambda e: controller.show_view("stash"))
    app.bind("<Control-Key-3>", lambda e: controller.show_view("lent"))
    app.bind("<Control-Key-4>", lambda e: controller.show_view("borrowed"))
    app.bind("<Control-Key-5>", lambda e: controller.show_view("trash"))
    app.bind("<Control-Key-0>", lambda e: controller.show_view("search"))
    app.bind("<F5>", lambda e: controller.refresh_current_view())
    app.bind("<Control-q>", lambda e: app.quit())
    app.bind("<Control-Q>", lambda e: app.quit())
    app.bind("<Control-h>", lambda e: show_shortcuts_help(app))
    app.bind("<Control-H>", lambda e: show_shortcuts_help(app))


def _focus_search(controller):
    view = controller.current_view
    if view and hasattr(view, "search"):
        view.search.entry.focus_set()
        view.search.entry.select_range(0, "end")
    return "break"


def show_shortcuts_help(parent):
    dialog = tk.Toplevel(parent)
    dialog.title("Keyboard Shortcuts")
    dialog.geometry("400x500")
    bg = "#1B1E26" if parent.cget("bg") == "#111318" else "#FAF8FF"
    fg = "#F5F5F7" if bg == "#1B1E26" else "#1A1B21"
    muted = "#A5A8B2" if bg == "#1B1E26" else "#6B7280"
    dialog.configure(bg=bg)
    dialog.transient(parent)
    dialog.grab_set()

    tk.Label(dialog, text="Keyboard Shortcuts", bg=bg, fg=fg,
             font=("Segoe UI", 16, "bold")).pack(pady=(20, 10))
    tk.Frame(dialog, bg="#30343D" if bg == "#1B1E26" else "#E5E7EB", height=1).pack(fill="x", padx=20)

    for shortcut, description in SHORTCUTS.items():
        row = tk.Frame(dialog, bg=bg)
        row.pack(fill="x", padx=30, pady=4)
        key_label = tk.Label(row, text=shortcut, bg="#252934" if bg == "#1B1E26" else "#E8EAF8",
                             fg=fg, font=("Segoe UI", 9, "bold"), padx=8, pady=2)
        key_label.pack(side="left")
        tk.Label(row, text=description, bg=bg, fg=muted,
                 font=("Segoe UI", 9)).pack(side="left", padx=(10, 0))

    tk.Button(dialog, text="Close", command=dialog.destroy,
              bg="#FF7A00", fg="white", relief="flat", cursor="hand2",
              font=("Segoe UI", 10, "bold"), padx=20, pady=4).pack(pady=20)