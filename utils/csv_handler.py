"""CSV import and export."""

import csv
from database import get_connection, add_item
from utils.validators import validate_csv_row


def export_to_csv(filepath: str) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE is_deleted = 0 ORDER BY date_added DESC")
    rows = c.fetchall()
    headers = [desc[0] for desc in c.description]
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    conn.close()
    return len(rows)


def import_from_csv(filepath: str) -> dict:
    imported = 0
    skipped = 0
    errors = []
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            try:
                data = {
                    "name": row.get("name", "").strip(),
                    "category": row.get("category", "General").strip(),
                    "room": row.get("room", row.get("location", "")).strip(),
                    "container": row.get("container", "").strip(),
                    "status": row.get("status", "stored").strip().lower(),
                    "person": row.get("person", "").strip(),
                    "due_date": row.get("due_date", "").strip(),
                    "photo_path": row.get("photo_path", "").strip(),
                    "tags": row.get("tags", "").strip(),
                    "notes": row.get("notes", "").strip(),
                }
                ok, msg = validate_csv_row(data)
                if not ok:
                    skipped += 1
                    errors.append(f"Row {row_num}: {msg}")
                    continue
                add_item(data)
                imported += 1
            except Exception as exc:
                skipped += 1
                errors.append(f"Row {row_num}: {exc}")
    return {
        "imported": imported,
        "skipped": skipped,
        "errors": errors,
        "total": imported + skipped,
    }


def get_csv_template() -> str:
    headers = [
        "name", "category", "room", "container",
        "status", "person", "due_date", "photo_path", "tags", "notes"
    ]
    return ",".join(headers) + "\n"