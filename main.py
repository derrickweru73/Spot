"""Spot - Responsive desktop inventory application."""

import tkinter as tk
from tkinter import messagebox, filedialog

from theme import (
    COLORS,
    FONTS,
    BREAKPOINTS,
    toggle_dark_mode
)

from components import RoundedButton

from database import (
    delete_item,
    export_to_csv,
    get_stats
)

from views.dashboard import DashboardView
from views.stash_view import StashView
from views.lent_view import LentView
from views.borrowed_view import BorrowedView


class SpotApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Spot - Personal Inventory")
        self.geometry("1200x720")
        self.minsize(900, 600)

        self.current_view = None
        self.current_view_name = None

        self.configure(
            bg=COLORS['bg']
        )

        self._build_layout()
        self.show_view("dashboard")

    # ====================================================
    # MAIN LAYOUT
    # ====================================================

    def _build_layout(self):

        self.sidebar = tk.Frame(
            self,
            bg=COLORS['sidebar'],
            width=220
        )

        self.sidebar.pack(
            side='left',
            fill='y'
        )

        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(
            self,
            bg=COLORS['bg']
        )

        self.content.pack(
            side='right',
            fill='both',
            expand=True
        )

        self._build_sidebar()

        self.bind(
            '<Configure>',
            self._on_window_resize
        )

    # ====================================================
    # SIDEBAR
    # ====================================================

    def _build_sidebar(self):

        # ------------------------------------------------
        # Logo
        # ------------------------------------------------

        logo_frame = tk.Frame(
            self.sidebar,
            bg=COLORS['sidebar']
        )

        logo_frame.pack(
            fill='x',
            padx=20,
            pady=(24, 30)
        )

        tk.Label(
            logo_frame,
            text="SPOT",
            bg=COLORS['sidebar'],
            fg=COLORS['text'],
            font=FONTS['logo']
        ).pack(
            anchor='w'
        )

        tk.Label(
            logo_frame,
            text="Personal Inventory",
            bg=COLORS['sidebar'],
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(
            anchor='w',
            pady=(2, 0)
        )

        # ------------------------------------------------
        # Navigation
        # ------------------------------------------------

        nav_frame = tk.Frame(
            self.sidebar,
            bg=COLORS['sidebar']
        )

        nav_frame.pack(
            fill='x',
            padx=12
        )

        self.nav_buttons = {}

        self._create_nav_button(
            nav_frame,
            "▣",
            "Dashboard",
            "dashboard"
        )

        self._create_nav_button(
            nav_frame,
            "□",
            "Inventory",
            "stash"
        )

        self._create_nav_button(
            nav_frame,
            "↗",
            "Lent Out",
            "lent"
        )

        self._create_nav_button(
            nav_frame,
            "↙",
            "Borrowed",
            "borrowed"
        )

        # ------------------------------------------------
        # Bottom stats
        # ------------------------------------------------

        bottom = tk.Frame(
            self.sidebar,
            bg=COLORS['sidebar']
        )

        bottom.pack(
            side='bottom',
            fill='x',
            padx=16,
            pady=20
        )

        divider = tk.Frame(
            bottom,
            bg=COLORS['border'],
            height=1
        )

        divider.pack(
            fill='x',
            pady=(0, 14)
        )

        tk.Label(
            bottom,
            text="Total Items",
            bg=COLORS['sidebar'],
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(
            anchor='w'
        )

        self.total_items_label = tk.Label(
            bottom,
            text="0",
            bg=COLORS['sidebar'],
            fg=COLORS['text'],
            font=('Segoe UI', 22, 'bold')
        )

        self.total_items_label.pack(
            anchor='w',
            pady=(2, 0)
        )

        self._refresh_sidebar_stats()

    # ====================================================
    # NAVIGATION BUTTON
    # ====================================================

    def _create_nav_button(
        self,
        parent,
        icon,
        text,
        view_name
    ):

        button = tk.Frame(
            parent,
            bg=COLORS['sidebar'],
            height=42,
            cursor='hand2'
        )

        button.pack(
            fill='x',
            pady=3
        )

        button.pack_propagate(False)

        icon_label = tk.Label(
            button,
            text=icon,
            bg=COLORS['sidebar'],
            fg=COLORS['text_muted'],
            font=('Segoe UI', 12)
        )

        icon_label.pack(
            side='left',
            padx=(14, 10)
        )

        text_label = tk.Label(
            button,
            text=text,
            bg=COLORS['sidebar'],
            fg=COLORS['text_dark'],
            font=FONTS['body_bold']
        )

        text_label.pack(
            side='left'
        )

        self.nav_buttons[view_name] = (
            button,
            icon_label,
            text_label
        )

        for widget in (
            button,
            icon_label,
            text_label
        ):

            widget.bind(
                '<Button-1>',
                lambda event, v=view_name:
                self.show_view(v)
            )

            widget.bind(
                '<Enter>',
                lambda event, v=view_name:
                self._nav_hover(v, True)
            )

            widget.bind(
                '<Leave>',
                lambda event, v=view_name:
                self._nav_hover(v, False)
            )

    # ====================================================
    # NAVIGATION STYLING
    # ====================================================

    def _nav_hover(
        self,
        view_name,
        entering
    ):

        if self.current_view_name == view_name:
            return

        button, icon, label = self.nav_buttons[view_name]

        bg = (
            COLORS['sidebar_hover']
            if entering
            else COLORS['sidebar']
        )

        button.config(bg=bg)
        icon.config(bg=bg)
        label.config(bg=bg)

    def _set_active_nav(
        self,
        view_name
    ):

        for name, widgets in self.nav_buttons.items():

            button, icon, label = widgets

            if name == view_name:

                button.config(
                    bg=COLORS['primary']
                )

                icon.config(
                    bg=COLORS['primary'],
                    fg=COLORS['text_inverse']
                )

                label.config(
                    bg=COLORS['primary'],
                    fg=COLORS['text_inverse']
                )

            else:

                button.config(
                    bg=COLORS['sidebar']
                )

                icon.config(
                    bg=COLORS['sidebar'],
                    fg=COLORS['text_muted']
                )

                label.config(
                    bg=COLORS['sidebar'],
                    fg=COLORS['text_dark']
                )

    # ====================================================
    # VIEWS
    # ====================================================

    def show_view(
        self,
        view_name
    ):

        if self.current_view:

            self.current_view.destroy()

        view_classes = {
            'dashboard': DashboardView,
            'stash': StashView,
            'lent': LentView,
            'borrowed': BorrowedView
        }

        view_class = view_classes.get(
            view_name,
            DashboardView
        )

        self.current_view_name = view_name

        self.current_view = view_class(
            self.content,
            self
        )

        self.current_view.pack(
            fill='both',
            expand=True
        )

        self._set_active_nav(
            view_name
        )

        self._refresh_sidebar_stats()

    # ====================================================
    # DARK / LIGHT MODE
    # ====================================================

    def toggle_theme(self):

        toggle_dark_mode()

        # Update main window background
        self.configure(
            bg=COLORS['bg']
        )

        # Rebuild sidebar
        self.sidebar.destroy()

        self.sidebar = tk.Frame(
            self,
            bg=COLORS['sidebar'],
            width=220
        )

        self.sidebar.pack(
            side='left',
            fill='y'
        )

        self.sidebar.pack_propagate(False)

        self._build_sidebar()

        # Rebuild current view
        if self.current_view:
            self.current_view.destroy()

        view_classes = {
            'dashboard': DashboardView,
            'stash': StashView,
            'lent': LentView,
            'borrowed': BorrowedView
        }

        view_class = view_classes.get(
            self.current_view_name,
            DashboardView
        )

        self.current_view = view_class(
            self.content,
            self
        )

        self.current_view.pack(
            fill='both',
            expand=True
        )

        self._set_active_nav(
            self.current_view_name
        )

        self._refresh_sidebar_stats()

    # ====================================================
    # ADD / EDIT
    # ====================================================

    def open_add(
        self,
        default_status='stored'
    ):

        from views.add_edit import AddEditWindow

        AddEditWindow(
            self,
            self,
            default_status=default_status
        )

    # ====================================================
    # ITEM DETAIL
    # ====================================================

    def open_detail(
        self,
        item
    ):

        from views.item_detail import ItemDetailWindow

        ItemDetailWindow(
            self,
            self,
            item['id']
        )

    # ====================================================
    # REFRESH
    # ====================================================

    def refresh_current_view(self):

        if (
            self.current_view
            and hasattr(
                self.current_view,
                'refresh'
            )
        ):

            self.current_view.refresh()

        self._refresh_sidebar_stats()

    def _refresh_sidebar_stats(self):

        try:

            stats = get_stats()

            self.total_items_label.config(
                text=str(
                    stats['total']
                ),
                fg=COLORS['text']
            )

        except Exception:

            self.total_items_label.config(
                text="0",
                fg=COLORS['text']
            )

    # ====================================================
    # DELETE
    # ====================================================

    def delete_item(
        self,
        item_id
    ):

        answer = messagebox.askyesno(
            "Delete Item",
            "Are you sure you want to delete this item?"
        )

        if not answer:
            return

        delete_item(
            item_id
        )

        self.refresh_current_view()

    # ====================================================
    # EXPORT
    # ====================================================

    def export_items(self):

        filepath = filedialog.asksaveasfilename(
            title="Export Inventory",
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )

        if not filepath:
            return

        try:

            export_to_csv(
                filepath
            )

            messagebox.showinfo(
                "Export Complete",
                "Inventory exported successfully."
            )

        except Exception as exc:

            messagebox.showerror(
                "Export Failed",
                f"Could not export inventory:\n\n{exc}"
            )

    # ====================================================
    # RESPONSIVE SIDEBAR
    # ====================================================

    def _on_window_resize(
        self,
        event
    ):

        if event.widget != self:
            return

        width = self.winfo_width()

        if width < BREAKPOINTS['md']:

            self.sidebar.config(
                width=190
            )

        else:

            self.sidebar.config(
                width=220
            )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app = SpotApp()
    app.mainloop()