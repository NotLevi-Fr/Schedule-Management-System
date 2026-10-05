from datetime import date

from PyQt6.QtCore import QDate
from PyQt6.QtGui import QColor, QTextCharFormat
from PyQt6.QtWidgets import (
    QCalendarWidget,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from features.schedule.model import Schedule
from features.schedule.service import StudentService

from .colors import DEFAULT_COLOR, KNOWN_TYPES, color_pair, display_type
from .dates import parse_date


class CalendarView(QWidget):
    def __init__(self, service: StudentService):
        super().__init__()
        self.service = service
        self.schedules_by_day: dict[date, list[Schedule]] = {}
        self.painted_days: list[date] = []

        self.build_ui()
        self.refresh()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.currentPageChanged.connect(self.refresh)
        self.calendar.selectionChanged.connect(self.show_selected_day)
        layout.addWidget(self.calendar)

        self.selected_label = QLabel()
        layout.addWidget(self.selected_label)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Time", "Type", "Title", "Description"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        layout.addLayout(self.build_legend())

    def build_legend(self) -> QHBoxLayout:
        legend = QHBoxLayout()
        legend.addWidget(QLabel("Legend:"))

        for name in KNOWN_TYPES:
            legend.addWidget(self.legend_chip(name, color_pair(name)))

        legend.addWidget(self.legend_chip("Other", DEFAULT_COLOR))
        legend.addStretch()
        return legend

    def legend_chip(self, name: str, pair: tuple[str, str]) -> QLabel:
        background, foreground = pair
        chip = QLabel(f"  {name}  ")
        chip.setStyleSheet(
            f"background-color: {background}; color: {foreground};"
            "border-radius: 3px; padding: 2px;"
        )
        return chip

    def refresh(self) -> None:
        self.schedules_by_day = self.group_by_day()
        self.paint_calendar()
        self.show_selected_day()

    def group_by_day(self) -> dict[date, list[Schedule]]:
        grouped: dict[date, list[Schedule]] = {}

        for schedule in self.service.list():
            day = parse_date(schedule.date)
            if day is None:
                continue
            grouped.setdefault(day, []).append(schedule)

        for schedules in grouped.values():
            schedules.sort(key=lambda item: (item.time, item.title.lower()))

        return grouped

    def paint_calendar(self) -> None:
        self.calendar.setUpdatesEnabled(False)

        for day in self.painted_days:
            self.calendar.setDateTextFormat(self.to_qdate(day), QTextCharFormat())

        self.painted_days = []
        for day, schedules in self.schedules_by_day.items():
            background, foreground = self.day_colors(schedules)

            text_format = QTextCharFormat()
            text_format.setBackground(QColor(background))
            text_format.setForeground(QColor(foreground))

            names = ", ".join(dict.fromkeys(display_type(item.typ) for item in schedules))
            text_format.setToolTip(f"{len(schedules)} schedule(s): {names}")

            self.calendar.setDateTextFormat(self.to_qdate(day), text_format)
            self.painted_days.append(day)

        self.calendar.setUpdatesEnabled(True)

    def to_qdate(self, day: date) -> QDate:
        return QDate(day.year, day.month, day.day)

    def day_colors(self, schedules: list[Schedule]) -> tuple[str, str]:
        if len(schedules) > 1:
            return DEFAULT_COLOR
        return color_pair(schedules[0].typ)

    def show_selected_day(self) -> None:
        selected = self.calendar.selectedDate()
        day = parse_date(selected.toString("MM/dd/yyyy"))
        schedules = self.schedules_by_day.get(day, []) if day else []

        heading = "No date selected" if day is None else day.strftime("%A, %B %d, %Y")
        if day is not None:
            heading = f"{heading} — {len(schedules)} schedule(s)"
        self.selected_label.setText(heading)

        self.table.setRowCount(0)
        for schedule in schedules:
            self.add_row(schedule)

    def add_row(self, schedule: Schedule) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)

        background, foreground = color_pair(schedule.typ)
        values = (
            schedule.time,
            display_type(schedule.typ),
            schedule.title,
            schedule.desc,
        )

        for column, value in enumerate(values):
            item = QTableWidgetItem(value)
            item.setBackground(QColor(background))
            item.setForeground(QColor(foreground))
            self.table.setItem(row, column, item)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.refresh()