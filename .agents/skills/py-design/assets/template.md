# System Design

## 1. Design baseline
- Project:
- Proposal path:
- Date:
- Status: Draft / Ready for build / Changes needed
- Scope changes and unresolved blockers:

## 2. System context
Include a Mermaid flowchart showing users, Django, SQLite, and any external services.

## 3. Data model
Include a Mermaid erDiagram and this field dictionary.

| Entity | Field | Django field type | Required / Default | Validation | Relationship / Deletion rule |
|---|---|---|---|---|---|

## 4. Pages and actions
| Requirement ID | Page / URL | User action / HTTP method | Input and validation | Result / Template |
|---|---|---|---|---|

## 5. Main user flow
Include a Mermaid flowchart with success, invalid-input, and empty-data paths.

## 6. Access and login
| Role | Allowed actions | Ownership / Access restriction |
|---|---|---|

Basic login is required. Describe Django session authentication, sign-in, POST sign-out, and a protected application page. Distinguish staff admin from application pages; admin login alone does not fulfill the initial build. Specify how demonstration users are created without recording credentials.

## 7. Integrations and configuration
| Dependency / API | Purpose | Official documentation | Environment variable names | Failure / Sample-data fallback |
|---|---|---|---|---|

## 8. Outputs and business rules
| Requirement ID | Output / Rule | Calculation or format | Example |
|---|---|---|---|

## 9. Build increments
| Increment ID | Demonstrable outcome | Requirement IDs | Data / Pages needed | Acceptance criterion IDs |
|---|---|---|---|---|

Make the first increment the runnable base Django/SQLite project with authentication and a protected application page. Map it to authentication requirement/criterion IDs and initial-build screenshot evidence. Defer business workflows to later increments. Preserve existing IDs when revising a design.

## 10. Verification and delivery plan
| Criterion ID | Sample input / Setup | Action | Expected result | Verification method |
|---|---|---|---|---|

Plan a video demonstration of the local SQLite app. Map acceptance criteria to demonstration steps, including saved data, useful outputs, authentication, and an error case. Plan initial-build screenshots of sign-in, the authenticated protected page, and the signed-out access restriction. The final video must connect proposal requirements to working behavior and highlight the design choices behind it.

## 11. Decisions, risks, and student explanation
Record assumptions, open decisions, and risks. Leave a prompt for the student to explain the request → URL → view → ORM → template → response path in their own words.
