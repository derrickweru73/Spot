"""Trash view with restore."""

import tkinter as tk
from theme import COLORS, FONTS
from components import SearchBar, RoundedButton
from database import get_deleted_items, restore_item, permanently_delete_item


class TrashView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg"])
        self.controller = controller
        self.search_text = ""
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=COLORS["bg"])
        header.pack(fill="x", padx=28, pady=(26, 16))

        title_frame = tk.Frame(header, bg=COLORS["bg"])
        title_frame.pack(side="left")

        tk.Label(title_frame, text="Trash", bg=COLORS["bg"], fg=COLORS["text"],
                 font=FONTS["title"]).pack(anchor="w")
        tk.Label(title_frame, text="Deleted items can be restored within 30 days",
                 bg=COLORS["bg"], fg=COLORS["text_muted"],
                 font=FONTS["small"]).pack(anchor="w", pady=(3, 0))

        RoundedButton(header, text="Empty Trash", command=self._empty_trash,
                      bg=COLORS["danger"], width=110, height=36).pack(side="right")

        search_frame = tk.Frame(self, bg=COLORS["bg"])
        search_frame.pack(fill="x", padx=28, pady=(0, 10))

        self.search = SearchBar(search_frame, on_search=self._on_search)
        self.search.pack(fill="x", expand=True)

        list_container = tk.Frame(self, bg=COLORS["bg"])
        list_container.pack(fill="both", expand=True, padx=28, pady=(5, 20))

        self.canvas = tk.Canvas(list_container, bg=COLORS["bg"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        self.list_frame = tk.Frame(self.canvas, bg=COLORS["bg"])

        self.list_frame.bind("<Configure>",
                             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas_window = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self._load_items()

    def _on_resize(self, event=None):
        if event:
            self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_search(self, text):
        self.search_text = text
        self._load_items()

    def _load_items(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        items = get_deleted_items(search=self.search_text)
        if not items:
            self._show_empty()
            return

        for item in items:
            self._create_trash_row(item)

    def _show_empty(self):
        empty = tk.Frame(self.list_frame, bg=COLORS["card"],
                         highlightbackground=COLORS["border"], highlightthickness=1)
        empty.pack(fill="x", pady=5)

        tk.Label(empty, text="Trash is empty", bg=COLORS["card"],
                 fg=COLORS["text"], font=FONTS["body_bold"]).pack(pady=(30, 4))
        tk.Label(empty, text="Deleted items will appear here.",
                 bg=COLORS["card"], fg=COLORS["text_muted"],
                 font=FONTS["small"]).pack(pady=(0, 30))

    def _create_trash_row(self, item):
        row = tk.Frame(self.list_frame, bg=COLORS["card"],
                       highlightbackground=COLORS["border"], highlightthickness=1)
        row.pack(fill="x", pady=(0, 6))

        info = tk.Frame(row, bg=COLORS["card"])
        info.pack(side="left", fill="both", expand=True, padx=14, pady=12)

        tk.Label(info, text=item["name"], bg=COLORS["card"],
                 fg=COLORS["text"], font=FONTS["body_bold"]).pack(anchor="w")
        deleted_at = item.get("deleted_at", "Unknown")
        tk.Label(info, text=f"Deleted: {deleted_at}", bg=COLORS["card"],
                 fg=COLORS["text_muted"], font=FONTS["small"]).pack(anchor="w", pady=(2, 0))

        actions = tk.Frame(row, bg=COLORS["card"])
        actions.pack(side="right", padx=14)

        RoundedButton(actions, text="Restore", command=lambda i=item: self._restore(i["id"]),
                      bg=COLORS["success"], width=80, height=28).pack(side="left", padx=2)
        RoundedButton(actions, text="Delete", command=lambda i=item: self._permanent_delete(i),
                      bg=COLORS["danger"], width=80, height=28).pack(side="left", padx=2)

    def _restore(self, item_id):
        restore_item(item_id)
        self.controller.refresh_current_view()
        self.controller.toast.show("Item restored", "success")

    def _permanent_delete(self, item):
        from tkinter import messagebox
        if messagebox.askyesno("Permanently Delete",
                               f"Permanently delete '{item['name']}'? This cannot be undone."):
            permanently_delete_item(item["id"])
            self._load_items()
            self.controller.toast.show("Item permanently deleted", "warning")

    def _empty_trash(self):
        from tkinter import messagebox
        items = get_deleted_items()
        if not items:
            return
        if messagebox.askyesno("Empty Trash",
                               f"Permanently delete all {len(items)} items? This cannot be undone."):
            for item in items:
                permanently_delete_item(item["id"])
            self._load_items()
            self.controller.toast.show("Trash emptied", "warning")

    def refresh(self):
        self._load_items()