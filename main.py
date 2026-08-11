"""Spot - App entry point with sidebar navigation and view routing."""

import tkinter as tk
from tkinter import messagebox, filedialog
from theme import COLORS, FONTS, BREAKPOINTS
from components import RoundedButton
from database import delete_item, export_to_csv, get_stats

from views.dashboard import DashboardView
from views.stash_view import StashView
from views.lent_view import LentView
from views.borrowed_view import BorrowedView
from views.add_edit import AddEditWindow


class SpotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spot - Never Lose Your Stuff Again")
        self.root.geometry("1100x750")
        self.root.minsize(500, 400)
        self.root.configure(bg=COLORS['bg'])

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=COLORS['sidebar'], width=220)
        self.sidebar.grid(row=0, column=0, sticky='nsew')
        self.sidebar.grid_propagate(False)
        self._build_sidebar()

        # Content area
        self.content = tk.Frame(self.root, bg=COLORS['bg'])
        self.content.grid(row=0, column=1, sticky='nsew')
        self.content.grid_rowconfigure(0, weight=0)
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_rowconfigure(2, weight=0)
        self.content.grid_columnconfigure(0, weight=1)

        # Mobile header (hidden by default)
        self.mobile_header = tk.Frame(self.content, bg=COLORS['sidebar'], height=50)
        self.mobile_header.grid(row=0, column=0, sticky='new')
        self.mobile_header.grid_remove()
        
        self.ham_btn = tk.Label(self.mobile_header, text='☰', bg=COLORS['sidebar'],
                                fg=COLORS['text'], font=('Segoe UI', 16), cursor='hand2')
        self.ham_btn.pack(side='left', padx=15)
        self.ham_btn.bind('<Button-1>', lambda e: self._toggle_sidebar())
        
        tk.Label(self.mobile_header, text='Spot', bg=COLORS['sidebar'],
                 fg=COLORS['text'], font=FONTS['heading']).pack(side='left')

        # View container
        self.view_container = tk.Frame(self.content, bg=COLORS['bg'])
        self.view_container.grid(row=1, column=0, sticky='nsew')
        self.view_container.grid_rowconfigure(0, weight=1)
        self.view_container.grid_columnconfigure(0, weight=1)

        # Status bar
        self.status_bar = tk.Frame(self.content, height=28, bg=COLORS['sidebar'])
        self.status_bar.grid(row=2, column=0, sticky='sew')
        self.status_bar.grid_propagate(False)
        
        tk.Label(self.status_bar, text="Spot v1.0.0", bg=COLORS['sidebar'],
                 font=FONTS['small'], fg=COLORS['text_muted']).pack(side='left', padx=12)
        dot = tk.Canvas(self.status_bar, width=8, height=8, bg=COLORS['sidebar'],
                        highlightthickness=0)
        dot.pack(side='left')
        dot.create_oval(0, 0, 8, 8, fill=COLORS['success'], outline='')
        tk.Label(self.status_bar, text="All systems ready", bg=COLORS['sidebar'],
                 font=FONTS['small'], fg=COLORS['text_muted']).pack(side='left', padx=5)

        self.current_view = None
        self.view_instance = None
        self.sidebar_visible = True

        self.show_view("dash")
        self.root.bind('<Configure>', self._on_root_resize)

    def _build_sidebar(self):
        logo = tk.Frame(self.sidebar, bg=COLORS['sidebar'])
        logo.pack(fill='x', pady=(25, 5), padx=20)
        
        pin = tk.Canvas(logo, width=32, height=32, bg=COLORS['sidebar'], highlightthickness=0)
        pin.pack(side='left')
        pin.create_oval(4, 2, 28, 26, fill=COLORS['secondary'], outline='')
        pin.create_polygon([16, 30, 8, 20, 24, 20], fill=COLORS['secondary'], outline='')
        
        tk.Label(logo, text="SPOT", bg=COLORS['sidebar'],
                 font=FONTS['logo'], fg=COLORS['text']).pack(side='left', padx=(10, 0))
        tk.Label(self.sidebar, text="Never Lose Your Stuff Again", bg=COLORS['sidebar'],
                 font=FONTS['small'], fg=COLORS['text_muted']).pack(anchor='w', padx=20, pady=(0, 25))

        self.nav_buttons = []
        for text, key in [("Dashboard", "dash"), ("My Items", "stash"),
                          ("Lent Out", "lent"), ("Borrowed", "borrowed")]:
            btn = tk.Label(self.sidebar, text=text, bg=COLORS['sidebar'],
                           fg=COLORS['text_muted'], font=FONTS['body_bold'],
                           padx=20, pady=12, anchor='w', cursor='hand2')
            btn.pack(fill='x')
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=COLORS['sidebar_hover']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=COLORS['sidebar']))
            btn.bind('<Button-1>', lambda e, k=key: self.show_view(k))
            btn.key = key
            self.nav_buttons.append(btn)

        self._build_storage_indicator()

    def _build_storage_indicator(self):
        for w in self.sidebar.winfo_children():
            if getattr(w, '_is_storage', False):
                w.destroy()

        stats = get_stats()
        frame = tk.Frame(self.sidebar, bg=COLORS['sidebar_active'], padx=15, pady=15)
        frame._is_storage = True
        frame.pack(fill='x', padx=15, pady=(20, 15), side='bottom')
        
        tk.Label(frame, text="Total Items", bg=COLORS['sidebar_active'],
                 font=FONTS['small'], fg=COLORS['text_muted']).pack(anchor='w')
        tk.Label(frame, text=str(stats['total']), bg=COLORS['sidebar_active'],
                 font=('Segoe UI', 18, 'bold'), fg=COLORS['primary']).pack(anchor='w')
        
        bar = tk.Frame(frame, height=4, bg=COLORS['sidebar'])
        bar.pack(fill='x', pady=(10, 5))
        fill = tk.Frame(bar, height=4, bg=COLORS['primary'])
        fill.pack(side='left')
        fill.config(width=60)

    def _on_root_resize(self, event=None):
        w = self.root.winfo_width()
        
        if w < BREAKPOINTS['md'] and self.sidebar_visible:
            self.sidebar.grid_remove()
            self.mobile_header.grid()
            self.sidebar_visible = False
        elif w >= BREAKPOINTS['md'] and not self.sidebar_visible:
            self.sidebar.grid()
            self.mobile_header.grid_remove()
            self.sidebar_visible = True

    def _toggle_sidebar(self):
        if self.sidebar.winfo_viewable():
            self.sidebar.grid_remove()
        else:
            self.sidebar.grid()

    def show_view(self, view_name):
        self.current_view = view_name
        
        for btn in self.nav_buttons:
            if btn.key == view_name:
                btn.config(bg=COLORS['sidebar_active'], fg=COLORS['text'])
            else:
                btn.config(bg=COLORS['sidebar'], fg=COLORS['text_muted'])

        for w in self.view_container.winfo_children():
            w.destroy()

        if view_name == "dash":
            self.view_instance = DashboardView(self.view_container, self)
        elif view_name == "stash":
            self.view_instance = StashView(self.view_container, self)
        elif view_name == "lent":
            self.view_instance = LentView(self.view_container, self)
        elif view_name == "borrowed":
            self.view_instance = BorrowedView(self.view_container, self)

        self.view_instance.grid(row=0, column=0, sticky='nsew')

    def refresh_current_view(self):
        if self.view_instance and hasattr(self.view_instance, 'refresh'):
            self.view_instance.refresh()
        self._build_storage_indicator()

    def open_add(self, default_status='stored'):
        AddEditWindow(self.root, self, default_status=default_status)

    def open_detail(self, item):
        popup = tk.Toplevel(self.root)
        popup.title(item['name'])
        popup.geometry("420x520")
        popup.minsize(320, 400)
        popup.configure(bg=COLORS['bg'])
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(popup, text=item['name'], bg=COLORS['bg'],
                 font=FONTS['title'], fg=COLORS['text']).pack(anchor='w', padx=20, pady=(20, 5))

        from components import StatusBadge
        status_text = 'Available' if item['status'] == 'stored' else item['status'].title()
        StatusBadge(popup, status_text).pack(anchor='w', padx=20)

        details = [
            f"Location: {item['room']}" + (f" → {item['container']}" if item.get('container') else ''),
            f"Category: {item.get('category', 'General')}",
        ]
        if item.get('person'):
            details.append(f"Person: {item['person']}")
        if item.get('due_date'):
            details.append(f"Due Date: {item['due_date']}")
        if item.get('tags'):
            details.append(f"Tags: {item['tags']}")

        for d in details:
            tk.Label(popup, text=d, bg=COLORS['bg'], font=FONTS['body'],
                     fg=COLORS['text_muted']).pack(anchor='w', padx=20, pady=2)

        if item.get('photo_path'):
            try:
                from PIL import Image, ImageTk
                img = Image.open(item['photo_path'])
                img.thumbnail((280, 180))
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(popup, image=photo, bg=COLORS['bg'])
                lbl.image = photo
                lbl.pack(pady=10)
            except Exception:
                pass

        tk.Label(popup, text="Move History", bg=COLORS['bg'],
                 font=FONTS['heading'], fg=COLORS['text']).pack(anchor='w', padx=20, pady=(15, 5))

        from database import get_history
        history = get_history(item['id'])

        hf = tk.Frame(popup, bg=COLORS['bg'])
        hf.pack(fill='x', padx=20, pady=5)

        if not history:
            tk.Label(hf, text="No history yet.", bg=COLORS['bg'],
                     font=FONTS['small'], fg=COLORS['text_muted']).pack()
        else:
            for h in history:
                text = f"{h['changed_at']}: {h['old_location']} → {h['new_location']}"
                tk.Label(hf, text=text, bg=COLORS['bg'],
                         font=FONTS['small'], fg=COLORS['text_muted']).pack(anchor='w', pady=1)

        bf = tk.Frame(popup, bg=COLORS['bg'])
        bf.pack(pady=16)
        RoundedButton(bf, text="Edit", width=80,
                      command=lambda: [popup.destroy(), self._edit_item(item['id'])]).pack(side='left', padx=4)
        RoundedButton(bf, text="Delete", width=80, bg=COLORS['danger'],
                      command=lambda: self._confirm_delete(item['id'], popup)).pack(side='left', padx=4)
        if item['status'] in ('lent', 'borrowed'):
            RoundedButton(bf, text="Mark Returned", width=130, bg=COLORS['success'],
                          command=lambda: self._mark_returned(item['id'], popup)).pack(side='left', padx=4)

    def _edit_item(self, item_id):
        AddEditWindow(self.root, self, item_id=item_id)

    def _confirm_delete(self, item_id, popup):
        if messagebox.askyesno("Confirm", "Delete this item permanently?"):
            delete_item(item_id)
            popup.destroy()
            self.refresh_current_view()

    def _mark_returned(self, item_id, popup):
        from database import get_item, update_item
        item = get_item(item_id)
        if item:
            item['status'] = 'stored'
            item['person'] = ''
            item['due_date'] = ''
            update_item(item_id, item)
            popup.destroy()
            self.refresh_current_view()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv',
            filetypes=[("CSV files", "*.csv")], title="Export Inventory")
        if path:
            export_to_csv(path)
            messagebox.showinfo("Exported", f"Saved to:\n{path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpotApp(root)
    root.mainloop()