# Bootstrap Report

## 1. Environment and sources

Checked November 16, 2026. Existing `.venv` reused; it contained Python 3.14.3 and no Django. Installed Django 6.1.3, asgiref 3.13.0, sqlparse 0.6.1; exact pins are in `requirements.txt`.

Official sources checked at execution time: [Django download](https://www.djangoproject.com/download/) listed 6.1.3 as the latest stable release; [Python compatibility](https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django) listed Python 3.14 for Django 6.1. SQLite is supplied by Python. No TMDb integration was attempted.

## 2. Files and commands

`config` is the Django project (settings and URL routing); `movies` is the business app (welcome and dashboard views). Shared templates and CSS supply the user-facing pages. Built-in Django LoginView, LogoutView, authentication form, password hashing and sessions manage access. The dashboard uses `login_required`; logout is a POST form with a CSRF token. No business models exist yet; built-in migrations created account/session tables in local SQLite.

Clean setup and macOS/Linux/PowerShell commands: [README](../README.md). Run `create_demo_user` for an ordinary local account using hidden interactive password prompts. No persistent demonstration account or credentials were created during this build. Environment configuration and the temporary secret-key fallback are documented in the README.

Commands executed: Django startproject/startapp, pip installation/freeze, migrate, check, makemigrations --check --dry-run, test, and runserver with --noreload. Dependency download and local server/network checks required sandbox approval.

## 3. Verification results

- `migrate`: all 18 built-in migrations applied successfully.
- `check`: no issues.
- `makemigrations --check --dry-run`: no changes detected.
- `test`: 8 authentication tests passed. Covers public welcome/login; anonymous dashboard redirect; valid login/session/dashboard; invalid-login errors with no access; POST logout ending access; GET logout rejected (405); login/logout CSRF enforcement (403 without token, success with token); rejection of external login redirects. Test passwords are generated in memory.
- Actual local HTTP smoke check: welcome returned 200; anonymous dashboard returned 302 to `/accounts/login/?next=/dashboard/`.
- Browser appearance, manual credential entry and screenshots: **unverified/pending**. No browser tools are available in this session.

Capture steps (do not include passwords):
1. Start the server and open `/accounts/login/`. Capture the empty sign-in form.
2. Sign in using your locally created fictional account. Capture `/dashboard/` with the greeting and logout control.
3. Click Log out; directly request `/dashboard/`. Capture the redirected login page with `next=/dashboard/` visible in the address bar.
4. Save the three images in `deliverables/screenshots/` and add their actual filenames here. No screenshots have been captured by the agent.

## 4. Student checkpoint

Pending student response: Explain what the virtual environment isolates, how `config` differs from `movies`, what `db.sqlite3` stores, and how a dashboard request checks the Django session before rendering. Explain why logout uses POST with CSRF protection. No student explanation or approval is claimed.

## 5. Open issues

INC-01 implementation and automated checks are complete; browser review and required screenshot evidence remain pending. Course Deliverable 3 is not fully evidenced until the screenshots are supplied. Registration is INC-02; popular movies/discovery/details/watchlists remain later work. Full FR-09 and all-route AC-03 checks cannot pass until those routes exist. FR-17's public welcome is implemented; its account-creation link waits for registration in INC-02, as sequenced in the design.
