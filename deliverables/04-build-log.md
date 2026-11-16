# Build Log

## INC-01: Django/SQLite authentication foundation

### Requirements

FR-01, FR-17 and foundation FR-09; AC-02, AC-04, AC-42 and foundation portions of AC-01/AC-03. Scope follows the design's first increment only.

### Changes

Created `config` project, `movies` app, SQLite authentication/session tables, public welcome, built-in login, server-protected dashboard, and CSRF-protected POST logout. Added responsive shared templates/CSS, interactive ordinary demo-user creation, dependency pins, ignored local data/secrets, setup guide and authentication tests. No credentials are stored in source.

### How to run and demonstrate

Follow [README](../README.md) to install, migrate, create a fictional account and run the server. Open welcome, log in, view the dashboard, log out and request `/dashboard/` directly. Use an incorrect password to show rejection. Capture the three screenshots described in [bootstrap report](03-bootstrap.md).

### Checks and actual results

November 16, 2026: migrations succeeded; Django check found no issues; migration consistency check reported no changes; 8 tests passed. Local HTTP returned 200 for welcome and 302 to login for anonymous dashboard. [Detailed evidence](03-bootstrap.md#3-verification-results).

| Criterion | Current evidence / status |
|---|---|
| AC-02 | Passed: invalid-login error, no session and no dashboard access |
| AC-04 | Passed: CSRF-protected POST logout ends session; dashboard requires login again |
| AC-42 | Partial: public welcome passes automated/HTTP checks; required registration link deferred to INC-02 |
| AC-01 (foundation) | Passed: valid login redirects to protected dashboard; popular movies/navigation pending INC-03 and later |
| AC-03 (foundation) | Passed for the only implemented application route, dashboard; other protected routes pending later increments |

Browser checks/screenshots remain unverified. All other Must requirements remain pending their designed increments; no whole-project completion is claimed.

### Student explanation

Pending: Please explain the virtual environment, project versus app, SQLite storage, and the request/session flow that protects the dashboard. Explain the purpose of POST and CSRF on logout. The student has not yet supplied a response.

### Open issues

Required screenshots and manual review remain pending; Deliverable 3 evidence is incomplete. FR-17's create-account link waits for INC-02 registration. Full FR-09/AC-01 and all-route AC-03 remain partial by design. Next increment: INC-02 registration and automatic login. No design scope or stable IDs were changed.
