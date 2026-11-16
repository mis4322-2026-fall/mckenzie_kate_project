# Movie Finder

INC-01 provides a public welcome page, Django login, a protected dashboard, and CSRF-protected POST logout. Accounts and sessions use SQLite. Registration and movie features are planned in later increments.

## macOS / Linux

Use Python 3.14 (the build used 3.14.3). From the project directory:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py create_demo_user
.venv/bin/python manage.py runserver
```

## Windows PowerShell

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py create_demo_user
.\.venv\Scripts\python.exe manage.py runserver
```

The account command creates an ordinary user and prompts for a password twice without displaying it. Choose a fictional username and a unique password; no credentials ship with the project. Optional admin access can be created with `manage.py createsuperuser` using the same interpreter.

Open http://127.0.0.1:8000/. Log in, open the dashboard, log out, and visit http://127.0.0.1:8000/dashboard/ again to see the login restriction. Stop the server with Ctrl+C. SQLite data remains in ignored `db.sqlite3`.

## Configuration

These are local development settings (`DEBUG=True`, localhost only). No API token is needed for INC-01. Settings read `DJANGO_SECRET_KEY` from the process environment. If absent, a temporary random key is generated each process, so existing sessions may require login again after restarting. For stable sessions, set a private random key before running commands:

```sh
export DJANGO_SECRET_KEY='your-private-random-value'
```

PowerShell equivalent:

```powershell
$env:DJANGO_SECRET_KEY = 'your-private-random-value'
```

Use a long randomly generated value; do not commit it. `.env.example` documents the name only; `.env` is not automatically loaded. SQLite, the virtual environment, and credentials are excluded from Git.

## Checks

```sh
.venv/bin/python manage.py check
.venv/bin/python manage.py makemigrations --check --dry-run
.venv/bin/python manage.py test
```

On Windows, substitute `.\.venv\Scripts\python.exe` for the interpreter. Tests create temporary accounts with random passwords in a separate test database.

See [bootstrap evidence](deliverables/03-bootstrap.md) and [build log](deliverables/04-build-log.md) for results and pending screenshots.
