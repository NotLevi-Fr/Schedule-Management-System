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
                (
                    schedule.title,
                    schedule.date,
                    schedule.time,
                    schedule.typ,
                    schedule.desc,
                ),
            )
            schedule.id = cursor.lastrowid

        return schedule

    def update(self, schedule: Schedule) -> Schedule:
        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE schedule
                SET title = ?, date = ?, time = ?, type = ?, desc = ?
                WHERE id = ?
                """,
                (
                    schedule.title,
                    schedule.date,
                    schedule.time,
                    schedule.typ,
                    schedule.desc,
                    schedule.id,
                ),
            )

        return schedule

    def delete(self, schedule_id: int) -> None:
        with self.database.connect() as connection:
            connection.execute("DELETE FROM schedule WHERE id = ?", (schedule_id,))

    def get(self, schedule_id: int) -> Schedule | None:
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT id, title, date, time, type, desc FROM schedule WHERE id = ?",
                (schedule_id,),
            ).fetchone()

        if row is None:
            return None

        return Schedule(
            id=row[0],
            title=row[1],
            date=row[2],
            time=row[3],
            typ=row[4],
            desc=row[5],
        )

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

