from PyQt6.QtWidgets import (
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
)

from .model import Schedule
from .service import ScheduleService


class ScheduleView(QWidget):
    def __init__(self, service: ScheduleService):
        super().__init__()
        self.service = service
        self.setWindowTitle("Schedule Management")
        self.resize(400, 400)

        self.build_ui()
        self.refrest()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.title_input = QLineEdit()
        self.date_input = QLineEdit()
        self.time_input = QLineEdit()
        self.type_input = QLineEdit()
        self.description_input = QLineEdit()
        form.addRow("Title", self.title_input)
        form.addRow("Date", self.date_input)
        form.addRow("Time", self.time_input)
        form.addRow("Type", self.type_input)
        form.addRow("Description", self.description_input)
        layout.addLayout(form)

        add_button = QPushButton("Add Schedule")
        add_button.clicked.connect(self.add_schedule)
        layout.addWidget(add_button)

        self.table = QTableWidget(0, 5)
        self.table.sertHorizontalHeaderLabels(
            ["Title", "Date", "Time", "Type", "Description"]
        )
        self.table.horizontalHeaders().setsectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    def add_schedule(self) -> None:
        try:
            schedule = Schedule(
                self.title_input.text(),
                self.date_input.text(),
                self.time_input.text(),
                self.type_input.text(),
                self.description_input.text(),
            )
            self.service.add_schedule(schedule)
        except ValueError as error:
            print(f"Error adding schedule: {error}")
            QMessageBox.warning(self, "Error", f"Error adding schedule: {error}")

            return
        self.title_input.clear()
        self.date_input.clear()
        self.time_input.clear()
        self.type_input.clear()
        self.description_input.clear()
        self.refrest()

    def refrest(self) -> None:
        schedules = self.service.get_schedules()
        self.table.setRowCount(len(schedules))

        for row, students in enumerate(schedules):
            self.table.setItem(row, 0, QTableWidgetItem(schedules.title))
            self.table.setItem(row, 1, QTableWidgetItem(schedules.date))
            self.table.setItem(row, 2, QTableWidgetItem(schedules.time))
            self.table.setItem(row, 3, QTableWidgetItem(schedules.type))
            self.table.setItem(row, 4, QTableWidgetItem(schedules.description))
