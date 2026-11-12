# Movie Finder — System Design

## 1. Design baseline

**Student:** Kate McKenzie · **Proposal:** [01-proposal.md](01-proposal.md), November 11, 2026. This is a proposed design, not completed work.

Movie Finder helps users choose movies and save them to private watchlists. **Scope change:** TMDb replaces the original CSV/local movie catalog. SQLite stores accounts and saved entries. Genre browsing matches ALL selected genres. Registration, popular movies, posters and watchlists are required. Rating/runtime/year filters, trailers, streaming, personal ratings and custom/personalized recommendations are excluded.

Retain active FR-01, FR-03, FR-04, FR-06, FR-08, FR-09, FR-10, FR-11, FR-12, FR-16 and FR-17. FR-07 remains Later for TV shows/interface polish. FR-02, FR-05 and FR-13–FR-15 remain retired; IDs are not reused.

## 2. System context

![Movie Finder — System Architecture](diagrams/system-architecture.png)

[Full-size diagram](diagrams/system-architecture.svg) · [Editable source](diagrams/system-architecture.dot)

Django checks requests/login and returns HTML/CSS pages. TMDb supplies movies and posters; SQLite stores accounts, sessions and private watchlists. Saved titles remain available during API outages, but discovery may not.

## 3. Data model

![Movie Finder — Data Model (ERD)](diagrams/data-model.png)

[Full-size diagram](diagrams/data-model.svg) · [Editable source](diagrams/data-model.dot)

One user owns many saved entries; each entry belongs to one user. Movies remain in TMDb, not a local movie table.

| Entity | Field | Django field type | Required / Default | Validation | Relationship / Deletion rule |
|---|---|---|---|---|---|
| User | id, username | Built-in ID, CharField | Required/automatic ID | Unique | Owns entries |
| User | password | Built-in CharField | Required | Django hash/validators | Never plain text |
| User | active/staff/superuser flags | Built-in BooleanFields | Django defaults | Permission checks | Admin access |
| WatchlistEntry | id | BigAutoField | Automatic | Unique | Entry ID |
| WatchlistEntry | user | ForeignKey | Required | Current user | CASCADE on user deletion |
| WatchlistEntry | tmdb_movie_id | PositiveIntegerField | Required | Unique with user; valid movie | External ID |
| WatchlistEntry | title_snapshot | CharField(500) | Required | Nonblank | Readable during outages |
| WatchlistEntry | saved_at | DateTimeField | Automatic timestamp | Server-set | Removed with entry |

The unique user/movie pair prevents duplicate saves. Removing one save affects neither other users nor TMDb.

## 4. Pages and actions

Welcome, registration and login are public; all other pages require login. GET reads data. Account and watchlist changes use POST with Django's CSRF protection against forged submissions.

| Requirement ID | Page / URL | User action / HTTP method | Input and validation | Result / Template |
|---|---|---|---|---|
| FR-17 | `/` | GET welcome | None | `welcome.html`; account links |
| FR-08, FR-04 | `/accounts/register/` | GET/POST register | Unique username; valid matching passwords | `registration/register.html`; errors or automatic login/dashboard |
| FR-01, FR-04, FR-09 | `/accounts/login/` | GET/POST login | Valid credentials | `registration/login.html`; dashboard/error |
| FR-01 | `/accounts/logout/` | POST logout | Session/CSRF | Welcome; session ended |
| FR-09, FR-12 | `/dashboard/` | GET popular movies | API response | `dashboard.html`; cards/navigation |
| FR-10, FR-04 | `/movies/search/?q=...` | GET search | Trim; nonblank, max 200 characters | `movies/search.html`; results/message |
| FR-16, FR-04 | `/movies/browse/?genre=...` | GET browse | One or more valid IDs; ALL matching | `movies/browse.html`; results/message |
| FR-11, FR-04 | `/movies/surprise/` | GET random/Try Again | Valid candidate set | Details or `movies/surprise.html` message |
| FR-03, FR-12 | `/movies/<tmdb_id>/` | GET details | Valid movie ID | `movies/detail.html`; fields, Save/related controls |
| FR-10 | `/movies/<tmdb_id>/recommendations/` | GET related movies | Valid ID | `movies/recommendations.html` |
| FR-06, FR-01 | `/watchlist/` | GET saved movies | Current owner only | `watchlist/list.html` |
| FR-06, FR-04 | `/watchlist/add/` | POST save | CSRF; server-valid movie/title | Redirect with saved/error feedback |
| FR-06, FR-01 | `/watchlist/<entry_id>/remove/` | POST remove | CSRF; entry belongs to user | Remove/redirect or not-found |

Forms have clear labels/errors, templates display text safely, and pages provide home navigation. Posters use placeholders when missing; all movie pages handle API failures.

## 5. Main user flow

![Movie Finder — Main User Flow](diagrams/main-user-flow.png)

[Full-size diagram](diagrams/main-user-flow.svg) · [Editable source](diagrams/main-user-flow.dot)

Login/registration leads to the dashboard. Users discover movies, open details, save/remove entries or log out. Error paths allow retry; rounded continuation nodes avoid crossing return arrows.

## 6. Access and login

| Role | Allowed actions | Ownership / Access restriction |
|---|---|---|
| Visitor | Welcome/register/login | No protected pages |
| Signed-in user | Movie discovery and own watchlist | Only their saved entries |
| Active superuser | Django Admin users/registered entries | Separate admin permissions |

Use Django forms, password hashing and sessions. Valid registration automatically logs the user in and opens the dashboard; valid login does the same. Invalid information shows errors.

Every protected view checks login, even for direct URLs. Watchlist queries use `request.user`, not a submitted owner. Only owner-checked POST requests save/remove entries; GET cannot change them. POST logout ends the session, so protected pages require login again.

Create local demo accounts with interactive Django tools, then ordinary fictional accounts for privacy checks. Keep credentials/database files out of Git. Admin login alone does not satisfy the required user-facing login and protected dashboard.

## 7. Integrations and configuration

| Dependency / API | Purpose | Official documentation | Environment variable names | Failure / Sample-data fallback |
|---|---|---|---|---|
| Python/Django | Backend/pages/authentication | [Django](https://docs.djangoproject.com/en/stable/), [Python](https://docs.python.org/3/) | `DJANGO_SECRET_KEY`; local debug/host settings if used | Accounts work without TMDb |
| SQLite | Accounts/sessions/watchlists | [SQLite notes](https://docs.djangoproject.com/en/stable/ref/databases/#sqlite-notes) | None required | Saved titles remain local |
| TMDb/images | Popular/search/genres/details/related movies/posters | [API](https://developer.themoviedb.org/docs/getting-started), [Authentication](https://developer.themoviedb.org/docs/authentication-application), [Images](https://developer.themoviedb.org/docs/image-basics) | `TMDB_READ_ACCESS_TOKEN` | 10-second timeout, helpful errors, placeholders; fictional test responses |

Use one server-side API helper. Keep tokens in environment variables, not browser code/Git. Distinguish no results from failed requests; validate movies before saving. Live API and usage checks remain open in section 11.

## 8. Outputs and business rules

Fictional examples: A has Comedy; B has Comedy/Family; C has Mystery.

| Requirement ID | Output / Rule | Calculation or format | Example |
|---|---|---|---|
| FR-09 | Popular movies | Provider order; unique IDs | A/B/B becomes A/B |
| FR-10 | Search/related movies | Match via TMDb; select by ID; exclude original/duplicate recommendations | For A, related A/B/B/C becomes B/C |
| FR-16 | ALL genres | Require every selected genre | Comedy: A/B; Comedy + Family: B |
| FR-11 | Surprise Me | Random unique valid candidate from one bounded popular response; repeats allowed | A/B/C: 1-in-3 each within that set |
| FR-03, FR-12 | Details | Poster/placeholder, title, genres, rating/scale, description | Missing rating says unavailable |
| FR-06 | Private saves | Unique user/movie; newest first; persistent owner-only removal | Saving twice leaves one entry |
| FR-04 | Helpful messages | Invalid, empty, missing or service-unavailable states | Failed API request is not “no matches” |

## 9. Build increments

Keep existing increment IDs; build watchlists earlier, after API details.

| Increment ID | Demonstrable outcome | Requirement IDs | Data / Pages needed | Acceptance criterion IDs |
|---|---|---|---|---|
| INC-01 | Django/SQLite login foundation | FR-01, FR-17; foundation FR-09 | Welcome/login/protected dashboard/logout | AC-02, AC-04, AC-42; foundation AC-01, AC-03 |
| INC-02 | Registration/automatic login | FR-08, FR-01, FR-09 | Form/session/layout | AC-15, AC-16; account AC-01 |
| INC-03 | Popular/search/details/posters | FR-09, FR-10, FR-03, FR-12, FR-04, FR-01 | API helper/cards/details | AC-01, AC-20, AC-23, AC-28, AC-41; portions AC-07, AC-08, AC-17, AC-40, AC-43 |
| INC-06 | Private watchlists | FR-06, FR-01, FR-03, FR-04, FR-09 | Model/migration/save/list/remove | AC-37–AC-39; watchlist portions AC-03, AC-07, AC-17, AC-40 |
| INC-04 | Genres/recommendations | FR-16, FR-10, FR-03, FR-12, FR-04, FR-01 | Browse/related pages | AC-19, AC-21, AC-33–AC-36; portions AC-07, AC-08, AC-40, AC-43 |
| INC-05 | Surprise Me/Try Again | FR-11, FR-03, FR-04, FR-01 | Random view/details | AC-24–AC-27; portions AC-07, AC-40 |

**November 18:** Complete INC-01 before movie features. Prove valid login, invalid-login rejection, protected access, anonymous denial/redirect and logout ending access. Required screenshots: sign-in, protected page after login, and restricted access after logout. Use a runnable Django/SQLite project, not admin login alone.

**Later targets:** Registration/API details November 22; watchlists November 24; genres/recommendations November 27; random discovery November 30. Complete full shared criteria by December 3; reserve December 4–7 for fixes and the video. API access is needed before INC-03.

## 10. Verification and delivery plan

Use fictional accounts/responses for Django tests, browser checks for visible behavior and separate live API evidence. Record outcomes in the build log.

| Criterion ID | Sample input / Setup | Action | Expected result | Verification method |
|---|---|---|---|---|
| AC-01, AC-02, AC-03, AC-04, AC-27, AC-42 | Valid/invalid/anonymous users | Login, direct URLs, logout, welcome | Correct protected/public access | Access tests/browser |
| AC-15, AC-16 | Valid/invalid registration | Register | Automatic login or errors/no account | Form/session tests |
| AC-07, AC-17, AC-28, AC-41 | Popular/details; missing data | Navigate all detail paths | Required fields/navigation/placeholders | View/browser checks |
| AC-08, AC-20, AC-21 | Blank/empty searches or related results | Submit | Helpful validation/empty state | Mocked view tests |
| AC-19, AC-23, AC-36 | Repeated titles/IDs | Select/recommend | Correct ID; original/duplicates excluded | Mocked requests/results |
| AC-24, AC-25, AC-26 | Valid/empty candidates | Random/Try Again | One result or message; repeats allowed | Controlled random tests |
| AC-33, AC-34, AC-35 | Comedy; Comedy/Family; invalid IDs | Browse | A/B; only B; validation errors | Parameter/result tests |
| AC-37, AC-38, AC-39 | Two users save B | Save twice/restart/remove/cross-user attempts/GET changes | Persistent unique private entries; safe removal | Database/CSRF tests; restart |
| AC-40 | API failure; saved title | Open movie features/watchlist | Error without secrets; saved titles visible | Mocked failures |
| AC-43 | Secure TMDb setup | Live popular/search/details/related/ALL-genres | Working responses and correct attribution | Live integration check |

Run Django system/migration/feature checks and record actual results. Sample responses do not prove live access; keep secrets out of evidence.

**December 7 video:** Show welcome/accounts/dashboard (FR-17, FR-08, FR-01, FR-09), search/details/recommendations/posters (FR-10, FR-03, FR-12), ALL genres (FR-16), Surprise Me (FR-11), private saves/removal/persistence (FR-06), an error (FR-04), and logout/protected access. Explain the diagrams and design choices. Supporting tests cover edge cases. Label simulated errors; record timestamps/link. Hosting is not required.

## 11. Decisions, risks, and student explanation

| Decision / Open risk | Reason or response |
|---|---|
| Django/SQLite/TMDb | One Python web project, local persistent watchlists, no maintained movie catalog/custom ranking |
| API access and terms | Confirm credentials, costs, limits, attribution, image use and title storage using [TMDb documentation](https://developer.themoviedb.org/docs/getting-started) before API work |
| Missing/changing information | Confirm rating scale and ALL-genre syntax; use timeouts/placeholders and live AC-43 checks |
| Privacy/timeline | Owner checks, duplicate prevention and two-user tests; authentication first; no added features |
| Review | Confirm compatible Python/Django versions, inspect GitHub diagrams and record instructor feedback |

**Student explanation — draft to personalize:** A search goes from the browser to a Django view, which checks login/input and asks TMDb for movies. A template displays the response. SQLite links each saved movie ID/title to its user's account, so authentication keeps watchlists private. Django's forms, templates and login tools fit a Python course project; SQLite provides persistence without another database service. TMDb supplies movie information instead of a CSV catalog.

Before submitting, personalize this explanation and review the diagrams. API access/terms and instructor review remain open.
