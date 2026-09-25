from data.data import Database

from .model import Schedule


class ScheduleRepository:
    def __init__(self, database: Database):
        self.database = database

    def add(self, schedule: Schedule) -> Schedule:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO schedule (title, date, time, type, desc)
                VALUES (?, ?, ?, ?, ?)
                """,
                (schedule.title, schedule.date, schedule.time, schedule.typ, schedule.desc),
            )
            schedule.id = cursor.lastrowid

        return schedule

    def list(self) -> list[Schedule]:
        with self.database.connect() as connection:
            rows = connection.execute(
                "SELECT id, title, date, time, type, desc FROM schedule"
            ).fetchall()

        return [
            Schedule(
                id=row[0],
                title=row[1],
                date=row[2],
                time=row[3],
                typ=row[4],
                desc=row[5],
            )
            for row in rows
        ]