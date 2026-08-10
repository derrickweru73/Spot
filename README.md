# Spot

> **Never Lose Your Stuff Again**

## Project Overview

**Spot** is a Python desktop application built with **tkinter** that helps users track their physical belongings. It allows users to record where items are stored, who has borrowed them, and items they have borrowed.

The application works completely offline using **SQLite3** for local data storage.

## Problems It Solves

- **Lost Items:** Helps users remember where their belongings are stored.
- **Lent Items:** Tracks who has borrowed your items and when they are due back.
- **Borrowed Items:** Records items borrowed from other people and their return dates.
- **Offline Tracking:** Stores all information locally without requiring internet access.
- **Poor Organization:** Provides a single place to manage physical belongings.

## Features

- Add, edit, and delete items.
- Track stored, lent, and borrowed items.
- Record item location, room, and container.
- Track people who have borrowed or lent items.
- Add due dates and detect overdue items.
- Search items by name, room, or tag.
- View item movement history.
- Attach photos to items.
- View dashboard statistics.
- Export inventory to CSV.
- Responsive tkinter layout.
- Local SQLite database.
- Fully offline application.

## Project Structure

```text
spot/
│
├── main.py
├── theme.py
├── database.py
├── components.py
├── spot.db
├── photos/
│
└── views/
    ├── __init__.py
    ├── dashboard.py
    ├── stash_view.py
    ├── lent_view.py
    ├── borrowed_view.py
    └── add_edit.py
```

## Technologies Used

- Python 3
- `tkinter`
- `SQLite3`
- `Pillow`
- CSV

## Core Python Concepts Demonstrated

- Object-Oriented Programming (classes for views and components)
- tkinter Widgets (`Canvas`, `Frame`, `Label`, `Entry`, `Scrollbar`)
- Functions and Methods
- Variables and Data Types
- Conditional Statements (`if`, `elif`, `else`)
- Loops (`for`, `while`)
- Lists and Dictionaries
- String Manipulation
- File Handling (CSV export, photo paths)
- Database CRUD Operations (Create, Read, Update, Delete)
- SQL Joins (linking history to items)
- Input Validation

## How the App Works

1. Launch the application with `main.py`.
2. Add an item using **Add Item**.
3. Enter the item's name, category, location, status, and other details.
4. Save the item to the SQLite database.
5. View items from **My Items**.
6. Track lent items from **Lent Out**.
7. Track borrowed items from **Borrowed**.
8. Search and update items when necessary.
9. View item history and dashboard statistics.
10. Export the inventory to CSV.

## Installation

### Prerequisites

- Python `3.8+`
- `pip`
- Visual Studio Code
- Git

### Clone the Repository

```bash
git clone https://github.com/yourusername/spot.git
```

### Open the Project

```bash
cd spot
```

```bash
code .
```

### Install Dependencies

```bash
pip install Pillow
```

### Run the App

```bash
python main.py
```

## Sample Usage

```text
========================================
              SPOT
       Never Lose Your Stuff Again
========================================

Stored Items: 12
Lent Out: 3
Borrowed: 2
Overdue: 1

Recent Items
----------------------------------------
Passport
Room: Bedroom
Container: Safe
Status: Stored

USB Drive
Room: Office
Status: Lent Out

Drill
Room: Garage
Status: Borrowed
Due: 2026-08-15
```

## Database

Spot uses **SQLite3** for local data storage.

```text
Database: spot.db

Stores:
- Item information
- Locations
- Lending information
- Borrowing information
- Due dates
- Item history
```

## Future Improvements

- Light/Dark theme toggle.
- Trash and restore functionality.
- Statistics charts.
- Category filters.
- Keyboard shortcuts.
- Bulk CSV import.
- Notification alerts.
- Print-friendly reports.
- Right-click context menus.
- Database backup and restore.
- Advanced search and filtering.

## Contribution

You can contribute by:

- Improving the UI.
- Adding new features.
- Improving database functionality.
- Fixing bugs.
- Adding new views.
- Improving performance.

### How to Contribute

1. Fork the repository.

2. Create a branch:

```bash
git checkout -b feature-name
```

3. Make your changes.

4. Commit your changes:

```bash
git commit -m "Added new feature"
```

5. Push your changes:

```bash
git push origin feature-name
```

6. Create a Pull Request.

## Author

**Developed by Derrick Weru**

## License

This project is for educational purposes and is free to use, modify, and distribute for learning and academic projects.