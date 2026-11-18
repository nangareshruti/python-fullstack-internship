"""Tests for CSV and JSON importers."""
import json

import pytest

from app.importer import import_csv, import_json
from app.models import ValidationError
from app.repository import StudentRepository


@pytest.fixture
def repo(tmp_path):
    r = StudentRepository(str(tmp_path / "test.db"))
    yield r
    r.close()


def test_import_csv_good_and_bad_rows(repo, tmp_path):
    f = tmp_path / "s.csv"
    f.write_text(
        "name,email,course,age\n"
        "Asha,asha@example.com,Python,21\n"
        "Ravi,ravi@example.com,Java,22\n"
        "Bad,not-an-email,Python,21\n"
        "Asha2,asha@example.com,Python,21\n"
        "NoAge,noage@example.com,SQL,\n",
        encoding="utf-8",
    )
    result = import_csv(str(f), repo)
    assert result.imported == 2
    assert result.skipped == 3
    assert len(repo.list_all()) == 2


def test_import_json(repo, tmp_path):
    f = tmp_path / "s.json"
    f.write_text(
        json.dumps(
            [
                {"name": "Amit", "email": "amit@example.com", "course": "FastAPI", "age": 23},
                {"name": "X", "email": "x@example.com", "course": "SQL", "age": "abc"},
            ]
        )
    )
    result = import_json(str(f), repo)
    assert result.imported == 1 and result.skipped == 1
    assert "Age must be a number" in result.errors[0]


def test_json_must_be_a_list(repo, tmp_path):
    f = tmp_path / "s.json"
    f.write_text(json.dumps({"name": "not a list"}))
    with pytest.raises(ValidationError):
        import_json(str(f), repo)
