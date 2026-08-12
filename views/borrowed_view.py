"""Borrowed view with search and due date tracking."""

import tkinter as tk

from theme import COLORS, FONTS
from components import SearchBar, ItemRow, RoundedButton


class BorrowedView(tk.Frame):

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
            text='Borrowed',
            bg=COLORS['bg'],
            fg=COLORS['text'],
            font=FONTS['title']
        ).pack(
            anchor='w'
        )

        tk.Label(
            title_frame,
            text='Items you currently have from other people',
            bg=COLORS['bg'],
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(
            anchor='w',
            pady=(3, 0)
        )

        RoundedButton(
            header,
            text='+ Borrowed',
            command=self._add_borrowed,
            bg=COLORS['secondary'],
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

    def _add_borrowed(self):

        self.controller.open_add(
            default_status='borrowed'
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
            status='borrowed',
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
                text='Nothing borrowed',
                bg=COLORS['card'],
                fg=COLORS['text'],
                font=FONTS['body_bold']
            ).pack(
                pady=(30, 4)
            )

            tk.Label(
                empty,
                text='You currently have no borrowed items.',
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