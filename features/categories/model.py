from dataclasses import dataclass


@dataclass
class Category:
    name: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.name = self.name.strip()
