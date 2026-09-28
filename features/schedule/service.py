from data.data import Database

from .model import Schedule
from .repository import ScheduleRepository


class ScheduleService:
    def __init__(self, data: Database):
        self.repository = ScheduleRepository(data)

    def add_schedule(self, schedule: Schedule) -> Schedule:
        return self.repository.add(schedule)


class StudentService:
    def __init__(self, database: Database):
        self.repository = ScheduleRepository(database)

    def add(self, schedule: Schedule) -> Schedule:
        return self.repository.add(schedule)

    def delete(self, schedule_id: int) -> None:
        self.repository.delete(schedule_id)

    def list(self) -> list[Schedule]:
        return self.repository.list()