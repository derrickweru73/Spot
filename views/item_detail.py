"""Item detail view."""

import tkinter as tk
from theme import COLORS, FONTS
from database import get_item, get_history


class ItemDetailWindow(tk.Toplevel):
    def __init__(self, parent, controller, item_id):
        super().__init__(parent)
        self.controller = controller
        self.item_id = item_id
        self.item = get_item(item_id)

        if not self.item:
            self.destroy()
            return

        self.title("Spot - Item Details")
        self.geometry("520x600")
        self.minsize(400, 450)
        self.configure(bg=COLORS["bg"])
        self.transient(parent)
        self.grab_set()

        self._build()
        self._center()

    def _center(self):
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - 260
        y = self.winfo_screenheight() // 2 - 300
        self.geometry(f"520x600+{x}+{y}")

    def _build(self):
        canvas = tk.Canvas(
            self, bg=COLORS["bg"], highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            self, orient="vertical", command=canvas.yview
        )
        content = tk.Frame(canvas, bg=COLORS["bg"])

        content.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        window = canvas.create_window(
            (0, 0), window=content, anchor="nw", width=490
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(
            side="left", fill="both", expand=True,
            padx=16, pady=16
        )
        scrollbar.pack(side="right", fill="y")

        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(
                window, width=max(e.width, 450)
            )
        )
        canvas.bind(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(
                int(-e.delta / 120), "units"
            )
        )

        close = tk.Label(
            self, text="✕", bg=COLORS["bg"],
            fg=COLORS["text_muted"],
            font=("Segoe UI", 16), cursor="hand2"
        )
        close.place(relx=1, x=-30, y=10, anchor="ne")
        close.bind("<Button-1>", lambda e: self.destroy())

        self._photo(content)
        self._details(content)
        self._history(content)
        self._buttons(content)

    def _photo(self, parent):
        frame = tk.Frame(
            parent, bg=COLORS["card"],
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        frame.pack(fill="x", pady=(0, 16))

        self.photo_label = tk.Label(
            frame, text="📷", bg=COLORS["card"],
            font=("Segoe UI", 48)
        )
        self.photo_label.pack(pady=30)

        path = self.item.get("photo_path")
        if not path:
            return

        try:
            from PIL import Image, ImageTk

            img = Image.open(path)
            img.thumbnail((300, 300))
            self._photo_image = ImageTk.PhotoImage(img)
            self.photo_label.config(
                image=self._photo_image, text=""
            )
        except Exception:
            self.photo_label.config(
                text="⚠ Image failed to load",
                font=("Segoe UI", 12)
            )

    def _details(self, parent):
        tk.Label(
            parent, text=self.item["name"],
            bg=COLORS["bg"], fg=COLORS["text"],
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        status = self.item.get("status", "stored")
        status_text = "Available" if status == "stored" else status.title()

        status_colors = {
            "stored": COLORS["success"],
            "lent": COLORS["primary"],
            "borrowed": COLORS["info"],
            "lost": COLORS["danger"]
        }

        tk.Label(
            parent, text=status_text,
            bg=status_colors.get(status, COLORS["text_muted"]),
            fg="white", font=FONTS["small_bold"],
            padx=12, pady=4
        ).pack(anchor="w", pady=(8, 16))

        details = tk.Frame(parent, bg=COLORS["bg"])
        details.pack(fill="x", pady=(0, 16))

        location = self.item.get("room", "")
        container = self.item.get("container", "")

        if container:
            location += f" → {container}"

        fields = [
            ("Category", self.item.get("category", "General")),
            ("Location", location),
            ("Person", self.item.get("person", "-")),
            ("Due Date", self.item.get("due_date", "-")),
            ("Added", self.item.get("date_added", "-")),
            ("Tags", self.item.get("tags", "-"))
        ]

        for row, (label, value) in enumerate(fields):
            tk.Label(
                details, text=label,
                bg=COLORS["bg"], fg=COLORS["text_muted"],
                font=FONTS["body_bold"]
            ).grid(row=row, column=0, sticky="nw",
                   pady=6, padx=(0, 20))

            tk.Label(
                details, text=value or "-",
                bg=COLORS["bg"], fg=COLORS["text"],
                font=FONTS["body"]
            ).grid(row=row, column=1, sticky="nw", pady=6)

        notes = self.item.get("notes")
        if notes:
            tk.Label(
                parent, text="Notes",
                bg=COLORS["bg"], fg=COLORS["text"],
                font=FONTS["heading"]
            ).pack(anchor="w", pady=(8, 4))

            tk.Label(
                parent, text=notes,
                bg=COLORS["card"], fg=COLORS["text"],
                font=FONTS["body"],
                wraplength=420, justify="left",
                padx=12, pady=10
            ).pack(fill="x", pady=(0, 16))

    def _history(self, parent):
        tk.Label(
            parent, text="History",
            bg=COLORS["bg"], fg=COLORS["text"],
            font=FONTS["heading"]
        ).pack(anchor="w", pady=(8, 4))

        history = get_history(self.item_id)

        if not history:
            tk.Label(
                parent, text="No history yet.",
                bg=COLORS["bg"],
                fg=COLORS["text_muted"],
                font=FONTS["body"]
            ).pack(pady=10)
            return

        for h in history[:5]:
            frame = tk.Frame(
                parent, bg=COLORS["card"],
                highlightbackground=COLORS["border"],
                highlightthickness=1
            )
            frame.pack(fill="x", pady=(0, 6))

            old = h.get("old_location", "")
            new = h.get("new_location", "")
            changed = h.get("changed_at", "")

            text = (
                f"{old} → {new}"
                if old and new
                else old or new or "Updated"
            )

            tk.Label(
                frame, text=text,
                bg=COLORS["card"], fg=COLORS["text"],
                font=FONTS["small"]
            ).pack(anchor="w", padx=12, pady=8)

            tk.Label(
                frame, text=changed,
                bg=COLORS["card"],
                fg=COLORS["text_muted"],
                font=FONTS["small"]
            ).pack(anchor="w", padx=12, pady=(0, 8))

    def _buttons(self, parent):
        from components import RoundedButton

        frame = tk.Frame(parent, bg=COLORS["bg"])
        frame.pack(fill="x", pady=(16, 0))

        status = self.item.get("status")

        # Returned button for lent/borrowed items
        if status in ("lent", "borrowed"):
            RoundedButton(
                frame, text="Mark Returned",
                command=self._mark_returned,
                bg=COLORS["success"],
                width=120
            ).pack(side="left", padx=4)

        # Found button for lost items
        if status == "lost":
            RoundedButton(
                frame, text="Mark Found",
                command=self._mark_found,
                bg=COLORS["success"],
                width=100
            ).pack(side="left", padx=4)

        # Edit and Delete should ALWAYS be available
        RoundedButton(
            frame, text="Edit Item",
            command=self._edit,
            bg=COLORS["primary"],
            width=100
        ).pack(side="left", padx=4)

        RoundedButton(
            frame, text="Delete",
            command=self._delete,
            bg=COLORS["danger"],
            width=100
        ).pack(side="left", padx=4)

    def _edit(self):
        from views.add_edit import AddEditWindow

        AddEditWindow(
            self.controller,
            self.controller,
            item_id=self.item_id
        )
        self.destroy()

    def _mark_returned(self):
        self._change_status(
            "stored",
            "Item marked as returned"
        )

    def _mark_found(self):
        self._change_status(
            "stored",
            "Item marked as found"
        )

    def _change_status(self, status, message):
        from database import update_item

        data = dict(self.item)
        data["status"] = status
        data["person"] = ""
        data["due_date"] = ""

        update_item(self.item_id, data)

        self.controller.toast.show(message, "success")
        self.controller.refresh_current_view()
        self.destroy()

    def _delete(self):
        from tkinter import messagebox
        from database import soft_delete_item

        if messagebox.askyesno(
            "Delete Item",
            "Move this item to trash?",
            parent=self
        ):
            soft_delete_item(self.item_id)
            self.controller.toast.show(
                "Item moved to trash", "warning"
            )
            self.controller.refresh_current_view()
            self.destroy()