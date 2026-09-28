from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from features.schedule.model import Schedule
from features.schedule.service import StudentService


class StudentView(QWidget):
    def __init__(self, service: StudentService):
        super().__init__()
        self.service = service
        self.setWindowTitle("Schedule Management System")
        self.resize(420, 480)

        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.title_input = QLineEdit()
        self.date_input = QLineEdit()
        self.time_input = QLineEdit()
        self.type_input = QLineEdit()
        self.desc_input = QLineEdit()
        self.title_input.returnPressed.connect(self.add_schedule)
        form.addRow("Title", self.title_input)
        form.addRow("Date (MM/DD/YYYY)", self.date_input)
        form.addRow("Time (HH:MM)", self.time_input)
        form.addRow("Type", self.type_input)
        form.addRow("Description (Optional)", self.desc_input)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        add_button = QPushButton("Add Schedule")
        add_button.clicked.connect(self.add_schedule)
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_schedule)
        buttons.addWidget(add_button)
        buttons.addWidget(delete_button)
        layout.addLayout(buttons)

        layout.addWidget(QLabel("Schedules"))
        self.list = QListWidget()
        layout.addWidget(self.list)

        self.show()

    def show(self, index: int = 0) -> None:
        self.refresh()
        super().show()

    def add_schedule(self) -> None:
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Missing title", "Please enter a title.")
            return

        self.service.add(
            Schedule(
                title,
                self.date_input.text(),
                self.time_input.text(),
                self.type_input.text(),
                self.desc_input.text(),
            )
        )

        for field in (
            self.title_input,
            self.date_input,
            self.time_input,
            self.type_input,
            self.desc_input,
        ):
            field.clear()

        self.refresh()

    def delete_schedule(self) -> None:
        item = self.list.currentItem()
        if item is None:
            QMessageBox.warning(
                self, "Nothing selected", "Please select a schedule to delete."
            )
            return

        confirm = QMessageBox.question(
            self, "Delete schedule", f"Delete {item.text()}?"
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.service.delete(item.data(Qt.ItemDataRole.UserRole))
        self.refresh()

    def refresh(self) -> None:
        self.list.clear()
        for schedule in self.service.list():
            item = QListWidgetItem(
                f"{schedule.title} | {schedule.date} | {schedule.time} | {schedule.typ} | {schedule.desc}"
            )
            item.setData(Qt.ItemDataRole.UserRole, schedule.id)
            self.list.addItem(item)
