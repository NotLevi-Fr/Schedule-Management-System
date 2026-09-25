from data.data import Database

from .model import Schedule
from .repository import ScheduleRepository


class ScheduleService:
    def __init__(self, data: Database):
        self.repository = ScheduleRepository(data)

    def add_schedule(self, schedule: Schedule) -> Schedule:
        return self.repository.add(schedule)