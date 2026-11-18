"""Tasks 1 + 3: CRUD layer on SQLite (stdlib only, parameterised queries)."""
import sqlite3
from typing import List, Optional

from app.logger import log_call
from app.models import Student, ValidationError


class StudentRepository:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL,
                age INTEGER NOT NULL
            )"""
        )
        self.conn.commit()

    @staticmethod
    def _row_to_student(row: sqlite3.Row) -> Student:
        return Student(**dict(row))

    @log_call
    def create(self, student: Student) -> Student:
        student.validate()
        try:
            cur = self.conn.execute(
                "INSERT INTO students (name, email, course, age) VALUES (?, ?, ?, ?)",
                (student.name, student.email, student.course, student.age),
            )
        except sqlite3.IntegrityError:
            raise ValidationError(f"Email already exists: {student.email}")
        self.conn.commit()
        student.id = cur.lastrowid
        return student

    @log_call
    def get(self, student_id: int) -> Optional[Student]:
        row = self.conn.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        ).fetchone()
        return self._row_to_student(row) if row else None

    @log_call
    def list_all(self) -> List[Student]:
        rows = self.conn.execute("SELECT * FROM students ORDER BY id").fetchall()
        return [self._row_to_student(r) for r in rows]

    @log_call
    def search(self, keyword: str) -> List[Student]:
        like = f"%{keyword}%"
        rows = self.conn.execute(
            "SELECT * FROM students WHERE name LIKE ? OR course LIKE ? OR email LIKE ?",
            (like, like, like),
        ).fetchall()
        return [self._row_to_student(r) for r in rows]

    @log_call
    def update(self, student_id: int, **fields) -> Optional[Student]:
        current = self.get(student_id)
        if current is None:
            return None
        for key, value in fields.items():
            if key not in {"name", "email", "course", "age"}:
                raise ValidationError(f"Unknown field: {key}")
            setattr(current, key, value)
        current.validate()
        try:
            self.conn.execute(
                "UPDATE students SET name=?, email=?, course=?, age=? WHERE id=?",
                (current.name, current.email, current.course, current.age, student_id),
            )
        except sqlite3.IntegrityError:
            raise ValidationError(f"Email already exists: {current.email}")
        self.conn.commit()
        return current

    @log_call
    def delete(self, student_id: int) -> bool:
        cur = self.conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def close(self) -> None:
        self.conn.close()
