---
name: py-bootstrap
description: Create the first Django/SQLite increment with basic authentication, or complete that foundation in an existing project.
---

# py-bootstrap

## Workflow

Inspect the repository for `manage.py`, Django settings, dependency manifests, and existing project instructions before writing anything. If a Django project exists, reuse its environment, settings, and versions; inspect and complete only missing foundation/authentication behavior without recreating or upgrading it. If several projects exist, clarify the target. Preserve existing files.

Only for a new project, consult official Django download/release and Python compatibility documentation at execution time. Select the latest stable Django release (no prereleases) and a supported Python interpreter. Record the checked sources, date, and actual versions. If a compatible interpreter is unavailable, explain the needed installation rather than silently using an older Django. Do not hard-code today's latest version into this skill.

For a new project, create `.venv` with `python -m venv`; use its interpreter and `python -m pip` explicitly. Set up a minimal project (prefer `config`) and an app named for the business domain. Use SQLite and Django's generated migrations. Record exact installed dependency versions in `requirements.txt`; respect an existing dependency convention. Provide macOS/Linux and Windows PowerShell setup/run commands in project `README.md`. Ignore `.venv/`, caches, `.env`, and `db.sqlite3`; commit migrations, never credentials. If environment configuration is used, provide `.env.example` containing names and dummy values and explain how values are loaded.

Implement Django session authentication with a sign-in template, POST sign-out with CSRF protection, and a simple protected application landing page. Use built-in auth views/forms and server-side access enforcement. Provide a local user-creation command with an interactive password prompt; do not save credentials in code, artifacts, or screenshots. Registration and business features are outside this foundation unless separately requested.

Run Django system checks, migrations, and a local HTTP smoke check when tools allow. Verify valid sign-in, invalid credentials, anonymous redirection or denial, authenticated page access, and sign-out ending access with focused Django tests. Capture initial-build screenshots when browser tools are available: sign-in, the authenticated page, and the access restriction after sign-out. Otherwise give exact capture steps and mark screenshot evidence pending; never claim uncaptured screenshots exist. Record actual outcomes and unrun checks in `deliverables/03-bootstrap.md` using sections: `1. Environment and sources`, `2. Files and commands`, `3. Verification results`, `4. Student checkpoint`, `5. Open issues`. Include reproducible clean setup commands. The checkpoint asks the student to explain the virtual environment, project versus app, SQLite file, and how authentication protects the application page. Record the foundation increment in `deliverables/04-build-log.md` using the sibling `py-build` format, mapped to the design IDs; link verification and screenshot evidence from the bootstrap report. This increment fulfills course Deliverable 3 only when it works and the required screenshots are supplied. Stop after the foundation for review unless further increments were explicitly requested.

## Course conventions

Work in the student's project root. Use plain business language and explain the Python/Django concepts behind changes so the student can explain their work. Prefer a small Django app with server-rendered templates, Django forms, ORM, and admin. SQLite is required throughout; final delivery is a video demonstration of the local app. Basic authentication is required for every course project: use Django’s built-in session authentication for sign-in, POST sign-out, and at least one protected application page. Enforce access on the server; never build password storage. Self-registration, password reset, and additional roles are optional unless required by the proposal. Add APIs, packages, or background services only when the design needs them. Use fictional demonstration data and keep credentials outside source control.

Read the relevant existing deliverables before editing. Keep stable IDs (`FR-01` for requirements, `AC-01` for acceptance criteria, `INC-01` for increments). Preserve IDs when scope changes and record the change. Do not invent student decisions, approval, execution results, or evidence. Ask focused questions for decisions that change scope; label other assumptions. Update existing artifacts instead of making duplicate versions.
