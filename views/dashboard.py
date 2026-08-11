"""Dashboard view with stats, recent items, reminders, and move history."""

import tkinter as tk
from theme import COLORS, FONTS, BREAKPOINTS
from components import RoundedButton, StatCard, ItemRow, SearchBar
from database import get_stats, get_all_items, get_history
from datetime import datetime


class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg'])
        self.controller = controller
        self._build()

    def _build(self):
        self.canvas = tk.Canvas(self, bg=COLORS['bg'], highlightthickness=0)
        self.scroll = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.content = tk.Frame(self.canvas, bg=COLORS['bg'])
        
        self.content_window = self.canvas.create_window((0, 0), window=self.content, anchor='nw')
        
        self.content.bind('<Configure>', lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox('all')))
        
        self.canvas.configure(yscrollcommand=self.scroll.set)
        
        self.canvas.pack(side='left', fill='both', expand=True)
        self.scroll.pack(side='right', fill='y')
        
        self.canvas.bind_all('<MouseWheel>',
                             lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))
        
        self.canvas.bind('<Configure>', self._on_canvas_resize)
        self.bind('<Configure>', self._on_view_resize)

        # Header
        header = tk.Frame(self.content, bg=COLORS['bg'])
        header.pack(fill='x', padx=20, pady=(20, 10))
        tk.Label(header, text="Dashboard", bg=COLORS['bg'],
                 font=FONTS['title'], fg=COLORS['text']).pack(side='left')

        RoundedButton(header, text="+ Add Item", command=self.controller.open_add,
                      bg=COLORS['primary'], width=120).pack(side='right')

        # Search
        bar = tk.Frame(self.content, bg=COLORS['bg'])
        bar.pack(fill='x', padx=20, pady=5)
        self.search = SearchBar(bar, on_search=self._on_search, placeholder='Search anything...')
        self.search.pack(fill='x', expand=True)

        # Stats cards container
        self.stats_frame = tk.Frame(self.content, bg=COLORS['bg'])
        self.stats_frame.pack(fill='x', padx=20, pady=15)

        stats = get_stats()
        self.stat_cards = [
            StatCard(self.stats_frame, '■', 'Total Items', stats['total'], COLORS['info'],
                     command=lambda: self.controller.show_view('stash')),
            StatCard(self.stats_frame, '!', 'Lost Items', stats['lost'], COLORS['danger']),
            StatCard(self.stats_frame, '↗', 'Lent Out', stats['lent'], COLORS['warning'],
                     command=lambda: self.controller.show_view('lent')),
            StatCard(self.stats_frame, '↙', 'Borrowed', stats['borrowed'], COLORS['success'],
                     command=lambda: self.controller.show_view('borrowed')),
        ]

        # Main split area
        self.main_area = tk.Frame(self.content, bg=COLORS['bg'])
        self.main_area.pack(fill='both', expand=True, padx=20, pady=10)
        self.main_area.grid_columnconfigure(0, weight=1)

        # Left: Recent Items
        self.left_panel = tk.Frame(self.main_area, bg=COLORS['bg'])
        self.left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        self.left_header = tk.Frame(self.left_panel, bg=COLORS['bg'])
        self.left_header.pack(fill='x', pady=(0, 8))
        tk.Label(self.left_header, text="Recent Items", bg=COLORS['bg'],
                 font=FONTS['heading'], fg=COLORS['text']).pack(side='left')
        va = tk.Label(self.left_header, text="View All →", bg=COLORS['bg'],
                      font=FONTS['small'], fg=COLORS['primary'], cursor='hand2')
        va.pack(side='right')
        va.bind('<Button-1>', lambda e: self.controller.show_view('stash'))
        
        self.recent_container = tk.Frame(self.left_panel, bg=COLORS['border'])
        self.recent_container.pack(fill='both', expand=True)

        # Right: Sidebar widgets
        self.right_panel = tk.Frame(self.main_area, bg=COLORS['bg'], width=300)
        self.right_panel.grid(row=0, column=1, sticky='ns', padx=(10, 0))
        self.right_panel.grid_propagate(False)
        
        # Quick Search
        tk.Label(self.right_panel, text="Quick Search", bg=COLORS['bg'],
                 font=FONTS['heading'], fg=COLORS['text']).pack(anchor='w', pady=(0, 8))
        qs_frame = tk.Frame(self.right_panel, bg=COLORS['card'], padx=15, pady=15)
        qs_frame.pack(fill='x', pady=(0, 15))
        qs_search = SearchBar(qs_frame, on_search=self._quick_search,
                              placeholder='What are you looking for?')
        qs_search.pack(fill='x')
        RoundedButton(qs_frame, text="Search", command=lambda: self._quick_search(qs_search.get()),
                      bg=COLORS['primary'], width=100).pack(pady=(10, 0))

        # Reminders
        tk.Label(self.right_panel, text="Reminders", bg=COLORS['bg'],
                 font=FONTS['heading'], fg=COLORS['text']).pack(anchor='w', pady=(10, 8))
        self.reminders_container = tk.Frame(self.right_panel, bg=COLORS['bg'])
        self.reminders_container.pack(fill='x')

        # Recently Moved
        tk.Label(self.right_panel, text="Recently Moved", bg=COLORS['bg'],
                 font=FONTS['heading'], fg=COLORS['text']).pack(anchor='w', pady=(20, 8))
        self.moved_container = tk.Frame(self.right_panel, bg=COLORS['bg'])
        self.moved_container.pack(fill='x')

        self._load_data()

    def _on_canvas_resize(self, event=None):
        canvas_width = self.canvas.winfo_width()
        if self.scroll.winfo_viewable():
            canvas_width -= 20
        self.canvas.itemconfig(self.content_window, width=max(canvas_width, 300))

    def _on_view_resize(self, event=None):
        w = self.winfo_width()
        
        if w >= BREAKPOINTS['lg']:
            cols = 4
        elif w >= BREAKPOINTS['sm']:
            cols = 2
        else:
            cols = 1
        
        for i, card in enumerate(self.stat_cards):
            card.grid_forget()
            row, col = divmod(i, cols)
            card.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')
        
        for c in range(cols):
            self.stats_frame.grid_columnconfigure(c, weight=1)

        if w >= BREAKPOINTS['md']:
            self.right_panel.grid()
            self.main_area.grid_columnconfigure(1, weight=0)
        else:
            self.right_panel.grid_remove()
            self.main_area.grid_columnconfigure(1, weight=0)

    def _on_search(self, text):
        self._load_recent(search=text)

    def _quick_search(self, text):
        self.controller.show_view('stash')

    def _load_data(self):
        self._load_recent()
        self._load_reminders()
        self._load_moved()

    def _load_recent(self, search=''):
        for w in self.recent_container.winfo_children():
            w.destroy()

        items = get_all_items(search=search, limit=8)
        if not items:
            tk.Label(self.recent_container, text="No items yet. Add your first!",
                     bg=COLORS['card'], font=FONTS['body'], fg=COLORS['text_muted'],
                     padx=20, pady=30).pack(fill='x')
            return

        for item in items:
            row = ItemRow(self.recent_container, item, on_click=self.controller.open_detail)
            row.pack(fill='x', pady=(0, 1))

    def _load_reminders(self):
        for w in self.reminders_container.winfo_children():
            w.destroy()

        now = datetime.now()
        items = get_all_items()
        reminders = []
        for item in items:
            if item.get('due_date') and item['status'] in ('lent', 'borrowed'):
                due = None
                # Try multiple date formats
                for fmt in ('%Y-%m-%d %H:%M', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y'):
                    try:
                        due = datetime.strptime(item['due_date'].strip(), fmt)
                        break
                    except ValueError:
                        continue
                
                if due is None:
                    continue  # Skip unparseable dates
                
                delta = (due - now).days
                if delta <= 3:  # Due within 3 days or overdue
                    reminders.append((item, delta))

        if not reminders:
            tk.Label(self.reminders_container, text="No upcoming reminders",
                     bg=COLORS['card'], font=FONTS['small'], fg=COLORS['text_muted'],
                     padx=12, pady=12).pack(fill='x')
            return

        for item, delta in reminders:
            frame = tk.Frame(self.reminders_container, bg=COLORS['card'], padx=12, pady=10)
            frame.pack(fill='x', pady=(0, 6))
            top = tk.Frame(frame, bg=COLORS['card'])
            top.pack(fill='x')
            icon = '↗' if item['status'] == 'lent' else '↙'
            color = COLORS['warning'] if delta >= 0 else COLORS['danger']
            due_text = f"Due in {delta} days" if delta > 0 else "Due today" if delta == 0 else "OVERDUE"
            tk.Label(top, text=f"{icon} {item['name']}", bg=COLORS['card'],
                     font=FONTS['body_bold'], fg=COLORS['text']).pack(side='left')
            tk.Label(top, text=due_text, bg=COLORS['card'],
                     font=FONTS['small_bold'], fg=color).pack(side='right')
            sub = f"Lent to {item['person']}" if item['status'] == 'lent' else f"Borrowed from {item['person']}"
            tk.Label(frame, text=sub, bg=COLORS['card'],
                     font=FONTS['small'], fg=COLORS['text_muted']).pack(anchor='w')

    def _load_moved(self):
        for w in self.moved_container.winfo_children():
            w.destroy()

        history = get_history(limit=4)
        if not history:
            tk.Label(self.moved_container, text="No moves yet",
                     bg=COLORS['card'], font=FONTS['small'], fg=COLORS['text_muted'],
                     padx=12, pady=12).pack(fill='x')
            return

        for h in history:
            frame = tk.Frame(self.moved_container, bg=COLORS['card'], padx=12, pady=8)
            frame.pack(fill='x', pady=(0, 6))
            tk.Label(frame, text=h['item_name'], bg=COLORS['card'],
                     font=FONTS['body_bold'], fg=COLORS['text']).pack(anchor='w')
            move_text = f"{h['old_location']} → {h['new_location']}"
            if len(move_text) > 35:
                move_text = move_text[:32] + '...'
            tk.Label(frame, text=move_text, bg=COLORS['card'],
                     font=FONTS['small'], fg=COLORS['text_muted']).pack(anchor='w')
            date = h['changed_at'].split()[0] if h['changed_at'] else ''
            tk.Label(frame, text=date, bg=COLORS['card'],
                     font=FONTS['small'], fg=COLORS['text_dark']).pack(anchor='w')

    def refresh(self):
        for w in self.content.winfo_children():
            w.destroy()
        self._build()