"""Add/Edit item modal form."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from theme import COLORS, FONTS
from components import RoundedButton
from database import add_item, update_item, get_item


class AddEditWindow(tk.Toplevel):

    def __init__(
        self,
        parent,
        controller,
        item_id=None,
        default_status='stored'
    ):

        super().__init__(parent)

        self.controller = controller
        self.item_id = item_id
        self.result_photo = ''

        self.title(
            'Edit Item' if item_id else 'Add New Item'
        )

        self.geometry(
            '480x620'
        )

        self.configure(
            bg=COLORS['bg']
        )

        self.minsize(
            360,
            500
        )

        self.transient(parent)
        self.grab_set()

        self._build_form(default_status)

        if item_id:
            self._load_data()

        self.center_window()

    # ====================================================
    # CENTER WINDOW
    # ====================================================

    def center_window(self):

        self.update_idletasks()

        width = 480
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
            f'{width}x{height}+{x}+{y}'
        )

    # ====================================================
    # FORM
    # ====================================================

    def _build_form(self, default_status):

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

        self.form_frame = tk.Frame(
            canvas,
            bg=COLORS['bg']
        )

        self.form_frame.bind(
            '<Configure>',
            lambda event:
            canvas.configure(
                scrollregion=canvas.bbox('all')
            )
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=self.form_frame,
            anchor='nw',
            width=450
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

        canvas.bind(
            '<Configure>',
            lambda event:
            canvas.itemconfig(
                canvas_window,
                width=max(event.width, 400)
            )
        )

        canvas.bind_all(
            '<MouseWheel>',
            lambda event:
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                'units'
            )
        )

        f = self.form_frame

        # ------------------------------------------------
        # Header
        # ------------------------------------------------

        tk.Label(
            f,
            text=(
                'Edit Item'
                if self.item_id
                else 'Add New Item'
            ),
            bg=COLORS['bg'],
            fg=COLORS['text'],
            font=FONTS['title']
        ).pack(
            anchor='w',
            pady=(0, 4)
        )

        tk.Label(
            f,
            text=(
                'Update your item information'
                if self.item_id
                else 'Add something to your inventory'
            ),
            bg=COLORS['bg'],
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(
            anchor='w',
            pady=(0, 12)
        )

        # ------------------------------------------------
        # Fields
        # ------------------------------------------------

        fields = [
            (
                'Item Name *',
                'name',
                'entry'
            ),
            (
                'Category',
                'cat',
                'combo',
                [
                    'General',
                    'Electronics',
                    'Clothes',
                    'Documents',
                    'Tools',
                    'Books',
                    'Kitchen',
                    'Sports',
                    'Seasonal'
                ]
            ),
            (
                'Room / Location *',
                'room',
                'combo',
                [
                    'Bedroom',
                    'Living Room',
                    'Kitchen',
                    'Office',
                    'Storage',
                    'Garage',
                    'Bathroom',
                    'Car'
                ]
            ),
            (
                'Container / Details',
                'container',
                'entry'
            ),
            (
                'Person (Lent/Borrowed)',
                'person',
                'entry'
            ),
            (
                'Due Date (YYYY-MM-DD HH:MM)',
                'due',
                'entry'
            ),
            (
                'Tags (comma separated)',
                'tags',
                'entry'
            )
        ]

        self.vars = {}

        for field in fields:

            label = field[0]
            key = field[1]
            widget_type = field[2]

            tk.Label(
                f,
                text=label,
                bg=COLORS['bg'],
                fg=COLORS['text'],
                font=FONTS['body_bold']
            ).pack(
                anchor='w',
                pady=(9, 3)
            )

            if widget_type == 'entry':

                var = tk.StringVar()

                self.vars[key] = var

                tk.Entry(
                    f,
                    textvariable=var,
                    font=FONTS['body'],
                    bg=COLORS['input_bg'],
                    fg=COLORS['text'],
                    insertbackground=COLORS['text'],
                    relief='flat',
                    highlightthickness=1,
                    highlightcolor=COLORS['primary'],
                    highlightbackground=COLORS['border']
                ).pack(
                    fill='x',
                    ipady=6
                )

            elif widget_type == 'combo':

                values = field[3]

                var = tk.StringVar(
                    value=values[0]
                )

                self.vars[key] = var

                combo = ttk.Combobox(
                    f,
                    textvariable=var,
                    values=values,
                    state='readonly',
                    font=FONTS['body']
                )

                combo.pack(
                    fill='x',
                    ipady=4
                )

        # ------------------------------------------------
        # Status
        # ------------------------------------------------

        tk.Label(
            f,
            text='Status',
            bg=COLORS['bg'],
            fg=COLORS['text'],
            font=FONTS['body_bold']
        ).pack(
            anchor='w',
            pady=(10, 4)
        )

        self.status_var = tk.StringVar(
            value=default_status
        )

        status_frame = tk.Frame(
            f,
            bg=COLORS['bg']
        )

        status_frame.pack(
            fill='x'
        )

        statuses = [
            ('stored', 'Available'),
            ('lent', 'Lent Out'),
            ('borrowed', 'Borrowed'),
            ('lost', 'Lost')
        ]

        for value, label in statuses:

            tk.Radiobutton(
                status_frame,
                text=label,
                variable=self.status_var,
                value=value,
                bg=COLORS['bg'],
                fg=COLORS['text'],
                activebackground=COLORS['bg'],
                activeforeground=COLORS['text'],
                selectcolor=COLORS['card'],
                font=FONTS['small']
            ).pack(
                side='left',
                padx=3
            )

        # ------------------------------------------------
        # Notes
        # ------------------------------------------------

        tk.Label(
            f,
            text='Notes',
            bg=COLORS['bg'],
            fg=COLORS['text'],
            font=FONTS['body_bold']
        ).pack(
            anchor='w',
            pady=(10, 3)
        )

        self.notes_text = tk.Text(
            f,
            height=3,
            font=FONTS['body'],
            bg=COLORS['input_bg'],
            fg=COLORS['text'],
            relief='flat',
            highlightthickness=1,
            highlightcolor=COLORS['primary'],
            highlightbackground=COLORS['border'],
            insertbackground=COLORS['text']
        )

        self.notes_text.pack(
            fill='x'
        )

        # ------------------------------------------------
        # Photo
        # ------------------------------------------------

        RoundedButton(
            f,
            text='Attach Photo',
            command=self._pick_photo,
            bg=COLORS['text_muted'],
            width=180
        ).pack(
            pady=12
        )

        self.photo_label = tk.Label(
            f,
            text='',
            bg=COLORS['bg'],
            fg=COLORS['text_muted'],
            font=FONTS['small']
        )

        self.photo_label.pack()

        # ------------------------------------------------
        # Buttons
        # ------------------------------------------------

        button_frame = tk.Frame(
            f,
            bg=COLORS['bg']
        )

        button_frame.pack(
            pady=16
        )

        RoundedButton(
            button_frame,
            text='Save',
            command=self._save,
            bg=COLORS['primary'],
            width=100
        ).pack(
            side='left',
            padx=4
        )

        RoundedButton(
            button_frame,
            text='Cancel',
            command=self.destroy,
            bg=COLORS['danger'],
            width=100
        ).pack(
            side='left',
            padx=4
        )

    # ====================================================
    # PHOTO
    # ====================================================

    def _pick_photo(self):

        path = filedialog.askopenfilename(
            title='Select Photo',
            filetypes=[
                (
                    'Images',
                    '*.png *.jpg *.jpeg *.gif *.bmp'
                )
            ]
        )

        if path:

            self.result_photo = path

            self.photo_label.config(
                text=f'Attached: {path.split("/")[-1]}',
                fg=COLORS['primary']
            )

    # ====================================================
    # LOAD DATA
    # ====================================================

    def _load_data(self):

        item = get_item(
            self.item_id
        )

        if not item:
            return

        self.vars['name'].set(
            item['name']
        )

        self.vars['cat'].set(
            item['category'] or 'General'
        )

        self.vars['room'].set(
            item['room'] or ''
        )

        self.vars['container'].set(
            item['container'] or ''
        )

        self.status_var.set(
            item['status'] or 'stored'
        )

        self.vars['person'].set(
            item['person'] or ''
        )

        self.vars['due'].set(
            item['due_date'] or ''
        )

        self.vars['tags'].set(
            item['tags'] or ''
        )

        self.notes_text.insert(
            '1.0',
            item['notes'] or ''
        )

        if item.get('photo_path'):

            self.result_photo = item['photo_path']

            self.photo_label.config(
                text=(
                    'Attached: '
                    + item['photo_path'].split('/')[-1]
                )
            )

    # ====================================================
    # SAVE
    # ====================================================

    def _save(self):

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
            'notes': self.notes_text.get(
                '1.0',
                'end'
            ).strip()
        }

        if self.item_id:

            update_item(
                self.item_id,
                data
            )

        else:

            add_item(
                data
            )

        self.controller.refresh_current_view()

        self.destroy()