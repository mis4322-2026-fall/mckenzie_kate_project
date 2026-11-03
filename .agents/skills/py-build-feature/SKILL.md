---
name: py-build-feature
description: Build one designed Django user workflow including its data model, forms, templates, outputs, and appropriate checks.
---

# py-build-feature

## Workflow

Read the proposal, design, current build log, and code. Select one design increment. Implement only the selected increment’s data needs: models, relationships, constraints, migrations, useful admin views, and fictional sample data. Inspect migrations before applying them, preserve existing records, and obtain permission before destructive data changes; never reset a database to avoid a migration problem. Make sample-data setup repeatable without overwriting records. Verify relevant constraints, relationships, and persistence. Explain model classes, rows, foreign keys, and CRUD in course language. Keep any design changes synchronized.

Implement its URL → view → ORM → template flow with Django forms and server-rendered HTML. Keep pages usable with clear labels, navigation, errors, and empty states. Use Django CSRF protection, validation, template escaping, and authentication/authorization where specified; enforce access in views and queries, not only by hiding links. Keep GET requests free of state changes. Use POST and a confirmation step for deletion.

Implement integrations only when required by the design. Keep API secrets server-side in environment variables; use timeouts and handle unavailable services, malformed responses, and empty results. Provide fictional/offline sample data when appropriate. Keep reports and calculations traceable to business rules. Avoid separate frontend frameworks and REST APIs unless the project actually needs them.

Exercise the success path, invalid input, empty state, and applicable access restrictions. Add focused Django tests for meaningful behavior such as calculations, validation, persistence, or ownership. Run relevant checks and tests and record actual outcomes. Update `deliverables/04-build-log.md` using the sibling `py-build` format; synchronize any design changes. Give the student exact local demonstration steps and a prompt to explain the feature's request/data flow. Stop after the selected increment unless more were requested.

## Course conventions

Work in the student's project root. Use plain business language and explain the Python/Django concepts behind changes so the student can explain their work. Prefer a small Django app with server-rendered templates, Django forms, ORM, and admin. SQLite is required throughout; final delivery is a video demonstration of the local app. Basic authentication is required for every course project: use Django’s built-in session authentication for sign-in, POST sign-out, and at least one protected application page. Enforce access on the server; never build password storage. Self-registration, password reset, and additional roles are optional unless required by the proposal. Add APIs, packages, or background services only when the design needs them. Use fictional demonstration data and keep credentials outside source control.

Read the relevant existing deliverables before editing. Keep stable IDs (`FR-01` for requirements, `AC-01` for acceptance criteria, `INC-01` for increments). Preserve IDs when scope changes and record the change. Do not invent student decisions, approval, execution results, or evidence. Ask focused questions for decisions that change scope; label other assumptions. Update existing artifacts instead of making duplicate versions.
