from dataclasses import dataclass


@dataclass
class Schedule:
    title: str
    date: str
    time: str
    typ: str
    desc: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        self.date = self.date.strip()
        self.typ = self.typ.strip()
        self.desc = self.desc.strip()