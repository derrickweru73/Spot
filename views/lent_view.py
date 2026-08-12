"""Lent Out view with search and overdue tracking."""

import tkinter as tk

from theme import COLORS, FONTS
from components import SearchBar, ItemRow, RoundedButton


class LentView(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(
            parent,
            bg=COLORS['bg']
        )

        self.controller = controller
        self.search_text = ''

        self._build()

    # ====================================================
    # BUILD
    # ====================================================

    def _build(self):

        header = tk.Frame(
            self,
            bg=COLORS['bg']
        )

        header.pack(
            fill='x',
            padx=28,
            pady=(26, 16)
        )

        title_frame = tk.Frame(
            header,
            bg=COLORS['bg']
        )

        title_frame.pack(
            side='left'
        )

        tk.Label(
            title_frame,
            text='Lent Out',
            bg=COLORS['bg'],
            fg=COLORS['text'],
            font=FONTS['title']
        ).pack(
            anchor='w'
        )

        tk.Label(
            title_frame,
            text='Items currently with other people',
            bg=COLORS['bg'],
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(
            anchor='w',
            pady=(3, 0)
        )

        RoundedButton(
            header,
            text='+ Lent Item',
            command=self._add_lent,
            bg=COLORS['primary'],
            width=110,
            height=36
        ).pack(
            side='right'
        )

        # ------------------------------------------------
        # Search
        # ------------------------------------------------

        search_frame = tk.Frame(
            self,
            bg=COLORS['bg']
        )

        search_frame.pack(
            fill='x',
            padx=28,
            pady=(0, 10)
        )

        self.search = SearchBar(
            search_frame,
            on_search=self._on_search
        )

        self.search.pack(
            fill='x',
            expand=True
        )

        # ------------------------------------------------
        # List
        # ------------------------------------------------

        list_container = tk.Frame(
            self,
            bg=COLORS['bg']
        )

        list_container.pack(
            fill='both',
            expand=True,
            padx=28,
            pady=(5, 20)
        )

        self.canvas = tk.Canvas(
            list_container,
            bg=COLORS['bg'],
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            list_container,
            orient='vertical',
            command=self.canvas.yview
        )

        self.list_frame = tk.Frame(
            self.canvas,
            bg=COLORS['bg']
        )

        self.list_frame.bind(
            '<Configure>',
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox('all')
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.list_frame,
            anchor='nw'
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.pack(
            side='left',
            fill='both',
            expand=True
        )

        self.scrollbar.pack(
            side='right',
            fill='y'
        )

        self.canvas.bind(
            '<Configure>',
            self._on_resize
        )

        self.canvas.bind_all(
            '<MouseWheel>',
            self._on_mousewheel
        )

        self._load_items()

    # ====================================================
    # ADD
    # ====================================================

    def _add_lent(self):

        self.controller.open_add(
            default_status='lent'
        )

    # ====================================================
    # SEARCH
    # ====================================================

    def _on_search(self, text):

        self.search_text = text
        self._load_items()

    # ====================================================
    # LOAD
    # ====================================================

    def _load_items(self):

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        from database import get_all_items

        items = get_all_items(
            status='lent',
            search=self.search_text
        )

        if not items:

            empty = tk.Frame(
                self.list_frame,
                bg=COLORS['card'],
                highlightbackground=COLORS['border'],
                highlightthickness=1
            )

            empty.pack(
                fill='x',
                pady=5
            )

            tk.Label(
                empty,
                text='Nothing lent out',
                bg=COLORS['card'],
                fg=COLORS['text'],
                font=FONTS['body_bold']
            ).pack(
                pady=(30, 4)
            )

            tk.Label(
                empty,
                text='Your items are all safely with you.',
                bg=COLORS['card'],
                fg=COLORS['text_muted'],
                font=FONTS['small']
            ).pack(
                pady=(0, 30)
            )

            return

        for item in items:

            row = ItemRow(
                self.list_frame,
                item,
                on_click=self.controller.open_detail,
                controller=self.controller
            )
            row.pack(
                fill='x',
                pady=(0, 6)
            )

    # ====================================================
    # RESIZE
    # ====================================================

    def _on_resize(self, event=None):

        if event:
            self.canvas.itemconfig(
                self.canvas_window,
                width=event.width
            )

    # ====================================================
    # MOUSE WHEEL
    # ====================================================

    def _on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            'units'
        )

    # ====================================================
    # REFRESH
    # ====================================================

    def refresh(self):

        self._load_items()