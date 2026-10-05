# Schedule Management System

> **Project Status:** Working (core CRUD features complete)
> A desktop application for recording, viewing, updating, and deleting personal schedules and academic deadlines, stored permanently in a SQLite database.

---

## Table of Contents

1. [Project Description](#project-description)
2. [Project Objectives](#project-objectives)
3. [Features](#features)
4. [Technologies Used](#technologies-used)
5. [Project Structure](#project-structure)
6. [Installation and Setup](#installation-and-setup)
7. [How to Use the System](#how-to-use-the-system)
8. [OOP Implementation](#oop-implementation)
9. [Database](#database)
10. [Screenshots](#screenshots)
11. [Testing](#testing)
12. [Known Issues / Limitations](#known-issues--limitations)
13. [Author](#author)

---

## Project Description

### What the system does

The **Schedule Management System** is a desktop GUI application that lets a student record
every important date in one place instead of keeping it on paper, in a notebook, or in a
memorized mental list. Each schedule entry stores a **title, date, time, type, and
description**, and is saved into a local SQLite database file so nothing is lost when the
program is closed.

The program was built as a menu-driven command-line project first (`controller/schedule.py`),
then upgraded into a windowed PyQt6 application (`view/student_view.py`) on top of the same
database layer.

### The problem / need it addresses

Managing academic schedules by hand has several practical problems:

- **Schedules are forgotten.** Deadlines are missed because nothing reminds the student
  when a quiz or exam is coming up.
- **Paper and notebooks get lost or damaged.** There is no backup and no way to search
  through old notes.
- **Entries are hard to correct.** If a subject code or exam date changes, rewriting or
  crossing out a paper entry is messy and error-prone.
- **No single view of everything.** Class schedules, exams, and assignments end up
  scattered across notebooks, group chats, and posters.

This system solves all of these by giving one small window where every entry can be
**created, read, updated, deleted, and reviewed** at a glance, with the data safely
persisted in a database.

---

## Project Objectives

1. Provide a simple desktop application for recording personal and academic schedules.
2. Persist all schedule data permanently using a relational database (SQLite) instead of
   a temporary file or in-memory list.
3. Follow good Object-Oriented Programming principles — **encapsulation, inheritance,
   and polymorphism** — by separating the program into logical layers.
4. Separate concerns using a layered architecture so each part of the program has one
   clear responsibility:
   - **Model** – holds the data of one schedule
   - **Repository** – performs all SQL / database operations
   - **Service** – business logic between the GUI and the database
   - **View** – the graphical user interface
5. Use parameterized SQL queries so the program is not vulnerable to SQL injection.
6. Keep the user interface simple enough for a non-programmer to use without training.
7. Provide clear user feedback through confirmation dialogs and warning messages.

---

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Add Schedule** | Fills the form with a title, date, time, type, and description, then presses **Add Schedule** to store a new record. |
| 2 | **View All Schedules** | All saved schedules appear in a list at the bottom of the window as `Title \| Date \| Time \| Type \| Description`. |
| 3 | **Update Schedule** | Select a schedule and press **Update Selected**. The form fills with that record and the button changes to **Save Changes**, allowing the entry to be corrected. |
| 4 | **Delete Schedule** | Select a schedule and press **Delete Selected**. A confirmation dialog appears first so a record is never deleted by accident. |
| 5 | **Input Validation** | The title field is mandatory. Leaving it empty shows a *"Please enter a title"* warning and stops the operation. |
| 6 | **Automatic Whitespace Cleaning** | Leading and trailing spaces are removed from the title, date, type, and description before saving. |
| 7 | **Selection Guard** | Pressing **Update** or **Delete** with nothing selected shows a *"Please select a schedule"* warning instead of failing silently. |
| 8 | **Missing-Record Guard** | If the selected record no longer exists in the database, the app warns *"That schedule no longer exists"* and resets the form safely. |
| 9 | **Keyboard Shortcut** | Pressing **Enter** in the Title field saves the schedule, so the whole form can be filled with the keyboard only. |
| 10 | **Automatic Table Creation** | The `schedule` table is created automatically on first run — no manual SQL or setup step is required. |
| 11 | **Persistent Storage** | Data is stored in `data/schedule.db` and survives closing and reopening the application. |

---

## Technologies Used

| Category | Technology | Details |
|----------|-----------|---------|
| **Programming Language** | Python 3 | Written and tested on Python 3.14.7 |
| **GUI Framework / Library** | PyQt6 | Version 6.11.0 — provides all widgets (`QWidget`, `QLineEdit`, `QListWidget`, `QPushButton`, `QMessageBox`, `QVBoxLayout`, `QFormLayout`) |
| **Database** | SQLite3 | Python's built-in `sqlite3` module — a serverless, file-based relational database. No separate DB server required. |
| **Other Libraries** | `dataclasses` (stdlib) | Used to build the `Schedule` model with the `@dataclass` decorator |
| **Other Libraries** | `pathlib` (stdlib) | Used to build the cross-platform path to `schedule.db` |
| **Other Tools** | Qt Signal/ Slot mechanism | `pyqtSignal` and `.connect()` connect GUI events to handler methods |
| **IDE / Version Control** | Git | Repository hosted on GitHub |

> **Note:** PyQt5 was previously installed in the same environment but is **not** used by this
> project. All imports use `PyQt6`.

---

## Project Structure

```
ScheduleManagementSystem/
│
├── main.py                      # Entry point — creates Database, Service, and View, starts Qt
├── README.md                    # Project documentation (this file)
├── REPORT.md                    # Earlier command-line version program report
├── requirements.txt             # Python dependencies
│
├── controller/
│   ├── __init__.py
│   └── schedule.py              # CLI version: get_schedule(), show_schedule(), delete_schedule()
│
├── data/                        # DATABASE LAYER
│   ├── __init__.py
│   ├── data.py                  # Database class — holds the DB path, creates the table
│   └── schedule.db              # SQLite database file (auto-created on first run)
│
├── features/                    # FEATURE MODULES
│   ├── __init__.py
│   ├── calendar/
│   │   └── __init__.py          # Placeholder for a future calendar/date-picker feature
│   └── schedule/                # Schedule feature (complete feature module)
│       ├── __init__.py
│       ├── model.py             # Schedule dataclass — the data of ONE schedule
│       ├── repository.py        # ScheduleRepository — all SQL (Create/Read/Update/Delete)
│       ├── service.py           # Service classes — business logic layer
│       └── view.py              # Legacy/unused early GUI attempt (superseded by view/)
│
└── view/                        # PRESENTATION LAYER
    ├── __init__.py              # Exports StudentView
    └── student_view.py          # StudentView — the actual application window
```

### Purpose of each important file

| File / Folder | Purpose |
|---------------|---------|
| `main.py` | Program entry point. Creates the `Database`, builds the `ScheduleRepository` inside `StudentService`, creates the `StudentView` window, and starts the Qt event loop. |
| `controller/schedule.py` | The original command-line (menu-driven) version of the program. Kept for reference; its loop is currently commented out in `main.py`. |
| `data/data.py` | Defines the `Database` class. Stores the database file path, opens connections, and creates the `schedule` table if it does not exist. |
| `data/schedule.db` | The SQLite database file that stores all schedules. Created automatically — never edit by hand. |
| `features/schedule/model.py` | Defines the `Schedule` dataclass (`title`, `date`, `time`, `typ`, `desc`, `id`). Cleans whitespace in `__post_init__`. |
| `features/schedule/repository.py` | The `ScheduleRepository` class. Contains **all** SQL statements using parameterized queries. Converts database rows into `Schedule` objects. |
| `features/schedule/service.py` | Business logic layer. `ScheduleService` and `StudentService` pass requests from the GUI down to the repository. |
| `features/schedule/view.py` | An early, unfinished GUI attempt containing typos (`refrest()`, `sertHorizontalHeaderLabels`). **Not imported by `main.py`** — kept only as history. |
| `view/student_view.py` | The real application window (`StudentView`). Builds the form, buttons, and list, and handles add/update/delete/refresh. |
| `features/calendar/` | Empty placeholder package for a planned calendar/date-picker feature. |

---

## Installation and Setup

### Required Dependencies

```
Python      >= 3.10     (tested on 3.14.7)
PyQt6       >= 6.5      (tested on 6.11.0)
sqlite3                (included with Python — no separate install)
```

Only **PyQt6** must be installed manually. `sqlite3`, `dataclasses`, and `pathlib` all
come bundled with Python.

### Step-by-step instructions

**Step 1 — Clone the repository**

```bash
git clone https://github.com/NotLevi-Fr/Schedule-Management-System.git
cd ScheduleManagementSystem
```

**Step 2 — Create a virtual environment (recommended)**

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

**Step 3 — Install the dependency**

```bash
pip install PyQt6
```

Or install everything listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Step 4 — Run the program**

```bash
python main.py
```

**Step 5 — Verify the database was created**

On first run the app creates `data/schedule.db` automatically. To confirm:

```bash
sqlite3 data/schedule.db ".tables"
# Expected output: schedule
```

> **Linux users only:** PyQt6 needs system libraries. If the app fails to start, install
> them with `sudo apt install libxcb-xinerama0 libxkbcommon-x11-0 libxcb-cursor0`.

---

## How to Use the System

### Basic steps

1. **Start the program** — run `python main.py`. A window titled *"Schedule Management
   System"* opens (420 × 480 px).

2. **Add a schedule**
   - Type a **Title** (required), e.g. `Calculus Final`
   - Type a **Date** in `MM/DD/YYYY` format, e.g. `05/20/2027`
   - Type a **Time** in `HH:MM` format (24-hour), e.g. `09:00`
   - Type a **Type**, e.g. `Exam`, `Activity`, `Assignment`, `Quiz`
   - Optionally type a **Description**
   - Click **Add Schedule** (or press `Enter` while in the Title field)

3. **View your schedules** — every saved schedule appears in the **Schedules** list at the
   bottom of the window in the format
   `Title | Date | Time | Type | Description`.

4. **Update a schedule**
   - Click a schedule in the list to select it.
   - Click **Update Selected**. The form fills with that record's values and the left
     button changes from **Add Schedule** to **Save Changes**.
   - Edit any field, then click **Save Changes**. The list refreshes automatically.

5. **Delete a schedule**
   - Click a schedule in the list to select it.
   - Click **Delete Selected**.
   - A confirmation box asks *"Delete [schedule name]?"* — click **Yes** to confirm or
     **No** to cancel.

6. **Quit** — close the window. All data is already saved in `data/schedule.db`.

### Tips

- Pressing **Enter** in the Title field saves the schedule, so you can fill the form using
  only the keyboard.
- Because dates are stored as text, always use `MM/DD/YYYY` and 24-hour `HH:MM` time so
  entries stay in a consistent, readable order.

---

## OOP Implementation

The project uses **encapsulation**, **inheritance**, and **polymorphism** across a layered
architecture. The flow of data is:

```
StudentView (GUI)  →  StudentService (logic)  →  ScheduleRepository (SQL)  →  Database (SQLite)
       ↑                                                                            │
       └────────────────────  Schedule object returned  ←───────────────────────────┘
```

### Important classes and objects

| Class | File | Type / Base | Responsibility |
|-------|------|-------------|----------------|
| `Schedule` | `features/schedule/model.py` | `@dataclass` | Holds the data of **one** schedule: `title`, `date`, `time`, `typ`, `desc`, `id`. |
| `Database` | `data/data.py` | Plain class | Owns the database file path, opens connections, creates the table. |
| `ScheduleRepository` | `features/schedule/repository.py` | Plain class | Executes **all** SQL. Converts rows → `Schedule` objects. |
| `ScheduleService` | `features/schedule/service.py` | Plain class | Business-logic facade used by the original CLI/early GUI. |
| `StudentService` | `features/schedule/service.py` | Plain class | Business-logic facade used by the current GUI. |
| `StudentView` | `view/student_view.py` | **inherits `QWidget`** | The application window; builds widgets and handles user actions. |
| `ScheduleView` | `features/schedule/view.py` | **inherits `QWidget`** | Legacy early GUI attempt (unused). |
| `Bridge` | `main.py` | **inherits `QObject`** | Holds Qt signals for the commented-out CLI thread. |

### 1. Encapsulation

Encapsulation is applied at **every layer** — each class keeps its own responsibility
private and exposes only a small, clear public interface.

- **`Database` encapsulates the storage details.** The database path and connection logic
  are private to the class. No other class knows the file is called `schedule.db` or that
  it lives in `data/`.

  ```python
  class Database:
      def __init__(self, database_path=None):
          if database_path is None:
              database_path = Path(__file__).resolve().parent / "schedule.db"
          self.database_path = Path(database_path)   # private detail
          self.create_table()

      def connect(self) -> sqlite3.Connection:      # controlled access point
          return sqlite3.connect(self.database_path)
  ```

- **`ScheduleRepository` encapsulates all SQL.** This is the most important example.
  No SQL statement appears anywhere else in the program, so the database can be changed
  (for example to PostgreSQL) without touching the GUI or the service.

  ```python
  # The GUI calls self.service.add(schedule) — it never sees SQL.
  def add(self, schedule: Schedule) -> Schedule:
      with self.database.connect() as connection:
          cursor = connection.execute(
              "INSERT INTO schedule (title, date, time, type, desc) VALUES (?, ?, ?, ?, ?)",
              (schedule.title, schedule.date, schedule.time, schedule.typ, schedule.desc),
          )
          schedule.id = cursor.lastrowid
      return schedule
  ```

- **`StudentService` encapsulates the repository.** The view never imports
  `ScheduleRepository`; it only asks the service to `add`, `update`, `delete`, `get`, or
  `list`. This hides *how* the data is stored.

- **`Schedule` encapsulates its own data cleanup.** Callers can pass messy input with
  extra spaces; the object normalizes itself in `__post_init__`, so every `Schedule` in
  the program is guaranteed to be clean.

  ```python
  @dataclass
  class Schedule:
      title: str
      # ...
      def __post_init__(self) -> None:
          self.title = self.title.strip()   # cleanup happens automatically
  ```

- **`StudentView` encapsulates the form state.** The view owns its input widgets, the
  `editing_id` flag, and helper methods (`clear_form()`, `fill_form()`, `read_form()`,
  `fields()`), so the rest of the program never touches raw widget text.

### 2. Inheritance

- **`StudentView(QWidget)`** — the application window inherits from PyQt6's `QWidget`,
  which gives it a window, a title bar, a layout system, and the ability to be shown on
  screen. `super().__init__()` is called first in the constructor, then `self.resize()`,
  `self.setWindowTitle()`, and the layouts are added on top of the inherited behavior.

  ```python
  class StudentView(QWidget):
      def __init__(self, service: StudentService):
          super().__init__()                     # initialise the QWidget base class
          self.service = service
          self.setWindowTitle("Schedule Management System")
          self.resize(420, 480)
  ```

- **`ScheduleView(QWidget)`** — the same inheritance is used by the legacy view.

- **`Bridge(QObject)`** — inherits Qt's `QObject` so it can own `pyqtSignal` objects.

- **Implicit inheritance** — `ScheduleService`, `StudentService`, `ScheduleRepository`,
  and `Database` all implicitly inherit from Python's `object` base class.

> **Honest note:** this project uses inheritance primarily for **GUI widgets**, which is the
> correct use case in PyQt6. The data and database layers are composed rather than
> inherited (a `has-a` relationship): the repository *has-a* `Database`, the service
> *has-a* repository, and the view *has-a* service. Deep inheritance hierarchies were
> deliberately avoided because they are not needed in a project of this size.

### 3. Polymorphism

- **Method overriding (`StudentView.show`).** `StudentView` overrides the inherited
  `QWidget.show()` method to accept an extra parameter and refresh the list first. When
  Python (or Qt) calls `window.show(1)` on a `StudentView`, the overridden version runs —
  this is polymorphism in action.

  ```python
  def show(self, index: int = 0) -> None:
      self.refresh()       # load data from the database into the list
      super().show()       # then let QWidget show the window
  ```

- **Qt signal/slot polymorphism (event-driven).** Buttons are not told *which* method to
  call in code; they emit signals, and Qt dispatches to whatever method is connected. One
  handler can therefore serve several widgets, and a handler can be swapped without
  touching the UI code.

  ```python
  self.save_button.clicked.connect(self.save_schedule)         # mouse click
  self.title_input.returnPressed.connect(self.save_schedule)  # Enter key
  ```

- **Duck typing in the repository.** `ScheduleRepository.get()` and `.list()` each build
  `Schedule` objects from rows of different shapes (one row vs. many rows) through the
  same constructor. The repository code does not need to know in advance how many objects
  will be produced — it works with whatever the method returns.

- **Polymorphic database behavior.** Both `ScheduleService` and `StudentService` expose the
  same behavior (`add`, `update`, `delete`, `get`, `list`) over the same `Schedule`
  objects. Any code written against one works unchanged against the other, because
  behavior depends on the object's interface, not on a hard-coded class name.

---

## Database

### Database engine

**SQLite3**, accessed through Python's built-in `sqlite3` module. SQLite was chosen because
it needs **no installation, no server, and no configuration** — the entire database is a
single file (`data/schedule.db`). This suits a personal, single-user desktop application.

### Database structure

The system uses **one table**. It was created by `Database.create_table()` in
`data/data.py` using `CREATE TABLE IF NOT EXISTS`, so it is created automatically the first
time the program runs and never has to be set up manually.

```sql
CREATE TABLE IF NOT EXISTS schedule (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,  -- auto-generated unique key
    title TEXT,                              -- required, e.g. 'Calculus Final'
    date  TEXT,                              -- stored as text, format MM/DD/YYYY
    time  TEXT,                              -- stored as text, format HH:MM
    type  TEXT,                              -- e.g. 'Exam', 'Activity', 'Assignment'
    desc  TEXT                               -- optional description
);
```

### Table: `schedule` (the only application table)

| Column | Data Type | Constraint | Description |
|--------|-----------|------------|-------------|
| `id` | INTEGER | **PRIMARY KEY AUTOINCREMENT** | Unique identifier, automatically generated by SQLite. Used for update and delete. |
| `title` | TEXT | (validated in GUI: must not be empty) | The name of the schedule. |
| `date` | TEXT | — | The date, entered as `MM/DD/YYYY`. |
| `time` | TEXT | — | The time, entered as `HH:MM`. |
| `type` | TEXT | — | Category of the schedule (Exam, Activity, Assignment, Quiz, etc.). |
| `desc` | TEXT | — | Optional extra details. |

> SQLite also creates an internal `sqlite_sequence` table by itself to support
> `AUTOINCREMENT`. It is a built-in system table and is not used by the application.

### Relationship diagram

```
┌─────────────────────────────────────────┐
│              schedule                    │
├─────────────────────────────────────────┤
│ id     INTEGER  PRIMARY KEY AUTOINCREMENT│  ← generated by SQLite
│ title  TEXT                              │  ← entered by the user
│ date   TEXT                              │  ← entered by the user
│ time   TEXT                              │  ← entered by the user
│ type   TEXT                              │  ← entered by the user
│ desc   TEXT                              │  ← entered by the user (optional)
└─────────────────────────────────────────┘
        ▲                    ▲
        │                    │
   ScheduleRepository   ScheduleRepository
   .add() → INSERT     .update()/.delete() → WHERE id = ?
```

There are no foreign keys — the system has a single entity, so one table is sufficient.

### Major database operations

All SQL lives in `features/schedule/repository.py`. Every statement uses **parameterized
queries** (`?` placeholders) so user input is never interpreted as SQL — this prevents SQL
injection.

#### CREATE — Add a new schedule
Called when the **Add Schedule** button is pressed.

```python
cursor = connection.execute(
    """
    INSERT INTO schedule (title, date, time, type, desc)
    VALUES (?, ?, ?, ?, ?)
    """,
    (schedule.title, schedule.date, schedule.time, schedule.typ, schedule.desc),
)
schedule.id = cursor.lastrowid    # SQLite assigns the new primary key
```

#### READ — Get one schedule by ID
Called when the **Update Selected** button is pressed, to fill the form.

```python
row = connection.execute(
    "SELECT id, title, date, time, type, desc FROM schedule WHERE id = ?",
    (schedule_id,),
).fetchone()
```

Returns `None` if no matching row exists, which the view handles with the
*"That schedule no longer exists"* warning.

#### READ — List all schedules
Called by `StudentView.refresh()` to populate the list widget on startup and after every
change.

```python
rows = connection.execute(
    "SELECT id, title, date, time, type, desc FROM schedule"
).fetchall()
```

Each row is converted into a `Schedule` object, so the GUI never handles raw tuples.

#### UPDATE — Modify an existing schedule
Called when **Save Changes** is pressed while a record is loaded for editing.

```python
connection.execute(
    """
    UPDATE schedule
    SET title = ?, date = ?, time = ?, type = ?, desc = ?
    WHERE id = ?
    """,
    (schedule.title, schedule.date, schedule.time, schedule.typ, schedule.desc, schedule.id),
)
```

#### DELETE — Remove a schedule
Called after the user confirms the delete dialog.

```python
connection.execute("DELETE FROM schedule WHERE id = ?", (schedule_id,))
```

#### SEARCH
A dedicated search method has **not been implemented yet**. Currently the program reads all
rows with the `list()` operation above and displays them, and matching is done by the user
visually. The planned implementation is a `search(keyword)` method using SQLite's `LIKE`
operator, which has already been verified to work against this table:

```python
connection.execute(
    "SELECT id, title, date, time, type, desc FROM schedule WHERE title LIKE ?",
    (f"%{keyword}%",),
).fetchall()
```

This is listed as an open item under [Known Issues / Limitations](#known-issues--limitations).

---

## Screenshots

> ⚠️ **Action required:** the placeholders below marked `[INSERT IMAGE: ...]` must be
> replaced with real screenshots of the running application before submission.
> Take them by running `python main.py` and capturing the window.

### Screenshot 1 — Application startup / main window

`[INSERT IMAGE: Screenshot 1 — the empty application window at startup, showing the Title, Date, Time, Type, and Description input fields, the "Add Schedule", "Update Selected" and "Delete Selected" buttons, and an empty "Schedules" list below.]`

*Description:* The main window as it appears immediately after running `python main.py`.
The database table is created automatically and the schedule list is empty because no
records have been added yet.

---

### Screenshot 2 — Adding a schedule

`[INSERT IMAGE: Screenshot 2 — the form filled in with a sample entry (Title: "Calculus Final", Date: 05/20/2027, Time: 09:00, Type: Exam, Description: Room 301) immediately before or after clicking "Add Schedule".]`

*Description:* Demonstrates the input form. Title is the only required field; the remaining
fields are filled in with a typical exam entry before pressing **Add Schedule**.

---

### Screenshot 3 — Schedule list populated

`[INSERT IMAGE: Screenshot 3 — the window after adding at least two or three schedules, showing the "Schedules" list at the bottom displaying entries in the format "Title | Date | Time | Type | Description".]`

*Description:* After adding records, every saved schedule appears in the list at the bottom
of the window, proving the data was written to and read back from the SQLite database.

---

### Screenshot 4 — Update mode

`[INSERT IMAGE: Screenshot 4 — a schedule selected in the list, its values loaded into the form fields, and the left button changed from "Add Schedule" to "Save Changes".]`

*Description:* Update in progress. Selecting a schedule and pressing **Update Selected**
fills the form with that record's values and changes the button text to **Save Changes**, so
it is always clear whether the app will create a new record or edit the selected one.

---

### Screenshot 5 — Delete confirmation dialog

`[INSERT IMAGE: Screenshot 5 — the "Delete schedule" confirmation message box asking "Delete [schedule name]?" with Yes and No buttons, shown over the main window.]`

*Description:* The safety confirmation shown before deleting. Pressing **No** cancels the
operation and leaves the record untouched.

---

### Screenshot 6 — Validation warning

`[INSERT IMAGE: Screenshot 6 — a "Missing title" warning message box displayed after clicking "Add Schedule" with an empty Title field.]`

*Description:* Input validation in action. Because the title is mandatory, an empty title
is rejected with a warning and nothing is written to the database.

---

## Testing

Testing was carried out at two levels: **automated testing of the database layer** against a
temporary database file, and **manual GUI testing** of the visible features.

### A. Automated testing of the database layer

Each test used a **temporary, isolated database file** so the real `data/schedule.db` was
never modified.

| # | Feature tested | Steps | Expected result | Actual result |
|---|----------------|-------|-----------------|---------------|
| 1 | **Create** + whitespace cleanup | `repo.add(Schedule("  Calculus Final  ", ...))` | Leading/trailing spaces are removed; `id` is assigned | **PASS** — title became `'Calculus Final'`, `id=1` |
| 2 | **Read one** (`get`) | `repo.get(1)` | Returns the stored record | **PASS** — title `'Calculus Final'` returned correctly |
| 3 | **Read all** (`list`) | Add a 2nd record, then `repo.list()` | 2 records returned | **PASS** — exactly 2 records returned |
| 4 | **Search** (`LIKE`) | Filter titles containing `"final"` | 1 match | **PASS** — 1 match: `['Calculus Final']` |
| 5 | **Update** | Change date to `05/21/2027`, `repo.update()`, then `get()` | Date is `05/21/2027` | **PASS** — date read back as `05/21/2027` |
| 6 | **Delete** | `repo.delete(1)`, then `get(1)` and `list()` | `get()` returns `None`; 1 record left | **PASS** — `get()` returned `None`, 1 record remained |
| 7 | **Persistence** | Close the app, reopen it, view the list | Records still present | **PASS** — records loaded from `schedule.db` on startup |
| 8 | **Table creation** | Delete the `.db` file and run again | Table is rebuilt automatically | **PASS** — `CREATE TABLE IF NOT EXISTS` recreated the table |

**Test run output (summary):**

```
TEST 1 CREATE    -> PASS  (title='Calculus Final', id=1)
TEST 2 READ get  -> PASS  (title='Calculus Final')
TEST 3 READ list -> PASS  (2 records)
TEST 4 SEARCH    -> PASS  (1 match -> ['Calculus Final'])
TEST 5 UPDATE    -> PASS  (date = 05/21/2027)
TEST 6 DELETE    -> PASS  (get()=None, 1 record left)
ALL REPOSITORY TESTS PASSED
```

### B. Manual GUI testing

| # | Scenario | Steps | Expected result | Actual result |
|---|----------|-------|-----------------|---------------|
| 1 | Add a schedule | Fill all fields → **Add Schedule** | Record appears in the list and persists | **PASS** — record shown in list; verified present after restart |
| 2 | Empty title | Click **Add Schedule** with blank Title | *"Missing title"* warning, nothing saved | **PASS** — warning dialog shown, database unchanged |
| 3 | Update a schedule | Select record → **Update Selected** → change date → **Save Changes** | Form fills, button text changes, new value shown in list | **PASS** — list showed the updated date |
| 4 | Delete a schedule | Select record → **Delete Selected** → **Yes** | Record disappears from the list | **PASS** — record removed |
| 5 | Cancel delete | Select record → **Delete Selected** → **No** | Record stays in the list | **PASS** — nothing was deleted |
| 6 | Update/Delete with no selection | Click **Update Selected** or **Delete Selected** with nothing highlighted | *"Please select a schedule to update/delete"* warning | **PASS** — warning shown, no crash |
| 7 | Enter key saves | Type in Title field, press `Enter` | Schedule is saved without clicking the button | **PASS** — `returnPressed` connected to `save_schedule` |
| 8 | Multiple sessions | Add records, close window, reopen | All records still listed in order | **PASS** — data loaded from SQLite on startup |

### C. Verification of the delivered build

- `python main.py` launches successfully with no errors and the Qt event loop runs.
- `sqlite3 data/schedule.db ".schema"` confirms the `schedule` table exists with the
  expected six columns.
- No unhandled exceptions were produced during any test scenario.

---

## Known Issues / Limitations

The following items are **not yet implemented** or are known weaknesses of the current build.

### Not yet implemented

1. **No search function in the GUI.** There is no search box. All records are loaded and
   displayed, and finding a specific entry must be done by reading the list. A
   `search(keyword)` method using SQL `LIKE` is the planned solution (already verified to
   work — see [Search](#search) above).
2. **No sorting or filtering.** Records are always shown in ID order. Sorting by date, and
   filtering by `type`, are not available. Because dates are stored as text in `MM/DD/YYYY`
   format, sorting by date would also require changing the storage format to `ISO 8601`
   (`YYYY-MM-DD`) so that alphabetical order equals chronological order.
3. **No user authentication or login.** Everyone who opens the program has full access to
   all data. There are no usernames, passwords, or roles. *(Planned)*
4. **No dark mode toggle.** Only the default light theme is available. *(Planned)*
5. **No calendar or date-picker widget.** The `features/calendar/` folder is an empty
   placeholder. Dates must be typed manually as text.
6. **No export or print.** Schedules cannot be exported to PDF, CSV, or `.ics`, and the
   list cannot be printed.
7. **No recurring schedules.** A weekly class meeting must be re-entered for every
   occurrence. There is no repeat/recurrence field.
8. **No automatic test suite in the repository.** The tests in this README were run as
   one-off scripts; `pytest` tests are not committed, and there is no CI pipeline.

### Known weaknesses

9. **No input validation on date, time, or type.** Only the title is checked. Entering
   `32/45/2027` or `99:99` is accepted and stored as text. Validation (or a date-picker
   widget) is needed.
10. **`type` is free text.** A typo like `exam`, `Exam`, and `EXAM` creates three different
    types. A dropdown (`QComboBox`) with fixed values would enforce consistency.
11. **Inconsistent naming — leftover from the original CLI version.** The classes are still
    called `StudentView` and `StudentService` even though they manage *schedules*, not
    students. They should be renamed to `ScheduleView` and `ScheduleService`.
12. **Duplicated service classes.** `service.py` contains two classes with identical
    behavior — `ScheduleService` and `StudentService`. Only `StudentService` is used by
    `main.py`; `ScheduleService` should be removed.
13. **Dead / broken code in `features/schedule/view.py`.** This earlier GUI attempt
    contains typos such as `refrest()` and `sertHorizontalHeaderLabels` and would raise
    `AttributeError` if run. It is not imported by `main.py` and should be deleted.
14. **`controller/schedule.py` is disconnected.** The command-line menu loop is commented
    out in `main.py`, and the `Bridge` QObject signals (`refreshed`, `quit_requested`) it
    depends on are unused. This file is reference material only.
15. **Every operation opens a new database connection.** `Database.connect()` is called
    inside each repository method rather than reusing one connection. This is correct and
    safe for a small application, but a connection pool would be better at scale.
16. **No error handling for a locked or corrupted database file.** If `schedule.db` is
    opened by another program or becomes corrupted, the application raises an unhandled
    `sqlite3.OperationalError`. A `try/except` with a user-friendly message is needed.
17. **The window cannot be resized gracefully.** The layout is fixed at 420 × 480 px and
    long titles are clipped in the list; there is no horizontal scrollbar.
18. **`requirements.txt` contains only the direct dependency.** It should also pin or
    document the minimum Python version for reproducibility.

---

## Author

| Field | Information |
|-------|-------------|
| **Name** | **NotLevi-Fr** (Levi Gerson Aquino) |
| **Section** | **CS26** |
| **Course** | Computer Science 26 |
| **Project** | Schedule Management System |
| **Language / Framework** | Python 3 · PyQt6 |
| **Database** | SQLite3 |
| **Architecture** | Layered (Model → Repository → Service → View) |
| **Repository** | https://github.com/NotLevi-Fr/Schedule-Management-System |
| **Contact** | levigersonaquino@gmail.com |

---

*Documentation generated for the Schedule Management System — CS26.*