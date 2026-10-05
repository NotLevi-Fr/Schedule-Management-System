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
        self.editing_id: int | None = None
        self.setWindowTitle("Schedule Management System")
        self.resize(420, 480)

        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.title_input = QLineEdit()
        self.date_input = QLineEdit()
        self.time_input = QLineEdit()
        self.type_input = QLineEdit()
        self.desc_input = QLineEdit()
        self.title_input.returnPressed.connect(self.save_schedule)
        form.addRow("Title", self.title_input)
        form.addRow("Date (MM/DD/YYYY)", self.date_input)
        form.addRow("Time (HH:MM)", self.time_input)
        form.addRow("Type", self.type_input)
        form.addRow("Description (Optional)", self.desc_input)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        self.save_button = QPushButton("Add Schedule")
        self.save_button.clicked.connect(self.save_schedule)
        update_button = QPushButton("Update Selected")
        update_button.clicked.connect(self.update_schedule)
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_schedule)
        buttons.addWidget(self.save_button)
        buttons.addWidget(update_button)
        buttons.addWidget(delete_button)
        layout.addLayout(buttons)

        layout.addWidget(QLabel("Schedules"))
        self.list = QListWidget()
        layout.addWidget(self.list)

        self.show()

    def show(self, index: int = 0) -> None:
        self.refresh()
        super().show()

    def selected_id(self, action: str) -> int | None:
        item = self.list.currentItem()
        if item is None:
            QMessageBox.warning(
                self, "Nothing selected", f"Please select a schedule to {action}."
            )
            return None

        return item.data(Qt.ItemDataRole.UserRole)

    def fields(self) -> tuple[QLineEdit, ...]:
        return (
            self.title_input,
            self.date_input,
            self.time_input,
            self.type_input,
            self.desc_input,
        )

    def clear_form(self) -> None:
        for field in self.fields():
            field.clear()

    def fill_form(self, schedule: Schedule) -> None:
        for field, value in zip(
            self.fields(),
            (
                schedule.title,
                schedule.date,
                schedule.time,
                schedule.typ,
                schedule.desc,
            ),
        ):
            field.setText(value)

    def read_form(self) -> Schedule | None:
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Missing title", "Please enter a title.")
            return None

        return Schedule(
            title,
            self.date_input.text(),
            self.time_input.text(),
            self.type_input.text(),
            self.desc_input.text(),
            id=self.editing_id,
        )

    def set_editing(self, schedule_id: int | None) -> None:
        self.editing_id = schedule_id
        self.save_button.setText(
            "Save Changes" if schedule_id is not None else "Add Schedule"
        )

    def save_schedule(self) -> None:
        schedule = self.read_form()
        if schedule is None:
            return

        if self.editing_id is None:
            self.service.add(schedule)
        else:
            self.service.update(schedule)

        self.set_editing(None)
        self.clear_form()
        self.refresh()

    def update_schedule(self) -> None:
        schedule_id = self.selected_id("update")
        if schedule_id is None:
            return

        schedule = self.service.get(schedule_id)
        if schedule is None:
            QMessageBox.warning(
                self, "Schedule not found", "That schedule no longer exists."
            )
            self.set_editing(None)
            self.refresh()
            return

        self.set_editing(schedule_id)
        self.fill_form(schedule)
        self.title_input.setFocus()

    def cancel_update(self) -> None:
        self.set_editing(None)
        self.clear_form()
        self.refresh()

    def delete_schedule(self) -> None:
        schedule_id = self.selected_id("delete")
        if schedule_id is None:
            return

        item = self.list.currentItem()
        confirm = QMessageBox.question(
            self, "Delete schedule", f"Delete {item.text()}?"
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        self.service.delete(schedule_id)

        if self.editing_id == schedule_id:
            self.cancel_update()
        else:
            self.refresh()

    def refresh(self) -> None:
        self.list.clear()
        for schedule in self.service.list():
            item = QListWidgetItem(
                f"{schedule.title} | {schedule.date} | {schedule.time} | {schedule.typ} | {schedule.desc}"
            )
            item.setData(Qt.ItemDataRole.UserRole, schedule.id)
            self.list.addItem(item)
