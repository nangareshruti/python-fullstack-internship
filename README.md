# Student Management System (CLI)

Python CLI app with SQLite storage, validation, structured logging and pytest tests.

**Covers tasks:** 1 (CLI student system), 3 (reusable CRUD module), 15 (logging decorator),
16 (env-based config), 23 (pytest), 24 (structured logging).

## Run

```bash
python -m venv venv \\\&\\\& source venv/bin/activate   # Windows: venv\\\\Scripts\\\\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Test

```bash
pytest -v
```

## Structure

```
app/config.py      env-based settings
app/logger.py      logger + @log\\\_call decorator
app/models.py      Student dataclass + validation
app/repository.py  CRUD on SQLite (parameterised queries)
app/cli.py         menu-driven interface
tests/             pytest tests
```

## Screenshots

!\[Menu](screenshots/menu.png)

!\[Tests](screenshots/tests.png)

