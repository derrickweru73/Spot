"""Chart widgets."""

import tkinter as tk
from theme import COLORS, FONTS


class BarChart(tk.Canvas):
    def __init__(self, parent, data, title="", width=400, height=250, **kwargs):
        super().__init__(parent, width=width, height=height, bg=COLORS["card"], highlightthickness=0, **kwargs)
        self.data = data
        self.chart_title = title
        self.chart_width = width
        self.chart_height = height
        self._draw()

    def _draw(self):
        self.delete("all")
        if not self.data:
            self.create_text(self.chart_width // 2, self.chart_height // 2,
                             text="No data", fill=COLORS["text_muted"], font=FONTS["body"])
            return
        if self.chart_title:
            self.create_text(20, 20, text=self.chart_title, anchor="w",
                             fill=COLORS["text"], font=FONTS["heading"])
        max_val = max(self.data.values()) if self.data else 1
        max_val = max(max_val, 1)
        bar_count = len(self.data)
        margin = 40
        top_margin = 50
        bottom_margin = 40
        bar_gap = 12
        available_width = self.chart_width - margin * 2
        bar_width = (available_width - bar_gap * (bar_count - 1)) // bar_count
        colors = ["#FF7A00", "#00A3FF", "#2EB872", "#E53935", "#8B5CF6", "#F59E0B"]

        for i, (label, value) in enumerate(self.data.items()):
            x1 = margin + i * (bar_width + bar_gap)
            bar_height = (value / max_val) * (self.chart_height - top_margin - bottom_margin)
            y1 = self.chart_height - bottom_margin - bar_height
            x2 = x1 + bar_width
            y2 = self.chart_height - bottom_margin
            color = colors[i % len(colors)]
            self.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)
            self.create_text((x1 + x2) // 2, y1 - 8, text=str(value),
                             fill=COLORS["text"], font=FONTS["small_bold"])
            self.create_text((x1 + x2) // 2, y2 + 14, text=label,
                             fill=COLORS["text_muted"], font=FONTS["small"])


class PieChart(tk.Canvas):
    def __init__(self, parent, data, title="", width=250, height=250, **kwargs):
        super().__init__(parent, width=width, height=height, bg=COLORS["card"], highlightthickness=0, **kwargs)
        self.data = data
        self.chart_title = title
        self.chart_width = width
        self.chart_height = height
        self._draw()

    def _draw(self):
        self.delete("all")
        if not self.data:
            self.create_text(self.chart_width // 2, self.chart_height // 2,
                             text="No data", fill=COLORS["text_muted"], font=FONTS["body"])
            return
        if self.chart_title:
            self.create_text(self.chart_width // 2, 18, text=self.chart_title,
                             fill=COLORS["text"], font=FONTS["heading"])
        total = sum(self.data.values())
        if total == 0:
            return
        colors = ["#FF7A00", "#00A3FF", "#2EB872", "#E53935", "#8B5CF6", "#F59E0B", "#EC4899"]
        cx = self.chart_width // 2
        cy = self.chart_height // 2 + 5
        radius = min(cx, cy) - 35
        start_angle = 0

        for i, (label, value) in enumerate(self.data.items()):
            extent = (value / total) * 360
            color = colors[i % len(colors)]
            self.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                            start=start_angle, extent=extent, fill=color, outline="")
            mid_angle = (start_angle + extent / 2) * 3.14159 / 180
            label_radius = radius + 25
            lx = cx + label_radius * 0.9 * (1 if mid_angle < 3.14159 else -1)
            ly = cy - label_radius * 0.3
            pct = round((value / total) * 100)
            self.create_text(lx, ly, text=f"{label}\n{pct}%", fill=COLORS["text_muted"],
                             font=FONTS["small"], justify="center")
            start_angle += extent

        hole_radius = radius // 3
        self.create_oval(cx - hole_radius, cy - hole_radius, cx + hole_radius, cy + hole_radius,
                         fill=COLORS["card"], outline="")
        self.create_text(cx, cy, text=str(total), fill=COLORS["text"],
                         font=("Segoe UI", 14, "bold"))