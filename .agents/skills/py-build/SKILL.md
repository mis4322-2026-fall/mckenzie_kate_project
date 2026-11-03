---
name: py-build
description: Coordinate iterative local implementation of an MIS Django project from its design.
---

# py-build

## Workflow

Read `deliverables/01-proposal.md`, `deliverables/02-design.md`, existing code, and `deliverables/04-build-log.md` if present. Resolve design gaps that block the next increment. Inspect for a Django project. Verify the foundation increment first: a runnable Django/SQLite project, sign-in, POST sign-out, and a protected application page. Read and follow the sibling `py-bootstrap/SKILL.md` if the project is absent or any foundation behavior is missing. Reuse existing projects and preserve their environment and versions. Record foundation evidence under the design’s increment ID. Stop after this first increment for review unless additional increments were explicitly requested. If the foundation is already complete, continue with the next unfinished increment.

Select the next unfinished design increment or the increment the student requested. Use `py-build-feature` for each business increment, including its models, migrations, admin, sample data, pages, forms, outputs, and integrations. Read the sibling skill when needed; if automatic invocation is unavailable, follow its file directly. Complete one demonstrable increment per iteration, verify it, and explain how to try it before moving on unless the student requested multiple increments. Before delivery, check all Must requirements and acceptance criteria, recording evidence and any failures in the build log. Run Django system checks, migration consistency checks, and relevant tests. Record browser checks as unverified when no browser is available. Prepare final local video delivery using the guidance below; hosting is not required.

Create/update `deliverables/04-build-log.md` with a `# Build Log` heading and one `## INC-xx: <outcome>` section per increment. Each section has `### Requirements`, `### Changes`, `### How to run and demonstrate`, `### Checks and actual results`, `### Student explanation`, and `### Open issues`. Record command outcomes honestly. Ask the student to explain the relevant data and request flow; never fabricate their response. Keep pending work visible, including design changes and failed checks. Do not describe the whole project as complete until Must requirements have evidence.

## Final video preparation

When the student requests final delivery preparation, read the proposal, design, README, and build log. Verify reproducible setup, migrations, fictional sample data, startup, and SQLite persistence after restart; record actual outcomes and unrun checks. Check every Must requirement and acceptance criterion before claiming readiness.

Write `deliverables/05-delivery.md` with a recording outline and evidence table: `Requirement ID | Criterion ID | Demonstration action | Expected result | Design choice | Video timestamp | Status`. The outline introduces the problem and users, demonstrates each proposal requirement in the running app (including authentication, useful outputs, and an error case), highlights relevant design decisions and the data/request flow, and identifies unmet requirements, design changes, limitations, and AI assistance. Reference reproducible README commands and build-log evidence. Keep credentials out of the recording. The student records and narrates; keep timestamps, the video link, submission status, and student reflections pending until supplied. Do not impose a video length absent instructor guidance.

## Course conventions

Work in the student's project root. Use plain business language and explain the Python/Django concepts behind changes so the student can explain their work. Prefer a small Django app with server-rendered templates, Django forms, ORM, and admin. SQLite is required throughout; final delivery is a video demonstration of the local app. Basic authentication is required for every course project: use Django’s built-in session authentication for sign-in, POST sign-out, and at least one protected application page. Enforce access on the server; never build password storage. Self-registration, password reset, and additional roles are optional unless required by the proposal. Add APIs, packages, or background services only when the design needs them. Use fictional demonstration data and keep credentials outside source control.

Read the relevant existing deliverables before editing. Keep stable IDs (`FR-01` for requirements, `AC-01` for acceptance criteria, `INC-01` for increments). Preserve IDs when scope changes and record the change. Do not invent student decisions, approval, execution results, or evidence. Ask focused questions for decisions that change scope; label other assumptions. Update existing artifacts instead of making duplicate versions.
