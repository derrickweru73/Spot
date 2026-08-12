"""Item detail window for Spot."""

import tkinter as tk
from tkinter import messagebox

from theme import COLORS, FONTS
from components import RoundedButton, StatusBadge
from database import get_item, get_history


class ItemDetailWindow(tk.Toplevel):

    def __init__(self, parent, controller, item_id):
        super().__init__(parent)

        self.controller = controller
        self.item_id = item_id

        self.item = get_item(item_id)

        if not self.item:
            messagebox.showerror(
                "Item Not Found",
                "This item could not be found.",
                parent=parent
            )
            self.destroy()
            return

        self.title(
            f"Spot - {self.item['name']}"
        )

        self.geometry(
            "560x650"
        )

        self.minsize(
            420,
            520
        )

        self.configure(
            bg=COLORS['bg']
        )

        self.transient(parent)
        self.grab_set()

        self._build()
        self.center_window()

    # ========================================================
    # Center
    # ========================================================

    def center_window(self):

        self.update_idletasks()

        width = 560
        height = 650

        x = (
            self.winfo_screenwidth() // 2
            - width // 2
        )

        y = (
            self.winfo_screenheight() // 2
            - height // 2
        )

        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # ========================================================
    # Build
    # ========================================================

    def _build(self):

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        header = tk.Frame(
            self,
            bg=COLORS['bg']
        )

        header.pack(
            fill='x',
            padx=24,
            pady=(24, 14)
        )

        tk.Label(
            header,
            text="Item Details",
            bg=COLORS['bg'],
            fg=COLORS['text'],
            font=FONTS['title']
        ).pack(
            side='left'
        )

        RoundedButton(
            header,
            text="✕",
            command=self.destroy,
            bg=COLORS['text_muted'],
            width=38,
            height=32,
            radius=8
        ).pack(
            side='right'
        )



        from ui.context_menu import ItemContextMenu
        self.context_menu = ItemContextMenu(self, self.controller, self.item)
        self.bind("<Button-3>", self.context_menu.show)

        # ----------------------------------------------------
        # Scrollable content
        # ----------------------------------------------------

        canvas = tk.Canvas(
            self,
            bg=COLORS['bg'],
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            self,
            orient='vertical',
            command=canvas.yview
        )

        content = tk.Frame(
            canvas,
            bg=COLORS['bg']
        )

        window_id = canvas.create_window(
            (0, 0),
            window=content,
            anchor='nw'
        )

        content.bind(
            '<Configure>',
            lambda event:
            canvas.configure(
                scrollregion=canvas.bbox('all')
            )
        )

        canvas.bind(
            '<Configure>',
            lambda event:
            canvas.itemconfig(
                window_id,
                width=event.width
            )
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side='left',
            fill='both',
            expand=True,
            padx=(24, 5),
            pady=(0, 20)
        )

        scrollbar.pack(
            side='right',
            fill='y',
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # Main card
        # ----------------------------------------------------

        card = tk.Frame(
            content,
            bg=COLORS['card'],
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )

        card.pack(
            fill='x',
            pady=(0, 12)
        )

        # ----------------------------------------------------
        # Photo
        # ----------------------------------------------------

        photo_frame = tk.Frame(
            card,
            bg=COLORS['card']
        )

        photo_frame.pack(
            fill='x',
            padx=20,
            pady=(20, 12)
        )

        self._display_photo(
            photo_frame
        )

        # ----------------------------------------------------
        # Name
        # ----------------------------------------------------

        tk.Label(
            card,
            text=self.item['name'],
            bg=COLORS['card'],
            fg=COLORS['text'],
            font=('Segoe UI', 20, 'bold')
        ).pack(
            anchor='w',
            padx=20
        )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        status = self.item.get(
            'status',
            'stored'
        )

        status_text = (
            'Available'
            if status == 'stored'
            else status.title()
        )

        StatusBadge(
            card,
            status_text,
            width=90,
            height=26
        ).pack(
            anchor='w',
            padx=20,
            pady=(8, 18)
        )

        # ----------------------------------------------------
        # Details
        # ----------------------------------------------------

        details = tk.Frame(
            card,
            bg=COLORS['card']
        )

        details.pack(
            fill='x',
            padx=20,
            pady=(0, 15)
        )

        self._detail_row(
            details,
            "Category",
            self.item.get(
                'category',
                'General'
            )
        )

        location = self.item.get(
            'room',
            ''
        )

        if self.item.get('container'):
            location += (
                f" → "
                f"{self.item['container']}"
            )

        self._detail_row(
            details,
            "Location",
            location
        )

        if self.item.get('person'):

            self._detail_row(
                details,
                "Person",
                self.item['person']
            )

        if self.item.get('due_date'):

            self._detail_row(
                details,
                "Due Date",
                self.item['due_date']
            )

        if self.item.get('date_added'):

            self._detail_row(
                details,
                "Added",
                self.item['date_added']
            )

        if self.item.get('tags'):

            self._detail_row(
                details,
                "Tags",
                self.item['tags']
            )

        # ----------------------------------------------------
        # Notes
        # ----------------------------------------------------

        if self.item.get('notes'):

            tk.Label(
                card,
                text="Notes",
                bg=COLORS['card'],
                fg=COLORS['text'],
                font=FONTS['body_bold']
            ).pack(
                anchor='w',
                padx=20,
                pady=(4, 4)
            )

            tk.Label(
                card,
                text=self.item['notes'],
                bg=COLORS['card'],
                fg=COLORS['text_muted'],
                font=FONTS['body'],
                justify='left',
                wraplength=450
            ).pack(
                anchor='w',
                padx=20,
                pady=(0, 18)
            )

        # ----------------------------------------------------
        # Actions
        # ----------------------------------------------------

        actions = tk.Frame(
            content,
            bg=COLORS['bg']
        )

        actions.pack(
            fill='x',
            pady=(0, 12)
        )

        RoundedButton(
            actions,
            text="Edit Item",
            command=self._edit,
            bg=COLORS['primary'],
            width=110,
            height=36
        ).pack(
            side='left',
            padx=(0, 6)
        )

        RoundedButton(
            actions,
            text="Delete",
            command=self._delete,
            bg=COLORS['danger'],
            width=100,
            height=36
        ).pack(
            side='left'
        )

        # ----------------------------------------------------
        # History
        # ----------------------------------------------------

        history = get_history(
            self.item_id,
            limit=5
        )

        if history:

            history_card = tk.Frame(
                content,
                bg=COLORS['card'],
                highlightbackground=COLORS['border'],
                highlightthickness=1
            )

            history_card.pack(
                fill='x'
            )

            tk.Label(
                history_card,
                text="Location History",
                bg=COLORS['card'],
                fg=COLORS['text'],
                font=FONTS['body_bold']
            ).pack(
                anchor='w',
                padx=20,
                pady=(16, 10)
            )

            for record in history:

                text = (
                    f"{record['old_location']}  →  "
                    f"{record['new_location']}"
                )

                tk.Label(
                    history_card,
                    text=text,
                    bg=COLORS['card'],
                    fg=COLORS['text_muted'],
                    font=FONTS['small'],
                    wraplength=450,
                    justify='left'
                ).pack(
                    anchor='w',
                    padx=20,
                    pady=(0, 3)
                )

                tk.Label(
                    history_card,
                    text=record['changed_at'],
                    bg=COLORS['card'],
                    fg=COLORS['text_muted'],
                    font=('Segoe UI', 8)
                ).pack(
                    anchor='w',
                    padx=20,
                    pady=(0, 9)
                )

    # ========================================================
    # Detail Row
    # ========================================================

    def _detail_row(
        self,
        parent,
        label,
        value
    ):

        row = tk.Frame(
            parent,
            bg=COLORS['card']
        )

        row.pack(
            fill='x',
            pady=4
        )

        tk.Label(
            row,
            text=label,
            bg=COLORS['card'],
            fg=COLORS['text_muted'],
            font=FONTS['small'],
            width=12,
            anchor='w'
        ).pack(
            side='left'
        )

        tk.Label(
            row,
            text=value or '-',
            bg=COLORS['card'],
            fg=COLORS['text'],
            font=FONTS['body'],
            anchor='w',
            wraplength=360,
            justify='left'
        ).pack(
            side='left',
            fill='x',
            expand=True
        )

    # ========================================================
    # Photo
    # ========================================================

    def _display_photo(self, parent):

        path = self.item.get(
            'photo_path'
        )

        if not path:

            tk.Label(
                parent,
                text="📷",
                bg=COLORS['card'],
                fg=COLORS['text_muted'],
                font=('Segoe UI', 32)
            ).pack()

            return

        try:

            from PIL import Image, ImageTk

            image = Image.open(path)

            image.thumbnail(
                (140, 140)
            )

            photo = ImageTk.PhotoImage(
                image
            )

            label = tk.Label(
                parent,
                image=photo,
                bg=COLORS['card']
            )

            label.image = photo

            label.pack()

        except Exception:

            tk.Label(
                parent,
                text="📷",
                bg=COLORS['card'],
                fg=COLORS['text_muted'],
                font=('Segoe UI', 32)
            ).pack()

    # ========================================================
    # Edit
    # ========================================================

    def _edit(self):

        from views.add_edit import AddEditWindow

        self.destroy()

        AddEditWindow(
            self.controller,
            self.controller,
            item_id=self.item_id
        )

    # ========================================================
    # Delete
    # ========================================================

    def _delete(self):

        answer = messagebox.askyesno(
            "Delete Item",
            f"Delete '{self.item['name']}'?",
            parent=self
        )

        if not answer:
            return

        self.controller.delete_item(
            self.item_id
        )

        self.destroy()