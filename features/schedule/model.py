from dataclasses import dataclass


@dataclass
class Schedule:
    title: str
    date: str
    time: str
    category: str
    desc: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        self.date = self.date.strip()
        self.category = self.category.strip()
        self.desc = self.desc.strip()

