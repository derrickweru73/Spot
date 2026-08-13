"""Add/Edit item modal form."""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from theme import COLORS, FONTS
from components import RoundedButton
from database import add_item, update_item, get_item


class AddEditWindow(tk.Toplevel):
    def __init__(self, parent, controller, item_id=None, default_status='stored'):
        super().__init__(parent)
        self.controller = controller
        self.item_id = item_id
        self.result_photo = ''
        self.title('Edit Item' if item_id else 'Add New Item')
        self.geometry('480x620')
        self.configure(bg=COLORS['bg'])
        self.minsize(360, 500)
        self.transient(parent)
        self.grab_set()
        self._build_form(default_status)

        if item_id:
            self._load_data()

        self.center_window()

    def center_window(self):
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - 240
        y = self.winfo_screenheight() // 2 - 310
        self.geometry(f'480x620+{x}+{y}')

    def _build_form(self, default_status):
        canvas = tk.Canvas(self, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient='vertical', command=canvas.yview)
        self.form_frame = tk.Frame(canvas, bg=COLORS['bg'])

        self.form_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        canvas_window = canvas.create_window(
            (0, 0), window=self.form_frame, anchor='nw', width=450
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True, padx=12, pady=12)
        scrollbar.pack(side='right', fill='y')

        canvas.bind(
            '<Configure>',
            lambda e: canvas.itemconfig(canvas_window, width=max(e.width, 400))
        )
        canvas.bind_all(
            '<MouseWheel>',
            lambda e: canvas.yview_scroll(int(-e.delta / 120), 'units')
        )

        f = self.form_frame

        tk.Label(
            f,
            text='Edit Item' if self.item_id else 'Add New Item',
            bg=COLORS['bg'], fg=COLORS['text'], font=FONTS['title']
        ).pack(anchor='w', pady=(0, 4))

        tk.Label(
            f,
            text='Update your item information' if self.item_id
            else 'Add something to your inventory',
            bg=COLORS['bg'], fg=COLORS['text_muted'], font=FONTS['small']
        ).pack(anchor='w', pady=(0, 12))

        fields = [
            ('Item Name *', 'name', 'entry'),
            ('Category', 'cat', 'combo',
            ['General', 'Electronics', 'Clothes', 'Documents',
            'Tools', 'Books', 'Kitchen', 'Sports', 'Seasonal',
            'Laundry', 'Gym Equipment', 'Jewelry', 'Baby Items',
            'Camping', 'Other']),
            
            ('Room / Location *', 'room', 'combo',
            ['Bedroom', 'Living Room', 'Kitchen', 'Office',
            'Storage Room', 'Garage', 'Bathroom', 'Car',
            'Laundry Room', 'Gym', 'Basement', 'Attic',
            'Balcony', 'Garden', 'Shed', 'Workshop']),

            ('Container / Details', 'container', 'entry'),
            ('Person (Lent/Borrowed)', 'person', 'entry'),
            ('Due Date (YYYY-MM-DD HH:MM)', 'due', 'entry'),
            ('Tags (comma separated)', 'tags', 'entry')
        ]

        self.vars = {}

        for field in fields:
            label, key, widget_type = field[:3]

            tk.Label(
                f, text=label, bg=COLORS['bg'],
                fg=COLORS['text'], font=FONTS['body_bold']
            ).pack(anchor='w', pady=(9, 3))

            var = tk.StringVar()
            self.vars[key] = var

            if widget_type == 'entry':
                tk.Entry(
                    f, textvariable=var, font=FONTS['body'],
                    bg=COLORS['input_bg'], fg=COLORS['text'],
                    insertbackground=COLORS['text'], relief='flat',
                    highlightthickness=1,
                    highlightcolor=COLORS['primary'],
                    highlightbackground=COLORS['border']
                ).pack(fill='x', ipady=6)

            else:
                ttk.Combobox(
                    f, textvariable=var, values=field[3],
                    state='normal', font=FONTS['body']
                ).pack(fill='x', ipady=4)
                var.set(field[3][0])

        tk.Label(
            f, text='Status', bg=COLORS['bg'],
            fg=COLORS['text'], font=FONTS['body_bold']
        ).pack(anchor='w', pady=(10, 4))

        self.status_var = tk.StringVar(value=default_status)
        status_frame = tk.Frame(f, bg=COLORS['bg'])
        status_frame.pack(fill='x')

        for value, label in [
            ('stored', 'Available'),
            ('lent', 'Lent Out'),
            ('borrowed', 'Borrowed'),
            ('lost', 'Lost')
        ]:
            tk.Radiobutton(
                status_frame, text=label, variable=self.status_var,
                value=value, bg=COLORS['bg'], fg=COLORS['text'],
                activebackground=COLORS['bg'],
                activeforeground=COLORS['text'],
                selectcolor=COLORS['card'],
                font=FONTS['small']
            ).pack(side='left', padx=3)

        tk.Label(
            f, text='Notes', bg=COLORS['bg'],
            fg=COLORS['text'], font=FONTS['body_bold']
        ).pack(anchor='w', pady=(10, 3))

        self.notes_text = tk.Text(
            f, height=3, font=FONTS['body'],
            bg=COLORS['input_bg'], fg=COLORS['text'],
            relief='flat', highlightthickness=1,
            highlightcolor=COLORS['primary'],
            highlightbackground=COLORS['border'],
            insertbackground=COLORS['text']
        )
        self.notes_text.pack(fill='x')

        RoundedButton(
            f, text='Attach Photo', command=self._pick_photo,
            bg=COLORS['text_muted'], width=180
        ).pack(pady=12)

        self.photo_label = tk.Label(
            f, text='', bg=COLORS['bg'],
            fg=COLORS['text_muted'], font=FONTS['small']
        )
        self.photo_label.pack()

        button_frame = tk.Frame(f, bg=COLORS['bg'])
        button_frame.pack(pady=16)

        RoundedButton(
            button_frame, text='Save', command=self._save,
            bg=COLORS['primary'], width=100
        ).pack(side='left', padx=4)

        RoundedButton(
            button_frame, text='Cancel', command=self.destroy,
            bg=COLORS['danger'], width=100
        ).pack(side='left', padx=4)

    def _pick_photo(self):
        path = filedialog.askopenfilename(
            title='Select Photo',
            filetypes=[('Images', '*.png *.jpg *.jpeg *.gif *.bmp')]
        )

        if not path:
            return

        self.result_photo = path
        filename = os.path.basename(path)
        self.photo_label.config(
            text=f'Attached: {filename}',
            fg=COLORS['primary']
        )

        if hasattr(self, '_photo_preview') and self._photo_preview.winfo_exists():
            self._photo_preview.destroy()

        try:
            from PIL import Image, ImageTk
            img = Image.open(path)
            img.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(img)

            self._photo_preview = tk.Label(
                self.form_frame, image=photo, bg=COLORS['bg']
            )
            self._photo_preview.image = photo
            self._photo_preview.pack(pady=(0, 8))

        except Exception as exc:
            messagebox.showerror(
                'Photo Error',
                f'Could not attach photo:\n\n{exc}',
                parent=self
            )

    def _load_data(self):
        item = get_item(self.item_id)

        if not item:
            return

        self.vars['name'].set(item['name'])
        self.vars['cat'].set(item['category'] or 'General')
        self.vars['room'].set(item['room'] or '')
        self.vars['container'].set(item['container'] or '')
        self.vars['person'].set(item['person'] or '')
        self.vars['due'].set(item['due_date'] or '')
        self.vars['tags'].set(item['tags'] or '')
        self.status_var.set(item['status'] or 'stored')
        self.notes_text.insert('1.0', item['notes'] or '')

        if item.get('photo_path'):
            self.result_photo = item['photo_path']
            filename = os.path.basename(item['photo_path'])
            self.photo_label.config(
                text=f'Attached: {filename}',
                fg=COLORS['primary']
            )

            try:
                from PIL import Image, ImageTk
                img = Image.open(item['photo_path'])
                img.thumbnail((100, 100))
                photo = ImageTk.PhotoImage(img)

                self._photo_preview = tk.Label(
                    self.form_frame, image=photo, bg=COLORS['bg']
                )
                self._photo_preview.image = photo
                self._photo_preview.pack(pady=(0, 8))

            except Exception:
                pass

    def _save(self):
        try:
            name = self.vars['name'].get().strip()
            room = self.vars['room'].get().strip()

            if not name or not room:
                messagebox.showerror(
                    'Required',
                    'Name and Room are required.',
                    parent=self
                )
                return

            data = {
                'name': name,
                'category': self.vars['cat'].get(),
                'room': room,
                'container': self.vars['container'].get().strip(),
                'status': self.status_var.get(),
                'person': self.vars['person'].get().strip(),
                'due_date': self.vars['due'].get().strip(),
                'photo_path': self.result_photo,
                'tags': self.vars['tags'].get().strip(),
                'notes': self.notes_text.get('1.0', 'end').strip()
            }

            if self.item_id:
                update_item(self.item_id, data)
            else:
                add_item(data)

            self.controller.refresh_current_view()
            self.destroy()

        except Exception as exc:
            messagebox.showerror(
                'Save Error',
                f'Could not save item:\n\n{exc}',
                parent=self
            )