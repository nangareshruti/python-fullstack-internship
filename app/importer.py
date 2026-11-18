"""Tasks 4 + 5: import students from CSV and JSON files.

Good rows are saved. Bad rows (missing data, wrong age, duplicate email)
are skipped, logged, and reported back instead of crashing the import.
"""
import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List

from app.logger import log
from app.models import Student, ValidationError
from app.repository import StudentRepository

REQUIRED_FIELDS = ("name", "email", "course", "age")


@dataclass
class ImportResult:
    imported: int = 0
    skipped: int = 0
    errors: List[str] = field(default_factory=list)


def _import_records(records: Iterable[dict], repo: StudentRepository) -> ImportResult:
    result = ImportResult()
    for line_no, record in enumerate(records, start=1):
        try:
            missing = [f for f in REQUIRED_FIELDS if not str(record.get(f, "")).strip()]
            if missing:
                raise ValidationError(f"Missing fields: {', '.join(missing)}")
            try:
                age = int(record["age"])
            except (TypeError, ValueError):
                raise ValidationError(f"Age must be a number, got {record['age']!r}")
            student = Student(
                name=str(record["name"]).strip(),
                email=str(record["email"]).strip(),
                course=str(record["course"]).strip(),
                age=age,
            )
            repo.create(student)
            result.imported += 1
        except ValidationError as e:
            result.skipped += 1
            message = f"Row {line_no}: {e}"
            result.errors.append(message)
            log.warning("Import skipped - %s", message)
    log.info("Import finished: %d imported, %d skipped", result.imported, result.skipped)
    return result


def import_csv(path: str, repo: StudentRepository) -> ImportResult:
    # utf-8-sig handles CSV files saved from Excel (they start with a hidden BOM)
    with open(Path(path), newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return _import_records(reader, repo)


def import_json(path: str, repo: StudentRepository) -> ImportResult:
    with open(Path(path), encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValidationError("JSON file must contain a list of student objects")
    return _import_records(data, repo)
