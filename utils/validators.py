"""Input validation."""

import re
from datetime import datetime


def validate_name(name: str) -> tuple[bool, str]:
    name = name.strip()
    if not name:
        return False, "Name is required."
    if len(name) > 100:
        return False, "Name must be under 100 characters."
    return True, ""


def validate_room(room: str) -> tuple[bool, str]:
    room = room.strip()
    if not room:
        return False, "Room/Location is required."
    if len(room) > 50:
        return False, "Room must be under 50 characters."
    return True, ""


def validate_due_date(due_date: str) -> tuple[bool, str]:
    if not due_date.strip():
        return True, ""
    formats = ["%Y-%m-%d %H:%M", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]
    for fmt in formats:
        try:
            datetime.strptime(due_date.strip(), fmt)
            return True, ""
        except ValueError:
            continue
    return False, "Invalid date format. Use YYYY-MM-DD HH:MM or YYYY-MM-DD."


def validate_tags(tags: str) -> tuple[bool, str]:
    if not tags.strip():
        return True, ""
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    if len(tag_list) > 20:
        return False, "Maximum 20 tags allowed."
    for tag in tag_list:
        if len(tag) > 30:
            return False, f"Tag too long: '{tag[:20]}...'"
    return True, ""


def validate_csv_row(row: dict) -> tuple[bool, str]:
    ok, msg = validate_name(row.get("name", ""))
    if not ok:
        return False, msg
    ok, msg = validate_room(row.get("room", ""))
    if not ok:
        return False, msg
    if row.get("due_date"):
        ok, msg = validate_due_date(row["due_date"])
        if not ok:
            return False, msg
    return True, ""


def sanitize_search(text: str) -> str:
    text = re.sub(r"[%'\"\\]", "", text)
    return text.strip()