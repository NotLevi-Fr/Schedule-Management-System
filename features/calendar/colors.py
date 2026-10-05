TYPE_COLORS: dict[str, tuple[str, str]] = {
    "exam": ("#f8c9c9", "#7f1d1d"),
    "quiz": ("#fde0b5", "#7c3e00"),
    "assignment": ("#bedcfa", "#1e3a8a"),
    "activity": ("#bee9c8", "#14532d"),
    "lecture": ("#dcc7f5", "#4c1d95"),
    "deadline": ("#fbc7e7", "#831843"),
}

TYPE_ALIASES: dict[str, str] = {
    "test": "quiz",
    "class": "lecture",
    "subject": "lecture",
    "homework": "assignment",
    "task": "assignment",
    "project": "deadline",
    "task due": "deadline",
}

DEFAULT_COLOR: tuple[str, str] = ("#e5e7eb", "#374151")

KNOWN_TYPES: tuple[str, ...] = tuple(TYPE_COLORS)


def normalize_type(text: str) -> str:
    value = " ".join(text.strip().lower().split())
    return TYPE_ALIASES.get(value, value)


def display_type(text: str) -> str:
    value = " ".join(text.strip().split())
    return value.title() if value else "Other"


def color_pair(text: str) -> tuple[str, str]:
    return TYPE_COLORS.get(normalize_type(text), DEFAULT_COLOR)