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

from .model import Category
from .service import CategoryService


class CategoryView(QWidget):
    def __init__(self, service: CategoryService):
        super().__init__()
        self.service = service
        self.editing_id: int | None = None
        self.setWindowTitle("Categories")
        self.resize(380, 420)

        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.returnPressed.connect(self.save_category)
        form.addRow("Category Name", self.name_input)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        self.save_button = QPushButton("Add Category")
        self.save_button.clicked.connect(self.save_category)
        update_button = QPushButton("Update Selected")
        update_button.clicked.connect(self.update_category)
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_category)
        buttons.addWidget(self.save_button)
        buttons.addWidget(update_button)
        buttons.addWidget(delete_button)
        layout.addLayout(buttons)

        layout.addWidget(QLabel("Categories"))
        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(self.update_category)
        layout.addWidget(self.list)

        self.refresh()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.refresh()

    def selected_id(self, action: str) -> int | None:
        item = self.list.currentItem()
        if item is None:
            QMessageBox.warning(self, "Nothing selected", f"Please select a category to {action}.")
            return None
        return item.data(Qt.ItemDataRole.UserRole)

    def clear_form(self) -> None:
        self.name_input.clear()

    def read_form(self) -> Category | None:
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing name", "Please enter a category name.")
            return None
        return Category(name, id=self.editing_id)

    def set_editing(self, category_id: int | None) -> None:
        self.editing_id = category_id
        self.save_button.setText("Save Changes" if category_id is not None else "Add Category")

    def save_category(self) -> None:
        category = self.read_form()
        if category is None:
            return
        if self.editing_id is None:
            self.service.add(category)
        else:
            self.service.update(category)
        self.set_editing(None)
        self.clear_form()
        self.refresh()

    def update_category(self) -> None:
        category_id = self.selected_id("update")
        if category_id is None:
            return
        category = self.service.get(category_id)
        if category is None:
            QMessageBox.warning(self, "Category not found", "That category no longer exists.")
            self.set_editing(None)
            self.refresh()
            return
        self.set_editing(category_id)
        self.name_input.setText(category.name)
        self.name_input.setFocus()

    def delete_category(self) -> None:
        category_id = self.selected_id("delete")
        if category_id is None:
            return
        item = self.list.currentItem()
        confirm = QMessageBox.question(self, "Delete category", f"Delete {item.text()}?")
        if confirm != QMessageBox.StandardButton.Yes:
            return
        self.service.delete(category_id)
        if self.editing_id == category_id:
            self.set_editing(None)
            self.clear_form()
        self.refresh()

    def refresh(self) -> None:
        self.list.clear()
        for category in self.service.list():
            item = QListWidgetItem(category.name)
            item.setData(Qt.ItemDataRole.UserRole, category.id)
            self.list.addItem(item)
