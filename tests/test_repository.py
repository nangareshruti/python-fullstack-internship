"""Task 23: pytest unit tests."""
import pytest

from app.models import Student, ValidationError
from app.repository import StudentRepository


@pytest.fixture
def repo(tmp_path):
    r = StudentRepository(str(tmp_path / "test.db"))
    yield r
    r.close()


def make(**over):
    data = dict(name="Asha", email="asha@example.com", course="Python", age=21)
    data.update(over)
    return Student(**data)


def test_create_and_get(repo):
    s = repo.create(make())
    assert s.id is not None
    assert repo.get(s.id).email == "asha@example.com"


def test_duplicate_email_rejected(repo):
    repo.create(make())
    with pytest.raises(ValidationError):
        repo.create(make(name="Other"))


@pytest.mark.parametrize(
    "bad", [dict(name=" "), dict(email="nope"), dict(age=5), dict(course="")]
)
def test_validation(repo, bad):
    with pytest.raises(ValidationError):
        repo.create(make(**bad))


def test_list_and_search(repo):
    repo.create(make())
    repo.create(make(name="Ravi", email="ravi@example.com", course="Java"))
    assert len(repo.list_all()) == 2
    assert [s.name for s in repo.search("Java")] == ["Ravi"]


def test_update(repo):
    s = repo.create(make())
    updated = repo.update(s.id, course="Django", age=22)
    assert updated.course == "Django" and updated.age == 22
    assert repo.update(999, name="X") is None


def test_delete(repo):
    s = repo.create(make())
    assert repo.delete(s.id) is True
    assert repo.get(s.id) is None
    assert repo.delete(s.id) is False

