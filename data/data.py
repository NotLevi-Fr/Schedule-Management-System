import sqlite3
from pathlib import Path


class Database:
    def __init__(self, database_path: str | Path | None = None):
        if database_path is None:
            database_path = Path(__file__).resolve().parent / "schedule.db"
        self.database_path = Path(database_path)
        self.create_table()

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def create_table(self) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS schedule (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    date TEXT,
                    time TEXT,
                    type TEXT,
                    desc TEXT
                )
                """
            )
