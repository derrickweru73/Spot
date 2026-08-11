"""My Items view with search and scrollable item rows."""

import tkinter as tk

from theme import COLORS, FONTS
from components import SearchBar, ItemRow, RoundedButton


class StashView(tk.Frame):

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

        # ------------------------------------------------
        # Header
        # ------------------------------------------------

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
            text='My Items',
            bg=COLORS['bg'],
            fg=COLORS['text'],
            font=FONTS['title']
        ).pack(
            anchor='w'
        )

        tk.Label(
            title_frame,
            text='Everything currently stored in your inventory',
            bg=COLORS['bg'],
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(
            anchor='w',
            pady=(3, 0)
        )

        RoundedButton(
            header,
            text='+ Add Item',
            command=self.controller.open_add,
            bg=COLORS['primary'],
            width=105,
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
        # Item list
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
    # RESIZE
    # ====================================================

    def _on_resize(self, event=None):

        if event:
            self.canvas.itemconfig(
                self.canvas_window,
                width=event.width
            )

    # ====================================================
    # SEARCH
    # ====================================================

    def _on_search(self, text):

        self.search_text = text
        self._load_items()

    # ====================================================
    # LOAD ITEMS
    # ====================================================

    def _load_items(self):

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        from database import get_all_items

        items = get_all_items(
            status='stored',
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
                text='No items found',
                bg=COLORS['card'],
                fg=COLORS['text'],
                font=FONTS['body_bold']
            ).pack(
                pady=(30, 4)
            )

            tk.Label(
                empty,
                text='Try another search or add a new item.',
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
                on_click=self.controller.open_detail
            )

            row.pack(
                fill='x',
                pady=(0, 6)
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