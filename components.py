"""Reusable custom Tkinter widgets for Spot."""

import tkinter as tk
from theme import COLORS, FONTS, STATUS_COLORS


# ============================================================
# Rounded Button
# ============================================================

class RoundedButton(tk.Canvas):
    def __init__(
        self,
        parent,
        text,
        command=None,
        bg=None,
        fg='white',
        width=120,
        height=36,
        radius=10,
        font=None,
        **kwargs
    ):
        self.btn_bg = bg or COLORS['primary']
        self.btn_fg = fg
        self.command = command
        self.radius = radius
        self._text = text

        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent.cget('bg'),
            highlightthickness=0,
            **kwargs
        )

        self.font = font or FONTS['button']
        self._draw(text)

        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)

    def _draw(self, text, bg=None):
        self.delete('all')

        bg = bg or self.btn_bg

        self.create_rounded_rect(
            0,
            0,
            int(self['width']),
            int(self['height']),
            self.radius,
            fill=bg,
            outline=''
        )

        self.create_text(
            int(self['width']) // 2,
            int(self['height']) // 2,
            text=text,
            fill=self.btn_fg,
            font=self.font
        )

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]

        return self.create_polygon(
            points,
            smooth=True,
            **kwargs
        )

    def _on_enter(self, _):
        self._draw(
            self._text,
            bg=self._shade_color(self.btn_bg, -20)
        )

    def _on_leave(self, _):
        self._draw(self._text)

    def _on_click(self, _):
        if self.command:
            self.command()

    @staticmethod
    def _shade_color(hex_color, amount):
        hex_color = hex_color.lstrip('#')

        rgb = tuple(
            int(hex_color[i:i + 2], 16)
            for i in (0, 2, 4)
        )

        new_rgb = tuple(
            max(0, min(255, c + amount))
            for c in rgb
        )

        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)


# ============================================================
# Status Badge
# ============================================================

class StatusBadge(tk.Canvas):
    STATUS_LABELS = {
        'stored': 'Available',
        'available': 'Available',
        'lent': 'Lent Out',
        'borrowed': 'Borrowed',
        'lost': 'Missing',
        'overdue': 'Overdue'
    }

    def __init__(
        self,
        parent,
        status,
        width=90,
        height=24,
        **kwargs
    ):
        self.status = status.lower()

        self.color = STATUS_COLORS.get(
            self.status,
            COLORS['text_muted']
        )

        self.text = self.STATUS_LABELS.get(
            self.status,
            status.title()
        )

        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent.cget('bg'),
            highlightthickness=0,
            **kwargs
        )

        bg_hex = self._make_soft_background(self.color)

        self.create_rounded_rect(
            0,
            0,
            width,
            height,
            height // 2,
            fill=bg_hex,
            outline=''
        )

        self.create_text(
            width // 2,
            height // 2,
            text=self.text,
            fill=self.color,
            font=FONTS['badge']
        )

    def create_rounded_rect(
        self,
        x1,
        y1,
        x2,
        y2,
        radius,
        **kwargs
    ):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]

        return self.create_polygon(
            points,
            smooth=True,
            **kwargs
        )

    @staticmethod
    def _make_soft_background(hex_color):
        """
        Creates a very light tint of the status color.
        """

        hex_color = hex_color.lstrip('#')

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # Blend with white.
        r = int(r * 0.12 + 255 * 0.88)
        g = int(g * 0.12 + 255 * 0.88)
        b = int(b * 0.12 + 255 * 0.88)

        return '#{:02x}{:02x}{:02x}'.format(r, g, b)


# ============================================================
# Statistic Card
# ============================================================

class StatCard(tk.Frame):
    def __init__(
        self,
        parent,
        icon,
        label,
        value,
        color,
        command=None,
        **kwargs
    ):
        super().__init__(
            parent,
            bg=COLORS['card'],
            padx=18,
            pady=16,
            highlightbackground=COLORS['border'],
            highlightthickness=1,
            **kwargs
        )

        self.command = command

        top = tk.Frame(
            self,
            bg=COLORS['card']
        )
        top.pack(
            fill='x'
        )

        icon_canvas = tk.Canvas(
            top,
            width=38,
            height=38,
            bg=COLORS['card'],
            highlightthickness=0
        )
        icon_canvas.pack(
            side='left'
        )

        icon_canvas.create_oval(
            2,
            2,
            36,
            36,
            fill=color,
            outline=''
        )

        icon_canvas.create_text(
            19,
            19,
            text=icon,
            fill='white',
            font=('Segoe UI', 11, 'bold')
        )

        info = tk.Frame(
            top,
            bg=COLORS['card']
        )
        info.pack(
            side='left',
            padx=(12, 0),
            fill='x',
            expand=True
        )

        tk.Label(
            info,
            text=label,
            bg=COLORS['card'],
            font=FONTS['small'],
            fg=COLORS['text_muted']
        ).pack(
            anchor='w'
        )

        tk.Label(
            info,
            text=str(value),
            bg=COLORS['card'],
            font=('Segoe UI', 21, 'bold'),
            fg=COLORS['text']
        ).pack(
            anchor='w',
            pady=(1, 0)
        )

        if command:
            self._bind_clickable(self)

    def _bind_clickable(self, widget):
        widget.bind(
            '<Button-1>',
            lambda event: self.command()
        )

        for child in widget.winfo_children():
            self._bind_clickable(child)


# ============================================================
# Item Row
# ============================================================

class ItemRow(tk.Frame):
    def __init__(
        self,
        parent,
        item,
        on_click=None,
        **kwargs
    ):
        super().__init__(
            parent,
            bg=COLORS['card'],
            padx=14,
            pady=12,
            highlightbackground=COLORS['border'],
            highlightthickness=1,
            **kwargs
        )

        self.item = item
        self.on_click = on_click

        # ----------------------------------------------------
        # Image
        # ----------------------------------------------------

        self.img_label = tk.Label(
            self,
            bg=COLORS['card'],
            text='📷',
            width=4,
            font=('Segoe UI', 15)
        )

        self.img_label.pack(
            side='left',
            padx=(0, 12)
        )

        if item.get('photo_path'):
            try:
                from PIL import Image, ImageTk

                img = Image.open(
                    item['photo_path']
                )

                img.thumbnail(
                    (46, 46)
                )

                photo = ImageTk.PhotoImage(img)

                self.img_label.config(
                    image=photo,
                    width=46,
                    height=46
                )

                self.img_label.image = photo

            except Exception:
                pass

        # ----------------------------------------------------
        # Main information
        # ----------------------------------------------------

        info = tk.Frame(
            self,
            bg=COLORS['card']
        )

        info.pack(
            side='left',
            fill='both',
            expand=True
        )

        tk.Label(
            info,
            text=item['name'],
            bg=COLORS['card'],
            font=FONTS['body_bold'],
            fg=COLORS['text']
        ).pack(
            anchor='w'
        )

        location = item.get('room', '')

        if item.get('container'):
            location += f"  →  {item['container']}"

        tk.Label(
            info,
            text=location,
            bg=COLORS['card'],
            font=FONTS['small'],
            fg=COLORS['text_muted']
        ).pack(
            anchor='w',
            pady=(2, 0)
        )

        # ----------------------------------------------------
        # Right side
        # ----------------------------------------------------

        right = tk.Frame(
            self,
            bg=COLORS['card']
        )

        right.pack(
            side='right',
            padx=(12, 0)
        )

        status = item.get(
            'status',
            'stored'
        )

        status_badge = StatusBadge(
            right,
            status,
            width=90
        )

        status_badge.pack(
            anchor='e'
        )

        date_text = ''

        if item.get('date_added'):
            date_text = item['date_added'].split()[0]

        tk.Label(
            right,
            text=date_text,
            bg=COLORS['card'],
            font=FONTS['small'],
            fg=COLORS['text_muted']
        ).pack(
            pady=(5, 0)
        )

        self._bind_events()

    # --------------------------------------------------------
    # Events
    # --------------------------------------------------------

    def _bind_events(self):
        self.bind(
            '<Enter>',
            self._on_enter
        )

        self.bind(
            '<Leave>',
            self._on_leave
        )

        self.bind(
            '<Button-1>',
            self._on_click
        )

        self._bind_children(
            self
        )

    def _bind_children(self, widget):
        for child in widget.winfo_children():
            child.bind(
                '<Button-1>',
                self._on_click
            )

            self._bind_children(
                child
            )

    def _on_enter(self, _):
        self._set_bg(
            COLORS['card_hover']
        )

    def _on_leave(self, _):
        self._set_bg(
            COLORS['card']
        )

    def _set_bg(self, color):
        self.config(
            bg=color
        )

        self._update_children_bg(
            self,
            color
        )

    def _update_children_bg(self, widget, color):
        for child in widget.winfo_children():

            try:
                child.config(
                    bg=color
                )
            except tk.TclError:
                pass

            self._update_children_bg(
                child,
                color
            )

    def _on_click(self, event=None):
        if self.on_click:
            self.on_click(
                self.item
            )


# ============================================================
# Search Bar
# ============================================================

class SearchBar(tk.Frame):
    def __init__(
        self,
        parent,
        on_search=None,
        placeholder='Search...',
        **kwargs
    ):
        super().__init__(
            parent,
            bg=parent.cget('bg'),
            **kwargs
        )

        self.on_search = on_search
        self.placeholder = placeholder

        # Search icon
        tk.Label(
            self,
            text='⌕',
            bg=COLORS['input_bg'],
            fg=COLORS['text_muted'],
            font=('Segoe UI', 15)
        ).pack(
            side='left',
            padx=(12, 0)
        )

        self.entry = tk.Entry(
            self,
            font=FONTS['body'],
            bg=COLORS['input_bg'],
            fg=COLORS['text_muted'],
            insertbackground=COLORS['text'],
            relief='flat',
            highlightthickness=1,
            highlightcolor=COLORS['primary'],
            highlightbackground=COLORS['border']
        )

        self.entry.pack(
            side='left',
            fill='x',
            expand=True,
            ipady=8,
            padx=(4, 10)
        )

        self.entry.insert(
            0,
            placeholder
        )

        self.entry.bind(
            '<FocusIn>',
            self._on_focus_in
        )

        self.entry.bind(
            '<FocusOut>',
            self._on_focus_out
        )

        self.entry.bind(
            '<KeyRelease>',
            self._on_key
        )

    def _on_focus_in(self, _):
        if self.entry.get() == self.placeholder:
            self.entry.delete(
                0,
                'end'
            )

            self.entry.config(
                fg=COLORS['text']
            )

    def _on_focus_out(self, _):
        if not self.entry.get().strip():

            self.entry.delete(
                0,
                'end'
            )

            self.entry.insert(
                0,
                self.placeholder
            )

            self.entry.config(
                fg=COLORS['text_muted']
            )

    def _on_key(self, _):
        if self.on_search:

            text = self.entry.get()

            if text == self.placeholder:
                text = ''

            self.on_search(
                text
            )

    def get(self):
        text = self.entry.get()

        if text == self.placeholder:
            return ''

        return text

 