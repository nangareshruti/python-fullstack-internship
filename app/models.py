"""Student data model with validation."""
import re
from dataclasses import dataclass
from typing import Optional

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ValidationError(ValueError):
    pass


@dataclass
class Student:
    name: str
    email: str
    course: str
    age: int
    id: Optional[int] = None

    def validate(self) -> None:
        if not self.name.strip():
            raise ValidationError("Name cannot be empty")
        if not EMAIL_RE.match(self.email):
            raise ValidationError(f"Invalid email: {self.email}")
        if not self.course.strip():
            raise ValidationError("Course cannot be empty")
        if not (15 <= self.age <= 100):
            raise ValidationError("Age must be between 15 and 100")
