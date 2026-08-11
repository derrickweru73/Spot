"""Item detail view for Spot."""

import tkinter as tk
from tkinter import messagebox

from theme import COLORS, FONTS
from components import RoundedButton, StatusBadge
from database import get_item, delete_item


class ItemDetailWindow(tk.Toplevel):

    def __init__(self, parent, controller, item):

        super().__init__(parent)

        self.controller = controller
        self.item_id = item['id']

        self.title("Item Details")
        self.geometry("520x620")
        self.configure(bg=COLORS['bg'])
        self.minsize(420, 500)

        self.transient(parent)
        self.grab_set()

        self._build(item)
        self._center()

    # ====================================================
    # CENTER WINDOW
    # ====================================================

    def _center(self):

        self.update_idletasks()

        width = 520
        height = 620

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

    # ====================================================
    # BUILD
    # ====================================================

    def _build(self, item):

        # ------------------------------------------------
        # Main scrollable area
        # ------------------------------------------------

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
            padx=12,
            pady=12
        )

        scrollbar.pack(
            side='right',
            fill='y'
        )

        # ------------------------------------------------
        # Header
        # ------------------------------------------------

        header = tk.Frame(
            content,
            bg=COLORS['bg']
        )

        header.pack(
            fill='x',
            padx=12,
            pady=(5, 18)
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

        # ------------------------------------------------
        # Card
        # ------------------------------------------------

        card = tk.Frame(
            content,
            bg=COLORS['card'],
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )

        card.pack(
            fill='x',
            padx=12
        )

        # ------------------------------------------------
        # Photo
        # ------------------------------------------------

        photo_frame = tk.Frame(
            card,
            bg=COLORS['card']
        )

        photo_frame.pack(
            fill='x',
            pady=(20, 8)
        )

        photo = item.get('photo_path')

        if photo:

            try:

                from PIL import Image, ImageTk

                image = Image.open(photo)
                image.thumbnail((150, 150))

                image_tk = ImageTk.PhotoImage(
                    image
                )

                image_label = tk.Label(
                    photo_frame,
                    image=image_tk,
                    bg=COLORS['card']
                )

                image_label.image = image_tk

                image_label.pack()

            except Exception:

                self._photo_placeholder(
                    photo_frame
                )

        else:

            self._photo_placeholder(
                photo_frame
            )

        # ------------------------------------------------
        # Item name
        # ------------------------------------------------

        tk.Label(
            card,
            text=item['name'],
            bg=COLORS['card'],
            fg=COLORS['text'],
            font=('Segoe UI', 20, 'bold')
        ).pack(
            pady=(8, 4)
        )

        # ------------------------------------------------
        # Status
        # ------------------------------------------------

        status = item.get(
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
            height=24
        ).pack(
            pady=(0, 18)
        )

        # ------------------------------------------------
        # Details
        # ------------------------------------------------

        details = tk.Frame(
            card,
            bg=COLORS['card']
        )

        details.pack(
            fill='x',
            padx=22,
            pady=(0, 15)
        )

        self._detail_row(
            details,
            "Category",
            item.get('category') or 'General'
        )

        location = item.get('room') or ''

        if item.get('container'):
            location += (
                f" → {item['container']}"
            )

        self._detail_row(
            details,
            "Location",
            location
        )

        if item.get('person'):

            self._detail_row(
                details,
                "Person",
                item['person']
            )

        if item.get('due_date'):

            self._detail_row(
                details,
                "Due Date",
                item['due_date']
            )

        if item.get('date_added'):

            self._detail_row(
                details,
                "Added",
                item['date_added']
            )

        if item.get('tags'):

            self._detail_row(
                details,
                "Tags",
                item['tags']
            )

        # ------------------------------------------------
        # Notes
        # ------------------------------------------------

        if item.get('notes'):

            tk.Label(
                details,
                text="Notes",
                bg=COLORS['card'],
                fg=COLORS['text'],
                font=FONTS['body_bold']
            ).pack(
                anchor='w',
                pady=(12, 3)
            )

            tk.Label(
                details,
                text=item['notes'],
                bg=COLORS['card'],
                fg=COLORS['text_muted'],
                font=FONTS['body'],
                justify='left',
                wraplength=430
            ).pack(
                anchor='w'
            )

        # ------------------------------------------------
        # Buttons
        # ------------------------------------------------

        buttons = tk.Frame(
            content,
            bg=COLORS['bg']
        )

        buttons.pack(
            pady=18
        )

        RoundedButton(
            buttons,
            text="Edit",
            command=self._edit,
            bg=COLORS['primary'],
            width=100
        ).pack(
            side='left',
            padx=5
        )

        RoundedButton(
            buttons,
            text="Delete",
            command=self._delete,
            bg=COLORS['danger'],
            width=100
        ).pack(
            side='left',
            padx=5
        )

        RoundedButton(
            buttons,
            text="Close",
            command=self.destroy,
            bg=COLORS['text_muted'],
            width=100
        ).pack(
            side='left',
            padx=5
        )

    # ====================================================
    # PHOTO PLACEHOLDER
    # ====================================================

    def _photo_placeholder(self, parent):

        tk.Label(
            parent,
            text="📷",
            bg=COLORS['input_bg'],
            fg=COLORS['text_muted'],
            font=('Segoe UI', 36),
            width=5,
            height=2
        ).pack()

    # ====================================================
    # DETAIL ROW
    # ====================================================

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
            pady=5
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
            text=str(value),
            bg=COLORS['card'],
            fg=COLORS['text'],
            font=FONTS['body'],
            anchor='w',
            wraplength=330
        ).pack(
            side='left',
            fill='x',
            expand=True
        )

    # ====================================================
    # EDIT
    # ====================================================

    def _edit(self):

        from views.add_edit import AddEditWindow

        AddEditWindow(
            self,
            self.controller,
            item_id=self.item_id
        )

        self.destroy()

    # ====================================================
    # DELETE
    # ====================================================

    def _delete(self):

        answer = messagebox.askyesno(
            "Delete Item",
            "Are you sure you want to delete this item?",
            parent=self
        )

        if not answer:
            return

        delete_item(
            self.item_id
        )

        self.controller.refresh_current_view()

        self.destroy()