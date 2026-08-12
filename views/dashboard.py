"""Spot dashboard view."""

import tkinter as tk

from theme import COLORS, FONTS, DARK_MODE
from components import (
    StatCard,
    ItemRow,
    RoundedButton,
    SearchBar
)
from database import get_stats, get_all_items


class DashboardView(tk.Frame):

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

        self.canvas = tk.Canvas(
            self,
            bg=COLORS['bg'],
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            self,
            orient='vertical',
            command=self.canvas.yview
        )

        self.container = tk.Frame(
            self.canvas,
            bg=COLORS['bg']
        )

        self.container.bind(
            '<Configure>',
            lambda event:
            self.canvas.configure(
                scrollregion=self.canvas.bbox('all')
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.container,
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
            self._resize_container
        )

        self.canvas.bind_all(
            '<MouseWheel>',
            self._on_mousewheel
        )

        self._build_content()

    # ====================================================
    # CONTENT
    # ====================================================

    def _build_content(self):

        content = self.container

        # ------------------------------------------------
        # Header
        # ------------------------------------------------

        header = tk.Frame(
            content,
            bg=COLORS['bg']
        )

        header.pack(
            fill='x',
            padx=28,
            pady=(26, 18)
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
            text='Dashboard',
            bg=COLORS['bg'],
            fg=COLORS['text'],
            font=FONTS['title']
        ).pack(
            anchor='w'
        )

        tk.Label(
            title_frame,
            text='Overview of your personal inventory',
            bg=COLORS['bg'],
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(
            anchor='w',
            pady=(3, 0)
        )

        # ------------------------------------------------
        # Header Actions
        # ------------------------------------------------

        actions = tk.Frame(
            header,
            bg=COLORS['bg']
        )

        actions.pack(
            side='right'
        )

        # Sun / Moon toggle
        self.theme_button = tk.Button(
            actions,
            text='☀' if DARK_MODE else '☾',
            command=self.controller.toggle_theme,
            bg=COLORS['card'],
            fg=COLORS['text'],
            activebackground=COLORS['card_hover'],
            activeforeground=COLORS['text'],
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            font=('Segoe UI Symbol', 16),
            width=3,
            height=1
        )

        self.theme_button.pack(
            side='left',
            padx=(0, 8)
        )

        # Add Item
        RoundedButton(
            actions,
            text='+ Add Item',
            command=self.controller.open_add,
            bg=COLORS['primary'],
            width=105,
            height=36
        ).pack(
            side='left'
        )

        # ------------------------------------------------
        # Search
        # ------------------------------------------------

        search_frame = tk.Frame(
            content,
            bg=COLORS['bg']
        )

        search_frame.pack(
            fill='x',
            padx=28,
            pady=(0, 5)
        )

        self.search = SearchBar(
            search_frame,
            on_search=self._on_search,
            placeholder='Search your items...'
        )

        self.search.pack(
            fill='x',
            expand=True
        )

        # ------------------------------------------------
        # Statistics
        # ------------------------------------------------

        self._build_stats(content)

        # ------------------------------------------------
        # Main sections
        # ------------------------------------------------

        self.sections = tk.Frame(
            content,
            bg=COLORS['bg']
        )

        self.sections.pack(
            fill='both',
            expand=True,
            padx=28,
            pady=(22, 30)
        )

        self.sections.grid_columnconfigure(
            0,
            weight=3
        )

        self.sections.grid_columnconfigure(
            1,
            weight=2
        )

        self._build_recent_items(
            self.sections
        )

        self._build_reminders(
            self.sections
        )

    # ====================================================
    # STATISTICS
    # ====================================================

    def _build_stats(self, parent):

        stats = get_stats()

        stats_frame = tk.Frame(
            parent,
            bg=COLORS['bg']
        )

        stats_frame.pack(
            fill='x',
            padx=28
        )

        for column in range(4):

            stats_frame.grid_columnconfigure(
                column,
                weight=1
            )

        cards = [
            (
                '▣',
                'Total Items',
                stats['total'],
                COLORS['stat_total'],
                None
            ),
            (
                '✓',
                'Available',
                stats['stored'],
                COLORS['success'],
                lambda:
                self.controller.show_view('stash')
            ),
            (
                '↗',
                'Lent Out',
                stats['lent'],
                COLORS['stat_lent'],
                lambda:
                self.controller.show_view('lent')
            ),
            (
                '↙',
                'Borrowed',
                stats['borrowed'],
                COLORS['stat_borrowed'],
                lambda:
                self.controller.show_view('borrowed')
            )
        ]

        for index, card_data in enumerate(cards):

            card = StatCard(
                stats_frame,
                *card_data
            )

            card.grid(
                row=0,
                column=index,
                sticky='nsew',
                padx=(
                    0 if index == 0 else 6,
                    0
                )
            )

    # ====================================================
    # RECENT ITEMS
    # ====================================================

    def _on_search(self, text):

        self.search_text = text

        if hasattr(
            self,
            'recent_section'
        ):

            self.recent_section.destroy()

        self._build_recent_items(
            self.sections
        )

    def _build_recent_items(self, parent):

        self.recent_section = tk.Frame(
            parent,
            bg=COLORS['card'],
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )

        self.recent_section.grid(
            row=0,
            column=0,
            sticky='nsew',
            padx=(0, 8)
        )

        header = tk.Frame(
            self.recent_section,
            bg=COLORS['card']
        )

        header.pack(
            fill='x',
            padx=18,
            pady=(16, 12)
        )

        tk.Label(
            header,
            text='Recent Items',
            bg=COLORS['card'],
            fg=COLORS['text'],
            font=FONTS['heading']
        ).pack(
            side='left'
        )

        tk.Button(
            header,
            text='View all',
            command=lambda:
            self.controller.show_view('stash'),
            bg=COLORS['card'],
            fg=COLORS['primary'],
            activebackground=COLORS['card'],
            activeforeground=COLORS['primary'],
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            font=FONTS['small_bold']
        ).pack(
            side='right'
        )

        items = get_all_items(
            search=getattr(
                self,
                'search_text',
                ''
            ),
            limit=5
        )

        list_frame = tk.Frame(
            self.recent_section,
            bg=COLORS['card']
        )

        list_frame.pack(
            fill='both',
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        if not items:

            tk.Label(
                list_frame,
                text='No items added yet.',
                bg=COLORS['card'],
                fg=COLORS['text_muted'],
                font=FONTS['body']
            ).pack(
                pady=35
            )

            return

        for item in items:

            row = ItemRow(
                list_frame,
                item,
                on_click=self.controller.open_detail
            )

            row.pack(
                fill='x',
                pady=(0, 6)
            )

    # ====================================================
    # REMINDERS
    # ====================================================

    def _build_reminders(self, parent):

        section = tk.Frame(
            parent,
            bg=COLORS['card'],
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )

        section.grid(
            row=0,
            column=1,
            sticky='nsew',
            padx=(8, 0)
        )

        header = tk.Frame(
            section,
            bg=COLORS['card']
        )

        header.pack(
            fill='x',
            padx=18,
            pady=(16, 12)
        )

        tk.Label(
            header,
            text='Reminders',
            bg=COLORS['card'],
            fg=COLORS['text'],
            font=FONTS['heading']
        ).pack(
            side='left'
        )

        reminder_items = self._get_reminder_items()

        overdue_count = sum(
            1
            for item in reminder_items
            if item.get('is_overdue')
        )

        badge_color = (
            COLORS['danger']
            if overdue_count > 0
            else COLORS['success']
        )

        tk.Label(
            header,
            text=str(overdue_count),
            bg=badge_color,
            fg=COLORS['text_inverse'],
            font=FONTS['small_bold'],
            padx=7,
            pady=2
        ).pack(
            side='right'
        )

        reminder_frame = tk.Frame(
            section,
            bg=COLORS['card']
        )

        reminder_frame.pack(
            fill='both',
            expand=True,
            padx=18,
            pady=(0, 18)
        )

        if reminder_items:

            for item in reminder_items[:5]:

                self._create_reminder(
                    reminder_frame,
                    item
                )

        else:

            empty = tk.Frame(
                reminder_frame,
                bg=COLORS['card']
            )

            empty.pack(
                fill='both',
                expand=True
            )

            tk.Label(
                empty,
                text='✓',
                bg=COLORS['card'],
                fg=COLORS['success'],
                font=('Segoe UI', 24, 'bold')
            ).pack(
                pady=(35, 5)
            )

            tk.Label(
                empty,
                text="You're all caught up!",
                bg=COLORS['card'],
                fg=COLORS['text'],
                font=FONTS['body_bold']
            ).pack()

            tk.Label(
                empty,
                text='No upcoming due dates.',
                bg=COLORS['card'],
                fg=COLORS['text_muted'],
                font=FONTS['small']
            ).pack(
                pady=(3, 0)
            )

    # ====================================================
    # REMINDER ITEM
    # ====================================================

    def _create_reminder(
        self,
        parent,
        item
    ):

        overdue = item.get(
            'is_overdue',
            False
        )

        accent = (
            COLORS['danger']
            if overdue
            else COLORS['primary']
        )

        frame = tk.Frame(
            parent,
            bg=COLORS['bg'],
            highlightbackground=COLORS['border'],
            highlightthickness=1,
            cursor='hand2'
        )

        frame.pack(
            fill='x',
            pady=(0, 8)
        )

        icon = tk.Label(
            frame,
            text='!' if overdue else '•',
            bg=accent,
            fg=COLORS['text_inverse'],
            font=('Segoe UI', 10, 'bold'),
            width=3
        )

        icon.pack(
            side='left',
            padx=10,
            pady=10
        )

        info = tk.Frame(
            frame,
            bg=COLORS['bg']
        )

        info.pack(
            side='left',
            fill='x',
            expand=True,
            pady=8
        )

        tk.Label(
            info,
            text=item['name'],
            bg=COLORS['bg'],
            fg=COLORS['text'],
            font=FONTS['body_bold']
        ).pack(
            anchor='w'
        )

        person = item.get(
            'person'
        ) or 'Unknown'

        tk.Label(
            info,
            text=f'With {person}',
            bg=COLORS['bg'],
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(
            anchor='w',
            pady=(2, 0)
        )

        due = item.get(
            'due_date'
        ) or ''

        due_label = (
            'Overdue'
            if overdue
            else 'Due'
        )

        tk.Label(
            frame,
            text=f'{due_label}\n{due}',
            bg=COLORS['bg'],
            fg=accent,
            font=FONTS['small_bold'],
            justify='right'
        ).pack(
            side='right',
            padx=10
        )

        frame.bind(
            '<Button-1>',
            lambda event, i=item:
            self.controller.open_detail(i)
        )

        for child in frame.winfo_children():

            child.bind(
                '<Button-1>',
                lambda event, i=item:
                self.controller.open_detail(i)
            )

    # ====================================================
    # OVERDUE
    # ====================================================

    def _get_reminder_items(self):

        from datetime import datetime

        items = get_all_items()

        now = datetime.now()

        reminders = []

        for item in items:

            due_date = item.get(
                'due_date'
            )

            if not due_date:
                continue

            if item.get(
                'status'
            ) not in (
                'lent',
                'borrowed'
            ):
                continue

            try:

                due = datetime.fromisoformat(
                    due_date
                )

                item = item.copy()

                item['is_overdue'] = (
                    due < now
                )

                reminders.append(
                    item
                )

            except ValueError:
                continue

        reminders.sort(
            key=lambda item: (
                not item['is_overdue'],
                item.get(
                    'due_date',
                    ''
                )
            )
        )

        return reminders

    # ====================================================
    # RESPONSIVE
    # ====================================================

    def _resize_container(
        self,
        event
    ):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    # ====================================================
    # MOUSE WHEEL
    # ====================================================

    def _on_mousewheel(
        self,
        event
    ):

        self.canvas.yview_scroll(
            int(
                -1 *
                (event.delta / 120)
            ),
            'units'
        )

    # ====================================================
    # REFRESH
    # ====================================================

    def refresh(self):

        for widget in self.container.winfo_children():
            widget.destroy()

        self._build_content()