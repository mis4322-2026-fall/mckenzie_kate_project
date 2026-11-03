---
name: py-design
description: Translate a course project proposal into a standardized Django system design with Mermaid diagrams.
---

# py-design

## Workflow

Read `deliverables/01-proposal.md`; if absent, request the idea and establish the proposal first. Identify unresolved decisions affecting design. Map each Must requirement to data, pages/actions, and an acceptance criterion. Use the proposal as the scope baseline; record changes instead of adding features silently.

Write `deliverables/02-design.md`. Include a Mermaid system flowchart, entity relationship diagram, and a main user-flow diagram. For apps with no stored business entities, state why and diagram any data actually stored. Model fields, relationships, validation, access rules, outputs, configuration, and external services explicitly. For every API document source, authentication, required environment variable names, failure behavior, and a sample-data fallback. Never put secret values in the document. Prefer built-in Django capabilities. Finish with small end-to-end increments, each producing something a student can demonstrate. The first increment is the base Django/SQLite project with basic authentication, before business features. Specify sign-in, POST sign-out, a protected application page, server-side access rules, and acceptance checks for valid/invalid sign-in and anonymous access. Map that increment to the proposal’s authentication requirement and criteria. It must be sufficient for course Deliverable 3 (initial build with screenshots); build increments are not the numbered course deliverables. For an existing design, preserve IDs and explicitly reorder or add the foundation increment instead of renumbering existing work.

Copy `assets/template.md` to the stated output path. Preserve every numbered heading, table column, and heading order. Replace prompts with project-specific content; use `Not applicable — <reason>` for unused sections. Mark unresolved decisions `Open`; do not silently fill them. Add rows as needed. Output Markdown, with Mermaid fenced code blocks where requested. A draft can contain open questions, but report them before advancing dependent work.

## Course conventions

Work in the student's project root. Use plain business language and explain the Python/Django concepts behind changes so the student can explain their work. Prefer a small Django app with server-rendered templates, Django forms, ORM, and admin. SQLite is required throughout; final delivery is a video demonstration of the local app. Basic authentication is required for every course project: use Django’s built-in session authentication for sign-in, POST sign-out, and at least one protected application page. Enforce access on the server; never build password storage. Self-registration, password reset, and additional roles are optional unless required by the proposal. Add APIs, packages, or background services only when the design needs them. Use fictional demonstration data and keep credentials outside source control.

Read the relevant existing deliverables before editing. Keep stable IDs (`FR-01` for requirements, `AC-01` for acceptance criteria, `INC-01` for increments). Preserve IDs when scope changes and record the change. Do not invent student decisions, approval, execution results, or evidence. Ask focused questions for decisions that change scope; label other assumptions. Update existing artifacts instead of making duplicate versions.
