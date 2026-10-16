from data.data import Database
from .model import Category


class CategoryRepository:
    def __init__(self, database: Database):
        self.database = database

    def add(self, category: Category) -> Category:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO categories (name)
                VALUES (?)
                """,
                (category.name,),
            )
            category.id = cursor.lastrowid
        return category

    def update(self, category: Category) -> Category:
        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE categories
                SET name = ?
                WHERE id = ?
                """,
                (category.name, category.id),
            )
        return category

    def delete(self, category_id: int) -> None:
        with self.database.connect() as connection:
            connection.execute("DELETE FROM categories WHERE id = ?", (category_id,))

    def get(self, category_id: int) -> Category | None:
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT id, name FROM categories WHERE id = ?",
                (category_id,),
            ).fetchone()
        if row is None:
            return None
        return Category(id=row[0], name=row[1])

    def list(self) -> list[Category]:
        with self.database.connect() as connection:
            rows = connection.execute(
                "SELECT id, name FROM categories ORDER BY name COLLATE NOCASE"
            ).fetchall()
        return [Category(id=row[0], name=row[1]) for row in rows]
