"""Advanced search with filters."""

import tkinter as tk
from tkinter import ttk
from theme import COLORS, FONTS
from components import ItemRow, RoundedButton
from database import advanced_search


class SearchResultsView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg"])
        self.controller = controller
        self.filters = {}
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=COLORS["bg"])
        header.pack(fill="x", padx=28, pady=(26, 16))

        title_frame = tk.Frame(header, bg=COLORS["bg"])
        title_frame.pack(side="left")

        tk.Label(title_frame, text="Advanced Search", bg=COLORS["bg"],
                 fg=COLORS["text"], font=FONTS["title"]).pack(anchor="w")
        tk.Label(title_frame, text="Filter and find items across your inventory",
                 bg=COLORS["bg"], fg=COLORS["text_muted"],
                 font=FONTS["small"]).pack(anchor="w", pady=(3, 0))

        filter_card = tk.Frame(self, bg=COLORS["card"],
                               highlightbackground=COLORS["border"], highlightthickness=1)
        filter_card.pack(fill="x", padx=28, pady=(0, 10))

        filters = tk.Frame(filter_card, bg=COLORS["card"])
        filters.pack(fill="x", padx=16, pady=14)

        self._add_filter(filters, "Name/Keyword", "search", 0, 0)

        self.status_var = tk.StringVar(value="All")
        self._add_combo(filters, "Status", "status",
                        ["All", "stored", "lent", "borrowed", "lost"], 0, 1)

        self.room_var = tk.StringVar(value="All")
        self._add_combo(filters, "Room", "room",
                        ["All", "Bedroom", "Living Room", "Kitchen", "Office",
                         "Storage", "Garage", "Bathroom", "Car"], 0, 2)

        self.cat_var = tk.StringVar(value="All")
        self._add_combo(filters, "Category", "category",
                        ["All", "General", "Electronics", "Clothes", "Documents",
                         "Tools", "Books", "Kitchen", "Sports", "Seasonal"], 1, 0)

        self._add_filter(filters, "Person", "person", 1, 1)
        self._add_filter(filters, "Due After", "date_from", 1, 2, "YYYY-MM-DD")

        btn_frame = tk.Frame(filter_card, bg=COLORS["card"])
        btn_frame.pack(fill="x", padx=16, pady=(0, 14))

        RoundedButton(btn_frame, text="Search", command=self._search,
                      bg=COLORS["primary"], width=100, height=32).pack(side="left", padx=2)
        RoundedButton(btn_frame, text="Clear", command=self._clear,
                      bg=COLORS["text_muted"], width=100, height=32).pack(side="left", padx=2)

        self.count_label = tk.Label(self, text="", bg=COLORS["bg"],
                                    fg=COLORS["text_muted"], font=FONTS["small"])
        self.count_label.pack(anchor="w", padx=28)

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

    def _add_filter(self, parent, label, key, row, col, placeholder=""):
        frame = tk.Frame(parent, bg=COLORS["card"])
        frame.grid(row=row, column=col, sticky="ew", padx=6, pady=4)

        tk.Label(frame, text=label, bg=COLORS["card"],
                 fg=COLORS["text_muted"], font=FONTS["small"]).pack(anchor="w")

        entry = tk.Entry(frame, font=FONTS["body"], bg=COLORS["input_bg"],
                         fg=COLORS["text"], insertbackground=COLORS["text"],
                         relief="flat", highlightthickness=1,
                         highlightcolor=COLORS["primary"],
                         highlightbackground=COLORS["border"])
        entry.pack(fill="x", ipady=4)
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=COLORS["text_muted"])
            entry.bind("<FocusIn>", lambda e, ent=entry, ph=placeholder:
                       (ent.delete(0, "end"), ent.config(fg=COLORS["text"])) if ent.get() == ph else None)
            entry.bind("<FocusOut>", lambda e, ent=entry, ph=placeholder:
                       (ent.insert(0, ph), ent.config(fg=COLORS["text_muted"])) if not ent.get().strip() else None)

        self.filters[key] = entry

    def _add_combo(self, parent, label, key, values, row, col):
        frame = tk.Frame(parent, bg=COLORS["card"])
        frame.grid(row=row, column=col, sticky="ew", padx=6, pady=4)

        tk.Label(frame, text=label, bg=COLORS["card"],
                 fg=COLORS["text_muted"], font=FONTS["small"]).pack(anchor="w")

        var = tk.StringVar(value=values[0])
        combo = ttk.Combobox(frame, textvariable=var, values=values,
                             state="readonly", font=FONTS["body"])
        combo.pack(fill="x")
        self.filters[key] = var

    def _on_resize(self, event=None):
        if event:
            self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _search(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        params = {
            "search": self.filters["search"].get(),
            "status": self.status_var.get() if self.status_var.get() != "All" else None,
            "room": self.room_var.get() if self.room_var.get() != "All" else None,
            "category": self.cat_var.get() if self.cat_var.get() != "All" else None,
            "person": self.filters["person"].get(),
        }

        date_from = self.filters.get("date_from")
        if date_from:
            val = date_from.get()
            if val and val != "YYYY-MM-DD":
                params["date_from"] = val

        items = advanced_search(**params)
        self.count_label.config(text=f"{len(items)} result(s) found")

        if not items:
            empty = tk.Frame(self.list_frame, bg=COLORS["card"],
                             highlightbackground=COLORS["border"], highlightthickness=1)
            empty.pack(fill="x", pady=5)
            tk.Label(empty, text="No items match your filters.",
                     bg=COLORS["card"], fg=COLORS["text_muted"],
                     font=FONTS["body"]).pack(pady=30)
            return

        for item in items:
            row = ItemRow(self.list_frame, item, on_click=self.controller.open_detail,
                          controller=self.controller)
            row.pack(fill="x", pady=(0, 6))

    def _clear(self):
        for key, widget in self.filters.items():
            if isinstance(widget, tk.Entry):
                widget.delete(0, "end")
        self.status_var.set("All")
        self.room_var.set("All")
        self.cat_var.set("All")
        self.count_label.config(text="")
        for widget in self.list_frame.winfo_children():
            widget.destroy()

    def refresh(self):
        pass