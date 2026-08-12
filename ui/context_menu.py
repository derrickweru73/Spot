"""Right-click context menus."""

import tkinter as tk
from theme import COLORS, FONTS


class ItemContextMenu:
    def __init__(self, parent, controller, item):
        self.controller = controller
        self.item = item
        self.menu = tk.Menu(parent, tearoff=0, bg=COLORS["card"],
                            fg=COLORS["text"], activebackground=COLORS["primary"],
                            activeforeground="white", font=FONTS["small"],
                            relief="flat", borderwidth=0)
        self._build()

    def _build(self):
        status = self.item.get("status", "stored")
        self.menu.add_command(label="View Details", command=self._view)
        self.menu.add_command(label="Edit Item", command=self._edit)
        self.menu.add_separator()
        if status in ("lent", "borrowed"):
            self.menu.add_command(label="Mark Returned", command=self._mark_returned)
        self.menu.add_command(label="Move to Trash", command=self._trash)
        self.menu.add_separator()
        self.menu.add_command(label="Copy Name", command=self._copy_name)

    def show(self, event):
        self.menu.post(event.x_root, event.y_root)

    def _view(self):
        self.controller.open_detail(self.item)

    def _edit(self):
        from views.add_edit import AddEditWindow
        AddEditWindow(self.controller, self.controller, item_id=self.item["id"])

    def _mark_returned(self):
        from database import update_item
        data = dict(self.item)
        data["status"] = "stored"
        data["person"] = ""
        data["due_date"] = ""
        update_item(self.item["id"], data)
        self.controller.refresh_current_view()
        self.controller.toast.show("Item marked as returned", "success")

    def _trash(self):
        from database import soft_delete_item
        soft_delete_item(self.item["id"])
        self.controller.refresh_current_view()
        self.controller.toast.show(f"'{self.item['name']}' moved to trash", "warning")

    def _copy_name(self):
        self.controller.clipboard_clear()
        self.controller.clipboard_append(self.item.get("name", ""))
        self.controller.toast.show("Item name copied to clipboard", "info")