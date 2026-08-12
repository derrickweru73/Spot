"""Overdue and due-soon reminders."""

from datetime import datetime, timedelta
from database import get_all_items


def get_overdue_items():
    items = get_all_items()
    now = datetime.now()
    overdue = []
    for item in items:
        due_date = item.get("due_date")
        if not due_date or item.get("status") not in ("lent", "borrowed"):
            continue
        try:
            due = datetime.fromisoformat(due_date)
            if due < now:
                item["is_overdue"] = True
                item["days_overdue"] = (now - due).days
                overdue.append(item)
        except ValueError:
            continue
    overdue.sort(key=lambda x: x.get("due_date", ""))
    return overdue


def get_due_soon_items(days=3):
    items = get_all_items()
    now = datetime.now()
    soon = now + timedelta(days=days)
    due_soon = []
    for item in items:
        due_date = item.get("due_date")
        if not due_date or item.get("status") not in ("lent", "borrowed"):
            continue
        try:
            due = datetime.fromisoformat(due_date)
            if now <= due <= soon:
                item["days_until_due"] = (due - now).days
                due_soon.append(item)
        except ValueError:
            continue
    due_soon.sort(key=lambda x: x.get("due_date", ""))
    return due_soon


def get_notification_summary():
    overdue = get_overdue_items()
    due_soon = get_due_soon_items()
    return {
        "overdue_count": len(overdue),
        "due_soon_count": len(due_soon),
        "overdue": overdue,
        "due_soon": due_soon,
        "total_alerts": len(overdue) + len(due_soon),
    }