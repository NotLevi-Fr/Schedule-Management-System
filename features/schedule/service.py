from data.data import Database

from .model import Schedule
from .repository import ScheduleRepository


class ScheduleService:
    def __init__(self, data: Database):
        self.repository = ScheduleRepository(data)

    def add_schedule(self, schedule: Schedule) -> Schedule:
        return self.repository.add(schedule)

    def update_schedule(self, schedule: Schedule) -> Schedule:
        return self.repository.update(schedule)

    def delete_schedule(self, schedule_id: int) -> None:
        self.repository.delete(schedule_id)

    def get_schedule(self, schedule_id: int) -> Schedule | None:
        return self.repository.get(schedule_id)

    def list_schedules(self) -> list[Schedule]:
        return self.repository.list()


class StudentService:
    def __init__(self, database: Database):
        self.repository = ScheduleRepository(database)

    def add(self, schedule: Schedule) -> Schedule:
        return self.repository.add(schedule)

    def update(self, schedule: Schedule) -> Schedule:
        return self.repository.update(schedule)

    def delete(self, schedule_id: int) -> None:
        self.repository.delete(schedule_id)

    def get(self, schedule_id: int) -> Schedule | None:
        return self.repository.get(schedule_id)

    def list(self) -> list[Schedule]:
        return self.repository.list()