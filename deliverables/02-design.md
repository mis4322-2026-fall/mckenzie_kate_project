# System Design

## 1. Design baseline

**Project:** Movie Finder — Kate McKenzie. **Baseline:** [01-proposal.md](01-proposal.md), November 11, 2026. **Status:** Proposed system design, not a record of completed implementation or testing. Instructor feedback has not been supplied.

Movie Finder helps users choose movies through search, genre browsing, recommendations and random discovery, with private watchlists.

**Scope changes:** TMDb replaces the CSV/local movie catalog. SQLite stores accounts, sessions and saved references. Multi-genre browsing requires ALL selected genres. Popular movies, registration, details, posters and private watchlists are required. Rating/runtime/year filters, runtime display, trailers, streaming availability, personal ratings, watched status and custom/personalized recommendations are excluded.

**IDs:** Retain the proposal's FR-01, FR-03, FR-04, FR-08–FR-11. FR-06/FR-12 are Must; FR-16 replaces retired FR-02; FR-17 covers welcome. FR-05/FR-13–FR-15 remain retired. FR-07 is Later for TV shows/interface polish.

## 2. System context

![Movie Finder — System Architecture](diagrams/system-architecture.png)

[Full-size SVG](diagrams/system-architecture.svg) · [Editable source](diagrams/system-architecture.dot)

Django checks requests/login and returns HTML/CSS pages. TMDb supplies movie information/posters; SQLite stores accounts, sessions and watchlists. Saved titles remain readable during API outages; discovery/details may be unavailable.

## 3. Data model

![Movie Finder — Data Model (ERD)](diagrams/data-model.png)

[Full-size SVG](diagrams/data-model.svg) · [Editable source](diagrams/data-model.dot)

Use Django's User and WatchlistEntry. Each entry belongs to one user and references a TMDb ID; no local Movie table is needed. Session tables are omitted for readability.

| Entity | Field | Django field type | Required / Default | Validation | Relationship / Deletion rule |
|---|---|---|---|---|---|
| User | id | Built-in primary key | Automatic | Unique | Owns saved entries |
| User | username | Built-in CharField | Required | Unique; Django rules | Account identity |
| User | password | Built-in CharField | Required | Django-managed hash/validators | Never plain text |
| User | is_active, is_staff, is_superuser | BooleanFields | Django defaults | Built-in permission checks | Admin access separate |
| WatchlistEntry | id | BigAutoField | Automatic | Unique | Entry identifier |
| WatchlistEntry | user | ForeignKey to AUTH_USER_MODEL | Required | Signed-in user | CASCADE on user deletion |
| WatchlistEntry | tmdb_movie_id | PositiveIntegerField | Required | Valid ID; unique with user | External movie reference |
| WatchlistEntry | title_snapshot | CharField(500) | Required | Nonblank; length limit | Readable during outages |
| WatchlistEntry | saved_at | DateTimeField | auto_now_add=True | Server timestamp | Removed with entry |

The database enforces a unique `(user, tmdb_movie_id)` pair. Removing an entry affects neither another user's saves nor the TMDb movie.

## 4. Pages and actions

Only welcome, registration and login are public. All other routes require login. GET reads information; account and saved-entry changes use CSRF-protected POST forms.

| Requirement ID | Page / URL | User action / HTTP method | Input and validation | Result / Template |
|---|---|---|---|---|
| FR-17 | `/` | GET welcome | None | `welcome.html`; account links |
| FR-08, FR-04 | `/accounts/register/` | GET form; POST register | Unique username; matching valid passwords | `registration/register.html`; errors or automatic login/dashboard |
| FR-01, FR-04, FR-09 | `/accounts/login/` | GET form; POST login | Django checks credentials | `registration/login.html`; error or dashboard |
| FR-01 | `/accounts/logout/` | POST logout | Session, CSRF | End session; welcome |
| FR-09, FR-12, FR-04 | `/dashboard/` | GET popular movies/navigation | Valid API response | `dashboard.html`; cards or message |
| FR-10, FR-12, FR-04 | `/movies/search/?q=...` | GET title search | Trim; nonblank submission, max 200 characters | `movies/search.html`; matches/message |
| FR-16, FR-12, FR-04 | `/movies/browse/?genre=...` | GET genre browsing; repeat genre parameter for multiple choices | Valid IDs; at least one on submission; ALL matching | `movies/browse.html`; matches/message |
| FR-11, FR-03, FR-04, FR-12 | `/movies/surprise/` | GET random movie/Try Again | Valid candidate set | Selected details with Try Again; error uses `movies/surprise.html` |
| FR-03, FR-12, FR-04 | `/movies/<tmdb_id>/` | GET details | Positive ID; handle missing data | `movies/detail.html`; Save/related controls |
| FR-10, FR-12, FR-04 | `/movies/<tmdb_id>/recommendations/` | GET related movies | Valid ID; exclude original/duplicates | `movies/recommendations.html` |
| FR-06, FR-01 | `/watchlist/` | GET saved entries | Current user only | `watchlist/list.html`; titles/detail/remove controls |
| FR-06, FR-04 | `/watchlist/add/` | POST save | CSRF; server-validated movie ID/title; prevent duplicates | Redirect with saved/error feedback |
| FR-06, FR-01 | `/watchlist/<entry_id>/remove/` | POST remove | CSRF; entry ID and current owner | Remove own entry; redirect, or generic not-found |

Use labeled forms, safely displayed text, poster placeholders and return-home links. Search/browse forms show no errors until submitted.

## 5. Main user flow

![Movie Finder — Main User Flow](diagrams/main-user-flow.png)

[Full-size SVG](diagrams/main-user-flow.svg) · [Editable source](diagrams/main-user-flow.dot)

Registration/login opens the dashboard. Discovery leads to details and saving; watchlists support opening/removing entries. Rounded nodes indicate retry/home navigation without crossing return arrows. Logout ends protected access.

## 6. Access and login

| Role | Allowed actions | Ownership / Access restriction |
|---|---|---|
| Visitor | Welcome, register, login | No discovery/details/watchlist access |
| Signed-in user | All movie features and own watchlist | Only their entries can be viewed or changed |
| Active superuser | Django Admin users/registered watchlist models | Separate admin permissions; normal application views remain owner-filtered |

Django's built-in forms validate usernames/passwords, store password hashes and manage sessions. Successful registration automatically signs the user in and opens `/dashboard/`; valid login does the same. Invalid information shows errors without granting access.

Protected views check login, including direct URLs. Watchlist queries use `request.user` to enforce ownership. Account changes/saves/removals require POST and Django's CSRF protection against forged submissions; GET cannot change saved data. Logout ends the session.

Create a local demonstration account using Django's interactive `createsuperuser`, then ordinary fictional accounts for privacy checks. Keep credentials and the local database out of Git. Django Admin alone does not meet the initial-build requirement: a user-facing login and protected application page are required.

## 7. Integrations and configuration

| Dependency / API | Purpose | Official documentation | Environment variable names | Failure / Sample-data fallback |
|---|---|---|---|---|
| Python/Django | Backend, templates, forms/authentication | [Python](https://docs.python.org/3/), [Django](https://docs.djangoproject.com/en/stable/) | `DJANGO_SECRET_KEY`; local `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` if used | Pin compatible versions during build; accounts work without TMDb |
| SQLite | Accounts, sessions, watchlists | [SQLite notes](https://docs.djangoproject.com/en/stable/ref/databases/#sqlite-notes) | None required | Migrations preserve data; saved titles remain available locally |
| TMDb API/images | Popular/search/genres/details/recommendations/posters | [API](https://developer.themoviedb.org/docs/getting-started), [Authentication](https://developer.themoviedb.org/docs/authentication-application), [Images](https://developer.themoviedb.org/docs/image-basics) | `TMDB_READ_ACCESS_TOKEN` | Timeout/error messages and poster placeholder; fictional responses for tests only |

One Django helper requests popular/search/genre/detail/recommendation data and posters. Use a server-side read-access token after checking TMDb's instructions. Keep credentials in environment variables, not browser code/Git; document local setup.

Use a 10-second timeout, readable errors and poster placeholders. Distinguish empty results from failures; never reveal credentials. Validate movies before saving. Open API checks appear in section 11.

## 8. Outputs and business rules

Fictional examples: A = Moonlight Picnic (Comedy); B = Garden of Laughs (Comedy, Family); C = Clockwork Harbor (Mystery).

| Requirement ID | Output / Rule | Calculation or format | Example |
|---|---|---|---|
| FR-09 | Popular dashboard | TMDb order; remove duplicate IDs; popularity differs from rating | A/B/B displays A/B |
| FR-10 | Search/recommendations | TMDb title matching; select by ID; related results retain provider order, excluding original/duplicates | For A, related A/B/B/C becomes B/C |
| FR-16 | ALL genres | At least one valid genre; every selected genre must match | Comedy matches A/B; Comedy + Family matches B |
| FR-11 | Surprise Me/Try Again | Choose one unique valid candidate from a bounded popular response; repeats allowed | A/B/C each have 1-in-3 chance within that set, not all TMDb |
| FR-03, FR-12 | Details/posters | Title, genres, rating/verified scale, description, poster/placeholder | Missing rating is labeled unavailable, not invented as zero |
| FR-06 | Save/view/remove | Unique user/movie pair; private newest-first list; owner-only POST removal; persistence across restart | Saving B twice leaves one entry; removing my B leaves other users' B unchanged |
| FR-04 | Messages | Helpful invalid-input, empty, missing-field or service-error message | API failure means unavailable, not no matches |

A saved title stays readable offline, but current movie details still depend on TMDb.

## 9. Build increments

Keep the six existing increment IDs, but build INC-06 after INC-03 so database functionality is demonstrated earlier. IDs identify work, not its position in the schedule.

| Increment ID | Demonstrable outcome | Requirement IDs | Data / Pages needed | Acceptance criterion IDs |
|---|---|---|---|---|
| INC-01 | Django/SQLite authentication foundation | FR-01, FR-17; foundation FR-09 | Migrations, welcome/login, protected dashboard shell, POST logout | AC-02, AC-04, AC-42; foundation portions AC-01, AC-03 |
| INC-02 | Registration with automatic login | FR-08, FR-01, FR-09 | Registration form, session/shared layout | AC-15, AC-16; account portion AC-01 |
| INC-03 | Popular/search/details/posters | FR-09, FR-10, FR-03, FR-12, FR-04, FR-01 | API helper, dashboard/search/details, placeholder | AC-01, AC-20, AC-23, AC-28, AC-41; relevant portions AC-07, AC-08, AC-17, AC-40, AC-43 |
| INC-06 | Private persistent watchlists | FR-06, FR-01, FR-03, FR-04, FR-09 | Model/migration, save/list/remove, two accounts | AC-37, AC-38, AC-39; watchlist portions AC-03, AC-07, AC-17, AC-40 |
| INC-04 | ALL-genre browse/recommendations | FR-16, FR-10, FR-03, FR-12, FR-04, FR-01 | Browse/related pages; reused details | AC-19, AC-21, AC-33, AC-34, AC-35, AC-36; relevant portions AC-07, AC-08, AC-40, AC-43 |
| INC-05 | Surprise Me/Try Again | FR-11, FR-03, FR-04, FR-01 | Random selection, details/retry | AC-24, AC-25, AC-26, AC-27; random portions AC-07, AC-40 |

**November 18 initial build — INC-01:** Before movie features, produce a runnable foundation proving valid login, invalid-login rejection, protected-page access, anonymous denial/redirect and logout ending access. Capture three screenshots: sign-in page, protected page after login, and restricted access after logout. Admin login alone is insufficient. Full popular-dashboard and later-route criteria remain pending until built.

**Later schedule:** Registration and API search/details by November 22; private watchlists by November 24; browsing/recommendations by November 27; Surprise Me by November 30. December 1–3 completes shared checks across all routes, including full AC-01, AC-03, AC-07, AC-17, AC-40 and AC-43. Reserve December 4–7 for fixes and the final video. Verify API access before INC-03; authentication does not depend on it. These are target dates.

## 10. Verification and delivery plan

Use fictional accounts and sample API responses for repeatable Django tests, browser checks for navigation/images, and a separate live TMDb check. Record actual outcomes in the build log.

| Criterion ID | Sample input / Setup | Action | Expected result | Verification method |
|---|---|---|---|---|
| AC-01, AC-02, AC-03, AC-04, AC-27, AC-42 | Valid/invalid accounts; anonymous visitor | Login, direct protected URLs, logout/revisit, welcome | Correct access; logout ends session; welcome public | Access tests/browser sequence; full dashboard checked later |
| AC-15, AC-16 | Valid/duplicate username; matching/mismatched/rejected passwords | Register | Automatic authenticated dashboard or errors/no account | Form/session tests; browser |
| AC-07, AC-17, AC-28, AC-41 | Popular/details responses; missing poster/fields/ID | Navigate all detail entry paths | Required fields, navigation, placeholders/honest messages | View/template tests; browser image-failure check |
| AC-08, AC-20, AC-21 | Blank/unknown search; empty browse/related results | Submit requests | Validation/empty messages; details remain usable | Mocked form/view tests |
| AC-19, AC-23, AC-36 | Duplicate titles/IDs; related A/B/B for A | Select movie and recommendations | Correct selected ID; B once; A excluded | Mocked requests/results; browser |
| AC-24, AC-25, AC-26 | A/B/C, one or no candidates | Surprise Me/Try Again | One valid result or message; repeats allowed | Controlled random-choice tests; browser |
| AC-33, AC-34, AC-35 | Comedy; Comedy + Family; empty/invalid genre IDs | Browse | A/B; only B; invalid input rejected before API call | Mocked parameter/result tests; live semantics separately |
| AC-37, AC-38, AC-39 | Two users save B | Save twice, restart, cross-user access/removal, own removal, GET mutation | Unique persistent saves; privacy; only own entry removed; GET cannot mutate | Database/CSRF/ownership tests; restart check |
| AC-40 | Timeout, denied access, rate limit, malformed response; saved title | Request movies and watchlist | Helpful error without secrets; saved titles readable | Mocked failure tests |
| AC-43 | Securely configured TMDb access | Live popular/search/details/related/ALL-genre requests | Real data or honest empty states; verified behavior/attribution | Separate live integration checklist |

During the build, run Django system, migration and feature tests; record counts and failures. Sample responses do not prove live access. Keep credentials out of screenshots/logs.

**Final video — December 7:** Explain the problem/scope; show welcome (FR-17), registration/login/popular dashboard (FR-08, FR-01, FR-09), search/recommendations/details/posters (FR-10, FR-03, FR-12), ALL-genre browsing (FR-16), Surprise Me (FR-11), private save/remove/persistence (FR-06), an error (FR-04), then logout/protected access. Explain the diagrams and key design choices. Supporting tests cover edge cases; label simulated failures. Record video timestamps and link when available. Hosting is not required.

## 11. Decisions, risks, and student explanation

Django unifies the Python backend and pages; SQLite stores local accounts/watchlists. TMDb replaces CSV preparation and custom recommendation logic.

| Risk / Open question | Planned response |
|---|---|
| TMDb access and usage terms | Check [official documentation](https://developer.themoviedb.org/docs/getting-started) and [FAQ](https://developer.themoviedb.org/docs/faq) for credentials, costs, request limits, image use, attribution and permitted title storage before API work. |
| API behavior and changing information | Confirm fields, rating scale and ALL-genre request format. Use repeatable sample responses plus the live check in AC-43. |
| Outages or incomplete data | Use timeouts, placeholders and helpful messages; preserve locally saved titles. |
| Watchlist privacy | Check ownership on the server, prevent duplicate saves and test with two accounts. |
| Schedule and review | Keep the November 18 foundation small and build watchlists earlier. Confirm compatible Python/Django versions, review the GitHub diagrams and record any instructor feedback. If API access is blocked, discuss the scope rather than silently replacing the source. |

### Student explanation — draft to review and personalize

When a user searches for a movie, the browser sends the title to Django. Django checks that the user is signed in, validates the title and asks TMDb for matching movies. A Django template then displays the results. Selecting a movie opens its details and available recommendations.

SQLite stores each saved movie's TMDb ID and title with a link to the user's account. This lets users return to their own watchlists later. Authentication is necessary so Django knows whose saved movies to display and prevents other users from changing them.

Django fits this project because its forms, templates and login tools work together in Python. SQLite is suitable for a local college project because it stores accounts and watchlists without another database service. TMDb provides the movie information, so the project can focus on the user experience instead of preparing a movie dataset.

**Before submission:** Personalize this draft, check the GitHub diagrams and confirm the scope. API access/terms and instructor review remain open. All 11 sections, active IDs, 29 criteria and three diagrams remain.
