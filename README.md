# Schedule Management System

> **Status:** Working — add, view, update, and delete are done.
> A desktop app for recording schedules and deadlines, stored in a local SQLite database.

---

## About This Project

**Scheduling apps already exist, and many are free.** This is not a claim to replace them.
It exists for three reasons:

**1. Built for personal use.**
I made it for myself, to solve my own scheduling problem my way. No client, no requirements
document. It stays small, fast, and free of accounts, subscriptions, ads, and internet needs.
It runs fully offline.

**2. Built to be modified.**
The layering (Model → Repository → Service → View) exists for *modifiability*. Each part
changes on its own:

- Swap SQLite for PostgreSQL — edit only `data/data.py` and `features/schedule/repository.py`.
- Swap PyQt6 for web or mobile — rewrite only the view layer; model, service, and database stay.
- Change a schedule's fields — edit only `features/schedule/model.py`.
- Add the calendar view without breaking existing features.

The goal is code that is easy to read, change, and learn from — not a finished product.

**3. Open source.**
Public so anyone can read, copy, learn from, improve, or use as a starting point. Forks,
issues, and pull requests are welcome.

> **Licensing note:** there is no `LICENSE` file yet, so the code is publicly readable but
> **not** formally licensed for reuse. To reuse or redistribute it, add a license —
> [MIT](https://opensource.org/license/mit) is the usual fit, since it allows modification
> and reuse as long as the original credit is kept.

---

## Table of Contents

1. [About This Project](#about-this-project)
2. [Project Description](#project-description)
3. [Project Objectives](#project-objectives)
4. [Features](#features)
5. [Technologies Used](#technologies-used)
6. [Project Structure](#project-structure)
7. [Installation and Setup](#installation-and-setup)
8. [How to Use the System](#how-to-use-the-system)
9. [OOP Implementation](#oop-implementation)
10. [Database](#database)
11. [Screenshots](#screenshots)
12. [Testing](#testing)
13. [Known Issues / Limitations](#known-issues--limitations)
14. [Author](#author)
15. [Contributing](#contributing)

---

## Project Description

### What it does

A desktop GUI app that keeps every important date in one place, instead of on paper or in
memory. Each entry stores a **title, date, time, type, and description**, saved to a local
SQLite file so nothing is lost when the program closes.

It started as a command-line project (`controller/schedule.py`), then became a PyQt6 window
(`view/student_view.py`) on top of the same database layer.

### The problem it addresses

Tracking schedules by hand fails in predictable ways:

- **Deadlines get missed.** Nothing reminds you when a quiz or exam is coming.
- **Paper gets lost or damaged.** No backup, no way to search old notes.
- **Entries are hard to fix.** A changed date means crossing out and rewriting.
- **Everything scatters.** Class schedules, exams, and assignments end up across notebooks,
  group chats, and posters.

This app puts all of it in one window, where every entry can be created, read, updated,
deleted, and reviewed at a glance.

---

## Project Objectives

1. Give a simple desktop app for recording personal and academic schedules.
2. Persist data in a real relational database (SQLite), not a temp file or memory list.
3. Apply **encapsulation, inheritance, and polymorphism** by separating the program into
   layers.
4. Give each layer one clear responsibility:
   - **Model** – holds the data of one schedule
   - **Repository** – performs all SQL
   - **Service** – business logic between GUI and database
   - **View** – the graphical interface
   - **Calendar** – the upcoming calendar and color coding feature
5. Use parameterized SQL to prevent SQL injection.
6. Keep the interface usable without training.
7. Give clear feedback through dialogs and warnings.
8. Show schedules in a **calendar view with color coding**, so deadlines are visible at a
   glance and types are distinguishable.

---

## Features

### Current (working)

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Add Schedule** | Fill in title, date, time, type, and description, then press **Add Schedule** to save a record. |
| 2 | **View Schedules** | Saved schedules list in the window as `Title \| Date \| Time \| Type \| Description`. |
| 3 | **Update Schedule** | Select a schedule → **Update Selected** → it loads into the form → edit → save. |
| 4 | **Delete Schedule** | Select a schedule → **Delete Selected**. A confirmation dialog prevents accidents. |
| 5 | **Save Data** | Everything is stored in SQLite and survives closing the app. |
| 6 | **Calendar View** | Schedules appear as color-coded dates on a monthly calendar. Click a date to list that day's schedules in a table, sorted by time. |
| 7 | **Color Coding** | Each schedule type gets its own color, so exams, quizzes, and activities are distinguishable at a glance. Days with mixed types turn grey. |

The app has two tabs: **Schedules** (features 1–5) and **Calendar** (features 6–7).

### Still planned

- Login and user accounts
- Dark mode toggle
- Export to PDF / CSV / `.ics`
- Recurring schedules
- Sorting and filtering

---

## Technologies Used

| Category | Technology | Details |
|----------|-----------|---------|
| **Language** | Python 3 | Written and tested on 3.14.7 |
| **GUI Framework** | PyQt6 | 6.11.0 — `QWidget`, `QLineEdit`, `QListWidget`, `QPushButton`, `QMessageBox`, `QVBoxLayout`, `QFormLayout` |
| **Database** | SQLite3 | Built-in `sqlite3` module. File-based, no server. |
| **Other Libraries** | `dataclasses` (stdlib) | Builds the `Schedule` model via `@dataclass` |
| **Other Libraries** | `pathlib` (stdlib) | Builds the cross-platform path to `schedule.db` |
| **Other Tools** | Qt Signals / Slots | `pyqtSignal` and `.connect()` link events to methods |
| **Version Control** | Git | Hosted on GitHub |

> PyQt5 is installed in the same environment but **not used**. All imports use `PyQt6`.

---

## Project Structure

```
ScheduleManagementSystem/
│
├── main.py                      # Entry point — creates Database, Service, View; starts Qt
├── README.md                    # This documentation
├── REPORT.md                    # Earlier command-line version report
├── requirements.txt             # Dependencies
│
├── controller/
│   ├── __init__.py
│   └── schedule.py              # CLI version: get_schedule(), show_schedule(), delete_schedule()
│
├── data/                        # DATABASE LAYER
│   ├── __init__.py
│   ├── data.py                  # Database class — holds DB path, creates the table
│   └── schedule.db              # SQLite file (auto-created on first run)
│
├── features/                    # FEATURE MODULES
│   ├── __init__.py
│   ├── calendar/                # Calendar feature (implemented)
│   │   ├── __init__.py          # Exports CalendarView, parse_date
│   │   ├── colors.py            # Schedule type → color mapping, aliases, legend data
│   │   ├── dates.py             # parse_date() — turns stored text into a real date
│   │   └── view.py              # CalendarView — the calendar window with color coding
│   └── schedule/                # Schedule feature
│       ├── __init__.py
│       ├── model.py             # Schedule dataclass — data of ONE schedule
│       ├── repository.py        # ScheduleRepository — all SQL (Create/Read/Update/Delete)
│       ├── service.py           # Service classes — business logic
│       └── view.py              # Unused early GUI attempt (superseded by view/)
│
└── view/                        # PRESENTATION LAYER
    ├── __init__.py              # Exports StudentView
    └── student_view.py          # StudentView — the actual application window
```

### Purpose of each file

| File / Folder | Purpose |
|---------------|---------|
| `main.py` | Entry point. Builds the `Database`, `StudentService`, and `StudentView`, then starts the Qt loop. |
| `controller/schedule.py` | The original command-line version. Reference only — its loop is commented out in `main.py`. |
| `data/data.py` | `Database` class. Holds the DB path, opens connections, creates the table. |
| `data/schedule.db` | The SQLite file storing all schedules. Auto-created — never edit by hand. |
| `features/schedule/model.py` | `Schedule` dataclass (`title`, `date`, `time`, `typ`, `desc`, `id`). Strips whitespace in `__post_init__`. |
| `features/schedule/repository.py` | `ScheduleRepository`. Holds **all** SQL with parameterized queries. Converts rows into `Schedule` objects. |
| `features/schedule/service.py` | Business logic. `ScheduleService` and `StudentService` pass GUI requests to the repository. |
| `features/schedule/view.py` | Unfinished early GUI attempt with typos (`refrest()`, `sertHorizontalHeaderLabels`). **Not imported by `main.py`.** |
| `view/student_view.py` | The real window (`StudentView`). Builds the form, buttons, and list; handles add/update/delete/refresh. |
| `features/calendar/dates.py` | `parse_date()` — converts stored date text (`MM/DD/YYYY`) into a real `date`, returning `None` if it can't. |
| `features/calendar/colors.py` | Maps a schedule type to its background/foreground colors. Handles case, spacing, and aliases (`homework` → assignment). |
| `features/calendar/view.py` | `CalendarView`. Builds the calendar, color-codes dates, and lists the selected day's schedules. |
| `features/calendar/` | The calendar feature package. Depends on the existing model and database layers. |

---

## Installation and Setup

### Dependencies

```
Python   >= 3.10   (tested on 3.14.7)
PyQt6    >= 6.5    (tested on 6.11.0)
sqlite3            (bundled with Python)
```

Only **PyQt6** needs manual install. `sqlite3`, `dataclasses`, and `pathlib` ship with Python.

### Steps

**1. Clone**

```bash
git clone https://github.com/NotLevi-Fr/Schedule-Management-System.git
cd ScheduleManagementSystem
```

**2. Virtual environment (recommended)**

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

**3. Install**

```bash
pip install PyQt6
# or
pip install -r requirements.txt
```

**4. Run**

```bash
python main.py
```

**5. Verify the database**

`data/schedule.db` is created automatically on first run:

```bash
sqlite3 data/schedule.db ".tables"
# Expected: schedule
```

> **Linux only:** if the app won't start, install system libraries:
> `sudo apt install libxcb-xinerama0 libxkbcommon-x11-0 libxcb-cursor0`

---

## How to Use the System

1. **Start** — run `python main.py`. A *"Schedule Management System"* window opens
   (420 × 480 px).

2. **Add a schedule**
   - **Title** (required), e.g. `Calculus Final`
   - **Date** as `MM/DD/YYYY`, e.g. `05/20/2027`
   - **Time** as 24-hour `HH:MM`, e.g. `09:00`
   - **Type**, e.g. `Exam`, `Activity`, `Assignment`
   - **Description** (optional)
   - Click **Add Schedule**, or press `Enter` in the Title field

3. **View** — saved schedules appear in the list at the bottom as
   `Title | Date | Time | Type | Description`.

4. **Update**
   - Click a schedule to select it.
   - Click **Update Selected**. The form fills, and the left button becomes **Save Changes**.
   - Edit, then click **Save Changes**. The list refreshes.

5. **Delete**
   - Click a schedule to select it.
   - Click **Delete Selected**.
   - Confirm in the dialog. **Yes** deletes, **No** cancels.

6. **See the calendar** — click the **Calendar** tab.
   - Each date with a schedule is **color-coded by type** (see the legend at the bottom).
   - Dates with more than one schedule are **grey**, and hovering shows how many and which types.
   - Click any date to list that day's schedules below, sorted by time.
   - Use the arrows to move between months.
   - Changes made on the **Schedules** tab appear here automatically when you switch to this tab.

7. **Quit** — close the window. Data is already saved.

### Tips

- **Enter** in the Title field saves, so the whole form works by keyboard.
- Dates are stored as text — always use `MM/DD/YYYY` and 24-hour `HH:MM` to keep entries
  consistent.

---

## OOP Implementation

The project uses **encapsulation**, **inheritance**, and **polymorphism** across a layered
architecture:

```
StudentView (GUI)  →  StudentService (logic)  →  ScheduleRepository (SQL)  →  Database (SQLite)
       ↑                                                                            │
       └────────────────────  Schedule object returned  ←───────────────────────────┘
```

### Classes

| Class | File | Type / Base | Responsibility |
|-------|------|-------------|----------------|
| `Schedule` | `features/schedule/model.py` | `@dataclass` | Data of **one** schedule: `title`, `date`, `time`, `typ`, `desc`, `id`. |
| `Database` | `data/data.py` | Plain class | Owns the DB path, opens connections, creates the table. |
| `ScheduleRepository` | `features/schedule/repository.py` | Plain class | Executes **all** SQL. Converts rows → `Schedule`. |
| `ScheduleService` | `features/schedule/service.py` | Plain class | Business-logic facade for the original CLI/early GUI. |
| `StudentService` | `features/schedule/service.py` | Plain class | Business-logic facade for the current GUI. |
| `StudentView` | `view/student_view.py` | **inherits `QWidget`** | The Schedules tab; builds widgets, handles actions. |
| `CalendarView` | `features/calendar/view.py` | **inherits `QWidget`** | The Calendar tab; color-codes dates, lists the selected day. |
| `ScheduleView` | `features/schedule/view.py` | **inherits `QWidget`** | Unused early GUI attempt. |
| `Bridge` | `main.py` | **inherits `QObject`** | Holds Qt signals for the commented-out CLI thread. |

### 1. Encapsulation

Every layer keeps its own responsibility private and exposes a small public interface.

- **`Database` encapsulates storage details.** The path and connection logic stay inside the
  class. No other class knows the file is `schedule.db` or that it lives in `data/`.

  ```python
  class Database:
      def __init__(self, database_path=None):
          if database_path is None:
              database_path = Path(__file__).resolve().parent / "schedule.db"
          self.database_path = Path(database_path)   # private detail
          self.create_table()

      def connect(self) -> sqlite3.Connection:      # controlled access
          return sqlite3.connect(self.database_path)
  ```

- **`ScheduleRepository` encapsulates all SQL.** The most important example. No SQL appears
  anywhere else, so the database can change without touching the GUI or service.

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
  `ScheduleRepository`; it only calls `add`, `update`, `delete`, `get`, or `list`.

- **`Schedule` encapsulates its own cleanup.** Messy input is normalized in
  `__post_init__`, so every `Schedule` is clean.

  ```python
  @dataclass
  class Schedule:
      title: str
      # ...
      def __post_init__(self) -> None:
          self.title = self.title.strip()   # cleanup happens automatically
  ```

- **`CalendarView` encapsulates calendar state.** It owns the calendar widget, the grouping
  of schedules by day, and the set of dates it has already painted. `main.py` never has to
  know that days are grouped or that colors must be cleared before repainting — it only
  constructs the view.

- **`StudentView` encapsulates form state.** It owns its widgets, the `editing_id` flag,
  and helpers (`clear_form()`, `fill_form()`, `read_form()`, `fields()`), so nothing else
  touches raw widget text.

### 2. Inheritance

- **`StudentView(QWidget)`** inherits PyQt6's window, title bar, layout system, and ability
  to be shown. `super().__init__()` runs first, then window setup on top of it.

  ```python
  class StudentView(QWidget):
      def __init__(self, service: StudentService):
          super().__init__()                     # initialise the base class
          self.service = service
          self.setWindowTitle("Schedule Management System")
          self.resize(420, 480)
  ```

- **`CalendarView(QWidget)`** — inherits PyQt6's window, title bar, layout system, and
  ability to be shown, exactly like `StudentView`. Both tabs are plain `QWidget`
  subclasses placed inside a `QTabWidget`, which is why they can coexist.

- **`ScheduleView(QWidget)`** — same pattern in the legacy view.
- **`Bridge(QObject)`** — inherits `QObject` so it can own `pyqtSignal` objects.
- **Implicit** — `ScheduleService`, `StudentService`, `ScheduleRepository`, and `Database`
  all inherit Python's `object`.

> **Honest note:** inheritance is used mainly for **GUI widgets**, which is correct in PyQt6.
> The data layers are composed, not inherited (`has-a`): repository *has-a* `Database`,
> service *has-a* repository, view *has-a* service. Deep hierarchies were deliberately
> avoided — they aren't needed at this size.

### 3. Polymorphism

- **Method overriding (`StudentView.show`).** It overrides `QWidget.show()` to take an extra
  parameter and refresh first. Calling `window.show(1)` runs the overridden version.

  ```python
  def show(self, index: int = 0) -> None:
      self.refresh()       # load data from the database into the list
      super().show()       # then let QWidget show the window
  ```

- **Method overriding (`CalendarView.showEvent`).** `CalendarView` overrides Qt's
  `showEvent()` to reload from the database whenever the tab becomes visible. This is why
  schedules added on the Schedules tab show up on the Calendar tab without any manual
  wiring between the two.

  ```python
  def showEvent(self, event) -> None:
      super().showEvent(event)   # let QWidget handle the event first
      self.refresh()             # then reload the calendar from the database
  ```

- **Qt signal/slot (event-driven).** Buttons aren't told which method to call; they emit
  signals and Qt dispatches to whatever is connected. One handler can serve several widgets
  and can be swapped without touching UI code.

  ```python
  self.save_button.clicked.connect(self.save_schedule)         # mouse click
  self.title_input.returnPressed.connect(self.save_schedule)  # Enter key

  self.calendar.selectionChanged.connect(self.show_selected_day)   # click a date
  self.calendar.currentPageChanged.connect(self.refresh)           # change month
  ```

- **Duck typing in the repository.** `get()` and `list()` build `Schedule` objects from
  differently shaped results (one row vs. many) through the same constructor. The code
  works with whatever it gets.

- **Uniform interface.** `ScheduleService` and `StudentService` expose the same behavior
  (`add`, `update`, `delete`, `get`, `list`) over the same objects, so code written against
  one works unchanged against the other.

---

## Database

### Engine

**SQLite3**, via Python's built-in `sqlite3`. Chosen because it needs no install, no server,
and no config — the whole database is one file (`data/schedule.db`). That fits a personal,
single-user desktop app.

### Structure

One table, created by `Database.create_table()` in `data/data.py` using
`CREATE TABLE IF NOT EXISTS`. It's built automatically on first run — no manual setup.

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

### Table: `schedule`

| Column | Type | Constraint | Description |
|--------|--------|------------|-------------|
| `id` | INTEGER | **PRIMARY KEY AUTOINCREMENT** | Unique ID, auto-generated. Used for update and delete. |
| `title` | TEXT | validated in GUI: not empty | Name of the schedule. |
| `date` | TEXT | — | Entered as `MM/DD/YYYY`. |
| `time` | TEXT | — | Entered as `HH:MM`. |
| `type` | TEXT | — | Category: Exam, Activity, Assignment, Quiz, etc. |
| `desc` | TEXT | — | Optional extra details. |

> **Why SQLite?** No install, no server, no config — one file. For a personal, offline,
> single-user tool it's the simplest option that's still a real relational database. Because
> SQL is confined to the repository layer, moving to PostgreSQL or MySQL later is a change to
> one file, not a rewrite.

> SQLite also creates an internal `sqlite_sequence` table for `AUTOINCREMENT`. It's a
> built-in system table, unused by the app.

### Diagram

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

No foreign keys — the system has one entity, so one table is enough.

### Operations

All SQL lives in `features/schedule/repository.py`. Every statement uses **parameterized
queries** (`?` placeholders), so user input is never treated as SQL — this prevents SQL
injection.

#### CREATE — Add a schedule
Called by **Add Schedule**.

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

#### READ — Get one by ID
Called by **Update Selected** to fill the form.

```python
row = connection.execute(
    "SELECT id, title, date, time, type, desc FROM schedule WHERE id = ?",
    (schedule_id,),
).fetchone()
```

Returns `None` if no row matches, which the view reports as *"That schedule no longer
exists"*.

#### READ — List all
Called by `StudentView.refresh()` on startup and after every change.

```python
rows = connection.execute(
    "SELECT id, title, date, time, type, desc FROM schedule"
).fetchall()
```

Each row becomes a `Schedule`, so the GUI never handles raw tuples.

#### UPDATE — Modify a schedule
Called by **Save Changes** while a record is loaded.

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
Called after the user confirms.

```python
connection.execute("DELETE FROM schedule WHERE id = ?", (schedule_id,))
```

#### SEARCH
Not implemented yet. The app currently reads all rows via `list()` and the user matches
visually. The plan is a `search(keyword)` method using SQLite's `LIKE`, already verified to
work against this table:

```python
connection.execute(
    "SELECT id, title, date, time, type, desc FROM schedule WHERE title LIKE ?",
    (f"%{keyword}%",),
).fetchall()
```

Tracked under [Known Issues / Limitations](#known-issues--limitations).

---

## Screenshots

> ⚠️ **Action required:** every `[INSERT IMAGE: ...]` placeholder below must be replaced
> with a real screenshot before submission. Run `python main.py` and capture the window.

### Screenshot 1 — Startup

`[INSERT IMAGE: the empty window on startup — Title, Date, Time, Type, Description fields; "Add Schedule", "Update Selected", "Delete Selected" buttons; empty Schedules list below.]`

*The window right after running `python main.py`. The table is created automatically and the
list is empty because nothing has been added yet.*

---

### Screenshot 2 — Adding a schedule

`[INSERT IMAGE: the form filled with a sample entry — Title: "Calculus Final", Date: 05/20/2027, Time: 09:00, Type: Exam, Description: Room 301 — just before clicking "Add Schedule".]`

*The input form. Only the title is required; the rest shows a typical exam entry.*

---

### Screenshot 3 — List populated

`[INSERT IMAGE: the window after adding two or three schedules, showing the Schedules list displaying entries as "Title | Date | Time | Type | Description".]`

*Saved records appear in the list, proving the data was written to and read back from SQLite.*

---

### Screenshot 4 — Update mode

`[INSERT IMAGE: a schedule selected in the list, its values loaded into the form, and the left button changed from "Add Schedule" to "Save Changes".]`

*Update in progress. The form is filled and the button text makes it clear the app will edit
the selected record, not create a new one.*

---

### Screenshot 5 — Delete confirmation

`[INSERT IMAGE: the "Delete schedule" dialog asking "Delete [schedule name]?" with Yes and No, over the main window.]`

*The safety confirmation before deleting. **No** cancels and leaves the record untouched.*

---

### Screenshot 6 — Validation warning

`[INSERT IMAGE: a "Missing title" warning after clicking "Add Schedule" with an empty Title field.]`

*Validation in action. An empty title is rejected and nothing is written to the database.*

---

### Screenshot 7 — Calendar view with color coding

`[INSERT IMAGE: the "Calendar" tab — a monthly calendar with schedule dates colored by type (for example a red exam date and a blue assignment date), a legend along the bottom, and the table below showing the selected day's schedules.]`

*The calendar tab. Each date is colored by its schedule type, grey means several types that day,
and clicking a date lists its schedules sorted by time.*

---

### Screenshot 8 — Day detail with legend

`[INSERT IMAGE: a single date selected on the calendar, with the "Day, Month DD, YYYY — N schedule(s)" label and a table of Time / Type / Title / Description rows for that day, with the legend row visible.]`

*Selecting a date lists its schedules. Each row carries the same color as its calendar date, so
the table and the calendar are read the same way.*

---

## Testing

Two levels: **automated** testing of the database layer against a temp file, and **manual**
GUI testing.

### A. Automated — database layer

Each test used a **temporary, isolated database file**, so the real `data/schedule.db` was
never modified.

| # | Feature | Steps | Expected | Actual |
|---|---------|-------|----------|--------|
| 1 | **Create** + whitespace cleanup | `repo.add(Schedule("  Calculus Final  ", ...))` | Spaces removed; `id` assigned | **PASS** — title `'Calculus Final'`, `id=1` |
| 2 | **Read one** (`get`) | `repo.get(1)` | Returns the record | **PASS** — title `'Calculus Final'` |
| 3 | **Read all** (`list`) | Add a 2nd record, then `repo.list()` | 2 records | **PASS** — exactly 2 returned |
| 4 | **Search** (`LIKE`) | Filter titles containing `"final"` | 1 match | **PASS** — 1 match: `['Calculus Final']` |
| 5 | **Update** | Set date to `05/21/2027`, `update()`, then `get()` | Date is `05/21/2027` | **PASS** — read back as `05/21/2027` |
| 6 | **Delete** | `delete(1)`, then `get(1)` and `list()` | `get()` → `None`; 1 record left | **PASS** — `None`, 1 remained |
| 7 | **Persistence** | Close app, reopen, view list | Records still present | **PASS** — loaded from `schedule.db` on startup |
| 8 | **Table creation** | Delete the `.db` file, run again | Table rebuilt automatically | **PASS** — `CREATE TABLE IF NOT EXISTS` recreated it |

```
TEST 1 CREATE    -> PASS  (title='Calculus Final', id=1)
TEST 2 READ get  -> PASS  (title='Calculus Final')
TEST 3 READ list -> PASS  (2 records)
TEST 4 SEARCH    -> PASS  (1 match -> ['Calculus Final'])
TEST 5 UPDATE    -> PASS  (date = 05/21/2027)
TEST 6 DELETE    -> PASS  (get()=None, 1 record left)
ALL REPOSITORY TESTS PASSED
```

### B. Manual — GUI

| # | Scenario | Steps | Expected | Actual |
|---|----------|-------|----------|--------|
| 1 | Add a schedule | Fill all fields → **Add Schedule** | Record appears in the list and persists | **PASS** — shown in list; present after restart |
| 2 | Empty title | **Add Schedule** with blank Title | *"Missing title"* warning, nothing saved | **PASS** — warning shown, database unchanged |
| 3 | Update | Select → **Update Selected** → change date → **Save Changes** | Form fills, button changes, new value listed | **PASS** — list showed the updated date |
| 4 | Delete | Select → **Delete Selected** → **Yes** | Record disappears from the list | **PASS** — record removed |
| 5 | Cancel delete | Select → **Delete Selected** → **No** | Record stays | **PASS** — nothing deleted |
| 6 | No selection | **Update** or **Delete** with nothing highlighted | *"Please select a schedule"* warning | **PASS** — warning shown, no crash |
| 7 | Enter key saves | Type in Title, press `Enter` | Saved without clicking | **PASS** — `returnPressed` → `save_schedule` |
| 8 | Multiple sessions | Add records, close, reopen | All records still listed in order | **PASS** — loaded from SQLite on startup |

### C. Automated — calendar feature

Tested headless against an isolated database file, exercising `parse_date`, `colors`, and
`CalendarView` directly.

| # | Feature | Steps | Expected | Actual |
|---|---------|-------|----------|--------|
| 9 | **Date parsing** | `parse_date("04/20/2027")`, `" 8/4/2027 "`, `"2027-08-04"` | Correct `date` objects | **PASS** — all three parsed (single-digit months/days work) |
| 10 | **Bad dates skipped** | `parse_date("99/99/2027")`, `"banana"`, `""` | `None`, never a crash | **PASS** — all returned `None` |
| 11 | **Color by type** | `color_pair("quiz")`, `"EXAM"`, `"homework"`, `"banana"` | Correct color per type | **PASS** — quiz orange, exam red, `homework`→assignment blue, unknown grey |
| 12 | **Grouping by day** | Add 5 schedules, 1 with an invalid date | 3 valid day-groups; invalid skipped | **PASS** — `2027-05-20` (2), `2027-06-01` (1), `2027-07-04` (1) |
| 13 | **Day detail sorted** | Select `05/20/2027` (09:00 exam, 13:00 assignment) | Table shows 2 rows, earliest time first | **PASS** — 09:00 Exam, then 13:00 Assignment |
| 14 | **Empty day** | Select `05/21/2027` | Label shows 0, table empty | **PASS** — 0 rows, no error |
| 15 | **Mixed types** | Day with 2 schedules | Date turns grey, tooltip lists both types | **PASS** — grey `#e5e7eb`, tooltip `"2 schedule(s): Exam, Assignment"` |
| 16 | **Cross-tab refresh** | Add via the Schedules tab, switch to Calendar | New record visible | **PASS** — appeared without restarting |
| 17 | **Cross-tab update** | Rename via the Schedules tab, switch to Calendar | New title shown | **PASS** — `Physics Quiz (moved)` |
| 18 | **Cross-tab delete** | Delete via the Schedules tab, switch to Calendar | Day no longer listed | **PASS** — group emptied, no stale color |

### D. Delivered build

- `python main.py` launches with no errors; both tabs are present.
- `sqlite3 data/schedule.db ".schema"` confirms the `schedule` table and its six columns.
- No unhandled exceptions in any scenario.

---

## Known Issues / Limitations

### Not yet implemented

1. **No search in the GUI.** No search box — all records load and the user reads the list.
   A `search(keyword)` method using `LIKE` is the plan (verified to work — see
   [Search](#search)).
2. **No sorting or filtering.** Records always show in ID order. Sorting by date also needs
   dates stored as `ISO 8601` (`YYYY-MM-DD`) so alphabetical order equals chronological order.
   Within a single calendar day, schedules *are* sorted by time.
3. **No authentication.** Anyone opening the app has full access. No accounts or roles.
   *(Planned)*
4. **No dark mode.** Default light theme only. *(Planned)*
5. **No export or print.** No PDF, CSV, or `.ics` export, and no printing.
6. **No recurring schedules.** A weekly meeting must be re-entered each time. No repeat field.
7. **No committed test suite.** The tests here ran as one-off scripts; no `pytest` files, no
   CI pipeline.

### Known weaknesses

8. **No validation on date, time, or type.** Only the title is checked. `32/45/2027` and
   `99:99` are accepted and stored as text — a bad date silently disappears from the calendar
   because `parse_date()` returns `None` for it. Needs validation or a date-picker.
9. **`type` is still free text.** The calendar copes by normalizing case and mapping aliases
   (`homework` → assignment), and unknown types fall back to grey. But `exam`, `Exam`, and
   `EXAM` are still three separate strings. A `QComboBox` dropdown on the add form would fix
   this properly and guarantee every type has a color.
10. **Multi-type days lose their color.** A date with more than one schedule type is drawn
    grey, because a single date cell can only hold one background color. A side-by-side list
    of chips per day would show all its colors at once.
11. **Inconsistent naming.** Classes are `StudentView` and `StudentService` but manage
    *schedules*. Should be `ScheduleView` and `ScheduleService`.
12. **Duplicated services.** `service.py` has two identical classes. Only `StudentService` is
    used by `main.py`; `ScheduleService` should go.
13. **Dead code in `features/schedule/view.py`.** Typos like `refrest()` and
    `sertHorizontalHeaderLabels` would raise `AttributeError`. Not imported — should be deleted.
14. **`controller/schedule.py` is disconnected.** Its menu loop is commented out in
    `main.py`, and the `Bridge` signals it needs are unused. Reference only.
15. **New connection per operation.** `Database.connect()` runs inside each repository method
    instead of reusing one. Fine for a small app; a pool scales better.
16. **No handling for a locked or corrupt DB file.** An unhandled `sqlite3.OperationalError`
    would crash. Needs `try/except` with a friendly message.
17. **No validation feedback for skipped dates.** When a schedule has an unreadable date it
    simply does not appear on the calendar, with no warning. Worth showing a count like
    "2 schedules could not be placed on the calendar".
18. **`requirements.txt` lists only the direct dependency.** It should also pin the minimum
    Python version.

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
| **License** | Open source — free to use, copy, modify, share. See [Contributing](#contributing). |

---

## Contributing

Open source — contributions welcome.

- **Use it** — if it's useful to you, that's reason enough.
- **Report bugs** — open an issue with what happened and what you expected.
- **Suggest features** — especially anything that improves personal scheduling.
- **Improve the code** — fork and open a pull request.
- **Learn from it** — a reference for a small layered PyQt6 app.

Changes that keep it small, offline, and dependency-free are preferred over ones that add
complexity.

---

*Documentation for the Schedule Management System — CS26.*