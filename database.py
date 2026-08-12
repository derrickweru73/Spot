"""SQLite persistence layer for Spot."""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'spot.db'
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():

    conn = get_connection()
    c = conn.cursor()

    # --------------------------------------------------------
    # Items
    # --------------------------------------------------------

    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            room TEXT NOT NULL,
            container TEXT,
            status TEXT DEFAULT 'stored',
            person TEXT,
            date_added TEXT,
            due_date TEXT,
            photo_path TEXT,
            tags TEXT,
            notes TEXT
        )
    ''')

    # --------------------------------------------------------
    # History
    # --------------------------------------------------------

    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            old_location TEXT,
            new_location TEXT,
            changed_at TEXT,
            FOREIGN KEY (item_id)
                REFERENCES items(id)
                ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


# ============================================================
# ADD ITEM
# ============================================================

def add_item(data: dict) -> int:

    conn = get_connection()
    c = conn.cursor()

    now = datetime.now().isoformat(
        sep=' ',
        timespec='minutes'
    )

    c.execute('''
        INSERT INTO items (
            name,
            category,
            room,
            container,
            status,
            person,
            date_added,
            due_date,
            photo_path,
            tags,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'],
        data.get('category', 'General'),
        data['room'],
        data.get('container', ''),
        data.get('status', 'stored'),
        data.get('person', ''),
        now,
        data.get('due_date', ''),
        data.get('photo_path', ''),
        data.get('tags', ''),
        data.get('notes', '')
    ))

    item_id = c.lastrowid

    location = (
        f"{data['room']} → "
        f"{data.get('container', 'unspecified')}"
    )

    c.execute('''
        INSERT INTO history (
            item_id,
            old_location,
            new_location,
            changed_at
        )
        VALUES (?, ?, ?, ?)
    ''', (
        item_id,
        'Created',
        location,
        now
    ))

    conn.commit()
    conn.close()

    return item_id


# ============================================================
# GET ALL ITEMS
# ============================================================

def get_all_items(
    status: str = None,
    search: str = None,
    room: str = None,
    limit: int = None
):

    conn = get_connection()
    c = conn.cursor()

    query = '''
        SELECT *
        FROM items
        WHERE 1=1
    '''

    params = []

    if status:

        query += ' AND status = ?'
        params.append(status)

    if room and room != 'All':

        query += ' AND room = ?'
        params.append(room)

    if search:

        query += '''
            AND (
                name LIKE ?
                OR tags LIKE ?
                OR room LIKE ?
                OR container LIKE ?
                OR person LIKE ?
            )
        '''

        like = f'%{search}%'

        params.extend([
            like,
            like,
            like,
            like,
            like
        ])

    query += '''
        ORDER BY date_added DESC
    '''

    if limit:

        query += ' LIMIT ?'
        params.append(limit)

    c.execute(
        query,
        params
    )

    rows = [
        dict(row)
        for row in c.fetchall()
    ]

    conn.close()

    return rows


# ============================================================
# GET SINGLE ITEM
# ============================================================

def get_item(item_id: int):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        'SELECT * FROM items WHERE id = ?',
        (item_id,)
    )

    row = c.fetchone()

    conn.close()

    return dict(row) if row else None


# ============================================================
# UPDATE ITEM
# ============================================================

def update_item(item_id: int, data: dict):

    conn = get_connection()
    c = conn.cursor()

    # Get previous information
    c.execute(
        'SELECT * FROM items WHERE id = ?',
        (item_id,)
    )

    old_row = c.fetchone()

    old = dict(old_row) if old_row else None

    old_loc = (
        f"{old['room']} → {old['container']}"
        if old
        else 'Unknown'
    )

    new_loc = (
        f"{data['room']} → "
        f"{data.get('container', '')}"
    )

    old_status = (
        old['status']
        if old
        else None
    )

    new_status = data.get(
        'status',
        'stored'
    )

    c.execute('''
        UPDATE items
        SET
            name=?,
            category=?,
            room=?,
            container=?,
            status=?,
            person=?,
            due_date=?,
            photo_path=?,
            tags=?,
            notes=?
        WHERE id=?
    ''', (
        data['name'],
        data.get('category', 'General'),
        data['room'],
        data.get('container', ''),
        new_status,
        data.get('person', ''),
        data.get('due_date', ''),
        data.get('photo_path', ''),
        data.get('tags', ''),
        data.get('notes', ''),
        item_id
    ))

    now = datetime.now().isoformat(
        sep=' ',
        timespec='minutes'
    )

    # --------------------------------------------------------
    # Record location changes
    # --------------------------------------------------------

    if old_loc != new_loc:

        c.execute('''
            INSERT INTO history (
                item_id,
                old_location,
                new_location,
                changed_at
            )
            VALUES (?, ?, ?, ?)
        ''', (
            item_id,
            old_loc,
            new_loc,
            now
        ))

    # --------------------------------------------------------
    # Record status changes
    #
    # We use the existing history columns so that
    # existing databases remain compatible.
    # --------------------------------------------------------

    if old_status != new_status:

        c.execute('''
            INSERT INTO history (
                item_id,
                old_location,
                new_location,
                changed_at
            )
            VALUES (?, ?, ?, ?)
        ''', (
            item_id,
            f"Status: {old_status or 'unknown'}",
            f"Status: {new_status}",
            now
        ))

    conn.commit()
    conn.close()


# ============================================================
# DELETE ITEM
# ============================================================

def delete_item(item_id: int):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        'DELETE FROM items WHERE id = ?',
        (item_id,)
    )

    conn.commit()
    conn.close()


# ============================================================
# ADD HISTORY ENTRY
# ============================================================

def add_history(
    item_id: int,
    old_location: str,
    new_location: str,
    changed_at: str = None
):

    conn = get_connection()
    c = conn.cursor()

    if changed_at is None:

        changed_at = datetime.now().isoformat(
            sep=' ',
            timespec='minutes'
        )

    c.execute('''
        INSERT INTO history (
            item_id,
            old_location,
            new_location,
            changed_at
        )
        VALUES (?, ?, ?, ?)
    ''', (
        item_id,
        old_location,
        new_location,
        changed_at
    ))

    conn.commit()
    conn.close()


# ============================================================
# GET HISTORY
# ============================================================

def get_history(
    item_id: int = None,
    limit: int = None
):

    conn = get_connection()
    c = conn.cursor()

    if item_id:

        query = '''
            SELECT
                h.*,
                i.name AS item_name
            FROM history h
            JOIN items i
                ON h.item_id = i.id
            WHERE h.item_id = ?
            ORDER BY h.changed_at DESC
        '''

        params = [item_id]

        if limit:

            query += ' LIMIT ?'
            params.append(limit)

        c.execute(
            query,
            params
        )

    else:

        query = '''
            SELECT
                h.*,
                i.name AS item_name
            FROM history h
            JOIN items i
                ON h.item_id = i.id
            ORDER BY h.changed_at DESC
        '''

        params = []

        if limit:

            query += ' LIMIT ?'
            params.append(limit)

        c.execute(
            query,
            params
        )

    rows = [
        dict(row)
        for row in c.fetchall()
    ]

    conn.close()

    return rows


# ============================================================
# STATISTICS
# ============================================================

def get_stats():

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT COUNT(*) FROM items WHERE status='stored'"
    )

    stored = c.fetchone()[0]

    c.execute(
        "SELECT COUNT(*) FROM items WHERE status='lent'"
    )

    lent = c.fetchone()[0]

    c.execute(
        "SELECT COUNT(*) FROM items WHERE status='borrowed'"
    )

    borrowed = c.fetchone()[0]

    c.execute(
        "SELECT COUNT(*) FROM items WHERE status='lost'"
    )

    lost = c.fetchone()[0]

    now = datetime.now().isoformat(
        sep=' ',
        timespec='minutes'
    )

    c.execute('''
        SELECT COUNT(*)
        FROM items
        WHERE
            due_date != ''
            AND due_date < ?
            AND status IN ('lent', 'borrowed')
    ''', (now,))

    overdue = c.fetchone()[0]

    c.execute(
        "SELECT COUNT(*) FROM items"
    )

    total = c.fetchone()[0]

    conn.close()

    return {
        'stored': stored,
        'lent': lent,
        'borrowed': borrowed,
        'lost': lost,
        'overdue': overdue,
        'total': total
    }


# ============================================================
# GET ROOMS
# ============================================================

def get_rooms():

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT DISTINCT room FROM items ORDER BY room"
    )

    rooms = [
        row[0]
        for row in c.fetchall()
        if row[0]
    ]

    conn.close()

    return rooms


# ============================================================
# EXPORT TO CSV
# ============================================================

def export_to_csv(filepath: str):

    import csv

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        'SELECT * FROM items ORDER BY date_added DESC'
    )

    rows = c.fetchall()

    headers = [
        description[0]
        for description in c.description
    ]

    with open(
        filepath,
        'w',
        newline='',
        encoding='utf-8'
    ) as f:

        writer = csv.writer(f)

        writer.writerow(headers)

        writer.writerows(rows)

    conn.close()


# ============================================================
# INITIALIZE DATABASE
# ============================================================

init_db()


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print("Database initialized!")

    stats = get_stats()

    print("Stats:", stats)

    item_id = add_item({
        'name': 'Test Passport',
        'room': 'Bedroom',
        'container': 'Top drawer',
        'status': 'stored',
        'tags': 'travel, important'
    })

    print(
        f"Added item with ID: {item_id}"
    )

    items = get_all_items()

    print(
        f"Total items now: {len(items)}"
    )

    if items:

        print(
            "First item:",
            items[0]['name']
        )