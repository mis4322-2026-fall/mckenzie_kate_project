---
name: py-propose
description: Turn a student business idea into a standardized proposal for a small Django web application.
---

# py-propose

## Workflow

Elicit the intended user, business problem, main workflow, useful output, and available data. Help narrow an oversized idea to a manageable first version. Recommend roughly 3–5 core requirements and a small data model as a starting point, not an assignment rule. Separate required work from future ideas. Explain feasibility in terms of course concepts; avoid promising an API or hosting service is available without checking.

Write `deliverables/01-proposal.md`. Requirements must describe observable behavior; acceptance criteria must be demonstrable with sample inputs and expected results. Include basic authentication as a Must requirement even for an otherwise public app. Add demonstrable acceptance criteria for valid and invalid sign-in, sign-out, and anonymous denial or redirection from a protected page. Keep authentication distinct from optional registration and domain-specific roles. Record who supplied decisions and leave instructor review pending unless supplied. Do not start implementation during proposal work.

Copy `assets/template.md` to the stated output path. Preserve every numbered heading, table column, and heading order. Replace prompts with project-specific content; use `Not applicable — <reason>` for unused sections. Mark unresolved decisions `Open`; do not silently fill them. Add rows as needed. Output Markdown, with Mermaid fenced code blocks where requested. A draft can contain open questions, but report them before advancing dependent work.

## Course conventions

Work in the student's project root. Use plain business language and explain the Python/Django concepts behind changes so the student can explain their work. Prefer a small Django app with server-rendered templates, Django forms, ORM, and admin. SQLite is required throughout; final delivery is a video demonstration of the local app. Basic authentication is required for every course project: use Django’s built-in session authentication for sign-in, POST sign-out, and at least one protected application page. Enforce access on the server; never build password storage. Self-registration, password reset, and additional roles are optional unless required by the proposal. Add APIs, packages, or background services only when the design needs them. Use fictional demonstration data and keep credentials outside source control.

Read the relevant existing deliverables before editing. Keep stable IDs (`FR-01` for requirements, `AC-01` for acceptance criteria, `INC-01` for increments). Preserve IDs when scope changes and record the change. Do not invent student decisions, approval, execution results, or evidence. Ask focused questions for decisions that change scope; label other assumptions. Update existing artifacts instead of making duplicate versions.
