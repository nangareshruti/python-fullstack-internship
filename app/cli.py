"""Menu-driven command line interface."""
from app.config import settings
from app.importer import import_csv, import_json
from app.logger import log
from app.models import Student, ValidationError
from app.repository import StudentRepository

MENU = """
===== Student Management System =====
1. Add student
2. List students
3. Search students
4. Update student
5. Delete student
6. Import students from CSV
7. Import students from JSON
0. Exit
"""


def _print_students(students):
    if not students:
        print("No students found.")
        return
    print(f"{'ID':<4} {'Name':<20} {'Email':<28} {'Course':<16} Age")
    print("-" * 76)
    for s in students:
        print(f"{s.id:<4} {s.name:<20} {s.email:<28} {s.course:<16} {s.age}")


def _read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def run() -> None:
    repo = StudentRepository(settings.DB_PATH)
    log.info("Application started")
    try:
        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()
            try:
                if choice == "1":
                    s = Student(
                        name=input("Name: "),
                        email=input("Email: "),
                        course=input("Course: "),
                        age=_read_int("Age: "),
                    )
                    created = repo.create(s)
                    print(f"Added student with ID {created.id}")
                elif choice == "2":
                    _print_students(repo.list_all())
                elif choice == "3":
                    _print_students(repo.search(input("Keyword: ")))
                elif choice == "4":
                    sid = _read_int("Student ID: ")
                    print("Leave a field blank to keep the current value.")
                    changes = {}
                    for field in ("name", "email", "course"):
                        value = input(f"New {field}: ").strip()
                        if value:
                            changes[field] = value
                    age = input("New age: ").strip()
                    if age.isdigit():
                        changes["age"] = int(age)
                    updated = repo.update(sid, **changes)
                    print("Updated." if updated else "Student not found.")
                elif choice == "5":
                    ok = repo.delete(_read_int("Student ID: "))
                    print("Deleted." if ok else "Student not found.")
                elif choice in ("6", "7"):
                    path = input("File path: ").strip().strip('"')
                    try:
                        importer = import_csv if choice == "6" else import_json
                        result = importer(path, repo)
                    except FileNotFoundError:
                        print("File not found. Check the path and try again.")
                    else:
                        print(f"Imported: {result.imported}, Skipped: {result.skipped}")
                        for err in result.errors:
                            print("  -", err)
                elif choice == "0":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option.")
            except ValidationError as e:
                print(f"Error: {e}")
    finally:
        repo.close()
        log.info("Application stopped")
