# System Design

## 1. Design baseline

**Project:** Movie Finder — Kate McKenzie. **Baseline:** [01-proposal.md](01-proposal.md), November 11, 2026. **Status:** Planning draft; nothing is claimed built or tested. Instructor feedback has not been supplied.

Movie Finder helps users choose movies through search, genre browsing, recommendations and random discovery, with private watchlists.

**Scope changes:** TMDb replaces the CSV/local movie catalog. SQLite stores accounts, sessions and saved references. Multi-genre browsing requires ALL selected genres. Popular movies, registration, details, posters and private watchlists are required. Rating/runtime/year filters, runtime display, trailers, streaming availability, personal ratings, watched status and custom/personalized recommendations are excluded.

**IDs:** FR-01, FR-03, FR-04, FR-08–FR-11 retain their revised proposal meanings. FR-06 and FR-12 are now Must. FR-16 replaces retired FR-02; FR-17 adds public welcome access. FR-05 and FR-13–FR-15 remain retired. FR-07 remains Later for TV shows/interface polish. No retired IDs are reused.

## 2. System context

![Movie Finder — System Architecture](diagrams/system-architecture.png)

[Full-size SVG](diagrams/system-architecture.svg) · [Editable source](diagrams/system-architecture.dot)

The browser displays HTML/CSS and Django templates. Django validates requests and checks login. TMDb supplies movie information and poster references; SQLite stores accounts, sessions and watchlists. Saved titles remain readable during an API outage, but discovery and current details may be unavailable.

## 3. Data model

![Movie Finder — Data Model (ERD)](diagrams/data-model.png)

[Full-size SVG](diagrams/data-model.svg) · [Editable source](diagrams/data-model.dot)

Use Django's built-in User and one WatchlistEntry model. One user owns many entries; each entry belongs to one user. TMDb IDs identify external movies, so no local Movie table is needed. Standard Django session tables are omitted from the ERD.

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

Use labeled forms, escaped text, shared cards, poster placeholders and return-home links. Initial unsubmitted search/browse forms show choices without errors. No numeric/year filters are included.

## 5. Main user flow

![Movie Finder — Main User Flow](diagrams/main-user-flow.png)

[Full-size SVG](diagrams/main-user-flow.svg) · [Editable source](diagrams/main-user-flow.dot)

Valid registration/login creates a session and opens the dashboard. Discovery leads to results, details and saving. The watchlist supports opening/removing saved movies. Error paths allow retry; rounded continuation nodes avoid crossing return arrows. Logout ends protected access.

## 6. Access and login

| Role | Allowed actions | Ownership / Access restriction |
|---|---|---|
| Visitor | Welcome, register, login | No discovery/details/watchlist access |
| Signed-in user | All movie features and own watchlist | Only their entries can be viewed or changed |
| Active superuser | Django Admin users/registered watchlist models | Separate admin permissions; normal application views remain owner-filtered |

Django's built-in forms validate usernames/passwords, store password hashes and manage sessions. Successful registration automatically signs the user in and opens `/dashboard/`; valid login does the same. Invalid information shows errors without granting access.

Every protected view checks login, including direct URL requests. Watchlist ownership comes from `request.user`, never a submitted user ID. List/removal queries filter by owner. POST/CSRF protections apply to registration, login, logout, saves and removal; GET cannot mutate saved entries. Logout clears the session and returns to welcome; new protected requests require login again.

Create foundation demo credentials locally with interactive `createsuperuser`, then use ordinary fictional accounts for registration/privacy checks. Never commit credentials or the local database. Django Admin alone does not fulfill the required user-facing login and protected-page build.

## 7. Integrations and configuration

| Dependency / API | Purpose | Official documentation | Environment variable names | Failure / Sample-data fallback |
|---|---|---|---|---|
| Python/Django | Backend, templates, forms/authentication | [Python](https://docs.python.org/3/), [Django](https://docs.djangoproject.com/en/stable/) | `DJANGO_SECRET_KEY`; local `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` if used | Pin compatible versions during build; accounts work without TMDb |
| SQLite | Accounts, sessions, watchlists | [SQLite notes](https://docs.djangoproject.com/en/stable/ref/databases/#sqlite-notes) | None required | Migrations preserve data; saved titles remain available locally |
| TMDb API/images | Popular/search/genres/details/recommendations/posters | [API](https://developer.themoviedb.org/docs/getting-started), [Authentication](https://developer.themoviedb.org/docs/authentication-application), [Images](https://developer.themoviedb.org/docs/image-basics) | `TMDB_READ_ACCESS_TOKEN` | Timeout/error messages and poster placeholder; fictional responses for tests only |

Use one server-side API helper with a proposed 10-second timeout. Planned requests cover popular movies, search, genre list, discover with ALL genres, details, recommendations and image configuration. Credentials stay in process environment variables, never browser code or Git. Document local setup; Django does not automatically load `.env` files.

Distinguish empty results from connection/authorization/rate-limit/malformed-response errors. Show helpful messages without raw errors or secrets. Failed movie validation must not create a new saved entry. Access, terms and attribution checks remain open in section 11; no live API access is claimed.

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

Saved title snapshots are not an offline movie catalog. No custom storyline scoring, personal ratings or removed features are restored.

## 9. Build increments

All six existing increment IDs remain. Each step must be demonstrated and checked before continuing.

| Increment ID | Demonstrable outcome | Requirement IDs | Data / Pages needed | Acceptance criterion IDs |
|---|---|---|---|---|
| INC-01 | Django/SQLite authentication foundation | FR-01, FR-17; foundation FR-09 | Migrations, welcome/login, protected dashboard shell, POST logout | AC-02, AC-04, AC-42; foundation portions AC-01, AC-03 |
| INC-02 | Registration with automatic login | FR-08, FR-01, FR-09 | Registration form, session/shared layout | AC-15, AC-16; account portion AC-01 |
| INC-03 | Popular/search/details/posters | FR-09, FR-10, FR-03, FR-12, FR-04, FR-01 | API helper, dashboard/search/details, placeholder | AC-01, AC-20, AC-23, AC-28, AC-41; relevant portions AC-07, AC-08, AC-17, AC-40, AC-43 |
| INC-04 | ALL-genre browse/recommendations | FR-16, FR-10, FR-03, FR-12, FR-04, FR-01 | Browse/related pages; reused details | AC-19, AC-21, AC-33, AC-34, AC-35, AC-36; relevant portions AC-07, AC-08, AC-40, AC-43 |
| INC-05 | Surprise Me/Try Again | FR-11, FR-03, FR-04, FR-01 | Random selection, details/retry | AC-24, AC-25, AC-26, AC-27; random portions AC-07, AC-40 |
| INC-06 | Private persistent watchlists | FR-06, FR-01, FR-03, FR-04, FR-09 | Model/migration, save/list/remove, two accounts | AC-37, AC-38, AC-39; finish AC-01, AC-03, AC-07, AC-17, AC-40, AC-43 |

**November 18 initial build — INC-01:** Before movie features, produce a runnable foundation proving valid login, invalid-login rejection, protected-page access, anonymous denial/redirect and logout ending access. Capture three screenshots: sign-in page, protected page after login, and restricted access after logout. Admin login alone is insufficient. Full popular-dashboard and later-route criteria remain pending until built.

**Before December 7:** Target registration/API search by November 22, browsing/recommendations by November 27, random selection by November 30 and watchlists by December 3. Reserve December 4–7 for fixes, verification and video. API readiness is needed before INC-03; local authentication work can proceed independently. Dates are planned, not completed milestones.

## 10. Verification and delivery plan

All checks are planned and unrun. Use fictional accounts/responses for repeatable Django tests, browser checks for navigation/images, and a separate live API check. Preserve actual pass/fail/blocked results in the build log.

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

Run Django system/migration checks and relevant tests during the build; record test counts and failures. Mocked passes do not prove live access. Screenshots/logs must not expose credentials.

**Final video — December 7:** Explain the problem/scope; show welcome (FR-17), registration/login/popular dashboard (FR-08, FR-01, FR-09), search/recommendations/details/posters (FR-10, FR-03, FR-12), ALL-genre browsing (FR-16), Surprise Me (FR-11), private save/remove/persistence (FR-06), an error (FR-04), then logout/protected access. Explain the diagrams and key design choices. Supporting tests cover remaining edge cases; clearly label simulated failures. The local video, timestamps/link and actual evidence remain pending; hosting is not required.

## 11. Decisions, risks, and student explanation

Django provides pages, forms, login and database tools in one Python project. SQLite supports local persistent accounts/watchlists. TMDb avoids maintaining a catalog or custom recommendation algorithm.

| Risk / Open question | Planned response |
|---|---|
| API access, costs, licensing and attribution | Check current [TMDb documentation](https://developer.themoviedb.org/docs/getting-started) and [FAQ](https://developer.themoviedb.org/docs/faq), credentials/networking, limits, image use and permitted title storage before API work. Do not assume unrestricted/free access. |
| Response formats, ALL-genre syntax and changing results | Verify rating scale, fields, image setup and endpoint semantics; use fictional tests plus AC-43 live evidence. |
| Outages, missing data, privacy or duplicates | Apply the messages/placeholders and owner/unique/POST rules above; test failures and two-user access. |
| Timeline and review | Build authentication first; exclude extra features. Choose compatible Python/Django versions during implementation. Instructor feedback, student explanation and remote diagram review remain pending. Document API blockers rather than silently changing sources. |

**Student explanation remains pending:** Kate described searching by movie/genre and seeing results. As a learning guide, a request reaches a Django URL and view; the view checks login/input, calls TMDb for movies or queries SQLite for the user's saves, then a template returns HTML. Saving adds an account-linked entry, not a movie to TMDb. Explain this in your own words, including why ownership matters and what works during outages.

**Rubric review:** Sections 1–11 retain the baseline/scope changes, architecture, data model/validation/deletion, page URLs, user flow, access rules, integration/configuration/failures, business examples, linked increments, all 29 active criteria/video plan, and decisions/risks/student checkpoint. All three image references are preserved. No application implementation or test success is claimed.
