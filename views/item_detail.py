"""Item detail view."""

import tkinter as tk
from theme import COLORS, FONTS
from database import get_item, get_history


class ItemDetailWindow(tk.Toplevel):
    def __init__(self, parent, controller, item_id):
        super().__init__(parent)
        self.controller = controller
        self.item_id = item_id
        self.title('Spot - Item Details')
        self.geometry('520x600')
        self.configure(bg=COLORS['bg'])
        self.minsize(400, 450)
        self.transient(parent)
        self.grab_set()

        self.item = get_item(item_id)
        if not self.item:
            self.destroy()
            return

        self._build()
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - 260
        y = self.winfo_screenheight() // 2 - 300
        self.geometry(f'520x600+{x}+{y}')

    def _build(self):
        canvas = tk.Canvas(self, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient='vertical', command=canvas.yview)
        content = tk.Frame(canvas, bg=COLORS['bg'])

        content.bind('<Configure>',
                     lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        window = canvas.create_window((0, 0), window=content, anchor='nw', width=490)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True, padx=16, pady=16)
        scrollbar.pack(side='right', fill='y')

        canvas.bind('<Configure>',
                    lambda e: canvas.itemconfig(window, width=max(e.width, 450)))
        canvas.bind_all('<MouseWheel>',
                        lambda e: canvas.yview_scroll(int(-e.delta / 120), 'units'))

        close_btn = tk.Label(self, text='✕', bg=COLORS['bg'],
                             fg=COLORS['text_muted'], font=('Segoe UI', 16),
                             cursor='hand2')
        close_btn.place(relx=1.0, x=-30, y=10, anchor='ne')
        close_btn.bind('<Button-1>', lambda e: self.destroy())

        photo_frame = tk.Frame(content, bg=COLORS['card'],
                               highlightbackground=COLORS['border'],
                               highlightthickness=1)
        photo_frame.pack(fill='x', pady=(0, 16))

        self.photo_label = tk.Label(photo_frame, bg=COLORS['card'],
                                    text='📷', font=('Segoe UI', 48))
        self.photo_label.pack(pady=30)
        self._detail_photo = None

        photo_path = self.item.get('photo_path')
        if photo_path:
            try:
                from PIL import Image, ImageTk
                img = Image.open(photo_path)
                img.thumbnail((300, 300))
                self._detail_photo = ImageTk.PhotoImage(img)
                self.photo_label.config(image=self._detail_photo, text='')
            except Exception:
                self.photo_label.config(
                    text='⚠ Image failed to load',
                    font=('Segoe UI', 12)
                )

        tk.Label(content, text=self.item['name'], bg=COLORS['bg'],
                 fg=COLORS['text'], font=('Segoe UI', 24, 'bold')).pack(anchor='w')

        status = self.item.get('status', 'stored')
        status_text = 'Available' if status == 'stored' else status.title()
        status_color = {
            'stored': '#2EB872',
            'lent': '#FF7A00',
            'borrowed': '#00A3FF',
            'lost': '#E53935'
        }.get(status, '#A5A8B2')

        tk.Label(content, text=status_text, bg=status_color, fg='white',
                 font=FONTS['small_bold'], padx=12, pady=4).pack(
                     anchor='w', pady=(8, 16))

        details = tk.Frame(content, bg=COLORS['bg'])
        details.pack(fill='x', pady=(0, 16))

        fields = [
            ('Category', self.item.get('category', 'General')),
            ('Location', f"{self.item.get('room', '')} → "
                         f"{self.item.get('container', '')}".rstrip(' →')),
            ('Person', self.item.get('person', '-')),
            ('Due Date', self.item.get('due_date', '-')),
            ('Added', self.item.get('date_added', '-')),
            ('Tags', self.item.get('tags', '-')),
        ]

        for i, (label, value) in enumerate(fields):
            tk.Label(details, text=label, bg=COLORS['bg'],
                     fg=COLORS['text_muted'],
                     font=FONTS['body_bold']).grid(
                         row=i, column=0, sticky='nw', pady=6, padx=(0, 20))
            tk.Label(details, text=value or '-', bg=COLORS['bg'],
                     fg=COLORS['text'], font=FONTS['body']).grid(
                         row=i, column=1, sticky='nw', pady=6)

        if self.item.get('notes'):
            tk.Label(content, text='Notes', bg=COLORS['bg'],
                     fg=COLORS['text'],
                     font=FONTS['heading']).pack(anchor='w', pady=(8, 4))
            tk.Label(content, text=self.item['notes'], bg=COLORS['card'],
                     fg=COLORS['text'], font=FONTS['body'],
                     wraplength=420, justify='left',
                     padx=12, pady=10).pack(fill='x', pady=(0, 16))

        tk.Label(content, text='History', bg=COLORS['bg'],
                 fg=COLORS['text'],
                 font=FONTS['heading']).pack(anchor='w', pady=(8, 4))

        history = get_history(self.item_id)

        if history:
            for h in history[:5]:
                h_frame = tk.Frame(content, bg=COLORS['card'],
                                   highlightbackground=COLORS['border'],
                                   highlightthickness=1)
                h_frame.pack(fill='x', pady=(0, 6))

                old = h.get('old_location', '')
                new = h.get('new_location', '')
                changed = h.get('changed_at', '')
                text = f"{old} → {new}" if old and new else (old or new or 'Updated')

                tk.Label(h_frame, text=text, bg=COLORS['card'],
                         fg=COLORS['text'],
                         font=FONTS['small']).pack(
                             anchor='w', padx=12, pady=8)
                tk.Label(h_frame, text=changed, bg=COLORS['card'],
                         fg=COLORS['text_muted'],
                         font=FONTS['small']).pack(
                             anchor='w', padx=12, pady=(0, 8))
        else:
            tk.Label(content, text='No history yet.', bg=COLORS['bg'],
                     fg=COLORS['text_muted'],
                     font=FONTS['body']).pack(pady=10)

        btn_frame = tk.Frame(content, bg=COLORS['bg'])
        btn_frame.pack(fill='x', pady=(16, 0))

        from components import RoundedButton

        # Show Mark Returned only for lent/borrowed items
        if status in ('lent', 'borrowed'):
            RoundedButton(
                btn_frame,
                text='Mark Returned',
                command=self._mark_returned,
                bg=COLORS['success'],
                width=120
            ).pack(side='left', padx=4)

        RoundedButton(
            btn_frame,
            text='Edit Item',
            command=self._edit,
            bg=COLORS['primary'],
            width=100
        ).pack(side='left', padx=4)

        RoundedButton(
            btn_frame,
            text='Delete',
            command=self._delete,
            bg=COLORS['danger'],
            width=100
        ).pack(side='left', padx=4)
    def _edit(self):
        from views.add_edit import AddEditWindow
        AddEditWindow(self.controller, self.controller, item_id=self.item_id)
        self.destroy()


    def _mark_returned(self):
        from database import update_item

        data = dict(self.item)
        data['status'] = 'stored'
        data['person'] = ''
        data['due_date'] = ''

        update_item(self.item_id, data)

        self.controller.toast.show(
            'Item marked as returned',
            'success'
        )

        self.controller.refresh_current_view()
        self.destroy()

    def _delete(self):
        from tkinter import messagebox
        if messagebox.askyesno('Delete Item', 'Move this item to trash?',
                               parent=self):
            from database import soft_delete_item
            soft_delete_item(self.item_id)
            self.controller.toast.show('Item moved to trash', 'warning')
            self.controller.refresh_current_view()
            self.destroy()