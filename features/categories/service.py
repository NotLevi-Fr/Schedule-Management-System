from data.data import Database
from .model import Category
from .repository import CategoryRepository


class CategoryService:
    def __init__(self, database: Database):
        self.repository = CategoryRepository(database)

    def add(self, category: Category) -> Category:
        return self.repository.add(category)

    def update(self, category: Category) -> Category:
        return self.repository.update(category)

    def delete(self, category_id: int) -> None:
        self.repository.delete(category_id)

    def get(self, category_id: int) -> Category | None:
        return self.repository.get(category_id)

    def list(self) -> list[Category]:
        return self.repository.list()
