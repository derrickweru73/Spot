"""Lent Out view with search and overdue tracking."""

import tkinter as tk
from theme import COLORS, FONTS
from components import SearchBar, ItemRow, RoundedButton


class LentView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg'])
        self.controller = controller
        self.search_text = ''
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=COLORS['bg'])
        header.pack(fill='x', padx=20, pady=(20, 10))
        tk.Label(header, text="Lent Out", bg=COLORS['bg'],
                 font=FONTS['title'], fg=COLORS['text']).pack(side='left')
        RoundedButton(header, text="+ Lent Item", command=self._add_lent,
                      bg=COLORS['warning'], width=110).pack(side='right')

        bar = tk.Frame(self, bg=COLORS['bg'])
        bar.pack(fill='x', padx=20, pady=5)
        self.search = SearchBar(bar, on_search=self._on_search)
        self.search.pack(fill='x', expand=True)

        self.canvas = tk.Canvas(self, bg=COLORS['bg'], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.list_frame = tk.Frame(self.canvas, bg=COLORS['border'])

        self.list_frame.bind('<Configure>',
                             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0, 0), window=self.list_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side='left', fill='both', expand=True, padx=20, pady=10)
        self.scrollbar.pack(side='right', fill='y')

        self.canvas.bind_all('<MouseWheel>',
                             lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))
        self.bind('<Configure>', self._on_resize)

        self._load_items()

    def _on_resize(self, event=None):
        w = self.winfo_width()
        self.canvas.itemconfig(1, width=max(w-80, 300))

    def _add_lent(self):
        self.controller.open_add(default_status='lent')

    def _on_search(self, text):
        self.search_text = text
        self._load_items()

    def _load_items(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        from database import get_all_items
        items = get_all_items(status='lent', search=self.search_text)

        if not items:
            tk.Label(self.list_frame, text="Nothing lent out. Your stuff is safe!",
                     bg=COLORS['card'], font=FONTS['body'], fg=COLORS['text_muted'],
                     padx=20, pady=40).pack(fill='x')
            return

        for item in items:
            row = ItemRow(self.list_frame, item, on_click=self.controller.open_detail)
            row.pack(fill='x', pady=(0, 1))

    def refresh(self):
        self._load_items()